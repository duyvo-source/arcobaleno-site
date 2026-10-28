"""Plumbing for the on-chain instruments: JSON-RPC reads at past blocks, and block-for-a-date lookup.

Standard library + requests only (no web3): the few contract reads we need are hand-encoded, so
there is no dependency that can change how a number is read.

Endpoint per chain: env ARC_RPC_<CHAIN> (e.g. ARC_RPC_ETHEREUM), else the free public default below.
The default must serve *archive* reads (state at old blocks); `python3 ocrpc.py --probe` checks it.
"""
import json
import os
import sys
import time

import requests

# Free public endpoints that answered archive reads ~600 days back when probed (2026-10-06), primary first.
# The second endpoint is an independent operator, used by --verify-rpc2 to re-read the same blocks.
# Tried and failing then: publicnode (archive needs a token), ankr (key), cloudflare-eth, llamarpc, 1rpc,
# blockpi + blockrazor (pruned), arb1.arbitrum.io + arbitrum.drpc + zan arb (no archive), every BNB Chain
# endpoint tried (pruned or down), avalanche.drpc (no archive).
CHAINS = {
    "ethereum":  {"id": 1,     "rpc": ["https://eth.drpc.org", "https://gateway.tenderly.co/public/mainnet"]},
    "base":      {"id": 8453,  "rpc": ["https://base.drpc.org", "https://mainnet.base.org"]},
    "arbitrum":  {"id": 42161, "rpc": ["https://gateway.tenderly.co/public/arbitrum"]},
    "avalanche": {"id": 43114, "rpc": ["https://api.avax.network/ext/bc/C/rpc", "https://gateway.tenderly.co/public/avalanche"]},
    "berachain": {"id": 80094, "rpc": ["https://berachain.drpc.org", "https://rpc.berachain.com"]},
    "hemi":      {"id": 43111, "rpc": ["https://rpc.hemi.network/rpc", "https://hemi.drpc.org"]},
    "gnosis":    {"id": 100,   "rpc": ["https://rpc.gnosischain.com", "https://gnosis.drpc.org"]},  # archive OK 2026-10-28 (block 40M)
    "bsc":       {"id": 56,    "rpc": []},  # no free archive endpoint found: needs ARC_RPC_BSC (paid; spend decision)
}
CHAIN_ID = {k: v["id"] for k, v in CHAINS.items()}


def endpoint(chain, which=0):
    """URL for a chain: env ARC_RPC_<CHAIN> (primary) / ARC_RPC2_<CHAIN> (second), else the table above."""
    env = os.environ.get(("ARC_RPC_" if which == 0 else "ARC_RPC2_") + chain.upper())
    if env:
        return env
    lst = CHAINS.get(chain, {}).get("rpc", [])
    return lst[which] if len(lst) > which else None


SEL = {  # 4-byte selectors of the read-only calls we use
    "asset()": "38d52e0f",
    "decimals()": "313ce567",
    "symbol()": "95d89b41",
    "totalAssets()": "01e1d114",
    "totalSupply()": "18160ddd",
    "convertToAssets(uint256)": "07a2d13a",
    "supportsInterface(bytes4)": "01ffc9a7",
    "safe()": "186f0354",       # Lagoon: the curator's address (company, not a depositor)
    "version()": "54fd4d50",    # Lagoon implementation version string
}
IFACE = {"7540deposit": 0xce3bbe50, "7540redeem": 0x620ee8e4}  # ERC-7540 async vault interface ids
# selectors and interface ids above checked against a live Lagoon vault and a live Morpho vault, 2026-10-06


class RpcError(Exception):
    pass


