---
type: concept
domain: 30-Models
tags: [pricing, options, stochastic-volatility]
status: math
stability: evolving
confidence: high
last_reviewed: 2026-04-11
review_interval_days: 90
sources:
  - "Gatheral, The Volatility Surface, ch. 1-2"
  - "Heston (1993), A Closed-Form Solution for Options with Stochastic Volatility"
created: 2026-04-12
---

> Mean-reverting stochastic variance; captures vol smile

> [!info] Problem Chain
> **Chain:** Pricing → Gap 5: BSM assumes constant σ — real markets show a volatility smile
> **This concept:** Solution B to Gap 5 — makes volatility itself a random mean-reverting process; the correlation ρ between stock and vol shocks generates the observed skew
> **Alternative approaches to this gap:** [[Local Volatility]] (Solution A — deterministic σ(S,t)), [[Merton Jump-Diffusion]] (Solution C — discrete jumps)
> **You need first:** [[Black-Scholes Model]], [[Volatility Surface]], [[Stochastic Differential Equations]]
> **This unlocks:** [[Volatility Surface]] (calibration target), [[SABR Model]] (analogous stochastic vol for rates), [[Exotic Options]] (stochastic vol pricing)

## Why This Exists

**The gap:** Black-Scholes assumes volatility is a single constant σ for all strikes and maturities. In practice, OTM puts trade at much higher implied vol than ATM options, and this "smile" changes shape over time. BSM cannot reproduce this — it is structurally incapable of generating a non-flat implied vol surface.

**What came before:** BSM's constant σ was the only option until practitioners observed that different strikes required different σ inputs to match market prices. Traders began using different σ values for different contracts (the "practitioner's BSM"), but this was unprincipled — there was no single consistent model behind it.

**What this adds:** Heston (1993) makes volatility itself stochastic: it has its own mean-reverting random process, correlated with the stock. When stocks fall, volatility spikes — this negative correlation ρ (typically −0.7 to −0.9 for equity indices) directly generates the downward-sloping skew observed in practice. Unlike BSM's flat line, Heston's model produces a family of smile shapes controlled by just five interpretable parameters. Crucially, Heston retains a semi-analytic pricing formula via Fourier methods — much faster than full Monte Carlo.

**What it still doesn't solve:** Heston still struggles with the extreme skew at very short maturities (days to weeks) that crash dynamics create. Calibration is non-trivial and parameter instability day-to-day is a practical challenge. Forward smile predictions — how today's smile predicts future smiles — are also unrealistic, making Heston problematic for some exotic products.

---

## Math Concepts

### The Two Coupled SDEs

The model is driven by two stochastic processes evolving together:

**Stock price:**
$$dS_t = r S_t \, dt + \sqrt{v_t} \, S_t \, dW_t^S$$

**Variance:**
$$dv_t = \kappa(\theta - v_t) \, dt + \xi \sqrt{v_t} \, dW_t^v$$

with correlation:
$$dW_t^S \, dW_t^v = \rho \, dt$$

### Parameters

| Symbol | Name | Plain English |
|--------|------|---------------|
| $r$ | risk-free rate | same as BSM |
| $v_0$ | initial variance | today's instantaneous variance (vol = $\sqrt{v_0}$) |
| $\kappa$ | mean-reversion speed | how fast variance snaps back to its long-run average; higher = faster |
| $\theta$ | long-run mean variance | the "equilibrium" variance the process drifts toward |
| $\xi$ | vol of vol | how much variance itself fluctuates; higher = fatter tails, wider smile |
| $\rho$ | correlation | typically negative for equities (−0.7 to −0.9); creates skew |

### Feller Condition

For variance to stay strictly positive (not hit zero), the parameters must satisfy:
$$2\kappa\theta > \xi^2$$

If this is violated, the variance process can touch zero. In practice, calibrated parameters often violate the Feller condition slightly, and practitioners accept this.

### Semi-Analytic Pricing

The European call price is computed by Fourier inversion of the characteristic function $\phi(\omega)$ of $\log S_T$:

$$C(S_0, K, T) = S_0 P_1 - K e^{-rT} P_2$$

where $P_1, P_2$ are risk-adjusted probabilities recovered from:

$$P_j = \frac{1}{2} + \frac{1}{\pi} \int_0^\infty \text{Re}\!\left[\frac{e^{-i\omega \ln K} \phi_j(\omega)}{i\omega}\right] d\omega$$

The characteristic function has a closed form involving complex exponentials. You don't need to derive it — you just plug parameters in and integrate numerically (or use a library).

