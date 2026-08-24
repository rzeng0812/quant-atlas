---
type: paper
title: "Modeling Term Structures of Defaultable Bonds"
authors: ["Darrell Duffie", "Kenneth J. Singleton"]
year: 1999
categories: ["q-fin.CR", "q-fin.PR"]
tags: [paper, classic, unread, credit-risk, reduced-form-model, fixed-income, credit-derivatives, defaultable-bonds, affine]
status: unread
added: 2026-08-23
journal: "Review of Financial Studies, 12(4), 687-720"
---

## Abstract
Duffie and Singleton develop a comprehensive framework for pricing defaultable bonds within the affine term structure class, extending the Jarrow-Turnbull approach to allow for stochastic default intensity and recovery rates. They introduce the "recovery of market value" (RMV) convention: upon default, the bondholder receives a fraction (1-L) of the bond's pre-default market value. Under RMV, the defaultable bond price satisfies the same affine pricing equation as a risk-free bond but with the short rate replaced by r + L·λ (risk-free rate plus loss rate). This tractable framework became the standard for pricing credit derivatives and corporate bonds.

## Key Contribution
Extended reduced-form credit modeling to affine term structure class. Introduced recovery of market value (RMV) convention → clean affine pricing. Showed that credit-risky bonds can be priced like risk-free bonds with a "loss-adjusted" short rate r + Lλ. Framework for time-series and cross-sectional identification of credit risk. Standard reference for CDS, bond, and CVA pricing.

## Methods
Default intensity λ(t) following affine dynamics (CIR or Gaussian). Recovery of market value: R(τ) = (1-L)·B(τ^-, T). Pricing under risk-neutral measure: B(t,T) = E^Q[exp(-∫_t^T (r+Lλ)ds)]. Calibration to credit spread curves. Estimation via extended Kalman filter on panel data.

## Results
Credit bond price = risk-free bond with short rate r + Lλ. Credit spread ≈ Lλ for small Lλ. Closed-form prices under CIR intensity. Stochastic correlation between default risk and interest rates captured. Framework nests Jarrow-Turnbull as a special case.

## Critique
RMV convention is a modeling convenience (recovery of face value or par more common in practice). Default correlation between issuers not directly modeled (requires copula or factor models). Intensity models are risk-neutral and don't directly link to firm fundamentals. Required extensions for credit portfolio risk (Li 2000 copula).

## Relevance
The standard reference for CDS pricing and credit bond valuation. CVA (Credit Valuation Adjustment) calculations use the DS framework. Every credit risk textbook covers this paper. Essential for sell-side credit trading, credit portfolio management, and regulatory capital calculations.

## Related
- [[Jarrow-Turnbull-1995-Pricing-Derivatives-Credit-Risk]]
- [[Merton-1974-Pricing-Corporate-Debt]]
- [[Cox-Ingersoll-Ross-1985-Theory-Term-Structure-Interest-Rates]]
