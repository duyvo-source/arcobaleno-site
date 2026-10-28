"""Step 4. USD-sleeve return per month vs the Sky Savings Rate, and KPK's Table 3 beside it.

Return = dollar profit / dollar-days of capital, so money moving mid-month counts only for the days it was there.
Annualised simply (x 365 / days). Deployed capital only, which is the basis KPK states; idle money is not included.
- Share-price venues (sUSDS, Morpho kpk USDC Prime, SyrupUSDC, sGHO, sDAI): profit per day = shares held at the start of
  the day x the day's change in share price (data/daily.json).
- stkGHO: each Merkl claim is spread over the days since the previous claim, in proportion to the stkGHO held each day
  (data/stkgho_logs.json). Pass --claim-basis to book each claim on its day instead (does not match KPK).
- April exits: the sale costs in data/exits.json are booked as losses on the sale day. Pass --no-exits to leave them out.
Assumes GHO, USDC and WXDAI are each worth $1. Not included: MORPHO reward tokens on the Morpho vault, a $0.56M Curve
pool held in January, and a fifth wallet that holds only BAL. Reads only data/; no network."""
import datetime as dt, json, pathlib, sys
DATA = pathlib.Path(__file__).resolve().parent / "data"
D = json.loads((DATA / "daily.json").read_text())
L = json.loads((DATA / "stkgho_logs.json").read_text())
X = json.loads((DATA / "exits.json").read_text())
KPK = [1.03, 0.34, 0.89, 0.20, 0.52, 0.42]  # KPK H1 2026 review, Table 3, USD stablecoins (forum.cow.fi/t/3533)
ADEC = {"sUSDS": 18, "morpho": 6, "syrup": 6, "sGHO": 18, "stkGHO": 18, "sDAI": 18}  # decimals of each venue's asset
STK = "0x1a88df1cfe15af22b3c4c783d4e6f7f9e0c1885d"
CLAIM_BASIS, WITH_EXITS = "--claim-basis" in sys.argv, "--no-exits" not in sys.argv

days = D["days"]; N = len(days) - 1
ts_day = [int(dt.datetime.fromisoformat(d).replace(tzinfo=dt.timezone.utc).timestamp()) for d in days]
day_of = lambda t: max(i for i in range(N) if ts_day[i] <= t)

def series(name):
    v = D["venues"][name]
    px = [p / 10 ** ADEC[name] if p is not None else None for p in v["price_raw"]]
    bal = [sum((b[i] or 0) for b in v["balance_raw"].values()) / 10 ** v["decimals"] for i in range(len(days))]
    return px, bal

pnl, cap = {}, {}
for name in ("sUSDS", "morpho", "syrup", "sGHO", "sDAI"):
    px, bal = series(name)
    pnl[name] = [bal[i] * (px[i + 1] - px[i]) if bal[i] and px[i] is not None else 0.0 for i in range(N)]
    cap[name] = [bal[i] * px[i] if bal[i] and px[i] is not None else 0.0 for i in range(N)]

_, sbal = series("stkGHO")
claims = sorted((c["ts"], c["amount"] / 1e18) for c in L["claimed"] if c["token"].lower() == STK)
prev = max(t for t, _ in claims if t < ts_day[0])           # last claim before 1 Jan
spnl = [0.0] * N
for t, amt in (c for c in claims if c[0] >= ts_day[0]):
    if CLAIM_BASIS:
        spnl[day_of(t)] += amt
    else:
        w = [sbal[i] * max(0, min(t, ts_day[i + 1]) - max(prev, ts_day[i])) for i in range(N)]
        pre = sbal[0] * max(0, min(t, ts_day[0]) - prev)  # share earned before 1 Jan: outside the window, dropped
        tot = sum(w) + pre
        for i in range(N): spnl[i] += amt * w[i] / tot if tot else 0.0
    prev = t
pnl["stkGHO"], cap["stkGHO"] = spnl, sbal[:N]
if WITH_EXITS:
    for x in X: pnl[x["venue"]][day_of(x["ts"])] -= x["cost_usd"]

bpx, _ = series("sUSDS")
print(f"{'month':5s} {'capital $M':>10s} {'sleeve':>7s} {'bench':>6s} {'excess':>7s} {'KPK':>6s}")
rows = []
for m in range(1, 7):
    idx = [i for i in range(N) if int(days[i][5:7]) == m]; nd = len(idx)
    tp = sum(pnl[k][i] for k in pnl for i in idx); tc = sum(cap[k][i] for k in pnl for i in idx)
    sleeve = tp / tc * 365 * 100
    bench = (bpx[idx[-1] + 1] / bpx[idx[0]] - 1) * 365 / nd * 100
    rows.append({"month": f"2026-{m:02d}", "avg_capital_usd": tc / nd, "sleeve_pct": sleeve, "benchmark_pct": bench,
                 "excess_pp": sleeve - bench, "kpk_table3_pp": KPK[m - 1]})
    print(f"2026-{m:02d} {tc/nd/1e6:10.2f} {sleeve:6.2f}% {bench:5.2f}% {sleeve-bench:+6.2f}  {KPK[m-1]:+5.2f}")
avg = lambda k: sum(x[k] for x in rows) / len(rows)
print(f"{'avg':5s} {'':10s} {avg('sleeve_pct'):6.2f}% {avg('benchmark_pct'):5.2f}% {avg('excess_pp'):+6.2f}  {avg('kpk_table3_pp'):+5.2f}")
(DATA / "result.json").write_text(json.dumps({"options": sys.argv[1:], "months": rows}, indent=1))
