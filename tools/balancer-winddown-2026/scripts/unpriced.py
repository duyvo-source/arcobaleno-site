"""Value the unpriced tokens from candidates.json. Pool tokens (V2 getPoolId / V3 getPoolTokenInfo) are looked through to their underlying at the
stated block; the underlying is priced at DefiLlama 18 Sep 14:00 UTC. Anything else stays unpriced and is listed, not called zero. Writes ../data/unpriced.json."""
import json, urllib.request, time
from common import *
ts=json.load(open(ROOT/"prices.json"))["ts"]; BL={"ethereum":26005414,"gnosis":48317441,"optimism":157078387,"arbitrum":506515723,"base":51482712,"polygon":94033766}
CH={"ethereum":"ethereum","gnosis":"xdai","optimism":"optimism","arbitrum":"arbitrum","base":"base","polygon":"polygon"}
V2="0xBA12222222228d8Ba445958a75a0704d566BF2C8"; V3="0xbA1333333333a1BA1108E8412f11850A5C319bA9"
d=json.load(open(ROOT/"candidates.json"))
U=[x for x in d if x.get("raw") and x.get("usd") is None and x["token"]!="NATIVE" and x["qty"]<1e12]
print("to value",len(U),"skipped as absurd supply",sum(1 for x in d if x.get("raw") and x.get("usd") is None and x["token"]!="NATIVE" and x["qty"]>=1e12),flush=True)
def words(r):
    h=r[2:]; return [h[i:i+64] for i in range(0,len(h),64)]
def supply(ch,t,n):
    for sig in ("getActualSupply()","totalSupply()"):
        try:
            v=word(call(ch,t,sig,"",n))
            if v: return v
        except Exception: pass
def look(ch,t,n):
    """(tokens, balances, supply) or None"""
    try:
        r=call(ch,t,"getPoolId()","",n)
        if r and len(r)>=66 and int(r,16):
            w=words(call(ch,V2,"getPoolTokens(bytes32)",r[2:66],n))
            nt=int(w[int(w[0],16)//32],16); o=int(w[0],16)//32+1; toks=["0x"+x[24:] for x in w[o:o+nt]]
            o2=int(w[1],16)//32+1; bals=[int(x,16) for x in w[o2:o2+nt]]
            # composable pools hold their own token: drop it
            keep=[i for i,k in enumerate(toks) if k.lower()!=t.lower()]
            return [toks[i] for i in keep],[bals[i] for i in keep],supply(ch,t,n)
    except Exception: pass
    if ch=="gnosis" or ch=="ethereum" or ch=="arbitrum" or ch=="base" or ch=="optimism" or ch=="polygon":
        try:
            r=call(ch,V3,"getPoolTokenInfo(address)",pad(t),n)
            if r and len(r)>2:
                w=words(r); nt=int(w[int(w[0],16)//32],16); o=int(w[0],16)//32+1; toks=["0x"+x[24:] for x in w[o:o+nt]]
                o2=int(w[2],16)//32+1; bals=[int(x,16) for x in w[o2:o2+nt]]
                return toks,bals,supply(ch,t,n)
        except Exception: pass
R=[]; want=set()
for i,x in enumerate(U):
    ch=x["chain"]; n=BL[ch]; l=look(ch,x["token"],n)
    if l and l[2]:
        toks,bals,sup=l; sh=x["raw"]/sup
        x["under"]=[(k,b*sh) for k,b in zip(toks,bals)]; x["share"]=sh
        for k in toks: want.add((ch,k))
    R.append(x)
    if i%50==0: save(); print(i,flush=True)
save()
dec={}
for ch,k in want:
    try:
        v=word(call(ch,k,"decimals()","",BL[ch])); dec[(ch,k)]=18 if v is None else v
    except Exception: dec[(ch,k)]=18
keys=sorted({f"{CH[c]}:{k}" for c,k in want}); P={}
for i in range(0,len(keys),80):
    u=f"https://coins.llama.fi/prices/historical/{ts}/"+",".join(keys[i:i+80])+"?searchWidth=6h"
    try:
        c=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=40))["coins"]
        for k,v in c.items(): P[k.lower()]=(v["price"],v.get("symbol"))
    except Exception as e: print("price err",e)
    time.sleep(.4)
for x in R:
    if "under" not in x: continue
    tot=0; miss=[]; parts=[]
    for k,a in x["under"]:
        p=P.get(f"{CH[x['chain']]}:{k}".lower()); q=a/10**dec[(x["chain"],k)]
        if p: tot+=q*p[0]; parts.append((p[1],q))
        else: miss.append((k,q))
    x["usd_look"]=tot; x["missing"]=miss; x["parts"]=parts
(ROOT/"unpriced.json").write_text(json.dumps(R,default=str))
pools=[x for x in R if "under" in x]; print("done pools",len(pools),"not pools",len(R)-len(pools))
for x in sorted(pools,key=lambda y:-y["usd_look"])[:30]:
    print(f"{x['holder'][:18]:18} {x['chain'][:8]:8} {x['token'][:12]} share {x['share']:.4%} ${x['usd_look']:12,.0f} miss {len(x['missing'])} {[(a,round(b,3)) for a,b in x['parts']][:3]}")
print("total looked-through $",round(sum(x["usd_look"] for x in pools)))
