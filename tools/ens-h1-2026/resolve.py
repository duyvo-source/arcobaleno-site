"""Resolve the ENS names KPK's reports use (endowment.ensdao.eth, wallet.ensdao.eth) to addresses, at the latest block.
Registry -> resolver(node) -> addr(node). Hand-encoded calls, same plumbing as the CoW scripts."""
import pathlib, sys
import ocrpc
from keccak import keccak256, selector
REGISTRY = "0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e"

def namehash(name):
    node = b"\x00" * 32
    for label in reversed(name.split(".")):
        node = keccak256(node + keccak256(label.encode()))
    return node.hex()

r = ocrpc.Rpc("ethereum")
for name in sys.argv[1:] or ["endowment.ensdao.eth", "wallet.ensdao.eth"]:
    nh = namehash(name)
    res = r._post("eth_call", [{"to": REGISTRY, "data": "0x" + selector("resolver(bytes32)") + nh}, "latest"])
    resolver = "0x" + res[-40:]
    a = r._post("eth_call", [{"to": resolver, "data": "0x" + selector("addr(bytes32)") + nh}, "latest"])
    print(name, "resolver", resolver, "addr", "0x" + a[-40:])
