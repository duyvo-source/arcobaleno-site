"""Daily on-chain state of the ENS Endowment Safe, 2026-01-01 .. 2026-07-01 (00:00 UTC blocks). Writes data/daily.json.
Position list = every yield-bearing token in data/transfers.json (found from Transfer logs, not from KPK's tables), plus the
StakeWise Genesis vault (not an ERC-20: read with getShares). Cached (data/cache-ethereum.json): reruns are free.

Three kinds of position, each read so that yield and deposits can't be confused:
  share  - units held x price per unit: ERC-4626 vaults (convertToAssets), LST exchange rates, and Aave aTokens as
           scaledBalanceOf x the pool's normalized income (an aToken's Transfer amount folds in accrued interest, so
           balance-minus-flows would book interest as a deposit).
  rebase - balanceOf already counts yield (stETH, eETH, Compound v3); yield = change in balance minus net transfers.
  idle   - plain balances (USDC, USDT, DAI, USDS, WETH, native ETH): capital that earns nothing.
"""
import datetime as dt, json, pathlib, sys
import ocrpc
from keccak import selector
HERE = pathlib.Path(__file__).resolve().parent / "data"
ENDOW = "0x4F2083f5fBede34C2714aFfb3105539775f7FE64"
EP = ENDOW.lower()[2:].rjust(64, "0")
AAVE_POOL = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"
CHAINLINK_ETH_USD = "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"
USDC, USDT, DAI, USDS, WETH = ("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "0x6B175474E89094C44Da98b954EedeAC495271d0F", "0xdC035D45d973E3EC169d2276DDab16f1E407384F",
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
# name: (kind, token, unit, decimals, how to price one unit) ; unit = what the price is in ("usd" or "eth")
POS = {
    "sUSDS":           ("share", "0xa3931d71877C0E7a3148CB7Eb4463524FEc27fbD", "usd", 18, ("4626",)),
    "KPK_USDC_Prime":  ("share", "0x4Ef53d2cAa51C447fdFEEedee8F07FD1962C9ee6", "usd", 18, ("4626",)),
    "kpk_USDC_Prime2": ("share", "0xe108fbc04852B5df72f9E44d7C29F47e7A993aDd", "usd", 18, ("4626",)),
    "KPK_ETH_Prime":   ("share", "0xBb50A5341368751024ddf33385BA8cf61fE65FF9", "eth", 18, ("4626",)),
    "fUSDC":           ("share", "0x9Fb7b4477576Fe5B32be4C1843aFB1e55F251B33", "usd", 6,  ("4626",)),
    "fUSDT":           ("share", "0x5C20B550819128074FD538Edf79791733ccEdd18", "usd", 6,  ("4626",)),
    "rETH":            ("share", "0xae78736Cd615f374D3085123A210448E74Fc6393", "eth", 18, ("call", "0xae78736Cd615f374D3085123A210448E74Fc6393", "getExchangeRate()")),
    "ETHx":            ("share", "0xA35b1B31Ce002FBF2058D22F30f95D405200A15b", "eth", 18, ("call", "0xcf5EA1b38380f6aF39068375516Daf40Ed70D299", "getExchangeRate()")),
    "weETH":           ("share", "0xCd5fE23C85820F7B72D0926FC9b05b43E359b7ee", "eth", 18, ("call", "0xCd5fE23C85820F7B72D0926FC9b05b43E359b7ee", "getRate()")),
    "StakeWise_Genesis": ("share", "0xAC0F906E433d58FA868F936E8A43230473652885", "eth", 18, ("4626",)),  # balance via getShares
    "aEthUSDS":        ("share", "0x32a6268f9Ba3642Dda7892aDd74f1D34469A4259", "usd", 18, ("aave", USDS)),
    "aEthDAI":         ("share", "0x018008bfb33d285247A21d44E50697654f754e63", "usd", 18, ("aave", DAI)),
    "aEthUSDC":        ("share", "0x98C23E9d8f34FEFb1B7BD6a91B7FF122F4e16F5c", "usd", 6,  ("aave", USDC)),
    "stETH":           ("rebase", "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84", "eth", 18, None),
    "eETH":            ("rebase", "0x35fA164735182de50811E8e2E824cFb9B6118ac2", "eth", 18, None),
    "cUSDSv3":         ("rebase", "0x5D409e56D886231aDAf00c8775665AD0f9897b56", "usd", 18, None),
    "cUSDCv3":         ("rebase", "0xc3d688B66703497DAA19211EEdff47f25384cdc3", "usd", 6,  None),
    "USDC":            ("idle", USDC, "usd", 6, None), "USDT": ("idle", USDT, "usd", 6, None),
    "DAI":             ("idle", DAI, "usd", 18, None), "USDS": ("idle", USDS, "usd", 18, None),
    "WETH":            ("idle", WETH, "eth", 18, None),
}
START = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
DAYS = [START + dt.timedelta(days=i) for i in range(182)]  # Jan 1 .. Jul 1 inclusive


def main():
    r = ocrpc.Rpc("ethereum", cache_path=str(HERE / "cache-ethereum.json"))

    def call(to, data, n):
        key = f"call:{to.lower()}:{data}:{n}"
        if key not in r.cache:
            try:
                r.cache[key] = r._post("eth_call", [{"to": to, "data": data}, hex(n)])
            except ocrpc.RpcError as e:
                if "gave up" in str(e):
                    raise
                r.cache[key] = None  # revert = not deployed yet / no such state: an answer, cached
        return r.cache[key]

    def word(res, i=0):
        return int(res[2 + 64 * i: 66 + 64 * i], 16) if res and len(res) >= 66 + 64 * i else None

    blocks = [r.block_at(int(d.timestamp())) for d in DAYS]
    r.save()
    out = {"days": [d.date().isoformat() for d in DAYS], "blocks": blocks, "endowment": ENDOW, "pos": {}}
    eth = []
    for n in blocks:
        res = call(CHAINLINK_ETH_USD, "0x" + selector("latestRoundData()"), n)
        eth.append(word(res, 1) / 1e8)
    out["eth_usd"] = eth
    out["native_eth"] = []
    for n in blocks:
        k = f"ethbal:{ENDOW.lower()}:{n}"
        if k not in r.cache:
            r.cache[k] = r._post("eth_getBalance", [ENDOW, hex(n)])
        out["native_eth"].append(int(r.cache[k], 16) / 1e18)
    r.save()
    for name, (kind, tok, unit, dec, how) in POS.items():
        units, px = [], []
        for n in blocks:
            if name == "StakeWise_Genesis":
                b = word(call(tok, "0x" + selector("getShares(address)") + EP, n))
            elif how and how[0] == "aave":
                b = word(call(tok, "0x" + selector("scaledBalanceOf(address)") + EP, n))
            else:
                b = word(call(tok, "0x" + selector("balanceOf(address)") + EP, n))
            units.append((b or 0) / 10 ** dec)
            if kind != "share":
                px.append(1.0)
            elif how[0] == "4626":
                p = word(call(tok, "0x" + selector("convertToAssets(uint256)") + format(10 ** dec, "064x"), n))
                px.append(p)  # raw; scaled below once the asset decimals are known
            elif how[0] == "call":
                px.append(word(call(how[1], "0x" + selector(how[2]), n)) / 1e18)
            elif how[0] == "aave":
                px.append(word(call(AAVE_POOL, "0x" + selector("getReserveNormalizedIncome(address)") + how[1].lower()[2:].rjust(64, "0"), n)) / 1e27)
        if kind == "share" and how[0] == "4626":
            res = call(tok, "0x" + selector("asset()"), blocks[-1])
            # no asset(): a native-ETH vault (StakeWise Genesis), assets in wei
            adec = word(call("0x" + res[-40:], "0x" + selector("decimals()"), blocks[-1])) if res else 18
            px = [p / 10 ** adec if p is not None else None for p in px]
        out["pos"][name] = {"kind": kind, "token": tok, "unit": unit, "units": units, "px": px}
        r.save()
        held = sum(1 for u in units if u)
        print(f"{name:18s} days held {held:3d}  first {units[0]:.2f}  last {units[-1]:.2f}", flush=True)
    (HERE / "daily.json").write_text(json.dumps(out))


if __name__ == "__main__":
    main()
