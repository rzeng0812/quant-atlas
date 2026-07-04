---
type: concept
domain: 10-Foundations
tags: [math, stochastic-calculus, probability]
status: evergreen
stability: stable
confidence: high
last_reviewed: 2026-04-11
review_interval_days: 365
sources:
  - "Hull ch.14"
  - "Shreve Vol I ch.1"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Pricing → Gap 2: To build the replicating portfolio, you need a model for how prices move
> **This concept:** Provides the raw continuous-time noise process — the source of randomness on which every stochastic price model is built.
> **Alternative approaches to this gap:** none — Brownian motion is the foundational primitive; GBM and other models layer on top of it
> **You need first:** none — this is a starting point
> **This unlocks:** [[Geometric Brownian Motion]], [[Stochastic Differential Equations]], [[Ito's Lemma]], [[Ornstein-Uhlenbeck Process]]

## Why This Exists

**The gap:** Practitioners needed a rigorous mathematical model for quantities that move continuously and unpredictably over time — prices, rates, spreads. There was no agreed continuous-time framework for this randomness.

**What came before:** Discrete random walk models (coin-flip sequences). These captured the intuition of random movement but were inherently discrete — they couldn't describe instantaneous changes, couldn't be differentiated, and couldn't be embedded in continuous-time calculus.

**What this adds:** A continuous-time stochastic process with well-defined statistical properties: independent increments, normally distributed moves, continuous paths, and variance that scales linearly with time. This makes it possible to write equations governing random processes at every instant — the prerequisite for SDEs, option pricing, and all of continuous-time finance.

**What it still doesn't solve:** Brownian motion alone can go negative and has no drift or scaling structure suited to price dynamics. It needs to be transformed into a model that keeps prices positive and makes proportional (not absolute) moves — that is Gap 2's remaining work, addressed by [[Geometric Brownian Motion]].

## Math Concepts

A standard Brownian motion $W_t$ is a stochastic process satisfying:

1. **Starts at zero:** $W_0 = 0$
2. **Independent increments:** for $0 \leq s < t$, the increment $W_t - W_s$ is independent of $\mathcal{F}_s$ (the history up to time $s$)
3. **Normal increments:** $W_t - W_s \sim \mathcal{N}(0,\ t - s)$
4. **Continuous paths:** $t \mapsto W_t$ is continuous almost surely

The variance of an increment scales *linearly* with time:

$$\text{Var}(W_t - W_s) = t - s$$

So the standard deviation scales as $\sqrt{t - s}$ — not linearly. This is the key: Brownian motion moves *faster* at short timescales relative to long ones.

**Quadratic variation** — a crucial property for Ito calculus:

$$[W, W]_t = t \qquad \text{i.e.,} \quad (dW_t)^2 = dt$$

This is not true for ordinary differentiable functions (where $(dx)^2 \to 0$). It means Brownian paths are nowhere differentiable, and second-order terms survive in the Taylor expansion — the origin of [[Ito's Lemma]].

## Walkthrough

Simulate one path of $W_t$ on $[0, 1]$ with $N = 1000$ steps:

$$\Delta t = \frac{1}{N}, \qquad \Delta W_i \sim \mathcal{N}(0, \Delta t), \qquad W_{i+1} = W_i + \Delta W_i$$

Notice:
- The path is jagged no matter how fine the grid — it never smooths out
- The spread of paths grows as $\sqrt{t}$ — wide at $t=1$, narrow at $t=0$
- Paths cross zero repeatedly (recurrence)

## Analysis

- **Not differentiable:** $W_t$ has no derivative in the ordinary sense. This forces a new calculus ([[Stochastic Differential Equations]], [[Ito's Lemma]]).
- **Martingale:** $\mathbb{E}[W_t \mid \mathcal{F}_s] = W_s$ — the best forecast of future value is current value. Central to [[Risk-Neutral Measure]] pricing.
- **Markov property:** the future of $W_t$ depends only on its current value, not its history.
- **Scaling:** $c^{-1/2} W_{ct} \overset{d}{=} W_t$ — Brownian motion is self-similar.

**Common confusion:** $dW_t \sim \mathcal{N}(0, dt)$ is shorthand. It means in the limit $\Delta W \sim \mathcal{N}(0, \Delta t)$ as $\Delta t \to 0$.

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

def simulate_brownian(T=1.0, N=1000, n_paths=5, seed=42):
    rng = np.random.default_rng(seed)
    dt = T / N
    t = np.linspace(0, T, N + 1)
    dW = rng.normal(0, np.sqrt(dt), size=(n_paths, N))
    W = np.concatenate([np.zeros((n_paths, 1)), np.cumsum(dW, axis=1)], axis=1)
    return t, W
```

Verify quadratic variation: sum of squared increments $\sum (\Delta W_i)^2 \to T$ as $N \to \infty$.

## Bridge to Quant / ML

- Direct input to [[Geometric Brownian Motion]] — the noise term $\sigma dW_t$
- Hurst exponent $H$: if $H = 0.5$ → pure Brownian; $H > 0.5$ → trending; $H < 0.5$ → mean-reverting. Key input to alpha factor construction
- In [[Regime Detection]], detecting regime shifts is detecting changes in the volatility $\sigma$ of the underlying Brownian driver

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** State the four defining properties of a standard Brownian motion without looking. Then check: which property is most commonly forgotten?

<details>
<summary>Answer</summary>

1. $W_0 = 0$ — starts at zero
2. Independent increments — $W_t - W_s$ is independent of $\mathcal{F}_s$ for $s < t$
3. Normal increments — $W_t - W_s \sim \mathcal{N}(0, t-s)$
4. Continuous paths — $t \mapsto W_t$ is continuous almost surely

**Most commonly forgotten:** Property 2 (independent increments). It's the subtlest — it says not just that successive increments are independent of each other, but that each increment is independent of the *entire history* up to the start of that increment. This is the Markov property at the heart of why we can price derivatives without knowing the full path history.

</details>

---

**Q2.** Why does standard deviation scale as $\sqrt{t}$ rather than linearly with time?

<details>
<summary>Answer</summary>

Because increments are independent and variance is additive. Divide $[0, t]$ into $n$ equal steps of size $\Delta t = t/n$. Each increment has variance $\Delta t$. Total variance = $n \cdot \Delta t = t$. So $\text{Var}(W_t) = t$ and $\text{std}(W_t) = \sqrt{t}$.

This is the same reason the standard error of a sample mean scales as $1/\sqrt{n}$ — summing $n$ independent random variables multiplies variance by $n$, so std only grows as $\sqrt{n}$.

**Key implication:** Uncertainty in prices grows as $\sigma\sqrt{T}$, not $\sigma T$. A stock that's volatile over one day is *much* less scary over one hour — uncertainty scales down as $\sqrt{1/24}$, not $1/24$.

</details>

---

**Q3.** What is quadratic variation and why does it matter for Ito calculus? What is the quadratic variation of a smooth differentiable function?

<details>
<summary>Answer</summary>

The quadratic variation of $W_t$ over $[0,t]$ is:
$$[W,W]_t = \lim_{n\to\infty} \sum_{i=1}^n (W_{t_i} - W_{t_{i-1}})^2 = t$$

Written informally: $(dW_t)^2 = dt$.

**Why it matters:** In ordinary calculus, $(dx)^2 \to 0$ faster than $dt$ — second-order terms vanish in Taylor expansions. For Brownian motion, $(dW)^2 = dt$ — second-order terms are *first-order in time* and survive. This is exactly why Ito's Lemma has an extra $\frac{1}{2}\sigma^2 f_{xx}$ term that ordinary calculus doesn't.

**Smooth differentiable function:** $[f, f]_t = 0$. For a differentiable path $x(t)$, increments satisfy $|\Delta x| \approx |x'| \cdot |\Delta t|$, so $(\Delta x)^2 \approx (x')^2 (\Delta t)^2 \to 0$ as $\Delta t \to 0$. Quadratic variation is zero. Brownian motion is the opposite — its paths are so jagged that quadratic variation is nonzero.

</details>

---

**Q4.** You simulate 10,000 paths of $W_t$ on $[0, 1]$ with $N=500$ steps. You compute $\sum_{i=1}^{500} (\Delta W_i)^2$ for each path. What value do you expect this sum to converge to, and why?

<details>
<summary>Answer</summary>

The sum converges to **1** (the quadratic variation $[W,W]_1 = T = 1$).

Each $\Delta W_i = W_{t_i} - W_{t_{i-1}} \sim \mathcal{N}(0, \Delta t)$, so $E[(\Delta W_i)^2] = \Delta t$. There are $N = 500$ steps, so:
$$E\!\left[\sum_{i=1}^N (\Delta W_i)^2\right] = N \cdot \Delta t = 500 \cdot \frac{1}{500} = 1$$

By the law of large numbers, the sum concentrates around its expectation as $N \to \infty$. This is not just an approximation — it converges *almost surely* to $T$ as $\Delta t \to 0$. This is the rigorous definition of quadratic variation.

**Implementation check:** The code in the note's Implementation section includes this verification — run it to confirm.

</details>

---

### Level 2 — Quantitative

**Q5.** Let $W_t$ be a standard Brownian motion. Compute:

a) $P(W_1 > 1.5)$
b) $P(W_4 - W_1 > 2)$
c) $\text{Cov}(W_s, W_t)$ for $s \leq t$

<details>
<summary>Answer</summary>

**a)** $W_1 \sim \mathcal{N}(0, 1)$, so $P(W_1 > 1.5) = 1 - \Phi(1.5) \approx 1 - 0.9332 = 6.7\%$.

**b)** $W_4 - W_1 \sim \mathcal{N}(0, 4-1) = \mathcal{N}(0, 3)$ by independent increments and $\text{Var}(W_t - W_s) = t - s$.

$$P\!\left(\frac{W_4 - W_1}{\sqrt{3}} > \frac{2}{\sqrt{3}}\right) = P(Z > 1.155) \approx 1 - \Phi(1.155) \approx 12.4\%$$

**c)** For $s \leq t$, write $W_t = W_s + (W_t - W_s)$. The increment $W_t - W_s$ is independent of $W_s$ (independent increments):

$$\text{Cov}(W_s, W_t) = \text{Cov}(W_s, W_s + (W_t - W_s)) = \text{Var}(W_s) + \text{Cov}(W_s, W_t - W_s) = s + 0 = s$$

So $\text{Cov}(W_s, W_t) = \min(s, t)$. The correlation is $\text{Corr}(W_s, W_t) = \sqrt{s/t}$ — two Brownian values close in time are highly correlated; far apart, less so.

</details>

---

**Q6.** You discretize $W_t$ on $[0, 2]$ into $N = 1000$ steps. Simulate the quadratic variation $\sum (\Delta W_i)^2$. Without running code:

a) What is the mean of each $(\Delta W_i)^2$?
b) What is the variance of each $(\Delta W_i)^2$?
c) By CLT, what is the approximate distribution of $\sum_{i=1}^{1000} (\Delta W_i)^2$?

<details>
<summary>Answer</summary>

$\Delta t = 2/1000 = 0.002$. Each $\Delta W_i \sim \mathcal{N}(0, \Delta t)$, so $(\Delta W_i)^2 / \Delta t \sim \chi^2_1$.

**a)** $E[(\Delta W_i)^2] = \Delta t = 0.002$.

**b)** $\text{Var}[(\Delta W_i)^2] = 2(\Delta t)^2 = 2 \times (0.002)^2 = 8 \times 10^{-6}$.

(Using $\text{Var}[Z^2] = 2$ for $Z \sim \mathcal{N}(0,1)$, scaled by $(\Delta t)^2$.)

**c)** By CLT with $N=1000$ i.i.d. terms:
$$\sum_{i=1}^{1000} (\Delta W_i)^2 \approx \mathcal{N}\!\left(N\Delta t,\ N \cdot 2(\Delta t)^2\right) = \mathcal{N}\!\left(2,\ 1000 \times 8\times10^{-6}\right) = \mathcal{N}(2, 0.008)$$

Std dev $\approx 0.089$. So the quadratic variation concentrates tightly around $T=2$, confirming its deterministic limit.

</details>

---

### Level 3 — Coding

**Q7.** The simulation code uses `rng.normal(0, np.sqrt(dt), size=(n_paths, N))` to generate increments. A colleague suggests using `rng.normal(0, 1, size=(n_paths, N)) * dt` instead. What is wrong with this?

<details>
<summary>Answer</summary>

The colleague's version generates increments with standard deviation $dt$ rather than $\sqrt{dt}$.

Brownian increments satisfy $\Delta W \sim \mathcal{N}(0, \Delta t)$, meaning **std dev = $\sqrt{\Delta t}$**, not $\Delta t$.

The code should be `rng.normal(0, 1) * np.sqrt(dt)` or equivalently `rng.normal(0, np.sqrt(dt))`.

Using $dt$ instead of $\sqrt{dt}$ makes the increments far too small (for small $dt$, $dt \ll \sqrt{dt}$) — the simulated paths would barely move, like a nearly flat line instead of a jagged Brownian path. The quadratic variation $\sum (\Delta W_i)^2 \approx N \cdot (dt)^2 = T \cdot dt \to 0$ as $\Delta t \to 0$ instead of converging to $T$ — a clear signal something is wrong.

</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "Brownian motion has zero mean, so it always stays near zero" | $E[W_t] = 0$ but $\text{Var}(W_t) = t$ grows without bound. Individual paths wander arbitrarily far from zero — the *average* over many paths stays at zero. |
| "$dW_t$ is the derivative of $W_t$" | $W_t$ is nowhere differentiable. $dW_t$ is formal notation for an infinitesimal increment, defined only in integral form. |
| "The Markov property means past increments are irrelevant" | Past increments are irrelevant for the *future distribution*, but the current value $W_t$ summarizes all relevant history. It's not that the past doesn't matter — it's that the current value is a sufficient statistic. |
| "Continuous paths means smooth paths" | Continuous ≠ smooth. Brownian paths are continuous but nowhere differentiable — they're infinitely jagged. You can draw them without lifting your pen, but the path has infinite total variation. |

## Related Concepts
- [[Geometric Brownian Motion]] — Brownian motion with drift and scaling
- [[Ito's Lemma]] — how to differentiate functions of $W_t$
- [[Stochastic Differential Equations]] — equations driven by $dW_t$
- [[Martingales]] — $W_t$ is a martingale
- [[Girsanov Theorem]] — changing the drift of a Brownian motion via measure change

## Sources Used
- Hull — *Options, Futures & Other Derivatives*, ch.14
- Shreve — *Stochastic Calculus for Finance I*, ch.1

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | Hull ch.14 + Shreve I ch.1 |
| 2026-04-11 | QA review: status → evergreen; path wikilinks → note-name wikilinks; last_reviewed updated | QA pass |
