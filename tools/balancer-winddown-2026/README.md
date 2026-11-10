# Balancer wind-down inventory, 18 September 2026: rebuilt from the chain

Arcobaleno Research · published 10 November 2026 · MIT licence (`LICENSE.txt`)

## What this checks

Balancer DAO is winding down. Each BAL that can redeem gets a share of what the DAO owns, and the
[published inventory](https://gist.github.com/marcusblabs/794a551c924bdac8a787045f4bc2a56c) (two lists, measured on
18 September 2026) puts that at **$0.1579 per BAL**: a distributable base of $9,959,416 over 63,068,820.84 BAL that can
redeem. Its author called it his own measurement and asked for it to be checked. The figures are re-measured at the
opening snapshot in May 2027; this check is of the 18 September lists.

These scripts read every line again from the chain, at the same blocks the lists state, and search the DAO's addresses
on six chains for anything the lists leave out. We wrote down what counts as a match before the first read (`PREREG.md`).

## Result

**The published inventory holds.** $0.1579 per BAL reproduces.

| Test (fixed in advance) | Published | Rebuilt | Limit | Result |
|---|---:|---:|---|---|
| Distributable base | $9,959,416 | $9,960,126 (+0.007%) | ±1% | **Matches** |
| BAL that can redeem, listed lines | 63,068,820.84 | every line matches | ±0.05% | **Matches** |
| BAL that can redeem, with the one vault we found | 63,068,820.84 | 63,036,667.89 (−0.051%) | ±0.05% | **Just outside** |
| Quantities, 33 lines | | 30 within 0.01% | ±0.01% | **Three small differences**, about $1 each or a rounding |

Three lines ($45,732, 0.46% of the base) we couldn't read and carried at the published value: AutoRange on Base
($41,943), HYPE ($3,605), BizDev dust ($184). OpCo ($763,009 rebuilt, $763,010 published) is shown apart from the base.

**One addition.** A Mimic fee vault, `0x9e5D6427D2cdaDC68870197b099C2Df535Ec3c97`, held 32,152.95 BAL at the snapshot.
It is in Balancer's address book as fee-processing infrastructure, but on neither list. It paid exactly that amount to
Onchain Ltd on 24 September. Counting it moves the value from $0.15791 to $0.15799 per BAL. Our suggestion: add Mimic
vaults to the address list for the opening snapshot. (That the vault belongs to the DAO is our reading of the address
book and the flows, not of a document.)

**Large balances that were rightly left out.** About $1.5M in the DAO multisig `0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f`
is exploit recovery and rescue money owed to pool users (BIP-930, BIP-892/923). $213,139 of rETH in `dao op` on Optimism
is being paid out to users through claims.

**One open question.** `dao arb` on Arbitrum holds $36,175 (WETH, wstETH, rETH, ETH). It looks like the same kind of
claims money, and the claim contract exists at the same address there, but we found no transfer history to prove it.

**Small, outside the base:** five balances of about $18k together (0.18% of the base), and about $16,500 of pool tokens in
the fee collectors (513 looked through, none worth $1,000). `unpriced.py` prints a total of about $32,200: it also
looks through one pool token in the Treasury Safe, the 80/20 BAL-WETH one ($15,743, mostly BAL), which is outside the
base under the lists' own rule.

## What this does not cover

- On Arbitrum, Base and Polygon the search covers a fixed list of major tokens only (the block explorers refuse
  automated reads). HyperEVM and Avalanche aren't covered.
- 219 tokens with no price and no pool are counted as zero.
- Prices come from one source, DefiLlama, at 18 September 2026 14:00 UTC, as in the published lists.
- axlBAL and parts of the lists' combined BAL line are carried, not read. ciUSDCv3 at $1 and dPOLc0 at the POL price
  follow the lists' own two assumptions.

## How to run it

**Download everything:** [balancer-winddown-2026.tar.gz](../balancer-winddown-2026.tar.gz)
([sha256](../balancer-winddown-2026.tar.gz.sha256), [signature](../balancer-winddown-2026.tar.gz.asc), signed with our
[release key](../arcobaleno-release-pubkey.asc)).

Python 3.10 or later, plus `requests`. No keys needed; it uses free public endpoints.

    python3 scripts/rule3.py   # the base and the value per BAL, from the data/ folder (fetches three prices from DefiLlama, no chain reads)
    ./run_all.sh               # read everything again from the chain (slow: can take hours on free endpoints)

Every script writes into `data/`. The files shipped there are what the scripts wrote on 2 November 2026.

Tested from a clean copy on 10 November 2026: every script runs, and `rule3.py`, `assets.py`, `fixes.py` and
`multisig.py` give identical files. Two known differences on today's free endpoints: the Polygon endpoint no longer
answers native-token balances at the September blocks (16 lines in `candidates.json` come back as read errors), and
a few small tokens now have no DefiLlama price. Neither touches a figure in the result.

| File | What it does |
|---|---|
| `scripts/assets.py` | Every asset line of the lists, at the stated block, priced at the stated hour → `data/assets.json`, `data/prices.json` |
| `scripts/fixes.py` | The lines that needed a second look: a second WETH buffer, the AutoRange block scan, sDAI, native-token dust → `data/fixes.json` |
| `scripts/denom.py`, `scripts/denom2.py` | BAL supply and every BAL line of the second list, plus BAL holders seen in the flows but not listed (prints) |
| `scripts/window.py` | Whether any BAL moved between DAO addresses inside the read window (prints) |
| `scripts/mimic.py` | The Mimic fee vaults at the stated blocks → `data/mimic.json`. Which tokens to read comes from the block explorer's list today, so the small tokens can differ from ours; the 32,152.95 BAL reads the same (re-run 10 November 2026) |
| `scripts/multisig.py` | What the DAO multisig held and where it came from → `data/multisig_transfers.json` |
| `scripts/candidates.py`, `scripts/unpriced.py` | The search: every token on every address, priced, with pool tokens looked through → `data/candidates.json`, `data/unpriced.json` |
| `scripts/rule3.py` | The distributable base and the value per BAL → `data/rule3.json` |
| `scripts/discover.py`, `scripts/hist_tokens.py` | Which tokens to look for, from the block explorers. Not in `run_all.sh`: they read today's state and the explorers now refuse us, so their October output ships in `data/` |
| `scripts/ocrpc.py`, `scripts/keccak.py`, `scripts/common.py` | Reading the chain, with no other libraries |
| `raw/` | The two published lists as we read them (`SHA256SUMS`), the address book, the forum threads |

## Who we are

Arcobaleno Research checks investment numbers independently: https://arcobaleno.cloud. Nobody paid for this check,
and we hold no BAL. We don't work for Balancer DAO or Balancer Labs. Questions or corrections: dvt@arcobaleno.cloud.
