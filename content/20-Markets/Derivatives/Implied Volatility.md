---
type: concept
domain: 20-Markets
tags: [volatility, options, markets]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-12
review_interval_days: 365
sources:
  - "Hull ch.19"
created: 2026-04-12
---

> Vol that equates BSM price to market price; forward-looking

> [!info] Problem Chain
> **Chain:** Pricing → Gap 5: BSM assumes constant σ — real markets show a volatility smile
> **This concept:** Extracts the market's consensus volatility expectation at each (strike, expiry) pair by inverting the BSM formula, making the smile visible and tradeable.
> **Alternative approaches to this gap:** [[Volatility Smile]] (documents the pattern), [[Local Volatility]] (models σ as a function of S and t), [[Heston Model]] (makes σ stochastic), [[Merton Jump-Diffusion]] (adds jumps)
> **You need first:** [[Black-Scholes Model]], [[Option Greeks]] (vega), [[Put-Call Parity]]
> **This unlocks:** [[Volatility Smile]], [[Volatility Surface]], [[Variance Swap]], [[VIX]], [[Gamma Scalping]]

## Why This Exists

**The gap:** BSM produces an option price given a volatility input. But in practice, you observe the option price in the market and want to know what volatility the market is pricing in. There was no standard way to read the market's collective volatility expectation from observable prices — traders needed to work backwards from price to volatility.

**What came before:** Traders used historical volatility — the realized standard deviation of past returns — as their volatility estimate. They would plug this into BSM and compare the resulting theoretical price to the market price. But historical vol looks backward, while options prices reflect forward-looking uncertainty. The two often diverged significantly, and there was no clean way to explain which was "right."

**What this adds:** By inverting BSM numerically (there's no closed form), you can extract the exact volatility that the market is currently pricing. This implied volatility (IV) is forward-looking, market-consensus, and strike-specific. It becomes the standard language for quoting and comparing options: instead of saying "this call costs \$7.50," traders say "this call is at 22% vol." IV also immediately reveals when markets are pricing more fear into puts than calls (the volatility smile), which historical vol could not explain.

**What it still doesn't solve:** IV is computed separately for each (strike, expiry) pair. In a BSM world there should be one vol — but the market produces a whole surface of different IVs. This inconsistency — the volatility smile — is the next gap that needs explaining. IV is the measurement tool that makes the smile visible; it doesn't explain why the smile exists.

## Math Concepts

**The BSM call pricing formula:**

$$C(S, K, r, T, \sigma) = S \cdot N(d_1) - K e^{-rT} \cdot N(d_2)$$

where:

$$d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}$$

- $N(\cdot)$ is the cumulative standard normal distribution
- $S$ = current stock price
- $K$ = strike price of the option
- $r$ = continuously compounded risk-free rate
- $T$ = time to expiry in years
- $\sigma$ = volatility (annualized standard deviation of log returns)

**Definition of Implied Volatility:**

Given the observed market price $C_{\text{mkt}}$ and known inputs $(S, K, r, T)$, the implied volatility $\sigma_{\text{IV}}$ satisfies:

$$C_{\text{BSM}}(S, K, r, T,\; \sigma_{\text{IV}}) = C_{\text{mkt}}$$

This equation has no closed-form solution for $\sigma_{\text{IV}}$, so it must be solved numerically.

**Vega — the sensitivity to volatility:**

$$\mathcal{V} = \frac{\partial C}{\partial \sigma} = S \sqrt{T} \cdot n(d_1)$$

where $n(\cdot)$ is the standard normal PDF. Vega is always positive for both calls and puts: higher $\sigma$ always raises option prices. This guarantees the IV equation has at most one solution, which makes numerical root-finding well-behaved.

**Newton-Raphson update rule:**

$$\sigma_{n+1} = \sigma_n - \frac{C_{\text{BSM}}(\sigma_n) - C_{\text{mkt}}}{\mathcal{V}(\sigma_n)}$$

Start with an initial guess (e.g., $\sigma_0 = 0.2$) and iterate until convergence.

## Walkthrough

