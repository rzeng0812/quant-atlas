---
type: paper
title: "Diagonal Frog: High-order positivity-preserving FD schemes for anisotropic Fokker-Planck equations"
authors: ["Andrey Itkin"]
year: 2026
arxiv_id: 2606.23980v1
categories: ['math.NA', 'physics.bio-ph', 'physics.comp-ph', 'q-fin.CP', 'q-fin.PR']
tags: [paper, unread, computational-finance, pricing]
status: unread
added: 2026-06-28
url: https://arxiv.org/abs/2606.23980v1
---

## Abstract
The Fokker-Planck equation is fundamental to statistical mechanics, yet in settings with multiple state variables, anisotropic (cross-) diffusion, and jumps, conventional discretizations frequently produce non-physical negative probability densities. Building on the operator approach of "A. Itkin, Pricing derivatives under Levy models. Modern finite difference and pseudo-differential operators approach, Springer, 2017, ISBN 978-1-4939-6792-6", we introduce a family of "Diagonal Frog" discretizations whose spatial operators are eventually M-matrices (EM-matrices). Although these operators lack a local M-matrix structure, positivity of the directional sub-operators emerges in the spirit of Zeno's paradox: the matrix exponential, assembled as the limit of infinitely many ever-smaller substeps, is provably nonnegative after a short transient even though no single substep is. For the mixed-derivative block, whose generator is not eventually nonnegative, positivity instead rests on a factorized resolvent solver and holds conditionally, on an explicit step-size window; discrete mass is conserved exactly by the splitting for every step size. The resulting schemes are second-order accurate in time and space and require O(m 2 N + m 3) operations per time step, where m is the dimension of the Krylov subspace used to apply the exponential. As stress tests, we solve a two-dimensional anisotropic Fokker-Planck equation in the strong cross-diffusion regime against an exact Gaussian reference, a Kramers escape problem in a double-well potential, and an advection-dominated problem, and observe that the schemes remain stable, nonnegative, and mass-conservative for a wide range of Pécklet numbers (so, don't need any flux limiter). Finally, we extend the construction to multidimensional processes and to the backward Kolmogorov equation with jumps.

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
