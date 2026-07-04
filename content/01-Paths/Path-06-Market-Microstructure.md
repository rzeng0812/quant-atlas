---
type: learning-path
title: Market Microstructure
goal: Understand how markets actually work at the level of order flow, and how to execute large orders efficiently
prereqs:
  - Basic trading knowledge (order types, bid-ask spread)
  - "[[01-Paths/Path-05-Trading-Strategies]]"
tags: [path]
status: active
created: 2026-04-18
---

## Goal
Understand the mechanics of price formation — why spreads exist, who sets them, and what happens when a large order hits the book. Build the theoretical toolkit to design or evaluate execution algorithms, from naive TWAP benchmarks up through Almgren-Chriss optimal liquidation and Avellaneda-Stoikov optimal market making.

## Prerequisites
- Basic trading knowledge — order types, bid-ask spread, limit vs. market orders
- [[01-Paths/Path-05-Trading-Strategies]] — Market Making (ch.4) is the most relevant prerequisite; the other strategy families provide useful context

## Curriculum

| # | Concept | Primary Source | Status | Notes |
|---|---------|---------------|--------|-------|
| 1 | [[Order Book]] | Cartea et al. ch.1 | math | Raw market structure; the substrate everything else rests on |
| 2 | [[Adverse Selection]] | Kyle (1985) | math | Why spreads exist; informed vs. uninformed order flow |
| 3 | [[Price Impact]] | Almgren et al. (2005) | math | Cost of trading size; temporary vs. permanent impact |
| 4 | [[TWAP-VWAP]] | Industry standard | math | Benchmark execution strategies every practitioner uses |
| 5 | [[Almgren-Chriss]] | Almgren & Chriss (2000) | math | Optimal execution theory; risk-adjusted liquidation |
| 6 | [[Avellaneda-Stoikov]] | Avellaneda & Stoikov (2008) | math | Optimal market making with inventory risk |

## Source Stack
1. **Cartea, Jaimungal & Penalva — Algorithmic and High-Frequency Trading** — ch.1, 4
   - Start here. Ch.1 covers order book mechanics; ch.4 (from Path-05) feeds directly into Avellaneda-Stoikov.
2. **Kyle (1985) — "Continuous Auctions and Insider Trading"**
   - The foundational adverse selection model. Mandatory reading before price impact.
3. **Almgren & Chriss (2000) — "Optimal Execution of Portfolio Transactions"**
   - The canonical liquidation paper. Read after price impact concepts are clear.
4. **Almgren et al. (2005) — "Direct Estimation of Equity Market Impact"**
   - Empirical companion to the 2000 paper. Grounds theory in real data.
5. **Avellaneda & Stoikov (2008) — "High-Frequency Trading in a Limit Order Book"**
   - Optimal market making model. Read after Almgren-Chriss; requires stochastic control intuition.

## Session Log

### 2026-04-18
- Path created.

## What's Next
- HFT research — latency arbitrage, co-location, and queue position modeling
- Execution algorithm development — applying Almgren-Chriss variants in live systems
- Market impact modeling — estimating and hedging your own price impact
