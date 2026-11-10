"""Discovery at the stated blocks: every token seen on an inventory address (today's scan + transfer history) + a fixed list of majors on the
chains where the explorer is blocked. Priced at DefiLlama 18 Sep 14:00 UTC. Unpriced tokens are listed as unpriced, not as zero. Writes ../data/candidates.json."""
import json, urllib.request, time
from common import *
ts=json.load(open(ROOT/"prices.json"))["ts"]; BL={"ethereum":26005414,"gnosis":48317441,"optimism":157078387,"arbitrum":506515723,"base":51482712,"polygon":94033766}
CH={"ethereum":"ethereum","gnosis":"xdai","optimism":"optimism","arbitrum":"arbitrum","base":"base","polygon":"polygon"}
d=json.load(open(ROOT/"discover.json")); h=json.load(open(ROOT/"hist_tokens.json"))
from discover_addr import A
pairs=set()
for x in d:
    if x["token"] and (x["usd"]>=1 or x["holder"] in ("Collector v2","Fee ctrl eth","Fee ctrl gno")): pairs.add((x["holder"],x["chain"],x["token"]))
for n,v in h.items():
    for t in v["tokens"]: pairs.add((n,"ethereum",t))
M={"arbitrum":{"USDC":"0xaf88d065e77c8cC2239327C5EDb3A432268e5831","USDC.e":"0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8","USDT":"0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9","DAI":"0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1","WETH":"0x82aF49447D8a07e3bd95BD0d56f35241523fBab1","wstETH":"0x5979D7b546E38E414F7E9822514be443A4800529","rETH":"0xEC70Dcb4A1EFa46b8F2D97C310C9c4790ba5ffA8","ARB":"0x912CE59144191C1204E64559FE8253a0e49E6548","WBTC":"0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f","GHO":"0x7dfF72693f6A4149b17e7C6314655f6A9F7c8B33"},
"base":{"USDC":"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913","USDbC":"0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA","WETH":"0x4200000000000000000000000000000000000006","wstETH":"0xc1CBa3fCea344f92D9239c08C0568f6F2F0ee452","rETH":"0xB6fe221Fe9EeF5aBa221c348bA20A1Bf5e73624c","cbETH":"0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22","DAI":"0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb","AERO":"0x940181a94A35A4569E4529A3CDfB74e38FD98631"},
"polygon":{"USDC":"0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359","USDC.e":"0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174","USDT":"0xc2132D05D31c914a87C6611C10748AEb04B58e8F","DAI":"0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063","WETH":"0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619","WMATIC":"0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270","wstETH":"0x03b54A6e9a984069379fae1a4fC4dBAE93B3bCCD","WBTC":"0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6"}}
for ch,tk in M.items():
    for t in tk.values():
        for n in A: pairs.add((n,ch,t))
pairs=sorted(pairs); print(len(pairs),flush=True)
R=[]
for i,(n,ch,t) in enumerate(pairs):
    try:
        v=bal(ch,t,A[n],BL[ch])
        if v: 
            dd=word(call(ch,t,"decimals()","",BL[ch])); R.append(dict(holder=n,chain=ch,token=t,raw=v,dec=18 if dd is None else dd))
    except Exception as e:
        R.append(dict(holder=n,chain=ch,token=t,err=str(e)[:80]))
    if i%200==0: save(); print(i,flush=True)
for n,a in A.items():
    for ch in BL:
        try:
            v=native(ch,a,BL[ch])
            if v: R.append(dict(holder=n,chain=ch,token="NATIVE",raw=v,dec=18))
        except Exception as e: R.append(dict(holder=n,chain=ch,token="NATIVE",err=str(e)[:80]))
save()
keys=sorted({f"{CH[r['chain']]}:{r['token']}" for r in R if r.get("raw") and r["token"]!="NATIVE"}); P={}
for i in range(0,len(keys),80):
    u=f"https://coins.llama.fi/prices/historical/{ts}/"+",".join(keys[i:i+80])+"?searchWidth=6h"
    try:
        c=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=40))["coins"]
        for k,v in c.items(): P[k.lower()]=(v["price"],v.get("symbol"))
    except Exception as e: print("price err",e)
    time.sleep(.4)
PX=json.load(open(ROOT/"prices.json"))["prices"]; NAT={"ethereum":PX["WETH"],"optimism":PX["WETH"],"arbitrum":PX["WETH"],"base":PX["WETH"],"polygon":PX["POL"],"gnosis":1.0}
for r in R:
    if not r.get("raw"): continue
    q=r["raw"]/10**r["dec"]; r["qty"]=q
    if r["token"]=="NATIVE": r["usd"]=q*NAT[r["chain"]]; r["sym"]="NATIVE"
    else:
        p=P.get(f"{CH[r['chain']]}:{r['token']}".lower())
        r["usd"]=q*p[0] if p else None; r["sym"]=p[1] if p else None
(ROOT/"candidates.json").write_text(json.dumps(R)); print("done",len(R))
