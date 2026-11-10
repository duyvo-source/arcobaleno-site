"""Rule 1/3: every asset line of gist section 1/4 at the stated block, priced at DefiLlama 18 Sep 2026 14:00 UTC. Writes ../data/assets.json."""
import datetime, json, urllib.request
from common import *
E_ = 26005414; G = 48317441; AB = 506515723; BA = 51482712; PO = 94033766
TS = "0x0EFcCBb9E2C09Ea29551879bd9Da32362b32fc89"; IF = "0x284a37B375e69c8cB30a5633Ee55f3584dd26808"; BD = "0xF3B4829C8B9E2910C2396538F49a12b0c2475a7e"
OC = "0x16b0056636Fcc85f92C49cD49a24bc519d4A1941"; OP = "0x3B8910F378034FD6E103Df958863e5c684072693"; LDOC = "0x884226c9f7b7205f607922E0431419276a64CF8f"
V3 = "0xbA1333333333a1BA1108E8412f11850A5C319bA9"
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"; WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"; USDT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
GHO = "0x40D16FC0246aD3160Ccc09B8D0D3A2cD28aE6C2f"; WSTETH = "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0"; STKAAVE = "0x4da27a545c0c5B758a6BA100e3a049001de870f5"
AAVE = "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"; COW = "0xDEf1CA1fb7FBcDC777520aa7f396b4E015F497aB"; SAFE = "0x5aFE3855358E112B5647B952709E6165e1c1eEEe"
WEETH = "0xCd5fE23C85820F7B72D0926FC9b05b43E359b7ee"; RETH = "0xae78736Cd615f374D3085123A210448E74Fc6393"; HOPR = "0xF5581dFeFD8Fb0e4aeC526bE659CFaB1f8c781dA"
POL = "0x455e53CBB86018Ac2B8092FdCd39d8444aFFC3F6"; LDO = "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32"; WBTC = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"; PAXG = "0x45804880De22913dAFE09f4980848ECE6EcbAf78"
BAL = "0xba100000625a3754423978a60c9317c58a424e3D"
DEC = {USDC: 6, USDT: 6, WBTC: 8}
SYM = {USDC: "USDC", WETH: "WETH", USDT: "USDT", GHO: "GHO", WSTETH: "wstETH", STKAAVE: "stkAAVE", COW: "COW", SAFE: "SAFE", WEETH: "weETH", RETH: "rETH", HOPR: "HOPR", POL: "POL", LDO: "LDO", WBTC: "WBTC", PAXG: "PAXG"}
ts = int(datetime.datetime(2026, 9, 18, 14, tzinfo=datetime.timezone.utc).timestamp())
ids = {SYM[k]: "ethereum:" + k for k in SYM}; ids["AAVE"] = "ethereum:" + AAVE
u = f"https://coins.llama.fi/prices/historical/{ts}/" + ",".join(ids.values()) + "?searchWidth=2h"
pr = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=30))["coins"]
P = {s: next((v["price"] for k, v in pr.items() if k.lower() == i.lower()), None) for s, i in ids.items()}
P["stkAAVE"] = P["stkAAVE"] or P["AAVE"]
(ROOT / "prices.json").write_text(json.dumps(dict(ts=ts, prices=P), indent=1))
print(P)
R = []
def line(bucket, name, chain, qty, sym, pub_q, pub_v, under=False):
    p = P.get(sym); v = qty * p if p else None
    R.append(dict(bucket=bucket, name=name, chain=chain, qty=qty, sym=sym, pub_q=pub_q, pub_v=pub_v, val=v, under=under))
def token(chain, t, who, n, d=18):
    return (bal(chain, t, who, n) or 0) / 10 ** d
def c4626(chain, v, who, n, d):
    sh = bal(chain, v, who, n) or 0
    return word(call(chain, v, "convertToAssets(uint256)", hex(sh)[2:].rjust(64, "0"), n)) / 10 ** d if sh else 0.0
