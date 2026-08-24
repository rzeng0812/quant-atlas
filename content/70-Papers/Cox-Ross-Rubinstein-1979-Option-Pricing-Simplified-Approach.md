---
type: paper
title: "Option Pricing: A Simplified Approach"
authors: ["John C. Cox", "Stephen A. Ross", "Mark Rubinstein"]
year: 1979
categories: ["q-fin.PR", "q-fin.CP"]
tags: [paper, classic, unread, pricing, options, binomial-model, american-options, computational-finance, risk-neutral-pricing]
status: unread
added: 2026-08-23
journal: "Journal of Financial Economics, 7(3), 229-263"
---

## Abstract
Cox, Ross, and Rubinstein introduce the binomial option pricing model as an intuitive and computationally tractable alternative to BSM. The model discretizes time into periods where the asset price moves up by factor u or down by factor d. Risk-neutral probabilities are derived from the no-arbitrage condition, and option values are computed by backward induction from expiry. As the number of periods n → ∞, the binomial model converges to BSM. Critically, the binomial tree naturally handles American option early exercise by comparing continuation value to intrinsic value at each node.

## Key Contribution
Made option pricing elementary and computational. Introduced risk-neutral pricing in a discrete, intuitive setting. Natural framework for American option valuation. Convergence to BSM proved. Widely taught as the canonical option pricing model. Foundation for all tree-based numerical methods in derivatives.

## Methods
Binomial lattice for underlying price. Risk-neutral probabilities: p = (e^{rΔt} - d)/(u - d). Backward induction: V(t) = e^{-rΔt}[p·V_u + (1-p)·V_d]. American option: compare to intrinsic value at each node. Convergence: u = e^{σ√Δt}, d = 1/u → BSM as n → ∞.

## Results
Closed-form risk-neutral pricing formula in discrete time. Automatic American option pricing. Dividends naturally incorporated by adjusting the tree. Converges to BSM for European options. Trinomial trees as a straightforward extension.

## Critique
Slow convergence for some options (especially near the money or with barriers). More computationally intensive than BSM for European options. Oscillation in Greeks for discrete trees. Superseded by Monte Carlo (for path-dependent options) and finite difference methods for more complex derivatives.

## Relevance
The most widely taught option pricing model. Every options textbook starts here. The risk-neutral pricing intuition (p = (F/S - d)/(u - d)) is the clearest explanation of risk-neutral valuation. Still used in practice for equity options with early exercise and for calibrating implied trees.

## Related
- [[Black-Scholes-1973-Pricing-of-Options-and-Corporate-Liabilities]]
- [[Merton-1973-Theory-of-Rational-Option-Pricing]]
- [[Longstaff-Schwartz-2001-Valuing-American-Options-LSM]]
- [[Harrison-Kreps-1979-Martingales-and-Arbitrage]]
