"""The "~190 bps" headline (stablecoins vs the Aave USDC benchmark), rebuilt at 31 Aug 2026 (rule: PREREG.md, Step 2).
Weights: the DAO's balances on 31 Aug from arbdata.com (Entropy's public feed, read 2026-10-22): sUSDC $12.063M, USDai $9.131M,
syrupUSDC $5.906M. Rates: our 30-day rate (method a) at 31 Aug from the share-price series in data/julaug/.
USDai's rate cannot be rebuilt (private terms, confirmed by Entropy), so it is taken at the report's 5.01%.
  python3 headline.py"""
import csv, datetime as dt, pathlib
HERE = pathlib.Path(__file__).resolve().parent
D = dt.date(2026, 8, 31)
def rate(v):
    sv = {dt.date.fromisoformat(r["date"]): float(r["share_value"]) for r in csv.DictReader(open(HERE / "data/julaug" / v / "series.csv"))}
    return (sv[D] / sv[D - dt.timedelta(days=30)] - 1) * 365 / 30 * 100
W = {"sUSDC": 12.063, "USDai": 9.131, "syrupUSDC": 5.906}
R = {"sUSDC": rate("sUSDC"), "syrupUSDC": rate("syrupUSDC"), "USDai": 5.01}
aave = rate("aaveUSDC")
with_usdai = sum(W[k] * R[k] for k in W) / sum(W.values())
without = (W["sUSDC"] * R["sUSDC"] + W["syrupUSDC"] * R["syrupUSDC"]) / (W["sUSDC"] + W["syrupUSDC"])
print(f"30-day rates at {D}: sUSDC {R['sUSDC']:.2f}%  syrupUSDC {R['syrupUSDC']:.2f}%  Aave benchmark {aave:.2f}%  (USDai taken at 5.01%)")
print(f"with USDai:    {with_usdai:.2f}% - {aave:.2f}% = {round((with_usdai - aave) * 100)} bps   (report: ~190)")
print(f"without USDai: {without:.2f}% - {aave:.2f}% = {round((without - aave) * 100)} bps")
