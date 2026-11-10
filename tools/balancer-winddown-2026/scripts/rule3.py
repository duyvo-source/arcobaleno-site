"""Rule 3: rebuild the distributable base from assets.json + fixes.json. Our quantities, DefiLlama 18 Sep 2026 14:00 UTC prices.
Lines we could not read are carried at the published value and marked. No chain reads here. Writes ../data/rule3.json."""
import json, urllib.request, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent / "data"  # bundle layout: outputs and caches live in data/
A = json.load(open(ROOT / "assets.json")); F = json.load(open(ROOT / "fixes.json")); PJ = json.load(open(ROOT / "prices.json")); ts = PJ["ts"]; P = PJ["prices"]
PUB = 9959416
ids = {"DAI": "ethereum:0x6B175474E89094C44Da98b954EedeAC495271d0F", "PAXG": "ethereum:0x45804880De22913dAFE09f4980848ECE6EcbAf78", "WBTC": "ethereum:0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"}
c = json.load(urllib.request.urlopen(urllib.request.Request(f"https://coins.llama.fi/prices/historical/{ts}/" + ",".join(ids.values()) + "?searchWidth=2h", headers={"User-Agent": "Mozilla/5.0"}), timeout=30))["coins"]
for s, i in ids.items(): P[s] = next(v["price"] for k, v in c.items() if k.lower() == i.lower())
DEC = {"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": (6, "USDC"), "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": (18, "WETH"), "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599": (8, "WBTC"), "0x45804880de22913dafe09f4980848ece6ecbaf78": (18, "PAXG")}
rows = []; carried = []; underrev = 0
def add(name, ours, pub, note=""): rows.append(dict(name=name, ours=ours, pub=pub, note=note))
for x in A:
    n = x["name"]
    if x.get("fail") or (x["name"] == "AutoRange (base)"): continue
    if "tokens" in x:
        v = 0
        for t, a in zip(x["tokens"], x["raw"]):
            d, s = DEC[t.lower()] if t.lower() in DEC else (None, None)
            if d is None: raise SystemExit(f"unknown {t}")
            v += a / 10 ** d * P[s]
        add(n, v, x["pub_v"]); continue
    q, s = x["qty"], x["sym"]
    if n == "sDAI": v = q * P["DAI"]
    elif n == "buffer WETH": q += F["weth2"]; v = q * P["WETH"]
    else: v = x["val"]
    if n in ("wallet WETH", "wallet USDC"): pub = {"wallet WETH": 1.0469 * P["WETH"], "wallet USDC": 1162.65 * P["USDC"]}[n]
    else: pub = x["pub_v"]
    add(f"{x['bucket']}: {n}", v, pub, "under review" if x.get("under") else "")
# native ETH read in fixes.py
eth = P["WETH"]
add("Onchain: ETH", 0.035 * eth, 66152 - 66094.56 * P["USDC"], "ETH to 2 decimals as published"); add("OpCo: ETH", 0.05 * eth, 763010 - 763246.42 * P["USDC"], "ETH to 2 decimals as published")
for n, v in [("AutoRange (base)", 41943), ("HYPE on HyperEVM", 3605), ("BizDev RPL/BOLD/ETH dust", 184), ("Aura: rAURA share (only from May 2027)", 20356), ("Aura: auraBAL WETH leg (only from May 2027)", 1313)]:
    carried.append(dict(name=n, pub=v))
apart = [r for r in rows if r["name"].startswith("OpCo")]; rows = [r for r in rows if not r["name"].startswith("OpCo")]  # section 1 shows OpCo and Aura apart from the base
carried_apart = [x for x in carried if x["name"].startswith("Aura")]; carried = [x for x in carried if not x["name"].startswith("Aura")]
print("shown apart: OpCo ours", round(sum(r["ours"] for r in apart)), "pub 763,010; Aura carried", sum(x["pub"] for x in carried_apart))
ours = sum(r["ours"] for r in rows); pubcov = sum(r["pub"] for r in rows); c_ = sum(x["pub"] for x in carried)
tot = ours + c_
print(f"read lines {len(rows)}: ours ${ours:,.0f} published ${pubcov:,.0f} diff {ours - pubcov:+,.0f}")
print(f"carried {len(carried)}: ${c_:,.0f} = {c_ / PUB:.2%}")
print(f"base ours ${tot:,.0f} vs ${PUB:,} = {tot / PUB - 1:+.3%}; published lines recomputed ${pubcov + c_:,.0f}")
for r in sorted(rows, key=lambda r: -abs(r["ours"] - r["pub"]))[:10]: print(f"  {r['name'][:38]:38} {r['ours']:12,.0f} {r['pub']:12,.0f} {r['ours'] - r['pub']:+9,.0f} {r['note']}")
(ROOT / "rule3.json").write_text(json.dumps(dict(rows=rows, carried=carried, ours=tot, pub=PUB, prices=P), indent=1))
