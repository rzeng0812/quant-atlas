---
type: learning-path
title: Interest Rate Models
goal: Understand how interest rates are modeled, how bonds are priced, and how to hedge rate risk
prereqs:
  - "[[01-Paths/Path-01-Derivatives-Foundation]]"
  - Basic bond knowledge
tags: [path, rates, fixed-income]
status: active
created: 2026-04-18
---

## Goal
Move from equity derivatives into the rates world. Understand the yield curve as the object being modeled, learn how duration and convexity quantify rate sensitivity, and build up from the simple Vasicek short-rate model to the arbitrage-free HJM framework that models the entire curve. Finish with SABR applied to rate options (caps, floors, swaptions) — the market standard in rates vol.

## Prerequisites
- [[01-Paths/Path-01-Derivatives-Foundation]] — BSM derivation, risk-neutral measure, and SDEs are directly reused. HJM in particular requires comfort with stochastic calculus.
- Basic bond knowledge — coupon bonds, zero-coupon bonds, discount factors. Hull ch.4 covers this; work through it first if unfamiliar.

## Curriculum

| # | Concept | Primary Source | Status | Notes |
|---|---------|---------------|--------|-------|
| 1 | [[Bond Basics]] | Hull ch.4 | math | Zero coupon, par, duration intuition |
| 2 | [[Yield Curve]] | Hull ch.4 | math | What we're modeling; bootstrapping zeros from par rates |
| 3 | [[Interest Rate Swaps]] | Hull ch.7 | math | Most liquid rates derivative; swap curve |
| 4 | [[Duration]] | Hull ch.4 | math | First-order rate sensitivity; DV01 |
| 5 | [[Convexity]] | Hull ch.4 | math | Second-order sensitivity; why duration alone misprices |
| 6 | [[Vasicek Model]] | Hull ch.31 | math | Simplest mean-reverting short-rate model |
| 7 | [[HJM Framework]] | Hull ch.31 / Shreve II ch.10 | math | Model the entire forward curve; arbitrage-free by construction |
| 8 | [[SABR Model]] | Hagan et al. (2002) | math | Rates options standard; swaptions, caps, floors |

## Source Stack
1. **Hull — Options, Futures & Other Derivatives** — ch.4, 31
   - Start here. Ch.4 builds bond/curve intuition; ch.31 covers Vasicek and HJM at an accessible level.
2. **Shreve — Stochastic Calculus for Finance II** — ch.10
   - Rigorous HJM treatment. Read after Hull ch.31 if you want the full mathematical derivation.
3. **Hagan et al. (2002) — "Managing Smile Risk"**
   - SABR applied to rate options. Same paper as Path-02; now read it through the lens of swaption vol surfaces.

## Session Log

### 2026-04-18
- Path created.

## What's Next
- Interest rate derivatives desk roles — the models in this path are live market practice
- Fixed income portfolio management — duration/convexity hedging at the portfolio level
- [[01-Paths/Path-04-Risk-and-Portfolio]] — apply rate sensitivity tools within a broader risk framework
