---
type: paper
title: "KineticSim: A Lightweight, High-Performance Execution Engine for Real-Time Market Simulators"
authors: ["Shakya Jayakody", "Prarthinie Jayakody"]
year: 2026
arxiv_id: 2606.21784v1
categories: ['cs.DC', 'cs.PF', 'q-fin.TR']
tags: [paper, unread, microstructure]
status: unread
added: 2026-06-28
url: https://arxiv.org/abs/2606.21784v1
---

## Abstract
Simulating financial markets at scale with multi-agent (Agent-Based) models is critical for market design, regulatory stress-testing, and reinforcement learning, but traditional CPU simulators are bottlenecked by sequential processing while vectorized GPU frameworks suffer from kernel-launch overhead and redundant global-memory round-trips. We formalize, analyze, and evaluate a reusable parallel design pattern: persistent, state-carrying clearing for iterative multi-agent reductions. By caching mutable simulation state in thread-block shared memory across step boundaries, aggregating agent actions via shared-memory atomics, and resolving the clearing function cooperatively, the pattern reduces the per-step critical-path depth from Theta(L+A) for sequential clearing (L price-grid ticks, A agents) to Theta(log L + ceil(A/L)) and makes global-memory traffic independent of the step count. We implement this in KineticSim, a lightweight GPU execution engine that simulates massive ensembles of limit-order books in parallel, reaching a peak throughput of over 54.7 billion agent-events per second. On a fixed workload it delivers speedups of 3406x over CPU (NumPy), 27.8x over PyTorch GPU, 42.8x over JAX GPU, and 8.4x over a naive custom CUDA baseline, while using roughly an order of magnitude less GPU memory than PyTorch. Across 53 configurations the two custom CUDA engines produce bitwise-identical order books, and aggregate statistics match the CPU reference to within 0.1%. The pattern generalizes to other iterative multi-agent workloads requiring state-persistent, block-localized reductions.

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
