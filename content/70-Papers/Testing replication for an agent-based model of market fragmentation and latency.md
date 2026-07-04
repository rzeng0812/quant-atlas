---
type: paper
title: "Testing replication for an agent-based model of market fragmentation and latency arbitrage"
authors: ["Ethan Ratliff-Crain", "Colin M. Van Oort", "Matthew T. K. Koehler", "Brian F. Tivnan"]
year: 2026
arxiv_id: 2604.20067v1
categories: ['q-fin.TR']
tags: [paper, unread, microstructure]
status: unread
added: 2026-04-25
url: https://arxiv.org/abs/2604.20067v1
---

## Abstract
This study strengthens the foundations of multi-venue market modeling by attempting an independent replication of Wah and Wellman's 2016 model of latency arbitrage in a fragmented market. We find that faithful replication is hindered by missing implementation details in the original paper and limited quantitative reporting. We demonstrate that increasing the number of simulation runs beyond the original design allows for the creation of bootstrap confidence intervals to support rigorous tests of quantitative alignment, compensating for lacking distributional information (e.g. variance). We also demonstrate that increased complexity across the modeled scenarios corresponds with increased difficulty aligning to the original results. We draw on a codebase released by the original authors in connection with a later paper to recover additional implementation details; however, we reject quantitative alignment between that codebase and the published results. Combining information from the paper and the released code, we achieve relational equivalence for most metrics but reject quantitative alignment for model settings where latency is non-zero. We show that many of the qualitative takeaways from the original paper on the effects of market fragmentation and latency arbitrage are sensitive to the specifics of a `greedy strategy' extension given to the zero-intelligence (ZI) trader agents. Under an alternative interpretation of this strategy, we find that market fragmentation decreases execution times in all experiments and increases trader welfare in most experiments. Finally, to facilitate future replication, critique, and extension, we provide an ODD (Overview, Design concepts, Details) protocol for our implementations of the model.

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
