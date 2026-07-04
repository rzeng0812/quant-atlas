---
type: learning-path
title: ML in Finance
goal: Apply ML/AI techniques to alpha generation, regime detection, and execution optimization
prereqs:
  - "[[01-Paths/Path-04-Risk-and-Portfolio]]"
  - ML fundamentals (neural-path modules 15–17)
tags: [path]
status: active
created: 2026-04-18
---

## Goal
Bridge general ML knowledge into quantitative finance applications. Learn how to engineer ML-ready features from raw financial data, construct and evaluate alpha factors, detect market regimes, apply reinforcement learning to execution and allocation, and run ML-powered statistical arbitrage. After this path, you can build an end-to-end signal pipeline from raw data to backtested strategy.

## Prerequisites
- [[01-Paths/Path-04-Risk-and-Portfolio]] — factor models and performance metrics are the evaluation vocabulary throughout this path
- ML fundamentals — classical models (neural-path Module 15) and deep learning/sequence models (neural-path Module 17) are assumed; review before starting Feature Engineering

## Curriculum

| # | Concept | Primary Source | Status | Notes |
|---|---------|---------------|--------|-------|
| 1 | [[Feature Engineering Finance]] | Lopez de Prado ch.3 | math | Raw financial data → ML-ready features; most overlooked step |
| 2 | [[Alternative Data]] | Lopez de Prado ch.3 | math | Non-traditional data sources for alpha |
| 3 | [[Alpha Factor]] | Lopez de Prado ch.4 | math | Signal construction, combinatorial purging, factor evaluation |
| 4 | [[Overfitting and Multiple Testing]] | Lopez de Prado ch.12 | math | Why most backtests fail; Bonferroni, MinBRL |
| 5 | [[Regime Detection]] | Lopez de Prado ch.14 | math | Market state classification; HMM and unsupervised approaches |
| 6 | [[Reinforcement Learning Trading]] | Cartea et al. ch.10 | math | RL for execution optimization and portfolio allocation |
| 7 | [[Statistical Arbitrage]] | Lopez de Prado ch.5 | math | ML-powered stat arb; revisits Path-05 with ML lens |

## Source Stack
1. **Lopez de Prado — Advances in Financial Machine Learning** — ch.3, 4, 5, 14
   - Primary text. Read chapters in curriculum order; ch.3 is a prerequisite for all others.
2. **Cartea, Jaimungal & Penalva — Algorithmic and High-Frequency Trading** — ch.10
   - Best available treatment of RL applied to execution. Requires stochastic control background.
3. **Lopez de Prado — Machine Learning for Asset Managers** (2020)
   - Shorter companion book. Good for regime detection and portfolio construction context.

## Cross-Vault Links
- [neural-path Module 15 — Classical ML](obsidian://open?vault=neural-path&file=Module-15-Classical-ML) — foundational models (trees, SVMs, ensembles) used in Feature Engineering and Alpha Factor
- [neural-path Module 17 — Deep Learning](obsidian://open?vault=neural-path&file=Module-17-Deep-Learning) — sequence models (LSTM, Transformer) for time series signals
- [neural-path Module 20 — Agent Engineering](obsidian://open?vault=neural-path&file=Module-20-Agent-Engineering) — RL agents; direct prerequisite for Reinforcement Learning Trading

## Session Log

### 2026-04-18
- Path created.

## What's Next
- Live trading system development — wiring trained models into an execution pipeline with real-time feature computation
- Alternative data integration — satellite imagery, NLP on filings, credit card transaction data as alpha sources
