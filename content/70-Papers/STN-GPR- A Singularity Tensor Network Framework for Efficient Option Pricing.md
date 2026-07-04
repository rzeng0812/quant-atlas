---
type: paper
title: "STN-GPR: A Singularity Tensor Network Framework for Efficient Option Pricing"
authors: ["Dominic Gribben", "Carolina Allende", "Alba Villarino", "Aser Cortines", "Mazen Ali", "Román Orús", "Pascal Oswald", "Noureddine Lehdili"]
year: 2026
arxiv_id: 2603.26318v1
categories: ['q-fin.PR', 'cs.CE', 'cs.LG', 'quant-ph']
tags: [paper, unread, pricing, machine-learning]
status: unread
added: 2026-04-18
url: https://arxiv.org/abs/2603.26318v1
---

## Abstract
We develop a tensor-network surrogate for option pricing, targeting large-scale portfolio revaluation problems arising in market risk management (e.g., VaR and Expected Shortfall computations). The method involves representing high-dimensional price surfaces in tensor-train (TT) form using TT-cross approximation, constructing the surrogate directly from black-box price evaluations without materializing the full training tensor. For inference, we use a Laplacian kernel and derive TT representations of the kernel matrix and its closed-form inverse in the noise-free setting, enabling TT-based Gaussian process regression without dense matrix factorization or iterative linear solves. We found that hyperparameter optimization consistently favors a large kernel length-scale and show that in this regime the GPR predictor reduces to multilinear interpolation for off-grid inputs; we also derive a low-rank TT representation for this limit. We evaluate the approach on five-asset basket options over an eight dimensional parameter space (asset spot levels, strike, interest rate, and time to maturity). For European geometric basket puts, the tensor surrogate achieves lower test error at shorter training times than standard GPR by scaling to substantially larger effective training sets. For American arithmetic basket puts trained on LSMC data, the surrogate exhibits more favorable scaling with training-set size while providing millisecond-level evaluation per query, with overall runtime dominated by data generation.

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
