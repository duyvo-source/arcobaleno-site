# DAO-held BAL sweep, 18 September 2026

Every address in the report and every `multisigs` entry of the Balancer Maxis address book, on every chain where it exists, checked for BAL in all forms: the token and its bridged versions, BPT with BAL inside (wallet, gauge, wrapper), liquid lockers (auraBAL, sdBAL, tetuBAL, stkauraBAL), lending and vault receipts (aEthBAL, aBAL, Across LP, TETU_ST_BAL), veBAL locks, and Balancer Vault internal balances. Conversions: BPT, sdBAL and veBAL-locked BPT at 5.162033 BAL per BPT (mainnet pool, block 26,005,258); auraBAL as its share of the 90% tranche of Aura's 3,684,354.77 BPT veBAL lock (0.900000 BPT per auraBAL against a supply of 3,684,353.77, block 26,006,274), then at 5.162033; DAO-held tetuBAL at the wind-down payment rate of 2.538962 BAL per tetuBAL, since the BAL behind it sits in the permalock line; pool BPT by the holder's share of the pool's BAL; axlBAL 1:1 (8,505.61 BAL in the Axelar gateway against 8,478.05 axlBAL supply, read at block 26,006,091); anyBAL 0 (Multichain routers hold no BAL).

## Coverage

| chain | RPC block | address discovery | token discovery |
|---|---:|---|---|
| arbitrum | 506515723 | address book multisigs + report addresses + v2 ProtocolFeesCollector + V3 fee controllers | Blockscout token list |
| avalanche | 95608611 | address book multisigs + report addresses + v2 ProtocolFeesCollector + V3 fee controllers | none: direct reads of BAL and known wrappers only |
| base | 51482712 | address book multisigs + report addresses + v2 ProtocolFeesCollector + V3 fee controllers | Blockscout token list |
| fraxtal | 41472102 | address book multisigs + report addresses + v2 ProtocolFeesCollector + V3 fee controllers | none, and BAL token address not known: not covered |
| gnosis | 48317441 | address book multisigs + report addresses + v2 ProtocolFeesCollector + V3 fee controllers | Blockscout token list |
| hyperevm | 46256977 | address book multisigs + report addresses + v2 ProtocolFeesCollector + V3 fee controllers | none, and BAL token address not known: not covered |
| mainnet | 26006091 | address book multisigs + report addresses + v2 ProtocolFeesCollector + V3 fee controllers | Blockscout token list |
| mode | 44793972 | address book multisigs + report addresses + v2 ProtocolFeesCollector + V3 fee controllers | Blockscout token list |
| monad | 105960703 | address book multisigs + report addresses + v2 ProtocolFeesCollector + V3 fee controllers | none, and BAL token address not known: not covered |
| optimism | 157078387 | address book multisigs + report addresses + v2 ProtocolFeesCollector + V3 fee controllers | Blockscout token list |
| plasma | 32815064 | address book multisigs + report addresses + v2 ProtocolFeesCollector + V3 fee controllers | none: direct BAL read only |
| polygon | 94033766 | address book multisigs + report addresses + v2 ProtocolFeesCollector + V3 fee controllers | Blockscout token list |
| xlayer | 70986928 | address book multisigs + report addresses + v2 ProtocolFeesCollector + V3 fee controllers | none, and BAL token address not known: not covered |
| zkevm | 33391890 | address book multisigs + report addresses + v2 ProtocolFeesCollector + V3 fee controllers | Blockscout token list |

Not covered by construction: Uniswap v3 style NFT positions, third-party gauges outside Balancer, and explorer index staleness (one 20,000 BPT balance the Base explorer reported for the LM multisig reads 0 on-chain). Vault internal balances of BAL were read for every DAO address on the eight v2 chains: all zero.

## Addresses

