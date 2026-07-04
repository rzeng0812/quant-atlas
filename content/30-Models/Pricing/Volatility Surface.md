---
type: concept
domain: 30-Models
tags: [volatility, options]
status: math
stability: evolving
confidence: high
last_reviewed: 2026-04-12
review_interval_days: 90
sources:
  - "Gatheral - The Volatility Surface ch.1"
  - "Hull ch.20"
created: 2026-04-12
---

> Implied vol as a function of strike and expiry; the market's fingerprint of non-lognormal returns

> [!info] Problem Chain
> **Chain:** Pricing → Gap 5: BSM assumes constant σ — real markets show a volatility smile
> **This concept:** Documents and parameterizes the entire landscape of implied vols across strikes and maturities — the empirical fact that Gap 5 is trying to address; the target that all Gap 5 models must reproduce
> **Alternative approaches to this gap:** [[Local Volatility]] (Solution A), [[Heston Model]] (Solution B), [[Merton Jump-Diffusion]] (Solution C) — these are models calibrated to fit this surface
> **You need first:** [[Black-Scholes Model]], [[Implied Volatility]], [[Volatility Smile]]
> **This unlocks:** [[Local Volatility]], [[Heston Model]], [[SABR Model]] — each of these is a model for the surface

## Why This Exists

**The gap:** Black-Scholes produces a single implied volatility for all options on the same underlying. When practitioners began looking at market prices across all listed strikes and maturities, they found something inconsistent: inverting BSM on each option produced a different σ for every strike and maturity. This was not data noise — it was a systematic pattern that repeated every day and moved with the market.

**What came before:** In the early days of options markets (post-1973), traders used BSM as if constant vol were approximately true. But the 1987 crash changed everything: post-crash, OTM put implied vols were persistently and dramatically higher than ATM vols. The market had "learned" that crashes happen, and it priced the insurance accordingly. BSM could not describe this — it would assign the same σ to an OTM put as to an ATM option.

**What this adds:** The volatility surface is the empirical observation that implied vol is a function of two variables — strike K and maturity T — not a constant. It provides a complete, option-market-consistent description of the market's collective view of return distributions: the left tail is fat (puts expensive), uncertainty decays with time (term structure), and the entire surface moves dynamically with the market. Parameterizing this surface (via SVI, SABR, or model-implied) is the prerequisite step before any serious options pricing or risk management.

