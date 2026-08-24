---
type: paper
title: "The Pricing of Options and Corporate Liabilities"
authors: ["Fischer Black", "Myron Scholes"]
year: 1973
categories: ["q-fin.PR", "q-fin.MF"]
tags: [paper, classic, unread, pricing, options, black-scholes, hedging, derivatives, replication]
status: unread
added: 2026-08-23
journal: "Journal of Political Economy, 81(3), 637-654"
url: https://doi.org/10.1086/260062
---

## Abstract
Black and Scholes derive a closed-form formula for European option prices by constructing a continuously rebalanced delta hedge that eliminates all risk. Under log-normal returns, constant volatility, no dividends, continuous trading, and frictionless markets, the option price satisfies a parabolic PDE (the Black-Scholes PDE). The solution yields the BSM formula: C = S·N(d1) - K·e^(-rT)·N(d2). They also show that corporate equity can be viewed as a call option on the firm's assets, linking option pricing to corporate finance. This paper founded modern quantitative finance and earned Scholes and Merton (for simultaneous contributions) the 1997 Nobel Prize.

## Key Contribution
First closed-form option pricing formula from first principles (no expected return needed). Introduced delta hedging and dynamic replication. The Black-Scholes PDE as the fundamental equation of derivatives pricing. Linked option pricing to corporate capital structure. Founded the multi-trillion dollar derivatives industry.

## Methods
Geometric Brownian Motion for the underlying asset. Delta hedging: long option, short Δ shares to eliminate risk. No-arbitrage: the hedged portfolio earns the risk-free rate. Derived the BSM PDE: ∂V/∂t + ½σ²S²∂²V/∂S² + rS∂V/∂S - rV = 0. Solved PDE with boundary conditions to get C = S·N(d1) - Ke^{-rT}·N(d2).

## Results
BSM formula for European call: C = S·N(d1) - K·e^{-rT}·N(d2). Greeks: Delta = N(d1), Gamma, Theta, Vega, Rho. Put-call parity. Equity as a call option on firm assets. The "implied volatility" as the market's inversion of the formula.

## Critique
Constant volatility assumption violated in practice (volatility smile/skew). Log-normal returns have thin tails. No dividends in original model (extended by Merton). Continuous trading and no transaction costs are idealizations. Model risk: every model is wrong, this one is famously useful.

## Relevance
The single most important paper in quantitative finance. Every options trader uses BSM or extensions as the starting point. Implied volatility—inverted from BSM—is the standard quoting convention for options. The BSM PDE is the foundation for all derivatives pricing.

## Related
- [[Merton-1973-Theory-of-Rational-Option-Pricing]]
- [[Cox-Ross-Rubinstein-1979-Option-Pricing-Simplified-Approach]]
- [[Heston-1993-Closed-Form-Solution-Options-Stochastic-Volatility]]
- [[Black-1976-Pricing-of-Commodity-Contracts]]
- [[Merton-1974-Pricing-Corporate-Debt]]
