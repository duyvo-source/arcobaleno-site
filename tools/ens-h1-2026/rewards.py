"""Reward tokens (COMP, MORPHO, FLUID): claims into the Endowment and their sales, Jan-Jun 2026, from data/transfers.json.
A sale is valued at what came back into the Endowment in the SAME transaction (USDC/USDT/DAI/USDS at $1, WETH at that
day's Chainlink price). Unsold claims are listed in tokens only (not priced: no oracle read here).
KPK books rewards as "realised investment P&L ... claimed and converted"; this shows when and for how much."""
import bisect, json, pathlib
HERE = pathlib.Path(__file__).resolve().parent / "data"
T = json.loads((HERE / "transfers.json").read_text())["rows"]
D = json.loads((HERE / "daily.json").read_text())
REWARD = {"0xc00e94cb662c3520282e6f5717214004a7f26888": "COMP", "0x58d97b57bb95320f9a05dc918aef65434969c2b2": "MORPHO",
          "0x6f40d4a6237c257fff2db00fa0510deeecd303eb": "FLUID"}
STABLE = {"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": 6, "0xdac17f958d2ee523a2206206994597c13d831ec7": 6,
          "0x6b175474e89094c44da98b954eedeac495271d0f": 18, "0xdc035d45d973e3ec169d2276ddab16f1e407384f": 18}
WETH = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
blocks, days, eth = D["blocks"], D["days"], D["eth_usd"]
lo, hi = blocks[0], blocks[-1]


def month(b):
    return int(days[max(0, bisect.bisect_right(blocks, b) - 1)][5:7])


claims, sales = [], []
for x in T:
    if x["token"] not in REWARD or not (lo < x["block"] <= hi):
        continue
    sym = REWARD[x["token"]]
    if x["side"] == "in":
        claims.append((month(x["block"]), sym, x["raw"] / 1e18, x["tx"]))
    else:
        got = 0.0
        for y in T:
            if y["tx"] == x["tx"] and y["side"] == "in":
                if y["token"] in STABLE:
                    got += y["raw"] / 10 ** STABLE[y["token"]]
                elif y["token"] == WETH:
                    got += y["raw"] / 1e18 * eth[max(0, bisect.bisect_right(blocks, y["block"]) - 1)]
        sales.append((month(x["block"]), sym, x["raw"] / 1e18, got, x["tx"]))
print("claims:"); [print(f"  m{m} {s:6s} {q:14,.2f}  {tx[:12]}") for m, s, q, tx in claims]
print("sales:");  [print(f"  m{m} {s:6s} {q:14,.2f} -> ${usd:10,.0f}  {tx[:12]}") for m, s, q, usd, tx in sales]
by_m = {m: sum(u for mm, _, _, u, _ in sales if mm == m) for m in range(1, 7)}
print("sale proceeds by month:", {m: round(v) for m, v in by_m.items()}, "total", round(sum(by_m.values())))
(HERE / "rewards.json").write_text(json.dumps({"claims": claims, "sales": sales, "proceeds_by_month": by_m}, indent=1))
