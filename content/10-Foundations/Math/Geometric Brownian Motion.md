---
type: concept
domain: 10-Foundations
tags: [math, stochastic-calculus, models]
status: evergreen
stability: stable
confidence: high
last_reviewed: 2026-04-11
review_interval_days: 365
sources:
  - "Hull ch.14"
  - "Shreve Vol II ch.1"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Pricing → Gap 2: To build the replicating portfolio, you need a model for how prices move
> **This concept:** Transforms raw Brownian motion into a model specifically suited for asset prices — positive, with proportional moves and lognormal returns.
> **Alternative approaches to this gap:** [[Stochastic Differential Equations]] (general framework); [[Ornstein-Uhlenbeck Process]] (for mean-reverting quantities like rates and spreads)
> **You need first:** [[Brownian Motion]], [[Ito's Lemma]] (to solve the GBM SDE and derive its closed form)
> **This unlocks:** [[Black-Scholes Model]], [[Heston Model]], [[Implied Volatility]], [[Volatility Smile]]

## Why This Exists

**The gap:** Once replication was established as the right pricing principle, practitioners needed an explicit mathematical model for how stock prices move. Plain Brownian motion fails: it allows negative prices and makes absolute (not proportional) moves — a \$10 fluctuation means something completely different at \$10 vs \$200.

**What came before:** Arithmetic Brownian motion (Bachelier, 1900) — adding noise directly to price levels. This allowed negative prices, made percentage volatility shrink as prices rose, and produced symmetric rather than skewed return distributions. It was the first attempt but wrong for equities.

**What this adds:** By multiplying the noise term by the current price level ($\sigma S_t\, dW_t$), GBM makes moves proportional to price. This gives three things simultaneously: prices always stay positive (they are an exponential), log-returns are normally distributed (roughly matching empirical data at short horizons), and a single volatility parameter $\sigma$ governs the percentage uncertainty regardless of price level.

**What it still doesn't solve:** GBM assumes $\sigma$ is constant. Real option markets show that different strikes and maturities imply different volatilities — the volatility smile. This is Gap 5 in the Pricing chain, addressed by [[Local Volatility]], [[Heston Model]], and [[Merton Jump-Diffusion]].

## Math Concepts

GBM is the SDE:

$$dS_t = \mu S_t \, dt + \sigma S_t \, dW_t$$

where:
- $S_t$ — asset price at time $t$
- $\mu$ — drift (expected return per unit time)
- $\sigma$ — volatility (standard deviation of returns per $\sqrt{\text{time}}$)
- $W_t$ — standard [[Brownian Motion]]

The $S_t$ multiplier on both terms means moves are *proportional* to the current price level.

**Closed-form solution** — applying [[Ito's Lemma]] to $f(S_t) = \ln S_t$:

$$S_t = S_0 \exp\!\left[\left(\mu - \frac{\sigma^2}{2}\right)t + \sigma W_t\right]$$

So $\ln S_t \sim \mathcal{N}\!\left(\ln S_0 + \left(\mu - \frac{\sigma^2}{2}\right)t,\ \sigma^2 t\right)$ — log-prices are normally distributed, prices are lognormal.

**The $-\frac{\sigma^2}{2}$ Ito correction:** Jensen's inequality means $\mathbb{E}[\ln S_t] \neq \ln \mathbb{E}[S_t]$. The drift of the log is $\mu - \frac{\sigma^2}{2}$, not $\mu$. This correction appears throughout derivatives pricing.

## Walkthrough

Starting from $S_0 = 100$, $\mu = 0.05$, $\sigma = 0.2$, $T = 1$ year:

1. Draw $Z \sim \mathcal{N}(0, 1)$
2. Compute $S_T = 100 \cdot \exp\!\left[(0.05 - 0.02) \cdot 1 + 0.2 \cdot Z\right]$
   $= 100 \cdot \exp(0.03 + 0.2 Z)$
3. $\mathbb{E}[S_T] = 100 \cdot e^{0.05} \approx 105.13$ (expected price grows at $\mu$)
4. Median $S_T = 100 \cdot e^{0.03} \approx 103.05$ (median grows at $\mu - \sigma^2/2$)

The gap between mean and median comes from the lognormal skew — a direct consequence of the Ito correction.

## Analysis

- **Constant $\sigma$ assumption:** GBM implies a flat volatility surface. Real markets show a [[Volatility Smile]] — the main failure of the model.
- **Normal log-returns:** empirical returns have fat tails and skew. GBM underestimates tail risk.
- **No mean reversion:** GBM drifts forever. Interest rates and volatility are mean-reverting — GBM is wrong for them (see [[Vasicek Model]], [[Heston Model]]).
- **Continuous paths:** GBM has no jumps. Markets do (earnings, crises). Jump-diffusion models extend GBM.

Despite these failures, GBM is the *starting point* for all derivatives pricing because it gives tractable closed forms.

## Implementation

```python
import numpy as np

def simulate_gbm(S0=100, mu=0.05, sigma=0.2, T=1.0, N=252, n_paths=1000, seed=42):
    """Simulate GBM paths using the exact solution."""
    rng = np.random.default_rng(seed)
    dt = T / N
    t = np.linspace(0, T, N + 1)
    # Exact solution: avoids discretization error
    Z = rng.standard_normal((n_paths, N))
    log_returns = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
    log_paths = np.concatenate(
        [np.zeros((n_paths, 1)), np.cumsum(log_returns, axis=1)], axis=1
    )
    return t, S0 * np.exp(log_paths)
```

Note: use the exact solution (not Euler-Maruyama) for GBM since it's available — no discretization error.

## Bridge to Quant / ML

- GBM is the price process assumed in [[Black-Scholes Model]] — understanding GBM is *required* before BSM makes sense
- The lognormal distribution of $S_T$ is what makes the BSM integral tractable
- In ML finance: GBM is a benchmark data-generating process for alpha factor testing — if your signal works on GBM data, it's spurious
- [[Regime Detection]] often aims to detect when real data departs from GBM behavior (jumps, clustering)

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** GBM is defined as $dS_t = \mu S_t\,dt + \sigma S_t\,dW_t$. Why does the $S_t$ multiplier appear in *both* the drift and diffusion terms — what does this mean economically?

<details>
<summary>Answer</summary>

The $S_t$ multiplier means that *returns* (not price levels) are the fundamental quantity, not absolute moves. A \$10 move is huge for a \$50 stock (20% return) but negligible for a \$1000 stock (1% return).

- **Drift:** $\mu S_t\,dt$ means the stock earns an expected return of $\mu\,dt$ per unit time, proportional to its current level. This is how compound interest works.
- **Diffusion:** $\sigma S_t\,dW_t$ means the random shock is also proportional to price — a 20% vol stock has larger dollar swings when it's at \$200 than when it's at \$50.

Mathematically, this makes the SDE *scale-invariant*: if you multiply $S_0$ by a constant, the entire path scales by the same constant. The log-returns $d(\ln S)$ are independent of the price level.

</details>

---

**Q2.** What is the Ito correction term $-\frac{\sigma^2}{2}$ in the GBM solution, and why does it appear? Without it, what would be wrong?

<details>
<summary>Answer</summary>

The GBM solution is $S_t = S_0 \exp\!\left[(\mu - \frac{\sigma^2}{2})t + \sigma W_t\right]$. The $-\frac{\sigma^2}{2}$ is the **Ito correction**.

**Why it appears:** Applying Ito's Lemma to $f(S) = \ln S$ gives a correction term $\frac{1}{2} \cdot (-\frac{1}{S^2}) \cdot \sigma^2 S^2\,dt = -\frac{\sigma^2}{2}\,dt$. In ordinary calculus, $d(\ln S) = dS/S$ exactly. In stochastic calculus, a second-order correction survives because $(dS)^2 \neq 0$.

**Without it:** If you wrote $S_t = S_0 e^{\mu t + \sigma W_t}$ (no correction), then $E[S_t] = S_0 e^{(\mu + \frac{\sigma^2}{2})t}$ — the stock would appear to earn more than $\mu$ on average, which violates the model's assumptions. The correction ensures $E[S_t] = S_0 e^{\mu t}$ as intended. The median return is $(\mu - \frac{\sigma^2}{2})t$, less than the mean — this is Jensen's inequality: $E[e^X] > e^{E[X]}$ for a random variable $X$.

</details>

---

**Q3.** Why is GBM unsuitable for modeling interest rates, but suitable for equity prices?

<details>
<summary>Answer</summary>

**Equity prices — GBM works because:**
- Prices must stay positive — GBM solution is an exponential, always positive ✓
- Returns (not levels) being normally distributed is empirically reasonable for short horizons
- No natural "equilibrium" — a stock can drift upward indefinitely ✓

**Interest rates — GBM fails because:**
- Rates are mean-reverting: if rates hit 15%, central banks cut; if they hit 0%, they raise. GBM has no mean reversion — it drifts without bound
- Very high/low rates have economic restoring forces that GBM ignores
- GBM allows explosive growth or collapse to zero — neither makes sense for rates

The [[Vasicek Model]] and [[Hull-White Model]] use Ornstein-Uhlenbeck processes instead, which explicitly model mean reversion toward a long-run equilibrium rate.

</details>

---

### Level 2 — Quantitative

**Q4.** A stock has $S_0 = 100$, $\mu = 0.08$, $\sigma = 0.25$, $T = 2$ years.

a) What is the distribution of $\ln(S_2/S_0)$?
b) What is $E[S_2]$?
c) What is the median of $S_2$?
d) What is $P(S_2 > 120)$?

