# Balancer wind-down: what is redeemable, and what each BAL gets

Quantities read on-chain on 18 September 2026 (Ethereum block 26,005,414 and the same hour on Gnosis, Arbitrum, Base, Polygon and HyperEVM); supply and BAL balances at blocks 26,005,258 to 26,006,274; the tetuBAL lock at block 25,977,785, the wind-down post block. Prices are DefiLlama prices at **18 September 2026 14:00 UTC** (ETH $2,550, stkAAVE $140.66, BAL $0.1114). These are today's values. Every line is re-measured at the opening snapshot at the end of May 2027; this document establishes the method and the order of magnitude, not the settlement figure. Vault tokens are converted to their underlying with `convertToAssets`, pool positions read through the Balancer V3 Vault, the POL delegation with `getTotalStake`. BAL and anything that resolves into BAL is excluded; BAL-paired positions count only their non-BAL leg. BAL held by DAO-controlled entities does not redeem; their non-BAL balances are distributable.

## 1. Distributable assets (non-BAL)

| bucket | address | value | share | status |
|---|---|---:|---:|---|
| Treasury Safe (kpk) | `0x0EFcCBb9E2C09Ea29551879bd9Da32362b32fc89` | $9,127,957 | 91.7% |  |
| v3 buffers (owned by the Treasury Safe) | `0xbA1333333333a1BA1108E8412f11850A5C319bA9 (V3 Vault)` | $397,709 | 4.0% |  |
| Innovation Fund | `0x284a37B375e69c8cB30a5633Ee55f3584dd26808` | $155,692 | 1.6% |  |
| MerkleRedeem LDO (BIP-922) | `0x884226c9f7b7205f607922E0431419276a64CF8f` | $137,709 | 1.4% | figure under review until 30 September; DAO property, no third-party claimants |
| BizDev, non-BAL | `0xF3B4829C8B9E2910C2396538F49a12b0c2475a7e` | $74,196 | 0.7% | figure under review until 30 September |
| Onchain Ltd, non-BAL | `0x16b0056636Fcc85f92C49cD49a24bc519d4A1941` | $66,152 | 0.7% |  |
| **Distributable base** | | **$9,959,416** | 100% | |

Shown apart:

| bucket | address | balance | note |
|---|---|---:|---|
| OpCo Safe, operating account, residual returns to holders | `0x3B8910F378034FD6E103Df958863e5c684072693` | $763,010 | 763,246 USDC plus dust, read on-chain at block 26,005,414. It carries the September and October notice period and the wind-down budget, with the residual returning to holders: between $63,010 and $283,010, derived from the proposal's budget lines, not measured. |
| Aura, only from May 2027 | `0x928966752dc0cc0D7babe343Fc2937BA13a5120c` + Gnosis auraBAL | $21,669 | rAURA redeems into stkAAVE and WETH from the `AuraRedemption` contract (expiry 13 May 2027) and auraBAL unlocks at Aura's stage 2; counted as the treasury's pro-rata share of what the contract holds today plus the WETH leg of 8,975 auraBAL, read on-chain. Separate because it exists only from May 2027. |

Figures are rounded to the dollar and to two decimals; column totals may differ by a unit.

## 2. BAL that can redeem (the denominator)