Suppose: $S = 100$, $K = 100$ (at-the-money), $r = 0.05$, $T = 0.5$ years, and you observe the call trading at $C_{\text{mkt}} = 7.50$.

Step 1 — Try $\sigma = 0.20$:
- $d_1 = \frac{\ln(1) + (0.05 + 0.02) \cdot 0.5}{0.20 \cdot 0.707} = \frac{0.035}{0.1414} \approx 0.2475$
- $d_2 = 0.2475 - 0.1414 = 0.1061$
- $C = 100 \cdot N(0.2475) - 100 e^{-0.025} \cdot N(0.1061) \approx 100(0.5977) - 97.53(0.5423) \approx 59.77 - 52.90 \approx 6.87$

Step 2 — The BSM price (\$6.87) is below market (\$7.50), so IV must be higher than 0.20. Vega $\approx 100 \cdot 0.707 \cdot n(0.2475) \approx 70.7 \cdot 0.387 \approx 27.4$.

Step 3 — Newton-Raphson update:
$$\sigma_1 = 0.20 - \frac{6.87 - 7.50}{27.4} = 0.20 + 0.023 = 0.223$$

Step 4 — Recompute BSM at $\sigma = 0.223$; answer will be very close to \$7.50. Typically 3–5 iterations achieve machine precision.

**Result:** $\sigma_{\text{IV}} \approx 0.223$, meaning the market is pricing in about 22.3% annualized volatility for this option.

## Analysis

**What IV is not:** IV is not a prediction that volatility *will* be 22.3%. It is the volatility the market is *pricing as if* it expects — a risk-neutral expectation, not a physical-world forecast. IV often exceeds realized volatility due to the variance risk premium (sellers demand a premium for bearing vol risk).

**IV surface:** In theory BSM implies a single flat sigma. In practice, computing IV for every strike and expiry produces a surface — IV varies by strike ([[Volatility Smile]]) and by expiry (term structure). This variation is direct evidence that BSM's constant-vol assumption is wrong.

**Bid-ask spread problem:** IV computed from the bid differs from IV on the ask. Practitioners usually use the mid-price and acknowledge a range of "fair" IV.

**Boundary conditions:**
- IV must be positive. If the market price violates put-call parity, IV may have no solution.
- Deep in-the-money options have very low vega, making the Newton-Raphson update numerically unstable — bisection is safer there.

**Common misconceptions:**
- "IV predicts the future move." It prices the *distribution* of moves, not the direction.
- "Lower IV means a calm market." IV is low when *option buyers and sellers* agree on low vol, but that consensus can be wrong.

## Implementation

```python
import numpy as np
from scipy.stats import norm

def bsm_call(S, K, r, T, sigma):
    """Black-Scholes-Merton call price."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def bsm_vega(S, K, r, T, sigma):
    """Vega: sensitivity of call price to sigma."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return S * np.sqrt(T) * norm.pdf(d1)

def implied_vol_newton(market_price, S, K, r, T,
                       sigma0=0.20, tol=1e-8, max_iter=100):
    """
    Compute implied volatility via Newton-Raphson.
    Falls back to bisection if Newton diverges.
    """
    sigma = sigma0
    for i in range(max_iter):
        price = bsm_call(S, K, r, T, sigma)
        diff = price - market_price
        if abs(diff) < tol:
            return sigma
        vega = bsm_vega(S, K, r, T, sigma)
        if vega < 1e-10:
            # Vega too small — switch to bisection
            break
        sigma = sigma - diff / vega
        sigma = max(sigma, 1e-6)  # keep positive

    # Bisection fallback
    lo, hi = 1e-6, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if bsm_call(S, K, r, T, mid) < market_price:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return (lo + hi) / 2


# --- Example ---
S, K, r, T = 100, 100, 0.05, 0.5
market_price = 7.50

iv = implied_vol_newton(market_price, S, K, r, T)
print(f"Implied Volatility: {iv:.4f} ({iv*100:.2f}%)")
# Expected: ~0.2230 (22.30%)

# Verify round-trip
print(f"BSM price at IV: {bsm_call(S, K, r, T, iv):.4f}")
```

