---
type: paper
title: "Learning to Aggregate Zero-Shot LLM Agents for Corporate Disclosure Classification"
authors: ["Kemal Kirtac"]
year: 2026
arxiv_id: 2603.20965v1
categories: ['q-fin.TR', 'cs.AI', 'cs.MA', 'q-fin.CP', 'q-fin.ST']
tags: [paper, unread, microstructure, ai, computational-finance, statistical-finance]
status: unread
added: 2026-04-18
url: https://arxiv.org/abs/2603.20965v1
---

## Abstract
This paper studies whether a lightweight trained aggregator can combine diverse zero-shot large language model judgments into a stronger downstream signal for corporate disclosure classification. Zero-shot LLMs can read disclosures without task-specific fine-tuning, but their predictions often vary across prompts, reasoning styles, and model families. I address this problem with a multi-agent framework in which three zero-shot agents independently read each disclosure and output a sentiment label, a confidence score, and a short rationale. A logistic meta-classifier then aggregates these signals to predict next-day stock return direction. I use a sample of 18,420 U.S. corporate disclosures issued by Nasdaq and S&P 500 firms between 2018 and 2024, matched to next-day stock returns. Results show that the trained aggregator outperforms all single agents, majority vote, confidence-weighted voting, and a FinBERT baseline. Balanced accuracy rises from 0.561 for the best single agent to 0.612 for the trained aggregator, with the largest gains in disclosures combining strong current performance with weak guidance or elevated risk. The results suggest that zero-shot LLM agents capture complementary financial signals and that supervised aggregation can turn cross-agent disagreement into a more useful classification target.

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
