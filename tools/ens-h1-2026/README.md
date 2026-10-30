# ENS Endowment, H1 2026: the yield, rebuilt from the chain

Arcobaleno Research · published 30 October 2026 · MIT licence (`LICENSE.txt`)

## What this checks

KPK manages the ENS Endowment. Its [H1 2026 review](https://discuss.ens.domains/t/kpk-h1-2026-review-for-the-ens-endowment/22358)
reports $1,370,722 of gross yield for January to June, and compares it with the benchmark in the ENS investment policy.

These scripts rebuild that yield using only public blockchain data: what the Endowment's wallet
(`endowment.ensdao.eth`) held, day by day, and how much each holding grew. The test for "does it match" was written and
committed before the first result existed: see [`PREREG.md`](PREREG.md).

## Result

| | Jan | Feb | Mar | Apr | May | Jun | H1 |
|---|---|---|---|---|---|---|---|
| **Gross yield rebuilt from the chain** ($k) | 313.5 | 223.6 | 245.3 | 210.0 | 223.9 | 182.2 | **1,398.7** |
| KPK H1 review ($k) | 294.3 | 201.5 | 199.5 | 260.3 | 229.4 | 185.7 | **1,370.7** |
| KPK monthly forum updates ($k) | 280.2 | 218.0 | 245.8 | 209.0 | 215.6 | 175.2 | **1,343.9** |
| Rebuilt APY, KPK's method | 3.68 | 3.01 | 3.20 | 2.70 | 3.10 | 3.20 | 3.15 |
| Rebuilt APY, on daily balances | 3.17 | 3.16 | 3.14 | 2.67 | 2.87 | 2.87 | 2.98 |
| KPK gross APY | 3.48 | 2.74 | 2.66 | 3.37 | 3.19 | 3.29 | 3.12 |
| Investment policy benchmark | 2.93 | 2.93 | 2.71 | 2.64 | 2.75 | 2.81 | 2.80 |

Against the rule in `PREREG.md`:

- **The half-year yield reproduces:** +2.0% against the review (the rule allows ±5%).
- **The month-by-month figures do not:** 2 of 6 months are within 0.15 points of the review's APY. The gap is mostly March
  and April. KPK's own monthly forum updates do match the chain in those months (March $245.8k, April $209.0k).
- **Coverage is good:** our month-end total is within 100.6% to 102.1% of KPK's in every month, so every month counts.
- Before fees, the yield beat the benchmark in every month on both of our methods. April is the closest (2.67 to 2.70
  against 2.64). The benchmark itself is KPK's published figure: we did not rebuild it.

**April's idle cash.** After the precautionary exits on 18 April, $15.6M of plain USDS and about 3,470 ETH sat uninvested
in the Endowment. On 23 April, $4.9M of the USDS was swapped to USDC and sent to `wallet.ensdao.eth`; on 24 April, 513 ETH
went back to KPK's ETH vault; the rest went back on 30 April, about 7 hours before the month ended. At what sUSDS and that
ETH vault paid over those days, the missed yield comes to about **$36,000** (`python3 idle.py`). That figure depends on the
rates assumed, and it is a little high because the last day counts in full. Exiting was a risk decision, and this does
not say it was wrong.

## What this does not cover

- Only yield. ETH price moves are left out, as in KPK's figures.
- COMP, MORPHO and FLUID rewards are counted when sold, at what the sale brought in ($15,771 for the half). Rewards earned
  but unclaimed on 1 July are not counted.
- ETH-denominated yield is converted to dollars at each day's Chainlink ETH/USD price. Liquid staking yield comes from each
  protocol's exchange rate, not its market price.
- Stablecoins are counted at exactly $1.
- The monthly checks use KPK's method (month's yield × 12 ÷ month-end assets) so they can be compared with the review.
  The daily-balance row is the same yield over the money actually invested each day.
- Fees are not rebuilt.

## How to run it

**Download everything:** [ens-h1-2026.tar.gz](../ens-h1-2026.tar.gz)
([sha256](../ens-h1-2026.tar.gz.sha256), [signature](../ens-h1-2026.tar.gz.asc), signed with our
[release key](../arcobaleno-release-pubkey.asc)).

Python 3.10 or later, plus `requests`. No keys needed; it uses free public endpoints.

    python3 blend.py      # print the table from the data/ folder shipped here, with no network
    python3 idle.py       # print the April idle-cash figure, with no network
    ./run_all.sh          # rebuild everything from the chain (slow on free endpoints), then print both

| File | What it does |
|---|---|
| [`transfers.py`](transfers.py) | Every token transfer in and out of the Endowment. This is how the list of positions was found, rather than from KPK's tables |
| [`daily.py`](daily.py) | Holdings and each position's share price, every day from 1 Jan to 1 Jul |
| [`aave_rewards.py`](aave_rewards.py) | Aave incentives earned, read from Aave's rewards contract |
| [`rewards.py`](rewards.py) | COMP, MORPHO and FLUID claims and sales |
| [`blend.py`](blend.py) | The table above, with KPK's figures beside it |
| [`idle.py`](idle.py) | April's idle cash and the yield missed |
| [`resolve.py`](resolve.py) | Confirms the ENS names point to the addresses used here |
| [`ocrpc.py`](ocrpc.py), [`keccak.py`](keccak.py) | Reading the chain, with no other libraries |
| `data/`: [daily](data/daily.json), [transfers](data/transfers.json), [Aave incentives](data/aave_rewards.json), [rewards](data/rewards.json), [result](data/blend.json), [idle cash](data/idle.json) | What the scripts wrote, so `blend.py` and `idle.py` can run offline |

**Address:** Endowment `0x4F2083f5fBede34C2714aFfb3105539775f7FE64`. The venues and their contract addresses are listed at
the top of `daily.py`.

## Who we are

Arcobaleno Research checks investment numbers independently: https://arcobaleno.cloud. We don't work for KPK or for ENS.
In early October we sent KPK a LinkedIn note about our service; nothing came of it. Questions or corrections:
dvt@arcobaleno.cloud.
