"""Step 3. The cost of the April 2026 precautionary exits.

On 18 April 2026 the wallet sold GHO (just redeemed 1:1 from stkGHO) and SyrupUSDC for USDC through CoW Protocol's
settlement contract instead of redeeming them at full value. Cost = what the tokens were worth (GHO at $1; syrupUSDC at
its share price one block before the sale) minus the USDC received. Both read from the transaction receipts.
Writes data/exits.json."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import ocrpc
from keccak import keccak256, selector
DATA = pathlib.Path(__file__).resolve().parent / "data"; DATA.mkdir(exist_ok=True)
W = "616de58c011f8736fa20c7ae5352f7f6fb9f0669"
GHO, SYRUP, USDC = "0x40d16fc0246ad3160ccc09b8d0d3a2cd28ae6c2f", "0x80ac24aa929eaf5013f6436cda2a7ba190f5cc0b", "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
SALES = [("stkGHO", "0x9737aba8a3c7a358c8e49403322692f6f9fae2b8eb03948e520e58d29b2c1a23", GHO, 18),
         ("syrup",  "0xf8ca5574053364d40c3784ade90c7c6c263ff354212f8ac5b877dde20de463a9", SYRUP, 6)]
T = "0x" + keccak256(b"Transfer(address,address,uint256)").hex()
r = ocrpc.Rpc("ethereum", which=1)
out = []
for venue, tx, token, dec in SALES:
    rc = r._post("eth_getTransactionReceipt", [tx])
    blk = int(rc["blockNumber"], 16)
    sold = got = 0
    for lg in rc["logs"]:
        if lg["topics"][0] != T or len(lg["topics"]) != 3: continue
        frm, to, amt = lg["topics"][1][-40:], lg["topics"][2][-40:], int(lg["data"][:66], 16)
        if lg["address"].lower() == token and frm == W: sold += amt / 10 ** dec
        if lg["address"].lower() == USDC and to == W: got += amt / 1e6
    if token == SYRUP:
        px = int(r._post("eth_call", [{"to": SYRUP, "data": "0x" + selector("convertToAssets(uint256)") + format(10 ** 6, "064x")}, hex(blk - 1)])[2:66], 16) / 1e6
    else:
        px = 1.0
    out.append({"venue": venue, "tx": tx, "block": blk, "ts": r.block_ts(blk), "sold": sold, "price": px,
                "worth_usd": sold * px, "received_usdc": got, "cost_usd": sold * px - got})
    print(f"{venue:7s} sold {sold:,.2f} worth ${sold*px:,.2f}, received {got:,.2f} USDC, cost ${sold*px-got:,.2f}")
(DATA / "exits.json").write_text(json.dumps(out, indent=1))
