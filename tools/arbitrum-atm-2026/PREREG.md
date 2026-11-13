# Arbitrum ATM stablecoin rates — the match rule, fixed before each rebuild

Copied word for word from our working file. Step 2 was committed (commit 0bd51d5, 2026-10-23) before the July & August rebuild ran; Step 2b (commit 6c4088a, 2026-11-10) before any September reading. Paths in it refer to our working folders; in this package the same files are under `data/`.

## Step 2 — the match rule (written 2026-10-23, BEFORE any rebuild was run; commit time is the proof)
**Our number.** From the vault's own share value (`onchain/oc1_vault_return.py`, daily, 2026-05-15 to 2026-09-05).
The report does not say how its "30D MA net APY" is calculated, so we compute two versions and **use whichever is
closer to the report** (the doubt goes in their favour):
- (a) 30-day simple: (value today ÷ value 30 days ago − 1) × 365/30
- (b) average of the last 30 daily rates, each daily rate × 365

**Checkpoints:** 07-15, 07-31, 08-15, 08-25 (07-01 kept as a check on the reading). To allow for the date
read-off, at each checkpoint we compare the reported value with **the nearest of our values within ±2 days**.

**Per line:**
- **MATCHES** — every checkpoint within **0.5 pp**.
- **DOES NOT MATCH** — **two or more** checkpoints more than **1.0 pp** away, under both (a) and (b).
- **UNCLEAR** — anything else. Reported as unclear, not rounded either way.

**Before calling a line DOES NOT MATCH, rule out the innocent explanations** and say which applied:
1. Reward tokens (e.g. MORPHO incentives) included in their number but not in the share value: check the
   protocol's own rewards APR for the window. If it closes the gap → "matches once rewards are counted; the
   report does not say rewards are included".
2. A different vault/share class than the one we read (e.g. a bridged token with its own rate).
3. Our own error: the second RPC endpoint and the protocol's own series (oc1's `--compare`) must agree with us.

**The flat USDai line** is not scored by this rule. A perfectly flat 5.01% for four months is not what a
market-rate product looks like; it may be a fixed-rate deal. **It is a question to ask, not a finding**, until we
know what the DAO actually holds.

**The ~190 bp claim:** benchmark and window are not stated. We check it only after the lines above, as: weighted
average of the rebuilt line rates at 08-31 (weights from the arbdata feed's balances that day) minus the rebuilt
Aave rate. **Consistent** if within 0.5 pp of 1.9 pp; otherwise say what definition would be needed to get 1.9.

**What any result means:** this checks the *rate each product paid*. It does not check that the DAO held those
amounts (no wallet addresses) or the dollar interest lines. The write-up must say so in plain words.

## Step 2b — September addendum (written 2026-11-10, BEFORE any September read or chart reading; commit time is the proof)
Source: the Q3 '26 quarterly report (see the restart triggers below), p.19 "30D MA Net APY", same chart type as the Jul & Aug p.10.
**Same rule as Step 2, unchanged**: both versions (a)/(b), nearest of ours within ±2 days, MATCHES = every checkpoint within
0.5 pp, DOES NOT MATCH = two or more checkpoints over 1.0 pp under both, UNCLEAR otherwise; the three innocent explanations first.
- **Checkpoints:** 09-15 and 09-28 (the end of the line is hard to read, so not 09-30). **08-25 is read again** from the Q3 chart as a
  check on the reading and on whether the Q3 chart repeats the Jul & Aug values; it is not scored again.
- **Lines scored:** Aave V3 USDC (benchmark), Spark sUSDC, Maple syrupUSDC. Gauntlet Core held nothing in September (out by 08-26):
  not scored. **USDai:** not scored (private terms, Entropy 11-03); we only say whether the line is still flat and at what level.
- **Our numbers:** oc1 re-run for each vault from 2026-08-01 to 2026-10-02 (the 30-day windows need August).
- **No headline claim to check:** the Q3 text makes no stablecoin-vs-benchmark claim (searched for "bps", "benchmark",
  "outperform"). We do not construct one.
- **Reading accuracy** is tested the same way: if Aave comes back within ~0.05 pp, the read-off is good.
