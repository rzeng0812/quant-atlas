---
type: paper
title: "High-Frequency Trading in a Limit Order Book"
authors: ["Marco Avellaneda", "Sasha Stoikov"]
year: 2008
categories: ["q-fin.TR", "q-fin.MF"]
tags: [paper, classic, unread, market-microstructure, market-making, high-frequency-trading, inventory, stochastic-control, optimal-quotes]
status: unread
added: 2026-08-23
journal: "Quantitative Finance, 8(3), 217-224"
---

## Abstract
Avellaneda and Stoikov formulate the market maker's optimal quoting problem as a stochastic control problem. A market maker posting bid and ask quotes earns the spread when orders arrive (modeled as Poisson processes with intensity λ depending on quote distance from midprice) but accumulates inventory risk. They derive a HJB equation and, in the limit of small inventory aversion, closed-form optimal bid and ask quotes: r_b = s - (δ^a + δ^b)/2 - γσ²(T-t)q for the reservation price, and the half-spread δ = (1/γ)·ln(1 + γ/k) + (1/2)·γσ²(T-t). The model introduced the "reservation price"—a bid-price adjusted for current inventory—which became the cornerstone of all subsequent market-making models.

## Key Contribution
Founded the stochastic control approach to market making. Derived the reservation price concept (mid adjusted for inventory). Closed-form optimal bid/ask quotes depending on inventory. Exponential utility with Gaussian price risk and Poisson order arrival. The reference model for all academic and industrial market-making research since 2008.

## Methods
Underlying price: arithmetic Brownian motion. Order arrivals: inhomogeneous Poisson, intensity λ(δ) = A·e^{-k·δ}. Market maker maximizes E[exp(-γ·W_T)] (CARA utility). HJB equation for value function. Exponential ansatz → closed-form approximate solution. Reservation price and half-spread in closed form.

## Results
Reservation price: r(s,q,t) = s - q·γσ²(T-t). Optimal half-spread: δ* = (1/γ)·ln(1+γ/k) + ½γσ²(T-t). Inventory risk reduces reservation price linearly in q and remaining time. Optimal spread increases with volatility and inventory aversion. As T-t → 0: quotes converge to midprice (risk management dominates).

## Critique
Simplified price impact model (no permanent impact). Symmetric order arrival (no adverse selection, unlike Kyle/Glosten-Milgrom). No queue position or LOB microstructure. Finite horizon creates terminal inventory liquidation problem. Extensions (Guéant-Lehalle-Tapia, Cartea-Jaimungal) address many of these issues.

## Relevance
The standard academic model for market making. Every quant working in algorithmic market making, HFT, or electronic market design references Avellaneda-Stoikov. Extended by dozens of papers adding adverse selection, multiple assets, LOB structure, and reinforcement learning. Essential for understanding the inventory management problem in market making.

## Related
- [[Kyle-1985-Continuous-Auctions-and-Insider-Trading]]
- [[Glosten-Milgrom-1985-Bid-Ask-Transaction-Prices]]
- [[Almgren-Chriss-2001-Optimal-Execution-Portfolio-Transactions]]
