---
type: paper
title: "An Equilibrium Characterization of the Term Structure"
authors: ["Oldrich Vasicek"]
year: 1977
categories: ["q-fin.PR", "q-fin.MF"]
tags: [paper, classic, unread, interest-rates, term-structure, fixed-income, short-rate-model, vasicek, mean-reversion]
status: unread
added: 2026-08-23
journal: "Journal of Financial Economics, 5(2), 177-188"
---

## Abstract
Vasicek introduces the first equilibrium model of the term structure of interest rates, derived from a general equilibrium framework with a Markov short rate process. The short rate follows an Ornstein-Uhlenbeck (mean-reverting) process: dr = κ(θ - r)dt + σdW. He derives closed-form bond prices of the form P(t,T) = A(T-t)·exp(-B(T-t)·r) (affine structure) and shows how the entire yield curve is determined by the current short rate. The model captures the tendency of rates to mean-revert to a long-run level θ at speed κ, with volatility σ.

## Key Contribution
First equilibrium term structure model. Introduced mean reversion to interest rate dynamics. Derived closed-form affine bond prices. Founded the affine term structure model (ATSM) class. Introduced the Ornstein-Uhlenbeck process to finance. Provided the framework for risk-neutral pricing of fixed income derivatives.

## Methods
Ornstein-Uhlenbeck process for the short rate. Equilibrium derivation using preferences and technology. Bond price as exponential-affine function of short rate. Risk-neutral pricing and the market price of interest rate risk.

## Results
Short rate: dr = κ(θ - r)dt + σdW under physical measure. Bond price: P = A(τ)·exp(-B(τ)·r) with explicit A, B. Yield curve: y(t,T) = -(1/τ)·ln P(t,T) = linear in r. Normal distribution for future rates (rates can go negative).

## Critique
Rates can be negative (Gaussian model). Single-factor model cannot fit the full yield curve shape simultaneously (need multi-factor extensions). Cannot independently be calibrated to the current term structure (fixed θ). Superseded by Hull-White (1990) for derivative pricing (which allows time-varying parameters to fit the market curve).

## Relevance
The starting point for all short-rate models. Every practitioner studying fixed income modeling begins with Vasicek. The analytical tractability of the affine structure (A·exp(-B·r)) is exploited in CIR, Hull-White, and all multi-factor extensions. Also has a large credit portfolio application (Vasicek's model for default correlation).

## Related
- [[Cox-Ingersoll-Ross-1985-Theory-Term-Structure-Interest-Rates]]
- [[Hull-White-1990-Pricing-Interest-Rate-Derivative-Securities]]
- [[Heath-Jarrow-Morton-1992-Bond-Pricing-Term-Structure]]
