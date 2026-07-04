---
type: learning-path
title: Risk and Portfolio
goal: Measure and manage portfolio risk; understand how to size positions and evaluate strategy performance
prereqs:
  - Basic statistics
  - "[[01-Paths/Path-01-Derivatives-Foundation]]"
tags: [path, risk, portfolio]
status: active
created: 2026-04-18
---

## Goal
Learn the core toolkit for measuring what can go wrong in a portfolio and deciding how much to bet. Move from intuitive performance metrics (Sharpe, drawdown) through regulatory risk measures (VaR, Expected Shortfall) to return decomposition via factor models, and finish with Kelly Criterion for principled position sizing. After this path you can evaluate a strategy's risk-adjusted performance, stress-test a portfolio, and size positions without overbetting.

## Prerequisites
- Basic statistics — mean, variance, covariance, normal distribution, and linear regression. These are used throughout.
- [[01-Paths/Path-01-Derivatives-Foundation]] — optional but helpful for the VaR/ES sections when options are in the portfolio.

## Curriculum

| # | Concept | Primary Source | Status | Notes |
|---|---------|---------------|--------|-------|
| 1 | [[Markowitz Mean-Variance Optimization]] | any quant text | math | Foundation of portfolio theory; efficient allocation |
| 2 | [[Efficient Frontier]] | any quant text | math | Visual/geometric output of MVO |
| 3 | [[CAPM]] | Sharpe (1964) | math | Equilibrium extension of Markowitz; beta and market risk premium |
| 4 | [[Sharpe Ratio]] | any quant finance text | math | Baseline risk-adjusted performance metric |
| 5 | [[Maximum Drawdown]] | any quant finance text | math | Tail risk intuition; path-dependent loss measure |
| 6 | [[Value at Risk]] | Hull ch.22 | math | Regulatory standard; percentile loss over a horizon |
| 7 | [[Expected Shortfall]] | Hull ch.22 | math | Coherent replacement for VaR; average loss beyond threshold |
| 8 | [[Factor Models]] | Fama & French (1993) | math | Decompose portfolio return and risk into systematic factors |
| 9 | [[Kelly Criterion]] | Kelly (1956) | math | Optimal position sizing; maximize long-run growth rate |
| 10 | [[Risk Parity]] | Bridgewater / Qian (2005) | math | Risk-based allocation; alternative to MVO |
| 11 | [[Stress Testing]] | Hull ch.22 | math | Scenario analysis beyond VaR |
| 12 | [[Correlation and Covariance Estimation]] | Lopez de Prado ch.2 | math | Input reliability for MVO and risk models |
| 13 | [[Monte Carlo Methods]] | Glasserman ch.1 | math | Simulation for VaR/ES when closed form unavailable |

## Source Stack
1. **Hull — Options, Futures & Other Derivatives** — ch.22
   - Primary source for VaR and Expected Shortfall. Clear numerical examples and regulatory context.
2. **Fama & French (1993) — "Common Risk Factors in the Returns on Stocks and Bonds"**
   - The canonical factor model paper. Read to understand the framework, then apply to strategy analysis.
3. **Kelly (1956) — "A New Interpretation of Information Rate"**
   - The original Kelly paper is short and worth reading directly. Supplement with any modern treatment for practical fractional Kelly.
4. **Any introductory quant finance text** (e.g., Joshi, Wilmott, or Quantitative Finance by Riskworx)
   - For Sharpe Ratio and Maximum Drawdown; these are covered well in most survey texts.

## Session Log

### 2026-04-18
- Path created.

## What's Next
- [[01-Paths/Path-05-Trading-Strategies]] — apply the risk measurement tools built here to real strategy construction and backtesting
