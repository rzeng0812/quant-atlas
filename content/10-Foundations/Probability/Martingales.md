---
type: concept
domain: 10-Foundations
tags: [math, probability]
status: evergreen
stability: stable
confidence: high
last_reviewed: 2026-04-11
review_interval_days: 365
sources:
  - "Shreve Vol I ch.2, ch.4"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Pricing → Gap 4: The derived option price still contains μ — but no one agrees on μ
> **This concept:** Provides the mathematical language of no-arbitrage — discounted prices are martingales under Q, which is what makes the risk-neutral pricing formula valid.
> **Alternative approaches to this gap:** [[Risk-Neutral Measure]] (the practical pricing result); [[Girsanov Theorem]] (the measure-change mechanism — all three work together for Gap 4)
> **You need first:** [[Brownian Motion]], [[Stochastic Differential Equations]]
> **This unlocks:** [[Risk-Neutral Measure]], [[Girsanov Theorem]], [[Black-Scholes Model]], [[Fundamental Theorem of Asset Pricing]]

## Why This Exists

**The gap:** The no-arbitrage principle says you cannot earn a riskless profit above the risk-free rate. But expressing this principle in a rigorous mathematical form — one that works for all derivatives and all trading strategies, not just the specific examples where arbitrage is visually obvious — required a precise framework.

**What came before:** Informal arbitrage arguments on a case-by-case basis: "if the price is too high, sell it and hedge; if too low, buy it and hedge." This worked for simple instruments but could not be systematically applied to complex derivatives, multi-period strategies, or continuous-time models.

**What this adds:** The martingale condition $\mathbb{E}^Q[\tilde{S}_t \mid \mathcal{F}_s] = \tilde{S}_s$ is the mathematical translation of no-arbitrage into a single, checkable property. If discounted prices are Q-martingales, no trading strategy can earn a riskless profit. This directly licenses the pricing formula $V_0 = e^{-rT}\mathbb{E}^Q[H_T]$ — option price equals discounted expected payoff under Q — because any derivation from this formula would violate the martingale property and hence create arbitrage.

**What it still doesn't solve:** The martingale framework tells you the form of the pricing formula and guarantees its consistency, but it does not specify which measure Q to use or how to construct it from the real-world dynamics. That is Gap 4's remaining work, addressed by [[Girsanov Theorem]] (constructing Q) and [[Risk-Neutral Measure]] (applying it).

## Math Concepts

**Filtration.** Let $(\Omega, \mathcal{F}, P)$ be a probability space. A filtration $\{\mathcal{F}_t\}_{t \ge 0}$ is an increasing family of $\sigma$-algebras: $\mathcal{F}_s \subseteq \mathcal{F}_t$ for $s \le t$. Think of $\mathcal{F}_t$ as "all information available up to time $t$."

**Adapted process.** A stochastic process $\{X_t\}$ is adapted if $X_t$ is $\mathcal{F}_t$-measurable for each $t$ — i.e., its value at time $t$ is determined by information available by time $t$, not the future.

**Martingale (formal definition).** An adapted, integrable process $\{X_t\}$ (meaning $E[|X_t|] < \infty$ for all $t$) is a **martingale** with respect to $\{\mathcal{F}_t\}$ and measure $P$ if

$$
E[X_t \mid \mathcal{F}_s] = X_s \quad \text{for all } s \le t.
$$

- $E[\,\cdot \mid \mathcal{F}_s]$: conditional expectation given information up to time $s$.
- $X_s$: the current (known) value — it equals its own conditional expectation trivially.

