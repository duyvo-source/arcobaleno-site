# CoW DAO treasury, H1 2026: the USD stablecoin result, rebuilt from the chain

Arcobaleno Research · published 28 October 2026 · MIT licence (`LICENSE.txt`)

## What this checks

KPK manages CoW DAO's treasury. Its [H1 2026 review](https://forum.cow.fi/t/kpk-h1-2026-review-for-cow-dao/3533)
says the USD stablecoin part of the treasury beat its benchmark, the Sky Savings Rate, in every month from January to
June (Table 3). Part of KPK's fee depends on that kind of figure: 30% of the return above the benchmark.

These scripts rebuild the USD figure using only public blockchain data: what each managed wallet actually held, day by
day, and how much each holding grew.

## Result

Return above the Sky Savings Rate, in percentage points per year:

| | Jan | Feb | Mar | Apr | May | Jun | Average |
|---|---|---|---|---|---|---|---|
| **Rebuilt from the chain** | +1.04 | +0.68 | +0.62 | +0.22 | +0.63 | +0.49 | **+0.61** |
| KPK, Table 3 | +1.03 | +0.34 | +0.89 | +0.20 | +0.52 | +0.42 | **+0.57** |

**KPK's figures hold up.** January and April match almost exactly. February and March are off in opposite directions,
but they're close when taken together (1.30 here, 1.23 in KPK's table). The most likely reason is how one large reward
payment in early March is split between the two months.

Two things we found along the way:

- **stkGHO's yield came entirely from reward payouts** (Merkl, paid in stkGHO every few weeks), not from the staking
  contract itself. We spread each payout over the days since the previous one. Booking each payout on the day it was
  claimed gives figures that don't match KPK's (`python3 blend.py --claim-basis`).
- **April's lower figure is the cost of the precautionary exits.** On 18 April, GHO and SyrupUSDC were swapped into
  USDC through CoW Swap instead of being redeemed at full value; KPK described these exits and linked both transactions
  in its [rsETH post](https://forum.cow.fi/t/3426). The cost wasn't stated there: it comes to about $13,500 (`exits.py`
  reads both transactions). Without it, April would come out at +1.20 (`python3 blend.py --no-exits`).

## What this does not cover

- Only the USD stablecoin part. ETH and EUR are not rebuilt.
- Only the money that was invested. Idle balances are left out, matching what KPK says it measures.
- MORPHO reward tokens earned on the Morpho vault (small; including them would raise our figure slightly), a $0.56M
  Curve pool held in January, and a fifth wallet that holds only BAL tokens.
- GHO, USDC and xDAI are each counted at exactly $1.
- Returns are annualised the simple way (x 365 / days in the month). KPK doesn't say which convention it uses.

## How to run it

**Download everything:** [cow-h1-2026.tar.gz](../cow-h1-2026.tar.gz)
([sha256](../cow-h1-2026.tar.gz.sha256), [signature](../cow-h1-2026.tar.gz.asc), signed with our
[release key](../arcobaleno-release-pubkey.asc)).

Python 3.10 or later, plus `requests`. No keys needed; it uses free public endpoints.

    ./run_all.sh          # rebuild everything from the chain (about 10 minutes), then print the table
    python3 blend.py      # print the table from the data/ folder shipped here, with no network

| File | What it does |
|---|---|
| [`daily.py`](daily.py) | Holdings of every managed wallet in each venue, plus each venue's share price, every day from 1 Jan to 1 Jul (Ethereum and Gnosis) |
| [`logs_stkgho.py`](logs_stkgho.py) | Every stkGHO reward claim by the wallet, and stkGHO moving in and out |
| [`exits.py`](exits.py) | The cost of the two 18 April sales, read from their transactions |
| [`blend.py`](blend.py) | Monthly return over invested money, minus the Sky Savings Rate (sUSDS) over the same days, with KPK's table beside it |
| [`ocrpc.py`](ocrpc.py), [`keccak.py`](keccak.py) | Reading the chain, with no other libraries |
| `data/`: [daily](data/daily.json), [stkGHO claims](data/stkgho_logs.json), [exits](data/exits.json), [result](data/result.json) | What the first three scripts wrote on 28 October 2026, so `blend.py` can run offline |

**Addresses:** wallets `0x523732d31B4432BcDD4BaaD108f7EBE54AD478b0`, `0x616dE58c011F8736fa20c7Ae5352F7f6FB9F0669`,
`0x7F8987D6A8bee31bD7bE80E877732579E2582a28`, `0x9009B4411D0e1171cc042b77D7701f46B737Fdb9` (from KPK's public
dashboard). The venues and their contract addresses are listed at the top of `daily.py`.

## Who we are

Arcobaleno Research checks investment numbers independently: https://arcobaleno.cloud. We don't work for KPK or for
CoW DAO. In early October we sent KPK a LinkedIn note about our service; nothing came of it. Questions or corrections:
dvt@arcobaleno.cloud.
