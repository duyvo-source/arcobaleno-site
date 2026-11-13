"""Score rebuilt 30-day rates against the read-off report values, per the rule in TEARDOWN_ARBITRUM_2026-10-23.md step 2.
  python3 score_lines.py <series.csv> <line name in reported_apy_digitised.txt>"""
import csv, sys, datetime as dt, os, re
rows = [(dt.date.fromisoformat(r["date"]), float(r["share_value"])) for r in csv.DictReader(open(sys.argv[1]))]
sv = dict(rows)
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
rep = {}
for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "reported_apy_digitised.txt")):
    if line.split()[0] == sys.argv[2]:
        for m in re.finditer(r"(\d\d)-(\d\d):([\d.]+)%", line):
            rep[dt.date(2026, int(m[1]), int(m[2]))] = float(m[3])
CPS = [dt.date(2026, 7, 15), dt.date(2026, 7, 31), dt.date(2026, 8, 15), dt.date(2026, 8, 25)]
print(f"{'date':10} {'reported':>8} | {'(a) 30d':>8} {'gap':>6} | {'(b) avg':>8} {'gap':>6} | (a)/(b) on the day")
worst = {"a": [], "b": []}
for d in sorted(rep):
    out = {}
    for name, f in (("a", a_simple), ("b", b_avg)):
        cands = [f(d + dt.timedelta(days=k)) for k in range(-2, 3)]
        cands = [c for c in cands if c is not None]
        best = min(cands, key=lambda c: abs(c - rep[d])) if cands else None
        out[name] = best
        if d in CPS and best is not None: worst[name].append(abs(best - rep[d]))
    ad, bd = a_simple(d), b_avg(d)
    tag = "" if d in CPS else "  (reading check, not scored)"
    print(f"{d} {rep[d]:7.2f}% | {out['a']:7.2f}% {out['a']-rep[d]:+6.2f} | {out['b']:7.2f}% {out['b']-rep[d]:+6.2f} | {ad:.2f}% / {bd:.2f}%{tag}")
def verdict(g):
    if len(g) < len(CPS): return "UNCLEAR (missing checkpoints)"
    if all(x <= 0.5 for x in g): return "MATCHES"
    return "DOES-NOT-MATCH candidate" if sum(x > 1.0 for x in g) >= 2 else "UNCLEAR"
va, vb = verdict(worst["a"]), verdict(worst["b"])
order = ["MATCHES", "UNCLEAR", "UNCLEAR (missing checkpoints)", "DOES-NOT-MATCH candidate"]
print(f"\nmethod (a): {va}   method (b): {vb}")
print("VERDICT (closer method, doubt in their favour):", min(va, vb, key=order.index))
