---
type: paper
title: "A Theory of the Term Structure of Interest Rates"
authors: ["John C. Cox", "Jonathan E. Ingersoll", "Stephen A. Ross"]
year: 1985
categories: ["q-fin.PR", "q-fin.MF"]
tags: [paper, classic, unread, interest-rates, term-structure, fixed-income, cir-model, short-rate-model, affine]
status: unread
added: 2026-08-23
journal: "Econometrica, 53(2), 385-407"
---

## Abstract
Cox, Ingersoll, and Ross derive the CIR (Cox-Ingersoll-Ross) model for the term structure of interest rates from a general equilibrium framework with production uncertainty. The short rate follows a mean-reverting square-root process: dr = κ(θ - r)dt + σ√r dW. The square-root diffusion ensures non-negative rates (rates cannot cross zero if 2κθ > σ²) and yields closed-form bond prices in the exponential-affine form. Compared to the Gaussian Vasicek model, CIR avoids negative rates while remaining analytically tractable. CIR also price bond options in closed form via the noncentral chi-squared distribution.

## Key Contribution
First general equilibrium non-Gaussian term structure model. Non-negative rates guaranteed by the square-root diffusion. Closed-form affine bond prices. Founded the affine term structure model (ATSM) class with non-Gaussian state variables. Closed-form bond option prices. Still used as the basis for multi-factor generalizations (Dai-Singleton 2000).

## Methods
General equilibrium production economy. Square-root process for the short rate: dr = κ(θ - r)dt + σ√r dW. Bond PDE derived from equilibrium. Solution: P(t,T) = A(τ)·exp(-B(τ)·r) with explicit A(τ), B(τ). Bond option prices via noncentral chi-squared distribution.

## Results
Bond prices: P(t,T) = A(τ)·exp(-B(τ)·r), τ = T - t. Non-negativity: r ≥ 0 a.s. if 2κθ ≥ σ². Bond option prices in closed form. Long-run rate = κθ/(κ + ½σ²/r). Risk premium is proportional to √r.

## Critique
Single-factor model (extended to multi-factor as AIII in Dai-Singleton). Cannot fit arbitrary yield curves without time-varying parameters. Square-root diffusion complicates simulation (Milstein or exact simulation required). Calibration is more complex than Vasicek.

## Relevance
Standard model for credit intensity processes (Duffie-Singleton) and for the short rate in many central bank DSGE models. The square-root process is also used for stochastic volatility (Heston 1993 uses the same process for variance). Essential for fixed income modeling, credit risk, and derivatives pricing.

## Related
- [[Vasicek-1977-Equilibrium-Characterization-Term-Structure]]
- [[Hull-White-1990-Pricing-Interest-Rate-Derivative-Securities]]
- [[Heston-1993-Closed-Form-Solution-Options-Stochastic-Volatility]]
- [[Duffie-Singleton-1999-Modeling-Term-Structures-Defaultable-Bonds]]
