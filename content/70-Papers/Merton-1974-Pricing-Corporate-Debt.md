---
type: paper
title: "On the Pricing of Corporate Debt: The Risk Structure of Interest Rates"
authors: ["Robert C. Merton"]
year: 1974
categories: ["q-fin.CR", "q-fin.PR"]
tags: [paper, classic, unread, credit-risk, structural-model, corporate-bonds, credit-spreads, default]
status: unread
added: 2026-08-23
journal: "Journal of Finance, 29(2), 449-470"
---

## Abstract
Merton applies option pricing theory to value corporate liabilities, treating equity as a call option on the firm's asset value with the face value of debt as the strike price. Default occurs when the firm's asset value V falls below debt face value D at maturity. Using BSM, Merton derives closed-form formulas for the value of equity (call option on V with strike D) and risky debt (= risk-free bond minus a put option). Credit spreads are determined by asset volatility and leverage. This founded the structural approach to credit risk modeling, used in KMV/Moody's Analytics distance-to-default models.

## Key Contribution
Founded structural credit risk modeling. Derived credit spreads from first principles using option pricing. Introduced "distance to default" concept. Showed that equity, debt, and firm value are linked through option pricing. Basis of the entire KMV framework and modern credit portfolio models.

## Methods
Geometric Brownian Motion for firm asset value V. Equity = max(V - D, 0) = call option with maturity T, strike D. Risky debt = D·e^{-rT} - put option = V - equity. BSM formula applied with V (unobservable) and σ_V as inputs. Calibration of V and σ_V from observable equity price and σ_E.

## Results
Credit spread = (1/T)·ln(D/(V - equity_value)) - r. Distance to default = (ln(V/D) + (μ - ½σ²)T) / (σ√T). Spread is monotonically increasing in leverage and asset volatility. Risky debt value = D·e^{-rT}·N(d2) + V·N(-d1).

## Critique
Assumes single maturity debt (bullet bond structure). Asset value V and σ_V are unobservable—requires calibration from equity market. Constant volatility and continuous asset process. Default only at maturity (first-passage extensions by Black-Cox 1976). Underestimates spreads for short maturities relative to market data (credit spread puzzle).

## Relevance
The structural foundation of credit risk. Every credit rating model and default probability model descends from this work. The KMV/Moody's Analytics EDF (Expected Default Frequency) is a direct implementation. Understanding this paper is essential for credit derivatives, CLO/CDO modeling, and bank risk management.

## Related
- [[Black-Scholes-1973-Pricing-of-Options-and-Corporate-Liabilities]]
- [[Jarrow-Turnbull-1995-Pricing-Derivatives-Credit-Risk]]
- [[Duffie-Singleton-1999-Modeling-Term-Structures-Defaultable-Bonds]]