**Super- and sub-martingales.**
- $E[X_t \mid \mathcal{F}_s] \le X_s$: **supermartingale** (expected to decrease — like a gambler's fortune against a house edge).
- $E[X_t \mid \mathcal{F}_s] \ge X_s$: **submartingale** (expected to increase).

**Brownian motion is a martingale.** If $W_t$ is standard Brownian motion,

$$
E[W_t \mid \mathcal{F}_s] = W_s \quad \text{for } s \le t,
$$

because increments $W_t - W_s$ are independent of $\mathcal{F}_s$ and have mean zero.

**Discounted prices under $Q$.** If $S_t$ is an asset price, $r$ is the risk-free rate, and $Q$ is the risk-neutral measure, then the discounted process $\tilde{S}_t = e^{-rt} S_t$ satisfies

$$
E^Q[\tilde{S}_t \mid \mathcal{F}_s] = \tilde{S}_s,
$$

making $\tilde{S}_t$ a $Q$-martingale. This is the cornerstone of derivative pricing.

**Optional Stopping Theorem (OST).** Let $\tau$ be a stopping time (a random time determined by the process, like "the first time $X$ hits 100"). Under mild integrability conditions,

$$
E[X_\tau] = E[X_0].
$$

This says you cannot gain an expected advantage over a martingale by choosing a clever time to stop — the expected value at stopping equals the starting value. This rules out many naive "beat the market" strategies.

## Walkthrough

**Discrete coin-flip example.** Start with $X_0 = 10$ (your wealth in dollars). Each step: flip a fair coin, win $+1$ on heads, $-1$ on tails.

| Time | $X_t$ (one possible path) | $E[X_{t+1} \mid \mathcal{F}_t]$ |
|------|--------------------------|--------------------------------|
| 0    | 10                        | 10                             |
| 1    | 11 (heads)                | 11                             |
| 2    | 10 (tails)                | 10                             |
| 3    | 11 (heads)                | 11                             |

At every step, regardless of the history of flips, the best prediction of tomorrow's wealth is today's wealth. No pattern in the past helps you.

**OST intuition.** Suppose you decide: "I'll stop the game the first time I'm ahead by \$2." Your wealth when you stop might be \$12. But the OST says $E[X_\tau] = X_0 = 10$ — the strategy cannot raise your *expected* stopping wealth. You might stop at $12$ sometimes, but to compensate you must sometimes be forced to play forever and never reach the target, dragging the expectation back to $10$.

## Analysis

**Key properties.**
- The martingale property is always *relative to a specific measure and filtration* — a process that is a martingale under $P$ may not be one under $Q$.
- Any Ito integral $\int_0^t H_s \, dW_s$ (with appropriate integrability of $H$) is a martingale. This is central to stochastic calculus.
- Martingales can have non-zero quadratic variation: $[W]_t = t$. The martingale property says nothing about variance — only about the conditional mean.

**Common confusions.**
- "Fair game" does not mean $X_t$ stays constant or near its start — it can wander widely. Brownian motion satisfies $E[W_t] = 0$ but $\text{Var}(W_t) = t$ grows without bound.
- The real-world drift of stock prices ($\mu > r$ typically) means $S_t$ itself is *not* a martingale under $P$. It only becomes a martingale (after discounting) under the risk-neutral measure $Q$.
- OST requires integrability conditions. Doubling strategies (bet $1, 2, 4, 8, \ldots$ until you win) appear to violate OST but fail the integrability condition — they require unbounded wealth.

**Efficient Market Hypothesis link.** In a perfectly efficient market, risk-adjusted log-returns should be unpredictable from past returns. Formally, the risk-neutral discounted price is always a martingale; under $P$, log-prices are approximately a martingale plus a drift term $(\mu - r)$.

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)

# ── Discrete coin-flip martingale ──────────────────────────────────────────
n_paths = 5
n_steps = 200
x0 = 10.0

flips = rng.choice([-1, 1], size=(n_paths, n_steps))   # fair coin
wealth = x0 + np.hstack([np.zeros((n_paths, 1)), flips.cumsum(axis=1)])

plt.figure(figsize=(10, 4))
for path in wealth:
    plt.plot(path, alpha=0.6, linewidth=0.8)
plt.axhline(x0, color="black", linewidth=1.2, linestyle="--", label=f"E[X_t] = {x0}")
plt.title("Fair coin-flip martingale — 5 paths")
plt.xlabel("Step")
plt.ylabel("Wealth ($)")
plt.legend()
plt.tight_layout()
plt.show()

