---
type: paper
title: "A New Interpretation of Information Rate"
authors: ["John L. Kelly Jr."]
year: 1956
categories: ["q-fin.PM", "q-fin.ST"]
tags: [paper, classic, unread, portfolio-management, kelly-criterion, information-theory, position-sizing, growth-optimal]
status: unread
added: 2026-08-23
journal: "Bell System Technical Journal, 35(4), 917-926"
---

## Abstract
Kelly introduces what became the Kelly criterion: the optimal fraction of wealth to bet in a repeated gambling game to maximize the long-run exponential growth rate of wealth. Using Shannon's information theory, Kelly shows that the optimal betting fraction equals the gambler's edge (expected net profit per unit wagered). Maximizing the expected logarithm of wealth is equivalent to maximizing long-run growth rate, and the resulting strategy (Kelly strategy) almost surely outperforms any other strategy with sufficiently many bets.

## Key Contribution
Derived the Kelly criterion for log-optimal betting. Linked information theory to optimal investment. Proved that log-utility maximization maximizes asymptotic growth rate. Showed that overbetting leads to ruin while underbetting is suboptimal.

## Methods
Shannon entropy and information rate. Maximization of expected log(wealth). Analysis of a binary bet with known odds. Asymptotic analysis of wealth growth rates. Connection to Shannon's noisy channel capacity.

## Results
Optimal bet fraction = edge / odds (for binary bets). General Kelly fraction: f* = argmax E[log(W)]. The Kelly strategy dominates all other strategies in the long run with probability 1. Half-Kelly reduces variance while preserving most of the growth benefit.

## Critique
Assumes known probabilities (edge estimation is the hard part in practice). Full Kelly has extremely high variance—large drawdowns. Requires maximizing log utility, which may not match investor preferences. Does not account for parameter uncertainty.

## Relevance
Foundational for position sizing and capital allocation in quantitative trading. The Kelly criterion is the theoretical optimal sizing rule for any trading strategy with a known edge. Widely applied in high-frequency trading, options market making, and sports betting. The basis for "risk-adjusted" capital allocation.

## Related
- [[Markowitz-1952-Portfolio-Selection]]
- [[Grinold-1989-Fundamental-Law-Active-Management]]
