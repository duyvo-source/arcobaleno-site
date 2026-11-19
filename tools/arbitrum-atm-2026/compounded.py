"""Correction of 19 November 2026: the report's "30D MA Net APY" is a compounded rate.

Our 13 November check used the simple yearly rate. This script recomputes every scored line, July to September, with the
compounded 30-day rate the report's word "APY" means, from the same daily share prices in data/, against the same chart
readings (reported_apy_digitised.txt, reported_apy_q3_vector.txt). It also recomputes the ~190 bps headline at 31 August.

    simple      = (S_t / S_t-30 - 1) * 365/30
    compounded  = (S_t / S_t-30) ** (365/30) - 1          S = the vault's share price at 00:00 UTC

Python 3.10 or later, no other packages.
    python3 compounded.py
"""
import csv, datetime as dt, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
D = dt.date


def load(period, v):
    return {D.fromisoformat(r["date"]): float(r["share_value"]) for r in csv.DictReader(open(HERE / "data" / period / v / "series.csv"))}


def simple(s, t): return (s[t] / s[t - dt.timedelta(30)] - 1) * 365 / 30 * 100
def comp(s, t): return ((s[t] / s[t - dt.timedelta(30)]) ** (365 / 30) - 1) * 100


rep = {}
for line in open(HERE / "reported_apy_digitised.txt"):
    m = re.match(r"(\w+)\s+(.*)", line.strip())
    if m:
        pts = re.findall(r"(\d\d-\d\d):([\d.]+)%", m.group(2))
        if pts: rep[m.group(1)] = [(D.fromisoformat("2026-" + a), float(b)) for a, b in pts]
q3 = {}
lines = open(HERE / "reported_apy_q3_vector.txt").read().splitlines()
head = lines[0].split()[1:-2]
for line in lines[1:]:
    p = line.split()
    if len(p) > 3 and p[0] in ("aave_bench", "susdc", "syrupusdc"):
        q3[p[0]] = {D.fromisoformat("2026-" + h): float(x) for h, x in zip(head, p[1:]) if x != "—"}

LINES = [("aave_bench", "aaveUSDC", "Aave USDC (benchmark)"), ("susdc", "sUSDC", "Spark sUSDC"),
         ("syrupusdc", "syrupUSDC", "Maple syrupUSDC"), ("gauntlet_core", "gtUSDCc", "Gauntlet USDC Core")]
print("Report minus ours, in points. Match rule (PREREG.md): every date within 0.5.\n")
print(f"{'line':24} {'date':10} {'report':>7} {'simple':>7} {'gap':>6} {'compounded':>11} {'gap':>6}")
for key, v, lab in LINES:
    s = load("julaug", v)
    rows = [(t, r, s) for t, r in rep[key] if t in s and t - dt.timedelta(30) in s]
    if key in ("aave_bench", "susdc", "syrupusdc"):
        s2 = load("sep", v)
        rows += [(t, q3[key][t], s2) for t in (D(2026, 9, 15), D(2026, 9, 28))]
    for t, r, ss in rows:
        a, c = simple(ss, t), comp(ss, t)
        print(f"{lab:24} {t.isoformat():10} {r:7.2f} {a:7.2f} {r - a:+6.2f} {c:11.2f} {r - c:+6.2f}")
    print()

W = {"sUSDC": 12.063, "USDai": 9.131, "syrupUSDC": 5.906}  # the DAO's balances on 31 Aug (arbdata.com), as in headline.py
H = D(2026, 8, 31)
R = {"sUSDC": comp(load("julaug", "sUSDC"), H), "syrupUSDC": comp(load("julaug", "syrupUSDC"), H), "USDai": 5.01}
aave = comp(load("julaug", "aaveUSDC"), H)
w = sum(W[k] * R[k] for k in W) / sum(W.values())
wo = (W["sUSDC"] * R["sUSDC"] + W["syrupUSDC"] * R["syrupUSDC"]) / (W["sUSDC"] + W["syrupUSDC"])
print(f"Headline at {H}, compounded: sUSDC {R['sUSDC']:.2f}%  syrupUSDC {R['syrupUSDC']:.2f}%  USDai 5.01% (report)  Aave {aave:.2f}%")
print(f"  with USDai:    {round((w - aave) * 100)} bps   (report: ~190)")
print(f"  without USDai: {round((wo - aave) * 100)} bps")