# Verify martingale property empirically: E[X_{t+1} | X_t] ≈ X_t
# Average wealth at each step should stay near x0
print("Sample mean of wealth at each step (should ≈ 10):")
print(f"  t=0:   {wealth[:, 0].mean():.2f}")
print(f"  t=50:  {wealth[:, 50].mean():.2f}")
print(f"  t=100: {wealth[:, 100].mean():.2f}")
print(f"  t=200: {wealth[:, 200].mean():.2f}")

# ── Brownian motion as martingale ──────────────────────────────────────────
n_bm_paths = 1000
T = 1.0
n_bm_steps = 252
dt = T / n_bm_steps

dW = rng.normal(0, np.sqrt(dt), size=(n_bm_paths, n_bm_steps))
W = np.hstack([np.zeros((n_bm_paths, 1)), dW.cumsum(axis=1)])

print("\nBrownian motion — E[W_t] (should ≈ 0) and Var[W_t] (should ≈ t):")
for t_idx, t_label in [(0, 0.0), (63, 0.25), (126, 0.5), (252, 1.0)]:
    print(f"  t={t_label:.2f}: E={W[:, t_idx].mean():.4f}, Var={W[:, t_idx].var():.4f}")

# ── Optional Stopping Theorem — can't beat a martingale ───────────────────
# Strategy: stop the first time wealth >= x0 + 2 OR we hit step 500
n_ost = 100_000
max_steps = 500
target_gain = 2

flips_ost = rng.choice([-1, 1], size=(n_ost, max_steps))
paths_ost = x0 + np.hstack([np.zeros((n_ost, 1)), flips_ost.cumsum(axis=1)])

stopping_wealth = []
for path in paths_ost:
    hit = np.where(path >= x0 + target_gain)[0]
    if len(hit):
        stopping_wealth.append(path[hit[0]])
    else:
        stopping_wealth.append(path[-1])  # forced stop

