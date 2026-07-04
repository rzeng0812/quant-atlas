---
type: paper
title: "Sequential Structure in Intraday Futures Data: LSTM vs Gradient Boosting on MNQ"
authors: ["Mathias Mesfin"]
year: 2026
arxiv_id: 2605.17724v1
categories: ['q-fin.TR', 'cs.LG', 'q-fin.CP', 'q-fin.ST']
tags: [paper, unread, microstructure, machine-learning, computational-finance, statistical-finance]
status: unread
added: 2026-05-24
url: https://arxiv.org/abs/2605.17724v1
---

## Abstract
This paper compares gradient boosting and long short-term memory (LSTM) architectures for intraday directional prediction in Micro E-Mini Nasdaq 100 futures (MNQ). Motivated by recent foundation-model research on financial candlestick data, including the Kronos architecture, we test whether five-minute OHLCV bar sequences contain exploitable sequential predictive structure at the scale of a single instrument dataset. Using 944 trading days from 2021-2025, four model configurations are evaluated under strict expanding-window walk-forward validation across three out-of-sample periods. The target variable is whether the session close exceeds the 10:30 AM open by more than ten points. No configuration produces statistically significant out-of-sample accuracy above the 51.8% base rate. Combined OOS accuracies range from 50.00% to 50.89% across gradient boosting variants, while the LSTM achieves 50.59%. Permutation tests yield p-values of 0.135 for the best gradient boosting model and 0.515 for the LSTM, indicating no statistically significant predictive edge. Feature importance instability across walk-forward folds suggests noise fitting rather than stable structural signal capture. The results indicate that four years of single-instrument five-minute OHLCV data are insufficient for reliable sequential ML-based intraday forecasting. The primary contribution is a documented evaluation of a Kronos-inspired architecture on a constrained real-world dataset, providing an empirical lower bound on data scale requirements for sequential financial ML.

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
