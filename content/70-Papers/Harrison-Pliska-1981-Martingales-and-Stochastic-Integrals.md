---
type: paper
title: "Martingales and Stochastic Integrals in the Theory of Continuous Trading"
authors: ["J. Michael Harrison", "Stanley R. Pliska"]
year: 1981
categories: ["q-fin.MF"]
tags: [paper, classic, unread, mathematical-finance, complete-markets, replication, martingales, continuous-time]
status: unread
added: 2026-08-23
journal: "Stochastic Processes and their Applications, 11(3), 215-260"
---

## Abstract
Harrison and Pliska extend the fundamental theorem of asset pricing to continuous-time markets, using the Itô stochastic integral as the mathematical tool for modeling self-financing trading strategies. They establish the Second Fundamental Theorem of Asset Pricing: a market is complete (every contingent claim is replicable by a self-financing trading strategy) if and only if the equivalent martingale measure is unique. In complete markets, derivative prices are uniquely determined. In incomplete markets (multiple EMMs), a range of no-arbitrage prices exists, and additional criteria are needed for valuation.

## Key Contribution
Extended FTAP to continuous-time markets with stochastic integrals. Proved the Second FTAP: completeness ⟺ unique EMM. Established Itô stochastic integrals as the model for trading gains. Proved that BSM is a complete market (unique EMM → unique option price). Founded continuous-time mathematical finance.

## Methods
Continuous-time trading with Itô processes. Self-financing trading strategies as stochastic integrals. Equivalent martingale measure in continuous time. Girsanov's theorem for change of measure. Completeness via representation theorems for Brownian filtrations.

## Results
Second FTAP: Complete market ⟺ unique EMM. In BSM (single Brownian motion, single risky asset): market is complete → all derivatives are replicable → unique prices. Multi-factor models require at least as many traded assets as Brownian motions for completeness.

## Critique
Idealized continuous trading. The mathematical framework (Itô integrals, Girsanov) requires measure theory. Practical markets are incomplete (jumps, stochastic vol, transaction costs). Later work by Delbaen-Schachermayer (1994) extended to the most general case using NFLVR.

## Relevance
The rigorous foundation of continuous-time derivatives pricing. Every proof that BSM prices are unique, or that a stochastic volatility model gives multiple prices, uses this framework. Essential for mathematical finance, exotic derivatives pricing, and incomplete market theory.

## Related
- [[Harrison-Kreps-1979-Martingales-and-Arbitrage]]
- [[Black-Scholes-1973-Pricing-of-Options-and-Corporate-Liabilities]]
- [[Heston-1993-Closed-Form-Solution-Options-Stochastic-Volatility]]