print(f"\nOptional Stopping — target gain = +{target_gain}")
print(f"  E[X_tau] = {np.mean(stopping_wealth):.4f}  (theory: {x0:.1f})")
```

## Bridge to Quant / ML

**Derivatives pricing.** The fundamental theorem of asset pricing states: a market is arbitrage-free if and only if there exists a probability measure $Q$ (the risk-neutral measure) under which all discounted asset prices are martingales. Every derivative price is computed as $V_0 = e^{-rT} E^Q[V_T]$ — a martingale expectation. Without the martingale property, pricing breaks down.

**Hedging.** The martingale representation theorem says every $Q$-martingale adapted to a Brownian filtration can be written as a stochastic integral. This is why every contingent claim can (in theory) be replicated by dynamic delta-hedging — the replicating portfolio is the stochastic integral representation.

**Risk and drawdown.** A portfolio that is a local martingale but not a true martingale (a "strict local martingale") can have $E[X_T] < X_0$ despite satisfying the local condition — this shows up in certain bubble models.

**ML connection.** In reinforcement learning, the value function $V(s_t) = E[\sum_k \gamma^k r_{t+k} \mid s_t]$ is the martingale component of the return sequence. Temporal difference (TD) learning is essentially martingale estimation. Q-learning's Bellman target is a martingale difference equation.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** State the formal definition of a martingale from memory. What property does it encode about the process's future values?

<details>
<summary>Answer</summary>

An adapted, integrable process $\{X_t\}$ on a filtered probability space is a **martingale** with respect to filtration $\{\mathcal{F}_t\}$ if:

$$\mathbb{E}[X_t \mid \mathcal{F}_s] = X_s \quad \text{for all } s \leq t$$

**What it encodes:** The current value is the best prediction of every future value, given all information up to now. There is no exploitable drift — the process is a "fair game." Knowledge of the full history $\mathcal{F}_s$ does not help you predict whether $X$ will be above or below $X_s$ in the future.

This is distinct from: (1) $X_t$ staying constant (it can wander widely), (2) the path being unpredictable in any sense (variance can grow without bound), and (3) being a martingale under all measures (it's always measure-specific).

</details>

---

**Q2.** Is standard Brownian motion $W_t$ a martingale? Is a GBM stock price $S_t$ a martingale under the real-world measure $\mathbb{P}$? Explain the difference.

<details>
<summary>Answer</summary>

**Brownian motion $W_t$ — YES, it is a $\mathbb{P}$-martingale:**

$$\mathbb{E}[W_t \mid \mathcal{F}_s] = \mathbb{E}[W_s + (W_t - W_s) \mid \mathcal{F}_s] = W_s + \mathbb{E}[W_t - W_s] = W_s + 0 = W_s$$

The increment $W_t - W_s$ is independent of $\mathcal{F}_s$ and has mean zero — exactly the martingale condition.

**GBM stock price $S_t$ under $\mathbb{P}$ — NO:**

$S_t = S_0 e^{(\mu - \sigma^2/2)t + \sigma W_t}$. Then $\mathbb{E}[S_t \mid \mathcal{F}_s] = S_s e^{\mu(t-s)} \neq S_s$ when $\mu \neq 0$.

The stock grows at rate $\mu$ on average — it is a *submartingale* if $\mu > 0$.

**The fix:** the discounted price $\tilde{S}_t = e^{-rt} S_t$ IS a martingale under the risk-neutral measure $\mathbb{Q}$ (where drift = $r$). This is the entire foundation of derivative pricing.

</details>

---

**Q3.** State the Optional Stopping Theorem and explain its practical implication for "beat the market" trading strategies.

<details>
<summary>Answer</summary>

**Optional Stopping Theorem:** Let $\{X_t\}$ be a martingale and $\tau$ be a stopping time (a random time determined only by the process history, not future values). Under mild integrability conditions:

$$\mathbb{E}[X_\tau] = \mathbb{E}[X_0]$$

The expected value at any cleverly chosen stopping time equals the starting value.

**Implication for trading:** The OST rules out strategies like "keep trading until you're profitable" as a systematic edge over a martingale. Even if you stop the first time your wealth hits some target $W_0 + a$, OST guarantees that the scenarios where you never hit the target (and eventually stop at the forced boundary) drag $\mathbb{E}[X_\tau]$ back to $W_0$.

**The doubling strategy counter-example:** Double your bet after each loss — the strategy eventually wins with probability 1. But OST is not violated because the integrability condition fails: the strategy requires unbounded capital (infinite expected maximum drawdown). It's a local martingale that fails to be a true martingale. Any realistic finite-wealth constraint prevents the strategy from working in expectation.

</details>

---

### Level 2 — Quantitative

**Q4.** A fair coin game starts at $X_0 = 10$. You play for exactly 100 steps ($+1$ or $-1$ equally).

a) What is $\mathbb{E}[X_{100}]$?
b) What is $\text{Var}(X_{100})$?
c) What is the approximate probability that $X_{100} > 20$?

<details>
<summary>Answer</summary>

**a)** By the martingale property: $\mathbb{E}[X_{100}] = X_0 = 10$.

**b)** Each step contributes variance 1 (since $(\pm 1)^2 = 1$ and increments are independent):
$$\text{Var}(X_{100}) = 100 \times 1 = 100 \implies \text{std}(X_{100}) = 10$$

**c)** $X_{100} = 10 + \sum_{i=1}^{100} \xi_i$ where $\xi_i \in \{-1, +1\}$ i.i.d. By CLT, $X_{100} \approx \mathcal{N}(10, 100)$.

$$P(X_{100} > 20) = P\!\left(Z > \frac{20 - 10}{10}\right) = P(Z > 1) \approx 1 - \Phi(1) \approx 15.9\%$$

Note: variance grows linearly, but std grows as $\sqrt{t}$ — a martingale can wander far from its start even though its expected value stays fixed.

</details>

---

**Q5.** You play the fair coin game ($X_0 = 10$) and decide to stop the first time your wealth reaches $15$ or falls to $5$. Let $\tau$ be this stopping time.

a) What does OST predict for $\mathbb{E}[X_\tau]$?
b) Compute $P(X_\tau = 15)$ and $P(X_\tau = 5)$.

<details>
<summary>Answer</summary>

**a)** OST predicts $\mathbb{E}[X_\tau] = X_0 = 10$.

**b)** The boundaries are $a = 15$ (upper, gain = $+5$) and $b = 5$ (lower, loss = $-5$). For a symmetric random walk starting at $x = 10$ with absorbing barriers at $a$ and $b$:

$$P(\text{hit upper barrier}) = \frac{x - b}{a - b} = \frac{10 - 5}{15 - 5} = \frac{5}{10} = 50\%$$

$$P(\text{hit lower barrier}) = \frac{a - x}{a - b} = \frac{15 - 10}{10} = 50\%$$

**Verify OST:** $\mathbb{E}[X_\tau] = 0.5 \times 15 + 0.5 \times 5 = 7.5 + 2.5 = 10 = X_0$. ✓

The symmetric starting point means equal probability of winning and losing — no edge, consistent with the OST.

</details>

---

### Level 3 — Coding

**Q6.** The OST simulation uses `max_steps = 500` as a forced cutoff. Why is this cutoff necessary, and what happens to `E[X_tau]` if `max_steps` is too small?

<details>
<summary>Answer</summary>

**Why it's necessary:** The OST proof requires integrability conditions — specifically, the stopping time must be finite (or the process must be bounded until stopping). In simulation, some paths may not hit the target gain of $+2$ within any finite window (they wander below the target indefinitely). Without `max_steps`, those paths would run forever and the simulation would never terminate.

**What happens if `max_steps` is too small:** If many paths haven't yet hit $X_0 + 2$ when they're forced to stop, they're stopped early at whatever value they currently have — often below 10 (they've been "punished" for not reaching the target). The forced stops are concentrated at values $< X_0 + 2$, pulling the sample mean $\mathbb{E}[X_\tau]$ **below** $X_0 = 10$.

**The OST guarantee is asymptotic:** as `max_steps → ∞`, paths that didn't hit the target eventually return to lower levels (random walk recurrence), and the overall mean converges to $X_0$. A truncation at small `max_steps` introduces a downward bias because it samples the "lucky" (hit target) and "unlucky-so-far" (forced stop at low value) paths unequally.

```python
# Demonstrate: try max_steps = 20 vs 500
# With max_steps=20, E[X_tau] will be noticeably below 10
# With max_steps=500, it converges close to 10
```

</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "A martingale stays near its starting value" | $\mathbb{E}[X_t] = X_0$ but $\text{Var}(X_t)$ grows over time. Paths can wander arbitrarily far — the *average* across all paths stays at $X_0$, not individual paths. |
| "GBM stock prices are martingales" | Only the *discounted* price $e^{-rt}S_t$ is a martingale, and only under $\mathbb{Q}$. Under $\mathbb{P}$, undiscounted stock prices are submartingales (trending upward). |
| "The doubling strategy beats a martingale" | It fails the OST's integrability condition — it requires potentially unbounded wealth. In reality, any finite bankroll limit makes the strategy have negative expected value once the ruin scenario is included. |
| "Martingale property implies no drift in any sense" | Only conditional drift is zero — the *unconditional* distribution of $X_t$ can be highly skewed or fat-tailed. The variance of a martingale can grow without bound. |

## Related Concepts

- [[Brownian Motion]]
- [[Risk-Neutral Measure]]
- [[Girsanov Theorem]]
- [[Ito's Lemma]]
- [[Stochastic Differential Equations]]
- [[Fundamental Theorem of Asset Pricing]]
- [[Black-Scholes Model]]

## Sources Used

- Shreve, *Stochastic Calculus for Finance I*, Ch. 2 (discrete martingales), Ch. 4 (continuous martingales)
- Shreve, *Stochastic Calculus for Finance II*, Ch. 1 (general theory)
- Williams, *Probability with Martingales*, Cambridge University Press

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review: status → evergreen; [[Ito Calculus]] → [[Ito's Lemma]]; dead code removed from wealth simulation; last_reviewed updated | QA pass |