---

## Walkthrough

### Typical Parameter Values (S&P 500 equity)

| Parameter | Typical Range | Intuition |
|-----------|--------------|-----------|
| $v_0$ | 0.04 (= 20% vol) | matches today's ATM vol |
| $\kappa$ | 1–5 | half-life of vol shock ~ 0.14–0.7 years |
| $\theta$ | 0.04–0.09 | long-run vol ~ 20–30% |
| $\xi$ | 0.2–0.8 | higher = wider smile |
| $\rho$ | −0.9 to −0.5 | negative = put skew |

### Calibration Sketch

1. Collect market prices (or implied vols) for a grid of strikes and expiries.
2. For each candidate parameter vector $(\kappa, \theta, \xi, \rho, v_0)$, compute model prices using the semi-analytic formula.
3. Minimize the weighted sum of squared differences between model and market implied vols.
4. Use a gradient-free optimizer (Nelder-Mead, differential evolution) or automatic differentiation.

### What the Model Produces

- A vol surface that curves — not flat like BSM.
- The slope of the skew is controlled primarily by $\rho$.
- The curvature (smile, not just slope) is controlled by $\xi$.
- The term structure of ATM vol is controlled by $\kappa$ and $\theta$.

---

## Analysis

### Pros vs BSM

- Naturally produces implied vol smile/skew without ad-hoc adjustments.
- Semi-analytic pricing formula — much faster than full Monte Carlo.
- Intuitive parameters with economic meaning.
- Widely used — industry standard for equity derivatives.

### Cons / Where It Breaks

- **Calibration is non-trivial.** The loss surface has flat regions and local minima; parameters can be unstable across days.
- **Feller violation in practice.** Calibrated parameters often imply variance can touch zero, which causes numerical issues in simulation.
- **Short-dated skew.** Heston underestimates the extreme skew at very short maturities (days to weeks). Jumps or rough vol models handle this better.
- **Forward smile dynamics are debatable.** The model predicts how the smile evolves over time, and traders sometimes find this unrealistic (similar complaint applies to local vol but in a different direction).
- **Not ideal for exotic products** that depend heavily on realized variance paths (e.g., variance swaps, cliquets) without additional calibration.

### Industry Usage

Still the most widely used stochastic vol model for equity and FX derivatives. Often extended to Local Stochastic Volatility (LSV) for better fit to the full surface.

---

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# ─── Heston Monte Carlo Simulation ───────────────────────────────────────────

def heston_simulate(S0, v0, r, kappa, theta, xi, rho, T, N_steps, N_paths, seed=42):
    """
    Simulate (S, v) paths under the Heston model using the Euler-Maruyama scheme.

    Parameters
    ----------
    S0      : initial stock price
    v0      : initial variance (e.g. 0.04 for 20% vol)
    r       : risk-free rate
    kappa   : mean-reversion speed for variance
    theta   : long-run variance
    xi      : vol of vol
    rho     : correlation between stock and variance Brownian motions
    T       : time horizon (years)
    N_steps : number of time steps
    N_paths : number of simulated paths
    """
    rng = np.random.default_rng(seed)
    dt = T / N_steps

    S = np.zeros((N_paths, N_steps + 1))
    v = np.zeros((N_paths, N_steps + 1))
    S[:, 0] = S0
    v[:, 0] = v0

    for t in range(N_steps):
        # Two independent standard normals
        Z1 = rng.standard_normal(N_paths)
        Z2 = rng.standard_normal(N_paths)

        # Correlated Brownians: dW_S and dW_v
        dW_S = Z1
        dW_v = rho * Z1 + np.sqrt(1 - rho**2) * Z2

        # Current variance, floored at 0 to avoid sqrt of negative
        v_cur = np.maximum(v[:, t], 0)

        # Variance update (Euler with floor — "full truncation" scheme)
        v[:, t+1] = np.maximum(
            v_cur + kappa * (theta - v_cur) * dt + xi * np.sqrt(v_cur * dt) * dW_v,
            0
        )

        # Stock price update (log-Euler for positivity)
        S[:, t+1] = S[:, t] * np.exp(
            (r - 0.5 * v_cur) * dt + np.sqrt(v_cur * dt) * dW_S
        )

    return S, v


# ─── Heston Semi-Analytic Call Price ─────────────────────────────────────────

