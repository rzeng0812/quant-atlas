---
type: paper
title: "Faster Monotone Implied Volatility Solver"
authors: ["Fabien Le Floc'h"]
year: 2026
arxiv_id: 2605.22427v1
categories: ['q-fin.CP', 'q-fin.PR']
tags: [paper, unread, computational-finance, pricing]
status: unread
added: 2026-05-24
url: https://arxiv.org/abs/2605.22427v1
---

## Abstract
We present ThiopheneIV, a Black-Scholes implied-volatility solver with a monotone core and explicit production guards. Prices are first reduced to Jäckel's out-of-the-money normalisation and inverted through a tail-stable logarithmic price equation. The solver starts from the non-iterative Choi-Huh-Su L3 lower-bound seed and applies three Euler-Chebyshev corrections. In exact arithmetic, the seed is below the admissible root and the Euler-Chebyshev map increases monotonically without overshooting; the proof is included. The implementation then adds the floating-point machinery needed in practice: parity normalisation, microscopic Bachelier-limit handling, saturated-price treatment, finite-update checks, fallback seeds, and an optional Jäckel-Newton polish. Against the highly accurate expanded Jäckel reference price, ThiopheneIV is faster than a Java port of Jäckel's Let's Be Rational while keeping regular-grid errors close. ThiopheneIV+ adds one final Jäckel-Newton correction for systems that need closer agreement with that expanded reference price. The broader lesson is that a convergence proof gives a clean core, but robust production inversion still depends on boundary handling and on the pricing objective one chooses to match.

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
