---
type: paper
title: "Theory of Rational Option Pricing"
authors: ["Robert C. Merton"]
year: 1973
categories: ["q-fin.PR", "q-fin.MF"]
tags: [paper, classic, unread, pricing, options, continuous-time, derivatives, american-options]
status: unread
added: 2026-08-23
journal: "Bell Journal of Economics and Management Science, 4(1), 141-183"
---

## Abstract
Merton rigorously extends and generalizes the Black-Scholes framework using Itô's stochastic calculus. He derives the general properties any rational option price must satisfy without specifying a return distribution: monotonicity, convexity, and boundary conditions. He derives conditions for early exercise of American options (early exercise of calls on non-dividend-paying stocks is never optimal; may be optimal for puts and dividend-paying calls). Merton extends BSM to continuous dividends, derives put-call parity in its modern form, and prices warrants and other derivatives. He also shows how to use options to complete markets.

## Key Contribution
Rigorous derivation of BSM using Itô calculus. General bounds on option prices from no-arbitrage alone. Proved American calls on non-dividend-paying stocks should never be exercised early. Extended BSM to dividend-paying assets. Introduced continuous-dividend yield model (Merton model for dividends). Established modern mathematical framework for derivatives pricing.

## Methods
Itô's lemma and stochastic differential equations. No-arbitrage bounds and dominance arguments. Dynamic replication and the risk-neutral pricing principle. Continuous-time optimal stopping for American options. Extensions to warrants, convertible bonds.

## Results
All rational option prices must lie between specific bounds (no-arbitrage). American call on non-dividend stock = European call (early exercise never optimal). European put-call parity: C - P = S - K·e^{-rT}. Continuous dividend yield option price: C = S·e^{-qT}·N(d1) - K·e^{-rT}·N(d2).

## Critique
Same BSM assumptions on volatility. More theoretical than practical—key contribution is rigor and generality. American put early exercise boundary requires numerical methods (no closed form).

## Relevance
Provides the rigorous mathematical foundation that Black-Scholes (a physics-style derivation) lacked. Every serious option pricing textbook begins here. The American option results are directly applied to early exercise decisions, convertible bonds, and real options.

## Related
- [[Black-Scholes-1973-Pricing-of-Options-and-Corporate-Liabilities]]
- [[Cox-Ross-Rubinstein-1979-Option-Pricing-Simplified-Approach]]
- [[Longstaff-Schwartz-2001-Valuing-American-Options-LSM]]
- [[Harrison-Kreps-1979-Martingales-and-Arbitrage]]