def heston_char_fn(phi, S0, v0, r, kappa, theta, xi, rho, T, j):
    """Characteristic function for Heston model (Heston 1993 formulation)."""
    i = 1j
    if j == 1:
        u = 0.5
        b = kappa - rho * xi
    else:
        u = -0.5
        b = kappa

    a = kappa * theta
    x = np.log(S0)

    d = np.sqrt((rho * xi * i * phi - b)**2 - xi**2 * (2 * u * i * phi - phi**2))
    g = (b - rho * xi * i * phi + d) / (b - rho * xi * i * phi - d)

    C = r * i * phi * T + (a / xi**2) * (
        (b - rho * xi * i * phi + d) * T
        - 2 * np.log((1 - g * np.exp(d * T)) / (1 - g))
    )
    D = ((b - rho * xi * i * phi + d) / xi**2) * (
        (1 - np.exp(d * T)) / (1 - g * np.exp(d * T))
    )

    return np.exp(C + D * v0 + i * phi * x)


def heston_call_price(S0, K, T, r, v0, kappa, theta, xi, rho):
    """
    Semi-analytic European call price under the Heston model.
    Uses numerical integration of the characteristic function.
    """
    def integrand(phi, j):
        cf = heston_char_fn(phi, S0, v0, r, kappa, theta, xi, rho, T, j)
        return np.real(np.exp(-1j * phi * np.log(K)) * cf / (1j * phi))

    P1, _ = quad(integrand, 1e-6, 200, args=(1,), limit=200)
    P2, _ = quad(integrand, 1e-6, 200, args=(2,), limit=200)

    P1 = 0.5 + P1 / np.pi
    P2 = 0.5 + P2 / np.pi

    return S0 * P1 - K * np.exp(-r * T) * P2


# ─── Example: simulate paths and price a call ─────────────────────────────────

# Typical S&P 500 parameters
params = dict(
    S0=100, v0=0.04, r=0.03,
    kappa=2.0, theta=0.04, xi=0.5, rho=-0.7,
    T=1.0
)

S_paths, v_paths = heston_simulate(**params, N_steps=252, N_paths=1000)

# Plot a sample of stock paths and variance paths
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
t_grid = np.linspace(0, params["T"], 253)

for i in range(20):
    axes[0].plot(t_grid, S_paths[i], alpha=0.4, lw=0.8)
axes[0].set_title("Heston: Stock Price Paths")
axes[0].set_xlabel("Time (years)")
axes[0].set_ylabel("Stock Price")

for i in range(20):
    axes[1].plot(t_grid, np.sqrt(v_paths[i]) * 100, alpha=0.4, lw=0.8)
axes[1].set_title("Heston: Volatility Paths (%)")
axes[1].set_xlabel("Time (years)")
axes[1].set_ylabel("Volatility (%)")
plt.tight_layout()
plt.savefig("heston_paths.png", dpi=150)
plt.show()

# Semi-analytic call price
call_price = heston_call_price(
    S0=100, K=100, T=1.0, r=0.03,
    v0=0.04, kappa=2.0, theta=0.04, xi=0.5, rho=-0.7
)
print(f"Heston ATM Call Price: {call_price:.4f}")

# MC price for comparison
payoffs = np.maximum(S_paths[:, -1] - 100, 0)
mc_price = np.exp(-params["r"] * params["T"]) * payoffs.mean()
print(f"Monte Carlo ATM Call Price: {mc_price:.4f}")

# Implied vol smile: price calls across strikes, invert BSM
from scipy.optimize import brentq
from scipy.stats import norm

def bsm_call(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)

def implied_vol(price, S, K, T, r):
    try:
        return brentq(lambda s: bsm_call(S, K, T, r, s) - price, 1e-6, 5.0)
    except Exception:
        return np.nan

strikes = np.linspace(70, 140, 30)
ivols = []
for K in strikes:
    p = heston_call_price(100, K, 1.0, 0.03, 0.04, 2.0, 0.04, 0.5, -0.7)
    ivols.append(implied_vol(p, 100, K, 1.0, 0.03))

