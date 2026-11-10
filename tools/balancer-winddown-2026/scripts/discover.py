"""Every token each inventory address holds, per chain, from Blockscout (token discovery only: balances are re-read from the chain).
Writes ../data/discover.json. Current state, so it shows what is there today, not on 18 September."""
import json, pathlib, time, urllib.request, urllib.error
ROOT = pathlib.Path(__file__).resolve().parent.parent / "data"  # bundle layout: outputs and caches live in data/
HOST = {"ethereum": "eth.blockscout.com", "gnosis": "gnosis.blockscout.com", "arbitrum": "arbitrum.blockscout.com",
        "base": "base.blockscout.com", "polygon": "polygon.blockscout.com", "optimism": "optimism.blockscout.com",
        "zkevm": "zkevm.blockscout.com"}
A = {"Treasury Safe": "0x0EFcCBb9E2C09Ea29551879bd9Da32362b32fc89", "OpCo": "0x3B8910F378034FD6E103Df958863e5c684072693",
     "BizDev": "0xF3B4829C8B9E2910C2396538F49a12b0c2475a7e", "Onchain Ltd": "0x16b0056636Fcc85f92C49cD49a24bc519d4A1941",
     "Innovation Fund": "0x284a37B375e69c8cB30a5633Ee55f3584dd26808", "MerkleRedeem LDO": "0x884226c9f7b7205f607922E0431419276a64CF8f",
     "DAO multisig": "0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f", "Collector v2": "0xce88686553686DA562CE7Cea497CE749DA109f9F",
     "Grants": "0xE2c91f3409Ad6d8cE3a2E2eb330790398CB23597", "BLabs Fundraise": "0xB129F73f1AFd3A49C701241F374dB17AE63B20Eb",
     "BLabs Team": "0xCDcEBF1f28678eb4A1478403BA7f34C94F7dDBc5", "Fee ctrl eth": "0x212F884252792ebaaA811FB0678444b21c7C2879",
     "Fee ctrl arb": "0x4638ab64022927C9bD5947607459D13f57f1551C", "Fee ctrl gno": "0xa7d524046ef89de9F8e4f2d7B029f66cCB738d48",
     "Fee ctrl base": "0x2FF226CD12C80511a641A6101F071d853A4e5363", "maxi_ops eth": "0x166f54F44F271407f24AA1BE415a730035637325",
     "maxi_ops arb": "0x5891b90CE909d4c3540d640d2BdAAF3fD5157EAD", "dao arb": "0xaF23DC5983230E9eEAf93280e312e57539D098D0",
     "dao op": "0x043f9687842771b3dF8852c1E9801DCAeED3f6bc", "lm poly": "0xc38c5f97B34E175FFd35407fc91a937300E33860",
     "lm gno": "0x14969B55a675d13a1700F71A37511bc22D90155a", "lm base": "0x65226673F3D202E0f897C862590d7e1A992B2048",
     "omni base": "0x9ff471F9f98F42E5151C7855fD1b5aa906b1AF7e"}
def get(u):
    for i in range(2):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=12))
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            time.sleep(2)
        except Exception:
            time.sleep(2)
    return "ERR"
out = []
for name, a in A.items():
    for ch, h in HOST.items():
        d = get(f"https://{h}/api/v2/addresses/{a}/token-balances")
        if d in (None, "ERR") or not isinstance(d, list):
            if d == "ERR": print("ERR", name, ch)
            continue
        c = get(f"https://{h}/api/v2/addresses/{a}") or {}
        nat = int(c.get("coin_balance") or 0) / 1e18 if isinstance(c, dict) else 0
        rate = float(c.get("exchange_rate") or 0) if isinstance(c, dict) else 0
        if nat: out.append(dict(holder=name, chain=ch, sym="NATIVE", name="", token=None, qty=nat, usd=nat * rate))
        for t in d:
            k = t.get("token") or {}
            if k.get("type") != "ERC-20": continue
            dec = int(k.get("decimals") or 18); q = int(t["value"]) / 10 ** dec; r = float(k.get("exchange_rate") or 0)
            out.append(dict(holder=name, chain=ch, sym=k.get("symbol"), name=k.get("name"), token=k.get("address_hash") or k.get("address"), qty=q, usd=q * r, volume=k.get("volume_24h"), holders=k.get("holders_count") or k.get("holders")))
        time.sleep(.15)
    (ROOT / "discover.json").write_text(json.dumps(out)); print("done", name, len(out), flush=True)
(ROOT / "discover.json").write_text(json.dumps(out))
print(len(out))
