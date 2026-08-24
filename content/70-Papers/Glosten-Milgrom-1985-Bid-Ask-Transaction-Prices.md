---
type: paper
title: "Bid, Ask and Transaction Prices in a Specialist Market with Heterogeneously Informed Traders"
authors: ["Lawrence R. Glosten", "Paul R. Milgrom"]
year: 1985
categories: ["q-fin.TR"]
tags: [paper, classic, unread, market-microstructure, bid-ask-spread, adverse-selection, liquidity, informed-trading]
status: unread
added: 2026-08-23
journal: "Journal of Financial Economics, 14(1), 71-100"
---

## Abstract
Glosten and Milgrom model the bid-ask spread as arising from adverse selection: a specialist market maker sets prices facing a mix of informed traders (who know the true asset value better than the market maker) and uninformed (liquidity) traders. The market maker sets bid and ask prices to break even in expectation, knowing that informed traders always buy when the true value is above the ask and sell when below the bid. The resulting spread is an increasing function of the probability of informed trading. This sequential trade model provides the first rigorous information-theoretic explanation of bid-ask spreads.

## Key Contribution
Founded the adverse selection theory of the bid-ask spread. Showed that spreads arise from information asymmetry, not inventory costs alone. Introduced the probability of informed trading (PIN) as a key microstructure variable. Established Bayesian updating as the mechanism for price discovery. Foundation for the PIN model and order flow toxicity research.

## Methods
Sequential trade model: each arriving trader is informed (prob μ) or uninformed (prob 1-μ). Bayesian updating by market maker after each trade. Market maker sets bid < E[V|sell] and ask > E[V|buy] to break even. Equilibrium spread derived from zero-profit condition. Dynamic: prices converge to true value as trades arrive.

## Results
Bid-ask spread increases in μ (probability of informed trading). Informed traders always trade at posted quotes (no negotiation). Price discovery: transaction prices are a martingale and converge to V. Higher noise trader volume → tighter spreads → better market quality.

## Critique
Exogenous trade arrival (not strategic). Single asset. Market maker cannot distinguish informed from uninformed order flow. Extensions include order size signaling, multiple assets, and dynamic strategies. Does not model the order book directly.

## Relevance
Foundation of modern market microstructure theory. The adverse selection framework underlies all research on spreads, order flow toxicity, and dark pools. The PIN (probability of informed trading) measure derived from this model is widely used by regulators and academics. Essential for understanding execution quality and TCA.

## Related
- [[Kyle-1985-Continuous-Auctions-and-Insider-Trading]]
- [[Avellaneda-Stoikov-2008-High-Frequency-Trading-Limit-Order-Book]]
- [[Almgren-Chriss-2001-Optimal-Execution-Portfolio-Transactions]]
