---
type: book
title: Options, Futures, and Other Derivatives
author: John C. Hull
year: 2022
tags: [book, derivatives, pricing, risk]
status: reference
difficulty: beginner-intermediate
role: The standard introductory text for derivatives — intuition-first, formula-second. Used in Path-01, Path-02, Path-03, Path-04.
---

## Overview
Hull is the canonical first stop for anyone entering derivatives. It covers the full landscape — from how futures and options markets work, to binomial trees, BSM, Greeks, vol smile, VaR, and interest rate derivatives — with consistent emphasis on economic intuition before mathematical formalism. The prose is unusually clear for a finance textbook, and worked examples appear throughout. It is used in virtually every university derivatives course globally, which means external resources (solutions manuals, lecture notes, forums) are abundant. The 11th edition (2022) includes updated chapters on crypto derivatives and recent regulatory changes.

## Role in quant-atlas
- **Path-01 (Foundations):** Ch.1 (markets), Ch.4 (interest rates), Ch.13–15 (trees + GBM + BSM) — the intuitive layer before Shreve
- **Path-02 (Volatility):** Ch.19 (Greeks), Ch.20 (vol smile) — core reading before Gatheral
- **Path-03 (Rates):** Ch.31 (HJM and interest rate derivatives) — after Shreve Vol II Ch.10
- **Path-04 (Risk):** Ch.22 (VaR) — introduces risk measurement before more rigorous treatments

## Chapter Map
| Chapter | Topic | Concept Notes Fed | Difficulty |
|---------|-------|-------------------|------------|
| 1 | Introduction to derivatives markets — forwards, futures, options, swaps; why they exist | [[Derivatives-Overview]], [[Market-Structure]] | Beginner |
| 4 | Interest rates, compounding conventions, yield curve, duration, convexity | [[Yield-Curve]], [[Duration-Convexity]], [[Discount-Factors]] | Beginner |
| 13 | Binomial trees — one-step and multi-step; risk-neutral pricing intuition | [[Binomial-Trees]], [[Risk-Neutral-Pricing]] | Beginner |
| 14 | Wiener processes, GBM, Ito's lemma (informal) | [[GBM]], [[Ito-Lemma-Intuition]], [[Stochastic-Processes]] | Intermediate |
| 15 | Black-Scholes-Merton derivation, formula, and assumptions | [[BSM-Model]], [[BSM-Derivation]] | Intermediate |
| 19 | The Greeks — delta, gamma, theta, vega, rho; delta hedging | [[Greeks]], [[Delta-Hedging]] | Intermediate |
| 20 | Volatility smile — skew, term structure, implied vol surface | [[Vol-Smile]], [[Implied-Volatility]], [[Vol-Surface]] | Intermediate |
| 22 | Value at Risk — historical simulation, model-based; expected shortfall | [[VaR]], [[Expected-Shortfall]], [[Risk-Measures]] | Intermediate |
| 25 | Exotic options — barriers, Asians, lookbacks, digitals | [[Exotic-Options]] | Intermediate |
| 31 | Interest rate derivatives — caps/floors, swaptions, HJM framework | [[HJM-Framework]], [[Caps-Floors]], [[Swaptions]] | Advanced |

## Reading Strategy
Beginners should read Ch.1, Ch.4, Ch.13–15, Ch.19–20 in that order — this is the core arc from "what are derivatives?" to "why does the vol smile exist?" These chapters can be read without heavy math background. Ch.22 (VaR) can follow independently. Skip Ch.25–30 until you specifically need exotic pricing. Ch.31 (interest rate derivatives and HJM) belongs after completing Path-03's theoretical groundwork in Shreve Vol II. Hull is best used as a reference after the first read-through — the chapter structure makes it easy to look up specific instruments or formulas.

## Key Insights
- Risk-neutral pricing doesn't mean investors are risk-neutral — it means you can price as if they were, by adjusting the probabilities. Hull explains this more clearly than almost any other text.
- The vol smile is a direct empirical refutation of BSM. Hull introduces this early (Ch.20) so readers understand that BSM is a tool, not a law.
- Ito's lemma is what makes continuous-time finance tractable — it's the chain rule for stochastic processes, and Hull's informal treatment in Ch.14 is the best starting point before tackling Shreve's rigorous version.
- Greeks are not just sensitivity measures — they define a hedging program. Gamma and theta trade off against each other in a way that reveals the cost of being long optionality.
- Duration and convexity (Ch.4) are the discrete-time versions of the sensitivity machinery that reappears throughout rates derivatives — understanding them early pays dividends across Path-03 and Path-04.

## Prerequisites
Basic calculus and probability (expected value, normal distribution). No measure theory required. Familiarity with how stock markets work is helpful but not required — Ch.1 is self-contained.

## What to Read Next
After Ch.13–15: [[Shreve-Stochastic-Calculus-I]] for the rigorous probability foundations underlying risk-neutral pricing. After Ch.20: [[Gatheral-Volatility-Surface]] for the full treatment of stochastic and local vol models.
