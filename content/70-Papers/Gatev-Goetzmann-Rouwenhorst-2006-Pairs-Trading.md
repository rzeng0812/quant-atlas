---
type: paper
title: "Pairs Trading: Performance of a Relative-Value Arbitrage Rule"
authors: ["Evan Gatev", "William N. Goetzmann", "K. Geert Rouwenhorst"]
year: 2006
categories: ["q-fin.PM", "q-fin.ST"]
tags: [paper, classic, unread, statistical-arbitrage, pairs-trading, mean-reversion, algorithmic-trading, convergence-trading]
status: unread
added: 2026-08-23
journal: "Review of Financial Studies, 19(3), 797-827"
---

## Abstract
Gatev, Goetzmann, and Rouwenhorst provide the first comprehensive academic study of pairs trading, a relative-value strategy that identifies pairs of stocks with similar price histories and trades the spread when prices diverge beyond a threshold (typically 2 standard deviations). Using US equity data from 1962-2002, they document annualized excess returns of approximately 11% (self-financing) before transaction costs, declining over time. Returns are not explained by market, size, value, or momentum factors and appear orthogonal to known risk factors. The strategy is mean-reverting by construction.

## Key Contribution
First systematic academic study of pairs trading. Defined the standard pairs trading methodology (distance approach). Showed significant risk-adjusted returns over 40 years. Returns not explained by standard risk factors. Documented the declining profitability of pairs trading post-1990s (arbitrage capital). Founded the academic literature on statistical arbitrage.

## Methods
Formation period (12 months): calculate normalized price series for each stock, find pairs with minimum sum of squared deviations. Trading period (6 months): open position when prices diverge by 2σ, close on convergence or end of period. Returns computed as self-financing positions (long/short equal-weight). Risk adjustment: Fama-French-Carhart four-factor model.

## Results
Annual excess returns: ~11% (top 5 pairs by distance), ~8% (top 20 pairs). Returns not significantly related to Fama-French-Carhart factors. Returns declining over time: higher in 1960s-70s, lower in 1990s-2000s. Pairs diverge about 18% of the time; most converge within 6 months. Risk: occasional failures to converge (pair breakdowns).

## Critique
Transaction costs (bid-ask spread, short selling) significantly reduce net returns. The "distance" approach is crude—cointegration-based or PCA-based approaches more sophisticated. Requires identifying economically similar pairs a priori. Mean-reversion not guaranteed—pair divergence can be permanent (fundamental change). Results have weakened further post-2006.

## Relevance
The foundational academic reference for statistical arbitrage. Pairs trading is still widely practiced by hedge funds. Motivates cointegration-based, Kalman filter, and machine learning extensions. The methodology is the basis for equity long-short market-neutral strategies and relative-value funds.

## Related
- [[Lo-MacKinlay-1988-Stock-Prices-Do-Not-Follow-Random-Walks]]
- [[Jegadeesh-Titman-1993-Returns-Buying-Winners-Selling-Losers]]
- [[Fama-1970-Efficient-Capital-Markets]]