<details>
<summary>Answer</summary>

**a)** $\ln(S_T/S_0) \sim \mathcal{N}\!\left((\mu - \frac{\sigma^2}{2})T,\ \sigma^2 T\right) = \mathcal{N}((0.08 - 0.03125)\times2,\ 0.0625\times2)$

$$= \mathcal{N}(0.0975,\ 0.125)$$

Std dev of log-return = $\sqrt{0.125} = 0.354$.

**b)** $E[S_2] = S_0 e^{\mu T} = 100 \cdot e^{0.16} \approx 100 \times 1.1735 = \$117.35$.

**c)** Median $= S_0 \cdot e^{(\mu - \sigma^2/2)T} = 100 \cdot e^{0.0975} \approx 100 \times 1.1024 = \$110.24$.

The mean exceeds the median — lognormal distributions are right-skewed (a few very large outcomes pull the mean up).

**d)** $P(S_2 > 120) = P(\ln(S_2/100) > \ln(1.2)) = P\!\left(Z > \frac{0.1823 - 0.0975}{0.354}\right) = P(Z > 0.240) \approx 1 - 0.595 = 40.5\%$.

</details>

---

**Q5.** Two stocks both have $\sigma = 0.30$. Stock A has $\mu_A = 0.10$ and Stock B has $\mu_B = 0.20$. After 10 years, which stock has a higher *median* value? Which has a higher *mean* value?

