# ENS rebuild — match rule, fixed BEFORE the first result (2026-10-29)

Written while `scripts/daily.py` was still collecting data; no rebuilt number had been seen. Committed before
`scripts/blend.py` was first run. Any later change to this rule gets a dated note below, never an edit.

## What is compared
KPK's H1 2026 review table (t/22358): monthly **gross DeFi yield (USD)** and **gross APY**, and the H1 totals
($1,370,722; 3.12%). Secondary: the monthly forum series (Syncrone, $1,343,890) and month-end NAV.

## How we compute
- Yield = growth of each position's value from its own exchange rate / share price / index (or, for rebasing tokens,
  change in balance minus net transfers), daily at 00:00 UTC, converted to USD at the same day's Chainlink ETH/USD.
  Excludes ETH price moves (as KPK does). Reward tokens (COMP, MORPHO, FLUID) are reported **separately**, because KPK's
  "realised investment P&L" includes rewards claimed and converted.
- APY two ways: (a) **KPK's method**, month's yield × 12 ÷ month-end NAV; (b) **daily capital**, yield ÷ dollar-days × 365.

## The rule
1. **H1 gross yield reproduces** if ours (with rewards) is within **±5%** of $1,370,722 (or of $1,343,890, whichever is
   closer; KPK publishes both and says the gap is timing).
2. **A month reproduces** if ours, on KPK's method (a), is within **±0.15pp** of KPK's monthly gross APY. Fewer than
   4 of 6 months reproducing = "doesn't match month by month", which we report as such.
3. **Month-end NAV coverage:** our on-chain total must be within ±3% of KPK's month-end figure for that month to count
   at all. Below that, the month is "not covered" (a gap in our position list), not a mismatch.
4. Whatever (b) shows next to (a) is reported as a **method difference**, not a mismatch.
