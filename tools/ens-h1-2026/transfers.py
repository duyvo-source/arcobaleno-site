"""Every ERC-20 Transfer into or out of the Endowment Safe, 2025-12-01 .. 2026-07-02, from eth_getLogs (chunked).
Writes data/transfers.json: one row per log. This is how the position list is found (not from KPK's tables)."""
import datetime as dt, json, pathlib, sys
import ocrpc
from keccak import keccak256
HERE = pathlib.Path(__file__).resolve().parent / "data"
ENDOW = "0x4f2083f5fbede34c2714affb3105539775f7fe64"
T = "0x" + keccak256(b"Transfer(address,uint256)".replace(b"(address,uint256)", b"(address,address,uint256)")).hex()
pad = "0x" + ENDOW[2:].rjust(64, "0")
r = ocrpc.Rpc("ethereum", cache_path=str(HERE / "cache-ethereum.json"))
logs_rpc = ocrpc.Rpc("ethereum", which=1)  # drpc free plan refuses getLogs ranges (even 4k blocks, 2026-10-29); tenderly takes 100k
b0 = r.block_at(int(dt.datetime(2025, 12, 1, tzinfo=dt.timezone.utc).timestamp()))
b1 = r.block_at(int(dt.datetime(2026, 7, 2, tzinfo=dt.timezone.utc).timestamp()))
r.save()
step = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
rows = []
for side, topics in (("in", [T, None, pad]), ("out", [T, pad])):
    a = b0
    while a <= b1:
        b = min(a + step - 1, b1)
        logs = logs_rpc._post("eth_getLogs", [{"fromBlock": hex(a), "toBlock": hex(b), "topics": topics}])
        for l in logs:
            rows.append({"side": side, "block": int(l["blockNumber"], 16), "token": l["address"].lower(),
                         "from": "0x" + l["topics"][1][-40:], "to": "0x" + l["topics"][2][-40:],
                         "raw": int(l["data"], 16) if l["data"] not in ("0x", "") else 0, "tx": l["transactionHash"]})
        a = b + 1
    print(side, len([x for x in rows if x["side"] == side]), flush=True)
(HERE / "transfers.json").write_text(json.dumps({"blocks": [b0, b1], "rows": rows}))