<details>
<summary>Answer</summary>

**Median** $= S_0 \cdot e^{(\mu - \sigma^2/2)T}$:
- Stock A: $e^{(0.10 - 0.045)\times10} = e^{0.55} \approx 1.73\times S_0$
- Stock B: $e^{(0.20 - 0.045)\times10} = e^{1.55} \approx 4.71\times S_0$

**Stock B has higher median** by a wide margin.

**Mean** $= S_0 \cdot e^{\mu T}$:
- Stock A: $e^{1.0} \approx 2.72\times S_0$
- Stock B: $e^{2.0} \approx 7.39\times S_0$

**Stock B also has higher mean.**

**Key insight:** With equal volatility, the higher-drift stock dominates both median and mean. The Ito correction $-\sigma^2/2$ reduces the log-growth rate equally for both stocks (both have the same $\sigma$), so the ranking is preserved.

If you asked: Stock A has $\mu=0.20$, $\sigma=0.60$ and Stock B has $\mu=0.10$, $\sigma=0.10$:
- A: median grows at $(0.20 - 0.18) = 0.02$ per year — barely growing
- B: median grows at $(0.10 - 0.005) = 0.095$ per year — faster!

High vol can destroy median growth even with a high drift — the Ito correction matters.

</details>

---

### Level 3 — Coding

