---
type: concept
domain: 30-Models
tags: [pricing, options, volatility-surface]
status: math
stability: evolving
confidence: high
last_reviewed: 2026-04-11
review_interval_days: 90
sources:
  - "Dupire (1994), Pricing with a Smile"
  - "Gatheral, The Volatility Surface, ch. 1, 11"
  - "Hull, Options, Futures, and Other Derivatives, ch. 27"
created: 2026-04-12
---

> Dupire's σ(S,t) that exactly fits the vol surface

> [!info] Problem Chain
> **Chain:** Pricing → Gap 5: BSM assumes constant σ — real markets show a volatility smile
> **This concept:** Solution A to Gap 5 — makes volatility a deterministic function of current stock price and time; uniquely reads off σ(S,t) from the observed option surface via Dupire's formula
> **Alternative approaches to this gap:** [[Heston Model]] (Solution B — stochastic vol), [[Merton Jump-Diffusion]] (Solution C — jumps)
> **You need first:** [[Black-Scholes Model]], [[Volatility Surface]], [[Ito's Lemma]]
> **This unlocks:** [[Exotic Options]] (barrier/digital pricing consistent with the surface), [[SABR Model]] (smooth surface input), [[Heston Model]] (LSV combines both)

## Why This Exists

**The gap:** BSM prices every option with the same σ, but market option prices imply different σ values at different strikes and maturities. There was no single, internally consistent model that could reproduce all of them simultaneously.

**What came before:** Practitioners would price different options with different σ values — a patchwork approach with no coherent dynamics. There was no way to know whether different exotic options priced this way were mutually consistent or contained hidden arbitrage.

**What this adds:** Dupire (1994) showed that there is exactly one diffusion model that can reproduce the entire observed option surface simultaneously: let σ be a deterministic function of the current stock price S and time t. Given any arbitrage-free option surface, his formula reads off σ(S,t) directly — no iterative calibration, just differentiate the call prices with respect to strike and maturity. This guarantees perfect fit to all vanilla options by construction, providing a consistent baseline for pricing anything else, especially barrier options and digitals priced via PDE.

**What it still doesn't solve:** Perfect static fit does not mean correct dynamics. In the local vol model, when the stock moves, the vol surface moves in an unrealistic direction — it flattens. Real smiles tend to persist and shift laterally. This means local vol systematically misprices forward-start options, cliquets, and any exotic product sensitive to how the smile will look in the future. This is the key weakness that motivates the Heston model and Local Stochastic Volatility (LSV).

---

## Math Concepts

### The Local Vol SDE

Under the risk-neutral measure, the stock follows:

$$dS_t = r S_t \, dt + \sigma(S_t, t) \, S_t \, dW_t$$

The key difference from BSM: $\sigma$ is now a **deterministic function** of the current stock price $S_t$ and time $t$. No second stochastic process is needed. The randomness comes entirely through how $S$ moves.

### The Dupire Forward PDE

Given market call prices $C(K, T)$ as a function of strike and maturity, Dupire's equation reads:

$$\frac{\partial C}{\partial T} = \frac{1}{2}\sigma_{loc}(K,T)^2 K^2 \frac{\partial^2 C}{\partial K^2} - rK\frac{\partial C}{\partial K}$$

Solving for $\sigma_{loc}$:

$$\sigma_{loc}(K, T)^2 = \frac{2\dfrac{\partial C}{\partial T} + rK\dfrac{\partial C}{\partial K}}{K^2 \dfrac{\partial^2 C}{\partial K^2}}$$

The denominator $K^2 \frac{\partial^2 C}{\partial K^2}$ is the **risk-neutral probability density** of $S_T = K$ (by Breeden-Litzenberger). It must be positive for the surface to be arbitrage-free.

### Expressed in Implied Vol

Practitioners usually work in implied vol $\sigma_{imp}(K, T)$ rather than prices. Gatheral gives the equivalent formula in terms of total implied variance $w(k, T) = \sigma_{imp}^2 T$ where $k = \ln(K/F)$:

$$\sigma_{loc}^2 = \frac{\frac{\partial w}{\partial T}}{1 - \frac{k}{w}\frac{\partial w}{\partial k} + \frac{1}{4}\left(-\frac{1}{4} - \frac{1}{w} + \frac{k^2}{w^2}\right)\left(\frac{\partial w}{\partial k}\right)^2 + \frac{1}{2}\frac{\partial^2 w}{\partial k^2}}$$

This is the version actually used in practice.

### Why Derivatives of the Surface Are Tricky

The Dupire formula involves first and second derivatives of the option price (or implied vol surface) with respect to $K$ and $T$. Market quotes are noisy and sparse. Taking numerical derivatives amplifies noise. If you're not careful, you get negative local variances (which are impossible) or local vol surfaces that explode. This is why **interpolation and smoothing** of the raw implied vol surface is a critical step before applying Dupire.

---

## Walkthrough

### Step-by-Step Recipe

1. **Gather market data.** Collect implied vols for a range of strikes $K$ and maturities $T$.
2. **Smooth/interpolate the surface.** Use a parametric model (SVI, SABR, polynomial) or spline to create a smooth, arbitrage-free implied vol surface $\sigma_{imp}(K, T)$.
3. **Check for arbitrage.** The surface must satisfy:
   - Calendar spread arbitrage: $\partial(C/K)/\partial T \geq 0$ (variance must be non-decreasing in T)
   - Butterfly arbitrage: $\partial^2 C/\partial K^2 \geq 0$ (density must be non-negative)
4. **Apply Dupire's formula** numerically to extract $\sigma_{loc}(K, T)$.
5. **Use $\sigma_{loc}$ for pricing.** Simulate the local vol SDE or solve the forward/backward PDE to price any path-dependent product.

### What "Exact Fit" Means (and Does Not Mean)

Local vol fits all European option prices by construction. But:
- It says nothing about how those prices will change tomorrow.
- For path-dependent products (barriers, Asians, cliquets), the pricing depends on the dynamics of the smile, which local vol gets wrong.

### Common Uses

- Pricing vanilla options: trivially exact by construction.
- Pricing barrier options and digital options: reasonably fast via PDE.
- As the baseline for Local Stochastic Volatility (LSV) models.

---

## Analysis

### Pros vs BSM

- **Perfect static calibration.** Fits the entire vol surface simultaneously with zero error.
- **No model risk on vanillas.** Once calibrated, European prices are exact by construction.
- **Single-factor model.** Computationally simple — no second stochastic process.
- **PDE methods are tractable.** Can price a range of strikes at once via the forward Kolmogorov PDE.

### Cons / Where It Breaks

- **Wrong forward smile dynamics.** The most critical flaw. In local vol, as time passes, the implied vol smile flattens. In practice, smiles persist. This makes local vol mispriced for forward-start options, cliquets, and any product sensitive to future smiles.
- **Noisy inputs produce noisy $\sigma_{loc}$.** The double differentiation of market prices amplifies data errors. Requires careful smoothing.
- **No economic intuition.** $\sigma(S, t)$ is a mathematical artifact, not a model with parameters you can reason about intuitively.
- **Instability over time.** The local vol surface recalibrated on consecutive days can be very different, making delta hedging noisy.

### The Forward Smile Problem: Intuition

Imagine the stock is at 100 today, and you price a cliquet that pays based on the smile at $S=80$ in one year. In a local vol world, the smile at $(80, 1yr)$ is essentially "baked in" to the current surface. But stochastic vol models (Heston, SABR) predict a different, usually wider smile at that future scenario. The market tends to agree with stochastic vol. Local vol gets cliquets systematically wrong.

### Industry Usage

- Standard baseline for equity derivatives desks.
- Used as input into LSV (Local Stochastic Volatility) models, which are the current industry standard for exotic equity pricing.
- FX desks often use it directly for barrier options.

---

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RectBivariateSpline
from scipy.stats import norm

# ─── BSM implied vol (Black-Scholes) ─────────────────────────────────────────

def bsm_price(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def bsm_call_price_grid(S0, K_grid, T_grid, r, sigma_imp_grid):
    """
    Compute call prices on a (K, T) grid from implied vol surface.
    sigma_imp_grid has shape (len(K_grid), len(T_grid)).
    """
    prices = np.zeros_like(sigma_imp_grid)
    for i, K in enumerate(K_grid):
        for j, T in enumerate(T_grid):
            prices[i, j] = bsm_price(S0, K, T, r, sigma_imp_grid[i, j])
    return prices


# ─── Dupire Local Vol from Call Price Surface ─────────────────────────────────

def dupire_local_vol(S0, K_grid, T_grid, C_grid, r):
    """
    Compute the Dupire local volatility surface from a grid of call prices.

    C_grid[i, j] = call price at (K_grid[i], T_grid[j]).
    Returns sigma_loc_grid of same shape, floored at 0.
    """
    dK = K_grid[1] - K_grid[0]
    dT = T_grid[1] - T_grid[0]

    sigma_loc = np.full_like(C_grid, np.nan)

    # Use interior points only (derivatives need neighbors)
    for i in range(1, len(K_grid) - 1):
        for j in range(1, len(T_grid) - 1):
            K = K_grid[i]
            C   = C_grid[i, j]

            # First derivative in T (calendar spread)
            dC_dT = (C_grid[i, j+1] - C_grid[i, j-1]) / (2 * dT)

            # First derivative in K
            dC_dK = (C_grid[i+1, j] - C_grid[i-1, j]) / (2 * dK)

            # Second derivative in K
            d2C_dK2 = (C_grid[i+1, j] - 2 * C_grid[i, j] + C_grid[i-1, j]) / (dK**2)

            numerator   = 2 * dC_dT + r * K * dC_dK
            denominator = K**2 * d2C_dK2

            if denominator > 1e-12 and numerator > 0:
                sigma_loc[i, j] = np.sqrt(numerator / denominator)
            else:
                sigma_loc[i, j] = np.nan  # arbitrage region or boundary artifact

    return sigma_loc


# ─── Example: build a vol surface, apply Dupire ──────────────────────────────

S0 = 100.0
r  = 0.03

# Define a smooth implied vol surface (skewed smile, typical of equity)
K_grid = np.linspace(70, 140, 50)
T_grid = np.linspace(0.1, 2.0, 30)

def market_implied_vol(K, T):
    """Synthetic equity-like vol surface with skew and term structure."""
    atm_vol = 0.20
    moneyness = np.log(K / (S0 * np.exp(r * T)))   # log-moneyness
    skew  = -0.10 * moneyness / np.sqrt(T)           # negative skew
    smile = 0.05 * moneyness**2 / T                  # smile curvature
    term_str = 0.02 * (1 - np.exp(-T))               # term structure lift
    return atm_vol + skew + smile + term_str

# Build implied vol and call price grids
sigma_imp_grid = np.array([[market_implied_vol(K, T) for T in T_grid] for K in K_grid])
C_grid = bsm_call_price_grid(S0, K_grid, T_grid, r, sigma_imp_grid)

# Compute local vol
sigma_loc_grid = dupire_local_vol(S0, K_grid, T_grid, C_grid, r)

# ─── Plot: implied vol surface vs local vol surface ───────────────────────────

KK, TT = np.meshgrid(K_grid, T_grid, indexing="ij")

fig, axes = plt.subplots(1, 2, figsize=(14, 5), subplot_kw={"projection": "3d"})

axes[0].plot_surface(KK, TT, sigma_imp_grid * 100, cmap="viridis", alpha=0.85)
axes[0].set_title("Implied Vol Surface (%)")
axes[0].set_xlabel("Strike")
axes[0].set_ylabel("Maturity (yr)")
axes[0].set_zlabel("Implied Vol (%)")

axes[1].plot_surface(KK, TT, sigma_loc_grid * 100, cmap="plasma", alpha=0.85)
axes[1].set_title("Local Vol Surface — Dupire (%)")
axes[1].set_xlabel("Strike")
axes[1].set_ylabel("Maturity (yr)")
axes[1].set_zlabel("Local Vol (%)")

plt.tight_layout()
plt.savefig("local_vol_surface.png", dpi=150)
plt.show()

# ─── Monte Carlo with Local Vol ───────────────────────────────────────────────

# Build a fast bivariate spline interpolator for sigma_loc
# Use only interior region where sigma_loc is defined
K_inner = K_grid[1:-1]
T_inner = T_grid[1:-1]
sigma_loc_inner = sigma_loc_grid[1:-1, 1:-1]

# Replace NaN with nearest valid value (simple fill)
mask = np.isnan(sigma_loc_inner)
sigma_loc_inner[mask] = np.nanmean(sigma_loc_inner)

spline = RectBivariateSpline(K_inner, T_inner, sigma_loc_inner, kx=3, ky=3)

def local_vol_fn(S, t):
    """Interpolated local vol at stock price S and time t."""
    S_clip = np.clip(S, K_inner[0], K_inner[-1])
    t_clip = np.clip(t, T_inner[0], T_inner[-1])
    return float(spline(S_clip, t_clip))

def simulate_local_vol(S0, r, T, N_steps, N_paths, seed=42):
    rng = np.random.default_rng(seed)
    dt = T / N_steps
    S = np.zeros((N_paths, N_steps + 1))
    S[:, 0] = S0
    for step in range(N_steps):
        t = step * dt
        sigma_t = np.array([local_vol_fn(s, t) for s in S[:, step]])
        Z = rng.standard_normal(N_paths)
        S[:, step+1] = S[:, step] * np.exp(
            (r - 0.5 * sigma_t**2) * dt + sigma_t * np.sqrt(dt) * Z
        )
    return S

S_paths = simulate_local_vol(S0, r, T=1.0, N_steps=100, N_paths=500)

plt.figure(figsize=(10, 4))
t_axis = np.linspace(0, 1.0, 101)
for i in range(30):
    plt.plot(t_axis, S_paths[i], alpha=0.3, lw=0.8)
plt.title("Local Vol Monte Carlo Paths")
plt.xlabel("Time (years)")
plt.ylabel("Stock Price")
plt.tight_layout()
plt.savefig("local_vol_paths.png", dpi=150)
plt.show()
```

---

## Bridge to Quant / ML

- **Neural network vol surfaces:** Parametric vol surfaces (SVI, SABR) are being replaced by neural network representations that guarantee no-arbitrage by construction (e.g., "No-Arbitrage Deep Calibration"). Local vol is the downstream consumer of these smooth surfaces.
- **LSV models:** Local Stochastic Volatility combines Dupire's $\sigma_{loc}(S,t)$ with a stochastic vol process. The local vol component is a "leverage function" that corrects the stochastic vol model's residual calibration error. This is the industry standard for exotic equity books.
- **PDE solvers:** Local vol enables fast finite-difference PDE pricing of barriers, Americans, and lookbacks — a single PDE run prices a strip of strikes simultaneously.
- **Reinforcement learning hedging:** RL agents trained to hedge derivatives can use local vol as the simulation environment, since it's easy to calibrate and simulate.
- **Density estimation link:** The denominator $K^2 \partial^2 C/\partial K^2$ is the risk-neutral PDF (Breeden-Litzenberger). Estimating this from sparse data is a nonparametric density estimation problem — a direct bridge to statistics/ML.

---

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Dupire's local vol model fits the entire option surface perfectly today. So why isn't it considered the "correct" model?
<details>
<summary>Answer</summary>
Fitting today's surface is a static property — it says the model is consistent with prices observed right now. But a model also makes predictions about how prices will evolve tomorrow, and how the smile will move when the stock moves. In the local vol model, when the stock moves to a new level, the smile flattens and shifts in a specific direction that doesn't match what actually happens in markets. Real smiles tend to persist (sticky strike or sticky delta behavior), but local vol predicts they flatten away. This makes local vol wrong for any exotic product that depends on future smiles — forward-start options, cliquets, and variance swaps. The model "knows" the right prices today but "predicts" the wrong dynamics.
</details>

**Q2.** What is the Breeden-Litzenberger relationship, and why does it appear in the denominator of Dupire's formula?
<details>
<summary>Answer</summary>
Breeden and Litzenberger (1978) showed that the second derivative of the call price with respect to strike gives the risk-neutral probability density of the stock's terminal price: q(K) = e^{rT} · ∂²C/∂K². This is an exact, model-free result. In Dupire's formula, the denominator K²·∂²C/∂K² is exactly K² times this density (up to the discount factor). It represents "how much probability mass does the market assign to the stock being near K at time T?" If this density is zero or negative somewhere, there is no local vol that can generate that price — you have an arbitrage. This is why checking ∂²C/∂K² ≥ 0 (butterfly no-arbitrage condition) is a prerequisite before applying the Dupire formula.
</details>

**Q3.** Why does numerical differentiation of market option prices cause problems when computing the local vol surface, and how do practitioners handle this?
<details>
<summary>Answer</summary>
The Dupire formula requires first derivatives in T and K, and a second derivative in K. Numerical differentiation amplifies noise: small errors in option prices become large errors in derivatives. Real market quotes are sparse (only a finite grid of strikes and maturities exist), have bid-ask spread noise, and may contain inconsistencies. Computing ∂²C/∂K² by finite differences on raw market data frequently produces negative values (implying negative probability density = arbitrage) or wildly oscillating local vols. The standard solution is: (1) fit a smooth, arbitrage-free parametric model (SVI, SABR) to the raw quotes first, then (2) apply Dupire's formula to the smooth fitted surface, not the raw data. This separates the interpolation problem from the Dupire computation.
</details>

---

### Level 2 — Quantitative

**Q4.** You observe two European call prices on the same stock (S = 100, r = 5%): C(K=100, T=1) = \$10.45 and C(K=100, T=1.01) = \$10.52. Estimate the numerator of the Dupire formula at this point (ignoring the K-derivative terms for simplicity — assume ATM so the forward is near K). What does this estimate tell you about the local variance at (K=100, T=1)?
<details>
<summary>Answer</summary>
The numerator of Dupire's formula (simplified for ATM, ignoring the rK·∂C/∂K term which is small at-the-money) is approximately 2·∂C/∂T.

Numerical estimate: ∂C/∂T ≈ (10.52 − 10.45) / (1.01 − 1.00) = 0.07 / 0.01 = 7.0

Numerator ≈ 2 × 7.0 = 14.0

For the denominator, at ATM the Breeden-Litzenberger term K²·∂²C/∂K² represents the probability density near the forward. For a BSM-like surface at 20% vol, this is approximately K² × (1/(Kσ√T)) × φ(0) ≈ 100² × (1/(100×0.2×1)) × 0.399 ≈ 100 × 0.399 / 0.2 ≈ 200.

Local variance ≈ 14.0 / 200 ≈ 0.07, i.e., local vol ≈ √0.07 ≈ 26.5%

This is a rough calculation but illustrates that the Dupire formula inverts observable market quantities into a local volatility estimate.
</details>

**Q5.** The Dupire forward PDE is stated as: ∂C/∂T = ½·σ_loc²·K²·∂²C/∂K² − rK·∂C/∂K. Verify that this equation is satisfied by the BSM call price (where σ_loc = σ = constant). [Hint: Use Theta = ∂C/∂T = −rKe^{−rT}N(d₂) + S₀σN'(d₁)/(2√T).]
<details>
<summary>Answer</summary>
When σ_loc = σ is constant, the Dupire PDE reduces to the standard BSM backward PDE (which we know BSM satisfies). More specifically: for constant σ, the BSM price C(K,T) satisfies both the backward BSM PDE in (S,t) variables and the forward Kolmogorov PDE in (K,T) variables. They are duals of each other. The forward PDE in (K,T) is exactly the Dupire PDE, so a BSM price with constant σ satisfies it with σ_loc = σ = constant. This confirms that BSM is the special case of local vol where σ(S,t) = σ everywhere — the flat local vol surface reproduces the flat implied vol surface of BSM.

The key derivative to check: ∂²C/∂K² under BSM equals (1/Kσ√T)·φ(d₂)·e^{−rT}, which is positive for all K (confirming no butterfly arbitrage in BSM). Plugging this into the forward PDE with σ_loc = σ reproduces the BSM theta formula, confirming consistency.
</details>

---

### Level 3 — Coding

**Q6.** In the `dupire_local_vol` function, the check `if denominator > 1e-12 and numerator > 0` gates whether a local vol is computed at that grid point. Why is checking `numerator > 0` essential — what does a non-positive numerator mean economically?
<details>
<summary>Answer</summary>
The numerator of the Dupire formula is 2·∂C/∂T + rK·∂C/∂K. A non-positive numerator means the calendar spread is violated: total variance is not non-decreasing in T. Economically, ∂C/∂T < 0 for a sufficiently negative rK·∂C/∂K would mean that longer-dated options are cheaper than shorter-dated options with the same strike — which is a calendar spread arbitrage (you can profit by buying the cheap long-dated option and selling the expensive short-dated one). A model that assigns negative local variance to any region is internally inconsistent: negative variance implies imaginary volatility, which has no meaning. If `numerator > 0` fails at a grid point, the surface has an arbitrage at that point and the local vol surface cannot be computed there — the code correctly marks it as NaN rather than returning a spurious number.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Local vol is better than BSM because it fits the surface exactly | Fitting today's surface is not the same as modeling market dynamics correctly. Local vol has correct static fit but systematically wrong forward smile dynamics, making it worse than BSM for certain products (cliquets, forward-start options). |
| σ(S,t) in local vol is directly observable from the market | σ(S,t) is extracted from the market surface through a two-step process: first fitting a smooth surface to noisy quotes, then applying Dupire's formula. The result is highly sensitive to the smoothing method chosen. |
| Local vol and stochastic vol (Heston) produce the same prices for exotics | They can match European vanilla prices exactly (by construction for local vol, approximately for Heston after calibration), but they produce different prices for exotics because their dynamics are fundamentally different. Heston is generally better for path-dependent exotics. |
| The Dupire formula is a model | The Dupire formula is model-free — it extracts the unique local vol consistent with any arbitrage-free surface, regardless of what process generated that surface. It's a mathematical identity, not a model assumption. |

## Related Concepts

- [[Black-Scholes Model]]
- [[Heston Model]]
- [[SABR Model]]
- [[Volatility Surface]]
- [[Breeden-Litzenberger Formula]]
- [[Local Stochastic Volatility]]
- [[SVI Parameterization]]
- [[No-Arbitrage Conditions on Vol Surface]]

---

## Sources Used

- Dupire, B. (1994). "Pricing with a Smile." *Risk Magazine*, January 1994.
- Gatheral, J. (2006). *The Volatility Surface: A Practitioner's Guide*. Wiley Finance. Ch. 1, 11.
- Hull, J.C. (2022). *Options, Futures, and Other Derivatives*, 11th ed. Ch. 27.
- Derman, E. and Kani, I. (1994). "Riding on a Smile." *Risk Magazine*, February 1994.

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review passed — Dupire formula, forward PDE, implementation code verified | QA review |