## Bridge to Quant / ML

- **Vol surface modeling:** Quants fit parametric models (SVI, SABR) to the IV surface to interpolate/extrapolate IVs at arbitrary strikes and expiries. This surface is the primary input to exotic option pricing.
- **Options market making:** Market makers quote in IV rather than dollars so that small price moves in the underlying don't make their quotes stale. This is why trading desks think in vol space.
- **Vol forecasting (ML):** One approach predicts the *next day's IV* using time-series models (GARCH, LSTMs). Alternatively, predict whether IV is "cheap" or "expensive" relative to subsequent realized volatility — this is the core alpha signal in many vol strategies.
- **Variance risk premium:** The difference $\mathbb{E}[\sigma_{\text{IV}}] - \mathbb{E}[\sigma_{\text{realized}}]$ is consistently positive — selling options is a long-run positive carry trade. This is a well-documented equity risk premium.
- **Calibration:** IV inversion is the most basic calibration step. All stochastic vol model calibrations (Heston, rough vol) generalize this: find model parameters so that model prices match the full IV surface.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** IV is described as the "market's collective forecast of future realized volatility." In what sense is this true, and in what sense is it misleading?
<details>
<summary>Answer</summary>
It is true in the sense that IV is the risk-neutral expectation of future volatility — the vol that makes the expected discounted payoff under Q equal to the market price. It reflects aggregate supply and demand from all option market participants, encoding their collective assessment of future uncertainty. It is misleading because IV is a risk-neutral quantity, not a real-world forecast. IV consistently exceeds realized volatility by 2–5 vol points on average for equity indices — this "variance risk premium" means sellers demand compensation for bearing vol risk. IV is not "what volatility will be"; it is "what volatility the market is willing to price, including a risk premium."
</details>

**Q2.** Why can't IV be solved for analytically from the BSM formula, and why does this require numerical methods?
<details>
<summary>Answer</summary>
The BSM formula C = S·N(d1) − Ke^{-rT}·N(d2) has σ appearing inside d1 and d2 in a nonlinear way — it appears both as σ√T in the denominator and as σ² inside the numerator. There is no algebraic manipulation that isolates σ on one side. The equation C_BSM(σ) = C_market is a transcendental equation in σ. Numerical methods (Newton-Raphson, bisection) find the root by iterative refinement: guess σ, compute the BSM price, compare to market price, adjust σ in the direction that reduces the error, repeat until convergence.
</details>

**Q3.** A deep in-the-money call has very low vega. Why does this create numerical problems for Newton-Raphson IV computation, and what does the code do about it?
<details>
<summary>Answer</summary>
Newton-Raphson updates: σ_new = σ_old − (C_BSM − C_market) / vega. If vega is near zero (deep ITM option has most of its value as intrinsic, with very little time value sensitive to vol), the denominator is tiny. A small pricing difference in the numerator produces an enormous σ update — the algorithm takes a massive step and overshoots, potentially producing negative σ or diverging entirely. The code handles this with `if vega < 1e-10: break` — it abandons Newton-Raphson when vega is too small and switches to bisection, which is slower but guaranteed to converge by bracketing the root between known bounds.
</details>

---

### Level 2 — Quantitative

**Q4.** S = 100, K = 110 (out-of-the-money call), r = 5%, T = 0.25 years. You observe the call trading at \$1.50. Without running the code, reason about whether IV will be higher or lower than 20%, given that BSM with σ = 20% prices an ATM call at roughly \$4.00.
<details>
<summary>Answer</summary>
The OTM call (K = 110 > S = 100) is worth less than an ATM call because it requires a larger stock move to end up in-the-money. BSM with σ = 20% would price this OTM call at roughly \$1.00–\$1.50 (significantly less than the \$4 ATM call). The observed price of \$1.50 is at the high end of what 20% vol would produce. To verify: run the Newton-Raphson solver. If BSM(σ=0.20) ≈ \$1.20 and market is \$1.50, then IV > 20% — likely around 24–26%. This is consistent with the equity volatility skew: OTM calls tend to have IV slightly above ATM, but less dramatically than OTM puts.
</details>

