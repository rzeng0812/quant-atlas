---
type: concept
domain: 30-Models
tags: [pricing, interest-rates, fixed-income]
status: math
stability: evolving
confidence: high
last_reviewed: 2026-04-18
review_interval_days: 90
sources:
  - "Hull & White (1990), Pricing Interest Rate Derivative Securities"
  - "Brigo & Mercurio — Interest Rate Models Theory and Practice, ch.3"
created: 2026-04-18
---

> Extended Vasicek with time-varying drift; fits the initial yield curve exactly by construction

> [!info] Problem Chain
> **Chain:** Pricing → Gap 5 extension: Vasicek cannot fit today's yield curve exactly with constant parameters
> **This concept:** Extends Vasicek by replacing the constant long-run mean with a time-varying function θ(t) uniquely determined by the market forward curve — guaranteeing exact fit to today's yield curve
> **Alternative approaches to this gap:** [[Vasicek Model]] (the predecessor, constant parameters only), [[HJM Framework]] (the general framework of which Hull-White is a special case)
> **You need first:** [[Vasicek Model]], [[Yield Curve]], [[Ito's Lemma]]
> **This unlocks:** [[HJM Framework]], [[Interest Rate Swaps]], [[Exotic Options]] (Bermudan swaption pricing)

## Why This Exists

**The gap:** Vasicek's model is elegant and analytically tractable, but with only four constant parameters it generates a single specific yield curve shape — and that shape almost never matches the market curve observed on any given day. Using Vasicek in production means your model systematically misprices the very bonds and swaps you are supposed to be hedging. Starting with the wrong curve means every subsequent derivative price is wrong from day one.

**What came before:** Vasicek (1977) was the foundational model, but practitioners immediately recognized that the four-parameter fit was too rigid. Various workarounds existed (refit the model daily, use different parameters for different maturities) but none provided a principled, internally consistent solution.

**What this adds:** Hull and White (1990) made the minimal possible change: replace the constant long-run mean b with a time-varying function θ(t). The key insight is that θ(t) is not an additional parameter to estimate — it is uniquely determined by the current market forward rate curve. Once you observe today's yield curve, θ(t) is computed analytically from the forward rates, and by construction the model reprices every zero-coupon bond on the market exactly. The cost is essentially zero: you retain all of Vasicek's analytical tractability (affine bond prices, closed-form bond options, efficient simulation), just with the initial curve fit built in.

**What it still doesn't solve:** Hull-White is still a one-factor Gaussian model — all rates move in lockstep (correlation = 1), and the model allows negative rates. With constant α and σ, it also cannot fit the full swaption volatility surface (only the overall level of rate vol, not the strike and tenor dependence). G2++ (two-factor Hull-White) addresses the one-factor limitation; SABR-LMM handles the vol surface.

---

## Math Concepts

### The SDE

$$dr_t = [\theta(t) - \alpha r_t]\,dt + \sigma\,dW_t$$

- $\alpha$ is the mean-reversion speed (same role as in Vasicek, typically constant).
- $\sigma$ is the short-rate volatility (constant in the basic model).
- $\theta(t)$ is the time-varying drift, chosen to fit the initial curve.

### Calibrating $\theta(t)$ to the Market Curve

Given today's observed market discount curve $P^M(0,t)$ and the implied instantaneous forward rate $f^M(0,t) = -\partial \ln P^M(0,t)/\partial t$, the exact fit condition yields:

$$\theta(t) = \frac{\partial f^M(0,t)}{\partial t} + \alpha\, f^M(0,t) + \frac{\sigma^2}{2\alpha}\!\left(1 - e^{-2\alpha t}\right)$$

This is not a free parameter to fit — it is uniquely determined by the market forward curve. Once $\alpha$ and $\sigma$ are chosen (from swaption vol calibration), $\theta(t)$ follows automatically.

### Affine Bond Price Formula

Zero-coupon bond prices have a closed-form affine structure:

$$P(t,T) = A(t,T)\cdot\exp(-B(t,T)\cdot r_t)$$

where:

$$B(t,T) = \frac{1 - e^{-\alpha(T-t)}}{\alpha}$$

$$\ln A(t,T) = \ln\!\frac{P^M(0,T)}{P^M(0,t)} + B(t,T)\,f^M(0,t) - \frac{\sigma^2}{4\alpha}\,B(t,T)^2\!\left(1 - e^{-2\alpha t}\right)$$

This is exactly the Vasicek affine structure, but with $A(t,T)$ absorbing the market initial curve. By construction, $P(0,T) = P^M(0,T)$ for all $T$ — the model reprices today's bond market exactly.

### Trinomial Tree

The standard implementation for American/Bermudan products is a trinomial tree on the short rate. The tree is constructed to match the mean-reversion and volatility of $r$, then the $\theta(t)$ layer is "fitted" on top to ensure each node reproduces the market discount factors. Hull and White (1994) describe this construction in detail.

### Connection to HJM

Hull-White is a special case of the Heath-Jarrow-Morton framework. The HJM drift restriction, when combined with the exponential volatility specification $\sigma(t,T) = \sigma e^{-\alpha(T-t)}$, reduces to exactly the Hull-White SDE. This shows that Hull-White is internally arbitrage-free by construction.

---

## Walkthrough

### Setup

Start with a flat initial yield curve: $r_0 = 3\%$ everywhere, so $P^M(0,T) = e^{-0.03T}$ and $f^M(0,T) = 0.03$ for all $T$.

Choose $\alpha = 0.10$ (slow mean reversion, half-life ~7 years) and $\sigma = 0.01$ (1% annualized short-rate vol).

### Vasicek vs. Hull-White

Under Vasicek with constant long-run mean $b$, the model-implied forward rate at horizon $T$ is:

$$f^{\text{Vasicek}}(0,T) = b + (r_0 - b)e^{-\alpha T} + \frac{\sigma^2}{2\alpha^2}(1 - e^{-\alpha T})^2$$

Unless $b$ is chosen very carefully (and $\sigma$ is small), this will diverge from $f^M(0,T) = 0.03$ at all maturities. The mismatch is systematic.

Under Hull-White, $\theta(t)$ is set by the formula above. For a flat curve, $\partial f^M/\partial t = 0$, so:

$$\theta(t) = \alpha \cdot 0.03 + \frac{\sigma^2}{2\alpha}\!\left(1 - e^{-2\alpha t}\right) \approx 0.003 + \text{small correction}$$

The model forward rate reproduces $f^M(0,T) = 0.03$ exactly for all $T$ — verified by plugging back into the affine formula.

### Rate Shock

Suppose the short rate rises from 3% to 5% instantaneously. The affine formula gives a new $P(0,T)$ for each $T$, implying a shifted yield curve. Because $B(t,T) = (1-e^{-\alpha(T-t)})/\alpha$ saturates to $1/\alpha$ for long maturities, long-end yields move less than short-end yields — the model naturally produces a parallel-plus-twist response with mean-reversion dampening the long end.

---

## Analysis

### Strengths

- **Exact initial curve fit.** No repricing error on the vanilla instruments used as hedges — essential for a production derivatives book.
- **Analytic tractability.** Closed-form bond prices, caps, floors, and European swaption prices (via bond option formula).
- **Trinomial tree.** Efficient implementation for Bermudan and callable structures without Monte Carlo.
- **Industry standard.** Universally used for CVA/XVA, rate risk sensitivities (DV01, key rate durations), and vanilla rate derivative pricing.

### Weaknesses

- **Gaussian — negative rates possible.** Because the SDE is Gaussian, $r_t$ can go negative. In the post-2008 and post-2022 environment this is sometimes a feature, but it implies negative nominal rates with nonzero probability even when undesired.
- **Constant $\alpha$ and $\sigma$.** With only two scalar parameters, the model cannot fit the full implied vol surface of swaptions (the "vol surface" in rates space). Practitioners extend to time-varying $\alpha(t)$ and $\sigma(t)$ for better swaption calibration.
- **One-factor limitation.** All rates move together with correlation 1 (one Brownian driver). Real curves have richer dynamics — parallel shifts, steepening, curvature changes. G2++ (two-factor Hull-White) captures the first two principal components independently.
- **Mean reversion vs. vol tradeoff.** $\alpha$ and $\sigma$ are partially degenerate for fitting ATM swaption vols alone — you need a richer calibration set to identify both.

### Industry Usage

Hull-White (or G2++) is the baseline model for interest rate derivatives at most bank trading desks. It is the standard choice for CVA and XVA calculations where thousands of exposure paths must be simulated efficiently. For pricing complex exotics (range accruals, TARNs), it is often superseded by SABR-LMM or full smile models.

---

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# ─── Market curve helpers ─────────────────────────────────────────────────────

def flat_discount(T, r=0.03):
    """Flat 3% continuous discount curve."""
    return np.exp(-r * T)

def flat_forward(T, r=0.03):
    """Instantaneous forward rate for flat curve."""
    return np.full_like(np.atleast_1d(T), r, dtype=float)

def flat_forward_deriv(T, r=0.03):
    """Derivative of forward rate w.r.t. T for flat curve (zero for flat)."""
    return np.zeros_like(np.atleast_1d(T), dtype=float)


# ─── theta(t) calibration ─────────────────────────────────────────────────────

def theta(t, alpha, sigma, fwd_fn, dfwd_fn):
    """
    Hull-White theta(t) from initial forward curve.

    theta(t) = df^M(0,t)/dt + alpha * f^M(0,t) + sigma^2/(2*alpha) * (1 - exp(-2*alpha*t))
    """
    t = np.atleast_1d(t)
    return dfwd_fn(t) + alpha * fwd_fn(t) + (sigma**2 / (2 * alpha)) * (1 - np.exp(-2 * alpha * t))


# ─── Affine bond pricing ───────────────────────────────────────────────────────

def B_hw(t, T, alpha):
    """B(t,T) factor in Hull-White affine bond formula."""
    return (1 - np.exp(-alpha * (T - t))) / alpha

def ln_A_hw(t, T, alpha, sigma, disc_fn, fwd_fn):
    """
    ln A(t,T) for Hull-White zero bond P(t,T) = A(t,T) * exp(-B(t,T)*r_t).
    Requires market discount curve P^M(0,·) and forward curve f^M(0,·).
    """
    B = B_hw(t, T, alpha)
    # ln(P^M(0,T) / P^M(0,t))
    ln_ratio = np.log(disc_fn(T)) - np.log(disc_fn(t))
    correction = B * fwd_fn(np.atleast_1d(t)).squeeze() - (sigma**2 / (4 * alpha)) * B**2 * (1 - np.exp(-2 * alpha * t))
    return ln_ratio + correction

def hw_bond_price(r_t, t, T, alpha, sigma, disc_fn, fwd_fn):
    """P(t,T) under Hull-White given current short rate r_t."""
    B = B_hw(t, T, alpha)
    lnA = ln_A_hw(t, T, alpha, sigma, disc_fn, fwd_fn)
    return np.exp(lnA - B * r_t)


# ─── Monte Carlo simulation ───────────────────────────────────────────────────

def hw_simulate(r0, alpha, sigma, T, N_steps, N_paths, disc_fn, fwd_fn, dfwd_fn, seed=42):
    """
    Simulate Hull-White short rate paths using Euler discretisation.
    Returns array of shape (N_paths, N_steps+1).
    """
    rng = np.random.default_rng(seed)
    dt = T / N_steps
    t_grid = np.linspace(0, T, N_steps + 1)

    r = np.zeros((N_paths, N_steps + 1))
    r[:, 0] = r0

    for i in range(N_steps):
        t_i = t_grid[i]
        th = theta(t_i, alpha, sigma, fwd_fn, dfwd_fn)
        Z = rng.standard_normal(N_paths)
        r[:, i+1] = r[:, i] + (th - alpha * r[:, i]) * dt + sigma * np.sqrt(dt) * Z

    return r, t_grid


# ─── Verification: model bond prices match market ─────────────────────────────

alpha, sigma, r0 = 0.10, 0.01, 0.03

maturities = np.array([0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0])
market_prices = flat_discount(maturities)
model_prices  = hw_bond_price(r0, t=0.0, T=maturities, alpha=alpha, sigma=sigma,
                              disc_fn=flat_discount, fwd_fn=flat_forward)

print("Maturity | Market P(0,T) | Model P(0,T) | Error")
print("-" * 55)
for T, mp, mdp in zip(maturities, market_prices, model_prices):
    print(f"  {T:5.1f}  |   {mp:.6f}   |  {mdp:.6f}   | {abs(mp-mdp):.2e}")

# ─── Simulate paths and plot ──────────────────────────────────────────────────

r_paths, t_grid = hw_simulate(
    r0=r0, alpha=alpha, sigma=sigma,
    T=10.0, N_steps=500, N_paths=500,
    disc_fn=flat_discount, fwd_fn=flat_forward, dfwd_fn=flat_forward_deriv
)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for i in range(50):
    axes[0].plot(t_grid, r_paths[i] * 100, alpha=0.3, lw=0.7, color="steelblue")
axes[0].axhline(r0 * 100, color="black", lw=1.5, linestyle="--", label=f"r₀ = {r0*100:.0f}%")
axes[0].set_title("Hull-White: Short Rate Paths (10yr horizon)")
axes[0].set_xlabel("Time (years)")
axes[0].set_ylabel("Short Rate (%)")
axes[0].legend()

# Model vs market yield curve (implied from bond prices at t=0 for grid of r0)
yields_model  = -np.log(model_prices) / maturities
yields_market = -np.log(market_prices) / maturities
axes[1].plot(maturities, yields_market * 100, "k--", lw=2, label="Market (flat 3%)")
axes[1].plot(maturities, yields_model * 100, "b-o", markersize=5, label="Hull-White model")
axes[1].set_title("Hull-White: Yield Curve Fit")
axes[1].set_xlabel("Maturity (years)")
axes[1].set_ylabel("Yield (%)")
axes[1].legend()

plt.tight_layout()
plt.savefig("hw_paths_and_curve.png", dpi=150)
plt.show()

# ─── Bond repricing check via Monte Carlo discount factors ────────────────────

# Average discounted $1 across paths at T=5
T_target = 5.0
N_steps_mc = 250
r_mc, t_mc = hw_simulate(r0, alpha, sigma, T_target, N_steps_mc, 20_000,
                          flat_discount, flat_forward, flat_forward_deriv, seed=1)
dt_mc = T_target / N_steps_mc
disc_factors = np.exp(-r_mc[:, :-1].sum(axis=1) * dt_mc)
mc_bond = disc_factors.mean()
analytic_bond = hw_bond_price(r0, 0.0, T_target, alpha, sigma, flat_discount, flat_forward)
print(f"\nP(0,5) — MC: {mc_bond:.5f}  Analytic: {analytic_bond:.5f}  Market: {flat_discount(T_target):.5f}")
```

---

## Bridge to Quant / ML

- **CVA/XVA.** Hull-White is the standard short-rate model for CVA (Credit Valuation Adjustment) and XVA calculations at bank trading desks. The affine structure allows fast simulation of thousands of paths across hundreds of counterparties.
- **G2++ (two-factor Hull-White).** The extension to two correlated mean-reverting factors captures parallel shifts and slope changes independently — the standard for multi-curve (OIS vs. LIBOR) modelling. G2++ retains the same affine structure and analytic tractability.
- **HJM connection.** Hull-White is HJM with $\sigma(t,T) = \sigma e^{-\alpha(T-t)}$ — the simplest non-trivial HJM specification. Understanding this connection is the bridge from single-factor short-rate models to the full forward-rate curve dynamics used in LMM (LIBOR Market Model).
- **Bermudan swaption pricing.** The trinomial tree implementation is the canonical method for pricing callable bonds and Bermudan swaptions. The backward induction on the tree is conceptually identical to the dynamic programming approach used in RL for option pricing.
- **Neural SDE calibration.** Recent work on neural SDEs and deep rate models often uses Hull-White as the "baseline physics" — the backbone onto which neural corrections are grafted to improve vol surface fit while preserving exact curve fit.

---

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why is it critical that an interest rate model for derivatives pricing exactly reprices today's yield curve? What goes wrong if it doesn't?
<details>
<summary>Answer</summary>
Interest rate derivatives are priced relative to the yield curve — a swap's value is the present-value difference between fixed and floating cash flows, discounted using the curve. If the model assigns different discount factors than the market, every derivative price is immediately wrong. More critically, when you delta-hedge a derivative, you use bonds and swaps as hedging instruments. If your model says a 5-year bond is worth \$X but the market says \$Y, then your hedge ratios are computed incorrectly, and your supposedly hedged position is not actually hedged. In practice, traders reprice their books daily against the market curve, and any model that cannot reproduce it generates systematic P&L noise — phantom gains and losses that are purely artifacts of the model mismatch, not real risk. Exact curve fit is a minimum hygiene requirement for a production-grade rates model.
</details>

**Q2.** θ(t) in Hull-White is described as a "free function," not a free parameter. What is the difference, and how does this function get determined?
<details>
<summary>Answer</summary>
A free parameter is a scalar you choose (like α or σ in Hull-White). A free function is an entire curve — a value for every t ≥ 0 — that you specify. In Hull-White, θ(t) is uniquely determined by the no-arbitrage condition applied to today's market. Specifically, given the observed instantaneous forward rate curve f^M(0,t) (derived from market bond prices), the formula θ(t) = ∂f^M(0,t)/∂t + α·f^M(0,t) + σ²/(2α)·(1−e^{−2αt}) uniquely specifies θ at every time t. Once you choose α and σ (the only true free parameters, calibrated to swaption vols), θ(t) follows automatically. There is no additional calibration step — it is a mathematical consequence of requiring the model to reprice today's bonds. This is what makes θ(t) a function rather than a parameter.
</details>

**Q3.** Hull-White is described as a special case of the HJM framework. What does this mean, and why is this connection important?
<details>
<summary>Answer</summary>
The HJM framework (Heath-Jarrow-Morton, 1992) models the entire forward rate curve as a system of SDEs and derives the no-arbitrage condition: the drift of every forward rate is determined by its volatility. Any arbitrage-free interest rate model can be expressed within HJM by specifying the volatility function σ(t,T) for each forward rate f(t,T). Hull-White corresponds to the choice σ(t,T) = σ·e^{−α(T−t)} — an exponential decay in maturity. Plugging this into the HJM drift condition and integrating recovers exactly the Hull-White SDE for the short rate. This connection is important because: (1) it proves Hull-White is internally arbitrage-free by construction (any HJM model with well-behaved vol is arbitrage-free); (2) it shows how to extend Hull-White by using more complex σ(t,T) specifications (the full LMM/BGM framework); (3) it reveals that Hull-White's exponential vol structure is what makes it Markovian — more general HJM vol specs produce non-Markovian path-dependent models requiring full Monte Carlo.
</details>

---

### Level 2 — Quantitative

**Q4.** Given a flat yield curve at r = 3% (so P^M(0,T) = e^{−0.03T} and f^M(0,T) = 0.03), compute θ(t) for the Hull-White model with α = 0.10 and σ = 0.01. What is θ(5)?
<details>
<summary>Answer</summary>
The formula is: θ(t) = ∂f^M(0,t)/∂t + α·f^M(0,t) + (σ²/2α)·(1−e^{−2αt})

For a flat curve, f^M(0,t) = 0.03 (constant), so ∂f^M(0,t)/∂t = 0.

θ(t) = 0 + 0.10 × 0.03 + (0.0001/0.20)·(1−e^{−0.2t})
      = 0.003 + 0.0005·(1−e^{−0.2t})

At t = 5:
θ(5) = 0.003 + 0.0005·(1 − e^{−1.0})
      = 0.003 + 0.0005·(1 − 0.3679)
      = 0.003 + 0.0005 × 0.6321
      = 0.003 + 0.000316
      = **0.003316** (0.33%)

Interpretation: For a flat curve, θ(t) ≈ α × b = 0.10 × 0.03 = 0.003, plus a small convexity correction from the σ²/(2α) term that grows with t and saturates. The function is essentially constant because the flat curve has no slope or curvature to absorb.
</details>

**Q5.** Compute the Hull-White bond price P(0, T=5) and verify it matches the market price e^{−0.03×5} = 0.8607. Use: r₀ = 0.03, α = 0.10, σ = 0.01, flat curve (P^M(0,T) = e^{−0.03T}).
<details>
<summary>Answer</summary>
The Hull-White affine formula: P(0,5) = A(0,5) × exp(−B(0,5) × r₀)

**B(0,5):**
B = (1 − e^{−α×5}) / α = (1 − e^{−0.5}) / 0.10 = (1 − 0.6065) / 0.10 = 0.3935/0.10 = **3.935**

**ln A(0,5):**
ln A = ln(P^M(0,5)/P^M(0,0)) + B×f^M(0,0) − (σ²/4α)×B²×(1−e^{−2α×0})

P^M(0,0) = 1 (value of \$1 today is \$1), so ln(P^M(0,5)/1) = −0.03×5 = −0.15

The third term: at t=0, (1−e^{−2α×0}) = 0, so the correction vanishes.

ln A = −0.15 + 3.935×0.03 − 0 = −0.15 + 0.11805 = **−0.03195**

**Bond price:**
P(0,5) = exp(−0.03195 − 3.935×0.03)
       = exp(−0.03195 − 0.11805)
       = exp(−0.15)
       = **0.8607**

This matches the market price e^{−0.03×5} = 0.8607 exactly — confirming by-construction exact curve fit.
</details>

---

### Level 3 — Coding

**Q6.** The `theta` function in the implementation takes `fwd_fn` and `dfwd_fn` as arguments rather than computing the forward rate and its derivative internally. Why is this design choice important for production use with a real (non-flat) yield curve?
<details>
<summary>Answer</summary>
For a real market yield curve, the instantaneous forward rate f^M(0,t) must be computed by differentiating the discount curve: f^M(0,t) = −∂ ln P^M(0,t)/∂t. The derivative ∂f^M(0,t)/∂t (needed for θ(t)) is the second derivative of the log discount curve. In practice, the market discount curve is given as a finite set of quotes at specific tenors (3M, 6M, 1Y, 2Y, 5Y, 10Y, 30Y), requiring interpolation before differentiation. The choice of interpolation method (linear rates, log-linear discounts, cubic spline) significantly affects the smoothness and accuracy of ∂f/∂t. By passing `fwd_fn` and `dfwd_fn` as function arguments, the theta computation is decoupled from the curve construction — the user can plug in any interpolation they want (cubic spline, Nelson-Siegel, bootstrapped discount factors) without changing the Hull-White code. In the flat curve example, this is trivial (constant forward rate, zero derivative), but in production with a real curve the distinction is critical: numerical differentiation of a poorly interpolated curve produces noisy θ(t) that causes simulation instability.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| θ(t) is an extra parameter that adds flexibility | θ(t) is uniquely determined by the market forward curve — it is not calibrated freely. Once α and σ are set, θ(t) is computed analytically. The model has exactly two genuine scalar parameters (α, σ). |
| Hull-White is a different model from Vasicek | Hull-White is "extended Vasicek" — exactly the same structure with θ(t) replacing the constant b. All Vasicek analytics (affine bond prices, simulation, bond option formulas) carry over with minor modifications. |
| Perfect curve fit means perfect hedging | Exact curve fit means the model correctly reprices vanilla bonds today. It does not mean the model correctly describes how the curve will move tomorrow (it is still a one-factor model with Gaussian rates). Hedging errors arise from incorrect dynamics, not from incorrect static pricing. |
| Hull-White cannot price derivatives because rates can go negative | Negative rates are a known feature of Gaussian models. For the EUR/JPY rate environment post-2015, this was actually realistic. Practitioners using Hull-White in negative-rate environments typically use it knowing rates can be negative and design products accordingly, or use a "shifted" version. |

## Related Concepts

- [[Vasicek Model]]
- [[HJM Framework]]
- [[Bond Basics]]
- [[Yield Curve]]
- [[Interest Rate Swaps]]
- [[SABR Model]]

---

## Sources Used

- Hull, J. & White, A. (1990). "Pricing Interest Rate Derivative Securities." *Review of Financial Studies* 3(4), 573–592.
- Brigo, D. & Mercurio, F. (2006). *Interest Rate Models — Theory and Practice*. Springer Finance. Ch. 3.

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | initial build |
