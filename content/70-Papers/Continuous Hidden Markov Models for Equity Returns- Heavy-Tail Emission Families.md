---
type: paper
title: "Continuous Hidden Markov Models for Equity Returns: Heavy-Tail Emission Families and Regime-Conditional Value-at-Risk"
authors: ["Abdulrahman Alswaidan", "Cade Jin", "Jeffrey D. Varner"]
year: 2026
arxiv_id: 2606.23492v1
categories: ['q-fin.ST', 'q-fin.CP', 'q-fin.RM']
tags: [paper, unread, statistical-finance, computational-finance, risk]
status: unread
added: 2026-06-28
url: https://arxiv.org/abs/2606.23492v1
---

## Abstract
Synthetic generators of daily equity returns let practitioners stress test, backtest, and design scenarios that a single realized market history cannot supply, but only if the generator reproduces the stylized facts of real returns: heavy tails, negligible linear autocorrelation, and slow decay of the absolute-return autocorrelation. Hidden Markov models with few Gaussian states were long thought unable to reproduce that slow decay, and the standard fix was to abandon them for more complex hidden semi-Markov models. We revisit this issue with a continuous hidden Markov model whose regime chain governs the autocorrelation while per-regime densities govern the marginal, separating the temporal and distributional sides of the original failure. A unified expectation-maximization framework fits Gaussian, Student-t, Laplace, and generalized-error emissions under shared forward-backward recursions and quantile-based initialization, and a spectral identity bounds the number of decay modes by the rank of the centred transition matrix. Across SPY walk-forward folds, a sector-balanced 30-ticker panel, a CRSP cross-decade transfer, and a six-asset basket, that bound was not binding once a few states were used: heavy-tailed marginals, not additional decay modes, closed most of the fit gap, recovering volatility clustering above the i.i.d. baseline and narrowing the kurtosis gap without a tuning hyperparameter. The original failure is therefore distributional, not temporal. On daily US equities, a simple, interpretable Markov model suffices, and unlike a bootstrap or semi-Markov fit that wins only on a single-window fit, the fitted model also yields a regime-conditional Value-at-Risk that passes a joint conditional-coverage test and a copula that reproduces cross-asset correlations: one interpretable generator serving both path simulation and downstream risk and portfolio tasks.

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
