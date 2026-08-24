---
type: paper
title: "Pricing Derivatives on Financial Securities Subject to Credit Risk"
authors: ["Robert A. Jarrow", "Stuart M. Turnbull"]
year: 1995
categories: ["q-fin.CR", "q-fin.PR"]
tags: [paper, classic, unread, credit-risk, reduced-form-model, credit-derivatives, fixed-income, default-intensity]
status: unread
added: 2026-08-23
journal: "Journal of Finance, 50(1), 53-85"
---

## Abstract
Jarrow and Turnbull introduce the reduced-form (intensity-based) approach to credit risk modeling as an alternative to Merton's structural approach. Default is modeled as the first jump of a Poisson process with a (possibly stochastic) intensity λ (hazard rate), rather than being triggered by the firm's asset value crossing a boundary. This framework enables tractable, closed-form pricing of credit-risky derivatives and is easily calibrated to observed credit spreads. The model treats default as a surprise event whose probability is captured by the intensity, without requiring knowledge of the firm's balance sheet.

## Key Contribution
Founded the reduced-form (intensity-based) approach to credit risk. Modeled default as a Poisson event with stochastic intensity. Tractable pricing of credit-risky bonds and derivatives. Easy calibration to market credit spreads. Foundation for the CDS market and all intensity-based credit models (Duffie-Singleton, Hull-White).

## Methods
Default time τ ~ first jump of a Poisson process with intensity λ(t). Recovery rate δ on default (fraction of face value recovered). Risk-neutral pricing: risky bond = expected discounted cash flows under Q accounting for default. Hazard rate bootstrapped from credit spread curve.

## Results
Risky bond price: B(t,T) = E^Q[e^{-∫_t^T (r(s)+λ(s)(1-δ))ds}]. Credit spread ≈ λ(1-δ) for small λ. Floating rate notes: clean pricing formula. Extensions to stochastic intensity (Cox process/doubly stochastic Poisson).

## Critique
Default is a surprise (no gradual deterioration visible before default). Structural models provide more economic interpretation. Calibration of recovery rates is difficult. Model risk: the hazard rate is risk-neutral, not physical. Multiple curves needed in practice (rates + credit).

## Relevance
The reduced-form approach underpins most credit derivative pricing in practice. CDS pricing is essentially the calibration of a hazard rate curve. Every credit quant needs to understand the distinction between structural and reduced-form models. CDO pricing, CVA, and credit risk management all use intensity-based frameworks.

## Related
- [[Merton-1974-Pricing-Corporate-Debt]]
- [[Duffie-Singleton-1999-Modeling-Term-Structures-Defaultable-Bonds]]
