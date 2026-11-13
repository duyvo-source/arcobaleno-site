# digitise the 30D MA net APY chart (report p.10) from a 400-dpi crop; prints value per series at checkpoints
import sys, datetime as dt
import numpy as np
from PIL import Image
im = np.array(Image.open(sys.argv[1]).convert('RGB')).astype(int)
# gridlines (px): 9.0%@68 ... 0%@1190 -> linear fit
Y0, Y9 = 1190, 68
def pct(y): return 9.0 * (Y0 - y) / (Y0 - Y9)
# month ticks (px) for the 1st of each month
ticks = {dt.date(2026,4,1):94, dt.date(2026,5,1):305, dt.date(2026,6,1):525, dt.date(2026,7,1):737, dt.date(2026,8,1):957}
def x_of(d):
    ks = sorted(ticks); 
    for a,b in zip(ks,ks[1:]+[None]):
        if b is None or d < b:
            if b is None: a,b = ks[-2],ks[-1]
            return ticks[a] + (ticks[b]-ticks[a]) * (d-a).days/(b-a).days
PAL = {'gauntlet_core':(42,76,179), 'susdc':(170,182,245), 'usdai':(79,203,138), 'syrupusdc':(92,212,242), 'aave_bench':(119,241,116)}
def series_y(x, rgb, tol=20):
    ys=[y for y in range(40,1185) if np.abs(im[y,int(round(x))]-np.array(rgb)).max() <= tol]
    return (sum(ys)/len(ys), len(ys)) if ys else (None,0)
cps=[dt.date(2026,7,1),dt.date(2026,7,15),dt.date(2026,7,31),dt.date(2026,8,15),dt.date(2026,8,25),dt.date(2026,8,28)]
for name,rgb in PAL.items():
    out=[]
    for d in cps:
        y,n=series_y(x_of(d),rgb)
        out.append(f"{d.strftime('%m-%d')}:{'—' if y is None else f'{pct(y):.2f}%'}")
    print(f"{name:14}", '  '.join(out))
