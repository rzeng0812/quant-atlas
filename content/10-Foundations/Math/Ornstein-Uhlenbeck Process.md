---
type: concept
domain: 10-Foundations
tags: [math, stochastic-calculus, mean-reversion]
status: evergreen
stability: stable
confidence: high
last_reviewed: 2026-04-18
review_interval_days: 365
sources:
  - "Hull, Options, Futures, and Other Derivatives, ch. 14"
  - "Shreve, Stochastic Calculus for Finance II, ch. 4"
created: 2026-04-18
---

> Mean-reverting SDE: dX = κ(μ − X)dt + σdW. The canonical model for anything that is pulled back toward an equilibrium.

> [!info] Problem Chain
> **Chain:** Pricing / Alpha → Gap 2: A model for mean-reverting quantities (rates, spreads, volatility)
> **This concept:** Provides the continuous-time model for any financial quantity that is pulled back toward an equilibrium — the counterpart to GBM for non-trending processes.
> **Alternative approaches to this gap:** [[Geometric Brownian Motion]] handles trending quantities; CIR process (positive-valued OU variant) is used when negativity is not allowed
> **You need first:** [[Brownian Motion]], [[Stochastic Differential Equations]], [[Ito's Lemma]]
> **This unlocks:** [[Vasicek Model]], [[Pairs Trading]], [[Mean Reversion]], [[Heston Model]] (variance process)

## Why This Exists

**The gap:** GBM models quantities that drift and diffuse without bound — appropriate for equity prices. But many financial quantities are pulled back toward equilibrium by economic forces: interest rates, yield spreads, implied volatility, pairs-trade spreads. GBM with no restoring force is the wrong model for these.

**What came before:** Applying GBM to interest rates or spreads. This fails immediately: GBM drifts without bound and can never settle around a long-run level. Very high rates choke borrowing (pushing rates back down); very low rates invite speculation (pushing rates back up). GBM has no mechanism for this.

**What this adds:** A drift term $\kappa(\mu - X_t)$ that acts as a restoring force — the further the process moves from its equilibrium $\mu$, the harder it is pulled back. The parameter $\kappa$ controls how fast reversion happens (expressed naturally as a half-life: $\ln 2 / \kappa$). The process has a stationary distribution, an exact solution, and a clean discrete-time equivalent as AR(1) — making it both theoretically tractable and practically estimable from data.

**What it still doesn't solve:** The OU process is Gaussian — it allows negative values, which is inappropriate for interest rates (though acceptable for log-spreads). For strictly positive mean-reverting processes, the CIR model replaces the constant diffusion $\sigma\,dW$ with $\sigma\sqrt{X_t}\,dW$, keeping the process non-negative. See [[Vasicek Model]] and [[Heston Model]].

---

## Math Concepts

### The SDE

The Ornstein-Uhlenbeck process $X_t$ satisfies:

$$dX_t = \kappa(\mu - X_t) \, dt + \sigma \, dW_t$$

| Symbol | Name | Plain English |
|--------|------|---------------|
| $\kappa > 0$ | speed of mean reversion | how fast the process snaps back; higher = faster |
| $\mu$ | long-run mean | the equilibrium level $X_t$ is pulled toward |
| $\sigma$ | volatility / noise | how much random shock hits the process each instant |
| $W_t$ | standard Brownian motion | the source of randomness |

**Key intuition:** The drift term $\kappa(\mu - X_t)$ is a restoring force. When $X_t > \mu$, the drift is negative (pushes down). When $X_t < \mu$, the drift is positive (pushes up). The further $X_t$ is from $\mu$, the stronger the pull. $\sigma dW_t$ adds continuous random shocks on top.

### Exact Solution

Because the SDE is linear in $X_t$, it can be solved exactly via integrating factor $e^{\kappa t}$:

$$X_t = \mu + (X_0 - \mu) e^{-\kappa t} + \sigma \int_0^t e^{-\kappa(t-s)} \, dW_s$$

The stochastic integral is Gaussian, so $X_t$ is **normally distributed** given $X_0$:

$$X_t \mid X_0 \sim \mathcal{N}\!\left(\mu + (X_0 - \mu) e^{-\kappa t},\ \frac{\sigma^2}{2\kappa}\left(1 - e^{-2\kappa t}\right)\right)$$

As $t \to \infty$, the distribution converges to the **stationary distribution**:

$$X_\infty \sim \mathcal{N}\!\left(\mu,\ \frac{\sigma^2}{2\kappa}\right)$$

The process is ergodic: it forgets its initial condition and settles into this stationary Normal.

### Half-Life of Mean Reversion

How long does it take for the process to cover half the distance back to $\mu$? From the conditional mean $\mathbb{E}[X_t] = \mu + (X_0 - \mu)e^{-\kappa t}$, the gap shrinks by half when $e^{-\kappa t} = 0.5$:

$$t_{1/2} = \frac{\ln 2}{\kappa}$$

This is the **half-life** — the most intuitive way to communicate $\kappa$. If $\kappa = 0.1$, the half-life is 6.9 time units. If $\kappa = 2$, it is 0.35 time units — very fast reversion.

### Discrete-Time Equivalent: AR(1)

Discretize the SDE with step $\Delta t$:

$$X_{t+\Delta t} \approx X_t + \kappa(\mu - X_t)\Delta t + \sigma\sqrt{\Delta t}\, Z, \quad Z \sim \mathcal{N}(0,1)$$

Rearranging:

$$X_{t+1} = \underbrace{a}_{= \kappa\mu\Delta t} + \underbrace{b}_{= 1 - \kappa\Delta t} X_t + \varepsilon_t$$

This is a first-order autoregressive process, **AR(1)**. The mapping is:

$$\kappa = \frac{1 - b}{\Delta t}, \qquad \mu = \frac{a}{1 - b}, \qquad \sigma = \frac{\text{std}(\varepsilon)}{\sqrt{\Delta t}}$$

This is the bridge to time-series econometrics: fitting an OU process to data is equivalent to running OLS on an AR(1) regression.

---

## Walkthrough

### Step 1: Understand the parameters qualitatively

Consider a spread $X_t$ with $\mu = 0$, $\kappa = 2$, $\sigma = 1$.

- Half-life: $\ln 2 / 2 \approx 0.35$ years — if we use annual time units, the spread halves its deviation in about 4 months.
- Stationary vol: $\sigma / \sqrt{2\kappa} = 1/2 = 0.5$ — in equilibrium, expect the spread to be within $\pm 1$ roughly 95% of the time.

### Step 2: Simulate using the exact method

Use the exact conditional distribution at each step (better than Euler for OU):

$$X_{t+dt} \sim \mathcal{N}\!\left(\mu + (X_t - \mu)e^{-\kappa \, dt},\ \frac{\sigma^2}{2\kappa}(1 - e^{-2\kappa \, dt})\right)$$

### Step 3: Fit AR(1) to real or synthetic data

Given a time series $\{X_1, X_2, \ldots, X_N\}$ sampled at interval $\Delta t$:

1. Run OLS: $X_{t+1} = a + b X_t + \varepsilon_t$
2. Recover: $\kappa = (1-b)/\Delta t$, $\mu = a/(1-b)$, $\sigma = \text{std}(\hat\varepsilon)/\sqrt{\Delta t}$
3. Check stationarity: need $|b| < 1$ (i.e., $\kappa > 0$). If $b \geq 1$, the series is a random walk or explosive — no mean reversion.

### Step 4: Assess trading signal

In pairs trading: compute the z-score of the current spread vs the estimated stationary distribution:

$$z_t = \frac{X_t - \mu}{\sigma / \sqrt{2\kappa}}$$

Enter a long position when $z_t < -2$, exit when $z_t \approx 0$, reverse when $z_t > +2$.

---

## Analysis

### Properties Summary

| Property | Value / Implication |
|----------|---------------------|
| Distribution at time $t$ | Normal (Gaussian) |
| Stationary distribution | $\mathcal{N}(\mu,\ \sigma^2 / 2\kappa)$ |
| Is it a martingale? | No — the drift is non-zero |
| Markov property | Yes — future depends only on current value |
| Half-life | $\ln 2 / \kappa$ |
| Quadratic variation | $\sigma^2 t$ (same as scaled BM) |

### When Mean Reversion Breaks Down

- If $\kappa \to 0$, the OU process approaches a random walk (Brownian motion with drift). The half-life $\to \infty$ — there is no reversion.
- In practice, estimate $\kappa$ and do an **Augmented Dickey-Fuller (ADF) test** for stationarity before assuming mean reversion. A non-significant ADF means the null of a unit root ($b = 1$) cannot be rejected — do not trade this spread as mean-reverting.
- **Regime changes** can make a historically mean-reverting spread break down: the two assets may decouple due to fundamental changes (e.g., a merger falls through, regulatory change, macro regime shift).

### OU vs GBM: The Key Contrast

| | GBM | OU |
|--|-----|----|
| Drift | $\mu S_t$ (proportional to level) | $\kappa(\mu - X_t)$ (proportional to deviation) |
| Long-run behavior | Drifts to $\pm\infty$ | Hovers around $\mu$ |
| Best for | Stock prices | Spreads, rates, vol |
| Discrete analog | Geometric random walk | AR(1) |

---

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ─── Exact OU Simulation ──────────────────────────────────────────────────────

def simulate_ou(X0, kappa, mu, sigma, T, N_steps, N_paths, seed=42):
    """
    Simulate Ornstein-Uhlenbeck paths using the exact conditional distribution.

    Parameters
    ----------
    X0     : initial value
    kappa  : speed of mean reversion
    mu     : long-run mean
    sigma  : volatility
    T      : total time horizon
    N_steps: number of time steps
    N_paths: number of paths
    """
    rng = np.random.default_rng(seed)
    dt = T / N_steps
    t = np.linspace(0, T, N_steps + 1)

    exp_kdt = np.exp(-kappa * dt)
    cond_mean_coeff = exp_kdt
    cond_mean_const = mu * (1 - exp_kdt)
    cond_std = sigma * np.sqrt((1 - np.exp(-2 * kappa * dt)) / (2 * kappa))

    X = np.zeros((N_paths, N_steps + 1))
    X[:, 0] = X0

    for i in range(N_steps):
        Z = rng.standard_normal(N_paths)
        X[:, i+1] = cond_mean_coeff * X[:, i] + cond_mean_const + cond_std * Z

    return t, X


# ─── Visualize Mean Reversion ─────────────────────────────────────────────────

params = dict(X0=3.0, kappa=2.0, mu=0.0, sigma=1.0, T=5.0)
t, X = simulate_ou(**params, N_steps=500, N_paths=200)

plt.figure(figsize=(10, 5))
for i in range(50):
    plt.plot(t, X[i], alpha=0.25, lw=0.7, color="steelblue")
plt.axhline(params["mu"], color="red", lw=2, linestyle="--",
            label=f"Long-run mean μ = {params['mu']}")
plt.axhline(params["X0"], color="green", lw=1.5, linestyle=":",
            label=f"Start X₀ = {params['X0']}")
half_life = np.log(2) / params["kappa"]
plt.axvline(half_life, color="orange", lw=1.5, linestyle="--",
            label=f"Half-life = {half_life:.2f}")
plt.xlabel("Time")
plt.ylabel("X(t)")
plt.title("Ornstein-Uhlenbeck: Mean Reversion (κ=2, μ=0, σ=1)")
plt.legend()
plt.tight_layout()
plt.savefig("ou_paths.png", dpi=150)
plt.show()


# ─── Fit AR(1) to Synthetic Data → Recover OU Parameters ─────────────────────

def fit_ou_from_ar1(series, dt):
    """
    Fit OU parameters from a time series using OLS on the AR(1) representation.

    Returns kappa, mu, sigma estimates.
    """
    X_t = series[:-1]
    X_tp1 = series[1:]

    # OLS: X_{t+1} = a + b * X_t + eps
    slope, intercept, r_value, p_value, std_err = stats.linregress(X_t, X_tp1)
    b = slope
    a = intercept
    residuals = X_tp1 - (a + b * X_t)

    kappa_hat = (1 - b) / dt
    mu_hat    = a / (1 - b)
    sigma_hat = np.std(residuals, ddof=2) / np.sqrt(dt)

    return kappa_hat, mu_hat, sigma_hat, r_value**2


# Generate synthetic data with known parameters
true_kappa, true_mu, true_sigma = 2.0, 0.0, 1.0
_, X_syn = simulate_ou(X0=0.0, kappa=true_kappa, mu=true_mu, sigma=true_sigma,
                        T=20.0, N_steps=2000, N_paths=1, seed=7)
series = X_syn[0]
dt = 20.0 / 2000

kappa_est, mu_est, sigma_est, r2 = fit_ou_from_ar1(series, dt)

print(f"True:      κ={true_kappa:.2f}, μ={true_mu:.2f}, σ={true_sigma:.2f}")
print(f"Estimated: κ={kappa_est:.2f}, μ={mu_est:.3f}, σ={sigma_est:.2f}, R²={r2:.4f}")


# ─── Pairs Trading Signal: Z-Score ────────────────────────────────────────────

stationary_std = true_sigma / np.sqrt(2 * kappa_est)
z_score = (series - mu_est) / stationary_std

plt.figure(figsize=(12, 4))
plt.plot(z_score[:500], lw=0.8, color="navy", label="Z-score of spread")
plt.axhline( 2, color="red",   lw=1.5, linestyle="--", label="Entry short (+2σ)")
plt.axhline(-2, color="green", lw=1.5, linestyle="--", label="Entry long (−2σ)")
plt.axhline( 0, color="gray",  lw=1.0, linestyle=":")
plt.xlabel("Time step")
plt.ylabel("Z-score")
plt.title("OU Process: Pairs Trading Z-Score Signal")
plt.legend()
plt.tight_layout()
plt.savefig("ou_zscore.png", dpi=150)
plt.show()
```

---

## Bridge to Quant / ML

- **Interest rate modeling:** The [[Vasicek Model]] is an OU process applied to the short rate $r_t$. The exact same math — just with $r$ in place of $X$ and a specific economic interpretation of $\kappa$, $\mu$, $\sigma$.
- **Pairs trading / statistical arbitrage:** The spread between two cointegrated assets is modeled as OU. Fit $\kappa$, $\mu$, $\sigma$ from historical data; trade z-scores. This is the backbone of classic stat arb strategies. See [[Pairs Trading]].
- **Volatility mean reversion:** Realized and implied volatility are modeled as OU in stochastic vol models (Heston uses a CIR-like process for variance, which is a positive-valued analog of OU). See [[Heston Model]].
- **Continuous-time RL:** In deep reinforcement learning (DDPG algorithm), Ornstein-Uhlenbeck noise is used for action exploration because it produces temporally correlated (smooth) random perturbations — more realistic for continuous control than white noise.
- **Regime detection:** A sudden shift in $\kappa$ (or even a flip to $\kappa < 0$) signals a regime change — the spread stopped mean-reverting and started trending. Detecting this in real time is a key [[Regime Detection]] challenge.
- **Kalman filter:** The OU process is a linear Gaussian state-space model. The Kalman filter is the optimal real-time estimator for the state $X_t$ when observations are noisy — directly applicable to latent spread estimation in pairs trading.

---

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** The OU SDE is $dX_t = \kappa(\mu - X_t)\,dt + \sigma\,dW_t$. Explain each term in plain English. What happens to the drift when $X_t$ is far above $\mu$ vs. far below $\mu$?

<details>
<summary>Answer</summary>

- $\kappa(\mu - X_t)\,dt$ — the **drift term**, a restoring force. It pulls $X_t$ toward the long-run mean $\mu$ at a rate proportional to how far away $X_t$ is. This is the "rubber band" — the further you pull, the harder it snaps back.
- $\sigma\,dW_t$ — the **diffusion term**, a continuous random shock of magnitude $\sigma$ per $\sqrt{dt}$. This is pure noise overlaid on the restoring force.

**When $X_t > \mu$:** The drift $\kappa(\mu - X_t)$ is *negative* — the process is pushed downward toward $\mu$.

**When $X_t < \mu$:** The drift $\kappa(\mu - X_t)$ is *positive* — the process is pushed upward toward $\mu$.

**When $X_t = \mu$:** The drift is zero — no restoring force, only noise.

The strength of the restoring force scales with $\kappa$ (speed of mean reversion) and with the current deviation $|X_t - \mu|$. This is what distinguishes OU from Brownian motion (where drift is constant) and GBM (where drift is proportional to level, not deviation).

</details>

---

**Q2.** What is the half-life formula for an OU process? Compute the half-life when $\kappa = 0.5$. What does the half-life mean intuitively for a pairs trade?

<details>
<summary>Answer</summary>

$$t_{1/2} = \frac{\ln 2}{\kappa}$$

For $\kappa = 0.5$: $t_{1/2} = \ln 2 / 0.5 \approx 1.386$ time units.

**Derivation:** The conditional mean is $\mathbb{E}[X_t] = \mu + (X_0 - \mu)e^{-\kappa t}$. The gap $X_0 - \mu$ shrinks to half when $e^{-\kappa t} = 0.5$, i.e., $t = \ln 2 / \kappa$.

**For pairs trading:** if the time unit is years and $\kappa = 0.5$, the spread halves its deviation in about $1.4$ years. In days: if $\kappa = 0.5$ per year and one step = 1 day (252 steps/year), then $t_{1/2} \approx 1.4 \times 252 \approx 349$ days. This is *slow* — the trade takes almost a year to converge half-way, which implies high holding-period risk. A desirable pairs trade typically has $t_{1/2}$ of days to weeks, not years — meaning $\kappa$ must be much larger (e.g., $\kappa \sim 50-250$ on a per-year basis with daily data).

</details>

---

**Q3.** The OU process has an AR(1) discrete-time analog. Write the AR(1) regression equation and the mapping from AR(1) parameters to OU parameters. What condition on the AR(1) slope $b$ indicates mean reversion?

<details>
<summary>Answer</summary>

**AR(1) regression** (fit from data with step $\Delta t$):
$$X_{t+\Delta t} = a + b \cdot X_t + \varepsilon_t, \quad \varepsilon_t \sim \mathcal{N}(0, s^2)$$

**Mapping to OU parameters:**
$$\kappa = \frac{1 - b}{\Delta t}, \qquad \mu = \frac{a}{1 - b}, \qquad \sigma = \frac{s}{\sqrt{\Delta t}}$$

**Condition for mean reversion:** $|b| < 1$, equivalently $b \in (-1, 1)$.

- If $b \geq 1$: the AR(1) has a unit root or is explosive — random walk behavior, no mean reversion. The ADF test assesses this.
- If $b = 0$: no serial correlation — each step is independent, no memory.
- If $b < 0$: overshooting — the process crosses $\mu$ every step (strong mean reversion).
- The most common pairs trading regime: $b \in (0.9, 1.0)$, meaning slow, consistent pull toward $\mu$.

**How to fit:** run OLS on $X_{t+\Delta t}$ vs $X_t$, recover $a$, $b$, $s = \text{std}(\hat\varepsilon)$, then apply the mapping.

</details>

---

### Level 2 — Quantitative

**Q4.** OU process with $\kappa = 2$, $\mu = 0$, $\sigma = 1$, starting at $X_0 = 3$.

a) What is $\mathbb{E}[X_1]$?
b) What is $\text{Var}(X_1)$?
c) What is the stationary distribution as $t \to \infty$?

<details>
<summary>Answer</summary>

**a)** $\mathbb{E}[X_1] = \mu + (X_0 - \mu)e^{-\kappa \cdot 1} = 0 + 3 \cdot e^{-2} \approx 3 \times 0.1353 = 0.406$.

Starting 3 units above $\mu = 0$, after 1 time unit, the expected value is only 0.41 — the process has reverted 86% of the way back ($e^{-2} \approx 0.14$ of deviation remains).

**b)** $\text{Var}(X_1) = \frac{\sigma^2}{2\kappa}(1 - e^{-2\kappa \cdot 1}) = \frac{1}{4}(1 - e^{-4}) \approx \frac{1}{4}(1 - 0.018) \approx 0.245$.

Standard deviation $\approx 0.495$.

**c)** Stationary distribution: $X_\infty \sim \mathcal{N}\!\left(\mu,\ \frac{\sigma^2}{2\kappa}\right) = \mathcal{N}\!\left(0,\ \frac{1}{4}\right)$.

Standard deviation in stationarity $= 1/2 = 0.5$. The process forgets its initial condition $X_0 = 3$ and settles into this distribution — ergodic.

</details>

---

**Q5.** You fit an AR(1) to daily spread data ($\Delta t = 1/252$ year) and obtain: $b = 0.98$, $a = 0.0004$, $\text{std}(\hat\varepsilon) = 0.015$.

Compute: (a) $\kappa$, (b) $\mu$, (c) $\sigma$, (d) the half-life in **days**.

<details>
<summary>Answer</summary>

$\Delta t = 1/252$.

**a)** $\kappa = (1 - b)/\Delta t = (1 - 0.98)/(1/252) = 0.02 \times 252 = 5.04$ per year.

**b)** $\mu = a/(1 - b) = 0.0004 / 0.02 = 0.02$.

**c)** $\sigma = \text{std}(\hat\varepsilon)/\sqrt{\Delta t} = 0.015 / \sqrt{1/252} = 0.015 \times \sqrt{252} \approx 0.015 \times 15.87 \approx 0.238$ per year.

**d)** Half-life $= \ln 2 / \kappa = 0.693 / 5.04 \approx 0.138$ years $= 0.138 \times 252 \approx 34.7$ days.

A half-life of ~35 days is reasonable for a pairs trade — the spread takes about a month to converge halfway to equilibrium. Stationary vol $= \sigma/\sqrt{2\kappa} = 0.238/\sqrt{10.08} \approx 0.075$.

</details>

---

### Level 3 — Coding

**Q6.** The simulation uses the **exact conditional distribution** at each step rather than Euler-Maruyama. Why is exact simulation preferred for OU, and when would you be forced to use Euler-Maruyama?

<details>
<summary>Answer</summary>

**Why exact simulation is preferred for OU:**

The OU process is one of the rare SDEs with a known closed-form transition density:

$$X_{t+\Delta t} \mid X_t \sim \mathcal{N}\!\left(\mu + (X_t - \mu)e^{-\kappa\Delta t},\ \frac{\sigma^2}{2\kappa}(1 - e^{-2\kappa\Delta t})\right)$$

Exact simulation draws directly from this distribution at each step — it has **zero discretization error** regardless of $\Delta t$. You get the true distribution of $X_{t+\Delta t}$ given $X_t$ exactly.

Euler-Maruyama would approximate:
$$X_{t+\Delta t} \approx X_t + \kappa(\mu - X_t)\Delta t + \sigma\sqrt{\Delta t}\,Z$$

This is $O(\Delta t)$ accurate in the conditional mean and variance — for large $\Delta t$, it overestimates variance and introduces bias in the autocorrelation structure.

**When Euler-Maruyama is forced:**
- SDEs with nonlinear drift/diffusion (e.g., Heston: $dv = \kappa(\theta - v)dt + \xi\sqrt{v}\,dW$) — the $\sqrt{v}$ makes the transition density non-Gaussian, no exact form available.
- CIR/Heston variance: must use Euler-Maruyama or specialized schemes (Andersen's QE scheme) because Euler can produce negative variance values.
- Any SDE where $\mu(X, t)$ or $\sigma(X, t)$ is a general nonlinear function — exact simulation is generally unavailable.

**Rule:** always use exact simulation when available (GBM, OU/Vasicek). Fall back to Euler-Maruyama only when forced.

</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "OU process can't go negative" | It can — the solution is Gaussian, with support on all of $\mathbb{R}$. Unlike GBM (which is always positive), OU has symmetric tails. This is a known flaw for interest rate models: the Vasicek model (OU for rates) can produce negative rates. |
| "Higher $\kappa$ means higher stationary variance" | The opposite: stationary variance $= \sigma^2/(2\kappa)$ **decreases** with $\kappa$. Faster reversion keeps the process tightly around $\mu$. |
| "A mean-reverting spread guarantees pairs trading profits" | Mean reversion can break down (regime change, fundamental decoupling). Always validate with ADF test, check the half-life (must be short enough to profit before holding-period costs exceed the signal), and monitor for structural breaks. |
| "Fitting AR(1) and calling it OU is enough" | You also need stationarity testing (ADF), out-of-sample validation of $\kappa$ stability, and an understanding that the AR(1) mapping assumes constant parameters — which markets rarely provide. |

## Related Concepts

- [[Stochastic Differential Equations]] — OU is one of the few SDEs with an exact solution
- [[Brownian Motion]] — the noise driver $dW_t$
- [[Vasicek Model]] — OU process applied to interest rates
- [[Geometric Brownian Motion]] — the trending analog; contrast with OU
- [[Pairs Trading]] — the main direct application in equity stat arb
- [[Mean Reversion]] — the broader concept; OU is its continuous-time model
- [[Regime Detection]] — detecting when mean reversion breaks down
- [[Heston Model]] — variance process is a close cousin of OU

---

## Sources Used

- Hull, J.C. (2022). *Options, Futures, and Other Derivatives*, 11th ed. Ch. 14.
- Shreve, S.E. (2004). *Stochastic Calculus for Finance II*. Ch. 4. Springer.
- Uhlenbeck, G.E. and Ornstein, L.S. (1930). "On the Theory of the Brownian Motion." *Physical Review* 36(5), 823–841.
- Chan, E.P. (2013). *Algorithmic Trading: Winning Strategies and Their Rationale*. Wiley. Ch. 2 (pairs trading and OU fitting).

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | initial build |
| 2026-04-11 | QA review: status → evergreen; all sections verified correct | QA pass |
