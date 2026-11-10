import json,urllib.request,re,time,sys
def g(u):
    try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=25))
    except Exception as e: return {"ERR":str(e)}
for a in sys.argv[1:]:
    d=g(f"https://eth.blockscout.com/api/v2/addresses/{a}")
    print(a,d.get("name"),d.get("is_contract"),[x.get("name") for x in (d.get("implementations") or [])])
    o=g(f"https://eth.blockscout.com/api/v2/addresses/{a}/token-transfers?type=ERC-20&token=0xba100000625a3754423978a60c9317c58a424e3D")
    for t in (o.get("items") or [])[:8]: print("  ",t["timestamp"][:10],round(int(t["total"]["value"])/1e18,2),t["from"]["hash"][:12],t["from"].get("name"),"->",t["to"]["hash"][:12],t["to"].get("name"))
    time.sleep(.3)
