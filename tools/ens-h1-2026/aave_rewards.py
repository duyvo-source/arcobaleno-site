"""Aave incentive rewards accrued to the Endowment, day by day, Jan 1 - Jul 1 2026.
Read: RewardsController.getUserRewards([aEthUSDS, aEthUSDC, aEthDAI], endowment, reward) at each 00:00 UTC block =
rewards accrued and not yet claimed. Daily accrual = change in that number + anything claimed that day (RewardsClaimed,
found 2026-10-29: 27 Feb and 21 Apr, paid in aEthUSDS). Writes data/aave_rewards.json. Rewards in aEthUSDS are worth $1."""
import json, pathlib, sys
import ocrpc
from keccak import selector
HERE = pathlib.Path(__file__).resolve().parent / "data"
D = json.loads((HERE / "daily.json").read_text())
RC = "0x8164Cc65827dcFe994AB23944CBC90e0aa80bFcb"
ENDOW = D["endowment"]
ATOKENS = ["0x32a6268f9Ba3642Dda7892aDd74f1D34469A4259", "0x98C23E9d8f34FEFb1B7BD6a91B7FF122F4e16F5c",
           "0x018008bfb33d285247A21d44E50697654f754e63"]
p = lambda a: a.lower()[2:].rjust(64, "0")
r = ocrpc.Rpc("ethereum", cache_path=str(HERE / "cache-ethereum.json"))


def reward_list(n):
    res = r._post("eth_call", [{"to": RC, "data": "0x" + selector("getRewardsList()")}, hex(n)])
    k = int(res[66:130], 16)
    return ["0x" + res[130 + 64 * i + 24: 130 + 64 * (i + 1)] for i in range(k)]


def unclaimed(reward, n):
    data = ("0x" + selector("getUserRewards(address[],address,address)") + format(0x60, "064x") + p(ENDOW) + p(reward)
            + format(len(ATOKENS), "064x") + "".join(p(a) for a in ATOKENS))
    key = f"call:{RC.lower()}:{data}:{n}"
    if key not in r.cache:
        r.cache[key] = r._post("eth_call", [{"to": RC, "data": data}, hex(n)])
    return int(r.cache[key], 16) / 1e18


rewards = reward_list(D["blocks"][-1])
print("reward tokens:", rewards)
out = {"rewards": rewards, "unclaimed": {}}
for rw in rewards:
    out["unclaimed"][rw] = [unclaimed(rw, n) for n in D["blocks"]]
    r.save()
    u = out["unclaimed"][rw]
    print(rw, "unclaimed Jan1 %.2f  max %.2f  Jul1 %.2f" % (u[0], max(u), u[-1]))
(HERE / "aave_rewards.json").write_text(json.dumps(out))
