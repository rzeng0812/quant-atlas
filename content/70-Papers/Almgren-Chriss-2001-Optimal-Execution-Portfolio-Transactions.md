---
type: paper
title: "Optimal Execution of Portfolio Transactions"
authors: ["Robert Almgren", "Neil Chriss"]
year: 2001
categories: ["q-fin.TR", "q-fin.PM"]
tags: [paper, classic, unread, market-microstructure, execution, price-impact, algo-trading, optimal-execution, twap, implementation-shortfall]
status: unread
added: 2026-08-23
journal: "Journal of Risk, 3(2), 5-39"
---

## Abstract
Almgren and Chriss formulate optimal portfolio liquidation as a mean-variance optimization over execution trajectories. A trader liquidating X shares over [0,T] faces a tradeoff: slow execution reduces market impact but increases timing risk (price moves away from initial quote), while fast execution reduces timing risk but increases market impact costs. The model separates price impact into permanent (linear, from Kyle's λ) and temporary (also linear). The efficient frontier of execution strategies is parameterized by risk aversion, with TWAP at one extreme and minimum-impact at the other. Closed-form optimal trading schedules emerge.

## Key Contribution
Founded the academic theory of optimal execution. Derived the efficient frontier of execution strategies in closed form. Separated permanent and temporary market impact. Showed TWAP is the zero-risk-aversion optimal schedule. Implementation shortfall as the objective function. Basis for virtually all modern algorithmic execution algorithms (VWAP, IS, POV).

## Methods
Linear price impact model: permanent η·v, temporary θ·v. Price dynamics: S_k = S_{k-1} - η·n_k/τ - ε_k (random walk + impact). Minimize E[X_c] + λ·Var[X_c] over trading trajectory {n_k}. Closed-form optimal trajectory: hyperbolic sine function of time. Efficient frontier parameterized by risk aversion λ.

## Results
Optimal trajectory: x(t) = X · sinh(κ(T-t)) / sinh(κT) where κ = √(λσ²/θ). High risk aversion → front-load execution (early trading). Zero risk aversion → TWAP (uniform trading rate). Efficient frontier is a hyperbola in (expected cost, variance) space. Implementation shortfall formula in closed form.

## Critique
Linear impact model: price impact is actually concave (square-root law empirically) — see Grinold, Kahn, and Cont. Static model: does not incorporate limit orders, spread crossing, or real LOB dynamics. Assumes Gaussian price increments. Extensions (Almgren 2003, Obizhaeva-Wang 2013) address some issues.

## Relevance
The canonical model for algorithmic execution. Every sell-side execution algorithm (IS, TWAP, VWAP, POV) references this framework. Transaction cost analysis (TCA) systems are built on this model. Any quant involved in trading implementation, portfolio rebalancing, or execution consulting must know this paper deeply.

## Related
- [[Kyle-1985-Continuous-Auctions-and-Insider-Trading]]
- [[Avellaneda-Stoikov-2008-High-Frequency-Trading-Limit-Order-Book]]
- [[Glosten-Milgrom-1985-Bid-Ask-Transaction-Prices]]