plt.figure(figsize=(8, 4))
plt.plot(strikes, np.array(ivols) * 100, "b-o", markersize=4)
plt.axhline(20, color="gray", linestyle="--", label="BSM flat vol (20%)")
plt.title("Heston Implied Volatility Smile (T=1yr)")
plt.xlabel("Strike")
plt.ylabel("Implied Vol (%)")
plt.legend()
plt.tight_layout()
plt.savefig("heston_smile.png", dpi=150)
plt.show()
```

---

## Bridge to Quant / ML

- **Vol surface calibration:** Heston is the baseline model you calibrate to the market vol surface. The five parameters $(v_0, \kappa, \theta, \xi, \rho)$ are found by minimizing calibration error. Neural networks (e.g., Deep Calibration, Horvath et al. 2021) can learn the inverse mapping from vol surface to Heston parameters in milliseconds.
- **Rough Volatility:** The Heston process is Markovian with exponentially decaying autocorrelation. Realized vol has longer memory (Hurst exponent < 0.5). Rough Heston (El Euch & Rosenbaum 2019) extends this with fractional Brownian motion.
- **Local Stochastic Volatility (LSV):** Heston is often used as the stochastic component of an LSV model, multiplied by a Dupire local vol function to fix residual calibration error.
- **Variance swaps:** The Heston model has a tractable formula for the fair variance strike, connecting to the VIX replication portfolio.
- **Risk management:** $\partial C / \partial \rho$, $\partial C / \partial \xi$ are "vol-of-vol" and "correlation" Greeks used by exotic desks.

---

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why does adding a second stochastic process for volatility allow Heston to produce a volatility smile, when BSM with its single process cannot?
<details>
<summary>Answer</summary>
In BSM, the stock price at expiry is lognormally distributed with fixed variance. The implied vol is therefore the same constant for every strike — the flat BSM smile. In Heston, variance v_t fluctuates randomly over time, so by the time you reach expiry, the stock's distribution is a mixture of lognormals (each conditioned on a different realized vol path). Mixtures of lognormals have fatter tails than a single lognormal. Fat tails mean OTM options (which depend on tail probabilities) are more expensive relative to ATM options — producing a smile. The correlation ρ between stock and vol movements introduces asymmetry: if stocks falling and vol rising are correlated (ρ < 0), the left tail is fatter than the right, creating skew (puts more expensive than calls) rather than a symmetric smile.
</details>

**Q2.** What role does the parameter ρ play in Heston, and why is it typically negative for equity indices?
<details>
<summary>Answer</summary>
ρ is the correlation between the Brownian motion driving the stock price and the Brownian motion driving the variance. When ρ < 0, a shock that drives the stock down tends to simultaneously drive variance up. This is empirically observed — the VIX spikes when equities sell off. In the pricing formula, this negative correlation makes the left tail of the stock price distribution heavier (large downside moves coincide with high vol, making them more likely), which means OTM puts are priced at higher implied vol than OTM calls. The steeper the negative ρ, the more pronounced the downward skew. For equity indices, ρ is typically between −0.7 and −0.9; for FX it is closer to zero.
</details>

**Q3.** What is the Feller condition in Heston, and why do practitioners sometimes accept its violation?
<details>
<summary>Answer</summary>
The Feller condition is 2κθ > ξ². When satisfied, the variance process v_t is strictly positive and cannot reach zero. When violated, v_t can touch zero (though it remains non-negative if the full-truncation scheme is used). In practice, calibration to market option prices often yields parameter sets where 2κθ ≤ ξ², because fitting the observed vol smile — especially the short-dated skew — sometimes requires high vol-of-vol ξ relative to the mean-reversion speed κ and long-run level θ. Practitioners accept the violation because (1) the numerical impact is manageable with the truncation scheme, (2) real-world variance does approach near-zero levels occasionally, and (3) forcing the Feller constraint degrades smile fit.
</details>

---

### Level 2 — Quantitative

**Q4.** Suppose you observe the following 1-year ATM implied vol at 20%, with a vol-of-vol ξ = 0.5, correlation ρ = −0.7, mean-reversion κ = 2.0, and long-run variance θ = 0.04 (i.e., 20% long-run vol). Estimate qualitatively what happens to the implied vol at the 80% strike vs. the 120% strike, and explain the directional effect of ρ = −0.7.
<details>
<summary>Answer</summary>
With ρ = −0.7 (strong negative correlation), the Heston model produces a pronounced downward skew:

- 80% strike (OTM put, left side): implied vol will be significantly higher than the ATM 20%, perhaps 23–27% depending on exact parameters. The left tail is fat because downside stock moves coincide with volatility spikes.
- 120% strike (OTM call, right side): implied vol will be lower than ATM, perhaps 17–19%. The right tail is compressed because upside moves tend to coincide with falling volatility.

The asymmetry is caused directly by ρ. If ρ were 0, you'd get a symmetric smile (both OTM puts and OTM calls more expensive than ATM by the same amount, driven purely by ξ). If ρ were +0.7, the smile would tilt the other way (OTM calls richer than OTM puts) — which is sometimes observed in commodity markets where prices and volatility are positively correlated.

At ξ = 0.5, the curvature (smile width) is also substantial — both wings elevated relative to a low-ξ model.
</details>

**Q5.** The Heston call pricing formula is C = S₀P₁ − K e^{−rT} P₂. Given that for BSM, C = S₀N(d₁) − K e^{−rT} N(d₂), identify what P₁ and P₂ correspond to and why Fourier integration is needed to compute them.
<details>
<summary>Answer</summary>
The structural parallel is exact: in BSM, N(d₂) is the risk-neutral probability Q(S_T > K), and N(d₁) is the risk-adjusted probability under the "stock measure." In Heston, P₂ plays the role of N(d₂) — the risk-neutral probability of finishing in-the-money — and P₁ plays the role of N(d₁).

The difference is that in BSM, S_T is lognormally distributed so Q(S_T > K) has a closed-form normal CDF expression. In Heston, S_T is not lognormal — its distribution is a complex mixture that depends on the stochastic variance path. There is no elementary closed-form CDF.

What Heston (1993) showed is that the *characteristic function* φ(ω) = E[e^{iω ln S_T}] does have a closed-form expression. You can recover the probabilities P₁ and P₂ from the characteristic function by Fourier inversion: P_j = ½ + (1/π) ∫₀^∞ Re[e^{−iω ln K} φ_j(ω) / (iω)] dω. This integral must be evaluated numerically, but it is a one-dimensional integral — fast and reliable.
</details>

---

### Level 3 — Coding

**Q6.** In the Monte Carlo simulation, the variance update uses `np.maximum(v_cur + ..., 0)` to floor the variance at zero. Why is this "full truncation" scheme used rather than just letting the Euler step run freely? What pathology would appear without it?
<details>
<summary>Answer</summary>
The Euler-Maruyama discretization of the variance SDE: v_{t+dt} = v_t + κ(θ − v_t)dt + ξ√(v_t·dt)·dW_v. If v_t is small and dW_v is sufficiently negative, the update can make v_{t+dt} negative. A negative variance is mathematically impossible (variance is a squared quantity) and practically catastrophic: taking √(v) in the next step would produce a NaN or imaginary number, crashing the simulation.

The full truncation scheme: v_{t+dt} = max(v_t + ..., 0) ensures non-negativity by absorbing the boundary. An alternative is "reflection" (take absolute value) but truncation is more common and produces better empirical results.

Without the floor, on a typical simulation with high ξ (vol-of-vol) or Feller condition violation, a significant fraction of paths would generate negative variance in the first few steps, producing NaN values that propagate through the entire simulation and make the price estimate meaningless.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Heston fits any vol surface perfectly | Heston is a 5-parameter model and cannot fit an arbitrary surface exactly. It fits the broad shape (skew, curvature, term structure) but not every liquid quote simultaneously. For perfect fit, you need Local Vol (Dupire) or an extension like Local Stochastic Volatility. |
| The Feller condition must always be satisfied | In practice it is frequently violated in calibrated parameters. Practitioners accept this and use truncation schemes in simulation. The condition is a theoretical requirement for strict non-negativity, not a calibration constraint. |
| A more negative ρ always means a better model | ρ controls the slope of the skew. A more negative ρ fits equity markets better in normal conditions, but during crises the skew steepens in ways that Heston (with any fixed ρ) cannot capture. The model has structural limits regardless of parameter choice. |
| Heston is slow because it requires Monte Carlo | The semi-analytic formula (Fourier inversion of the characteristic function) prices European calls much faster than Monte Carlo — comparable speed to BSM once the numerical integration is set up. Monte Carlo is only needed for path-dependent exotics. |

## Related Concepts

- [[Black-Scholes Model]]
- [[Local Volatility]]
- [[SABR Model]]
- [[Volatility Surface]]
- [[Characteristic Functions and Fourier Pricing]]
- [[Variance Swaps]]
- [[CIR Model]]

---

## Sources Used

- Heston, S.L. (1993). "A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options." *Review of Financial Studies* 6(2).
- Gatheral, J. (2006). *The Volatility Surface: A Practitioner's Guide*. Wiley Finance. Ch. 1–2.
- Rouah, F.D. (2013). *The Heston Model and Its Extensions in Matlab and C#*. Wiley.

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review passed — SDEs, Feller condition, characteristic function, Monte Carlo code verified | QA review |
