---
type: paper
title: "Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation"
authors: ["Robert F. Engle"]
year: 1982
categories: ["q-fin.ST", "q-fin.RM"]
tags: [paper, classic, unread, volatility, arch, garch, time-series, statistical-finance, risk, volatility-clustering]
status: unread
added: 2026-08-23
journal: "Econometrica, 50(4), 987-1007"
url: https://doi.org/10.2307/1912773
---

## Abstract
Engle introduces the ARCH (Autoregressive Conditional Heteroscedasticity) model to capture the empirically observed phenomenon that large price changes tend to be followed by large changes—volatility clustering. The model specifies that the conditional variance of a time series depends on past squared residuals: σ²_t = ω + α₁ε²_{t-1} + ... + αₚε²_{t-p}. Applied to UK inflation data, ARCH successfully models the time-varying uncertainty in macroeconomic forecasts. This work earned Engle the 2003 Nobel Prize in Economics and spawned an enormous literature on volatility models including GARCH, EGARCH, GJR-GARCH, and many others.

## Key Contribution
Introduced ARCH: the first formal model of time-varying conditional variance. Proved volatility clustering can be modeled parametrically. Provided MLE estimation procedure. Introduced LM test for ARCH effects. Earned the 2003 Nobel Prize in Economics. Foundation of all GARCH-family volatility models.

## Methods
Conditional variance model: ht = ω + Σαᵢε²_{t-i}. Maximum likelihood estimation under normality or t-distribution. Lagrange multiplier (LM) test for ARCH effects (test H₀: α₁=...=αₚ=0). Applied to UK CPI inflation 1958-1977.

## Results
UK inflation variance is time-varying and predictable from past squared residuals. ARCH(4) fits significantly better than constant variance. Forecasts of inflation uncertainty improve substantially. Stationarity requires Σαᵢ < 1.

## Critique
High-order ARCH models require many parameters to capture persistence. Long lag lengths needed for financial data (volatility persistence is very high). Superseded by GARCH (Bollerslev 1986) for parsimony. Does not capture the leverage effect (asymmetric volatility response to up vs. down moves).

## Relevance
The father of all conditional volatility models. Every VaR model, option pricing model with stochastic volatility, and risk management system uses ARCH/GARCH as a core component. Understanding ARCH is prerequisite to GARCH, E-GARCH, GJR-GARCH, realized volatility models, and option-implied volatility.

## Related
- [[Bollerslev-1986-GARCH]]
- [[Mandelbrot-1963-Variation-of-Certain-Speculative-Prices]]
- [[Heston-1993-Closed-Form-Solution-Options-Stochastic-Volatility]]
- [[Cont-2001-Empirical-Properties-Asset-Returns-Stylized-Facts]]
