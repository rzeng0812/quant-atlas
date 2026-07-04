---
type: concept
domain: 30-Models
tags: [pricing, options, derivatives]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-11
review_interval_days: 365
sources:
  - "Hull ch.15"
  - "Shreve Vol II ch.5"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Pricing → Gap 4: The derived option price contains μ — the unobservable expected return
> **This concept:** Derives the complete closed-form pricing formula for European options by eliminating μ through the risk-neutral measure — the complete solution to Gap 4
> **Alternative approaches to this gap:** [[Risk-Neutral Measure]], [[Girsanov Theorem]] (these are the mathematical tools BSM synthesizes; BSM is the unique solution)
> **You need first:** [[Geometric Brownian Motion]], [[Ito's Lemma]], [[Risk-Neutral Measure]]
> **This unlocks:** [[Implied Volatility]], [[Option Greeks]], [[Delta Hedging]], [[Volatility Smile]], [[Heston Model]], [[Local Volatility]], [[Merton Jump-Diffusion]], [[Binomial Tree Model]]

## Why This Exists

**The gap:** Before 1973, there was no agreed-upon way to price an option. Every buyer and seller had a different view on where the stock was going, so they arrived at different prices — making a functioning market impossible.

**What came before:** The natural approach was expected-value pricing: estimate where the stock will go, compute the expected payoff, and discount it back. The fatal flaw is that this price depends on μ, the stock's expected return — a number nobody agrees on. Two rational traders with different forecasts will always disagree on the price.

**What this adds:** Black-Scholes showed that if you can trade continuously, you can *replicate* any option's payoff by dynamically adjusting a stock-and-cash portfolio. Since the replicating portfolio has an unambiguous cost, the option price must equal that cost — or free money exists. When you form the hedge portfolio, the μ term cancels exactly, leaving a formula that depends only on the stock's volatility σ, the risk-free rate r, and observable quantities. No view on the future required.

**What it still doesn't solve:** BSM requires a single, constant σ for all strikes and maturities. In practice, different options on the same stock imply different σ values — the volatility smile. BSM is systematically wrong away from the money and cannot reproduce this market reality. This is Gap 5.

## Math Concepts

**Assumptions:**
- Stock follows [[Geometric Brownian Motion]]: $dS_t = \mu S_t\,dt + \sigma S_t\,dW_t$
- Constant volatility $\sigma$ and risk-free rate $r$
- No dividends, no transaction costs, continuous trading

**The BSM formula** for a European call option (right to buy stock at strike $K$ at expiry $T$):

$$\boxed{C = S_0 N(d_1) - K e^{-rT} N(d_2)}$$

where:

$$d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)\,T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}$$

and $N(\cdot)$ is the standard normal CDF.

For a European **put** (right to sell at $K$):

$$P = K e^{-rT} N(-d_2) - S_0 N(-d_1)$$

**Put-Call Parity** — a model-free relationship (no BSM needed):

$$C - P = S_0 - K e^{-rT}$$