K = "Treasury"
line(K, "kpk USDC Prime V2", "ethereum", c4626("ethereum", "0x4Ef53d2cAa51C447fdFEEedee8F07FD1962C9ee6", TS, E_, 6), "USDC", 1413462.89, 1412793)
line(K, "kpk USDC Yield V2", "ethereum", c4626("ethereum", "0xD5cCe260E7a755DDf0Fb9cdF06443d593AaeaA13", TS, E_, 6), "USDC", 642047.11, 641743)
line(K, "ciUSDCv3", "ethereum", token("ethereum", "0x207158a267CBD2598BB3d611D8CBdEE2709F2F8C", TS, E_, 6), "USDC", 500244.90, 500008)
line(K, "stkAAVE", "ethereum", token("ethereum", STKAAVE, TS, E_), "stkAAVE", 19549.40, 2749911)
line(K, "COW", "ethereum", token("ethereum", COW, TS, E_), "COW", 1230445, 175130)
line(K, "SAFE", "ethereum", token("ethereum", SAFE, TS, E_), "SAFE", 845094, 82627)
line(K, "weETH", "ethereum", token("ethereum", WEETH, TS, E_), "weETH", 350.8384, 988738)
line(K, "rETH", "ethereum", token("ethereum", RETH, TS, E_), "rETH", 62.6945, 187074)
sg = c4626("ethereum", "0xE1753F2e00940cC31213dd92013cF019DFE4ca1d", TS, E_, 18); wg = c4626("ethereum", "0xC71Ea051a5F82c67ADcF634c36FFE6334793D24C", TS, E_, 18)
print("sGHO", sg, "waEthLidoGHO", wg)
line(K, "sGHO + waEthLidoGHO", "ethereum", sg + wg, "GHO", 150704.40, 150458)
st = call("ethereum", "0x97997023aAB1D6b9760538Eb621bF10cfCD84868", "getTotalStake(address)", pad(TS), E_)
line(K, "dPOLc0 stake", "ethereum", word(st) / 1e18 if st else 0, "POL", 106114.23, 10664)
line(K, "HOPR", "ethereum", token("ethereum", HOPR, TS, E_), "HOPR", 617205, 7541)
au = token("ethereum", "0x98C23E9d8f34FEFb1B7BD6a91B7FF122F4e16F5c", TS, E_, 6); cu = token("ethereum", "0xc3d688B66703497DAA19211EEdff47f25384cdc3", TS, E_, 6)
print("aEthUSDC", au, "cUSDCv3", cu)
line(K, "aEthUSDC+cUSDCv3", "ethereum", au + cu, "USDC", 4828.59, 4828)
BPT = "0x5c6Ee304399DBdB9C8Ef030aB642B10820DB8F56"; VE = "0xC128a9954e6c874eA3d62ce62B468bA073093F25"; VAULT2 = "0xBA12222222228d8Ba445958a75a0704d566BF2C8"
POOLID = "5c6ee304399dbdb9c8ef030ab642b10820db8f56000200000000000000000014"
n0 = 26005258
b_wall = (bal("ethereum", BPT, TS, n0) or 0) / 1e18; lk = call("ethereum", VE, "locked(address)", pad(TS), n0); b_ve = (word(lk) or 0) / 1e18
r = call("ethereum", VAULT2, "getPoolTokens(bytes32)", POOLID, n0); h = r[2:]; w = [int(h[i:i + 64], 16) for i in range(0, len(h), 64)]
# (tokens offset, balances offset, lastChangeBlock, ntok, t0, t1, nbal, b0, b1)
bal_pool, weth_pool = w[7] / 1e18, w[8] / 1e18; ts_b = word(call("ethereum", BPT, "totalSupply()", "", n0)) / 1e18
tsa = word(call("ethereum", BPT, "getActualSupply()", "", n0)); ts_a = tsa / 1e18 if tsa else ts_b
print(f"BPT wallet {b_wall} veBAL {b_ve} pool BAL {bal_pool} WETH {weth_pool} supply {ts_b} actual {ts_a} BALperBPT {bal_pool/ts_a}")
bp = b_wall + b_ve
line(K, "BPT WETH leg", "ethereum", bp * weth_pool / ts_a, "WETH", 1.2531, 3193)
line(K, "sDAI", "gnosis", c4626("gnosis", "0xaf204776c7245bF4147c2612BF6e5972Ee483701", TS, G, 18), "USDC", 2213652.08, 2213250)
# buffers: owner shares / total shares of (underlying + wrapped converted)
K = "Buffers"
WR = {"WETH": ("0x0FE906e030a44eF24CA8c7dC7B7c53A6C4F00ce9", 18, 67.8999, 173004), "USDT": ("0x7Bc3485026Ac48b6cf9BaF0A377477Fff5703Af8", 6, 51695.4652, 51656),
      "GHO": ("0xC71Ea051a5F82c67ADcF634c36FFE6334793D24C", 18, 50491.1716, 50409), "wstETH": ("0x775F661b0bD1739349b9A2A3EF60be277c5d2D29", 18, 22.2825, 70818),
      "USDC": ("0xD4fa2D31b7968E448877f69A96DE69f5de8cD23E", 6, 51845.8910, 51821)}
