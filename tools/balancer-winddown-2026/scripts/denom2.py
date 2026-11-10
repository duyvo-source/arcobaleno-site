"""Rest of the denominator (rule 2) and BAL holders seen in the flows but absent from the gist's address list."""
import json, time, urllib.request
from common import *
BAL="0xba100000625a3754423978a60c9317c58a424e3D"; B80="0x5c6Ee304399DBdB9C8Ef030aB642B10820DB8F56"; VE="0xC128a9954e6c874eA3d62ce62B468bA073093F25"; VAULT="0xBA12222222228d8Ba445958a75a0704d566BF2C8"
POOLID="5c6ee304399dbdb9c8ef030ab642b10820db8f56000200000000000000000014"; TS="0x0EFcCBb9E2C09Ea29551879bd9Da32362b32fc89"
def pool(n):
    r=call("ethereum",VAULT,"getPoolTokens(bytes32)",POOLID,n); h=r[2:]; w=[int(h[i:i+64],16) for i in range(0,len(h),64)]
    return w[7]/1e18, word(call("ethereum",B80,"totalSupply()","",n))/1e18
b,s=pool(26005258); rate=b/s; print("BAL per BPT",rate,"pub 5.162033")
print("Treasury BPT content",21827.015932550967*rate,"pub 112,671.77")
b2,s2=pool(25977785); print("at post block",b2,s2,b2/s2,"pub 31,412,036.42 / 6,074,087.19 = 5.171483")
lk=call("ethereum",VE,"locked(address)",pad("0x9cC56Fa7734DA21aC88F6a816aF10C5b898596Ce"),25977785); tb=word(lk)/1e18; print("Tetu BPT",tb,"pub 539,726.48")
print("tetu payment",.5*tb*b2/s2,"pub 1,395,593.07; permalock",tb*rate,"pub 2,786,085.71")
AU="0x616e8BfA43F920657B3497DBf40D6b1A02D4608d"; RA="0x928966752dc0cc0D7babe343Fc2937BA13a5120c"; VP="0xaF52695E1bB01A16D33D7194C28C42b10e0Dbec2"
n=26006274; lock=word(call("ethereum",VE,"locked(address)",pad(VP),n))/1e18; aus=word(call("ethereum",AU,"totalSupply()","",n))/1e18; ras=word(call("ethereum",RA,"totalSupply()","",n))/1e18
rt=(bal("ethereum",RA,TS,n) or 0)/1e18; ag=(bal("gnosis","0x63803B132a59E481920c4c46a981bF45555b0421",TS,48317898) or 0)/1e18
print("Aura lock",lock,"auraBAL sup",aus,"rAURA sup",ras,"T rAURA",rt,"T auraBAL gno",ag)
bpt=ag/aus*.9*lock+rt/ras*.1*lock; print("Aura claim BPT",bpt,"BAL",bpt*rate,"pub 137,679.47")
print("rAURA contract stkAAVE",(bal("ethereum","0x4da27a545c0c5B758a6BA100e3a049001de870f5",RA,26005414) or 0)/1e18,"WETH",(bal("ethereum","0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",RA,26005414) or 0)/1e18)
print("Arbitrum Treasury BAL",(bal("arbitrum","0x040d1EdC9569d4Bab2D15287Dc5A4F10F56a56B8",TS,506515723) or 0)/1e18,"pub 11,530.27")
def g(u):
    for i in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=25))
        except Exception: time.sleep(2)
seen={}
for a in [TS,"0x16b0056636Fcc85f92C49cD49a24bc519d4A1941","0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f"]:
    d=g(f"https://eth.blockscout.com/api/v2/addresses/{a}/token-transfers?type=ERC-20&token={BAL}")
    for t in d["items"]:
        if t["to"]["hash"].lower()==a.lower(): seen[t["from"]["hash"]]=(t["from"].get("name"),t["timestamp"][:10],int(t["total"]["value"])/1e18,t["transaction_hash"])
for k,v in seen.items():
    h=[(bal("ethereum",BAL,k,x) or 0)/1e18 for x in (26005258,26006274,26300000)]
    print(k,v[0],v[1],round(v[2],2),v[3][:14],"BAL at 26005258/26006274/26.3M",[round(x,2) for x in h])
save()
