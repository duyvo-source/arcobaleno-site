"""Read the Q3 '26 report's "30D MA Net APY" chart (PDF page index 18, printed p.16) from its VECTOR paths, not pixels.

The chart lines are drawn as vector paths in the PDF, so each line's points can be read exactly; only the axis calibration
is an assumption: gridlines 0%..9% (y = 308.59 .. 108.81, every 1.5%), month ticks at the 1st of Nov '25, Jan, Mar, May,
Jul, Sep '26 (x = 115.11 .. 500.15). Colours matched to the legend swatches. Written 2026-11-10 under Step 2b
(TEARDOWN_ARBITRUM_2026-10-23.md), after that addendum was committed.
Run: python3 extract_q3_chart.py <Q3 report PDF>   (PDF not committed; sha256 3724045d…989121aa)
"""
import datetime as dt, sys
import pymupdf

LEGEND = {(0.333, 0.475, 0.533): "gauntlet_core", (0.11, 0.306, 0.722): "aave_bench", (0.467, 0.945, 0.455): "gauntlet_prime",
          (0.925, 0.988, 0.796): "syrupusdc", (0.0, 0.882, 1.0): "usdai", (0.004, 0.839, 0.561): "kpk", (0.647, 0.757, 1.0): "susdc"}
Y0, Y9 = 308.59, 108.81
TICKS = [(dt.date(2025, 11, 1), 115.11), (dt.date(2026, 1, 1), 192.31), (dt.date(2026, 3, 1), 267.03),
         (dt.date(2026, 5, 1), 344.22), (dt.date(2026, 7, 1), 421.41), (dt.date(2026, 9, 1), 500.15)]


def pct(y): return 9.0 * (Y0 - y) / (Y0 - Y9)


def x_of(d):
    for (a, xa), (b, xb) in zip(TICKS, TICKS[1:]):
        if d < b or b == TICKS[-1][0]:
            return xa + (xb - xa) * (d - a).days / (b - a).days


def date_of(x):
    (a, xa), (b, xb) = TICKS[-2], TICKS[-1]
    return a + dt.timedelta(days=(x - xa) * (b - a).days / (xb - xa))


def lines(page):
    out = {}
    for g in page.get_drawings():
        c = tuple(round(v, 3) for v in (g.get("color") or ()))
        if c in LEGEND and len(g["items"]) > 20:
            pts = []
            for it in g["items"]:
                pts += [it[1], it[-1]] if it[0] in ("l", "c") else []
            out[LEGEND[c]] = sorted({(round(p.x, 3), p.y) for p in pts})
    return out


def at(pts, x):
    """Linear interpolation between the two path points around x; None outside the line."""
    if not pts or x < pts[0][0] - 0.3 or x > pts[-1][0] + 0.3:
        return None
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if x1 <= x <= x2:
            return y1 if x2 == x1 else y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    return pts[0][1] if x < pts[0][0] else pts[-1][1]


if __name__ == "__main__":
    page = pymupdf.open(sys.argv[1])[18]
    L = lines(page)
    cps = [dt.date(2026, m, d) for m, d in [(7, 15), (7, 31), (8, 15), (8, 25), (9, 1), (9, 8), (9, 15), (9, 22), (9, 28)]]
    print("line            " + "  ".join(c.strftime("%m-%d") for c in cps) + "   last point")
    for name, pts in L.items():
        vals = [at(pts, x_of(c)) for c in cps]
        last = pts[-1]
        print(f"{name:15} " + "  ".join("  —  " if v is None else f"{pct(v):5.2f}" for v in vals)
              + f"   {date_of(last[0]).isoformat()} {pct(last[1]):.2f}%")
    u = L.get("usdai", [])
    sep = [pct(y) for x, y in u if x >= x_of(dt.date(2026, 9, 1))]
    if sep:
        print(f"usdai in September: {len(sep)} points, min {min(sep):.3f}%, max {max(sep):.3f}%")
