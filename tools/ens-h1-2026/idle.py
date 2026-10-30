"""April idle cash: yield the Endowment's uninvested USDS, WETH and native ETH would have earned, 17 Apr - 1 May 2026.
Each day's idle balance (00:00 UTC, data/daily.json) x that day's growth in sUSDS (for USDS) and in KPK's ETH Prime vault
(for WETH and native ETH), the vaults the money came from or went back to. Daily balances, so the last day counts in full
though the money went back ~7 hours before the month ended: slightly high, by about one day's rate on the 30 Apr part."""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent / "data"
D = json.loads((HERE / "daily.json").read_text())
days, eth, P = D["days"], D["eth_usd"], D["pos"]
i0, i1 = days.index("2026-04-17"), days.index("2026-05-01")
usds, wethp = P["sUSDS"]["px"], P["KPK_ETH_Prime"]["px"]
tot_usd = tot_eth = 0.0
print(f"{'day':10s} {'idle USDS':>12s} {'idle ETH':>9s} {'USD part':>9s} {'ETH part':>9s}")
for i in range(i0, i1):
    idle_eth = P["WETH"]["units"][i] + D["native_eth"][i]
    u = P["USDS"]["units"][i] * (usds[i + 1] / usds[i] - 1)
    e = idle_eth * (wethp[i + 1] / wethp[i] - 1) * eth[i]
    tot_usd += u; tot_eth += e
    print(f"{days[i]:10s} {P['USDS']['units'][i]:12,.0f} {idle_eth:9,.1f} {u:9,.0f} {e:9,.0f}")
print(f"missed yield: USD ${tot_usd:,.0f} + ETH ${tot_eth:,.0f} = ${tot_usd + tot_eth:,.0f}")
(HERE / "idle.json").write_text(json.dumps({"usd": tot_usd, "eth": tot_eth, "total": tot_usd + tot_eth}, indent=1))