| line | BAL |
|---|---:|
| BAL total supply (`BAL.totalSupply()`, read on-chain at block 26,005,258) | 72,373,883.13 |
| less Treasury Safe `0x0EFcCBb9E2C09Ea29551879bd9Da32362b32fc89`: 3,435,806.35 direct, 112,671.77 inside 21,827 BPT at 5.162033 BAL per BPT, 11,530.27 BAL and 8,471.17 axlBAL on Arbitrum (read on-chain at block 26,005,258 and Arbitrum block 506,515,723) | 3,568,479.56 |
| less BLabs Fundraise Safe `0xB129F73f1AFd3A49C701241F374dB17AE63B20Eb` (blabs_fundraise in the Maxis address book; read on-chain at block 26,005,266) | 1,599,054.29 |
| less BLabs Team Safe (`0xCDcEBF1f28678eb4A1478403BA7f34C94F7dDBc5`, the safe the proposal calls BLabs Vesting Safe; read on-chain at block 26,005,266; the gap to the 0.98M in BIP-919 is vesting paid out since that snapshot) | 928,041.34 |
| less OpCo Safe `0x3B8910F378034FD6E103Df958863e5c684072693` BAL (read on-chain at block 26,005,266) | 408,730.39 |
| less BizDev Safe `0xF3B4829C8B9E2910C2396538F49a12b0c2475a7e` BAL (read on-chain at block 26,005,266) | 410,713.10 |
| less Onchain Ltd Safe `0x16b0056636Fcc85f92C49cD49a24bc519d4A1941` BAL (read on-chain at block 26,005,414) | 235,321.55 |
| less other DAO-held BAL, aggregated (per-address detail in the sweep file) | 26,549.95 |
| less the DAO's claim on Aura's veBAL BPT, through auraBAL (90% tranche) and rAURA (10% tranche): 137,679.47 BAL, redeemable only from May 2027 (8,975.4178 auraBAL and 2,323,130.85 rAURA against supplies of 3,684,353.77 and 46,033,045.19 and Aura's lock of 3,684,354.77 BPT, read on-chain at block 26,006,274 and Gnosis block 48,317,898; at 5.162033 BAL per BPT) | 137,679.47 |
| plus BAL paid from the treasury to tetuBAL holders: half of the 539,726.48 BPT locked by the Tetu locker at block 25,977,785 × 5.171483 BAL per BPT at that block (derived; fixed at the post block by the proposal) | 1,395,593.07 |
| less BAL behind the Tetu permalock: 539,726.48 BPT × 5.162033 BAL per BPT read on-chain at block 26,005,258 (derived; never redeemable) | 2,786,085.71 |
| less BAL on loan to Amber under BIP-664, returning to the treasury: 600,000.00 outstanding from BAL Transfer logs (1,000,000 lent by the OpCo in August 2024, 400,000 repaid on 2 June 2026) | 600,000.00 |
| **= redeemable BAL** | **63,068,820.84** |

**tetuBAL backing, case 2 of the three in the decision.** The veBAL position behind tetuBAL is held by the Tetu `BalLocker` `0x9cC56Fa7734DA21aC88F6a816aF10C5b898596Ce`, which had 539,726.48 BPT locked at block 25,977,785 (read on-chain; detail in the sweep file). That is less than the 549,670.66 tetuBAL supply, so the cap does not bind and the payment is 1,395,593.07 BAL, fixed at the post block by the proposal, while the permalock exclusion uses today's BAL-per-BPT ratio because it is a fact about BAL that exists now, not by oversight. The lock ends 8 April 2027, before round one opens, but the Tetu BalLocker exposes no function that withdraws from veBAL (verified ABI), so the BPT can never leave and that BAL can never redeem.

BAL held by the DAO and its entities, including the Amber loan and the Aura claim, comes to 5,387,474.02 BAL across the lines above, about $600,165 at $0.1114. Of that, 1,395,593.07 BAL is paid from the treasury to tetuBAL holders at opening and does redeem; the remaining 3,991,880.95 BAL never does.

## 3. Value per BAL

| | value |
|---|---:|
| distributable base | $9,959,416 |
| redeemable BAL | 63,068,820.84 |
| **value per BAL** | **$0.1579** |
| per tetuBAL (2.538962 BAL each) | $0.4009 |

## 4. Position detail

| bucket | position | chain | quantity | value | note |
|---|---|---|---|---:|---|
| Treasury Safe (kpk) | kpk USDC Prime V2 Morpho vault | Ethereum | 1,413,462.89 USDC | $1,412,793 | ERC-4626 convertToAssets |
| Treasury Safe (kpk) | kpk USDC Yield V2 Morpho vault | Ethereum | 642,047.11 USDC | $641,743 | ERC-4626 convertToAssets |
| Treasury Safe (kpk) | Compound Institutional USDC (ciUSDCv3) | Ethereum | 500,244.90 USDC | $500,008 | Comet balanceOf is in USDC units; assumes 1:1 withdrawal |
| Treasury Safe (kpk) | stkAAVE | Ethereum | 19,549.40 | $2,749,911 |  |
| Treasury Safe (kpk) | COW | Ethereum | 1,230,445 | $175,130 |  |
| Treasury Safe (kpk) | SAFE | Ethereum | 845,094 | $82,627 |  |
| Treasury Safe (kpk) | weETH | Ethereum | 350.8384 | $988,738 |  |
| Treasury Safe (kpk) | rETH | Ethereum | 62.6945 | $187,074 |  |
| Treasury Safe (kpk) | sGHO (+ liquid waEthLidoGHO) | Ethereum | 150,704.40 GHO | $150,458 | convertToAssets |
| Treasury Safe (kpk) | Delegated POL (dPOLc0) | Ethereum | 106,114.23 POL | $10,664 | ValidatorShare getTotalStake |
| Treasury Safe (kpk) | HOPR | Ethereum | 617,205 | $7,541 |  |
| Treasury Safe (kpk) | aEthUSDC + cUSDCv3 + cDAI | Ethereum | 4,827 + 1.59 USDC, 45.16 cDAI | $4,828 |  |
| Treasury Safe (kpk) | B-80BAL-20WETH 21,827 BPT, WETH leg only | Ethereum | 1.2531 WETH | $3,193 | BAL leg excluded |
| Treasury Safe (kpk) | sDAI | Gnosis | 2,213,652.08 WXDAI | $2,213,250 | convertToAssets |
| v3 buffers (owned by the Treasury Safe) | buffer liquidity in WETH | Ethereum | 67.8999 WETH | $173,004 | Vault getBufferOwnerShares / getBufferBalance |
| v3 buffers (owned by the Treasury Safe) | buffer liquidity in USDT | Ethereum | 51,695.4652 USDT | $51,656 | Vault getBufferOwnerShares / getBufferBalance |
| v3 buffers (owned by the Treasury Safe) | buffer liquidity in GHO | Ethereum | 50,491.1716 GHO | $50,409 | Vault getBufferOwnerShares / getBufferBalance |
| v3 buffers (owned by the Treasury Safe) | buffer liquidity in wstETH | Ethereum | 22.2825 wstETH | $70,818 | Vault getBufferOwnerShares / getBufferBalance |
| v3 buffers (owned by the Treasury Safe) | buffer liquidity in USDC | Ethereum | 51,845.8910 USDC | $51,821 | Vault getBufferOwnerShares / getBufferBalance |
| Innovation Fund | AutoRange WETH/USDC - C (eth) | Ethereum | 34,231.9362 USDC, 3.1446 WETH | $42,228 | 99.95% of pool, V3 Vault getPoolTokenInfo |
| Innovation Fund | AutoRange WETH/USDC (eth) | Ethereum | 34,213.1349 USDC, 3.1299 WETH | $42,172 | 99.95% of pool, V3 Vault getPoolTokenInfo |
| Innovation Fund | AutoRange WETH/USDC (base) | Base | 3.0787 WETH, 34,114.6334 USDC | $41,943 | 99.93% of pool, V3 Vault getPoolTokenInfo |
| Innovation Fund | BTFSH BTC:PAXG:USDC (eth) | Ethereum | 0.1682 WBTC, 0.1297 PAXG, 4,820.7337 USDC | $18,833 | 37.67% of pool, V3 Vault getPoolTokenInfo |
| Innovation Fund | wallet: WETH, USDC | Ethereum | 1.0469 WETH, 1,162.65 USDC | $3,830 |  |
| Innovation Fund | wallet: USDC | Base | 3,083.22 USDC | $3,082 |  |
| Innovation Fund | wallet: HYPE | HyperEVM | 39.8446 HYPE | $3,605 | native balance; no explorer for other tokens |
| MerkleRedeem LDO (BIP-922) | LDO held by the contract | Ethereum | 350,515.40 LDO | $137,709 |  |
| BizDev | USDC | Ethereum | 22,047.28 | $22,037 |  |
| BizDev | USDC | Polygon | 34,000.00 | $33,984 |  |
| BizDev | POL (native) | Polygon | 98,942.85 | $9,943 |  |
| BizDev | USDC | Arbitrum | 6,670.55 | $6,667 |  |
| BizDev | USDC | Base | 1,382.00 | $1,381 |  |
| BizDev | RPL, BOLD, ETH dust | Ethereum | 60.8 RPL, 51.2 BOLD, 0.01 ETH | $184 |  |
| Onchain Ltd | USDC (+0.035 ETH) | Ethereum | 66,094.56 USDC | $66,152 |  |
| Aura, only from May 2027 | rAURA 2,323,131: pro-rata share of what AuraRedemption holds today | Ethereum | 59.05 stkAAVE, 4.7290 WETH | $20,356 | 5.047% of supply; full allocation would be 165.5 stkAAVE + 13.25 WETH; expiry 13 May 2027 |
| Aura, only from May 2027 | auraBAL 8,975 on Gnosis, WETH leg only | Gnosis | 0.5153 WETH | $1,313 | BAL leg excluded |
| OpCo Safe | USDC (+0.05 ETH) | Ethereum | 763,246.42 USDC | $763,010 |  |

Two values are read but rest on an assumption: ciUSDCv3 at 1:1 USDC (Comet reports the balance in USDC units), and dPOLc0 at the POL price for the staked amount. Sources: Tenderly and dRPC archive nodes, Blockscout for token discovery only, DefiLlama `coins.llama.fi` for prices, Balancer V3 Vault for buffers and pools.
