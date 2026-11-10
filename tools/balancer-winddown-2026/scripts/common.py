"""Shared reads for the Balancer inventory check. Standard library + requests, same plumbing as the CoW and ENS rebuilds."""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent / "data"  # bundle layout: outputs and caches live in data/
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))  # ocrpc.py, keccak.py ship next to this file
import ocrpc
from keccak import selector
URLS = {"polygon": "https://polygon.drpc.org", "arbitrum": "https://gateway.tenderly.co/public/arbitrum",
        "ethereum": "https://gateway.tenderly.co/public/mainnet", "gnosis": "https://rpc.gnosischain.com",
        "base": "https://base.drpc.org", "optimism": "https://optimism.drpc.org"}
_rpc = {}

def rpc(chain):
    if chain not in _rpc:
        _rpc[chain] = ocrpc.Rpc(chain, url=URLS[chain], cache_path=str(ROOT / f"cache-{chain}.json"), min_interval=0.2)
    return _rpc[chain]

def pad(a):
    return a.lower()[2:].rjust(64, "0")

def call(chain, to, sig, args="", n=None):
    r = rpc(chain); data = "0x" + selector(sig) + args
    key = f"call:{to.lower()}:{data}:{n}"
    if key not in r.cache:
        try:
            r.cache[key] = r._post("eth_call", [{"to": to, "data": data}, hex(n)])
        except ocrpc.RpcError as e:
            if "gave up" in str(e):
                raise
            r.cache[key] = None
    return r.cache[key]

def word(res, i=0):
    return int(res[2 + 64 * i: 66 + 64 * i], 16) if res and len(res) >= 66 + 64 * i else None

def bal(chain, token, who, n):
    return word(call(chain, token, "balanceOf(address)", pad(who), n))

def native(chain, who, n):
    r = rpc(chain); k = f"ethbal:{who.lower()}:{n}"
    if k not in r.cache:
        r.cache[k] = r._post("eth_getBalance", [who, hex(n)])
    return int(r.cache[k], 16)

def save():
    for r in _rpc.values():
        r.save()
