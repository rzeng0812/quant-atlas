---
type: paper
title: "Valuing American Options by Simulation: A Simple Least-Squares Approach"
authors: ["Francis A. Longstaff", "Eduardo S. Schwartz"]
year: 2001
categories: ["q-fin.CP", "q-fin.PR"]
tags: [paper, classic, unread, pricing, american-options, monte-carlo, computational-finance, lsm, simulation]
status: unread
added: 2026-08-23
journal: "Review of Financial Studies, 14(1), 113-147"
---

## Abstract
Longstaff and Schwartz introduce the Least-Squares Monte Carlo (LSM) algorithm for pricing American and Bermudan options by simulation. At each exercise date, the continuation value is estimated by ordinary least-squares regression of realized discounted payoffs on a set of basis functions of the state variables (e.g., polynomials of the asset price). Comparing the estimated continuation value to the immediate exercise payoff determines the optimal exercise decision. Options are then priced by forward simulation applying the learned exercise strategy. This tractable, flexible approach revolutionized the pricing of complex options in high-dimensional settings.

## Key Contribution
Introduced LSM algorithm—the standard method for American/Bermudan options via Monte Carlo. Solved the "simulation + backward induction" problem elegantly. Applies to any state space dimension (avoids curse of dimensionality of tree methods). Naturally handles path-dependent underlying dynamics. Now universally implemented in quant finance systems.

## Methods
Forward simulation of M paths of state variables. Backward induction: at each exercise date t_k, regress V(t_{k+1}) on basis functions of X(t_k) (Laguerre polynomials). Estimate continuation value Ĉ(t_k, X) = Σ βⱼ·ψⱼ(X). Exercise if payoff(X) > Ĉ(X). Compute option price as average over paths.

## Results
LSM gives biased-low estimate (high variance paths may not be optimal to exercise in-sample). Upper bound via duality (Haugh-Kogan, Rogers) available. Shown to converge to true price as M → ∞ and number of basis functions → ∞. Outperforms tree methods for high-dimensional and path-dependent options.

## Critique
Regression basis function choice is critical. In-sample exercise strategy biased (low by Jensen's inequality for standard regression). High-dimensional state spaces require many paths and basis functions. Computational cost grows with paths × time steps × assets. Machine learning extensions (neural network continuation value) are active research area.

## Relevance
LSM is implemented in every major quant library (QuantLib, internal bank systems). Essential for Bermudan swaptions (the most complex fixed income derivative), callable bonds, variable annuities, and real options. Understanding LSM is required for any quant doing Monte Carlo-based derivatives pricing.

## Related
- [[Merton-1973-Theory-of-Rational-Option-Pricing]]
- [[Cox-Ross-Rubinstein-1979-Option-Pricing-Simplified-Approach]]
- [[Black-Scholes-1973-Pricing-of-Options-and-Corporate-Liabilities]]
- [[Heston-1993-Closed-Form-Solution-Options-Stochastic-Volatility]]
