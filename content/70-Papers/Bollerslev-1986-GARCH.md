---
type: paper
title: "Generalized Autoregressive Conditional Heteroskedasticity"
authors: ["Tim Bollerslev"]
year: 1986
categories: ["q-fin.ST", "q-fin.RM"]
tags: [paper, classic, unread, volatility, garch, arch, time-series, statistical-finance, risk, volatility-clustering]
status: unread
added: 2026-08-23
journal: "Journal of Econometrics, 31(3), 307-327"
---

## Abstract
Bollerslev generalizes Engle's ARCH model to GARCH (Generalized ARCH) by allowing the conditional variance to depend on both past squared residuals (ARCH terms) and past conditional variances (GARCH terms): h_t = ω + α·ε²_{t-1} + β·h_{t-1}. The GARCH(1,1) model captures the high persistence in financial volatility with just three parameters, far outperforming high-order ARCH. GARCH became the workhorse model for financial volatility forecasting, return distribution modeling, option pricing, and risk management.

## Key Contribution
Introduced GARCH: the parsimonious generalization of ARCH. GARCH(1,1) as the universal volatility model (α + β ≈ 0.95-0.98 for most financial series). Solved the parameter explosion problem of high-order ARCH. Proved stationarity conditions (α + β < 1). Variance targeting for parameter estimation. Foundation of all GARCH extensions (EGARCH, GJR-GARCH, DCC-GARCH, etc.).

## Methods
GARCH(1,1): h_t = ω + α·ε²_{t-1} + β·h_{t-1}. More generally GARCH(p,q): h_t = ω + Σαᵢε²_{t-i} + Σβⱼh_{t-j}. ARCH(∞) representation: GARCH is an ARMA model for ε²_t. MLE under Gaussian or Student-t conditional distribution. Quasi-MLE (QMLE) properties.

## Results
GARCH(1,1) fits financial volatility with 3 parameters. Stationarity: α + β < 1. Persistence: half-life of volatility shocks = ln(0.5)/ln(α+β). IGARCH (α+β=1): integrated GARCH, infinite persistence. Long-run variance: ω/(1-α-β).

## Critique
Symmetric response to positive and negative shocks (leverage effect not captured—requires EGARCH or GJR-GARCH). Gaussian errors understate fat tails in practice. IGARCH (near-unit root in variance) common in practice. Multivariate GARCH (DCC) is computationally challenging.

## Relevance
The most widely used financial volatility model. VaR calculations, option pricing under stochastic volatility, and portfolio risk estimation all commonly rely on GARCH. Every quant needs to understand GARCH before studying more sophisticated volatility models. Standard benchmark in volatility forecasting competitions.

## Related
- [[Engle-1982-ARCH]]
- [[Heston-1993-Closed-Form-Solution-Options-Stochastic-Volatility]]
- [[Cont-2001-Empirical-Properties-Asset-Returns-Stylized-Facts]]
- [[Mandelbrot-1963-Variation-of-Certain-Speculative-Prices]]
