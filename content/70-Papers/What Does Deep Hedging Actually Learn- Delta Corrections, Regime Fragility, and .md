---
type: paper
title: "What Does Deep Hedging Actually Learn? Delta Corrections, Regime Fragility, and Symbolic Distillation"
authors: ["Kirill Zernikov"]
year: 2026
arxiv_id: 2605.21696v1
categories: ['q-fin.RM', 'q-fin.CP', 'q-fin.PR']
tags: [paper, unread, risk, computational-finance, pricing]
status: unread
added: 2026-05-24
url: https://arxiv.org/abs/2605.21696v1
---

## Abstract
This paper studies empirical deep hedging for S&P 500 index options under a local downside-shortfall reward. It moves beyond performance comparison by asking what the learned hedge does, when it fails, and whether it can be made auditable. TD3 agents are compared with a daily-updated Black-Scholes delta hedge on the same option episodes. In walk-forward tests from 2015 to 2023, the agents usually learn a systematic delta haircut relative to Black-Scholes. The correction is explained by spot-implied-volatility co-movement and often improves accumulated reward and terminal downside variance, but it is regime-fragile: 2022 exposes losses in adverse daily states, while 2023 shows that underhedging can raise ordinary variance when option P&L is spot-dominated and the volatility channel is unusually weak. Symbolic regression distills the neural policies into compact formulas that can be traded out of sample; these formulas preserve much of the reward, downside-variance, and CVaR advantage over Black-Scholes, and sometimes sharpen it, but inherit the same fragility in difficult regimes.

## Key Contribution
*Fill after reading.*

## Methods
*Fill after reading.*

## Results
*Fill after reading.*

## Critique
*Fill after reading.*

## Relevance
*Fill after reading.*

## Related
-
