"""Step 2. stkGHO rewards for the managed wallet, from event logs.

stkGHO paid nothing through its own staking contract in H1 2026 (reward index unchanged, emission 0). Its yield came as
Merkl rewards, paid in stkGHO and claimed every few weeks. This reads every Merkl claim by the wallet from 1 Dec 2025
(so the last claim before 1 Jan is known) to 1 May 2026, plus stkGHO moving in and out of the wallet.
Writes data/stkgho_logs.json. Uses the second Ethereum endpoint: the first refuses eth_getLogs on its free plan."""
import datetime as dt, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import ocrpc
from keccak import keccak256
DATA = pathlib.Path(__file__).resolve().parent / "data"; DATA.mkdir(exist_ok=True)
W = "0x616dE58c011F8736fa20c7Ae5352F7f6FB9F0669"
STK = "0x1a88Df1cFe15Af22B3c4c783D4e6F7F9e0C1885d"     # Aave stkGHO
MERKL = "0x3Ef3D8bA38EBe18DB133cEc108f4D14CE00Dd9Ae"   # Merkl distributor
T = lambda s: "0x" + keccak256(s.encode()).hex()
pad = lambda a: "0x" + a.lower()[2:].rjust(64, "0")
r = ocrpc.Rpc("ethereum", which=1)
lo = r.block_at(int(dt.datetime(2025, 12, 1, tzinfo=dt.timezone.utc).timestamp()))
hi = r.block_at(int(dt.datetime(2026, 5, 1, tzinfo=dt.timezone.utc).timestamp()))

def logs(addr, topics, step=9000):
    out = []
    for a in range(lo, hi, step):
        out += r._post("eth_getLogs", [{"address": addr, "topics": topics, "fromBlock": hex(a), "toBlock": hex(min(a + step - 1, hi))}])
    return out

transfer = T("Transfer(address,address,uint256)")
res = {"wallet": W, "from_block": lo, "to_block": hi, "claimed": [], "stk_in": [], "stk_out": []}
for lg in logs(MERKL, [T("Claimed(address,address,uint256)"), pad(W)]):
    b = int(lg["blockNumber"], 16)
    res["claimed"].append({"block": b, "ts": r.block_ts(b), "token": "0x" + lg["topics"][2][-40:],
                           "amount": int(lg["data"][:66], 16), "tx": lg["transactionHash"]})
for key, topics in (("stk_in", [transfer, None, pad(W)]), ("stk_out", [transfer, pad(W)])):
    for lg in logs(STK, topics):
        res[key].append({"block": int(lg["blockNumber"], 16), "from": "0x" + lg["topics"][1][-40:], "to": "0x" + lg["topics"][2][-40:],
                         "amount": int(lg["data"][:66], 16), "tx": lg["transactionHash"]})
(DATA / "stkgho_logs.json").write_text(json.dumps(res, indent=1))
print("claims:", len(res["claimed"]), " stkGHO in:", len(res["stk_in"]), " out:", len(res["stk_out"]))
