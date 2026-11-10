"""Does any BAL move between DAO addresses inside the read window 26,005,258-26,006,274? Also LDO outflows and the Amber loan."""
import json, time, urllib.request, urllib.parse, datetime
from common import *
BAL="0xba100000625a3754423978a60c9317c58a424e3D"; LDO="0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32"
def g(u):
    for i in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=25))
        except Exception: time.sleep(2)
def transfers(a,token,maxp=30):
    q={};rows=[]
    for p in range(maxp):
        d=g(f"https://eth.blockscout.com/api/v2/addresses/{a}/token-transfers?type=ERC-20&token={token}"+("&"+urllib.parse.urlencode(q) if q else ""))
        if not d: print("ERR",a,p); break
        rows+=d["items"]; q=d.get("next_page_params")
        if not q: break
        time.sleep(.2)
    return rows
A={"Treasury":"0x0EFcCBb9E2C09Ea29551879bd9Da32362b32fc89","BLabs Fundraise":"0xB129F73f1AFd3A49C701241F374dB17AE63B20Eb","BLabs Team":"0xCDcEBF1f28678eb4A1478403BA7f34C94F7dDBc5","OpCo":"0x3B8910F378034FD6E103Df958863e5c684072693","BizDev":"0xF3B4829C8B9E2910C2396538F49a12b0c2475a7e","Onchain":"0x16b0056636Fcc85f92C49cD49a24bc519d4A1941","DAO multisig":"0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f","Collector":"0xce88686553686DA562CE7Cea497CE749DA109f9F","Grants":"0xE2c91f3409Ad6d8cE3a2E2eb330790398CB23597"}
print("BAL at both ends of the window")
for k,a in A.items():
    x=bal("ethereum",BAL,a,26005258)/1e18; y=bal("ethereum",BAL,a,26006274)/1e18; z=bal("ethereum",BAL,a,26005000)/1e18
    print(f"{k:16} 26005000 {z:16,.2f} 26005258 {x:16,.2f} 26006274 {y:16,.2f} chg {y-x:+,.2f}")
allr={}
for k,a in A.items():
    if k=="Collector": continue
    for t in transfers(a,BAL):
        if t["timestamp"]>="2026-05-25": allr[t["transaction_hash"]+str(t.get("log_index"))]=t
rows=sorted(allr.values(),key=lambda t:t["block_number"])
print("BAL transfers touching DAO addresses since 25 May")
for t in rows:
    print(t["timestamp"][:16],t["block_number"],round(int(t["total"]["value"])/1e18,2),(t["from"].get("name") or t["from"]["hash"])[:30],t["from"]["hash"][:8],"->",(t["to"].get("name") or t["to"]["hash"])[:30],t["to"]["hash"][:8],t["transaction_hash"][:12])
print("OpCo all-time BAL")
for t in transfers(A["OpCo"],BAL):
    print(t["timestamp"][:10],round(int(t["total"]["value"])/1e18,2),t["from"]["hash"],"->",t["to"]["hash"],t["transaction_hash"][:12])
print("LDO MerkleRedeem")
M="0x884226c9f7b7205f607922E0431419276a64CF8f"
for t in transfers(M,LDO)[:14]:
    print(t["timestamp"][:16],t["block_number"],round(int(t["total"]["value"])/1e18,2),t["from"]["hash"][:10],"->",(t["to"].get("name") or t["to"]["hash"])[:24],t.get("method"))
for n in (26005414,26100000,26200000):
    try: print("LDO in contract",n,bal("ethereum",LDO,M,n)/1e18)
    except Exception as e: print(n,e)
save()
