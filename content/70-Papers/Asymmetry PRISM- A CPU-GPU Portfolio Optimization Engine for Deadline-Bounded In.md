---
type: paper
title: "Asymmetry PRISM: A CPU/GPU Portfolio Optimization Engine for Deadline-Bounded Institutional Rebalancing"
authors: ["Debdoot Ghosh"]
year: 2026
arxiv_id: 2606.23367v1
categories: ['q-fin.CP', 'cs.CE', 'cs.DC', 'math.OC', 'q-fin.PM']
tags: [paper, unread, computational-finance, portfolio]
status: unread
added: 2026-06-28
url: https://arxiv.org/abs/2606.23367v1
---

## Abstract
Institutional rebalancing is a batched optimization workload with a hard operating deadline: hundreds of accounts need new weights under budget, turnover, exposure, exclusion, and tax-aware controls before trading can proceed. This paper evaluates Asymmetry PRISM, a CPU/GPU portfolio optimization engine, through a public evaluation boundary; problem data in, and returned weights, status codes, timings, memory class, external feasibility diagnostics, eligible objective comparisons, and audit records out. Within that boundary, the evaluation protocol fixes hardware and software versions, declares timing lanes, separates cold single calls from repeated workloads, and admits objective-gap claims only where an eligible reference solver completed. On completed multi-solver rows from N=100 to N=2,000, Asymmetry PRISM-CPU is 4.5x to 24.1x faster than the fastest completed reference row in the same lane. In the production queue study, Asymmetry PRISM-GPU completes 500/500 accounts over a 10,000-instrument universe in 109.5 s within a declared 25-minute operating window, with zero missed deadlines and an audit record for every solve; the recorded OSQP queue baseline completes 4/500. On an operationally constrained real-data suite (tax-motivated transition penalties, restriction caps, turnover controls, batches), Asymmetry PRISM clears constrained solves 3.4x to 126.7x faster than the best completing incumbent at certified-equal objectives, and the GPU route widens to 8.8x over the CPU route at N=384,800. Rows without a completed reference are reported as feasibility, timing, memory, and failure-status evidence.

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