**Q6.** The implementation uses the *exact* solution rather than Euler-Maruyama. When would you *need* Euler-Maruyama, and what error does it introduce?

<details>
<summary>Answer</summary>

**When Euler-Maruyama is needed:** When the SDE has no closed-form solution. GBM is the rare exception — most SDEs (Heston, SABR, CIR) cannot be solved analytically and require numerical discretization.

**Euler-Maruyama scheme for GBM:**
$$S_{t+\Delta t} \approx S_t + \mu S_t \Delta t + \sigma S_t \Delta W_t$$

**Error introduced:** Euler-Maruyama has *strong order 0.5* convergence — the pathwise error is $O(\sqrt{\Delta t})$. This means to halve the error you must quarter the step size (4× more computation).

For GBM specifically, Euler-Maruyama introduces a discretization bias:
```python
# Euler-Maruyama (biased for GBM):
S_next = S + mu * S * dt + sigma * S * dW

# Exact (no bias):
S_next = S * np.exp((mu - 0.5*sigma**2)*dt + sigma*dW)
```
The exact method has zero discretization error — always use it for GBM. Euler-Maruyama is only needed when you have no choice (complex SDEs like Heston).

**Common bug:** Using Euler-Maruyama for GBM and forgetting that terminal prices will be slightly biased upward (Euler overestimates the drift slightly for convex payoffs). For Monte Carlo option pricing, always use the exact GBM solution.

</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "The drift $\mu$ appears in the option price" | It doesn't. BSM option prices contain only $r$, $\sigma$, $S_0$, $K$, $T$. The drift $\mu$ cancels when you change to the risk-neutral measure. |
| "Log-returns being normal means returns are normal" | Log-returns $\ln(S_t/S_0) \sim \mathcal{N}$ means *prices* are lognormal, and arithmetic returns $(S_t - S_0)/S_0$ are lognormally distributed — not normal. The two are different distributions. |
| "Higher volatility means higher expected return" | GBM has $E[S_T] = S_0 e^{\mu T}$ regardless of $\sigma$. Higher vol *lowers* the median return (via the $-\sigma^2/2$ correction) while leaving the mean unchanged. More vol = more right-skew, not more average return. |
| "GBM can go negative" | No — $S_t = S_0 \exp(\ldots) > 0$ always, since exponentials are always positive. This is a feature, not a bug: prices can never go below zero in GBM. |

## Related Concepts
- [[Brownian Motion]] — the $dW_t$ driver
- [[Ito's Lemma]] — used to solve the GBM SDE
- [[Black-Scholes Model]] — prices options assuming $S_t$ follows GBM
- [[Heston Model]] — extends GBM with stochastic $\sigma$
- [[Implied Volatility]] — the market's view on what $\sigma$ should be

## Sources Used
- Hull — *Options, Futures & Other Derivatives*, ch.14
- Shreve — *Stochastic Calculus for Finance II*, ch.1

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | Hull ch.14 + Shreve II ch.1 |
| 2026-04-11 | QA review: status → evergreen; path wikilinks → note-name wikilinks; last_reviewed updated | QA pass |
