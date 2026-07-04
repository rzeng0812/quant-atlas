---
type: concept
domain: 10-Foundations
tags: [foundations, stochastic-processes, brownian-motion]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-25
review_interval_days: 365
sources:
  - "Shreve - Stochastic Calculus for Finance II ch.3"
created: 2026-04-25
---

> [!info] Problem Chain
> **Chain:** Pricing → Gap 6: Many contracts have no closed-form solution
> **This concept:** Provides an exact analytic tool for computing the distribution of Brownian motion extrema, enabling closed-form pricing of barrier options.
> **Alternative approaches to this gap:** [[Monte Carlo Methods]], [[Numerical Methods PDE]] or finite-difference grids
> **You need first:** [[Brownian Motion]], [[Geometric Brownian Motion]]
> **This unlocks:** [[Exotic Options]] (barrier options), [[Monte Carlo Methods]] (variance reduction via importance sampling)

> Symmetry of Brownian motion about a level; used to derive hitting-time distributions and barrier option prices

## Why This Exists

**The gap:** Vanilla option pricing via Black-Scholes gives you the terminal distribution of a stock price but says nothing about whether the stock breached a particular level *during* the life of the contract.
**What came before:** The Black-Scholes PDE and risk-neutral pricing framework price European options based only on the terminal value $S_T$. Barrier options (which knock in or knock out if $S$ touches a level $H$) require the joint distribution of $(S_T, \max_{t \leq T} S_t)$ — a path property that BSM cannot compute directly.
**What this adds:** The reflection principle exploits the spatial symmetry of Brownian motion: a path that reaches level $a$ and then ends below $a$ can be "reflected" to produce a path that ends above $a$. This one-to-one mapping gives the exact distribution of the running maximum $M_T = \max_{t \leq T} W_t$, which is all you need to price barriers analytically.
**What it still doesn't solve:** The reflection principle applies to standard Brownian motion. For GBM with drift, you need a Girsanov change of measure first, adding complexity. It also does not handle two-sided barriers (double knock-out) without series expansions.

## Math Concepts

### Standard Brownian Motion Recap

A standard Brownian motion $W = (W_t)_{t \geq 0}$ satisfies:
- $W_0 = 0$
- Independent increments: $W_t - W_s \perp \mathcal{F}_s$ for $t > s$
- $W_t - W_s \sim N(0, t-s)$
- Continuous paths almost surely

### The Reflection Principle

**Theorem (Reflection Principle):** Let $W$ be a standard Brownian motion and $a > 0$. Define the first hitting time $\tau_a = \inf\{t \geq 0 : W_t = a\}$. Then:

$$P(M_T \geq a) = 2 P(W_T \geq a)$$

where $M_T = \max_{0 \leq t \leq T} W_t$.

**Intuition:** For any path that ends below $a$ but has at some point touched $a$, reflect the portion after the first hitting time across the level $a$. This creates a one-to-one correspondence between:
- Paths that touch $a$ but end below $a$ ($M_T \geq a$ and $W_T < a$)
- Paths that end above $a$ ($W_T > a$)

Because paths that end above $a$ have definitely touched $a$:

$$P(M_T \geq a, W_T < a) = P(W_T > a)$$

Adding $P(M_T \geq a, W_T \geq a) = P(W_T \geq a)$ on both sides:

$$P(M_T \geq a) = 2 P(W_T \geq a) = 2\left(1 - \Phi\left(\frac{a}{\sqrt{T}}\right)\right)$$

### Joint Distribution of $(W_T, M_T)$

The joint density follows from differentiating the reflection result:

$$P(W_T \leq x, M_T \geq a) = P(W_T \geq 2a - x) \quad \text{for } x < a$$

This gives the joint CDF:

$$P(M_T \leq m, W_T \leq x) = \Phi\left(\frac{x}{\sqrt{T}}\right) - e^{-\frac{2mx}{T}} \cdot \Phi\left(\frac{x - 2m}{\sqrt{T}}\right) \quad \text{for } x \leq m, \, m > 0$$

### Hitting Time Distribution

The first passage time $\tau_a$ has the inverse Gaussian distribution:

$$P(\tau_a \leq t) = 2\left(1 - \Phi\left(\frac{a}{\sqrt{t}}\right)\right)$$

$$f_{\tau_a}(t) = \frac{a}{\sqrt{2\pi t^3}} e^{-a^2/(2t)}, \quad t > 0$$

### Extension to GBM: Down-and-Out Call