class Rpc:
    """One chain's endpoint, with retry/backoff and an on-disk cache of immutable answers.

    Only answers at a fixed block number are cached (the chain's past does not change); 'latest' never is.
    """

    def __init__(self, chain, url=None, cache_path=None, min_interval=0.12, which=0):
        self.chain = chain
        self.url = url or endpoint(chain, which)
        if not self.url:
            raise RpcError(f"no {'second ' if which else ''}RPC endpoint for chain {chain!r}: "
                           f"set ARC_RPC{'2' if which else ''}_{chain.upper()} (no free archive endpoint known)")
        self.cache_path = cache_path
        self.cache = {}
        if cache_path and os.path.exists(cache_path):
            with open(cache_path) as f:
                self.cache = json.load(f)
        self.min_interval = min_interval
        self._last = 0.0
        self.calls = 0
        # one kept-alive connection per endpoint; a bare requests.post per call left unread error
        # responses holding sockets open (CLOSE-WAIT pile-up seen on the 10-06 Ethereum run)
        self.session = requests.Session()

    def save(self):
        if self.cache_path:
            tmp = self.cache_path + ".tmp"
            with open(tmp, "w") as f:
                json.dump(self.cache, f)
            os.replace(tmp, self.cache_path)

    def _post(self, method, params):
        backoff = 1.0
        for attempt in range(9):  # ~4 minutes of patience in total before giving up
            wait = self.min_interval - (time.time() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.time()
            self.calls += 1
            try:
                with self.session.post(self.url, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params},
                                       timeout=30) as r:  # 'with' releases the socket on every path, errors included
                    if r.status_code == 429:
                        # rate-limited: slow down for the rest of the run, not just this call
                        self.min_interval = min(self.min_interval * 2 or 0.25, 2.0)
                        raise RpcError("HTTP 429")
                    if r.status_code >= 500:
                        raise RpcError(f"HTTP {r.status_code}")
                    j = r.json()
            except (requests.RequestException, ValueError, RpcError) as e:
                last = e
                time.sleep(backoff)
                backoff = min(backoff * 2, 60)
                continue
            if "error" in j:
                msg = str(j["error"])
                # rate limits come back as JSON errors on some providers: retry those, fail on the rest
                if any(k in msg.lower() for k in ("rate", "limit", "too many", "timeout")):
                    last = RpcError(msg)
                    self.min_interval = min(self.min_interval * 2 or 0.25, 2.0)
                    time.sleep(backoff)
                    backoff = min(backoff * 2, 60)
                    continue
                raise RpcError(f"{method}: {msg}")
            return j["result"]
        raise RpcError(f"{method}: gave up after retries ({last})")

    def _cached(self, key, method, params):
        if key in self.cache:
            return self.cache[key]
        res = self._post(method, params)
        self.cache[key] = res
        return res

    # --- chain ---
    def head(self):
        return int(self._post("eth_blockNumber", []), 16)

    def block_ts(self, n):
        key = f"ts:{n}"
        if key not in self.cache:  # keep only the timestamp: whole blocks made a year's cache ~70 MB
            res = self._post("eth_getBlockByNumber", [hex(n), False])
            if res is None:
                raise RpcError(f"block {n} not found")
            self.cache[key] = int(res["timestamp"], 16)
        return self.cache[key]

    def has_code(self, addr, n):
        """Is there a contract at addr at block n? (Cached as a yes/no, not the bytecode.)"""
        key = f"code:{addr.lower()}:{n}"
        if key not in self.cache:
            code = self._post("eth_getCode", [addr, hex(n)])
            self.cache[key] = bool(code and code != "0x")
        return self.cache[key]

    def call(self, addr, sig, n, arg=None):
        """eth_call of a read-only function at block n. Returns the raw 32-byte words as hex, or None on revert."""
        if sig == "supportsInterface(bytes4)":
            arg = arg << 224  # bytes4 is left-aligned in its 32-byte word
        data = "0x" + SEL[sig] + (format(arg, "064x") if arg is not None else "")
        key = f"call:{addr.lower()}:{data}:{n}"
        if key in self.cache:
            return self.cache[key]
        try:
            res = self._post("eth_call", [{"to": addr, "data": data}, hex(n)])
        except RpcError as e:
            # a revert is an answer; a network failure is not (and "gave up ... execution timeout" is a failure)
            msg = str(e).lower()
            if "gave up" not in msg and ("revert" in msg or "execution" in msg):
                res = None
            else:
                raise
        self.cache[key] = res
        return res

    def block_at(self, ts, head=None):
        """First block with timestamp >= ts. Interpolation search with a bisection fallback."""
        key = f"blockat:{ts}"
        if key in self.cache:
            return self.cache[key]
        hi = head if head is not None else self.head()
        hi_ts = self.block_ts(hi)
        if hi_ts < ts:
            raise RpcError(f"timestamp {ts} is after the chain head")
        lo, lo_ts = 0, self.block_ts(0)
        if lo_ts >= ts:
            return 0
        # invariant: ts(lo) < ts <= ts(hi). Each round: one interpolated probe, plus a bisection probe
        # if interpolation narrowed the range by less than half (irregular block times).
        while hi - lo > 1:
            width = hi - lo
            for probe in ("interp", "bisect"):
                if hi - lo <= 1:
                    break
                if probe == "interp":
                    g = lo + int((ts - lo_ts) * (hi - lo) / max(hi_ts - lo_ts, 1))
                else:
                    if (hi - lo) * 2 <= width:
                        break
                    g = (lo + hi) // 2
                g = min(max(g, lo + 1), hi - 1)
                g_ts = self.block_ts(g)
                if g_ts >= ts:
                    hi, hi_ts = g, g_ts
                else:
                    lo, lo_ts = g, g_ts
        self.cache[key] = hi
        return hi


def word_int(hexstr, i=0):
    h = hexstr[2:] if hexstr.startswith("0x") else hexstr
    return int(h[64 * i:64 * (i + 1)], 16)


def word_addr(hexstr):
    return "0x" + format(word_int(hexstr), "040x")


def decode_string(hexstr):
    """ABI string, with a fallback for old tokens that return bytes32."""
    h = hexstr[2:] if hexstr.startswith("0x") else hexstr
    try:
        off = int(h[:64], 16)
        ln = int(h[2 * off:2 * off + 64], 16)
        return bytes.fromhex(h[2 * off + 64:2 * off + 64 + 2 * ln]).decode("utf-8", "replace")
    except (ValueError, IndexError):
        return bytes.fromhex(h[:64]).rstrip(b"\0").decode("utf-8", "replace")


if __name__ == "__main__":
    if "--probe" in sys.argv:
        chain = sys.argv[sys.argv.index("--probe") + 1] if len(sys.argv) > sys.argv.index("--probe") + 1 else "ethereum"
        rpc = Rpc(chain)
        h = rpc.head()
        old = max(h - 2_000_000, 1)
        try:
            rpc.call("0x" + "0" * 40, "totalSupply()", old)
            rpc.block_ts(old)
            print(f"{chain}: {rpc.url} OK, head {h}, read at block {old} answered (archive)")
        except RpcError as e:
            print(f"{chain}: {rpc.url} FAILED archive read: {e}")
            sys.exit(1)
