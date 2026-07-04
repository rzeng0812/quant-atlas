---
type: paper
title: "A Penalty-Free Pipeline for Direct Quantum-Annealer Portfolio Optimization"
authors: ["Luis Lozano"]
year: 2026
arxiv_id: 2605.17628v1
categories: ['quant-ph', 'math.OC', 'q-fin.PM']
tags: [paper, unread, portfolio]
status: unread
added: 2026-05-24
url: https://arxiv.org/abs/2605.17628v1
---

## Abstract
Direct quantum-annealer portfolio optimization is commonly formulated as a penalty-encoded QUBO and submitted to D-Wave hardware. We show that this standard formulation fails on current devices and identify the structural reason: the cardinality penalty contributes a dense rank-one term proportional to the all-ones matrix that makes the logical interaction graph complete regardless of the covariance structure. On Pegasus and Zephyr, chain-break fractions reach 83 percent at N equal to 24 and 92 percent at N equal to 49, producing no feasible samples. Attempting to fix this through topology-aware sparsification reveals a second problem: any sparsifier that removes off-diagonal entries also dilutes the cardinality constraint, so raw samples remain infeasible even when chains no longer break, and an ablation shows that for structurally favorable cases such as betting with settlement-graph priors the classical feasibility projector alone explains the result rather than the QPU. We propose dropping the penalty entirely: build an objective-only QUBO from the expected returns and the risk-scaled covariance, sample it on hardware, and enforce the cardinality constraint classically as a post-processing step. On D-Wave Advantage and Advantage2 for equities up to N equal to 49 and betting up to N equal to 48, mean chain-break fractions per sample averaged over reads drop from the range of 71 to 92 percent down to at most 0.04 percent. The QPU returns lower-energy feasible portfolios than the greedy heuristic on betting at N equal to 39 and 48, which is an energy comparison and not a proof of optimality, and the equity post-processed regret is at most 0.03 percent at all tested scales. These results establish that the penalty encoding, not the sparse hardware topology, is the binding constraint for direct QPU portfolio optimization at currently accessible scales.

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