**Q5.** Perform one iteration of Newton-Raphson to find the IV for: S = 100, K = 100, r = 5%, T = 0.5 years, market price = \$7.50, starting guess σ_0 = 0.20. Show the computation of d1, the BSM price, the vega, and the updated σ.
<details>
<summary>Answer</summary>
σ_0 = 0.20:
d1 = [ln(100/100) + (0.05 + 0.02) × 0.5] / (0.20 × √0.5) = [0 + 0.035] / 0.1414 = 0.2475.
d2 = 0.2475 − 0.1414 = 0.1061.
N(0.2475) ≈ 0.5977, N(0.1061) ≈ 0.5423.
C_BSM = 100 × 0.5977 − 100 × e^{-0.025} × 0.5423 = 59.77 − 97.53 × 0.5423 = 59.77 − 52.90 = 6.87.

Vega = S × √T × n(d1) = 100 × 0.7071 × n(0.2475). n(0.2475) = (1/√(2π)) × e^{-0.0306} ≈ 0.3867.
Vega = 100 × 0.7071 × 0.3867 = 27.35.

σ_1 = 0.20 − (6.87 − 7.50) / 27.35 = 0.20 − (−0.63) / 27.35 = 0.20 + 0.023 = 0.223.
After one iteration, σ ≈ 22.3%.
</details>

---

### Level 3 — Coding

**Q6.** The `implied_vol_newton` function has a fallback to bisection when `vega < 1e-10`. Why is the bisection search bounded between `lo = 1e-6` and `hi = 5.0` rather than, say, `lo = 0` and `hi = 100`? What would go wrong with those bounds?
<details>
<summary>Answer</summary>
The bisection requires a valid bracket: `bsm_call(lo)` must be below `market_price` and `bsm_call(hi)` must be above it. Two problems with `lo = 0` and `hi = 100`: (1) At σ = 0, BSM call price becomes max(S − Ke^{-rT}, 0) — the intrinsic value. For OTM options, this is zero and the function is not differentiable at zero; `bsm_call(σ=0)` may not be well-defined numerically due to division by σ√T in d1. Using `lo = 1e-6` avoids the singularity. (2) At σ = 100.0, BSM call approaches S (the stock price) because an option with 10,000% vol is almost certain to end in the money. For typical market prices (far below S), this upper bound is fine, but it forces 200 bisection iterations to converge to the same accuracy as `hi = 5.0`, wasting computation. The bounds [1e-6, 5.0] cover all realistic implied vols (0.0001% to 500%) while keeping the algorithm numerically stable.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| IV predicts what volatility will actually be | IV is a risk-neutral measure — it includes a variance risk premium and reflects supply/demand for options. It consistently overstates subsequent realized vol by 2–5 points on average |
| Lower IV means the market expects calm conditions | Low IV means option buyers and sellers have agreed on a low vol price. This consensus can be wrong — IV was very low just before the 2020 COVID crash |
| A call and put on the same strike can have different IVs | By put-call parity, they must have the same IV at any given strike and expiry. Different IVs signal a data error or a genuine (brief) arbitrage |
| IV computation always converges cleanly | Deep ITM or very short-dated options have near-zero vega, causing Newton-Raphson to diverge. Bisection fallback and careful numerical bounds are required for production-grade solvers |

## Related Concepts

- [[Black-Scholes Model]]
- [[Volatility Smile]]
- [[Variance Swap]]
- [[VIX]]
- [[Option Greeks]]
- [[Volatility Surface]]
- [[Gamma Scalping]]

## Sources Used

- Hull, *Options, Futures, and Other Derivatives*, Ch. 19 (The Greek Letters and Implied Volatility)
- Hull, Ch. 15 (The Black-Scholes-Merton Model) for BSM formula derivation

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | Hull + initial build |
| 2026-04-12 | Note created | bootstrap |
| 2026-04-11 | QA review: fixed [[Greeks]] → [[Option Greeks]]; added [[Volatility Surface]] to Related Concepts | quality review |
