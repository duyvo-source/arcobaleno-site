"""Monthly gross DeFi yield and APY of the ENS Endowment from daily on-chain state (data/daily.json), next to KPK's tables.
Rule: PREREG.md. Yield excludes ETH price moves (as KPK's does) and reward tokens (counted in rewards.py).
APY (a) = KPK's method: month's yield x 12 / month-end NAV.  (b) = yield / dollar-days x 365."""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent / "data"
D = json.loads((HERE / "daily.json").read_text())
T = json.loads((HERE / "transfers.json").read_text())["rows"]
KPK_YIELD = [294337, 201468, 199468, 260335, 229449, 185665]          # H1 review (Dune 8164884)
KPK_FORUM = [280181, 218045, 245822, 209000, 215606, 175236]          # monthly forum updates (Syncrone)
KPK_APY = [3.48, 2.74, 2.66, 3.37, 3.19, 3.29]
KPK_NAV = [101629844, 88300530, 90145206, 92575624, 86253259, 67651393]  # Steakhouse, month-end
BENCH = [2.93, 2.93, 2.71, 2.64, 2.75, 2.81]
days, blocks, eth = D["days"], D["blocks"], D["eth_usd"]
N = len(days) - 1
month_of = [int(d[5:7]) for d in days[:-1]]


def netflow(token, i):
    """Net tokens into the Endowment between day i's block (exclusive) and day i+1's (inclusive)."""
    t = token.lower(); s = 0
    for x in T:
        if x["token"] == t and blocks[i] < x["block"] <= blocks[i + 1]:
            s += x["raw"] if x["side"] == "in" else -x["raw"]
    return s


pnl, cap = {}, {}
for name, p in D["pos"].items():
    u, px, usd = p["units"], p["px"], (lambda i: eth[i]) if p["unit"] == "eth" else (lambda i: 1.0)
    if p["kind"] == "idle":
        pnl[name] = [0.0] * N
    elif p["kind"] == "share":
        pnl[name] = [u[i] * (px[i + 1] - px[i]) * usd(i) if u[i] and px[i] is not None and px[i + 1] is not None else 0.0
                     for i in range(N)]
    else:  # rebase: change in balance minus net transfers (raw -> units with the token's decimals)
        dec = {"cUSDCv3": 6}.get(name, 18)
        pnl[name] = [(u[i + 1] - u[i] - netflow(p["token"], i) / 10 ** dec) * usd(i) for i in range(N)]
    cap[name] = [u[i] * (px[i] if px[i] is not None else 0) * usd(i) for i in range(N + 1)]
# Aave incentives (aave_rewards.py): accrued-unclaimed read daily from the RewardsController; accrual = change + claims.
# Claims arrive as aEthUSDS from the rewards vault 0xac14...8fcd; the blend above books them as units, not yield, so
# counting the accrual here does not double count.
AR = json.loads((HERE / "aave_rewards.json").read_text())
au = AR["unclaimed"]["0x32a6268f9ba3642dda7892add74f1d34469a4259"]
claimed = lambda i: sum(x["raw"] for x in T if x["from"] == "0xac140648435d03f784879cd789130f22ef588fcd"
                        and blocks[i] < x["block"] <= blocks[i + 1]) / 1e18
pnl["Aave incentives"] = [au[i + 1] - au[i] + claimed(i) for i in range(N)]
cap["Aave incentives"] = [0.0] * (N + 1)  # accrued rewards are not capital until claimed
# COMP / MORPHO / FLUID: cash basis, at the sale proceeds in the month sold (rewards.py)
RW = json.loads((HERE / "rewards.json").read_text())["proceeds_by_month"]
cap["native ETH"] = [D["native_eth"][i] * eth[i] for i in range(N + 1)]
pnl["native ETH"] = [0.0] * N

print(f"{'mon':3s} {'NAV ours':>12s} {'NAV KPK':>12s} {'cov':>6s} {'yield ours':>11s} {'KPK H1':>9s} {'forum':>9s}"
      f" {'APY(a)':>7s} {'KPK':>5s} {'diff':>6s} {'APY(b)':>7s} {'bench':>6s}")
rows = []
for m in range(1, 7):
    idx = [i for i in range(N) if month_of[i] == m]; end = idx[-1] + 1; nd = len(idx)
    nav_end = sum(c[end] for c in cap.values())
    y = sum(pnl[k][i] for k in pnl for i in idx) + RW[str(m)]
    dd = sum(cap[k][i] for k in cap for i in idx)
    a = y * 12 / nav_end * 100; b = y / dd * 365 * 100
    cov = nav_end / KPK_NAV[m - 1]
    rows.append({"month": m, "nav_end": nav_end, "coverage": cov, "yield": y, "apy_kpk_method": a, "apy_daily": b,
                 "kpk_yield": KPK_YIELD[m - 1], "kpk_forum": KPK_FORUM[m - 1], "kpk_apy": KPK_APY[m - 1],
                 "by_position": {**{k: sum(pnl[k][i] for i in idx) for k in pnl if any(pnl[k][i] for i in idx)},
                                 "COMP/MORPHO/FLUID sold": RW[str(m)]}})
    print(f"{m:<3d} {nav_end:12,.0f} {KPK_NAV[m-1]:12,.0f} {cov:6.1%} {y:11,.0f} {KPK_YIELD[m-1]:9,d} {KPK_FORUM[m-1]:9,d}"
          f" {a:6.2f}% {KPK_APY[m-1]:4.2f} {a-KPK_APY[m-1]:+6.2f} {b:6.2f}% {BENCH[m-1]:5.2f}")
ty = sum(r["yield"] for r in rows)
print(f"H1 yield ours {ty:,.0f}  vs KPK H1 {sum(KPK_YIELD):,}  ({ty/sum(KPK_YIELD)-1:+.1%})  vs forum {sum(KPK_FORUM):,} ({ty/sum(KPK_FORUM)-1:+.1%})")
print("avg APY(a) %.2f vs KPK 3.12 ; avg APY(b) %.2f" % (sum(r["apy_kpk_method"] for r in rows) / 6, sum(r["apy_daily"] for r in rows) / 6))
print("\nby position, USD yield per month:")
names = sorted({k for r in rows for k in r["by_position"]})
for k in names:
    print(f"  {k:18s} " + " ".join(f"{r['by_position'].get(k, 0):10,.0f}" for r in rows))
(HERE / "blend.json").write_text(json.dumps(rows, indent=1))
