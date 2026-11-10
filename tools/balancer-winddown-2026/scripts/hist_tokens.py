"""Tokens that moved through each inventory address (Blockscout transfers, newest first, back past 1 Sep 2026): catches tokens held
on 18 Sep but gone from today's list. Discovery only; every balance is re-read from the chain. Writes ../data/hist_tokens.json."""
import json, pathlib, time, urllib.request, urllib.parse
ROOT = pathlib.Path(__file__).resolve().parent.parent / "data"  # bundle layout: outputs and caches live in data/
A = {"Treasury Safe": "0x0EFcCBb9E2C09Ea29551879bd9Da32362b32fc89", "OpCo": "0x3B8910F378034FD6E103Df958863e5c684072693",
     "BizDev": "0xF3B4829C8B9E2910C2396538F49a12b0c2475a7e", "Onchain Ltd": "0x16b0056636Fcc85f92C49cD49a24bc519d4A1941",
     "Innovation Fund": "0x284a37B375e69c8cB30a5633Ee55f3584dd26808", "MerkleRedeem LDO": "0x884226c9f7b7205f607922E0431419276a64CF8f",
     "DAO multisig": "0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f"}
def get(u):
    for i in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=20))
        except Exception as e:
            time.sleep(2)
    return None
out = {}
for name, a in A.items():
    seen = {}; q = {}; pages = 0; oldest = None
    while pages < 25:
        u = f"https://eth.blockscout.com/api/v2/addresses/{a}/token-transfers?type=ERC-20"
        if q: u += "&" + urllib.parse.urlencode(q)
        d = get(u)
        if not d: print("ERR", name, pages); break
        for t in d.get("items", []):
            k = t["token"]; ad = k.get("address_hash") or k.get("address")
            seen.setdefault(ad, dict(sym=k.get("symbol"), dec=k.get("decimals"), n=0, last=t["timestamp"], block=t.get("block_number")))
            seen[ad]["n"] += 1; oldest = t["timestamp"]
        pages += 1
        q = d.get("next_page_params")
        if not q or (oldest and oldest < "2026-08-15"): break
        time.sleep(.2)
    out[name] = dict(oldest=oldest, tokens=seen); print(name, len(seen), oldest, flush=True)
(ROOT / "hist_tokens.json").write_text(json.dumps(out))
