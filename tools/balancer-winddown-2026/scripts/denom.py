"""Section 2 of the gist: BAL supply and the direct BAL lines, at the stated Ethereum blocks."""
from common import *
BAL = "0xba100000625a3754423978a60c9317c58a424e3D"; B80 = "0x5c6Ee304399DBdB9C8Ef030aB642B10820DB8F56"
VAULT = "0xBA12222222228d8Ba445958a75a0704d566BF2C8"; POOLID = "5c6ee304399dbdb9c8ef030ab642b10820db8f56000200000000000000000014"
n = 26005258
L = [("Treasury Safe direct", "0x0EFcCBb9E2C09Ea29551879bd9Da32362b32fc89", 26005258, 3435806.35),
     ("BLabs Fundraise", "0xB129F73f1AFd3A49C701241F374dB17AE63B20Eb", 26005266, 1599054.29),
     ("BLabs Team", "0xCDcEBF1f28678eb4A1478403BA7f34C94F7dDBc5", 26005266, 928041.34),
     ("OpCo", "0x3B8910F378034FD6E103Df958863e5c684072693", 26005266, 408730.39),
     ("BizDev", "0xF3B4829C8B9E2910C2396538F49a12b0c2475a7e", 26005266, 410713.10),
     ("Onchain Ltd", "0x16b0056636Fcc85f92C49cD49a24bc519d4A1941", 26005414, 235321.55),
     ("DAO multisig", "0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f", 26006091, 13974.93),
     ("Collector v2", "0xce88686553686DA562CE7Cea497CE749DA109f9F", 26006091, 2565.31),
     ("Grants", "0xE2c91f3409Ad6d8cE3a2E2eb330790398CB23597", 26006091, 1569.17)]
sup = word(call("ethereum", BAL, "totalSupply()", "", n)) / 1e18
print(f"supply {sup:,.2f} published 72,373,883.13 diff {sup-72373883.13:+.2f}")
for name, a, b, pub in L:
    v = bal("ethereum", BAL, a, b) / 1e18
    print(f"{name:22s} {v:16,.2f} pub {pub:16,.2f} diff {v-pub:+.2f}")
bpt = bal("ethereum", B80, L[0][1], 26005258) / 1e18
ts = word(call("ethereum", B80, "totalSupply()", "", n)) / 1e18
r = call("ethereum", VAULT, "getPoolTokens(bytes32)", POOLID, n)
print("raw words", len(r)); off = word(r, 1); k = word(r, 3) if False else None
h = r[2:]; ntok = int(h[0:0+64], 16) if False else None
w = [int(h[i:i + 64], 16) for i in range(0, len(h), 64)]
print(w[:12])
print("Treasury BPT", bpt, "BPT supply", ts)
save()
