---
type: paper
title: "Martingales and Arbitrage in Multiperiod Securities Markets"
authors: ["J. Michael Harrison", "David M. Kreps"]
year: 1979
categories: ["q-fin.MF"]
tags: [paper, classic, unread, mathematical-finance, arbitrage, risk-neutral-pricing, martingales, fundamental-theorem]
status: unread
added: 2026-08-23
journal: "Journal of Economic Theory, 20(3), 381-408"
---

## Abstract
Harrison and Kreps establish the mathematical foundation for modern derivatives pricing by proving the First Fundamental Theorem of Asset Pricing (FTAP): the absence of arbitrage is equivalent to the existence of an equivalent martingale measure (EMM, or risk-neutral measure). Under the EMM, discounted asset prices are martingales, and the price of any derivative is its discounted expected payoff under this measure. This theorem unifies and rigorously justifies the risk-neutral pricing used intuitively in the BSM framework, and establishes no-arbitrage as the central principle of derivatives valuation.

## Key Contribution
Proved the First Fundamental Theorem of Asset Pricing. Established equivalence between no-arbitrage and existence of an equivalent martingale measure. Provided rigorous mathematical justification for risk-neutral pricing. Founded modern mathematical finance as a discipline (together with Harrison-Pliska 1981).

## Methods
Finite probability space and multiperiod securities markets. Convex analysis and separation theorems. Definition of arbitrage: a trading strategy with non-negative payoff, positive probability of positive payoff, and zero cost. Proof of FTAP via Hahn-Banach theorem (or equivalent functional analysis).

## Results
FTAP: No arbitrage ⟺ ∃ equivalent martingale measure Q. Under Q: discounted asset prices are martingales. Price of any attainable payoff X = E^Q[e^{-rT}·X]. Multiple EMMs correspond to incomplete markets.

## Critique
Finite-state, discrete-time formulation. Continuous-time extension required Harrison-Pliska (1981) and later Delbaen-Schachermayer for the most general case (NFLVR condition). The existence of an EMM is a mathematical object—finding and calibrating it is the hard practical problem.

## Relevance
The theoretical cornerstone of all of derivatives pricing. Every time a practitioner uses risk-neutral pricing, they are using this theorem (whether they know it or not). Required reading for anyone who wants to understand why the risk-neutral measure exists and what it means.

## Related
- [[Harrison-Pliska-1981-Martingales-and-Stochastic-Integrals]]
- [[Black-Scholes-1973-Pricing-of-Options-and-Corporate-Liabilities]]
- [[Samuelson-1965-Proof-That-Properly-Anticipated-Prices]]
- [[Cox-Ross-Rubinstein-1979-Option-Pricing-Simplified-Approach]]
