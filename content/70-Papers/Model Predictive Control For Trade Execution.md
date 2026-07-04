---
type: paper
title: "Model Predictive Control For Trade Execution"
authors: ["Thomas P. McAuliffe", "Samuel Liew", "Yuchao Li", "Andrey Ushenin", "Chihang Wang", "Alexandros Tasos", "Jack Pearce", "Dimitris Tasoulis"]
year: 2026
arxiv_id: 2603.28898v1
categories: ['q-fin.TR']
tags: [paper, unread, microstructure]
status: unread
added: 2026-04-18
url: https://arxiv.org/abs/2603.28898v1
---

## Abstract
We address the problem of executing large client orders in continuous double-auction markets under time and liquidity constraints. We propose a model predictive control (MPC) framework that balances three competing objectives: order completion, market impact, and opportunity cost. Our algorithm is guided by a trading schedule (such as time-weighted average price or volume-weighted average price) but allows for deviations to reduce the expected execution cost, with due regard to risk.
  Our MPC algorithm executes the order progressively, and at each decision step it solves a fast quadratic program that trades off expected transaction cost against schedule deviation, while incorporating a residual cost term derived from a simple base policy. Approximate schedule adherence is maintained through explicit bounds, while variance constraints on deviation provide direct risk control. The resulting system is modular, data-driven, and suitable for deployment in production trading infrastructure.
  Using six months of NASDAQ 'level 3' data and simulated orders, we show that our MPC approach reduces schedule shortfall by approximately 40-50% relative to spread-crossing benchmarks and achieves significant reductions in slippage. Moreover, augmenting the base policy with predictive price information further enhances performance, highlighting the framework's flexibility for integration with forecasting components.

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
