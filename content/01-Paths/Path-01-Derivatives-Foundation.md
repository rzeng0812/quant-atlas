---
type: learning-path
title: Derivatives Foundation
goal: Understand how options are priced, why Black-Scholes works, and what its limits are
prereqs:
  - Calculus
  - Basic probability
  - "[[10-Foundations/Probability/Martingales]]"
tags: [path, derivatives, pricing]
status: active
created: 2026-04-12
---

## Goal
Price a vanilla European option from first principles, understand where the BSM formula comes from, and know exactly where it breaks down.

## Prerequisites
- Calculus (chain rule, integration)
- Basic probability (expectation, normal distribution)
- [[Martingales]] — optional but helpful

## Curriculum

| # | Concept | Primary Source | Status | Notes |
|---|---------|---------------|--------|-------|
| 1 | [[Brownian Motion]] | Hull ch.14 | math | |
| 2 | [[Geometric Brownian Motion]] | Hull ch.14 | math | |
| 3 | [[Ito's Lemma]] | Hull ch.14 / Shreve II ch.4 | math | Core tool |
| 4 | [[Risk-Neutral Measure]] | Hull ch.13 | math | Key conceptual leap |
| 5 | [[Put-Call Parity]] | Hull ch.10 | math | No-arb constraint on call/put prices |
| 6 | [[Binomial Tree Model]] | Hull ch.13 | math | Discrete option pricing; intuition for risk-neutral measure |
| 7 | [[Black-Scholes Model]] | Hull ch.15 | math | Destination of this path |
| 8 | [[Option Greeks]] | Hull ch.19 | math | Practical use of BSM |
| 9 | [[Delta Hedging]] | Hull ch.19 | math | Why BSM hedging works |
| 10 | [[American Options]] | Hull ch.11 | math | Early exercise; where BSM needs extension |
| 11 | [[Implied Volatility]] | Hull ch.20 | math | Where BSM breaks |
| 12 | [[Volatility Smile]] | Hull ch.20 / Gatheral ch.1 | math | What BSM misses |

## Source Stack
1. **Hull — Options, Futures & Other Derivatives** — ch.13–15, 19–20
   - Primary source. Intuition-first, less rigorous but very clear.
2. **Shreve — Stochastic Calculus for Finance II** — ch.4–5
   - For Ito's Lemma and BSM derivation done rigorously. Read after Hull.
3. **Gatheral — The Volatility Surface** — ch.1
   - After you understand BSM, read ch.1 to see exactly where it fails.

## Session Log

### 2026-04-12
- Path created. Starting from scratch.

## What's Next
- [[01-Paths/Path-02-Stochastic-Volatility]] — Heston, SABR (unlocked after this)
- [[01-Paths/Path-03-Interest-Rate-Models]] — Vasicek, HJM
