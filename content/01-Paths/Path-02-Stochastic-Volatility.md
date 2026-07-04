---
type: learning-path
title: Stochastic Volatility
goal: Understand why BSM fails, what the vol smile is, and how Heston/SABR fix it
prereqs:
  - "[[01-Paths/Path-01-Derivatives-Foundation]]"
tags: [path, volatility, pricing]
status: active
created: 2026-04-18
---

## Goal
Build on BSM to understand why a single constant volatility cannot explain observed option prices across strikes and expiries. Learn how stochastic volatility models — Heston, SABR, and Local Vol — recover the empirical vol surface, and understand how traders use variance swaps and gamma scalping to trade volatility directly.

## Prerequisites
- [[01-Paths/Path-01-Derivatives-Foundation]] — especially BSM derivation, Greeks, and Implied Volatility. You need to understand what BSM assumes before you can understand why those assumptions fail.

## Curriculum

| # | Concept | Primary Source | Status | Notes |
|---|---------|---------------|--------|-------|
| 1 | [[Volatility Smile]] | Gatheral ch.1 | math | Why BSM breaks across strikes |
| 2 | [[Implied Volatility]] | Hull ch.20 | math | Deepen from Path-01; build intuition for the surface |
| 3 | [[Volatility Surface]] | Gatheral ch.1-2 | math | The full 2D strike × expiry picture |
| 4 | [[Heston Model]] | Gatheral ch.2 | math | Stochastic vol solution with analytic formula |
| 5 | [[SABR Model]] | Hagan et al. (2002) | math | Rates market standard; tractable smile dynamics |
| 6 | [[Local Volatility]] | Gatheral ch.1 / Dupire (1994) | math | Exact surface fit via Dupire's equation |
| 7 | [[Variance Swap]] | Gatheral ch.4 | math | Model-free vol product; realized vs implied |
| 8 | [[Gamma Scalping]] | Hull ch.19 | math | Vol trading in practice; P&L from delta hedging |

## Source Stack
1. **Gatheral — The Volatility Surface** — ch.1-2, 4
   - Primary source for this path. Clear treatment of smile, Heston, Local Vol, and variance products.
2. **Hull — Options, Futures & Other Derivatives** — ch.19-20
   - Use for Greeks review (ch.19) and Implied Vol foundations (ch.20) before moving to Gatheral.
3. **Hagan et al. (2002) — "Managing Smile Risk"** — original SABR paper
   - Short and readable. Read after Gatheral ch.2 to understand how SABR is used for rate options.
4. **Dupire (1994) — "Pricing with a Smile"**
   - The original Local Vol derivation. Two pages; worth reading directly.

## Session Log

### 2026-04-18
- Path created.

## What's Next
- [[01-Paths/Path-03-Interest-Rate-Models]] — apply vol modeling ideas to the rates world (SABR for swaptions)
- Exotic pricing deep-dive — barrier options, cliquet structures, forward vol agreements
