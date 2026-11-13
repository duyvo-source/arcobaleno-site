"""Score September per Step 2b (TEARDOWN_ARBITRUM_2026-10-23.md): same rule as score_lines.py, checkpoints 09-15 and 09-28,
08-25 re-read as a check only. Reported values: reported_apy_q3_vector.txt (from extract_q3_chart.py).
  python3 score_sep.py <sep series.csv> <line name in reported_apy_q3_vector.txt> [<Jul-Aug series.csv>]
The optional Jul-Aug series supplies late July (needed only for the 08-25 reading check); overlapping days must agree."""
import csv, sys, datetime as dt, os
def load(f): return {dt.date.fromisoformat(r["date"]): float(r["share_value"]) for r in csv.DictReader(open(f))}
sv = load(sys.argv[1])
if len(sys.argv) > 3:
    old = load(sys.argv[3]); both = sorted(set(old) & set(sv))
    worst = max(abs(old[d] / sv[d] - 1) for d in both)
    print(f"overlap with the Jul-Aug run: {len(both)} days, largest relative difference {worst:.2e}")
    assert worst < 1e-9, "the two runs disagree"
    sv = {**old, **sv}
def a_simple(d):
    p = d - dt.timedelta(days=30)
    return (sv[d] / sv[p] - 1) * 365 / 30 * 100 if d in sv and p in sv else None
def b_avg(d):
    rs = []
    for k in range(30):
        t, p = d - dt.timedelta(days=k), d - dt.timedelta(days=k + 1)
        if t not in sv or p not in sv: return None
        rs.append((sv[t] / sv[p] - 1) * 365)
    return sum(rs) / 30 * 100
here = os.path.dirname(os.path.abspath(__file__))
lines = open(os.path.join(here, "reported_apy_q3_vector.txt")).read().splitlines()
head = lines[0].split()[1:-2]
rep = {}
for line in lines[1:]:
    parts = line.split()
    if parts and parts[0] == sys.argv[2]:
        for h, v in zip(head, parts[1:1 + len(head)]):
            if v != "—": rep[dt.date(2026, int(h[:2]), int(h[3:]))] = float(v)
CPS = [dt.date(2026, 9, 15), dt.date(2026, 9, 28)]
SHOW = [dt.date(2026, 8, 25)] + CPS
print(f"{'date':10} {'reported':>8} | {'(a) 30d':>8} {'gap':>6} | {'(b) avg':>8} {'gap':>6}")
worst = {"a": [], "b": []}
for d in SHOW:
    if d not in rep: print(d, "not on the chart"); continue
    out = {}
    for name, f in (("a", a_simple), ("b", b_avg)):
        cands = [c for c in (f(d + dt.timedelta(days=k)) for k in range(-2, 3)) if c is not None]
        out[name] = min(cands, key=lambda c: abs(c - rep[d])) if cands else None
        if d in CPS and out[name] is not None: worst[name].append(abs(out[name] - rep[d]))
    tag = "" if d in CPS else "  (reading check, not scored)"
    print(f"{d} {rep[d]:7.2f}% | {out['a']:7.2f}% {out['a']-rep[d]:+6.2f} | {out['b']:7.2f}% {out['b']-rep[d]:+6.2f}{tag}")
def verdict(g):
    if len(g) < len(CPS): return "UNCLEAR (missing checkpoints)"
    if all(x <= 0.5 for x in g): return "MATCHES"
    return "DOES-NOT-MATCH candidate" if sum(x > 1.0 for x in g) >= 2 else "UNCLEAR"
order = ["MATCHES", "UNCLEAR", "UNCLEAR (missing checkpoints)", "DOES-NOT-MATCH candidate"]
va, vb = verdict(worst["a"]), verdict(worst["b"])
print(f"\nmethod (a): {va}   method (b): {vb}")
print("VERDICT (closer method, doubt in their favour):", min(va, vb, key=order.index))
