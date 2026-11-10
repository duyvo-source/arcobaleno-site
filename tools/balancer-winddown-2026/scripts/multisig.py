"""DAO multisig 0x10A19e7e: what it held at the snapshot block, how native ETH got there, who sent the LST inflows."""
import json, time, urllib.request, urllib.parse
from common import *
M="0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f"; E_=26005414
T={"WETH":"0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2","wstETH":"0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0","rETH":"0xae78736Cd615f374D3085123A210448E74Fc6393","weETH":"0xCd5fE23C85820F7B72D0926FC9b05b43E359b7ee","USDe":"0x4c9EDD5852cd905f086C759E8383e09bff1E68B3","osETH":"0xf1C9acDc66974dFB6dEcB12aA385b9cD01190E38"}
print("ETH",native("ethereum",M,E_)/1e18)
for s,a in T.items(): print(s,(bal("ethereum",a,M,E_) or 0)/1e18)
# ETH + WETH + rETH + wstETH through time (roughly 2 weeks apart)
prev=None
for n in range(23600000,26180000,100000):
    e=native("ethereum",M,n)/1e18; w=(bal("ethereum",T["WETH"],M,n) or 0)/1e18; r=(bal("ethereum",T["rETH"],M,n) or 0)/1e18; s=(bal("ethereum",T["wstETH"],M,n) or 0)/1e18
    print(n,round(e,3),round(w,3),round(r,3),round(s,3))
save()
def g(u):
    for i in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=25))
        except Exception: time.sleep(2)
q={};rows=[]
for p in range(40):
    d=g(f"https://eth.blockscout.com/api/v2/addresses/{M}/token-transfers?type=ERC-20"+("&"+urllib.parse.urlencode(q) if q else ""))
    if not d: print("ERR page",p); break
    rows+=d["items"]; q=d.get("next_page_params")
    if not q: break
    time.sleep(.2)
print("transfers",len(rows),rows[-1]["timestamp"] if rows else None)
big=[]
for t in rows:
    k=t["token"]
    if k.get("symbol") not in ("RETH","WETH","WSTETH","WEETH","OSETH","USDE","BAL","COW"): continue
    v=int(t["total"]["value"])/10**int(k["decimals"])
    f=t["from"];to=t["to"]; inb=to["hash"].lower()==M.lower()
    if v>=0.5 or k["symbol"] in("USDE","BAL"):
        big.append(dict(ts=t["timestamp"][:10],sym=k["symbol"],v=v,dir="IN" if inb else "OUT",cp=(f if inb else to)["hash"],name=(f if inb else to).get("name"),tx=t["transaction_hash"]))
(ROOT/"multisig_transfers.json").write_text(json.dumps(big,indent=0))
for b in big[:70]: print(b["ts"],b["sym"],round(b["v"],3),b["dir"],(b["name"] or b["cp"])[:42],b["tx"][:12])
