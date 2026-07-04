---
type: paper
title: "PEB Separation and State Migration: Unmasking the New Frontiers of DeFi AML Evasion"
authors: ["Yixin Cao", "Xianfeng Cheng", "Yijie Liu"]
year: 2026
arxiv_id: 2603.26290v1
categories: ['cs.CR', 'q-fin.TR']
tags: [paper, unread, microstructure]
status: unread
added: 2026-04-18
url: https://arxiv.org/abs/2603.26290v1
---

## Abstract
Transfer-based anti-money laundering (AML) systems monitor token flows through transaction-graph abstractions, implicitly assuming that economically meaningful value migration is sufficiently encoded in transfer-layer connectivity. In this paper, we demonstrate that this assumption, the bedrock of current industrial forensics, fundamentally collapses in composable smart-contract ecosystems.
  We formalize two structural mechanisms that undermine the completeness of transfer-layer attribution. First, we introduce Principal-Execution-Beneficiary (PEB) separation, where intent originators, transaction executors (e.g., MEV searchers), and ultimate beneficiaries are functionally decoupled. Second, we formalize state-mediated value migration, where economic coupling is enforced through invariant-driven contract state transitions (e.g., AMM reserve rebalancing) rather than explicit transfer continuity.
  Through a real-world case study of role-separated limit order execution and a constructive cross-pool arbitrage model, we prove that these mechanisms render transfer-layer observation neither attribution-complete nor causally closed. We further argue that simply expanding transfer-layer tracing capabilities fails to resolve the underlying attribution ambiguity inherent in structurally decoupled execution. Under modular composition and open participation markets, these mechanisms are structurally generative, implying that heuristic-based flow tracing has reached a formal observational boundary. We advocate for a paradigm shift toward AML based on execution semantics, focusing on the restitution of economic causality from atomic execution logic and state invariants rather than static graph connectivity.

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
