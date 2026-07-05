---
type: paper
title: "Heads, Not Backbones: Output Heads Dominate Architectures on Fat-Tailed Returns"
authors: ["Sichao He", "Yansong Zhang"]
year: 2026
arxiv_id: 2606.30037v1
categories: ['cs.LG', 'q-fin.RM', 'q-fin.ST']
tags: [paper, unread, machine-learning, risk, statistical-finance]
status: unread
added: 2026-07-04
url: https://arxiv.org/abs/2606.30037v1
---

## Abstract
In a deep forecasting pipeline for fat-tailed financial returns at short horizons, which matters more -- the backbone architecture or the output head? The authors compare four modern backbones (TimesNet, DLinear, N-BEATS, iTransformer) under three output heads (point, single-Gaussian density, and a Gaussian mixture density head with K=4 components) on S&P 500 monthly log-returns (1871-2023) under anchored walk-forward validation. The three heads form a strict gradient: switching from point to Gaussian improves CRPS by about 1.3%, and switching from Gaussian to mixture adds a further 2.4%, while switching between backbones changes CRPS by less than 1.5% on the point-head row. The Model Confidence Set on squared errors does not exclude any of the 12 variants at the 5% level -- the head separates them only on distributional metrics, not squared error -- and the mixture head's incremental value is largest in the highest-volatility regimes (13.9% in 1970s stagflation at h=12). The picture is horizon-dependent: the head dominates at short horizons, but the backbone re-takes the lead at long horizons (h>=6), confirming the mixture captures tail risk beyond what a unimodal Gaussian can express during crisis periods when risk-management decisions actually matter.

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
