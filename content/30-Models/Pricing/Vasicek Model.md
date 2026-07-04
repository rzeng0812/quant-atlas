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
  - "Vasicek (1977), An Equilibrium Characterization of the Term Structure"
  - "Hull, Options, Futures, and Other Derivatives, ch. 31-32"
  - "Brigo & Mercurio, Interest Rate Models, ch. 3"
created: 2026-04-12
---

> Mean-reverting short rate: dr = a(b-r)dt + σdW

> [!info] Problem Chain
> **Chain:** Pricing → Gap 5 extension: Interest rate analog of Gap 5 — equity GBM extended to mean-reverting rates
> **This concept:** The first rigorous equilibrium model of the full yield curve; derives bond prices at all maturities from a single mean-reverting short-rate SDE
> **Alternative approaches to this gap:** [[CIR Model]] (non-negative rates via √r diffusion), [[Hull-White Model]] (Vasicek extended to fit today's yield curve exactly)
> **You need first:** [[Black-Scholes Model]], [[Geometric Brownian Motion]], [[Ito's Lemma]], [[Ornstein-Uhlenbeck Process]]
> **This unlocks:** [[Hull-White Model]], [[HJM Framework]], [[Bond Basics]], [[Yield Curve]]

## Why This Exists

**The gap:** Before Vasicek (1977), there was no principled model linking today's short-term interest rate to bond prices at all maturities. The yield curve was treated as empirically given — you read it from market prices and extrapolated, but there was no dynamic model specifying how rates evolve and whether bond prices at different maturities were mutually consistent.

**What came before:** The prevailing approach was to treat the yield curve descriptively — fit a polynomial or exponential to observed yields and use it for interpolation. This gave no insight into how the curve moves over time, provided no framework for pricing interest rate derivatives, and could not detect whether the prices of bonds at different maturities were arbitrage-free relative to each other.

**What this adds:** Vasicek modeled the short-term interest rate as an Ornstein-Uhlenbeck process — continuously drifting toward a long-run mean while receiving random shocks. From this single SDE, no-arbitrage conditions uniquely determine the price of every zero-coupon bond at every maturity. The result is an analytic closed-form formula for the entire yield curve. Bond prices are exponential-affine functions of the short rate, giving a clean, tractable model with only four parameters. This was the first demonstration that the entire yield curve can be derived from a single factor.

**What it still doesn't solve:** Vasicek allows negative interest rates (the Gaussian distribution has support on all reals), and with just four constant parameters it cannot exactly fit any arbitrary observed yield curve. The calibrated Vasicek yield curve approximates the market curve but always has fitting error at some maturities. Hull-White fixes this by making the drift time-varying.

---

## Math Concepts

### The SDE

Under the risk-neutral measure:

$$dr_t = a(b - r_t) \, dt + \sigma \, dW_t$$

This is an **Ornstein-Uhlenbeck (OU) process** applied to interest rates.

### Parameters

| Symbol | Name | Plain English |
|--------|------|---------------|
| $a$ | speed of mean reversion | how fast the rate snaps back; higher = faster reversion; half-life $\approx \ln 2 / a$ |
| $b$ | long-run mean rate | the equilibrium level the rate drifts toward (e.g., 5% in normal times) |
| $\sigma$ | volatility | how much the rate fluctuates around its mean |
| $r_0$ | initial short rate | today's instantaneous rate |

### Exact Solution

Because the SDE is linear (the OU process), it has an exact solution:

$$r_t = r_0 e^{-at} + b(1 - e^{-at}) + \sigma \int_0^t e^{-a(t-s)} dW_s$$

This means $r_t$ is **normally distributed** given $r_0$:

$$r_t \sim \mathcal{N}\!\left(r_0 e^{-at} + b(1-e^{-at}),\ \frac{\sigma^2}{2a}(1-e^{-2at})\right)$$

As $t \to \infty$, the distribution converges to $\mathcal{N}(b,\ \sigma^2/(2a))$ — the stationary distribution.

### Bond Pricing: Closed Form

The price at time $t$ of a zero-coupon bond maturing at $T$ (paying 1) is:

$$P(t, T) = A(t,T) \cdot e^{-B(t,T) \cdot r_t}$$

where $\tau = T - t$ and:

$$B(\tau) = \frac{1 - e^{-a\tau}}{a}$$

$$\ln A(\tau) = \left(b - \frac{\sigma^2}{2a^2}\right)(B(\tau) - \tau) - \frac{\sigma^2}{4a} B(\tau)^2$$

The corresponding continuously-compounded yield for maturity $\tau$ is:

$$R(t, T) = -\frac{\ln P(t,T)}{\tau} = \frac{B(\tau)}{T-t} r_t - \frac{\ln A(\tau)}{T-t}$$

This is linear in $r_t$ — yields at all maturities are affine functions of the short rate. Vasicek is an **affine term structure model**.

### Yield Curve Shapes

Depending on parameters and the current short rate, the Vasicek model can produce:
- **Normal (upward sloping):** $r_0 < b$ — rates expected to rise
- **Inverted (downward sloping):** $r_0 > b$ — rates expected to fall
- **Humped:** possible for intermediate parameter values

---

## Walkthrough

### Typical Parameter Values (historical calibration)

| Parameter | Example Value | Notes |
|-----------|--------------|-------|
| $a$ | 0.15–0.50 | half-life of ~1.5–4.5 years |
| $b$ | 0.04–0.08 | long-run rate = 4–8% |
| $\sigma$ | 0.01–0.03 | 1–3% annualized vol on the rate level |
| $r_0$ | current short rate | observed or derived from 3-month T-bill |

### Calibration Sketch

**Time-series approach:** Fit OU parameters to historical short-rate data using MLE or method of moments (use the exact conditional distribution).

**Cross-sectional (yield curve fitting):** Given today's yield curve $\{R^{mkt}(\tau_i)\}$, choose $(a, b, \sigma, r_0)$ to minimize the sum of squared yield errors. Note: Vasicek has only 4 parameters and cannot perfectly fit an arbitrary yield curve. For perfect fit, use **Hull-White** (time-varying $b(t)$).

### Using the Model

Once calibrated:
- Price any zero-coupon bond: use the $A, B$ formula.
- Price a coupon bond: sum of zero-coupon bond prices.
- Price a European bond option: Jamshidian (1989) decomposes it into a sum of zero-coupon bond options, each priced analytically.
- Simulate rate paths for Monte Carlo pricing of path-dependent products.

---

## Analysis

### Pros vs BSM / Other Rates Models

- **Closed-form bond prices.** No numerical methods needed for the core product (discount bonds).
- **Mean reversion is economically motivated.** Rates don't just diffuse away from today's level.
- **Tractable distribution.** Normal distribution makes analytics easy.
- **First rigorous equilibrium term structure model** — historically foundational.

### Cons / Where It Breaks

- **Negative rates.** Normal distribution has support on all of $\mathbb{R}$. For typical parameters, there's a positive probability of negative rates. This was the main criticism pre-2015; post-2015 Europe/Japan it became less embarrassing.
- **Cannot fit the initial yield curve exactly.** Vasicek with 3–4 parameters cannot match the entire observed yield curve. Hull-White (1990) adds a deterministic shift $\theta(t)$ to fix this.
- **Single-factor model.** The entire yield curve moves in lockstep driven by one Brownian motion. Real yield curves show independent movements at short and long ends (level, slope, curvature factors). Multi-factor extensions (CIR++, G2++) address this.
- **Constant volatility.** Rates have time-varying and strike-dependent vol; the SABR model handles this for rate options.

### Extensions and Successors

| Model | What It Adds |
|-------|-------------|
| CIR (Cox, Ingersoll, Ross 1985) | $\sqrt{r}$ diffusion keeps rates non-negative |
| Hull-White (1990) | Time-varying $\theta(t)$ for exact yield curve fit |
| G2++ / 2-factor Vasicek | Two correlated OU processes for better curve dynamics |
| LIBOR Market Model | Models rates at discrete tenors; better for swaptions |

### Industry Usage

Vasicek itself is rarely used directly in production today. But it is:
- The conceptual foundation that every rates quant learns first.
- The backbone of Hull-White (still widely used for callable bond pricing and CVA).
- A useful simulation environment for testing rates strategies.

---

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# ─── Vasicek Simulation ───────────────────────────────────────────────────────

def vasicek_simulate(r0, a, b, sigma, T, N_steps, N_paths, seed=42):
    """
    Simulate short rate paths under the Vasicek model (exact transition).

    At each step, use the exact conditional distribution:
      r(t+dt) | r(t) ~ N(mu, s^2)
      mu = r(t)*exp(-a*dt) + b*(1 - exp(-a*dt))
      s^2 = (sigma^2 / (2a)) * (1 - exp(-2a*dt))

    Parameters
    ----------
    r0      : initial short rate (e.g. 0.03)
    a       : mean-reversion speed
    b       : long-run mean rate
    sigma   : volatility
    T       : time horizon (years)
    N_steps : number of time steps
    N_paths : number of simulated paths
    """
    rng = np.random.default_rng(seed)
    dt = T / N_steps

    exp_adt = np.exp(-a * dt)
    cond_mean_coeff = exp_adt                           # coefficient on r(t)
    cond_mean_const = b * (1 - exp_adt)                 # constant term
    cond_var = (sigma**2 / (2 * a)) * (1 - np.exp(-2 * a * dt))
    cond_std = np.sqrt(cond_var)

    r = np.zeros((N_paths, N_steps + 1))
    r[:, 0] = r0

    for t in range(N_steps):
        Z = rng.standard_normal(N_paths)
        r[:, t+1] = cond_mean_coeff * r[:, t] + cond_mean_const + cond_std * Z

    return r


# ─── Vasicek Bond Pricing ─────────────────────────────────────────────────────

def vasicek_bond_price(r0, tau, a, b, sigma):
    """
    Closed-form zero-coupon bond price P(0, tau) in Vasicek model.

    Parameters
    ----------
    r0    : current short rate
    tau   : time to maturity (years)
    a, b, sigma : Vasicek parameters
    """
    B = (1 - np.exp(-a * tau)) / a
    ln_A = (b - sigma**2 / (2 * a**2)) * (B - tau) - (sigma**2 / (4 * a)) * B**2
    return np.exp(ln_A - B * r0)


def vasicek_yield(r0, tau, a, b, sigma):
    """Continuously-compounded yield R(0, tau)."""
    P = vasicek_bond_price(r0, tau, a, b, sigma)
    return -np.log(P) / tau


# ─── Example 1: Simulate rate paths ──────────────────────────────────────────

params = dict(r0=0.03, a=0.3, b=0.05, sigma=0.02, T=10.0)
r_paths = vasicek_simulate(**params, N_steps=500, N_paths=200)

t_grid = np.linspace(0, params["T"], 501)

plt.figure(figsize=(10, 5))
for i in range(50):
    plt.plot(t_grid, r_paths[i] * 100, alpha=0.3, lw=0.7, color="steelblue")
plt.axhline(params["b"] * 100, color="red", lw=2, linestyle="--",
            label=f"Long-run mean b = {params['b']*100:.1f}%")
plt.axhline(params["r0"] * 100, color="green", lw=1.5, linestyle=":",
            label=f"Starting rate r0 = {params['r0']*100:.1f}%")
plt.xlabel("Time (years)")
plt.ylabel("Short Rate (%)")
plt.title("Vasicek Model: Short Rate Paths (a=0.3, b=5%, σ=2%)")
plt.legend()
plt.tight_layout()
plt.savefig("vasicek_paths.png", dpi=150)
plt.show()

# ─── Example 2: Yield curves under different r0 ───────────────────────────────

maturities = np.linspace(0.25, 30, 200)
a, b, sigma = 0.3, 0.05, 0.02

plt.figure(figsize=(10, 5))
for r0, label in [(0.01, "r₀=1% (below normal)"),
                  (0.05, "r₀=5% (at normal)"),
                  (0.09, "r₀=9% (above normal)")]:
    yields = [vasicek_yield(r0, tau, a, b, sigma) * 100 for tau in maturities]
    plt.plot(maturities, yields, lw=2, label=label)

plt.axhline(b * 100, color="gray", linestyle="--", alpha=0.7, label=f"Long-run b = {b*100:.0f}%")
plt.xlabel("Maturity (years)")
plt.ylabel("Yield (%)")
plt.title("Vasicek Yield Curves: Normal, Flat, Inverted")
plt.legend()
plt.tight_layout()
plt.savefig("vasicek_yield_curves.png", dpi=150)
plt.show()

# ─── Example 3: Probability of negative rates ────────────────────────────────

from scipy.stats import norm as sp_norm

def prob_negative_rate(r0, a, b, sigma, t):
    """Probability that r(t) < 0 under Vasicek."""
    mean_t = r0 * np.exp(-a * t) + b * (1 - np.exp(-a * t))
    var_t  = (sigma**2 / (2 * a)) * (1 - np.exp(-2 * a * t))
    std_t  = np.sqrt(var_t)
    return sp_norm.cdf(0, loc=mean_t, scale=std_t)

horizons = np.linspace(0.1, 10, 100)
prob_neg = [prob_negative_rate(0.03, 0.3, 0.05, 0.02, t) for t in horizons]

plt.figure(figsize=(8, 4))
plt.plot(horizons, np.array(prob_neg) * 100, "purple", lw=2)
plt.xlabel("Horizon (years)")
plt.ylabel("P(r < 0) (%)")
plt.title("Vasicek: Probability of Negative Rates over Time\n(r₀=3%, a=0.3, b=5%, σ=2%)")
plt.tight_layout()
plt.savefig("vasicek_neg_prob.png", dpi=150)
plt.show()

# ─── Example 4: Calibrate to yield curve ─────────────────────────────────────

# Synthetic "market" yield curve (upward sloping, slightly humped)
observed_maturities = np.array([0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])
observed_yields = np.array([0.030, 0.032, 0.035, 0.038, 0.041, 0.044, 0.046, 0.047, 0.048, 0.047])

def yield_curve_error(params_vec):
    a, b, sigma, r0 = params_vec
    if a <= 0 or sigma <= 0 or r0 < -0.1:
        return 1e10
    model_yields = np.array([vasicek_yield(r0, tau, a, b, sigma) for tau in observed_maturities])
    return np.sum((model_yields - observed_yields)**2)

x0 = [0.3, 0.05, 0.015, 0.03]
bounds = [(0.01, 5), (0.0, 0.2), (0.001, 0.1), (-0.05, 0.15)]
result = minimize(yield_curve_error, x0, method="L-BFGS-B", bounds=bounds)
a_fit, b_fit, sigma_fit, r0_fit = result.x
print(f"Calibrated: a={a_fit:.3f}, b={b_fit:.3f}, sigma={sigma_fit:.4f}, r0={r0_fit:.4f}")

model_yields_fit = [vasicek_yield(r0_fit, tau, a_fit, b_fit, sigma_fit) * 100
                    for tau in maturities]

plt.figure(figsize=(9, 4))
plt.plot(maturities, model_yields_fit, "b-", lw=2, label="Vasicek (calibrated)")
plt.scatter(observed_maturities, observed_yields * 100, color="red", zorder=5, s=60, label="Market yields")
plt.xlabel("Maturity (years)")
plt.ylabel("Yield (%)")
plt.title("Vasicek Yield Curve Calibration")
plt.legend()
plt.tight_layout()
plt.savefig("vasicek_calibration.png", dpi=150)
plt.show()
```

---

## Bridge to Quant / ML

- **Hull-White extension:** Adding a time-varying drift $\theta(t)$ to exactly fit today's yield curve makes Vasicek practically useful. Hull-White is widely implemented for callable bond pricing, CVA, and XVA desks.
- **ML for yield curve modeling:** The affine structure (yield = $A(\tau) + B(\tau) r_t$) is the inspiration for **factor models** of the yield curve. PCA of yield changes recovers level, slope, and curvature factors — analogous to multi-factor Vasicek. Neural networks can learn nonlinear generalizations.
- **OU process in ML:** The Vasicek SDE is an Ornstein-Uhlenbeck process — the same dynamics used in continuous-time RL (Ornstein-Uhlenbeck noise for exploration in DDPG), and in mean-reversion trading strategies (pairs trading, statistical arbitrage).
- **Bond option pricing:** Jamshidian's decomposition allows analytic pricing of bond options under Vasicek/Hull-White — the backbone of swaption pricing in many banks.
- **Short rate simulation for CVA:** Monte Carlo simulation of short rates (using Vasicek or Hull-White) is the foundation of CVA/DVA/XVA computation on rates books.
- **Parameter estimation:** Fitting Vasicek to historical rate data is a standard exercise in MLE with latent processes — directly relevant to state-space models and Kalman filtering.

---

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why does mean reversion make the Vasicek model more economically sensible for interest rates than a simple GBM would be?
<details>
<summary>Answer</summary>
GBM (as used for stock prices) allows the process to drift arbitrarily far from its starting point over time — the variance grows without bound as T → ∞, and there is no central tendency. This is appropriate for stock prices, where there is no economic reason they should return to a fixed level. Interest rates, however, are subject to macroeconomic forces that pull them back toward equilibrium: when rates are very high, borrowing becomes expensive, investment slows, and central banks eventually cut; when rates are very low, the reverse happens. The Vasicek model's a(b − r)dt drift term captures exactly this gravitational pull: the further rates deviate from the long-run mean b, the stronger the restoring force. This prevents rates from wandering to infinity and ensures the process has a stationary long-run distribution — far more realistic for an interest rate.
</details>

**Q2.** What does it mean that Vasicek is an "affine term structure model"? Why is this property economically useful?
<details>
<summary>Answer</summary>
Affine means that the continuously-compounded yield at each maturity is a linear (affine) function of the current short rate: R(t,T) = A(τ) + B(τ)·r_t, where A and B depend only on the time-to-maturity τ = T−t. This has two important implications. First, if you observe the current short rate r_t (or proxy it with, say, the 3-month T-bill rate), you can immediately compute the entire yield curve at all maturities from a simple formula — no simulation or numerical methods needed. Second, all yields move together: when r_t rises, all yields rise proportionally (modified by B(τ), which is less than 1/a for long maturities due to mean-reversion dampening). This creates a one-factor model of the curve — a simplification, but one that makes the model analytically tractable and easy to use.
</details>

**Q3.** Vasicek allows negative interest rates. Before 2015 this was considered a critical flaw. What happened after 2015 to change practitioners' views, and what does this reveal about model design philosophy?
<details>
<summary>Answer</summary>
After 2015, the European Central Bank and Bank of Japan pushed policy rates below zero. German Bund yields went negative across much of the curve. Swiss government bonds had negative yields out to 10 years. The phenomenon that was supposed to be "impossible" in real markets actually occurred. As a result, the Vasicek model's Gaussian distribution (which allows negative rates) went from being a theoretical embarrassment to being the more realistic model for European and Japanese government bonds — CIR (which forces non-negativity) was actually less accurate in that environment. This reveals an important principle: model "flaws" are relative to the current market regime. A model feature that seems unrealistic in one era can become the accurate description in another. Design decisions should be judged against the range of scenarios the model will face, not just the current regime.
</details>

---

### Level 2 — Quantitative

**Q4.** Using the Vasicek closed-form formula, compute the 5-year zero-coupon bond price given: r₀ = 3%, a = 0.3, b = 5%, σ = 2%, τ = 5 years. Show all steps.
<details>
<summary>Answer</summary>

**Step 1: Compute B(τ)**

B(5) = (1 − e^{−0.3×5}) / 0.3
     = (1 − e^{−1.5}) / 0.3
     = (1 − 0.2231) / 0.3
     = 0.7769 / 0.3
     = **2.590**

**Step 2: Compute ln A(τ)**

ln A = (b − σ²/(2a²))(B − τ) − (σ²/(4a))·B²

b − σ²/(2a²) = 0.05 − 0.0004/(2×0.09) = 0.05 − 0.00222 = 0.04778

(B − τ) = 2.590 − 5 = −2.410

First term = 0.04778 × (−2.410) = −0.1152

σ²/(4a) = 0.0004/1.2 = 0.000333

B² = 2.590² = 6.708

Second term = −0.000333 × 6.708 = −0.00224

ln A = −0.1152 − 0.00224 = **−0.1174**

**Step 3: Compute bond price**

P(0,5) = exp(ln A − B·r₀)
       = exp(−0.1174 − 2.590 × 0.03)
       = exp(−0.1174 − 0.0777)
       = exp(−0.1951)
       = **0.8228**

The 5-year zero-coupon bond trades at \$0.8228 per dollar of face value, implying a continuously-compounded yield of −ln(0.8228)/5 = 0.199/5 = **3.97%**.

This is above r₀ = 3% because rates are expected to rise toward b = 5%.
</details>

**Q5.** Given the parameters above, compute the probability that r_t goes negative at t = 2 years (starting from r₀ = 3%). Should a practitioner be concerned about this in a 3% rate environment?
<details>
<summary>Answer</summary>

Under Vasicek, r_t at time t is normally distributed:

Mean: μ_t = r₀e^{−at} + b(1−e^{−at})
    = 0.03 × e^{−0.6} + 0.05 × (1 − e^{−0.6})
    = 0.03 × 0.5488 + 0.05 × 0.4512
    = 0.01646 + 0.02256 = **0.03902** (3.9%)

Variance: σ²_t = (σ²/(2a))(1 − e^{−2at})
        = (0.0004/0.6)(1 − e^{−1.2})
        = 0.000667 × (1 − 0.3012)
        = 0.000667 × 0.6988 = **0.000466**

Std dev = **0.0216** (2.16%)

P(r_t < 0) = N((0 − 0.03902)/0.0216) = N(−1.807) ≈ **3.5%**

In a 3% rate environment with 2% volatility, there is about a 3.5% chance of negative rates at the 2-year horizon. Whether this is concerning depends on context: for pre-2015 developed market rates it was embarrassing; post-2015 with negative European rates, it is actually realistic. For a simple teaching model used for rate dynamics, this level of negative-rate probability is generally acceptable. For production pricing of instruments that require strictly positive rates (like CIR-based models), it would motivate switching to Hull-White or CIR.
</details>

---

### Level 3 — Coding

**Q6.** The simulation uses the *exact* conditional distribution at each step rather than Euler discretization. Why is this possible for Vasicek but not, for example, for the Heston variance process?
<details>
<summary>Answer</summary>
The Vasicek SDE dr = a(b−r)dt + σdW is linear — the drift is affine in r and the diffusion is constant. For linear SDEs driven by Brownian motion, the solution is a Gaussian process whose transition distribution r_{t+dt} | r_t is analytically available: r_{t+dt} ~ N(r_t·e^{−a·dt} + b·(1−e^{−a·dt}), (σ²/2a)·(1−e^{−2a·dt})). You can sample from this distribution exactly, so each simulated path is statistically identical to what a true continuous-path Vasicek process would produce — no time-step error.

The Heston variance process dv = κ(θ−v)dt + ξ√v·dW has a square-root diffusion coefficient. This is the CIR process, whose exact transition distribution is a scaled non-central chi-squared distribution. While technically exact sampling is possible (using the Broadie-Kaya scheme), it requires computing non-central chi-squared quantiles at every step, which is computationally expensive. More importantly, the two SDEs (stock and variance) are coupled and correlated, making the exact joint transition distribution even more complex. This is why the Heston simulation uses Euler-Maruyama despite its approximation error, while Vasicek simulation uses exact conditional sampling.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| The long-run mean b is a prediction about where rates will end up | b is a model parameter that captures the equilibrium level in the model's risk-neutral dynamics. It is calibrated to match market prices and is not a forecast. The real-world expected rate may differ significantly from b due to the market price of risk. |
| Vasicek's negative rate "bug" was fixed by CIR | CIR (with √r diffusion) prevents negative rates but introduces other problems: it is harder to calibrate, has no exact simulation, and also cannot fit the initial yield curve exactly. Hull-White is the preferred solution to the curve-fit problem, and practitioners sometimes prefer Vasicek's analytical tractability over CIR's non-negativity guarantee. |
| The yield curve can move in any direction in the Vasicek model | Vasicek is a one-factor model — the single Brownian motion W_t drives everything. All yields are perfectly correlated (correlation = 1). Real yield curves show independent short-end and long-end movements. Multi-factor models (G2++) are needed to capture level/slope/curvature movements independently. |
| Calibrating Vasicek to the current yield curve requires only four numbers | With four parameters (a, b, σ, r₀), Vasicek cannot exactly match an arbitrary observed yield curve — it can only match a specific shape. Hull-White uses a time-varying θ(t) to absorb this fitting error, at the cost of an extra calibration step. |

## Related Concepts

- [[HJM Framework]] — Vasicek is a special case of HJM (exponential vol spec)
- [[CIR Model]]
- [[Hull-White Model]]
- [[Affine Term Structure Models]]
- [[Bond Basics]]
- [[Yield Curve]]
- [[Ornstein-Uhlenbeck Process]]
- [[SABR Model]]
- [[LIBOR Market Model]]

---

## Sources Used

- Vasicek, O.A. (1977). "An Equilibrium Characterization of the Term Structure." *Journal of Financial Economics* 5(2), 177–188.
- Hull, J.C. (2022). *Options, Futures, and Other Derivatives*, 11th ed. Ch. 31–32.
- Brigo, D. and Mercurio, F. (2006). *Interest Rate Models: Theory and Practice*, 2nd ed. Ch. 3. Springer.
- James, J. and Webber, N. (2000). *Interest Rate Modelling*. Wiley.

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review passed — OU solution, bond pricing A/B formulas, simulation code verified | QA review |
