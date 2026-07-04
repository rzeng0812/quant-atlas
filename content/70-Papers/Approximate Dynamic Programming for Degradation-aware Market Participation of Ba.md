---
type: paper
title: "Approximate Dynamic Programming for Degradation-aware Market Participation of Battery Energy Storage Systems: Bridging Market and Degradation Timescales"
authors: ["Flemming Holtorf", "Sungho Shin"]
year: 2026
arxiv_id: 2603.21089v1
categories: ['eess.SY', 'math.OC', 'q-fin.TR']
tags: [paper, unread, microstructure]
status: unread
added: 2026-04-18
url: https://arxiv.org/abs/2603.21089v1
---

## Abstract
We present an approximate dynamic programming framework for designing degradation-aware market participation policies for battery energy storage systems. The approach employs a tailored value function approximation that reduces the state space to state of charge and battery health, while performing dynamic programming along a pseudo-time axis encoded by state of health. This formulation enables an offline/online computation split that separates long-term degradation dynamics (months to years) from short-term market dynamics (seconds to minutes) -- a timescale mismatch that renders conventional predictive control and dynamic programming approaches computationally intractable. The main computational effort occurs offline, where the value function is approximated via coarse-grained backward induction along the health dimension. Online decisions then reduce to a real-time tractable one-step predictive control problem guided by the precomputed value function. This decoupling allows the integration of high-fidelity physics-informed degradation models without sacrificing real-time feasibility. Backtests on historical market data show that the resulting policy outperforms several benchmark strategies with optimized hyperparameters.

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
