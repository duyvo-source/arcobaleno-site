# Balancer wind-down inventory check — match rule, fixed BEFORE the first read (2026-10-30)

Written after reading Marcus's published method (gist 794a551c…, version 890e1153, 2026-10-06; saved in `raw/`) and before reading any
balance from the chain. Committed before the first result. Any later change gets a dated note below, never an edit.

## What is compared
The gist's section 1 (distributable base $9,959,416), section 2 (redeemable BAL 63,068,820.84) and section 4 (position detail), at the
same blocks it states: Ethereum 26,005,414 (assets) and 26,005,258–26,006,274 (BAL and supply), Gnosis 48,317,441 / 48,317,898,
Arbitrum 506,515,723, Base 51,482,712, Polygon 94,033,766, tetuBAL lock at Ethereum 25,977,785.

## The rule
1. **A quantity reproduces** if ours at the stated block is within **±0.01%** of the published figure. Same chain, same block: it
   should be exact. Where the stated block is a range or unclear, we say so; a difference there is "block unclear", not a mismatch.
2. **The denominator reproduces** if ours is within **±0.05%** of 63,068,820.84.
3. **The base reproduces** if ours is within **±1%** of $9,959,416, using DefiLlama prices at the stated hour (18 Sep 2026, 14:00 UTC).
   If a price can't be had, that line's published value is carried and marked as carried.
4. Lines the gist marks "under review until 30 September" are reported, and don't count against rule 3 if they moved for that reason.

## Discovery (the second question, separate from the rule)
Are there DAO assets the inventory doesn't count? We check, for every address in the gist and the Balancer address book it cites, what
else it holds, including the fee collectors. A **candidate** is anything worth **≥$1,000**. A candidate is not a finding until we have
checked three things: is it really there on-chain, does it belong to the DAO and not to LPs or third parties (BIP-928 excludes
attack-recovery funds), and is it already covered elsewhere (for example paid out or moved since 18 September).

## How we report
Whatever comes out gets reported, including "it all holds". Differences are stated as differences, not faults. Marcus called this his
own measurement and asked for it to be checked: the point is to help, and the opening snapshot is re-measured anyway.
