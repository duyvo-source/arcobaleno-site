"""Step 1. Daily balances and share prices from the chain, 1 Jan - 1 Jul 2026 (first block at or after 00:00 UTC),
for every USD-stablecoin venue in the CoW DAO treasury and every managed wallet. Writes data/daily.json.
Answers are cached in data/cache-<chain>.json, so a rerun costs nothing."""
import datetime as dt, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import ocrpc
from keccak import selector
HERE = pathlib.Path(__file__).resolve().parent / "data"; HERE.mkdir(exist_ok=True)
WALLETS = ["0x523732d31B4432BcDD4BaaD108f7EBE54AD478b0", "0x616dE58c011F8736fa20c7Ae5352F7f6FB9F0669",
           "0x7F8987D6A8bee31bD7bE80E877732579E2582a28", "0x9009B4411D0e1171cc042b77D7701f46B737Fdb9"]
VENUES = {  # name: (chain, address, priced) — priced = ERC-4626 share price; else 1 share = 1 unit of a ~$1 asset
    "sUSDS":   ("ethereum", "0xa3931d71877C0E7a3148CB7Eb4463524FEc27fbD", True),   # benchmark; balances read too
    "morpho":  ("ethereum", "0x4Ef53d2cAa51C447fdFEEedee8F07FD1962C9ee6", True),
    "syrup":   ("ethereum", "0x80ac24aA929eaF5013f6436cdA2a7ba190f5Cc0b", True),
    "sGHO":    ("ethereum", "0xE1753F2e00940cC31213dd92013cF019DFE4ca1d", True),
    "stkGHO":  ("ethereum", "0x1a88Df1cFe15Af22B3c4c783D4e6F7F9e0C1885d", False),  # rate 1:1; yield = Merkl claims
    "sDAI":    ("gnosis",   "0xaf204776c7245bF4147c2612BF6e5972Ee483701", True),
}
START = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
DAYS = [START + dt.timedelta(days=i) for i in range(182)]  # Jan 1 .. Jul 1 inclusive

def word(res):
    return int(res[2:66], 16) if res and res not in ("0x",) else None

def main():
    rpc = {c: ocrpc.Rpc(c, cache_path=str(HERE / f"cache-{c}.json")) for c in ("ethereum", "gnosis")}
    out = {"days": [d.date().isoformat() for d in DAYS], "blocks": {}, "venues": {}}
    for c, r in rpc.items():
        out["blocks"][c] = [r.block_at(int(d.timestamp())) for d in DAYS]
        r.save()
    sel_bal, sel_px = selector("balanceOf(address)"), selector("convertToAssets(uint256)")
    for name, (chain, addr, priced) in VENUES.items():
        r = rpc[chain]; blocks = out["blocks"][chain]
        dec = word(r.call(addr, "decimals()", blocks[-1]))
        def call(data, n):
            key = f"call:{addr.lower()}:{data}:{n}"
            if key not in r.cache:
                try: r.cache[key] = r._post("eth_call", [{"to": addr, "data": data}, hex(n)])
                except ocrpc.RpcError as e:
                    if "gave up" in str(e): raise
                    r.cache[key] = None
            return r.cache[key]
        px = [word(call("0x" + sel_px + format(10 ** dec, "064x"), n)) if priced else 10 ** dec for n in blocks]
        bal = {}
        for w in WALLETS:
            b = [word(call("0x" + sel_bal + w.lower()[2:].rjust(64, "0"), n)) for n in blocks]
            if any(b): bal[w] = b
        out["venues"][name] = {"chain": chain, "address": addr, "decimals": dec, "price_raw": px, "balance_raw": bal}
        r.save()
        print(name, "wallets holding:", [w[:6] for w in bal], flush=True)
    (HERE / "daily.json").write_text(json.dumps(out))

if __name__ == "__main__":
    main()
