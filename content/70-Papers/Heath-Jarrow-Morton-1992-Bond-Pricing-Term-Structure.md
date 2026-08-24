---
type: paper
title: "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation"
authors: ["David Heath", "Robert Jarrow", "Andrew Morton"]
year: 1992
categories: ["q-fin.PR", "q-fin.MF"]
tags: [paper, classic, unread, interest-rates, term-structure, fixed-income, hjm, forward-rates, no-arbitrage]
status: unread
added: 2026-08-23
journal: "Econometrica, 60(1), 77-105"
---

## Abstract
Heath, Jarrow, and Morton introduce a general no-arbitrage framework for modeling the entire term structure of interest rates through the dynamics of instantaneous forward rates f(t,T). Rather than modeling the short rate, HJM directly models the evolution of the full yield curve. The key result—the HJM drift condition—states that under the risk-neutral measure, the drift of forward rates is completely determined by their volatility structure: α(t,T) = σ(t,T)·∫_t^T σ(t,s)ds. This unifying framework encompasses virtually all existing interest rate models (Vasicek, CIR, Hull-White) as special cases and directly led to the LIBOR Market Model.

## Key Contribution
Unified framework for the entire term structure via forward rate dynamics. HJM drift condition: no-arbitrage constraint on forward rate drifts. Encompasses all short-rate models as special cases. Directly led to the Brace-Gatarek-Musiela (BGM/LMM) LIBOR market model. Revolutionized multi-factor interest rate modeling.

## Methods
Forward rate dynamics: df(t,T) = α(t,T)dt + σ(t,T)dW(t). Change of measure via Girsanov: drift α(t,T) = σ(t,T)·∫_t^T σ(t,s)ds under Q. Bond price as exponential of integrated forward rates: P(t,T) = exp(-∫_t^T f(t,s)ds). Specification of volatility structure σ(t,T) determines the model.

## Results
HJM drift condition: drift of forward rates uniquely determined by volatility under Q. Vasicek: σ(t,T) = σe^{-κ(T-t)} is a special case. HJM with deterministic volatility = Gaussian interest rate model. Non-Markovian in general (path-dependent forward rates). Markovian when σ depends only on f(t,T) in specific ways.

## Critique
General HJM is non-Markovian → infinite-dimensional state space → computationally intractable in general. Requires Musiela's parameterization or discretization to implement. Special cases (proportional volatility → LMM) required for practical tractability. Non-negative rate constraint not automatically satisfied.

## Relevance
The theoretical foundation for all multi-factor interest rate modeling. The LIBOR Market Model (BGM, 1997)—the industry standard for exotic interest rate derivatives—is a direct application of HJM with log-normal forward LIBOR rates. Understanding HJM is essential for sophisticated fixed income modeling, swaption markets, and CMS products.

## Related
- [[Vasicek-1977-Equilibrium-Characterization-Term-Structure]]
- [[Hull-White-1990-Pricing-Interest-Rate-Derivative-Securities]]
- [[Black-1976-Pricing-of-Commodity-Contracts]]
