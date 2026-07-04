---
type: learning-path
title: Trading Strategies
goal: Understand the main families of systematic trading strategies and how to evaluate them
prereqs:
  - "[[01-Paths/Path-04-Risk-and-Portfolio]]"
tags: [path]
status: active
created: 2026-04-18
---

## Goal
Survey the principal families of systematic strategies — mean reversion, statistical arbitrage, momentum, and market making — and understand the statistical and economic logic behind each. By the end, you can read a strategy description, identify which family it belongs to, and apply the right evaluation framework (Sharpe, MaxDD, factor exposure) to assess it.

## Prerequisites
- [[01-Paths/Path-04-Risk-and-Portfolio]] — Sharpe ratio, Max Drawdown, and Factor Models are used throughout to evaluate every strategy discussed here

## Curriculum

| # | Concept | Primary Source | Status | Notes |
|---|---------|---------------|--------|-------|
| 1 | [[Mean Reversion]] | Lopez de Prado ch.2 | math | Statistical foundation for all arb strategies |
| 2 | [[Statistical Arbitrage]] | Lopez de Prado ch.5 | math | General framework; encompasses pairs and beyond |
| 3 | [[Pairs Trading]] | Gatev et al. (2006) | math | Simplest stat arb; concrete cointegration example |
| 4 | [[Momentum]] | Jegadeesh & Titman (1993) | math | Trend-following foundation; cross-sectional & time-series |
| 5 | [[Carry Strategies]] | AQR / Koijen et al. (2018) | math | Harvesting carry premium across asset classes |
| 6 | [[CTA and Trend Following]] | Faber (2007) | math | Systematic trend-following in practice |
| 7 | [[Market Making]] | Cartea et al. ch.4 | math | Liquidity provision as a systematic strategy |
| 8 | [[Options Strategies]] | Hull ch.11 | math | Spreads, straddles, and structured payoffs |
| 9 | [[Volatility Arbitrage]] | Gatheral / practitioner lit | math | Trade implied vs realized vol; vega risk |
| 10 | [[Backtesting Methodology]] | Lopez de Prado ch.11 | math | Essential meta-skill: validate before you trust |

## Source Stack
1. **Lopez de Prado — Advances in Financial Machine Learning** — ch.2, 5
   - Primary source for mean reversion and stat arb. Dense but authoritative. Read ch.2 before ch.5.
2. **Cartea, Jaimungal & Penalva — Algorithmic and High-Frequency Trading** — ch.4
   - Best treatment of market making as a strategy. Bridges theory and practice.
3. **Gatev, Goetzmann & Rouwenhorst (2006) — "Pairs Trading: Performance of a Relative Value Arbitrage Rule"**
   - The canonical pairs trading paper. Read alongside Lopez de Prado ch.5.
4. **Jegadeesh & Titman (1993) — "Returns to Buying Winners and Selling Losers"**
   - The foundational momentum paper. Short read; high information density.

## Session Log

### 2026-04-18
- Path created.

## What's Next
- [[01-Paths/Path-06-Market-Microstructure]] — execution: how to actually trade these strategies without being picked off
- [[01-Paths/Path-07-ML-Finance]] — signal generation: using ML to improve entry/exit signals
