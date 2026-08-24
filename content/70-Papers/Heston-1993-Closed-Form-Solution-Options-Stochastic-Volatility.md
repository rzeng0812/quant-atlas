---
type: paper
title: "A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options"
authors: ["Steven L. Heston"]
year: 1993
categories: ["q-fin.PR", "q-fin.CP"]
tags: [paper, classic, unread, pricing, options, stochastic-volatility, volatility-smile, derivatives, characteristic-function]
status: unread
added: 2026-08-23
journal: "Review of Financial Studies, 6(2), 327-343"
url: https://doi.org/10.1093/rfs/6.2.327
---

## Abstract
Heston derives a closed-form solution for European options when volatility follows a mean-reverting CIR process correlated with the asset price. The option price is obtained via characteristic function inversion (Fourier transform), yielding a semi-analytic formula. The Heston model captures the volatility smile/skew observed in options markets—impossible under constant-volatility BSM—through three mechanisms: mean reversion of variance (κ, θ), variance of variance (ξ), and correlation between asset and variance shocks (ρ, capturing the leverage effect). The model became the dominant stochastic volatility model in equity and FX derivatives pricing.

## Key Contribution
First closed-form (semi-analytic) option price under stochastic volatility. Captures volatility smile through four economically intuitive parameters. Characteristic function method for option pricing—now the standard approach. Correlation between asset and volatility (leverage effect). Still the dominant stochastic volatility model 30+ years later.

## Methods
Asset: dS = μS dt + √v S dW₁. Variance: dv = κ(θ - v)dt + ξ√v dW₂, with Corr(dW₁, dW₂) = ρ. Fourier transform of the characteristic function. Option price: C = S·P₁ - K·e^{-rT}·P₂ where P₁, P₂ obtained by integrating the characteristic function. Feller condition for non-negative variance: 2κθ > ξ².

## Results
Semi-analytic option prices via one-dimensional numerical integration. Reproduces BSM for ρ=0, ξ→0. Skew captured by ρ < 0 (negative correlation = left skew for equities). Term structure of implied volatility from mean reversion. Calibration to market smile via 5 parameters (κ, θ, ξ, ρ, v₀).

## Critique
Cannot fit steep short-term skew well (requires rough volatility or jumps). Calibration is non-convex—multiple local optima. CIR variance can hit zero when Feller condition violated (common in calibration). Rough Heston (El Euch-Rosenbaum) addresses some of these issues. Monte Carlo simulation requires careful discretization.

## Relevance
The dominant model for equity and FX options pricing. Every options desk uses Heston or a variant (Bates, SABR) as their primary model. Understanding Heston is essential for volatility surface modeling, exotic options pricing, and calibration. The characteristic function method introduced here is now the standard for more exotic processes.

## Related
- [[Black-Scholes-1973-Pricing-of-Options-and-Corporate-Liabilities]]
- [[Cox-Ingersoll-Ross-1985-Theory-Term-Structure-Interest-Rates]]
- [[Harrison-Pliska-1981-Martingales-and-Stochastic-Integrals]]
- [[Bollerslev-1986-GARCH]]
