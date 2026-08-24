---
type: paper
title: "Pricing Interest Rate Derivative Securities"
authors: ["John Hull", "Alan White"]
year: 1990
categories: ["q-fin.PR", "q-fin.MF"]
tags: [paper, classic, unread, interest-rates, term-structure, fixed-income, hull-white, calibration, short-rate-model]
status: unread
added: 2026-08-23
journal: "Review of Financial Studies, 3(4), 573-592"
---

## Abstract
Hull and White introduce the extended Vasicek (Hull-White) model by replacing the constant mean-reversion level θ with a time-dependent function θ(t), enabling exact calibration to the observed initial yield curve while maintaining analytical tractability. The short rate follows: dr = [θ(t) - κr]dt + σdW, where θ(t) is chosen to match current market zero-coupon bond prices exactly. The model provides closed-form formulas for bond prices and European bond options, and Hull-White develop the trinomial tree implementation that became the industry standard. The Hull-White model is the dominant one-factor model for interest rate derivative pricing.

## Key Contribution
Extended Vasicek to fit the initial yield curve exactly (no-arbitrage model). Time-dependent drift θ(t) calibrated to market data. Closed-form bond and bond option prices. Trinomial tree implementation for American/Bermudan options. Hull-White remains the dominant one-factor interest rate model in practice.

## Methods
Short rate: dr = [θ(t) - κr]dt + σdW (extended Vasicek) or dr = [θ(t) - a(t)r]dt + σ(t)dW (general form). θ(t) derived from initial forward curve: θ(t) = ∂f(0,t)/∂t + κf(0,t) + σ²/(2κ)·(1-e^{-2κt}). Bond prices remain affine: P(t,T) = A(t,T)·exp(-B(t,T)·r). Trinomial tree for numerical implementation.

## Results
Bond prices: P(t,T) = A(t,T)·exp(-B(t,T)·r). Bond option prices: Black-like formula in terms of bond price volatility. European swaptions: approximate closed-form. Exact fit to initial yield curve by construction. Rates can go negative (Gaussian model).

## Critique
Single-factor (one source of uncertainty). Gaussian rates → negative rates possible (became a real issue post-2008). Cannot independently calibrate to both yield curve and cap volatilities without extending σ to time-varying. Extensions to two-factor Hull-White (G2++) address some limitations.

## Relevance
The standard model for pricing interest rate derivatives in sell-side systems. Used for Bermudan swaptions, callable bonds, and structured products. The trinomial tree implementation is the basis for most bank production pricing systems. Must-know for any fixed income quant.

## Related
- [[Vasicek-1977-Equilibrium-Characterization-Term-Structure]]
- [[Cox-Ingersoll-Ross-1985-Theory-Term-Structure-Interest-Rates]]
- [[Heath-Jarrow-Morton-1992-Bond-Pricing-Term-Structure]]
- [[Black-1976-Pricing-of-Commodity-Contracts]]
