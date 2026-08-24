---
type: paper
title: "The Pricing of Commodity Contracts"
authors: ["Fischer Black"]
year: 1976
categories: ["q-fin.PR"]
tags: [paper, classic, unread, pricing, options, futures, black-76, fixed-income, derivatives, interest-rate-derivatives]
status: unread
added: 2026-08-23
journal: "Journal of Financial Economics, 3(1-2), 167-179"
---

## Abstract
Black extends the Black-Scholes model to price options on futures contracts. Since futures have zero initial cost (mark-to-market settlement), the model replaces the spot price S with the futures price F and eliminates the cost-of-carry term. Under log-normal futures prices, European options on futures have closed-form prices analogous to BSM. Black's model became the market standard for pricing interest rate caps, floors, and swaptions—where the underlying is a forward rate or swap rate rather than a spot price—and remains widely used in fixed income despite the low-rate environment challenging the log-normal rate assumption.

## Key Contribution
Extended BSM to futures/forward contracts. Eliminated cost-of-carry from option pricing. Became the market standard for interest rate derivatives (caps, floors, swaptions). Introduced the concept of "forward" or "futures" volatility distinct from spot volatility.

## Methods
Geometric Brownian Motion for futures price F. Zero drift for futures price under risk-neutral measure. Black's formula: C = e^{-rT}[F·N(d1) - K·N(d2)] where d1 = (ln(F/K) + ½σ²T)/(σ√T). Applied to options on bond futures, Eurodollar futures, commodity futures.

## Results
Black's formula for European call on futures: C = e^{-rT}[F·N(d1) - K·N(d2)]. Market convention for quoting cap/floor/swaption volatilities ("Black vols"). Direct application to LIBOR market model.

## Critique
Log-normal rate assumption breaks down near zero rates (negative rates impossible under Black's model). Caused problems during the low/negative rate era (2010s). Replaced by Bachelier (normal) model for interest rate derivatives in low-rate environments. Shifted-Black model is a common workaround.

## Relevance
Essential for any fixed income derivatives practitioner. Cap/floor/swaption pricing and quoting conventions are built on Black's model. Understanding Black '76 is prerequisite to the LIBOR market model (LMM/BGM). Direct precursor to the caplet/floorlet model.

## Related
- [[Black-Scholes-1973-Pricing-of-Options-and-Corporate-Liabilities]]
- [[Heath-Jarrow-Morton-1992-Bond-Pricing-Term-Structure]]
- [[Hull-White-1990-Pricing-Interest-Rate-Derivative-Securities]]
