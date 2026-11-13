# Arbitrum treasury (ATM), July to September 2026: the stablecoin rates, rebuilt from the chain

Arcobaleno Research · published 13 November 2026 · MIT licence (`LICENSE.txt`)

## What this checks

The Arbitrum Treasury Management council's July & August 2026 report, prepared by Entropy Advisors, gives a 30-day APY for
each stablecoin position (a chart on page 10) and says the stablecoins beat their benchmark by about 190 bps. Entropy's Q3
2026 report carries the same chart through September.

These scripts rebuild those rates from public blockchain data: each vault's share price, read for every day, turned into a
30-day rate. What counts as a match was written down and committed before each rebuild ran: see [`PREREG.md`](PREREG.md).
Our forum post: [t/29627, post 27](https://forum.arbitrum.foundation/t/atm-council-updates/29627/27). The two-page report:
[report-arbitrum-atm-julaug-2026.pdf](../report-arbitrum-atm-julaug-2026.pdf).

## Result: mostly holds

| Position | Report vs our rebuild | Outcome |
|---|---|---|
| Aave USDC on Arbitrum (the benchmark) | within 0.03 points at every date | matches |
| Spark sUSDC | report about 0.06 points higher, steadily | matches |
| Maple syrupUSDC | report about 0.1 points higher; 15 July can't be read off the July & August chart | unclear, on that technicality |
| Morpho Gauntlet USDC Core | in August the report is 0.6 to 0.9 points above our rebuild, Morpho's own figures and Entropy's own balance data, which agree with each other | not reproduced (Entropy: private terms) |
| USDai | exactly 5.01% on every date, April to September | can't be checked (private terms) |
| "~190 bps" above the benchmark | 188 bps with USDai at 5.01%; 150 bps without it | adds up, but about 40 bps rest on USDai |
| September (Q3 report) | benchmark, sUSDC and syrupUSDC match: at most 0.03, about 0.07 and about 0.12 points high | matches |

## What this does not cover

- It checks the rate each product paid. It does not check that the DAO held these amounts (the report gives no wallet
  addresses) or the dollar interest figures.
- The tokenised money-market funds, the ETH positions and the Morpho USDG vaults (from October) are left out.
- On Arbitrum the chain is read through one public endpoint. For Gauntlet Core, Morpho's own share-price data agrees with
  ours exactly (`morpho_api_gtUSDCc_history.json`).
- The report's charts are images (July & August) or drawn shapes (Q3); the reported values are read off them. The Aave line,
  which we can rebuild exactly, is the test of that reading.

## How to run it

Python 3.10 or later, plus `requests`. The chart readers also need `numpy` and `Pillow` (July & August) or `pymupdf` (Q3).
No keys needed.

    python3 score_lines.py data/julaug/gtUSDCc/series.csv gauntlet_core     # July & August, one line at a time
    python3 score_lines.py data/julaug/sUSDC/series.csv susdc
    python3 score_lines.py data/julaug/syrupUSDC/series.csv syrupusdc
    python3 score_lines.py data/julaug/aaveUSDC/series.csv aave_bench
    python3 score_sep.py data/sep/sUSDC/series.csv susdc data/julaug/sUSDC/series.csv   # September
    python3 headline.py                                                     # the ~190 bps

To re-read the chain yourself (a few minutes per vault on free endpoints):

    python3 oc1_vault_return.py --vault 0x7e97fa6893871A2751B5fE961978DCCb2c201E65 --chain arbitrum --start 2026-05-15 --end 2026-09-05 --out data/julaug/gtUSDCc

| File | What it does |
|---|---|
| [`oc1_vault_return.py`](oc1_vault_return.py), [`ocrpc.py`](ocrpc.py) | Reads a vault's share price every day and writes `series.csv` |
| [`score_lines.py`](score_lines.py), [`score_sep.py`](score_sep.py) | Compare our 30-day rates with the report's, under the rule in `PREREG.md` |
| [`headline.py`](headline.py) | The ~190 bps, with and without USDai |
| [`digitize_apy_chart.py`](digitize_apy_chart.py), [`extract_q3_chart.py`](extract_q3_chart.py) | Read the report's chart values (needs the report itself, from the forum thread) |
| [`reported_apy_digitised.txt`](reported_apy_digitised.txt), [`reported_apy_q3_vector.txt`](reported_apy_q3_vector.txt) | The values we read off the two charts |
| `data/` | Our daily share prices and summaries for each vault |

**Addresses:** Gauntlet USDC Core `0x7e97fa6893871A2751B5fE961978DCCb2c201E65` (Arbitrum) · Spark sUSDC
`0x940098b108fB7D0a7E374f6eDED7760787464609` (Arbitrum) · Aave USDC static-aToken `0x7F6501d3B98eE91f9b9535E4b0ac710Fb0f9e0bc`
(Arbitrum) · Maple syrupUSDC `0x80ac24aA929eaF5013f6436cdA2a7ba190f5Cc0b` (Ethereum, where its rate is set).

## Who we are

Arcobaleno Research checks investment numbers independently: https://arcobaleno.cloud. Nobody paid for this. We hold no ARB
and no money in any of these vaults. One of our research tests trades on paper only (no real money) across every listed
futures market; it closed two paper ARB trades in October (+20.9% and +6.7%) and holds none now. Questions or corrections:
dvt@arcobaleno.cloud.
