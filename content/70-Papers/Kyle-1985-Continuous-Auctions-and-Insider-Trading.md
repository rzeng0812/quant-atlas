---
type: paper
title: "Continuous Auctions and Insider Trading"
authors: ["Albert S. Kyle"]
year: 1985
categories: ["q-fin.TR", "q-fin.MF"]
tags: [paper, classic, unread, market-microstructure, price-impact, informed-trading, liquidity, kyle-lambda, market-depth]
status: unread
added: 2026-08-23
journal: "Econometrica, 53(6), 1315-1335"
url: https://doi.org/10.2307/1913210
---

## Abstract
Kyle develops a game-theoretic model of strategic trading by a single informed insider competing against noise traders and a risk-neutral, competitive market maker. In the continuous-time limit, the informed trader optimally spreads trades over the entire trading period to conceal information gradually, revealing it only as trading concludes. The key equilibrium result: market depth (lambda, λ)—the price impact per unit of order flow—is constant throughout the day and determined by the ratio of insider information to noise trading. Kyle's λ became the canonical measure of market liquidity and price impact.

## Key Contribution
Founded the modern theory of strategic informed trading. Introduced Kyle's λ as the price impact coefficient. Showed that informed traders optimally disguise trades as noise. Derived the linear equilibrium in a Gaussian setting. Kyle's λ is now the universal measure of market depth/illiquidity. Foundation for all subsequent market microstructure and price impact models.

## Methods
Three players: informed trader (private signal V), noise traders (order flow u), market maker (sets price). Linear equilibrium: insider submits x = β(V - p₀), price set by market maker: Δp = λ·(x + u). Solving the resulting ODE for the continuous-time limit. Gaussian signals and noise.

## Results
Kyle's λ = σ_v / (2σ_u) where σ_v is information volatility, σ_u is noise trading. Informed trader reveals information at a constant rate over [0,T]. Market depth 1/λ is higher when noise trading is greater. Price converges to true value V by time T. The insider captures exactly half the total information value as profit.

## Critique
Single informed trader (no competition between informed traders). Linear equilibrium (unique but restrictive). No transaction costs for market maker. Continuous time—requires non-trivial math. Extensions to multiple informed traders (Kyle 1989), multiple assets, and dynamic settings are significant papers in themselves.

## Relevance
Kyle's λ is used in every market microstructure paper and in algorithmic trading research. The price impact framework (ΔP = λ·Q) is the foundation of execution cost models (Almgren-Chriss) and LOB models. Essential for understanding adverse selection, market making, and transaction cost analysis (TCA).

## Related
- [[Glosten-Milgrom-1985-Bid-Ask-Transaction-Prices]]
- [[Almgren-Chriss-2001-Optimal-Execution-Portfolio-Transactions]]
- [[Avellaneda-Stoikov-2008-High-Frequency-Trading-Limit-Order-Book]]
