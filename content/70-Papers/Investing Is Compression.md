---
type: paper
title: "Investing Is Compression"
authors: ["Oscar Stiffelman"]
year: 2026
arxiv_id: 2604.10758v3
categories: ['cs.CE', 'q-fin.PM']
tags: [paper, unread, portfolio]
status: unread
added: 2026-04-18
url: https://arxiv.org/abs/2604.10758v3
---

## Abstract
In 1956 John Kelly wrote a paper at Bell Labs describing the relationship between gambling and Information Theory. What came to be known as the Kelly Criterion is both an objective and a closed-form solution to sizing wagers when odds and edge are known. Samuelson argued it was arbitrary and subjective, and successfully kept it out of mainstream economics. Luckily it lived on in computer science, mostly because of Tom Cover's work at Stanford. He showed that it is the uniquely optimal way to invest: it maximizes long-term wealth, minimizes the risk of ruin, and is competitively optimal in a game-theoretic sense, even over the short term.
  One of Cover's most surprising contributions to portfolio theory was the universal portfolio. Related to universal compression in information theory, it performs asymptotically as well as the best constant-rebalanced portfolio in hindsight. I borrow a trick from that algorithm to show that Kelly's objective, even in the general form, factors the investing problem into three terms: a money term, an entropy term, and a divergence term. The only way to maximize growth is to minimize divergence which measures the difference between our distribution and the true distribution in bits. Investing is, fundamentally, a compression problem.
  This decomposition also yields new practical results. Because the money and entropy terms are constant across strategies in a given backtest, the difference in log growth between two strategies measures their relative divergence in bits. I also introduce a winner fraction heuristic which allocates capital in proportion to each asset's probability of dominating the candidate set. The growth shortfall of this heuristic relative to the optimal portfolio is bounded by the entropy of the winner fraction distribution. To my knowledge, both the heuristic and the entropy bound are original contributions.

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
