"""Mimic fee-processing vaults (Balancer address book, not in the gist): holdings at the stated blocks. Writes ../data/mimic.json."""
import json, time, urllib.request
from common import *
V3="0x9e5D6427D2cdaDC68870197b099C2Df535Ec3c97"; V1="0x94Dd9C6152a2A0BBcB52d3297b723A6F01D5F9f7"; OPV3="0x1D8e78300DB118dcE5d8176c93BeF1D6028d74EB"
BL={"ethereum":26005414,"gnosis":48317441,"optimism":157078387}
HOST={"ethereum":"eth.blockscout.com","gnosis":"gnosis.blockscout.com","optimism":"optimism.blockscout.com"}
def g(u):
    for i in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=25))
        except Exception: time.sleep(2)
R=[]
for ch,h in HOST.items():
    for a in (V3,V1,OPV3):
        seen={}
        d=g(f"https://{h}/api/v2/addresses/{a}/token-balances") or []
        for t in d:
            k=t["token"]
            if k.get("type")=="ERC-20": seen[k.get("address_hash") or k.get("address")]=k
        d=g(f"https://{h}/api/v2/addresses/{a}/token-transfers?type=ERC-20") or {}
        for t in d.get("items",[]): k=t["token"]; seen[k.get("address_hash") or k.get("address")]=k
        print(ch,a[:8],len(seen),flush=True)
        for ta,k in seen.items():
            v=bal(ch,ta,a,BL[ch])
            if v:
                dec=int(k.get("decimals") or 18); q=v/10**dec; r=float(k.get("exchange_rate") or 0)
                R.append(dict(chain=ch,vault=a,sym=k.get("symbol"),token=ta,qty=q,today_rate=r,usd_today_rate=q*r))
MJ={"arbitrum":(506515723,{"BAL":("0x040d1EdC9569d4Bab2D15287Dc5A4F10F56a56B8",18),"USDC":("0xaf88d065e77c8cC2239327C5EDb3A432268e5831",6),"USDC.e":("0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",6),"WETH":("0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",18)}),
"base":(51482712,{"BAL":("0x4158734D47Fc9692176B5085E0F52ee0Da5d47F1",18),"USDC":("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",6),"WETH":("0x4200000000000000000000000000000000000006",18)}),
"polygon":(94033766,{"BAL":("0x9a71012B13CA4d3D0Cdc72A177DF3ef03b0E76A3",18),"USDC":("0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",6),"USDC.e":("0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",6)})}
for ch,(n,tk) in MJ.items():
    for s,(t,dec) in tk.items():
        for a in (V3,V1):
            v=bal(ch,t,a,n)
            if v: R.append(dict(chain=ch,vault=a,sym=s,token=t,qty=v/10**dec,direct=True))
save(); (ROOT/"mimic.json").write_text(json.dumps(R,indent=0))
for r in sorted(R,key=lambda x:-(x.get("usd_today_rate") or 0))[:30]: print(r["chain"][:6],r["vault"][:8],r["sym"],round(r["qty"],4),round(r.get("usd_today_rate") or 0),r.get("direct",""))