**What it still doesn't solve:** The surface is a static snapshot — it describes prices now but not how they will evolve. Every model (Local Vol, Heston, SABR) must both fit the current surface and make predictions about its future dynamics. Models that fit today's surface can still predict the wrong forward smiles (this is Local Vol's main weakness) or fail to capture extreme short-dated moves.

## Math Concepts

The volatility surface is the function:

$$\sigma_{imp}(K, T) : \text{strike} \times \text{expiry} \to \text{implied vol}$$

**Two dimensions:**
- **Smile / skew** (across strikes at fixed $T$): how IV varies with moneyness
- **Term structure** (across expiries at fixed $K$): how IV varies with time to expiry

**Moneyness conventions:**
- Simple: $K/S_0$ (ratio of strike to spot)
- Log-moneyness: $\ln(K/F)$ where $F = S_0 e^{rT}$ is the forward
- Delta: options quoted by their BSM delta (25-delta put, ATM, 25-delta call)

**Surface parameterizations** — the raw surface from quotes is noisy and incomplete; practitioners fit smooth models:
- **SVI (Stochastic Volatility Inspired):** $w(k) = a + b[\rho(k-m) + \sqrt{(k-m)^2 + \sigma^2}]$, where $w = \sigma_{imp}^2 \cdot T$ is total implied variance and $k = \ln(K/F)$. Gatheral (2004). 5 parameters per slice.
- **SSVI:** surface extension of SVI ensuring no calendar spread arbitrage across expiries.
- Model-implied surface: run [[Heston Model]] or [[SABR Model]], calibrate to quotes, read off the surface.

**No-arbitrage constraints** — a valid surface must satisfy:
1. **Butterfly arbitrage free:** $\partial^2 C / \partial K^2 \geq 0$ (call price is convex in strike)
2. **Calendar spread arbitrage free:** total variance $w(k,T)$ is non-decreasing in $T$
3. **No negative density:** Breeden-Litzenberger risk-neutral density $q(K,T) = e^{rT} \partial^2 C/\partial K^2 \geq 0$

## Walkthrough

A typical equity vol surface (e.g., S&P 500) looks like:

| Expiry | 80% strike | 90% | 100% (ATM) | 110% | 120% |
|--------|-----------|-----|------------|------|------|
| 1M | 28% | 22% | 17% | 15% | 14% |
| 3M | 26% | 21% | 17% | 15% | 14% |
| 6M | 25% | 20% | 17% | 15% | 14% |
| 1Y | 24% | 20% | 18% | 16% | 15% |

Key observations:
- **Negative skew:** OTM puts (low strikes) are more expensive than OTM calls — crash fear
- **Term structure:** short-dated IV more volatile; long-dated IV more stable
- **Smile flattens** at longer expiries — uncertainty averages out

## Analysis

- **The surface is dynamic:** it moves every day as the market updates its view. Managing a book means hedging against surface movements, not just spot movements.
- **Sticky strike vs sticky delta:** when spot moves, does the surface stay fixed by strike (sticky strike) or by delta (sticky delta / sticky moneyness)? Different dynamics, different hedging strategies.
- **Forward smile:** the surface today implies a surface at future dates. [[Local Volatility]] and [[Heston Model]] make different predictions for forward smiles — this matters for exotic options.
- **Gaps and illiquidity:** the surface only has reliable data at liquid strikes/expiries. Interpolation (SVI) and extrapolation into tails is model-dependent and risky.

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RectBivariateSpline

def build_vol_surface(strikes, expiries, iv_matrix):
    """
    Fit a smooth vol surface via 2D spline interpolation.
    iv_matrix[i,j] = implied vol at expiries[i], strikes[j]
    """
    spline = RectBivariateSpline(expiries, strikes, iv_matrix, kx=3, ky=3)
    return spline

def plot_vol_surface(strikes, expiries, iv_matrix):
    K, T = np.meshgrid(strikes, expiries)
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(K, T, iv_matrix, cmap='viridis', alpha=0.8)
    ax.set_xlabel('Strike'); ax.set_ylabel('Expiry (yr)'); ax.set_zlabel('Implied Vol')
    ax.set_title('Volatility Surface')
    plt.tight_layout(); plt.show()

# Example SPX-like surface
strikes  = np.array([0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20])
expiries = np.array([1/12, 3/12, 6/12, 1.0, 2.0])
iv_matrix = np.array([
    [0.28, 0.25, 0.22, 0.19, 0.17, 0.16, 0.15, 0.15, 0.14],
    [0.26, 0.23, 0.21, 0.19, 0.17, 0.16, 0.15, 0.15, 0.14],
    [0.25, 0.22, 0.20, 0.18, 0.17, 0.16, 0.15, 0.14, 0.14],
    [0.24, 0.22, 0.20, 0.18, 0.18, 0.16, 0.16, 0.15, 0.15],
    [0.23, 0.21, 0.19, 0.18, 0.18, 0.17, 0.16, 0.15, 0.15],
])
plot_vol_surface(strikes, expiries, iv_matrix)
```

## Bridge to Quant / ML

- The vol surface is a rich ML input: predicting its next-day shape, detecting arbitrage violations, and interpolating sparse quotes are all active research problems
- **Neural vol surfaces:** deep learning models (e.g., neural SVI) learn to fit surfaces with no-arbitrage constraints baked into the architecture
- Risk management: Vega bucketing — decompose portfolio Vega across surface grid points to understand where exposure lives
- Connection to [[Regime Detection]]: surface shape (level of skew, term structure slope) is a powerful regime indicator

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why do OTM puts on equity indices consistently trade at higher implied vol than ATM options (the "skew"), even in calm markets?
<details>
<summary>Answer</summary>
There are two complementary explanations. First, the real-world return distribution of equity indices has a fat left tail — the probability of large crashes is higher than a lognormal distribution implies. Options pricing under the risk-neutral measure reflects this, so the market charges extra for OTM puts (crash insurance). Second, there is a structural demand imbalance: institutions (pension funds, mutual funds) systematically buy OTM puts to protect equity portfolios, while there are few natural sellers — so the insurance premium is persistently elevated beyond what pure risk-neutral valuation would suggest. Both effects compound: fat tails raise the model price, and excess demand raises the market price further. This is why the equity skew persists even in normal volatility regimes.
</details>

**Q2.** What is the difference between "sticky strike" and "sticky delta" (sticky moneyness) behavior, and why does it matter for delta hedging?
<details>
<summary>Answer</summary>
When the stock moves, the vol surface can shift in two ways:
- Sticky strike: the implied vol at each fixed strike K stays constant as S moves. The vol at K=90 stays at 22% whether the stock is at 95 or 105. This implies that as the stock falls, the ATM vol decreases (because the ATM strike, which was at 100, is no longer ATM).
- Sticky delta (sticky moneyness): the implied vol at each delta level stays constant as S moves. The 25-delta put always trades at, say, 22% regardless of where the stock is. As the stock falls, the entire vol surface shifts lower in strike space.

For delta hedging, this matters enormously. Under sticky strike, the option's delta is just the BSM delta (since vol doesn't change when S moves). Under sticky delta, the vol at your option's strike changes as S moves, creating an additional vanna (dDelta/dVol) contribution to the hedge. Real equity markets are closer to sticky delta, which means BSM delta underestimates the true delta of OTM puts — a systematic hedging error for vol-naive traders.
</details>

**Q3.** What are the two no-arbitrage conditions a valid vol surface must satisfy, and what kinds of trades would be possible if they were violated?
<details>
<summary>Answer</summary>
1. **Butterfly (strike) arbitrage free:** ∂²C/∂K² ≥ 0 — call prices must be convex in strike. Equivalently, the risk-neutral probability density q(K) = e^{rT}·∂²C/∂K² must be non-negative everywhere. If violated, you can construct a butterfly spread (buy two wing strikes, sell the middle) that costs nothing but pays positive in some scenario — free money.

2. **Calendar spread arbitrage free:** Total implied variance w(k,T) = σ_imp²(K,T)×T must be non-decreasing in T for each fixed log-moneyness k. If violated, you can buy the shorter-dated option and sell the longer-dated option at the same strike and collect a premium while having a position that is always worth something at the shorter expiry — free money.

Both conditions have direct consequences: if the surface has negative local variance anywhere (from Dupire's formula), that's a signal of butterfly arbitrage. If total variance decreases in T, that's calendar arbitrage. Any parameterization of the surface (SVI, SABR, spline) must be checked against these conditions before it can be used for consistent pricing.
</details>

---

### Level 2 — Quantitative

**Q4.** Using the typical SPX surface given in the walkthrough, compute the slope of the vol smile at the 1-month expiry. Express this as "vol per unit of moneyness (strike/spot)." What does this number tell a trader?
<details>
<summary>Answer</summary>
From the table, at T=1M:
- Strike 80% → IV = 28%
- Strike 90% → IV = 22%
- Strike 100% (ATM) → IV = 17%
- Strike 110% → IV = 15%

Slope from 90% to 100% (left side of ATM):
Δ IV / Δ(K/S) = (17% − 22%) / (100% − 90%) = −5% / 10% = **−0.5 vol % per % moneyness**

Slope from 100% to 110% (right side):
= (15% − 17%) / (110% − 100%) = −2% / 10% = **−0.2 vol % per % moneyness**

The left side of ATM has 2.5× more slope than the right side — confirming strong left skew for 1-month SPX options.

For a trader, the 1-month skew slope of −0.5 on the left means: for every 1% you move below ATM in strike, implied vol increases by 0.5%. This directly calibrates how much to charge for OTM puts relative to ATM. A trader who buys a 95% put and sells an ATM put (a put spread) benefits from this skew — the bought put is expensive relative to a flat-vol world.
</details>

**Q5.** Suppose the 1-year ATM implied vol is 17% and the 1-month ATM implied vol is also 17%. What does the SVI parameterization's term structure parameter tell us about the market's expectation of near-term vs. long-term volatility? Now suppose the 1-month vol spikes to 25% while the 1-year vol stays at 17%. Interpret this in terms of the vol term structure.
<details>
<summary>Answer</summary>
When 1-month and 1-year ATM vols are both 17%, the total implied variance is:
- 1-month: w(T=1/12) = 17%² × 1/12 = 0.0289/12 = 0.0024
- 1-year: w(T=1) = 17%² × 1 = 0.0289

The 1-month vol accounts for 0.0024/0.0289 = 8.3% of the annual variance budget in 8.3% of the time — exactly proportional. This is a flat vol term structure: the market assigns roughly the same vol to every month of the year.

When 1-month vol spikes to 25% while 1-year stays at 17%:
- 1-month total variance: 25%² × 1/12 = 0.0625/12 = 0.0052
- 1-year total variance: 17%² × 1 = 0.0289

The 1-month accounts for 0.0052/0.0289 = 18% of annual variance in 8.3% of the time — the market assigns more than double its proportional share to the near term. This is an inverted term structure: the market expects near-term turbulence but a return to calm over the longer horizon. This is typical during crises (VIX spike, earnings, Fed meetings) — fear is priced in the front of the curve, but long-dated uncertainty remains anchored.
</details>

---

### Level 3 — Coding

**Q6.** The `build_vol_surface` function uses `RectBivariateSpline` with `kx=3, ky=3` (cubic splines in both dimensions). What would happen if you used linear interpolation (`kx=1, ky=1`) instead, and why does this matter for downstream use with the Dupire local vol formula?
<details>
<summary>Answer</summary>
Linear interpolation (`kx=1, ky=1`) produces a surface that is continuous but not smooth — the first and second derivatives are discontinuous at each knot (grid point). The Dupire local vol formula requires computing ∂C/∂T and ∂²C/∂K² — the first derivative in T and second derivative in K. With linear spline:

- ∂C/∂T is a step function (piecewise constant between maturities) — it jumps discontinuously at each maturity knot.
- ∂²C/∂K² is zero almost everywhere (linear segments have zero curvature) and undefined at the knots.

This makes the Dupire formula practically unusable: the second derivative in K is either zero (implying infinite local vol, since it appears in the denominator) or undefined at knots. The resulting local vol surface would be mostly NaN or ±∞. Cubic splines (`kx=3, ky=3`) have continuous first and second derivatives everywhere (by construction of cubic spline interpolation), providing smooth, well-behaved derivatives that the Dupire formula can use reliably. This is why smooth parameterizations (SVI, SABR, cubic splines) are always used before applying Dupire — the quality of the local vol surface is entirely determined by the smoothness of the input surface.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| The vol surface shows the market's view of future realized volatility | The surface shows implied (risk-neutral) volatility — a risk-adjusted measure that includes both the market's volatility forecast and a risk premium for volatility uncertainty. Implied vol is systematically higher than realized vol on average, by the volatility risk premium. |
| A flat vol surface means options are correctly priced by BSM | A flat surface means BSM is consistent with market prices at that moment. It does not mean the market is "right" or that BSM assumptions are satisfied — it might just mean implied volatility happens to be uniform that day. The surface becomes non-flat immediately when any tail event occurs. |
| SVI and SABR are models of how volatility behaves | They are parameterizations of the vol surface — compact descriptions of the shape. SABR has a stochastic vol interpretation, but SVI is purely a curve-fitting tool with no model dynamics. Neither predicts how the surface will move. |
| Managing portfolio vol means hedging against surface shifts | Managing vol means hedging vega (sensitivity to ATM vol). Managing the surface means also hedging skew (vanna: sensitivity to changes in skew) and curvature (volga/vomma: sensitivity to vol-of-vol). Full surface risk management requires decomposing vega into buckets across strikes and maturities — not just one number. |

## Related Concepts
- [[Implied Volatility]] — the value at each point on the surface
- [[Volatility Smile]] — the strike dimension of the surface
- [[Local Volatility]] — Dupire's model that exactly fits the surface
- [[Heston Model]] — stochastic vol model calibrated to the surface
- [[SABR Model]] — parameterizes the smile per expiry slice
- [[Black-Scholes Model]] — the model the surface is derived from (and that it violates)
- [[Option Greeks]] — Vega and Vanna describe sensitivity across the surface

## Sources Used
- Gatheral — *The Volatility Surface*, ch.1
- Hull — *Options, Futures & Other Derivatives*, ch.20

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | Gatheral ch.1 + Hull ch.20 |
| 2026-04-11 | QA review: added callout blurb; fixed path-based wikilink to [[Regime Detection]] | quality review |