| holder | address | chains in the findings |
|---|---|---|
| 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x212F884252792ebaaA811FB0678444b21c7C2879` | mainnet |
| 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x4638ab64022927C9bD5947607459D13f57f1551C` | arbitrum |
| 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0xa7d524046ef89de9F8e4f2d7B029f66cCB738d48` | gnosis |
| 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x2FF226CD12C80511a641A6101F071d853A4e5363` | base |
| 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x3630D26E51c03026f4f063d69d65F8E234eEAf5b` | avalanche |
| BizDev Safe | `0xF3B4829C8B9E2910C2396538F49a12b0c2475a7e` | mainnet, base |
| DAO multisig | `0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f` | mainnet |
| multisig _deprecated/maxi_ops | `0x166f54F44F271407f24AA1BE415a730035637325` | mainnet |
| multisig _deprecated/maxi_ops | `0x5891b90CE909d4c3540d640d2BdAAF3fD5157EAD` | arbitrum |
| multisig alliance_program/lido | `0x87D93d9B2C672bf9c9642d853a8682546a5012B5` | mainnet |
| multisig alliance_program/rocket | `0xb867EA3bBC909954d737019FEf5AB25dFDb38CB9` | mainnet |
| multisig beets_treasury | `0xea06e1b4259730724885a39CE3ca670eFB020E26` | mainnet |
| multisig blabs_fundraise | `0xB129F73f1AFd3A49C701241F374dB17AE63B20Eb` | mainnet |
| multisig blabs_team | `0xCDcEBF1f28678eb4A1478403BA7f34C94F7dDBc5` | mainnet |
| multisig dao | `0xaF23DC5983230E9eEAf93280e312e57539D098D0` | arbitrum |
| multisig dao | `0x043f9687842771b3dF8852c1E9801DCAeED3f6bc` | optimism |
| multisig grants_treasury | `0xE2c91f3409Ad6d8cE3a2E2eb330790398CB23597` | mainnet |
| multisig lm | `0xc38c5f97B34E175FFd35407fc91a937300E33860` | polygon |
| multisig lm | `0x14969B55a675d13a1700F71A37511bc22D90155a` | gnosis |
| multisig lm | `0x65226673F3D202E0f897C862590d7e1A992B2048` | base |
| multisig maxi_beets_lm | `0x09Df1626110803C7b3b07085Ef1E053494155089` | optimism |
| multisig omni | `0x9ff471F9f98F42E5151C7855fD1b5aa906b1AF7e` | base |
| multisig stakedao_vebal_manager | `0xB0552b6860CE5C0202976Db056b5e3Cc4f9CC765` | mainnet |
| Onchain Ltd Safe | `0x16b0056636Fcc85f92C49cD49a24bc519d4A1941` | mainnet |
| OpCo Safe | `0x3B8910F378034FD6E103Df958863e5c684072693` | mainnet |
| ProtocolFeesCollector (v2) | `0xce88686553686DA562CE7Cea497CE749DA109f9F` | mainnet, polygon, arbitrum, optimism, gnosis, base |
| Treasury Safe | `0x0EFcCBb9E2C09Ea29551879bd9Da32362b32fc89` | mainnet, arbitrum, gnosis |

## Findings with BAL inside

| chain | holder | address | form | quantity | BAL-equivalent | conversion | denominator treatment |
|---|---|---|---|---:|---:|---|---|
| arbitrum | 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x4638ab64…` | BAL | 0.3945 | 0.39 | 1:1 | other-chain fee contracts line, ADDED in this patch |
| arbitrum | ProtocolFeesCollector (v2) | `0xce886865…` | BAL | 251.7368 | 251.74 | 1:1 | other-chain fee contracts line, ADDED in this patch |
| arbitrum | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 33AURA-33ARB-33BAL | 141.5084 | 48.93 | share 55.5552% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| arbitrum | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT GOLD-BAL-AURA-wstETH | 5.8602 | 21.79 | share 3.3688% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| arbitrum | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 10BAL-20CRV-20SUSHI-25UNI-25GMX | 4.0606 | 4.13 | share 98.8433% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| arbitrum | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT axlBAL/BAL | 1.3870 | 0.80 | share 95.6726% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| arbitrum | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 25BAL-25AURA-25wstETH-25ARB | 0.7747 | 1.62 | share 99.9298% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| arbitrum | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 67BAL-29WBTC-4wstETH | 0.3017 | 10.56 | share 99.3624% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| arbitrum | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 50BAL-50ARB | 0.0615 | 0.03 | share 6.2376% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| arbitrum | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 80BAL-20WETH | 0.0146 | 0.06 | share 99.9291% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| arbitrum | Treasury Safe | `0x0efccbb9…` | BAL | 11,530.2668 | 11,530.27 | 1:1 | Treasury Safe line (Arbitrum) |
| arbitrum | Treasury Safe | `0x0efccbb9…` | axlBAL | 8,471.1674 | 8,471.17 | bal | Treasury Safe line, ADDED in this patch |
| avalanche | 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x3630d26e…` | BAL | 0.0248 | 0.02 | 1:1 | other-chain fee contracts line, ADDED in this patch |
| base | 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x2ff226cd…` | BAL | 12.3627 | 12.36 | 1:1 | other-chain fee contracts line, ADDED in this patch |
| base | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 50AURA-50BAL | 382.7773 | 188.03 | share 88.8669% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| base | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 8AURA-8BAL-33GOLD-50COIN | 97.0070 | 0.05 | share 99.7286% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| base | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT GOLD/BAL/USDC | 19.4651 | 48.39 | share 17.7759% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| base | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT axlBAL/BAL | 1.7519 | 1.42 | share 14.2499% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| base | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 50BAL-50DAI | 0.0580 | 0.12 | share 1.5623% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| base | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 50BAL-50USDbC | 0.0234 | 0.03 | share 6.0060% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| base | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 50BAL-50WETH | 0.0174 | 1.74 | share 5.1323% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| base | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 50BAL-50USDbC | 0.0120 | 0.02 | share 2.0310% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| base | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 50BAL-50DAI | 0.0101 | 0.01 | share 3.7233% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| base | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 30BAL-70WETH | 0.0000 | 0.01 | share 1.1612% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| base | multisig lm | `0x65226673…` | v2 BPT axlBAL/BAL | 20,000.0000 | 16,221.53 | share 162676.6261% of pool BAL | explorer-index artifact: on-chain balance is 0 |
| gnosis | 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0xa7d52404…` | BAL | 0.0372 | 0.04 | 1:1 | other-chain fee contracts line, ADDED in this patch |
| gnosis | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 10BAL-45GROSH-15crvUSD-15sDAI-15WXDAI | 234.4697 | 0.02 | share 0.7766% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| gnosis | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT USDC.e-USDT-BAL-GROSH-sDAI | 150.2281 | 0.01 | share 0.5098% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| gnosis | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT B-50wstETH-25BAL-25AURA | 1.6858 | 41.07 | share 0.2741% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| gnosis | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT BAL-GNO-wstETH/WETH-WXDAI | 1.5593 | 0.12 | share 93.8809% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| gnosis | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 25WETH-25BAL-25GNO-25wxDAI | 1.2113 | 51.18 | share 86.3349% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| gnosis | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 20WETH-80BAL | 0.0120 | 0.06 | share 99.4076% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| gnosis | Treasury Safe | `0x0efccbb9…` | auraBAL | 8,975.4178 | 41,698.27 | 90% tranche of Aura's veBAL lock (0.900000 BPT per auraBAL), at 5.162033 BAL per BPT | Aura claim line (90% tranche of Aura's veBAL BPT) |
| gnosis | multisig lm | `0x14969b55…` | BAL | 0.4277 | 0.43 | 1:1 | aggregated line |
| mainnet | 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x212f8842…` | sdBAL | 0.0010 | 0.01 | bpt | other-chain fee contracts line, ADDED in this patch |
| mainnet | BizDev Safe | `0xf3b4829c…` | BAL | 410,713.1046 | 410,713.10 | 1:1 | BizDev line |
| mainnet | DAO multisig | `0x10a19e7e…` | BAL | 13,974.9299 | 13,974.93 | 1:1 | aggregated line |
| mainnet | DAO multisig | `0x10a19e7e…` | auraBAL | 903.0793 | 4,195.55 | 90% tranche of Aura's veBAL lock (0.900000 BPT per auraBAL), at 5.162033 BAL per BPT | aggregated line |
| mainnet | DAO multisig | `0x10a19e7e…` | aEthBAL | 0.0140 | 0.01 | bal | aggregated line (0.01, below rounding) |
| mainnet | Onchain Ltd Safe | `0x16b00566…` | BAL | 235,321.5548 | 235,321.55 | 1:1 | Onchain Ltd line |
| mainnet | OpCo Safe | `0x3b8910f3…` | BAL | 408,730.3880 | 408,730.39 | 1:1 | OpCo line |
| mainnet | ProtocolFeesCollector (v2) | `0xce886865…` | BAL | 2,565.3119 | 2,565.31 | 1:1 | aggregated line |
| mainnet | ProtocolFeesCollector (v2) | `0xce886865…` | auraBAL | 434.2928 | 2,017.65 | 90% tranche of Aura's veBAL lock (0.900000 BPT per auraBAL), at 5.162033 BAL per BPT | aggregated line |
| mainnet | ProtocolFeesCollector (v2) | `0xce886865…` | sdBAL | 102.9787 | 531.58 | bpt | aggregated line, ADDED in this patch |
| mainnet | ProtocolFeesCollector (v2) | `0xce886865…` | B-80BAL-20WETH | 114.7394 | 592.29 | bpt | aggregated line |
| mainnet | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 5WBTC-10BAL-10WETH-75NODED | 177,764.9660 | 0.36 | share 0.3113% of pool BAL | ? |
| mainnet | Treasury Safe | `0x0efccbb9…` | BAL | 3,435,806.3544 | 3,435,806.35 | 1:1 | Treasury Safe line |
| mainnet | Treasury Safe | `0x0efccbb9…` | B-80BAL-20WETH | 21,827.0159 | 112,671.77 | bpt | Treasury Safe line (BPT) |
| mainnet | multisig blabs_fundraise | `0xb129f73f…` | BAL | 1,599,054.2900 | 1,599,054.29 | 1:1 | BLabs Fundraise line |
| mainnet | multisig blabs_team | `0xcdcebf1f…` | BAL | 928,041.3357 | 928,041.34 | 1:1 | BLabs Team line |
| mainnet | multisig grants_treasury | `0xe2c91f34…` | BAL | 1,569.1724 | 1,569.17 | 1:1 | aggregated line |
| optimism | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 33CRV-33SNX-33BAL | 4.3987 | 3.13 | share 95.0887% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| optimism | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 80BAL-20WETH | 0.2924 | 1.86 | share 2.0678% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| optimism | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 13wstETH-13sBTC-25aOptSUSD-25sEUR-6SNX-6AAVE-6BAL-6CRV | 0.1366 | 0.48 | share 24.4151% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| optimism | ProtocolFeesCollector (v2) | `0xce886865…` | unclassified token bpt-fraxethe / Fraximalist Ethereum | 0.1307 | not BAL | not resolved | other-chain fee contracts line, ADDED in this patch |
| optimism | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 33CRV-33SNX-33BAL | 0.0840 | 0.04 | share 100.0000% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| polygon | ProtocolFeesCollector (v2) | `0xce886865…` | BAL | 384.9049 | 384.90 | 1:1 | other-chain fee contracts line, ADDED in this patch |
| polygon | ProtocolFeesCollector (v2) | `0xce886865…` | tetuBAL | 2.8599 | 7.26 | payment rate 2.538962 BAL per tetuBAL | aggregated line |
| polygon | ProtocolFeesCollector (v2) | `0xce886865…` | unclassified token TETU / TETU | 433,165.2783 | not BAL | not resolved | other-chain fee contracts line, ADDED in this patch |
| polygon | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 20BAL-80TEL | 3,128.2402 | 17.13 | share 29.4756% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| polygon | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 10WMATIC-45SP-45BAL/StarSeeds_Protocol | 2,245.4033 | 0.06 | share 99.7008% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| polygon | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 15WMATIC-10BAL-15SAND-45GROSH-15TEL | 438.7096 | 0.50 | share 99.7887% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| polygon | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 6WMATIC-6WBTC-44BAL-44STARV3-M/StarSeeds_Protocol | 57.9844 | 0.01 | share 97.7457% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| polygon | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 40SOL-10BAL-50GROSH | 10.3973 | 0.19 | share 99.9198% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| polygon | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT balDE | 9.1515 | 0.07 | share 53.4120% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| polygon | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 25SD-25USDC-25BAL-25LDO | 2.1539 | 1.22 | share 99.0529% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| polygon | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT WM-HEX-BAL-SAND-GROSH | 2.0707 | 0.02 | share 81.4605% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| polygon | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 33TETU-33BAL-33AAVE | 0.0448 | 0.01 | share 99.8257% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| polygon | ProtocolFeesCollector (v2) | `0xce886865…` | v2 BPT 40WBTC-10SD-30WETH-10BAL-10LDO | 0.0034 | 1.35 | share 98.7895% of pool BAL | other-chain fee contracts line, ADDED in this patch |
| arbitrum | multisig _deprecated/maxi_ops | `0x5891b90c…` | unclassified token AURA / Aura | 2,859.3709 | not BAL | not resolved | not BAL (see notes) |
| arbitrum | multisig dao | `0xaf23dc59…` | unclassified token anyBAL / Balancer | 20,000.0000 | not BAL | not resolved | not BAL (see notes) |
| base | 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x2ff226cd…` | unclassified token WBCOIN / Wrapped Backed Coinbase Global | 0.0259 | not BAL | not resolved | not BAL |
| base | 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x2ff226cd…` | unclassified token BALAJIS / balajis | 164.5576 | not BAL | not resolved | not BAL |
| base | 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x2ff226cd…` | unclassified token AURA / Aura Finance | 1.2994 | not BAL | not resolved | not BAL |
| base | 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x2ff226cd…` | unclassified token BAL / Balancer | 1,739.0999 | not BAL | not resolved | not BAL |
| base | 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x2ff226cd…` | unclassified token aura / aura | 322.8937 | not BAL | not resolved | not BAL |
| base | 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x2ff226cd…` | unclassified token GORE / Global Oil Reserve Exchange | 100.0000 | not BAL | not resolved | not BAL |
| base | 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x2ff226cd…` | unclassified token MBG / Moon Bag Global | 27.0000 | not BAL | not resolved | not BAL |
| base | BizDev Safe | `0xf3b4829c…` | unclassified token MBG / Moon Bag Global | 52.0000 | not BAL | not resolved | not BAL (see notes) |
| base | multisig omni | `0x9ff471f9…` | unclassified token CGUSD / Cygnus Finance Global USD | 0.0000 | not BAL | not resolved | not BAL (see notes) |
| base | multisig omni | `0x9ff471f9…` | unclassified token GORE / Global Oil Reserve Exchange | 100.0000 | not BAL | not resolved | not BAL (see notes) |
| gnosis | 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0xa7d52404…` | unclassified token AURA / Aura Finance | 0.1593 | not BAL | not resolved | not BAL |
| mainnet | 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x212f8842…` | unclassified token AURA / Aura Finance | 106.2192 | not BAL | not resolved | not BAL |
| mainnet | 20250214-v3-protocol-fee-controller-v2/ProtocolFeeController | `0x212f8842…` | unclassified token kaiAURA / Kai Aura | 217.0119 | not BAL | not resolved | not BAL |
| mainnet | BizDev Safe | `0xf3b4829c…` | unclassified token YFIB / YFIBALANCER.FINANCE | 0.0200 | not BAL | not resolved | not BAL (see notes) |
| mainnet | Onchain Ltd Safe | `0x16b00566…` | unclassified token YFIB / YFIBALANCER.FINANCE | 0.0200 | not BAL | not resolved | not BAL (see notes) |
| mainnet | OpCo Safe | `0x3b8910f3…` | unclassified token YFIB / YFIBALANCER.FINANCE | 0.0200 | not BAL | not resolved | not BAL (see notes) |
| mainnet | ProtocolFeesCollector (v2) | `0xce886865…` | unclassified token AURA / Aura Finance | 20,595.8620 | not BAL | not resolved | not BAL (see notes) |
| mainnet | ProtocolFeesCollector (v2) | `0xce886865…` | unclassified token BPT / BlackPool | 0.1684 | not BAL | not resolved | not BAL (see notes) |
| mainnet | ProtocolFeesCollector (v2) | `0xce886865…` | unclassified token graviAURA / Gravitationally Bound AURA | 560.2821 | not BAL | not resolved | not BAL (see notes) |
| mainnet | ProtocolFeesCollector (v2) | `0xce886865…` | unclassified token ePyvBalancer-BoostedAaveUSD-04MAY23 / Element Principal Token yvBala | 18.2616 | not BAL | not resolved | not BAL (see notes) |
| mainnet | ProtocolFeesCollector (v2) | `0xce886865…` | unclassified token YFIB / YFIBALANCER.FINANCE | 0.0700 | not BAL | not resolved | not BAL (see notes) |
| mainnet | Treasury Safe | `0x0efccbb9…` | unclassified token rAURA / Redeemed AURA | 2,323,130.8466 | not BAL | not resolved | not BAL (see notes) |
| mainnet | Treasury Safe | `0x0efccbb9…` | unclassified token YFIB / YFIBALANCER.FINANCE | 0.0200 | not BAL | not resolved | not BAL (see notes) |
| mainnet | multisig _deprecated/maxi_ops | `0x166f54f4…` | unclassified token sdBal-gauge / Stake DAO sdBal Gauge | 0.0000 | not BAL | not resolved | not BAL (see notes) |
| mainnet | multisig alliance_program/lido | `0x87d93d9b…` | veBAL lock (BPT) | 4,954.6416 | 25,576.02 | bpt | not DAO-controlled (partner committee safe under BIP-812/822/829), stays in the denominator |
| mainnet | multisig alliance_program/rocket | `0xb867ea3b…` | veBAL lock (BPT) | 8,263.8619 | 42,658.32 | bpt | not DAO-controlled (partner committee safe under BIP-812/822/829), stays in the denominator |
| mainnet | multisig beets_treasury | `0xea06e1b4…` | BAL | 1,430.4804 | 1,430.48 | 1:1 | not DAO-controlled, stays in the denominator |
| mainnet | multisig beets_treasury | `0xea06e1b4…` | veBAL lock (BPT) | 9,464.4598 | 48,855.85 | bpt | not DAO-controlled, stays in the denominator |
| mainnet | multisig beets_treasury | `0xea06e1b4…` | unclassified token AURA / Aura Finance | 191,951.3020 | not BAL | not resolved | not DAO-controlled, stays in the denominator |
| mainnet | multisig beets_treasury | `0xea06e1b4…` | unclassified token YFIB / YFIBALANCER.FINANCE | 0.0200 | not BAL | not resolved | not DAO-controlled, stays in the denominator |
| mainnet | multisig blabs_fundraise | `0xb129f73f…` | unclassified token YFIB / YFIBALANCER.FINANCE | 0.0200 | not BAL | not resolved | not BAL (see notes) |
| mainnet | multisig blabs_team | `0xcdcebf1f…` | unclassified token YFIB / YFIBALANCER.FINANCE | 0.0200 | not BAL | not resolved | not BAL (see notes) |
| mainnet | multisig grants_treasury | `0xe2c91f34…` | unclassified token YFIB / YFIBALANCER.FINANCE | 0.0200 | not BAL | not resolved | not BAL (see notes) |
| mainnet | multisig stakedao_vebal_manager | `0xb0552b68…` | BAL | 1.5779 | 1.58 | 1:1 | not DAO-controlled, stays in the denominator |
| mainnet | multisig stakedao_vebal_manager | `0xb0552b68…` | unclassified token sdLUSD3CRV-f-gauge / Stake DAO LUSD3CRV-f Gauge | 0.3655 | not BAL | not resolved | not DAO-controlled, stays in the denominator |
| mainnet | multisig stakedao_vebal_manager | `0xb0552b68…` | unclassified token YFIB / YFIBALANCER.FINANCE | 0.0200 | not BAL | not resolved | not DAO-controlled, stays in the denominator |
| mainnet | multisig stakedao_vebal_manager | `0xb0552b68…` | unclassified token sdcbETH/ETH-f-gauge / Stake DAO cbETH/ETH-f Gauge | 0.0000 | not BAL | not resolved | not DAO-controlled, stays in the denominator |
| mainnet | multisig stakedao_vebal_manager | `0xb0552b68…` | unclassified token sdfrxETHCRV-gauge / Stake DAO frxETHCRV Gauge | 0.0000 | not BAL | not resolved | not DAO-controlled, stays in the denominator |
| optimism | multisig dao | `0x043f9687…` | unclassified token anyBAL / Balancer | 20,000.0000 | not BAL | not resolved | not BAL (see notes) |
| optimism | multisig maxi_beets_lm | `0x09df1626…` | BAL | 870.7491 | 870.75 | 1:1 | not DAO-controlled, stays in the denominator |
| polygon | multisig lm | `0xc38c5f97…` | unclassified token ABAL / Aave v3 BAL | 0.0001 | not BAL | not resolved | not BAL (see notes) |
| polygon | multisig lm | `0xc38c5f97…` | unclassified token 780 $UЅDС - Redeem: (t.ly/cpool) - #38 / $UЅDС TOKEN DISTRIBUTION | 1.0000 | not BAL | not resolved | not BAL (see notes) |

## Components of the summary's "other DAO-held BAL, aggregated" line

| component | BAL-equivalent |
|---|---:|
| DAO multisig | 18,170.48 |
| ProtocolFeesCollector | 5,175.25 |
| grants Safe | 1,569.17 |
| Gnosis LM multisig | 0.43 |
| ProtocolFeesCollector sdBAL, mainnet | 531.58 |
| v2 ProtocolFeesCollector, polygon (tetuBAL at the payment rate) | 412.73 |
| v2 ProtocolFeesCollector, arbitrum | 339.66 |
| v2 ProtocolFeesCollector, base | 239.84 |
| v2 ProtocolFeesCollector, gnosis | 92.47 |
| v2 ProtocolFeesCollector, optimism | 5.51 |
| V3 protocol fee controllers, five chains | 12.82 |
| **aggregated line** | **26,549.95** |

Not in it: the Optimism fees / maxi_beets_lm multisig (870.75 BAL), Beets-controlled, which stays in the denominator.

## What changed

| item | BAL-equivalent | applied to |
|---|---:|---|
| DAO claim on Aura's veBAL BPT: Treasury auraBAL on Gnosis (90% tranche) and rAURA (10% tranche), replacing the earlier auraBAL-only exclusion of 46,331.40 | 137,679.47 | Aura claim line |
| Treasury axlBAL on Arbitrum | 8,471.17 | Treasury Safe line |
| ProtocolFeesCollector sdBAL, mainnet | 531.58 | aggregated line |
| v2 ProtocolFeesCollector on Polygon, Arbitrum, Base, Gnosis, Optimism | 1,097.77 | new line |
| V3 protocol fee controllers | 12.82 | new line |
| **total newly excluded** | **146,224.15** | denominator 63,215,044.98 → 63,068,820.84 (after the Beets multisig, the auraBAL tranche basis and the tetuBAL payment rate were applied to the aggregated line) |

Left in the denominator, not DAO-controlled: Beets treasury (1,430.48 BAL and a 9,464.46 BPT veBAL lock), StakeDAO veBAL manager (1.58 BAL), and the two Alliance Program safes, Lido DAO Growth Committee `0x87D93d9B2C672bf9c9642d853a8682546a5012B5` (4,954.64 BPT locked, lock ends 24 Sep 2026) and Rocket Pool Incentive Management Committee `0xb867EA3bBC909954d737019FEf5AB25dFDb38CB9` (8,263.86 BPT locked, ends 19 Nov 2026), whose signers are the partners' under BIP-822 and BIP-829. Not BAL: AURA, kaiAURA, graviAURA, rAURA, TETU, Element principal tokens, BlackPool BPT, and spam tokens named BAL or USDC on Base. anyBAL held by the Arbitrum and Optimism DAO multisigs (20,000 each) has no backing and counts as zero.

## tetuBAL lock detail (moved from the summary)

`veBAL.locked()` at Ethereum block 25,977,785 (read on-chain): Tetu `BalLocker` `0x9cC56Fa7734DA21aC88F6a816aF10C5b898596Ce` 539,726.483105586104931977 BPT, lock end 8 April 2027; TETU_ST_BAL `0xFE700D523094Cc6C673d78F1446AE0743C89586E` 0 (its `totalSupply()` is 539,726.483105586104931842, the vault share that mirrors the lock); holder `0xBb84098e47d217f51cB014f692eada1F2280a179` 0; strategy `0x308a756b4f9aa3148cad7ccf8e72c18c758b2ef2` 0; deployer `0xbbbbb8C4364eC2ce52c59D2Ed3E56F307E529a94` 0. Payment = ½ × 539,726.483105586104931977 × 31,412,036.419940263341261971 / 6,074,087.188053669664018760 = 1,395,593.07 BAL, exact rational arithmetic, cap at the 549,670.662004021226732283 tetuBAL supply not binding. BalLocker verified source: no `delegatecall`, no generic call, no `selfdestruct`, no call to `veBAL.withdraw`; only `create_lock`, `increase_amount`, `increase_unlock_time`; not a proxy (EIP-1967 slot zero, 9,751 bytes of code).

## Aura claim detail

Aura VoterProxy `0xaF52695E1bB01A16D33D7194C28C42b10e0Dbec2` veBAL lock 3,684,354.766369 BPT, end 29 April 2027; auraBAL supply 3,684,353.766369; rAURA supply 46,033,045.186945 (all read on-chain at block 26,006,274). Treasury: 8,975.417770 auraBAL on Gnosis (block 48,317,898) → 8,077.88 BPT of the 90% tranche; 2,323,130.846614 rAURA → 18,593.68 BPT of the 10% tranche; total 26,671.56 BPT = 137,679.47 BAL at 5.162033. The 903.08 and 434.29 auraBAL held by the DAO multisig and the ProtocolFeesCollector are converted on the same tranche basis inside the aggregated line, 6,213.20 BAL.

## DAO-held BAL total (summary, section 2)

Summed lines: Treasury Safe (direct, BPT content, Arbitrum BAL and axlBAL), OpCo Safe, BizDev Safe, Onchain Ltd Safe, other DAO-held BAL aggregated, the Aura claim, and the Amber loan: 5,387,474.02 BAL, of which 1,395,593.07 is paid to tetuBAL holders at opening and redeems. Not summed: the two BLabs safes (Balancer Labs property, excluded by the proposal but not DAO-held) and the Tetu permalock (third-party BAL that can never redeem).
