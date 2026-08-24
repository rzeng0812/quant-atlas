---
type: paper
title: "Coherent Measures of Risk"
authors: ["Philippe Artzner", "Freddy Delbaen", "Jean-Marc Eber", "David Heath"]
year: 1999
categories: ["q-fin.RM"]
tags: [paper, classic, unread, risk, risk-management, coherent-risk, var, cvar, expected-shortfall, axioms]
status: unread
added: 2026-08-23
journal: "Mathematical Finance, 9(3), 203-228"
---

## Abstract
Artzner, Delbaen, Eber, and Heath provide an axiomatic characterization of coherent risk measures. They define four properties that any reasonable risk measure ρ should satisfy: (1) translation invariance: ρ(X + a) = ρ(X) - a; (2) subadditivity: ρ(X + Y) ≤ ρ(X) + ρ(Y); (3) positive homogeneity: ρ(λX) = λρ(X); (4) monotonicity: X ≥ Y ⟹ ρ(X) ≤ ρ(Y). Value-at-Risk (VaR) violates subadditivity and is therefore not coherent—it can penalize diversification. Expected Shortfall (CVaR/ES = average loss beyond VaR) satisfies all four axioms and is coherent. This paper transformed risk measurement theory.

## Key Contribution
Defined the four axioms of coherent risk measures. Proved VaR is not coherent (not subadditive). Proved Expected Shortfall (CVaR/ES) is coherent. Characterized all coherent risk measures as worst-case expectations over a set of probability measures. Foundation for Basel III/IV adoption of Expected Shortfall over VaR.

## Methods
Axiomatic approach to risk measures. Dual representation: coherent risk measures = sup_{P ∈ P} E^P[-X] for some set P of probability measures. Counter-examples to VaR subadditivity (credit portfolio example: two concentrated positions can appear safer separately). Representation theorem for coherent risk measures.

## Results
VaR is not subadditive: two portfolios each just below VaR threshold can combine to exceed threshold. ES is coherent: ES_α = E[-X | X ≤ -VaR_α]. Representation: ρ is coherent ⟺ ρ(X) = sup_{Q ∈ Q} E^Q[-X]. Scenario-based risk measures are coherent.

## Critique
Coherent risk measures may not capture all risk preferences. ES requires estimation of the tail beyond VaR (harder with limited data). Regulatory adoption came slowly (Basel IV adopted ES in 2019). Convex risk measures (Föllmer-Schied) generalize by dropping homogeneity.

## Relevance
Transformed how regulators and risk managers think about risk measurement. Basel III/IV shifted from VaR to Expected Shortfall precisely because of this paper. Every serious discussion of portfolio risk measurement must address coherence. CVaR/ES optimization (Rockafellar-Uryasev) is a direct consequence.

## Related
- [[Rockafellar-Uryasev-2000-Optimization-of-CVaR]]
- [[Mandelbrot-1963-Variation-of-Certain-Speculative-Prices]]
- [[Engle-1982-ARCH]]