For $S_t = S_0 e^{(r - \frac{1}{2}\sigma^2)t + \sigma W_t}$, a **down-and-out call** with barrier $H < S_0$ and strike $K$ pays $(S_T - K)^+$ only if $S$ never touches $H$. Applying the reflection principle after a Girsanov drift change gives the closed-form:

$$C_{DO} = C_{BSM} - \left(\frac{H}{S_0}\right)^{2\lambda} C_{BSM}\left(S_0' = \frac{H^2}{S_0}\right)$$

where $\lambda = \frac{r}{\sigma^2} + \frac{1}{2}$ and $C_{BSM}$ is the standard Black-Scholes call price.

## Walkthrough

**Setup:** Standard BM, $T = 1$, $a = 1.5$.

**Step 1: Probability the maximum exceeds 1.5.**

$$P(M_1 \geq 1.5) = 2 P(W_1 \geq 1.5) = 2(1 - \Phi(1.5)) = 2(1 - 0.9332) = 2 \times 0.0668 = 0.1336$$

So there is a 13.4% chance that standard BM exceeds 1.5 at some point in $[0,1]$.

**Step 2: Barrier option pricing.**

$S_0 = 100$, $H = 90$ (knock-out barrier), $K = 100$ (at-the-money), $r = 5\%$, $\sigma = 20\%$, $T = 1$ year.

Standard BSM call: $C_{BSM} \approx \$10.45$.

Compute $\lambda = 0.05/0.04 + 0.5 = 1.75$.

Reflected spot: $S_0' = H^2/S_0 = 8100/100 = 81$.

BSM call at $S_0' = 81$: $C_{BSM}(81) \approx \$3.97$.

Reflection term: $(H/S_0)^{2\lambda} = (0.9)^{3.5} \approx 0.698$.

$$C_{DO} = 10.45 - 0.698 \times 3.97 \approx 10.45 - 2.77 = \$7.68$$

The knock-out barrier reduces the call value from \$10.45 to \$7.68 — the difference is the value of the paths that would have touched \$90 and been knocked out.

## Analysis

**Why the reflection principle works geometrically:**

The key is that Brownian motion is symmetric around any level it has visited. Once $W$ touches level $a$ at time $\tau_a$, the future path $(W_{\tau_a + s})_{s \geq 0}$ is itself a standard BM. Reflecting $(W_{\tau_a + s})$ gives another valid BM path. This symmetry is exact and leads to no approximation error.

**Drift breaks the pure symmetry:** When you add drift (as in GBM), the paths are no longer symmetric around $a$. Paths going up are more likely than paths going down (or vice versa). You must use Girsanov's theorem to change to a driftless measure, apply the reflection principle there, then change back. The formula for the down-and-out call captures this via the $(H/S_0)^{2\lambda}$ factor.

**Practical importance of barrier options:**

Barrier options are extremely common in practice:
- Structured products with capital protection levels
- FX options with knock-out barriers
- Equity-linked notes with trigger levels

Pricing them analytically is possible only because of the reflection principle. Monte Carlo is 10-100x slower for single-barrier options when an analytical formula exists.

## Implementation

```python
import numpy as np
from scipy.stats import norm

# ── Standard BM maximum distribution ────────────────────────────────────────────

def prob_max_exceeds(a: float, T: float) -> float:
    """P(max_{0<=t<=T} W_t >= a) using reflection principle."""
    return 2 * (1 - norm.cdf(a / np.sqrt(T)))


def hitting_time_pdf(t: float, a: float) -> float:
    """PDF of first passage time to level a for standard BM."""
    return (a / np.sqrt(2 * np.pi * t**3)) * np.exp(-a**2 / (2 * t))


# ── Black-Scholes call price (helper) ───────────────────────────────────────────

def bsm_call(S, K, r, sigma, T):
    """Standard BSM European call price."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


# ── Down-and-out call via reflection principle ───────────────────────────────────

def down_and_out_call(S0: float, K: float, H: float,
                      r: float, sigma: float, T: float) -> float:
    """
    Closed-form price of a down-and-out European call using the reflection principle.

    Parameters
    ----------
    S0    : float - current stock price
    K     : float - strike price
    H     : float - knock-out barrier (H < S0)
    r     : float - risk-free rate (continuously compounded)
    sigma : float - volatility
    T     : float - time to expiry (years)

    Returns
    -------
    float : down-and-out call price
    """
    if H >= S0:
        raise ValueError("Barrier H must be strictly below S0.")

    lam = r / sigma**2 + 0.5                  # drift parameter in BM space
    S_reflected = H**2 / S0                    # reflected stock price

    vanilla = bsm_call(S0, K, r, sigma, T)
    reflected = bsm_call(S_reflected, K, r, sigma, T)

    price = vanilla - (H / S0)**(2 * lam) * reflected
    return max(price, 0.0)


# ── Example ───────────────────────────────────────────────────────────────────

S0, K, H = 100.0, 100.0, 90.0
r, sigma, T = 0.05, 0.20, 1.0

vanilla_price = bsm_call(S0, K, r, sigma, T)
barrier_price = down_and_out_call(S0, K, H, r, sigma, T)

print(f"Standard BM: P(max >= 1.5 over T=1) = {prob_max_exceeds(1.5, 1.0):.4f}")
print(f"\nVanilla BSM call:    ${vanilla_price:.4f}")
print(f"Down-and-out call:   ${barrier_price:.4f}")
print(f"Knock-out discount:  ${vanilla_price - barrier_price:.4f}")

# ── Monte Carlo validation ────────────────────────────────────────────────────

np.random.seed(42)
N_paths = 500_000
N_steps = 252  # daily

dt = T / N_steps
paths = np.zeros((N_paths, N_steps + 1))
paths[:, 0] = S0

for i in range(N_steps):
    z = np.random.standard_normal(N_paths)
    paths[:, i + 1] = paths[:, i] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)

min_path = paths.min(axis=1)
terminal  = paths[:, -1]

# Survived: never touched H
survived_mask = min_path > H
payoff = np.maximum(terminal - K, 0) * survived_mask
mc_price = np.exp(-r * T) * payoff.mean()
mc_se    = np.exp(-r * T) * payoff.std() / np.sqrt(N_paths)

print(f"\nMonte Carlo price:   ${mc_price:.4f} ± ${1.96 * mc_se:.4f} (95% CI)")
print(f"Analytical price:    ${barrier_price:.4f}")
print(f"Difference:          ${abs(mc_price - barrier_price):.4f}")
```

## Bridge to Quant / ML

- **Variance reduction in MC:** Knowing the exact barrier-crossing probability analytically allows you to use importance sampling — simulating paths conditional on not crossing the barrier — dramatically reducing Monte Carlo variance for rare-event barrier contracts.
- **Path-dependent feature construction:** In ML-based option pricing models (neural networks trained to price exotic options), the running maximum $M_T$ and minimum $m_T$ of the underlying are natural features. The reflection principle gives their exact distribution, useful for validating and calibrating such models.
- **Credit risk:** First passage models of default (e.g., Black-Cox model) use the reflection principle to compute the probability that a firm's asset value hits a default boundary before debt maturity — the same mathematics as a down-and-out option.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why does the reflection principle require Brownian motion to be symmetric? What property of BM makes it valid?
<details><summary>Answer</summary>The reflection principle relies on the fact that once BM touches a level $a$ at time $\tau_a$, the future increments are independent of the past and have the same distribution. Reflecting the path after $\tau_a$ across level $a$ produces another valid BM path — this is only true because BM has no drift and has spatially homogeneous, symmetric increments. With drift, the reflected path has a different drift and is no longer a valid copy of the original process.</details>

**Q2.** What is the difference between the reflection principle result for the running maximum and a simple normal probability? Why are they related by a factor of 2?
<details><summary>Answer">The running maximum $P(M_T \geq a) = 2P(W_T \geq a)$ because the event $\{M_T \geq a\}$ is the union of two disjoint events: paths that touch $a$ and end above $a$ (probability $= P(W_T \geq a)$), and paths that touch $a$ but end below $a$ (which by the reflection bijection also has probability $= P(W_T \geq a)$). Summing these two equal probabilities gives the factor of 2.</details>

**Q3.** Why does a down-and-out call price decrease relative to a vanilla call? Under what condition is the discount largest?
<details><summary>Answer</summary>The down-and-out call is worth less because some paths where the stock ends in-the-money would have previously touched the barrier and knocked out the option. The discount is largest when the barrier $H$ is close to the current spot $S_0$ (many paths will hit it), when volatility is high (paths wander more), and when time to expiry is long (more opportunity to touch the barrier).</details>

---

### Level 2 — Quantitative

**Q4.** For a standard BM with $T = 4$ years, what is the probability that the path exceeds level $a = 2$ at some point during $[0,4]$?
<details><summary>Answer</summary>Using the reflection principle: $P(M_4 \geq 2) = 2P(W_4 \geq 2) = 2(1 - \Phi(2/\sqrt{4})) = 2(1 - \Phi(1)) = 2(1 - 0.8413) = 2 \times 0.1587 = 0.3174$. There is a 31.7% chance the path exceeds 2 at some point in 4 years.</details>

**Q5.** A stock has $S_0 = 100$, $\sigma = 25\%$, $r = 0$, $T = 0.5$ years, $K = 100$, $H = 85$. Compute the vanilla BSM call price and estimate the down-and-out call price (use $\lambda = r/\sigma^2 + 0.5 = 0.5$ since $r=0$).
<details><summary>Answer</summary>With $r=0$, $\sigma=0.25$, $T=0.5$: $d_1 = (0 + 0.5 \times 0.0625 \times 0.5)/(0.25\sqrt{0.5}) = 0.03125/0.17678 \approx 0.177$; $d_2 = 0.177 - 0.177 = 0$. Vanilla call $\approx 100\Phi(0.177) - 100\Phi(0) = 100(0.570 - 0.500) = \$7.00$.

For the barrier: $\lambda = 0.5$, $S_0' = 85^2/100 = 72.25$. BSM call with $S=72.25$, $K=100$, $r=0$, $\sigma=0.25$, $T=0.5$: $d_1 = \ln(72.25/100)/(0.25\sqrt{0.5}) \approx -0.325/0.177 \approx -1.84$; $\Phi(-1.84) \approx 0.033$. $C(72.25) \approx 72.25 \times 0.033 - 100 \times \Phi(-2.02) \approx 2.38 - 100 \times 0.022 = \$0.18$. $(H/S_0)^{2\lambda} = (0.85)^1 = 0.85$. $C_{DO} \approx 7.00 - 0.85 \times 0.18 = 7.00 - 0.15 = \$6.85$. The barrier discount is small here because the barrier is far from spot relative to $\sigma\sqrt{T}$.</details>

---

### Level 3 — Coding

**Q6.** Extend the `down_and_out_call` function to price a **down-and-in call** — a call that only pays if the stock *has* touched the barrier $H$ at some point. Use the in-out parity relationship.
<details><summary>Answer</summary>In-out parity: $C_{DI} + C_{DO} = C_{vanilla}$ (a barrier that always knocks in plus one that always knocks out together equal a vanilla call). Therefore:

```python
def down_and_in_call(S0, K, H, r, sigma, T):
    vanilla = bsm_call(S0, K, r, sigma, T)
    barrier_out = down_and_out_call(S0, K, H, r, sigma, T)
    return vanilla - barrier_out
```

This follows because every path either touches the barrier (knock-in activates) or doesn't (knock-out survives). The two options together cover every scenario exactly once, so they sum to the vanilla call.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| $P(M_T \geq a) = P(W_T \geq a)$ | The maximum is twice as likely to exceed $a$ as the terminal value alone: $P(M_T \geq a) = 2P(W_T \geq a)$ |
| The reflection principle applies directly to GBM | It applies to driftless BM. For GBM you must apply a Girsanov drift removal first, then reflect, then change back. |
| A down-and-out call is always cheaper than a vanilla call | Correct — it is always cheaper or equal (never more). The barrier can only reduce value since it extinguishes payoffs that would otherwise have been positive. |
| The barrier discount is negligible for far barriers | For high-volatility or long-dated options, barriers only 10–15% below spot can cause 20–40% discounts because the probability of touching grows with $\sigma\sqrt{T}$. |

## Related Concepts

- [[Brownian Motion]] — the process the reflection principle applies to
- [[Geometric Brownian Motion]] — stock price model; reflection principle applied after drift adjustment
- [[Exotic Options]] — barrier options are the primary application
- [[Monte Carlo Methods]] — numerical alternative; reflection gives benchmark for validation
- [[Girsanov Theorem]] — the tool that handles drift when extending reflection to GBM

## Sources Used

- Shreve, S. — *Stochastic Calculus for Finance II*, ch. 3 (Brownian Motion Stopping Times)
- Hull, J. — *Options, Futures, and Other Derivatives*, ch. 26 (Exotic Options)
- Karatzas, I. & Shreve, S. — *Brownian Motion and Stochastic Calculus*, ch. 2

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-25 | Note created and full content written | bootstrap |
