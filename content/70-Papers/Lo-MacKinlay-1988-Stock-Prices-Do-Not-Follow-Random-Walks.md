---
type: paper
title: "Stock Market Prices Do Not Follow Random Walks: Evidence from a Simple Specification Test"
authors: ["Andrew W. Lo", "A. Craig MacKinlay"]
year: 1988
categories: ["q-fin.ST"]
tags: [paper, classic, unread, statistical-finance, efficient-markets, return-predictability, random-walk, variance-ratio]
status: unread
added: 2026-08-23
journal: "Review of Financial Studies, 1(1), 41-66"
---

## Abstract
Lo and MacKinlay develop the variance ratio test and apply it to weekly US stock returns from 1962-1985, decisively rejecting the random walk hypothesis. Under a random walk, the variance of k-period returns should equal k times the variance of 1-period returns; the test statistic measures deviations from this ratio. The authors find significant positive autocorrelation in weekly returns for individual stocks and especially for portfolios, implying return predictability. The findings challenge the weak-form EMH and sparked an enormous literature on return predictability, short-term momentum, and market anomalies.

## Key Contribution
Introduced the variance ratio test—now a standard tool in empirical finance. Rejected the random walk for weekly stock returns with high statistical power. Distinguished between random walk H1 (iid increments) and H2 (uncorrelated but heteroscedastic). Showed small stocks are more predictable than large stocks. Motivated the literature on short-term momentum and reversal.

## Methods
Variance ratio: VR(k) = Var(r_t + ... + r_{t+k-1}) / [k·Var(r_t)]. Test statistic: M(k) = [VR(k) - 1] under H₀: random walk. Asymptotic distribution under both iid and heteroscedasticity assumptions. Applied to CRSP value-weighted and equal-weighted indices and size portfolios.

## Results
VR(k) > 1 for k = 2,...,8 weeks for most portfolios. Positive weekly autocorrelation: small stocks most predictable. Equal-weighted index much more predictable than value-weighted. Rejection robust to heteroscedasticity (non-constant variance over time).

## Critique
Weekly return predictability is small in magnitude (though statistically significant). Transaction costs likely eliminate exploitable profits for most investors. Effect has weakened post-publication (Grossman-Stiglitz paradox). Positive autocorrelation may reflect thin trading and non-synchronous prices for small stocks.

## Relevance
Established return predictability as a legitimate empirical fact. The variance ratio test is standard in EMH testing. This paper is the direct precursor to the short-term momentum and reversal literature, and to the construction of "price momentum" signals in quantitative factor models.

## Related
- [[Fama-1970-Efficient-Capital-Markets]]
- [[Jegadeesh-Titman-1993-Returns-Buying-Winners-Selling-Losers]]
- [[Gatev-Goetzmann-Rouwenhorst-2006-Pairs-Trading]]