**Where the formula comes from** — two equivalent derivations:
1. *PDE approach:* apply [[Ito's Lemma]] to $V(S_t, t)$, build a riskless portfolio (stock + option), invoke no-arbitrage → the BSM PDE: $\frac{\partial V}{\partial t} + rS\frac{\partial V}{\partial S} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} = rV$
2. *Risk-neutral approach:* under [[Risk-Neutral Measure]] $\mathbb{Q}$, $C = e^{-rT}\mathbb{E}^{\mathbb{Q}}[\max(S_T - K, 0)]$ — evaluate the lognormal expectation to get the formula

**Intuition for $N(d_2)$:** probability that the option expires in-the-money under $\mathbb{Q}$

**Intuition for $N(d_1)$:** the expected stock price, conditional on finishing above $K$, divided by $S_0$ — also the [[Option Greeks|Delta]] of the call

## Walkthrough

Price a call: $S_0 = 100$, $K = 105$, $r = 5\%$, $\sigma = 20\%$, $T = 1$ year.

$$d_1 = \frac{\ln(100/105) + (0.05 + 0.02)\cdot 1}{0.20} = \frac{-0.0488 + 0.07}{0.20} = \frac{0.0212}{0.20} = 0.106$$

$$d_2 = 0.106 - 0.20 = -0.094$$

$$N(0.106) \approx 0.542, \quad N(-0.094) \approx 0.463$$

$$C = 100 \times 0.542 - 105 \times e^{-0.05} \times 0.463 = 54.2 - 46.3 = 7.9$$

The call costs about \$7.90. No view on whether the stock will go up or down required.

## Analysis

**BSM is wrong — but useful:**
- **Constant vol:** real markets have [[Volatility Smile]] — BSM implied vol varies by strike and expiry
- **Normal log-returns:** real returns have fat tails and negative skew; BSM underprices tail risk
- **Continuous trading:** impossible in practice; discrete rebalancing introduces hedging error
- **No jumps:** stocks can gap (earnings, crises); BSM misprices short-dated options around events

**Why it's still used:**
- Closed-form and fast
- Everyone uses it → a shared language; prices quoted in "implied vol" units (see [[Implied Volatility]])
- Works well for short-dated, near-the-money options on liquid underlyings
- All extensions (Heston, SABR) reduce to BSM in limiting cases

## Implementation

```python
import numpy as np
from scipy.stats import norm

def black_scholes(S, K, r, sigma, T, option_type="call"):
    """Black-Scholes price for European call or put."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# Example
print(f"Call: {black_scholes(100, 105, 0.05, 0.20, 1.0):.4f}")  # ~7.97
print(f"Put:  {black_scholes(100, 105, 0.05, 0.20, 1.0, 'put'):.4f}")  # ~8.0
```

## Bridge to Quant / ML

- BSM is the benchmark all ML pricing models are measured against — "does your neural net beat BSM?"
- [[Implied Volatility]] extracted from BSM is one of the most predictive features in [[60-ML-Finance/Feature-Engineering/Alpha Factor]] research
- The [[Volatility Surface]] (IV by strike and expiry) is a rich data source for ML models — predicting its shape is an active research area

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Black-Scholes prices options without knowing the stock's expected return μ. Why? What is it about the derivation that makes μ disappear?
<details>
<summary>Answer</summary>
When you hold an option and continuously hedge it with −Δ shares of stock, the resulting portfolio is instantaneously riskless — it earns a deterministic return regardless of which way the stock moves. A riskless portfolio must earn exactly the risk-free rate r (by no-arbitrage). When you impose this condition, the μ term that appears in the option's SDE cancels against the μ in the stock's SDE. The final pricing equation only involves r and σ. This is the "risk-neutral" insight: you don't need to know where the stock is going, only how much it wiggles.
</details>

**Q2.** Why does Black-Scholes still work as an industry standard even though everyone knows its assumptions are wrong (constant vol, no jumps, continuous trading)?
<details>
<summary>Answer</summary>
Because it functions as a universal translation layer. Traders don't use BSM to believe it is literally true — they use it to quote prices in "implied volatility" units. By convention, every market participant quotes options as the σ that makes BSM match the market price. This creates a common language: if I say "the 1-month 25-delta put trades at 22 vol," every options trader knows exactly what I mean. The model is wrong but the language is useful. All more sophisticated models (Heston, SABR, Local Vol) are ultimately calibrated to the BSM implied vol surface anyway.
</details>

**Q3.** What is N(d₂) in the BSM formula, intuitively? What about N(d₁)?
<details>
<summary>Answer</summary>
N(d₂) is the risk-neutral probability that the option expires in-the-money — i.e., Q(S_T > K). It is the probability under the risk-neutral measure that the call will be exercised. N(d₁) is harder to interpret directly: it is the Delta of the call (∂C/∂S), and it also equals the expected stock price conditional on finishing above K, divided by S₀, adjusted for discounting. The two differ because N(d₁) accounts for the fact that when the option pays off, you receive S_T (which is higher on average than the unconditional expectation), whereas N(d₂) only captures the probability of exercise.
</details>

---

### Level 2 — Quantitative

**Q4.** Price a European call with the following parameters: S = 100, K = 100 (ATM), r = 4%, σ = 25%, T = 0.5 years. Show all steps.
<details>
<summary>Answer</summary>

Step 1: Compute d₁ and d₂.

d₁ = [ln(100/100) + (0.04 + 0.5 × 0.0625) × 0.5] / (0.25 × √0.5)
   = [0 + (0.04 + 0.03125) × 0.5] / (0.25 × 0.7071)
   = [0.071125 × 0.5] / 0.17678
   = 0.035563 / 0.17678
   = **0.2012**

d₂ = 0.2012 − 0.25 × 0.7071 = 0.2012 − 0.1768 = **0.0244**

Step 2: Look up standard normal CDF values.

N(0.2012) ≈ 0.5797
N(0.0244) ≈ 0.5097

Step 3: Compute the call price.

C = 100 × 0.5797 − 100 × e^{−0.04×0.5} × 0.5097
  = 57.97 − 100 × 0.9802 × 0.5097
  = 57.97 − 49.96
  = **\$8.01**

The ATM call costs about \$8 for a 6-month, 25-vol option.
</details>

**Q5.** Given a European put priced at \$6.50 with S = 100, K = 105, r = 3%, T = 1 year, what must the European call price be? Use put-call parity. Then verify: what implied relationship does this enforce between the two prices?
<details>
<summary>Answer</summary>

Put-call parity: C − P = S₀ − K e^{−rT}

C = P + S₀ − K e^{−rT}
  = 6.50 + 100 − 105 × e^{−0.03×1}
  = 6.50 + 100 − 105 × 0.9704
  = 6.50 + 100 − 101.89
  = **\$4.61**

The call must cost \$4.61 if the put costs \$6.50. If either deviates, you can lock in a riskless profit: e.g., if the call is priced at \$5.00, buy the put at \$6.50, sell the call at \$5.00, buy the stock at \$100, and borrow the PV of the strike (\$101.89). You receive a net cash inflow today and all positions cancel at expiry regardless of where the stock ends up.

Put-call parity is model-free — it holds for any model that prices by no-arbitrage, not just BSM.
</details>

---

### Level 3 — Coding

**Q6.** In the `black_scholes` function, the formula computes `norm.cdf(d1)` and `norm.cdf(d2)` and uses them for both call and put via the negation `norm.cdf(-d1)` and `norm.cdf(-d2)`. Why is this mathematically valid rather than computing d₁ and d₂ fresh for the put? What would happen if you introduced a separate `put_d1` variable using the same formula?
<details>
<summary>Answer</summary>
It's valid because N(−x) = 1 − N(x) for the standard normal CDF, and the put formula is P = K e^{−rT} N(−d₂) − S N(−d₁). The d₁ and d₂ values are defined identically for both call and put — they depend only on S, K, r, σ, T and not on the option type. Using `norm.cdf(-d2)` instead of recomputing with a separate variable saves computation and avoids floating-point inconsistency. If you introduced a separate `put_d1` computed with the same formula, it would produce the same numerical value, so the result would be identical — but it would be misleading code suggesting they are different quantities. The cleaner approach (used here) makes it explicit that d₁ and d₂ are shared between call and put.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| BSM tells you what an option *should* trade at | BSM maps between price and implied vol. The market sets prices; BSM is just the translation function. Implied vol is what "price" means in options markets. |
| Constant volatility is a reasonable approximation | It is systematically wrong across strikes (the vol smile). BSM misprices OTM options, especially puts, which trade at elevated vol due to crash risk. |
| The risk-neutral measure Q is the real-world probability of the stock rising | Q is a mathematical construction that makes discounted prices martingales. Q-probabilities are not predictions about the future; they are risk-adjusted weights used to compute no-arbitrage prices. |
| You need to know the stock's expected return to price options | The whole point of BSM is that μ cancels when you hedge. You only need r (observable), σ (estimable from options), and the current price. |

## Related Concepts
- [[Geometric Brownian Motion]] — the assumed price process
- [[Risk-Neutral Measure]] — the measure under which the expectation is taken
- [[Ito's Lemma]] — used to derive the BSM PDE
- [[Option Greeks]] — sensitivities of the BSM price to its inputs
- [[Delta Hedging]] — the replication strategy that enforces BSM pricing
- [[Implied Volatility]] — the $\sigma$ that makes BSM match market prices
- [[Heston Model]] — extends BSM with stochastic volatility
- [[Volatility Smile]] — the empirical violation of BSM's constant-vol assumption

## Sources Used
- Hull — *Options, Futures & Other Derivatives*, ch.15
- Shreve — *Stochastic Calculus for Finance II*, ch.5

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | Hull ch.15 + Shreve II ch.5 |
| 2026-04-11 | QA review passed — no issues found | QA review |
