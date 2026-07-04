---
type: concept
domain: 10-Foundations
tags: [math, stochastic-calculus]
status: evergreen
stability: stable
confidence: high
last_reviewed: 2026-04-11
review_interval_days: 365
sources:
  - "Shreve Vol II ch.4"
  - "Øksendal, Stochastic Differential Equations, 6th ed., ch.5"
  - "Glasserman, Monte Carlo Methods in Financial Engineering, ch.3"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Pricing → Gap 2: A general framework for all continuous-time models of prices, rates, and volatility
> **This concept:** Provides the unifying mathematical language — the grammar — for describing how any financial quantity evolves when subject to both predictable trends and continuous random shocks.
> **Alternative approaches to this gap:** none — SDEs are the framework, not a solution to be compared; GBM, OU, and all other specific models are instances of SDEs
> **You need first:** [[Brownian Motion]], [[Ito's Lemma]]
> **This unlocks:** [[Geometric Brownian Motion]], [[Ornstein-Uhlenbeck Process]], [[Girsanov Theorem]], [[Risk-Neutral Measure]], [[Monte Carlo Methods]]

## Why This Exists

**The gap:** Individual models like GBM and the Vasicek rate model look structurally similar — both have a drift term and a diffusion term. Practitioners needed a unified framework that could describe all such models, state conditions for when they have solutions, and provide tools for working with them systematically.

**What came before:** Isolated model-by-model specifications. GBM was defined on its own; mean-reverting rate models were derived separately. There was no common language linking them, no general existence/uniqueness theory, and no framework for moving between models or extending them (e.g., to multi-dimensional or stochastic-vol settings).

**What this adds:** The general Ito SDE $dX_t = \mu(X_t, t)\,dt + \sigma(X_t, t)\,dW_t$ covers all the specific models as special cases by plugging in different drift and diffusion functions. It comes with existence/uniqueness conditions (Lipschitz + linear growth), a canonical numerical method (Euler-Maruyama), and the Ito calculus machinery (Ito's Lemma, Girsanov) that applies uniformly across all instances.

**What it still doesn't solve:** Most SDEs — including Heston and SABR — have no closed-form solution. Solving or simulating them requires numerical methods (Euler-Maruyama, higher-order schemes) and, for pricing, the risk-neutral measure machinery. See [[Numerical Methods PDE]] and [[Monte Carlo Methods]].

## Math Concepts

**General form.** An Ito SDE for a scalar process $X_t$ is written

$$
dX_t = \mu(X_t, t) \, dt + \sigma(X_t, t) \, dW_t,
$$

where:
- $\mu(X_t, t)$: **drift** coefficient — the predictable, infinitesimal expected change per unit time.
- $\sigma(X_t, t)$: **diffusion** coefficient — the magnitude of random shocks per unit of $\sqrt{dt}$.
- $dW_t$: increment of a standard Brownian motion; $dW_t \sim N(0, dt)$ heuristically.

The integral form (more rigorous) is:

$$
X_t = X_0 + \int_0^t \mu(X_s, s) \, ds + \int_0^t \sigma(X_s, s) \, dW_s.
$$

The second integral is an Ito stochastic integral — it is not a Riemann integral and requires Ito's lemma to manipulate.

**Existence and uniqueness.** If $\mu$ and $\sigma$ satisfy global Lipschitz and linear growth conditions:

$$
|\mu(x,t) - \mu(y,t)| + |\sigma(x,t) - \sigma(y,t)| \le K|x-y|,
$$

$$
|\mu(x,t)|^2 + |\sigma(x,t)|^2 \le K^2(1 + |x|^2),
$$

then the SDE has a unique strong solution adapted to the natural filtration of $W$.

---

**Key models in finance.**

**1. Geometric Brownian Motion (GBM).** The Black-Scholes stock price model:

$$
dS_t = \mu S_t \, dt + \sigma S_t \, dW_t.
$$

Here drift and diffusion scale proportionally with $S_t$ — percentage returns are i.i.d. Closed-form solution via Ito's lemma:

$$
S_t = S_0 \exp\!\left(\left(\mu - \tfrac{1}{2}\sigma^2\right)t + \sigma W_t\right).
$$

Note the $-\frac{1}{2}\sigma^2$ Ito correction: it arises because $d(\ln S) \ne dS/S$ when $S$ is stochastic.

**2. Vasicek model (mean-reverting interest rates):**

$$
dr_t = a(b - r_t) \, dt + \sigma \, dW_t.
$$

- $a > 0$: speed of mean reversion — how fast rates snap back.
- $b$: long-run mean level.
- $\sigma$: constant volatility.

This is an Ornstein-Uhlenbeck process. Closed-form solution:

$$
r_t = b + (r_0 - b)e^{-at} + \sigma \int_0^t e^{-a(t-s)} \, dW_s.
$$

$r_t$ is Gaussian (can go negative — a known limitation).

**3. Heston stochastic volatility model:**

$$
dS_t = \mu S_t \, dt + \sqrt{v_t} S_t \, dW_t^S,
$$
$$
dv_t = \kappa(\theta - v_t) \, dt + \xi \sqrt{v_t} \, dW_t^v, \quad d\langle W^S, W^v \rangle_t = \rho \, dt.
$$

- $v_t$: instantaneous variance (a CIR process).
- $\kappa$: mean-reversion speed of variance.
- $\theta$: long-run variance.
- $\xi$: volatility of volatility ("vol of vol").
- $\rho$: correlation between asset returns and variance shocks (typically $\rho < 0$ — leverage effect).

No closed-form path solution; semi-analytic characteristic function exists for option pricing.

**Ito's Lemma (the chain rule for SDEs).** For a smooth function $f(X_t, t)$ where $X_t$ satisfies the SDE above:

$$
df = \left(\frac{\partial f}{\partial t} + \mu \frac{\partial f}{\partial x} + \frac{1}{2}\sigma^2 \frac{\partial^2 f}{\partial x^2}\right)dt + \sigma \frac{\partial f}{\partial x} \, dW_t.
$$

The extra $\frac{1}{2}\sigma^2 \frac{\partial^2 f}{\partial x^2}$ term (the Ito correction) has no analog in ordinary calculus — it arises because $(dW_t)^2 = dt$ stochastically.

**Euler-Maruyama discretization.** For a time grid $0 = t_0 < t_1 < \cdots < t_N = T$ with step $\Delta t$:

$$
X_{t_{k+1}} \approx X_{t_k} + \mu(X_{t_k}, t_k)\,\Delta t + \sigma(X_{t_k}, t_k)\,\Delta W_k,
$$

where $\Delta W_k = W_{t_{k+1}} - W_{t_k} \sim N(0, \Delta t)$. This is a strong order 0.5 scheme (errors $\sim O(\sqrt{\Delta t})$).

## Walkthrough

**GBM step by step.**

Given $dS_t = \mu S_t \, dt + \sigma S_t \, dW_t$ with $S_0 = 100$, $\mu = 0.10$, $\sigma = 0.20$, $T = 1$ year.

*Step 1 — apply Ito's lemma to $f(S) = \ln S$:*

$$
d(\ln S_t) = \frac{1}{S_t}dS_t - \frac{1}{2}\frac{1}{S_t^2}(dS_t)^2
= \left(\mu - \tfrac{1}{2}\sigma^2\right)dt + \sigma\,dW_t.
$$

*Step 2 — integrate both sides:*

$$
\ln S_T - \ln S_0 = \left(\mu - \tfrac{1}{2}\sigma^2\right)T + \sigma W_T.
$$

*Step 3 — exponentiate:*

$$
S_T = 100 \cdot \exp\!\left((0.10 - 0.02) \times 1 + 0.20 \times W_1\right)
= 100 \cdot \exp(0.08 + 0.20 \, W_1).
$$

Since $W_1 \sim N(0,1)$, we have $\ln(S_T/S_0) \sim N(0.08, 0.04)$: log-returns are normally distributed with mean 8% and std 20%.

*Verification:* $E[S_T] = S_0 e^{\mu T} = 100 e^{0.10} \approx 110.52$. The $-\frac{1}{2}\sigma^2$ shift ensures this is consistent.

## Analysis

**Key properties.**
- GBM ensures $S_t > 0$ always (prices can't go negative), because the solution is an exponential.
- Vasicek allows negative rates — it is Gaussian. The CIR model ($dr = a(b-r)dt + \sigma\sqrt{r}\,dW$) keeps rates non-negative by the Feller condition $2ab \ge \sigma^2$.
- Euler-Maruyama is simple but can drift negative for models requiring positivity (e.g., CIR, Heston variance). The Milstein scheme (order 1.0) adds a correction term $\frac{1}{2}\sigma\sigma'(\Delta W^2 - \Delta t)$.

**Ito vs Stratonovich.** Ito integration evaluates the integrand at the *left* endpoint of each interval; Stratonovich uses the midpoint. Physics often uses Stratonovich (chain rule works normally); finance uses Ito (no look-ahead bias, martingale property preserved).

**Common confusions.**
- "$dX_t = \mu \, dt + \sigma \, dW_t$" looks like a derivative but $W_t$ is nowhere differentiable. The equation is shorthand for the integral form — the $dt$ and $dW_t$ are formal symbols governed by Ito calculus rules, not ordinary differentials.
- The Ito correction $-\frac{1}{2}\sigma^2 t$ in GBM is often forgotten: the *expected* log-return is $(\mu - \frac{1}{2}\sigma^2)T$, not $\mu T$. Missing this is a classic Monte Carlo bug.
- "Solving an SDE" means finding $X_t$ as an explicit function of $t$ and $W_t$. Most SDEs (e.g., Heston) have no such closed form and must be simulated numerically.

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)

# ── Parameters ─────────────────────────────────────────────────────────────
S0    = 100.0
mu    = 0.10
sigma = 0.20
T     = 1.0
n_steps = 252          # daily steps
n_paths = 1000
dt    = T / n_steps

# ── 1. Geometric Brownian Motion — Euler-Maruyama ──────────────────────────
dW = rng.normal(0, np.sqrt(dt), size=(n_paths, n_steps))

S_em = np.zeros((n_paths, n_steps + 1))
S_em[:, 0] = S0
for k in range(n_steps):
    S_em[:, k+1] = (S_em[:, k]
                    + mu    * S_em[:, k] * dt          # drift
                    + sigma * S_em[:, k] * dW[:, k])   # diffusion

# ── 2. GBM exact solution (for comparison) ────────────────────────────────
t_grid = np.linspace(0, T, n_steps + 1)
W_cumsum = np.hstack([np.zeros((n_paths, 1)), dW.cumsum(axis=1)])
S_exact = S0 * np.exp((mu - 0.5 * sigma**2) * t_grid + sigma * W_cumsum)

# ── Compare terminal distributions ─────────────────────────────────────────
print("GBM terminal price comparison:")
print(f"  Euler-Maruyama:  mean={S_em[:, -1].mean():.2f}, std={S_em[:, -1].std():.2f}")
print(f"  Exact:           mean={S_exact[:, -1].mean():.2f}, std={S_exact[:, -1].std():.2f}")
print(f"  Theory E[S_T]:   {S0 * np.exp(mu * T):.2f}")

# ── Plot sample paths ──────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 4))

for path in S_exact[:10]:
    axes[0].plot(t_grid, path, alpha=0.6, linewidth=0.8)
axes[0].set_title("GBM — 10 sample paths (exact solution)")
axes[0].set_xlabel("Time (years)")
axes[0].set_ylabel("$S_t$")

axes[1].hist(S_exact[:, -1], bins=60, density=True, color="steelblue", alpha=0.7, label="Simulated")
axes[1].axvline(S0 * np.exp(mu * T), color="black", linestyle="--", label=f"E[S_T]={S0*np.exp(mu*T):.1f}")
axes[1].set_title("Terminal distribution of $S_T$ (GBM)")
axes[1].set_xlabel("$S_T$")
axes[1].legend()
plt.tight_layout()
plt.show()

# ── 3. Vasicek (Ornstein-Uhlenbeck) mean-reverting rates ──────────────────
a     = 2.0    # mean-reversion speed
b     = 0.05   # long-run mean (5%)
sig_r = 0.01   # rate volatility
r0    = 0.08   # start above long-run mean

r = np.zeros((n_paths, n_steps + 1))
r[:, 0] = r0
dW_r = rng.normal(0, np.sqrt(dt), size=(n_paths, n_steps))
for k in range(n_steps):
    r[:, k+1] = (r[:, k]
                 + a * (b - r[:, k]) * dt    # mean-reversion drift
                 + sig_r * dW_r[:, k])       # diffusion

print(f"\nVasicek — terminal rate stats:")
print(f"  Mean = {r[:, -1].mean():.4f}  (theory long-run = {b:.4f})")
print(f"  Std  = {r[:, -1].std():.4f}  (theory = {sig_r * np.sqrt(1 / (2*a)):.4f})")

plt.figure(figsize=(10, 4))
for path in r[:5]:
    plt.plot(t_grid, path * 100, alpha=0.7, linewidth=0.8)
plt.axhline(b * 100, color="black", linestyle="--", linewidth=1.2, label=f"Long-run mean = {b*100:.0f}%")
plt.title("Vasicek model — 5 rate paths")
plt.xlabel("Time (years)")
plt.ylabel("Rate (%)")
plt.legend()
plt.tight_layout()
plt.show()

# ── 4. Euler-Maruyama convergence: effect of step size ────────────────────
# True GBM terminal mean for reference
true_mean = S0 * np.exp(mu * T)
step_sizes = [1, 4, 12, 52, 252]
errors = []
n_conv = 50_000

for steps in step_sizes:
    dt_k = T / steps
    dW_k = rng.normal(0, np.sqrt(dt_k), size=(n_conv, steps))
    S_k = np.zeros((n_conv, steps + 1))
    S_k[:, 0] = S0
    for i in range(steps):
        S_k[:, i+1] = S_k[:, i] + mu * S_k[:, i] * dt_k + sigma * S_k[:, i] * dW_k[:, i]
    errors.append(abs(S_k[:, -1].mean() - true_mean))

print("\nEuler-Maruyama convergence (weak error on E[S_T]):")
for steps, err in zip(step_sizes, errors):
    print(f"  n_steps={steps:3d}, dt={T/steps:.4f}: |error| = {err:.4f}")
```

## Bridge to Quant / ML

**Derivatives pricing.** Every closed-form option pricing formula (Black-Scholes, Bachelier, displaced diffusion) is derived by solving the SDE for the underlying and computing $e^{-rT}E^Q[\text{payoff}]$. When no closed form exists (Heston, SABR), Monte Carlo simulation of the SDE is the pricing engine.

**Risk management / scenario generation.** Risk systems simulate thousands of SDE paths for assets, rates, and spreads to estimate VaR, CVA, and stress P&L. The accuracy of the Euler-Maruyama discretization directly affects P&L reliability.

**Calibration.** Model parameters $(\mu, \sigma, \kappa, \theta, \ldots)$ are estimated by fitting the SDE's implied option prices or time-series moments to market data. Maximum likelihood for SDEs (e.g., Vasicek) involves the transition density; for complex SDEs, particle filters or neural SDE approaches approximate it.

**Neural SDEs (ML frontier).** A neural SDE replaces $\mu(\cdot)$ and $\sigma(\cdot)$ with neural networks, learned end-to-end from data. This enables latent-variable generative models for time series that respect the continuous-time SDE structure and can be calibrated to option surface data. Frameworks: `torchsde`, `diffrax`.

**Reinforcement Learning.** Continuous-time RL problems (e.g., optimal execution, portfolio optimization) are formulated as controlled SDEs: $dX_t = \mu(X_t, u_t, t)\,dt + \sigma(X_t, t)\,dW_t$ where $u_t$ is the control. Hamilton-Jacobi-Bellman (HJB) equations extend the SDE to find optimal policies — the continuous-time analog of Bellman equations.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** In the SDE $dX_t = \mu(X_t, t)\,dt + \sigma(X_t, t)\,dW_t$, what is the role of the drift $\mu$ versus the diffusion $\sigma$? Give a concrete financial interpretation for both in the GBM case.

<details>
<summary>Answer</summary>

**Drift $\mu(X_t, t)\,dt$:** the predictable, deterministic component of the change. Over a small interval $dt$, the process is expected to move by $\mu\,dt$ regardless of any randomness. It's the "trend."

**Diffusion $\sigma(X_t, t)\,dW_t$:** the random component, with magnitude $\sigma$ scaled by a Brownian increment $dW_t \sim \mathcal{N}(0, dt)$. It injects continuous random noise of size $\sim \sigma\sqrt{dt}$ per step.

**For GBM** $dS_t = \mu S_t\,dt + \sigma S_t\,dW_t$:
- $\mu S_t\,dt$ — the stock is expected to earn a return of $\mu\,dt$ over the next instant, proportional to its current price. $\mu$ is the annualized expected return (drift). A $\$100$ stock with $\mu = 10\%$ expects to earn $\$10/\text{yr}$ in drift.
- $\sigma S_t\,dW_t$ — random return shock of magnitude $\sigma\,dW_t$ (annualized volatility $\sigma$). A $20\%$ volatility stock gets shocks of size $\pm 20\% \times \sqrt{dt}$ per unit time, scaled to the current price. A $\$200$ stock gets twice the dollar-shock of a $\$100$ stock at the same $\sigma$.

The $S_t$ multiplier on both terms makes the SDE scale-free — it's about proportional returns, not absolute dollar moves.

</details>

---

**Q2.** GBM has the solution $S_t = S_0\exp\!\left[(\mu - \frac{\sigma^2}{2})t + \sigma W_t\right]$. Why is there a $-\frac{\sigma^2}{2}$ correction? Where does it come from?

<details>
<summary>Answer</summary>

The $-\frac{\sigma^2}{2}$ comes from **Ito's Lemma** applied to $f(S) = \ln S$.

In ordinary calculus, $d(\ln S) = dS/S$. But for a stochastic process, the chain rule picks up a second-order correction because $(dW_t)^2 = dt \neq 0$:

$$d(\ln S_t) = \frac{1}{S_t}dS_t - \frac{1}{2}\frac{1}{S_t^2}(dS_t)^2 = (\mu - \tfrac{\sigma^2}{2})\,dt + \sigma\,dW_t$$

The $-\frac{1}{2S^2}(dS)^2$ term gives $-\frac{1}{2}\sigma^2\,dt$ — the Ito correction.

**Why it matters:** if you ignored it and wrote $S_t = S_0 e^{\mu t + \sigma W_t}$, then $\mathbb{E}[S_t] = S_0 e^{(\mu + \sigma^2/2)t}$ — the stock would appear to earn more than $\mu$ per year. The $-\sigma^2/2$ correction ensures that $\mathbb{E}[S_t] = S_0 e^{\mu t}$ as the model intends. The median growth rate is $\mu - \sigma^2/2$ (below the mean) — Jensen's inequality for the lognormal distribution.

**Practical impact:** forgetting this correction in Monte Carlo simulation gives a systematically biased estimate of expected payoffs.

</details>

---

**Q3.** What makes the Heston model fundamentally different from GBM as a stochastic system? What does the correlation parameter $\rho$ capture?

<details>
<summary>Answer</summary>

**Structural difference:** GBM is a **one-dimensional** SDE — one source of randomness ($dW_t$), one state variable ($S_t$), constant parameters. Heston is a **two-dimensional coupled SDE system** — two state variables ($S_t$ and $v_t$) driven by two correlated Brownian motions ($dW_t^S$ and $dW_t^v$).

In GBM, $\sigma$ is constant — volatility is fixed forever. In Heston, $v_t$ (instantaneous variance) is itself stochastic, following a CIR process:
$$dv_t = \kappa(\theta - v_t)\,dt + \xi\sqrt{v_t}\,dW_t^v$$

This means the *future volatility distribution* is uncertain — a key real-world feature GBM can't capture. Heston generates a **volatility smile** (non-flat implied vol surface) because the stochastic vol produces fat tails in returns.

**The role of $\rho$:** $d\langle W^S, W^v\rangle_t = \rho\,dt$ is the instantaneous correlation between asset returns and variance shocks. Empirically, $\rho < 0$ (the "leverage effect"): when the stock falls, volatility tends to spike. This produces a downward-sloping implied vol skew — puts are more expensive than calls, as observed in equity markets. If $\rho = 0$, the model has symmetric implied vol; $\rho < 0$ tilts it leftward.

</details>

---

### Level 2 — Quantitative

**Q4.** GBM with $S_0 = 100$, $\mu = 0.10$, $\sigma = 0.20$, $T = 1$ year.

a) Compute $\mathbb{E}[S_T]$.
b) What is the distribution of $\ln(S_T / S_0)$?
c) Compute $P(S_T > 120)$.

<details>
<summary>Answer</summary>

**a)** $\mathbb{E}[S_T] = S_0 e^{\mu T} = 100 \cdot e^{0.10} \approx \$110.52$.

**b)** $\ln(S_T/S_0) \sim \mathcal{N}\!\left((\mu - \tfrac{\sigma^2}{2})T,\ \sigma^2 T\right) = \mathcal{N}(0.08,\ 0.04)$

Mean log-return $= 0.10 - 0.02 = 0.08$; standard deviation $= 0.20$.

**c)** $P(S_T > 120) = P(\ln(S_T/100) > \ln 1.2) = P\!\left(Z > \frac{0.1823 - 0.08}{0.20}\right) = P(Z > 0.512)$

$= 1 - \Phi(0.512) \approx 1 - 0.696 = 30.4\%$

**Sanity check:** with $\mathbb{E}[S_T] \approx \$110.52$, a probability of ~30% above $\$120$ is reasonable — about 1 standard deviation in log space above the mean.

</details>

---

**Q5.** Euler-Maruyama has **strong order 0.5** convergence — errors scale as $O(\sqrt{\Delta t})$.

a) If you halve $\Delta t$ (double the number of steps), by what factor does the strong error reduce?
b) To halve the strong error, how many times more steps do you need?
c) Compare this to the Crank-Nicolson FDM scheme for the BSM PDE (order 2 in $\Delta t$). To halve CN's error, how many more time steps?

<details>
<summary>Answer</summary>

**a)** Strong error $\sim C\sqrt{\Delta t}$. Halving $\Delta t$: new error $\sim C\sqrt{\Delta t/2} = C\sqrt{\Delta t}/\sqrt{2}$. The error reduces by factor $1/\sqrt{2} \approx 0.707$ — about 30% reduction.

**b)** To halve the error: $C\sqrt{\Delta t'} = \frac{1}{2} C\sqrt{\Delta t}$. So $\Delta t' = \Delta t/4$. You need **4× more steps** (quadruple the computation) to halve the error.

**c)** Crank-Nicolson: error $\sim C'(\Delta t)^2$. To halve: $C'(\Delta t')^2 = \frac{1}{2}C'(\Delta t)^2$, so $\Delta t' = \Delta t/\sqrt{2}$. You need $\sqrt{2} \approx 1.41\times$ more steps — much cheaper. CN is dramatically more efficient per unit of accuracy improvement.

**Summary:** Euler-Maruyama is wasteful for accuracy improvements; it's used when no better scheme exists (complex nonlinear SDEs). For GBM, always use the exact solution. For linear SDEs like Vasicek, use exact simulation.

</details>

---

### Level 3 — Coding

**Q6.** The code compares Euler-Maruyama and exact GBM simulation. For a **CIR model** $dr_t = a(b - r_t)\,dt + \sigma\sqrt{r_t}\,dW_t$ (used for interest rates and Heston variance), what numerical problem can Euler-Maruyama produce, and how is it typically addressed?

<details>
<summary>Answer</summary>

**The problem:** Euler-Maruyama for CIR discretizes as:
$$r_{t+\Delta t} \approx r_t + a(b - r_t)\Delta t + \sigma\sqrt{r_t}\,\Delta W_t$$

If $r_t$ is small and $\Delta W_t$ is a large negative draw, $r_{t+\Delta t}$ can go **negative** — but the CIR model requires $r_t \geq 0$ (it models rates or variance, which must be non-negative). A negative $r_t$ makes $\sqrt{r_t}$ imaginary — the simulation crashes.

**Solutions:**

1. **Absorption:** $r_{t+\Delta t} = \max(r_{t+\Delta t}^{\text{EM}},\ 0)$ — truncate negatives to zero. Simple but introduces bias.

2. **Reflection:** $r_{t+\Delta t} = |r_{t+\Delta t}^{\text{EM}}|$ — reflect at zero. Slightly less biased.

3. **Andersen's QE (Quadratic-Exponential) scheme** — matches the first two moments of the true CIR transition distribution using a mixture of a displaced chi-squared and an exponential. Most accurate and used in production Heston pricers.

4. **Log-transform:** simulate $\ln r_t$ using Ito's Lemma, then exponentiate. The log is always real, but the SDE for $\ln r$ picks up a correction term.

**Feller condition:** if $2ab \geq \sigma^2$, the CIR process never hits zero under the true dynamics. But Euler-Maruyama can still violate this with finite $\Delta t$ even when the condition holds.

```python
# Simple fix: absorption
r_next = r + a * (b - r) * dt + sigma * np.sqrt(np.maximum(r, 0)) * dW
r_next = np.maximum(r_next, 0)  # prevent negative values
```

</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "$dX_t$ is a derivative of $X_t$ with respect to $t$" | $W_t$ is nowhere differentiable, so $dX_t$ cannot be a classical derivative. The SDE notation $dX_t = \ldots$ is shorthand for the integral form $X_t = X_0 + \int_0^t \mu\,ds + \int_0^t \sigma\,dW_s$, where the second integral is an Ito stochastic integral. |
| "Every SDE has a closed-form solution" | GBM and Vasicek/OU are exceptions. Most SDEs (Heston, SABR, CIR in multi-factor settings) have no closed-form path solution and require numerical methods (Monte Carlo, FDM). |
| "The Ito correction $-\sigma^2/2$ is small and can be ignored" | It's $O(dt)$ — exactly the same order as the drift. Ignoring it changes the mean log-return by $-\sigma^2/2$ per year. For $\sigma = 30\%$, that's a $4.5\%/\text{yr}$ systematic error — enormous in any pricing or risk application. |
| "Euler-Maruyama with small enough $\Delta t$ is always accurate" | For SDEs with positivity constraints (CIR, Heston variance), Euler-Maruyama can produce negative values regardless of $\Delta t$. Structural schemes (QE, log-transform) are needed. |

## Related Concepts

- [[Brownian Motion]]
- [[Ito's Lemma]]
- [[Martingales]]
- [[Girsanov Theorem]]
- [[Black-Scholes Model]]
- [[Vasicek Model]]
- [[Heston Model]]
- [[Monte Carlo Methods]]
- [[Risk-Neutral Measure]]

## Sources Used

- Shreve, *Stochastic Calculus for Finance II*, Ch. 4 (stochastic differential equations)
- Øksendal, *Stochastic Differential Equations*, 6th ed., Ch. 5
- Glasserman, *Monte Carlo Methods in Financial Engineering*, Ch. 3 (discretization schemes)

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review: status → evergreen; [[Ito Calculus]] → [[Ito's Lemma]]; sources frontmatter expanded; last_reviewed updated | QA pass |
