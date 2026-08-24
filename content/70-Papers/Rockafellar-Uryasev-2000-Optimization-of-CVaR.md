---
type: paper
title: "Optimization of Conditional Value-at-Risk"
authors: ["R. Tyrrell Rockafellar", "Stanislav Uryasev"]
year: 2000
categories: ["q-fin.RM", "q-fin.PM"]
tags: [paper, classic, unread, risk, cvar, expected-shortfall, optimization, portfolio-management, linear-programming]
status: unread
added: 2026-08-23
journal: "Journal of Risk, 2(3), 21-41"
---

## Abstract
Rockafellar and Uryasev show that Conditional Value-at-Risk (CVaR, also known as Expected Shortfall), the expected loss conditional on losses exceeding VaR, can be minimized using a simple linear programming formulation. They introduce an auxiliary function F_α(x, ζ) = ζ + (1/(1-α))·E[max(−x^T r - ζ, 0)] whose minimization over ζ simultaneously determines VaR and CVaR. This transforms CVaR portfolio optimization from an intractable problem involving tail distributions into a convex (in fact, linear) optimization, enabling practical use of CVaR as the portfolio risk criterion.

## Key Contribution
Showed CVaR minimization is a linear program (convex optimization). Introduced the Rockafellar-Uryasev formula for CVaR. Made tail risk optimization practically tractable. Provided unified framework: minimizing F_α gives both optimal VaR and CVaR simultaneously. Foundation for all CVaR-based portfolio optimization in practice.

## Methods
CVaR_α(X) = E[X | X ≥ VaR_α(X)]. Auxiliary function: F_α(x,ζ) = ζ + 1/(1-α)·E[max(-r^T x - ζ, 0)]. Key theorem: min_{x ∈ X} CVaR_α(x) = min_{x ∈ X, ζ} F_α(x,ζ). Sample approximation: replace expectation with sample average → linear program. Extension: CVaR constraint as linear constraint in LP.

## Results
CVaR minimization is a convex problem (linear program with scenario representation). Sample average approximation: N scenarios → LP with N constraints. CVaR portfolio optimization: mean-CVaR efficient frontier. No need to estimate the loss distribution parametrically.

## Critique
LP scales well with sample size but can be slow for very large N. Requires a sample of scenarios (simulation or historical). Sensitive to the choice of confidence level α. Does not directly minimize VaR (which is non-convex). Tail estimation uncertainty not formally addressed.

## Relevance
Transformed CVaR from a theoretical measure (Artzner et al.) into a practical optimization tool. Used in portfolio construction (mean-CVaR portfolios), regulatory capital optimization, and risk budgeting. Banks use CVaR optimization for market risk capital under Basel IV. Essential for any quant building risk-aware portfolio optimization.

## Related
- [[Artzner-1999-Coherent-Measures-of-Risk]]
- [[Markowitz-1952-Portfolio-Selection]]
- [[Almgren-Chriss-2001-Optimal-Execution-Portfolio-Transactions]]
