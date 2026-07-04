---
type: paper
title: "A Hybrid Gaussian Process Regression Framework for Stable Volatility-Covariance Estimation: Evidence from Global Equity Indices"
authors: ["Ujjwala Vadrevu"]
year: 2026
arxiv_id: 2605.17275v1
categories: ['q-fin.RM', 'cs.LG']
tags: [paper, unread, risk, machine-learning]
status: unread
added: 2026-05-24
url: https://arxiv.org/abs/2605.17275v1
---

## Abstract
Accurate forecasting of the Volatility-Covariance Matrix (VCV) is central to regulatory capital adequacy processes such as the Internal Capital Adequacy Assessment Process (ICAAP) and the Comprehensive Capital Analysis and Review (CCAR). Traditional econometric models, including GARCH-family and Exponentially Weighted Moving Average (EWMA) approaches, suffer from parametric rigidity, distributional assumptions, and numerical instability under stress, leading to systematic underestimation of tail risk. This paper proposes and validates a novel Hybrid Gaussian Process Regression-Historical Simulation (GPR-HS) framework for estimating Value-at-Risk (VaR) and Expected Shortfall (ES) across a diversified portfolio of seven major global equity indices. The framework decouples the VCV estimation problem: individual asset volatilities are modelled dynamically using Univariate GPR with a Matern 5/2 kernel, while inter-asset correlations are estimated via stable historical covariance. A key methodological contribution is the Aggressive Noise Initialization (ANI) strategy, which sets the initial White Noise kernel variance equal to the empirical variance of the training returns, ensuring Gram matrix positive-definiteness, regularization, and conservative, regulatory-compliant forecasts. Evaluated using an expanding window forward-chaining cross-validation scheme over June 2020 -June 2025, the GPR-HS framework achieves regulatory compliance in the majority of test splits; including a 100% ES pass rate at the portfolio level, while outperforming the static Historical VaR benchmark in 71.4% of univariate cases by Quadratic Loss and 100% of cases by violation count.

## Key Contribution
*Fill after reading.*

## Methods
*Fill after reading.*

## Results
*Fill after reading.*

## Critique
*Fill after reading.*

## Relevance
*Fill after reading.*

## Related
-
