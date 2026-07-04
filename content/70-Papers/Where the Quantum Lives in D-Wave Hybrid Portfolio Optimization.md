---
type: paper
title: "Where the Quantum Lives in D-Wave Hybrid Portfolio Optimization"
authors: ["Luis Lozano"]
year: 2026
arxiv_id: 2605.17623v1
categories: ['quant-ph', 'math.OC', 'q-fin.PM']
tags: [paper, unread, portfolio]
status: unread
added: 2026-05-24
url: https://arxiv.org/abs/2605.17623v1
---

## Abstract
We audit how much of D-Wave's hybrid quantum-classical portfolio-optimization service is actually quantum. On cardinality-constrained mean-variance-turnover instances spanning N equal to 10 to 640 with a Gurobi MIQP optimality anchor, the constraint-native LeapHybridCQM service matches Gurobi's proven optimum on all 54 instances where Gurobi proves optimality, but the mean QPU access time is only 0.034 seconds out of a 5-second wall-clock budget, roughly 0.7 percent of the run. The remaining roughly 99 percent is the service's classical decomposition, sub-problem assembly, and feasibility-aware reassembly, so the reported D-Wave hybrid win on this problem class is a constraint-native classical pipeline with a small QPU contribution rather than a quantum-sampling win. Two structural results sharpen this audit. First, the cardinality penalty contributes a dense rank-one term that makes the penalty-encoded logical graph fully connected regardless of the original covariance density, collapsing the intended density benchmark axis for all penalty-encoded paths while leaving the constraint-native sparsity intact. Second, the constraint-native service returns identical solutions at every tested wall-clock budget from 5 to 300 seconds and across 10 repeated calls, a determinism property of the service on this problem class. Together with two classical baselines, namely Gurobi MIQP and simulated annealing, and a comparison against the penalty-encoded hybrid interface, these results extend the prior constraint-native versus penalty-encoded observation of Sakuler et al. from the statement that the constraint-native interface handles constraints natively to the operational decomposition of where the win actually originates, a finding that reframes how D-Wave hybrid performance should be reported in quantum-finance benchmarks.

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
