"""Outliers from assets.py: second WETH buffer, AutoRange block scan, sDAI block, native dust, Base pool lookup. Writes ../data/fixes.json."""
import json, urllib.request
from common import *
from assets_lib import v3pool
TS="0x0EFcCBb9E2C09Ea29551879bd9Da32362b32fc89"; V3="0xbA1333333333a1BA1108E8412f11850A5C319bA9"; IF="0x284a37B375e69c8cB30a5633Ee55f3584dd26808"
E_=26005414; out={}
wt="0x0bfc9d54Fc184518A81162F8fB99c2eACa081202"
os_=word(call("ethereum",V3,"getBufferOwnerShares(address,address)",pad(wt)+pad(TS),E_)) or 0
tot=word(call("ethereum",V3,"getBufferTotalShares(address)",pad(wt),E_)) or 0
bb=call("ethereum",V3,"getBufferBalance(address)",pad(wt),E_); und=word(bb,0) or 0; wr=word(bb,1) or 0
wu=(word(call("ethereum",wt,"convertToAssets(uint256)",hex(wr)[2:].rjust(64,"0"),E_)) or 0) if wr else 0
q=(und+wu)*os_/tot/1e18 if tot else 0
print("waEthWETH buffer",os_/1e18,tot/1e18,und/1e18,wr/1e18,"=>",q); out["weth2"]=q
print("sum WETH buffers",q+27.1957,"pub 67.8999")
# AutoRange at nearby blocks
pools={"C":("0x84f2195dC84d540a3AB92e659603D770014F0440",34231.9362,3.1446),"eth":("0xaA8A8A383FFfcc4f370E1840b38766211fDdb9E3",34213.1349,3.1299)}
for k,(p,pu,pw) in pools.items():
    best=None
    for n in range(26005000,26006400,100):
        t,a,s=v3pool("ethereum",p,IF,n); u,w=a[0]/1e6,a[1]/1e18
        d=abs(u/pu-1)
        if best is None or d<best[0]: best=(d,n,u,w)
    print(k,"closest",best,"pub",pu,pw)
    out[k]=best
# sDAI at candidates
SD="0xaf204776c7245bF4147c2612BF6e5972Ee483701"
for n in [48317441,48317898]:
    sh=bal("gnosis",SD,TS,n); a=word(call("gnosis",SD,"convertToAssets(uint256)",hex(sh)[2:].rjust(64,"0"),n))/1e18
    print("sDAI",n,sh/1e18,a)
sh=bal("gnosis",SD,TS,48317441); print("rate implied by pub",2213652.08/(sh/1e18))
for n in [48317441,48305000,48290000]:
    a=word(call("gnosis",SD,"convertToAssets(uint256)",hex(10**24)[2:].rjust(64,"0"),n)); print(" rate",n,a/1e24)
for nm,a in [("Onchain","0x16b0056636Fcc85f92C49cD49a24bc519d4A1941"),("OpCo","0x3B8910F378034FD6E103Df958863e5c684072693"),("Treasury",TS),("BizDev","0xF3B4829C8B9E2910C2396538F49a12b0c2475a7e"),("Innovation",IF),("DAO multisig","0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f")]:
    print("ETH",nm,native("ethereum",a,E_)/1e18)
save(); (ROOT/"fixes.json").write_text(json.dumps(out))
