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
  - "Shreve Vol II ch.5"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Pricing → Gap 4: The derived option price still contains μ — but no one agrees on μ
> **This concept:** Proves rigorously that you can shift the drift of a Brownian motion from μ to r by reweighting probabilities, making the Risk-Neutral Measure construction mathematically valid.
> **Alternative approaches to this gap:** [[Risk-Neutral Measure]] (the practical pricing result); [[Martingales]] (the mathematical language of no-arbitrage — both are needed for Gap 4)
> **You need first:** [[Brownian Motion]], [[Stochastic Differential Equations]], [[Ito's Lemma]], [[Martingales]]
> **This unlocks:** [[Risk-Neutral Measure]], [[Black-Scholes Model]], [[Change of Numeraire]]

## Why This Exists

**The gap:** Using Ito's Lemma to derive an option's price produced a formula that depended on $\mu$, the stock's expected return. But $\mu$ is subjective — every investor estimates it differently. If two traders disagree on $\mu$, they price the option differently. The replication argument showed $\mu$ must cancel, but the mechanism for doing so rigorously — actually changing the probability measure so the stock grows at $r$ instead of $\mu$ — needed mathematical justification.

**What came before:** The intuition that a hedged portfolio must earn the risk-free rate, so $\mu$ should disappear. This was economically clear from the Black-Scholes derivation, but the machinery for formally constructing the risk-neutral measure and proving it was a valid probability measure (not just a convenient fiction) was missing.

**What this adds:** A precise theorem: define the Radon-Nikodym derivative $Z_T = \exp(-\lambda W_T^P - \frac{1}{2}\lambda^2 T)$ where $\lambda = (\mu-r)/\sigma$ is the market price of risk. Under the new measure $Q$ defined by $dQ/dP = Z_T$, the process $W_t^Q = W_t^P + \lambda t$ is a standard Brownian motion and the stock's drift shifts from $\mu$ to $r$. The Novikov condition guarantees $Z_t$ is a true martingale, so $Q$ is a valid probability measure equivalent to $P$.

**What it still doesn't solve:** Girsanov establishes that the risk-neutral measure exists and is valid. It does not evaluate the option price — that requires computing $e^{-rT}\mathbb{E}^Q[H_T]$, which is the domain of the [[Black-Scholes Model]] (closed form for European options) or [[Numerical Methods PDE]] and [[Monte Carlo Methods]] (for everything else).

## Math Concepts

**Setup.** Work on a filtered probability space $(\Omega, \mathcal{F}, \{\mathcal{F}_t\}, P)$ where $W_t^P$ is a standard Brownian motion under the real-world measure $P$.

**Market price of risk.** For an asset with dynamics $dS_t = \mu S_t \, dt + \sigma S_t \, dW_t^P$, define the market price of risk (Sharpe ratio of the asset):

$$
\lambda = \frac{\mu - r}{\sigma},
$$

where $r$ is the risk-free rate, $\mu$ is the real-world drift, and $\sigma$ is volatility. $\lambda$ measures how much excess return per unit of volatility the asset earns.

**Radon-Nikodym derivative (the change-of-measure weight).** Define the process

$$
Z_t = \exp\!\left(-\lambda W_t^P - \tfrac{1}{2}\lambda^2 t\right).
$$

By Ito's lemma, $dZ_t = -\lambda Z_t \, dW_t^P$, so $Z_t$ is a martingale under $P$ with $E^P[Z_T] = 1$. The new measure $Q$ is defined by its Radon-Nikodym derivative:

$$
\frac{dQ}{dP}\bigg|_{\mathcal{F}_T} = Z_T = \exp\!\left(-\lambda W_T^P - \tfrac{1}{2}\lambda^2 T\right).
$$

This re-weights each scenario $\omega$ by $Z_T(\omega)$: scenarios where $W_T^P$ ended up large and positive (asset moved a lot in the risky direction) get down-weighted; scenarios where it ended negative get up-weighted. Net effect: the mean of the Brownian motion shifts.

**Girsanov's Theorem (statement).** Under the new measure $Q$,

$$
W_t^Q = W_t^P + \lambda t
$$

is a standard Brownian motion. Equivalently, $dW_t^P = dW_t^Q - \lambda \, dt$, so the asset dynamics become

$$
dS_t = \mu S_t \, dt + \sigma S_t \, (dW_t^Q - \lambda \, dt)
= (\mu - \sigma\lambda) S_t \, dt + \sigma S_t \, dW_t^Q
= r S_t \, dt + \sigma S_t \, dW_t^Q.
$$

The drift changes from $\mu$ to $r$; the diffusion coefficient $\sigma$ is unchanged.

**General (multidimensional) form.** For $n$ Brownian motions and a market price of risk vector $\boldsymbol{\lambda}_t$ (possibly time-varying), the Novikov condition

$$
E^P\!\left[\exp\!\left(\tfrac{1}{2}\int_0^T \|\boldsymbol{\lambda}_t\|^2 \, dt\right)\right] < \infty
$$

guarantees $Z_t$ is a true (not just local) martingale, so the change of measure is valid.

**Expectation under change of measure.** For any $\mathcal{F}_T$-measurable payoff $V$,

$$
E^Q[V] = E^P\!\left[Z_T \cdot V\right], \qquad E^P[V] = E^Q\!\left[\frac{1}{Z_T} \cdot V\right].
$$

This is the bridge between real-world and risk-neutral expectations.

## Walkthrough

**Concrete numbers.** Suppose:
- $\mu = 0.12$ (12% expected return under $P$)
- $r = 0.05$ (5% risk-free rate)
- $\sigma = 0.20$ (20% volatility)

Then $\lambda = (0.12 - 0.05)/0.20 = 0.35$ (a Sharpe ratio of 0.35).

Under $P$, a one-year Brownian path that ends at $W_1^P = 0.5$ gets a Radon-Nikodym weight of:

$$
Z_1 = \exp\!\left(-0.35 \times 0.5 - \tfrac{1}{2} \times 0.35^2 \times 1\right)
= \exp(-0.175 - 0.06125)
= \exp(-0.23625) \approx 0.790.
$$

That scenario is down-weighted to 79% of its original probability under $Q$. A path ending at $W_1^P = -0.5$:

$$
Z_1 = \exp(-0.35 \times (-0.5) - 0.06125) = \exp(0.175 - 0.06125) = \exp(0.11375) \approx 1.120.
$$

That scenario is *up*-weighted. The net effect: under $Q$, the average of $W_1^P$ shifts to $-\lambda \cdot 1 = -0.35$, which is exactly offset by the $+\lambda t$ correction so that $W_1^Q = W_1^P + 0.35$ has mean zero — a standard Brownian motion.

**Pricing a European call.** Under $Q$, $S_T = S_0 \exp\bigl((r - \tfrac{1}{2}\sigma^2)T + \sigma W_T^Q\bigr)$. The call price is

$$
C_0 = e^{-rT} E^Q[\max(S_T - K, 0)],
$$

which evaluates to the Black-Scholes formula. Girsanov's theorem is what licenses using $r$ (not $\mu$) inside the formula.

## Analysis

**Key properties.**
- The diffusion term $\sigma$ is invariant under the Girsanov change of measure — only drifts shift. This is why implied volatility (estimated from option prices under $Q$) and realized volatility (estimated from returns under $P$) measure the same object structurally, even if their numerical values differ due to variance risk premia.
- $Z_t$ is always positive (it's an exponential), so $Q$ and $P$ are **equivalent measures**: they agree on which events have probability zero. This is essential — the same scenarios are considered possible; only their probabilities differ.
- If $\lambda$ is too large and Novikov's condition fails, $Z_t$ is only a local martingale and the change of measure may not be globally valid (related to bubbles in asset pricing).

**Common confusions.**
- "Changing measure" sounds magical but it is simply re-weighting the probability of scenarios, like adjusting a histogram. The underlying sample paths $\omega$ are identical.
- Under $Q$, you should not interpret $r$ as the "expected return" in an economic sense — $Q$ is a mathematical construct for pricing, not a description of what an investor actually expects.
- The Radon-Nikodym derivative $Z_T$ must be computed at the terminal horizon $T$. For derivatives pricing you typically choose $T$ = maturity of the instrument.

**Multiple assets.** With $n$ risky assets and $n$ Brownian drivers, $\boldsymbol{\lambda}_t$ is a vector, and the unique risk-neutral measure exists when the market is complete (no redundant or missing sources of risk). Incomplete markets admit infinitely many equivalent martingale measures.

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

rng = np.random.default_rng(0)

# ── Parameters ─────────────────────────────────────────────────────────────
S0    = 100.0
mu    = 0.12      # real-world drift
r     = 0.05      # risk-free rate
sigma = 0.20      # volatility
T     = 1.0       # 1 year
K     = 105.0     # strike
n     = 500_000   # Monte Carlo paths
lam   = (mu - r) / sigma   # market price of risk = 0.35

# ── Simulate terminal Brownian increments under P ──────────────────────────
W_P = rng.normal(0, np.sqrt(T), size=n)  # W_T^P ~ N(0, T)

# Real-world stock price at T
S_T_P = S0 * np.exp((mu - 0.5 * sigma**2) * T + sigma * W_P)

# ── Radon-Nikodym derivative Z_T ──────────────────────────────────────────
Z_T = np.exp(-lam * W_P - 0.5 * lam**2 * T)
print(f"E^P[Z_T] = {Z_T.mean():.6f}  (should be 1.000)")

# ── Risk-neutral stock price: W_T^Q = W_T^P + lambda*T ─────────────────────
W_Q = W_P + lam * T     # shift the Brownian motion
S_T_Q = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * W_Q)
# equivalently: S_T_Q = S_T_P * exp((r - mu)*T)  for GBM

# ── Verify drift shift ─────────────────────────────────────────────────────
# Under P: E[S_T] = S0 * exp(mu * T)
# Under Q: E[S_T] = S0 * exp(r  * T)
print(f"\nE^P[S_T] = {S_T_P.mean():.2f}  (theory: {S0 * np.exp(mu * T):.2f})")
print(f"E^Q[S_T] = {S_T_Q.mean():.2f}  (theory: {S0 * np.exp(r  * T):.2f})")

# ── Price a European call three ways ───────────────────────────────────────
payoff = np.maximum(S_T_Q - K, 0)

# Method 1: direct Q simulation
C_Q = np.exp(-r * T) * payoff.mean()

# Method 2: importance sampling under P (using Z_T as weight)
payoff_P = np.maximum(S_T_P - K, 0)
C_IS = np.exp(-r * T) * (Z_T * payoff_P).mean()

# Method 3: Black-Scholes closed form
d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)
C_BS = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

print(f"\nEuropean call price (K={K}, T={T}):")
print(f"  Q-simulation (direct):      {C_Q:.4f}")
print(f"  P-simulation (IS / Girsanov): {C_IS:.4f}")
print(f"  Black-Scholes formula:       {C_BS:.4f}")

# ── Visualise the measure shift ────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Left: distribution of S_T under P vs Q
axes[0].hist(S_T_P, bins=100, density=True, alpha=0.5, label="P (real world)", color="steelblue")
axes[0].hist(S_T_Q, bins=100, density=True, alpha=0.5, label="Q (risk-neutral)", color="tomato")
axes[0].axvline(K, linestyle="--", color="black", label=f"K={K}")
axes[0].set_title("Distribution of $S_T$ under $P$ vs $Q$")
axes[0].set_xlabel("$S_T$")
axes[0].legend()

# Right: Radon-Nikodym weights Z_T vs W_T^P
axes[1].scatter(W_P[::500], Z_T[::500], alpha=0.2, s=5, color="purple")
axes[1].set_xlabel("$W_T^P$")
axes[1].set_ylabel("$Z_T = dQ/dP$")
axes[1].set_title("Radon-Nikodym weights: down-weight positive paths")
plt.tight_layout()
plt.show()
```

## Bridge to Quant / ML

**Derivatives pricing (the core use).** Every Black-Scholes style formula implicitly uses Girsanov. When you write $dS = rS\,dt + \sigma S\,dW^Q$, you have already applied the theorem. The risk-neutral measure $Q$ only exists because Girsanov guarantees that shifting the drift by $\lambda$ produces a valid equivalent measure.

**Interest rate models.** Moving between different numeraires (e.g., using a bond price as numeraire rather than a money market account) is a Girsanov-style change of measure. The $T$-forward measure used in pricing swaptions and caps is exactly this.

**Hedging and the market price of risk.** The vector $\boldsymbol{\lambda}_t$ appears in the stochastic discount factor (SDF) / pricing kernel in equilibrium models. Estimating $\lambda$ from time-series data (under $P$) and cross-sectional option prices (under $Q$) is a major research area: the gap between $P$ and $Q$ distributions is what traders call the "variance risk premium."

**ML / importance sampling.** Girsanov underpins importance sampling in Monte Carlo simulation: simulate under an easy measure $P$, weight by $Z_T = dQ/dP$, and recover $Q$-expectations. This is used in rare-event simulation and in policy gradient methods in reinforcement learning (the log-derivative / REINFORCE trick is a discrete analog of the Girsanov weight).

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** In plain English: what does Girsanov's theorem do? What changes when you move from $\mathbb{P}$ to $\mathbb{Q}$, and what stays the same?

<details>
<summary>Answer</summary>

Girsanov's theorem provides the mathematical mechanism for **changing the probability measure** — specifically, for shifting the drift of a Brownian motion without changing the sample paths or the volatility.

**What changes:** The drift of the process. Under $\mathbb{P}$, the stock grows at $\mu$ (real-world expected return). Under $\mathbb{Q}$, the drift becomes $r$ (risk-free rate). The Brownian motion $W_t^P$ is replaced by $W_t^Q = W_t^P + \lambda t$, which has a shifted mean trajectory.

**What stays the same:**
- The **sample paths** — the actual random realizations $\omega$ are identical under both measures; only their probabilities (weights) change.
- The **volatility $\sigma$** — this is the key structural invariant. Girsanov only shifts drifts, never diffusion coefficients. This is why implied volatility (computed under $\mathbb{Q}$) measures the same fundamental quantity as realized volatility (measured under $\mathbb{P}$), even though the two measures assign different drift probabilities.
- **Which events have probability zero** — $\mathbb{P}$ and $\mathbb{Q}$ are equivalent measures; they agree on impossibility.

The practical punchline: moving to $\mathbb{Q}$ is like adjusting a histogram. Every scenario that was possible remains possible — just with a different weight.

</details>

---

**Q2.** What is the market price of risk $\lambda$, and why is it the key quantity that determines the Girsanov measure change?

<details>
<summary>Answer</summary>

$$\lambda = \frac{\mu - r}{\sigma}$$

**Interpretation:** $\lambda$ is the **Sharpe ratio** of the asset — the excess return above the risk-free rate, per unit of volatility. It measures how much investors are compensated per unit of risk they bear.

**Why it's the key quantity:** The Girsanov change of measure shifts the Brownian motion by exactly $-\lambda$ per unit time: $W_t^Q = W_t^P + \lambda t$. Substituting into the asset dynamics:

$$dS_t = \mu S_t\,dt + \sigma S_t\,dW_t^P = (\mu - \sigma\lambda) S_t\,dt + \sigma S_t\,dW_t^Q = r S_t\,dt + \sigma S_t\,dW_t^Q$$

The entire risk premium $\mu - r = \sigma\lambda$ is exactly canceled by the $-\lambda$ shift. A larger Sharpe ratio ($\lambda$) requires a larger measure change — the two worlds ($\mathbb{P}$ and $\mathbb{Q}$) are further apart. If $\lambda = 0$ (no risk premium), $\mathbb{P} = \mathbb{Q}$ — the real world and risk-neutral world coincide.

**Practically:** $\lambda$ is not directly observable but can be estimated by comparing $\mathbb{P}$-distribution moments (from historical returns) to $\mathbb{Q}$-distribution moments (from option prices). The gap between the two is the **variance risk premium**.

</details>

---

**Q3.** What does it mean for $\mathbb{P}$ and $\mathbb{Q}$ to be "equivalent measures"? Why is equivalence necessary for derivative pricing to make sense?

<details>
<summary>Answer</summary>

Two measures $\mathbb{P}$ and $\mathbb{Q}$ are **equivalent** if they agree on which events have probability zero (and therefore which events are impossible):

$$\mathbb{P}(A) = 0 \iff \mathbb{Q}(A) = 0 \quad \text{for all events } A \in \mathcal{F}$$

Equivalently, the Radon-Nikodym derivative $Z_T = d\mathbb{Q}/d\mathbb{P}$ is strictly positive ($Z_T > 0$ a.s.), which is guaranteed for Girsanov since $Z_T = e^{-\lambda W_T^P - \lambda^2 T/2}$ is always strictly positive.

**Why equivalence is necessary:**

1. **Replication must work in all possible worlds.** If a derivative can be replicated under $\mathbb{Q}$ in every scenario, it must also be replicated under $\mathbb{P}$ in every scenario (since they share the same set of possible scenarios). If $\mathbb{Q}$ considered a scenario impossible that $\mathbb{P}$ considered possible, a replicating strategy could fail under $\mathbb{P}$ — arbitrage would exist.

2. **Pricing must be consistent with the real world.** If $\mathbb{Q}$ assigned zero probability to some event that actually happens (positive $\mathbb{P}$-probability), the risk-neutral price could be disconnected from reality — not just mathematically but economically. Equivalence ensures the risk-neutral price is the correct no-arbitrage price in the real world too.

</details>

---

### Level 2 — Quantitative

**Q4.** Parameters: $\mu = 0.15$, $r = 0.04$, $\sigma = 0.25$, $T = 1$.

a) Compute the market price of risk $\lambda$.
b) A simulated path ends with $W_T^P = 1.2$. Compute the Radon-Nikodym weight $Z_T$.
c) Another path ends with $W_T^P = -0.8$. Compute $Z_T$. Which path is up-weighted under $\mathbb{Q}$?

<details>
<summary>Answer</summary>

**a)** $\lambda = (\mu - r)/\sigma = (0.15 - 0.04)/0.25 = 0.11/0.25 = 0.44$.

**b)** For $W_T^P = 1.2$:
$$Z_T = \exp\!\left(-\lambda W_T^P - \tfrac{1}{2}\lambda^2 T\right) = \exp(-0.44 \times 1.2 - \tfrac{1}{2} \times 0.44^2)$$
$= \exp(-0.528 - 0.0968) = \exp(-0.6248) \approx 0.535$

This path is **down-weighted** to 53.5% of its original probability.

**c)** For $W_T^P = -0.8$:
$$Z_T = \exp(-0.44 \times (-0.8) - 0.0968) = \exp(0.352 - 0.0968) = \exp(0.2552) \approx 1.291$$

This path is **up-weighted** to 129.1% of its original probability.

**Interpretation:** The path where $W_T^P = 1.2$ means the stock moved strongly upward under $\mathbb{P}$ (favorable outcome for the risky asset). Under $\mathbb{Q}$, we down-weight these "lucky" paths. The path where $W_T^P = -0.8$ means the stock moved downward — these adverse scenarios get up-weighted under $\mathbb{Q}$. Net effect: $\mathbb{Q}$ is more pessimistic about stock performance, consistent with the drift shifting from $\mu = 15\%$ to $r = 4\%$.

</details>

---

**Q5.** Explain mathematically why simulating under $\mathbb{P}$ and weighting by $Z_T$ gives the same result as simulating directly under $\mathbb{Q}$. Write the formula.

<details>
<summary>Answer</summary>

From the Radon-Nikodym relationship:

$$\mathbb{E}^{\mathbb{Q}}[V] = \mathbb{E}^{\mathbb{P}}\!\left[\frac{d\mathbb{Q}}{d\mathbb{P}} \cdot V\right] = \mathbb{E}^{\mathbb{P}}[Z_T \cdot V]$$

So the option price under $\mathbb{Q}$ is:

$$C_0 = e^{-rT}\mathbb{E}^{\mathbb{Q}}[\text{payoff}(S_T^Q)] = e^{-rT}\mathbb{E}^{\mathbb{P}}[Z_T \cdot \text{payoff}(S_T^P)]$$

**In simulation:**

```python
# Method 1: simulate under Q directly
S_T_Q = S0 * np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
C_Q = np.exp(-r*T) * np.maximum(S_T_Q - K, 0).mean()

# Method 2: simulate under P, weight by Z_T (importance sampling)
S_T_P = S0 * np.exp((mu - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
Z_T = np.exp(-lam*np.sqrt(T)*Z - 0.5*lam**2*T)  # lam = (mu-r)/sigma
C_IS = np.exp(-r*T) * (Z_T * np.maximum(S_T_P - K, 0)).mean()
```

Both converge to the same Black-Scholes price. Method 2 is "importance sampling under Girsanov" — useful when it's easier to simulate under $\mathbb{P}$ than $\mathbb{Q}$, or when you want to price many options from a single set of $\mathbb{P}$-paths.

</details>

---

### Level 3 — Coding

**Q6.** The code verifies $\mathbb{E}^{\mathbb{P}}[Z_T] \approx 1.0$. Why MUST $\mathbb{E}^{\mathbb{P}}[Z_T] = 1$ exactly in theory? What would $\mathbb{E}^{\mathbb{P}}[Z_T] \neq 1$ indicate about the simulation or the model?

<details>
<summary>Answer</summary>

**Why $\mathbb{E}^{\mathbb{P}}[Z_T] = 1$ must hold:**

$Z_T = d\mathbb{Q}/d\mathbb{P}$ is a Radon-Nikodym derivative between two probability measures. For $\mathbb{Q}$ to be a valid probability measure, it must integrate to 1 over all scenarios:

$$\mathbb{E}^{\mathbb{P}}\!\left[\frac{d\mathbb{Q}}{d\mathbb{P}}\right] = \int_\Omega \frac{d\mathbb{Q}}{d\mathbb{P}} \, d\mathbb{P} = \int_\Omega d\mathbb{Q} = \mathbb{Q}(\Omega) = 1$$

$Z_t$ being a martingale under $\mathbb{P}$ with $Z_0 = 1$ ensures $\mathbb{E}^{\mathbb{P}}[Z_T] = Z_0 = 1$ for all $T$.

**What $\mathbb{E}^{\mathbb{P}}[Z_T] \neq 1$ would indicate:**

1. **Novikov condition violated:** if $\lambda$ is too large or time-varying such that $\mathbb{E}^{\mathbb{P}}[e^{\frac{1}{2}\int_0^T \lambda_t^2\,dt}] = \infty$, then $Z_T$ is only a local martingale (not a true martingale), and $\mathbb{E}^{\mathbb{P}}[Z_T] < 1$. The change of measure is not globally valid — $\mathbb{Q}$ is not a probability measure.

2. **Simulation bug:** incorrect formula for $Z_T$ (e.g., wrong sign on $\lambda$, missing the $-\lambda^2 T/2$ term). This is easy to catch because $\mathbb{E}^{\mathbb{P}}[Z_T]$ is a simple diagnostic check.

3. **Bubble model:** in certain bubble models, the stock price process is a strict local martingale under $\mathbb{Q}$, and $\mathbb{E}^{\mathbb{Q}}[S_T/S_0] < 1$ — the discounted price martingale fails. $\mathbb{E}^{\mathbb{P}}[Z_T] < 1$ is the signature.

**Quick diagnostic in code:**
```python
Z_T = np.exp(-lam * W_P - 0.5 * lam**2 * T)
print(f"E^P[Z_T] = {Z_T.mean():.6f}  (should be 1.000)")
# If this is not ≈ 1.0, debug before proceeding
```

</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "Changing from $\mathbb{P}$ to $\mathbb{Q}$ changes the physical price paths" | The sample paths $\omega$ are identical — the same realizations of $W_t$. Only the probability weights (likelihood of each path) change. Think of reweighting a histogram, not redrawing it. |
| "Under $\mathbb{Q}$, investors expect the stock to return $r$" | $\mathbb{Q}$ is a pricing tool, not a description of what investors actually believe. No investor actually expects to earn $r$ — they expect to earn $\mu > r$. The $\mathbb{Q}$-drift $r$ is a mathematical construction for no-arbitrage pricing, not an economic prediction. |
| "Girsanov's theorem only works when $\lambda$ is constant" | Girsanov works for any adapted process $\lambda_t$ satisfying Novikov's condition $\mathbb{E}^{\mathbb{P}}[\exp(\frac{1}{2}\int_0^T \lambda_t^2\,dt)] < \infty$. Time-varying market prices of risk (stochastic $\lambda_t$) arise in factor models and stochastic vol frameworks. |
| "$\sigma$ is different under $\mathbb{P}$ and $\mathbb{Q}$" | $\sigma$ is invariant under the Girsanov measure change — only drifts shift. This is why implied vol (a $\mathbb{Q}$ object) and realized vol (a $\mathbb{P}$ object) are measuring the same underlying volatility structure, even if their values differ due to variance risk premia. |

## Related Concepts

- [[Brownian Motion]]
- [[Martingales]]
- [[Risk-Neutral Measure]]
- [[Stochastic Differential Equations]]
- [[Ito's Lemma]]
- [[Black-Scholes Model]]
- [[Fundamental Theorem of Asset Pricing]]
- [[Change of Numeraire]]

## Sources Used

- Shreve, *Stochastic Calculus for Finance II*, Ch. 5 (Girsanov's theorem and risk-neutral pricing)
- Björk, *Arbitrage Theory in Continuous Time*, Ch. 11–12
- Glasserman, *Monte Carlo Methods in Financial Engineering*, Ch. 4 (importance sampling)

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review: status → evergreen; [[Ito Calculus]] → [[Ito's Lemma]]; last_reviewed updated | QA pass |