for s, (wt, d, pq, pv) in WR.items():
    os_ = word(call("ethereum", V3, "getBufferOwnerShares(address,address)", pad(wt) + pad(TS), E_)) or 0
    tot = word(call("ethereum", V3, "getBufferTotalShares(address)", pad(wt), E_)) or 0
    bb = call("ethereum", V3, "getBufferBalance(address)", pad(wt), E_); und = word(bb, 0) or 0; wr = word(bb, 1) or 0
    wu = word(call("ethereum", wt, "convertToAssets(uint256)", hex(wr)[2:].rjust(64, "0"), E_)) or 0 if wr else 0
    q = (und + wu) * os_ / tot / 10 ** d if tot else 0
    print(s, "buffer shares", os_, "/", tot, "und", und, "wrap", wr)
    line(K, f"buffer {s}", "ethereum", q, s, pq, pv)
    wb = bal("ethereum", wt, TS, E_) or 0
    if wb: print("  wrapped in wallet at block", s, wb)
# Innovation fund
K = "Innovation"
def v3pool(chain, pool, who, n):
    bp_ = bal(chain, pool, who, n) or 0; sup = word(call(chain, pool, "totalSupply()", "", n))
    r = call(chain, V3, "getPoolTokenInfo(address)", pad(pool), n); h = r[2:]; w = [h[i:i + 64] for i in range(0, len(h), 64)]
    n_t = int(w[int(w[0], 16) // 32], 16); toks = ["0x" + x[24:] for x in w[int(w[0], 16) // 32 + 1:][:n_t]]
    off = int(w[2], 16) // 32; bals = [int(x, 16) for x in w[off + 1:off + 1 + n_t]]
    return toks, [b * bp_ / sup for b in bals], bp_ / sup
for nm, pool, ch, n, pv in [("AutoRange C (eth)", "0x84f2195dC84d540a3AB92e659603D770014F0440", "ethereum", E_, 42228), ("AutoRange (eth)", "0xaA8A8A383FFfcc4f370E1840b38766211fDdb9E3", "ethereum", E_, 42172),
                            ("AutoRange (base)", "0x3Aa14db771113B8707ea0F3D9a591B543045a8b6", "base", BA, 41943), ("BTFSH", "0x6B61D8680C4F9E560c8306807908553f95c749C5", "ethereum", E_, 18833)]:
    try:
        tk, am, sh = v3pool(ch, pool, IF, n); print(nm, tk, am, sh)
        R.append(dict(bucket=K, name=nm, chain=ch, tokens=tk, raw=am, share=sh, pub_v=pv))
    except Exception as e:
        print("POOL FAIL", nm, ch, e); R.append(dict(bucket=K, name=nm, chain=ch, fail=str(e), pub_v=pv))
line(K, "wallet WETH", "ethereum", token("ethereum", WETH, IF, E_), "WETH", 1.0469, None)
line(K, "wallet USDC", "ethereum", token("ethereum", USDC, IF, E_, 6), "USDC", 1162.65, None)
line(K, "wallet USDC base", "base", token("base", "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", IF, BA, 6), "USDC", 3083.22, 3082)
line("LDO", "LDO", "ethereum", token("ethereum", LDO, LDOC, E_), "LDO", 350515.40, 137709, True)
K = "BizDev"
line(K, "USDC eth", "ethereum", token("ethereum", USDC, BD, E_, 6), "USDC", 22047.28, 22037, True)
pu = token("polygon", "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359", BD, PO, 6); pe = token("polygon", "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174", BD, PO, 6); print("poly usdc", pu, pe)
line(K, "USDC polygon", "polygon", pu + pe, "USDC", 34000.00, 33984, True)
line(K, "POL native", "polygon", native("polygon", BD, PO) / 1e18, "POL", 98942.85, 9943, True)
au_ = token("arbitrum", "0xaf88d065e77c8cC2239327C5EDb3A432268e5831", BD, AB, 6); ae = token("arbitrum", "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8", BD, AB, 6)
line(K, "USDC arbitrum", "arbitrum", au_ + ae, "USDC", 6670.55, 6667, True)
line(K, "USDC base", "base", token("base", "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", BD, BA, 6), "USDC", 1382.00, 1381, True)
line("Onchain", "USDC", "ethereum", token("ethereum", USDC, OC, E_, 6), "USDC", 66094.56, 66152)
line("OpCo", "USDC", "ethereum", token("ethereum", USDC, OP, E_, 6), "USDC", 763246.42, 763010)
save()
(ROOT / "assets.json").write_text(json.dumps(R, indent=1))
print()
for x in R:
    if "qty" in x:
        d = (x["qty"] / x["pub_q"] - 1) * 100 if x["pub_q"] else 0
        dv = f"{x['val'] - x['pub_v']:+10,.0f}" if x.get("val") and x.get("pub_v") else ""
        print(f"{x['bucket'][:9]:9} {x['name'][:22]:22} {x['qty']:16,.4f} pub {x['pub_q']:16,.4f} {d:+8.3f}% val {x['val'] or 0:12,.0f} pub {x['pub_v'] or 0:10,.0f} {dv}")
