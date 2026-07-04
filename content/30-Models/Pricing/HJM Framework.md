---
type: concept
domain: 30-Models
tags: [pricing, interest-rates, fixed-income]
status: math
stability: evolving
confidence: high
last_reviewed: 2026-04-11
review_interval_days: 90
sources:
  - "Hull ch.31"
  - "Shreve Vol II ch.10"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Pricing → Gap for forward rate modeling: Short-rate models derive the curve from one number; practitioners need a framework that models the entire yield curve jointly
> **This concept:** The meta-framework that models the entire forward rate curve as a system of SDEs; the no-arbitrage drift condition shows that once you choose volatility, the drift of every forward rate is fully determined
> **Alternative approaches to this gap:** [[Vasicek Model]], [[Hull-White Model]] — these are special cases of HJM (specific vol specifications); [[SABR Model]] combined with LMM is the practical implementation
> **You need first:** [[Vasicek Model]], [[Hull-White Model]], [[Ito's Lemma]], [[Risk-Neutral Measure]]
> **This unlocks:** [[Hull-White Model]] (emerges from HJM with exponential vol), LIBOR Market Model (practical HJM implementation), [[Interest Rate Swaps]], complex rate exotic pricing

## Why This Exists

**The gap:** Short-rate models (Vasicek, CIR, Hull-White) model a single number — today's short-term interest rate — and derive all bond prices from it. But when the short rate changes, all yields across all maturities move together in a perfectly correlated way (one Brownian driver). Real yield curves don't behave like this: the short end can move independently of the long end (twist movements), and the 2-year rate often diverges from the 30-year rate. Practitioners modeling complex interest rate derivatives — particularly those sensitive to multiple parts of the curve simultaneously — needed a richer framework.

**What came before:** Each short-rate model was its own special case, derived independently. There was no unifying framework that could describe all possible interest rate dynamics consistently. Practitioners choosing between Vasicek and CIR were choosing between two different model philosophies without a common language.

**What this adds:** Heath, Jarrow, and Morton (1992) modeled the entire forward rate curve directly: every point f(t,T) on the curve has its own SDE. The critical insight is the HJM drift condition — once you specify the volatility function σ(t,T), the no-arbitrage condition uniquely determines the drift. You cannot freely choose both; σ determines μ completely. This reveals that all arbitrage-free interest rate models are parameterized entirely by their vol specification σ(t,T), and that Vasicek, Hull-White, and Ho-Lee are all special cases corresponding to different σ choices. HJM also fits today's curve exactly by construction — the initial forward curve f(0,T) is an input to the model.

**What it still doesn't solve:** In general, the HJM forward rate f(t,T) depends on the entire path of the Brownian motion up to time t — the model is non-Markovian. This means you cannot write a PDE in a finite state space; you must use Monte Carlo to price most products. Only special σ(t,T) specifications (like exponential decay) produce Markovian models reducible to tractable short-rate dynamics. The practical implementation of HJM for market-quoted instruments (caps, swaptions) uses the LIBOR Market Model (LMM/BGM), which discretizes the forward curve to observable LIBOR rates.

## Math Concepts

**Forward rate $f(t, T)$:** the instantaneous interest rate contracted at time $t$ for borrowing at time $T$. The yield curve is the collection of all $f(0, T)$ for varying $T$.

**HJM SDE** — under the real-world measure, each forward rate evolves as:

$$df(t, T) = \mu(t, T)\,dt + \sigma(t, T)\,dW_t$$

where $\mu$ and $\sigma$ can be arbitrary (possibly path-dependent) functions.

**The HJM drift condition** — under the [[Risk-Neutral Measure]] $\mathbb{Q}$, no-arbitrage forces:

$$\mu(t, T) = \sigma(t, T) \int_t^T \sigma(t, u)\,du$$

This is the key result. The drift of every forward rate is *not free* — it is completely determined by the volatility structure. You only get to choose $\sigma(t, T)$; the drift is implied.

**Bond price** from the forward curve:

$$P(t, T) = \exp\!\left(-\int_t^T f(t, u)\,du\right)$$

**Recovering short-rate models as special cases:**
- If $\sigma(t, T) = \sigma$ (constant): recovers Ho-Lee model
- If $\sigma(t, T) = \sigma e^{-\kappa(T-t)}$: recovers Hull-White (extended Vasicek)
- HJM is a *meta-framework* — most short-rate models are special cases

## Walkthrough

Suppose you observe today's forward curve $f(0, T)$ from market bond prices. You choose a volatility specification $\sigma(t,T) = \sigma_0 e^{-\kappa(T-t)}$.

1. The HJM drift condition gives: $\mu(t,T) = \sigma_0 e^{-\kappa(T-t)} \cdot \frac{\sigma_0}{\kappa}(1 - e^{-\kappa(T-t)})$
2. Simulate paths of $f(t,T)$ for all $T$ jointly using the SDE
3. Compute bond prices $P(t,T) = \exp(-\int_t^T f(t,u)\,du)$ at each time step
4. Price any interest rate derivative as $e^{-rT}\mathbb{E}^{\mathbb{Q}}[\text{payoff}]$

The model is calibrated to today's curve by construction — $f(0,T)$ is an *input*, not an output.

## Analysis

- **Non-Markovian in general:** the forward rate $f(t,T)$ depends on the full path of $W_s$ for $s \leq t$, not just the current state. This makes Monte Carlo necessary for most payoffs — no PDE approach.
- **Markovian special cases:** certain $\sigma(t,T)$ specifications (exponential, separable) yield finite-dimensional Markov representations → recover tractable short-rate models.
- **Infinite-dimensional state space:** the full forward curve is the state. In practice, discretize to $N$ tenor points and model them jointly.
- **LIBOR Market Model (BGM):** the practical implementation of HJM using market-quoted forward LIBOR rates instead of instantaneous forward rates. Industry standard for caps, floors, and swaptions.

## Implementation

```python
import numpy as np

def simulate_hjm_ho_lee(f0, sigma, T_max, n_tenors, n_steps, n_paths, seed=42):
    """
    Simplest HJM: Ho-Lee model (constant sigma).
    f0: initial forward curve f(0, T) as array of length n_tenors
    Returns: forward curve paths shape (n_paths, n_steps+1, n_tenors)
    """
    rng = np.random.default_rng(seed)
    dt = T_max / n_steps
    tenors = np.linspace(0, T_max, n_tenors)

    # HJM drift: mu(t,T) = sigma^2 * (T - t)  [Ho-Lee]
    # f(t+dt, T) = f(t, T) + sigma^2*(T-t)*dt + sigma*dW
    paths = np.zeros((n_paths, n_steps + 1, n_tenors))
    paths[:, 0, :] = f0

    for step in range(n_steps):
        t = step * dt
        dW = rng.normal(0, np.sqrt(dt), n_paths)
        remaining = np.maximum(tenors - t, 0)           # T - t for each tenor
        drift = sigma**2 * remaining * dt               # HJM drift condition
        diffusion = sigma * dW[:, None]                 # same dW for all tenors
        paths[:, step + 1, :] = paths[:, step, :] + drift + diffusion

    return paths

# Example: flat initial curve at 4%
tenors = 50
f0 = np.full(tenors, 0.04)
paths = simulate_hjm_ho_lee(f0, sigma=0.01, T_max=5.0,
                             n_tenors=tenors, n_steps=252, n_paths=100)
```

## Bridge to Quant / ML

- HJM is the foundation for pricing interest rate exotics: Bermudan swaptions, CMS products, range accruals
- **ML calibration:** choosing $\sigma(t,T)$ to fit cap/floor/swaption vol surfaces is a high-dimensional calibration problem — neural networks are used to learn the mapping from market quotes to HJM vol parameters
- **Factor models of the curve:** PCA on daily yield curve changes reveals ~3 factors explain >99% of variance (level, slope, curvature) — a data-driven way to parameterize $\sigma(t,T)$
- Connection to [[Duration]] and [[Convexity]]: HJM makes the curve-shift assumptions of duration analysis explicit and generalized

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** What is the HJM drift condition, and why is it the central result of the framework?
<details>
<summary>Answer</summary>
The HJM drift condition states that under the risk-neutral measure Q, the drift of each forward rate f(t,T) is not free — it must equal: μ(t,T) = σ(t,T) × ∫_t^T σ(t,u) du. The drift at each maturity T is determined by the volatility σ at that maturity multiplied by the integral of all volatilities from t to T.

This is the central result because it means: once you choose your volatility structure σ(t,T), you have no remaining freedom in the drift. The entire dynamics of the forward curve are specified. Equivalently, any model that violates this condition allows arbitrage. This is why "choosing an interest rate model" reduces to "choosing σ(t,T)" — the rest follows mathematically. It also unifies all existing interest rate models: Vasicek, CIR, Ho-Lee, and Hull-White all correspond to different functional forms of σ(t,T), and they all automatically satisfy the drift condition by construction when derived within HJM.
</details>

**Q2.** Why does the HJM framework produce non-Markovian models in general, and why does this matter computationally?
<details>
<summary>Answer</summary>
The HJM forward rate at time t depends on the integrated history of σ(s,T)·dW_s for all s ≤ t — the full path of the Brownian motion, not just its current value. This is because the drift condition involves ∫_t^T σ(t,u) du, and σ(t,u) itself may depend on the path history. A Markovian process can be fully described by its current state; a non-Markovian process requires knowing where it has been. For computational pricing, Markovian processes admit PDE solutions (finite difference on a grid of current state values), while non-Markovian processes require Monte Carlo (you must simulate entire paths). A 1D PDE can be solved in milliseconds; Monte Carlo requires thousands of paths and takes seconds to minutes. For exotic derivatives (Bermudans, range accruals) that need early exercise decisions, Monte Carlo with American exercise is especially expensive (requires Longstaff-Schwartz regression). This is why the exponential vol specification (yielding Hull-White, which is Markovian) is preferred over more complex HJM specs despite its limited flexibility.
</details>

**Q3.** Show that Ho-Lee (constant σ) and Hull-White (exponential vol) are special cases of HJM by stating what σ(t,T) each corresponds to, and what their drift conditions reduce to.
<details>
<summary>Answer</summary>
**Ho-Lee:** σ(t,T) = σ (constant, independent of t and T).

HJM drift: μ(t,T) = σ × ∫_t^T σ du = σ² × (T−t)

So df(t,T) = σ²(T−t)dt + σ dW. This is the Ho-Lee forward rate SDE. It implies a short rate that is Gaussian with linearly growing variance — no mean reversion. Rates wander without bound.

**Hull-White:** σ(t,T) = σ·e^{−α(T−t)} (exponential decay in maturity T−t).

HJM drift: μ(t,T) = σe^{−α(T−t)} × ∫_t^T σe^{−α(u−t)} du = σe^{−α(T−t)} × (σ/α)(1−e^{−α(T−t)})

When you integrate over T to get the short rate (r_t = f(t,t)), this produces exactly the Hull-White drift θ(t) − α·r_t — mean-reverting with exponential pull. The exponential vol spec is precisely what gives Hull-White its mean-reversion and Markovian property.
</details>

---

### Level 2 — Quantitative

**Q4.** In the Ho-Lee model (constant σ = 0.01), the HJM drift is μ(t,T) = σ²(T−t). Compute the expected change in the 5-year forward rate over one year from now (i.e., from T=5 looking at E[f(1,5) − f(0,5)]).
<details>
<summary>Answer</summary>
Under the Ho-Lee HJM drift condition, the expected change in f(t,T) over [0,1] is:

E[f(1,T) − f(0,T)] = ∫_0^1 μ(t,T) dt = ∫_0^1 σ²(T−t) dt

For T=5:

= σ² ∫_0^1 (5−t) dt = σ² [5t − t²/2]_0^1 = σ² (5 − 0.5) = σ² × 4.5

= (0.01)² × 4.5 = 0.0001 × 4.5 = **0.00045** (4.5 basis points)

The expected change in the 5-year forward rate over one year is +4.5 bps, purely from the convexity drift (risk-neutral drift correction). This is small but non-zero — it accumulates over time and represents the "convexity adjustment" that distinguishes forward rates from expected future spot rates in interest rate theory. Note: this is the risk-neutral drift, not a real-world prediction.
</details>

**Q5.** The bond price in HJM is P(t,T) = exp(−∫_t^T f(t,u) du). If the entire forward curve shifts up by 1% (i.e., all f(0,u) increase by 0.01), what is the approximate percentage change in P(0,10)? Connect this to the concept of duration.
<details>
<summary>Answer</summary>
P(0,10) = exp(−∫_0^{10} f(0,u) du)

If all forward rates increase by Δ = 0.01:

New P = exp(−∫_0^{10} [f(0,u) + 0.01] du) = exp(−∫_0^{10} f(0,u) du − 0.01×10) = P(0,10) × e^{−0.1}

Percentage change = e^{−0.1} − 1 ≈ −0.1 + 0.005 − ... ≈ **−9.52%**

More precisely: ΔP/P ≈ −Duration × Δ where Duration for a zero-coupon bond with maturity T is exactly T. For T=10: ΔP/P = −10 × 0.01 = **−10%** (first-order approximation).

The second-order correction (convexity ≈ T²) gives: ΔP/P ≈ −10×0.01 + ½×100×0.0001 = −0.10 + 0.005 = −9.5%.

This directly connects HJM to duration: in the HJM framework, sensitivity to a parallel shift in the forward curve equals the maturity T of the bond — which is exactly the modified duration of a zero-coupon bond. HJM makes this precise by specifying that duration is the sensitivity of the log-bond-price to the entire forward curve, not just the yield-to-maturity.
</details>

---

### Level 3 — Coding

**Q6.** In the `simulate_hjm_ho_lee` function, the same Brownian increment `dW` (shape: N_paths) is applied to all tenors simultaneously via `sigma * dW[:, None]`. This means all forward rates move by the same amount in each time step. What does this imply about the correlation structure, and how would you modify the code to allow different tenors to have partially correlated movements (as in a 2-factor HJM model)?
<details>
<summary>Answer</summary>
Using a single dW for all tenors means all forward rates have correlation 1 — a one-factor model where the entire curve moves up or down in lockstep. The only variation is in the drift (σ²×(T−t) differences across maturities), but the random shocks are perfectly correlated.

To implement a 2-factor HJM model, you would:

1. Define two orthogonal Brownian motions dW₁ and dW₂ (each shape: N_paths).
2. Specify two volatility functions σ₁(t,T) and σ₂(t,T) — e.g., σ₁ = σ_level (a level factor, same for all T) and σ₂ = σ_slope × (T−t) (a slope factor, increasing with maturity).
3. The diffusion term becomes: σ₁(t,T)×dW₁[:, None] + σ₂(t,T)×dW₂[:, None].
4. The drift condition becomes: μ(t,T) = σ₁(t,T)×∫_t^T σ₁(t,u)du + σ₂(t,T)×∫_t^T σ₂(t,u)du.

With two factors, parallel shifts are captured by W₁ and slope changes (short vs. long rates diverging) by W₂. The correlation between the 2-year and 10-year forward rates would be less than 1, matching the real market where long-end yields often move independently of short-end yields.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| HJM is a specific model you calibrate and use | HJM is a meta-framework — a set of conditions that all arbitrage-free interest rate models must satisfy. It is not itself a model; you must specify σ(t,T) to get a concrete model (Ho-Lee, Hull-White, LMM). |
| The HJM drift condition means you cannot choose the drift | It means you cannot independently choose both drift and diffusion. Once σ(t,T) is fixed, the risk-neutral drift is determined. You are free to choose any σ(t,T) you want — that choice determines the entire model. |
| HJM requires the entire forward curve as input | HJM takes today's observed forward curve f(0,T) as an input (which is what gives exact fit to today's market). But specifying f(0,T) is not a model assumption — it is data. The model dynamics are determined by σ(t,T), which is a modeling choice. |
| All HJM models require Monte Carlo | Only non-Markovian HJM specs require Monte Carlo. HJM with separable or exponential vol specs (Ho-Lee, Hull-White) produce finite-dimensional Markov systems that admit PDE solutions and analytic bond pricing. The Markovian special cases are the ones widely used in practice. |

## Related Concepts
- [[Vasicek Model]] — a special case of HJM (exponential vol spec)
- [[Yield Curve]] — the object HJM models directly
- [[Risk-Neutral Measure]] — HJM drift condition derived under $\mathbb{Q}$
- [[Duration]] — first-order sensitivity of bond prices to parallel yield shifts
- [[Stochastic Differential Equations]] — the mathematical machinery

## Sources Used
- Hull — *Options, Futures & Other Derivatives*, ch.31
- Shreve — *Stochastic Calculus for Finance II*, ch.10

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | Hull ch.31 + Shreve II ch.10 |
| 2026-04-11 | QA review passed — drift condition, Ho-Lee special case, simulation code verified | QA review |
