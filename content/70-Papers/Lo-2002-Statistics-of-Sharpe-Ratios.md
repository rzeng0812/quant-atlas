---
type: paper
title: "The Statistics of Sharpe Ratios"
authors: ["Andrew W. Lo"]
year: 2002
categories: ["q-fin.PM", "q-fin.ST"]
tags: [paper, classic, unread, portfolio-management, sharpe-ratio, performance-evaluation, statistical-finance, autocorrelation]
status: unread
added: 2026-08-23
journal: "Financial Analysts Journal, 58(4), 36-52"
---

## Abstract
Lo derives the asymptotic distribution of the Sharpe ratio under both IID and non-IID return assumptions. Under IID, the annualized Sharpe ratio SR_A = √T · SR_monthly is asymptotically normal with standard deviation √(1/T·(1 + SR²/2)). When returns exhibit autocorrelation (as hedge fund and momentum strategy returns often do), the standard formula for annualizing the Sharpe ratio overstates statistical significance substantially. Lo derives an autocorrelation-adjusted Sharpe ratio and shows that many reported Sharpe ratios in the industry are statistically indistinguishable from zero. This paper is essential for rigorous performance evaluation.

## Key Contribution
Derived the asymptotic distribution of the Sharpe ratio under IID and autocorrelated returns. Showed that standard annualization (SR_A = √12 · SR_monthly) is incorrect under autocorrelation. Provided autocorrelation-adjusted Sharpe ratio formula. Showed many published Sharpe ratios are statistically insignificant. Foundation for rigorous performance evaluation and hypothesis testing.

## Methods
Delta method for asymptotic distribution of SR under IID. Generalization to stationary time series with autocorrelation (Newey-West type correction). SR^A = (μ/σ)·√T where adjustment factor η(ρ) = 1 + 2Σₖρₖ (1-k/n). Applied to hedge fund returns (significant positive autocorrelation → SR overstated by 50-70%). Monte Carlo validation.

## Results
IID case: Var(SR_A) ≈ (1 + SR²/2)/T. Autocorrelated case: effective "annual observations" reduced; autocorrelation correction factor η > 1 inflates the variance. High autocorrelation (ρ₁ ≈ 0.5): SR overstated by factor √(η) ≈ 1.4 - 1.7. Implication: many hedge funds with reported SR > 1 are actually not statistically different from 0.

## Critique
Assumes stationarity of return series. Only first-order autocorrelation correction discussed in detail. Does not address non-stationarity (structural breaks, regime changes). Multiple testing / selection bias (among many strategies, best one has higher SR by luck) not addressed—see Bailey-Prado-López de Prado for that.

## Relevance
Required reading for anyone evaluating or reporting investment strategy performance. The autocorrelation adjustment is critical for hedge funds, fixed income strategies, and any strategy with illiquid or smoothed returns. The confidence interval for the Sharpe ratio is used in strategy selection and fund-of-funds evaluation. Directly relevant to the "backtest overfitting" and p-hacking debates in quantitative finance.

## Related
- [[Grinold-1989-Fundamental-Law-Active-Management]]
- [[Markowitz-1952-Portfolio-Selection]]
- [[Fama-French-1993-Common-Risk-Factors]]
- [[Lo-MacKinlay-1988-Stock-Prices-Do-Not-Follow-Random-Walks]]
