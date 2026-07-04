---
type: concept
domain: 10-Foundations
tags: [math, probability, derivatives]
status: evergreen
stability: stable
confidence: high
last_reviewed: 2026-04-11
review_interval_days: 365
sources:
  - "Hull ch.13"
  - "Shreve Vol II ch.5"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Pricing → Gap 4: The derived option price still contains μ — but no one agrees on μ
> **This concept:** Removes μ from option prices entirely by pricing in a fictional world where every asset grows at r — the practical application of the no-arbitrage principle to derivatives valuation.
> **Alternative approaches to this gap:** [[Girsanov Theorem]] (the rigorous mathematical mechanism behind this measure change); [[Martingales]] (the mathematical language that makes the pricing formula consistent)
> **You need first:** [[Brownian Motion]], [[Geometric Brownian Motion]], [[Ito's Lemma]], [[Martingales]]
> **This unlocks:** [[Black-Scholes Model]], [[Implied Volatility]], [[Girsanov Theorem]], all derivatives pricing models

## Why This Exists

**The gap:** Applying Ito's Lemma to a hedged option portfolio produces a formula that depends on $\mu$, the stock's real-world expected return. Since every investor estimates $\mu$ differently, there is no agreed option price — the same fundamental problem that motivated no-arbitrage pricing in the first place, reappearing in mathematical form.

**What came before:** Attempting to price options using expected-return discounting — estimating where the stock would go, computing the expected payoff, and discounting at a risk-adjusted rate. This produced a price that depended on the investor's subjective view of the stock's prospects. No two investors agreed, and the market could not function.

**What this adds:** By switching to a probability measure Q in which the stock drifts at the risk-free rate r instead of μ, the option price becomes $V_0 = e^{-rT}\mathbb{E}^Q[H_T]$ — with no μ anywhere. Both investors, regardless of their real-world return expectations, agree on this price, because the drift difference (μ − r) is exactly the risk premium that gets hedged away when you replicate the option. The volatility σ is unchanged across measures, so the pricing formula depends only on r, σ, S₀, K, and T — all observable or agreed-upon quantities.

**What it still doesn't solve:** The risk-neutral framework prices options correctly only when markets are complete — when every payoff can be replicated by dynamic hedging. With jumps, stochastic volatility without full hedging instruments, or missing assets, multiple valid risk-neutral measures exist and prices are no longer unique. This is the domain of model risk, addressed by [[Heston Model]], [[Merton Jump-Diffusion]], and [[Volatility Smile]].

## Math Concepts

**Setup:** in the real world, a stock follows GBM with drift $\mu$:

$$dS_t = \mu S_t\,dt + \sigma S_t\,dW_t^P$$

where $W_t^P$ is Brownian motion under the real-world measure $\mathbb{P}$.

**The risk-neutral measure $\mathbb{Q}$** is a different probability measure — same events, different probabilities — chosen so that all discounted asset prices are [[Martingales]]:

$$\frac{S_t}{e^{rt}} \text{ is a martingale under } \mathbb{Q}$$

Under $\mathbb{Q}$, the stock grows at $r$ (not $\mu$):

$$dS_t = r S_t\,dt + \sigma S_t\,dW_t^Q$$

The drift changed from $\mu$ to $r$. The volatility $\sigma$ is unchanged — this is key.

**Pricing formula:** the price of any derivative with payoff $H_T$ at time $T$ is:

$$V_0 = e^{-rT}\,\mathbb{E}^{\mathbb{Q}}[H_T]$$

Price = discounted expected payoff under the risk-neutral measure. No $\mu$ anywhere.

**How the measures connect:** [[Girsanov Theorem]] tells us how to move between $\mathbb{P}$ and $\mathbb{Q}$. The change is achieved by shifting the Brownian motion's drift by the *market price of risk* $\lambda = (\mu - r)/\sigma$.

## Walkthrough

Suppose a stock is at $S_0 = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 1$ year.

Under $\mathbb{Q}$: $S_T = 100 \cdot \exp\!\left[(0.05 - 0.02)\cdot 1 + 0.2 Z\right]$, $Z \sim \mathcal{N}(0,1)$.

Price a call with strike $K = 105$:

$$C_0 = e^{-0.05} \cdot \mathbb{E}^{\mathbb{Q}}[\max(S_T - 105,\ 0)]$$

We don't need to know the stock's real expected return to compute this — only $r$, $\sigma$, $S_0$, $K$, $T$. The [[Black-Scholes Model]] gives the closed form for this expectation.

## Analysis

- **"Fictional" doesn't mean "wrong":** the risk-neutral measure is a mathematical tool, not a belief about the world. It gives the *correct arbitrage-free price*.
- **$\sigma$ is the same in both worlds:** only drift changes. This means [[Implied Volatility]] — inferred from market prices under $\mathbb{Q}$ — tells you something real about uncertainty, even though the measure is fictional.
- **No unique measure with incomplete markets:** risk-neutral pricing works cleanly only when the market is complete (every payoff is replicable). With jumps, stochastic vol, or missing instruments, multiple risk-neutral measures exist → option prices are not unique → this is why model risk exists.
- **Connection to no-arbitrage:** the existence of a risk-neutral measure is *equivalent* to the absence of arbitrage (First Fundamental Theorem of Asset Pricing).

## Implementation

```python
import numpy as np

def risk_neutral_call_mc(S0, K, r, sigma, T, n_sims=100_000, seed=42):
    """Price a European call via risk-neutral Monte Carlo."""
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal(n_sims)
    # Simulate S_T under Q (drift = r, not mu)
    S_T = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    payoff = np.maximum(S_T - K, 0)
    return np.exp(-r * T) * payoff.mean()

print(risk_neutral_call_mc(100, 105, 0.05, 0.20, 1.0))
# Compare to Black-Scholes closed form — should match closely
```

## Bridge to Quant / ML

- Every options pricing model (BSM, Heston, SABR) operates under a risk-neutral measure
- [[Implied Volatility]] is the $\sigma$ that makes the BSM risk-neutral price match the market price — it's a measure-$\mathbb{Q}$ object
- In ML finance, models trained to predict *real-world* returns live under $\mathbb{P}$; pricing models live under $\mathbb{Q}$. Confusing the two is a common source of errors

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** A stock has real-world drift $\mu = 8\%$ and the risk-free rate is $r = 3\%$. Under the risk-neutral measure $\mathbb{Q}$, what is the stock's drift? Why does it change?

<details>
<summary>Answer</summary>

Under $\mathbb{Q}$, the stock's drift becomes $r = 3\%$ — not the real-world 8%.

**Why it changes:** The risk-neutral measure is constructed precisely so that all discounted asset prices $e^{-rt} S_t$ are martingales. For $S_t/e^{rt}$ to have zero drift, $S_t$ itself must drift at $r$. This is achieved by the Girsanov theorem, which shifts the Brownian motion by the market price of risk $\lambda = (\mu - r)/\sigma$, changing the drift from $\mu$ to $r$ while leaving $\sigma$ unchanged.

The key insight: the risk premium $\mu - r$ is the excess return investors demand for bearing risk. Under $\mathbb{Q}$, this premium is removed — it's "priced away" because any payoff can be replicated by hedging.

</details>

---

**Q2.** Why does the Black-Scholes option price contain no $\mu$ (the real-world drift)? Intuitively, shouldn't a stock with a higher expected return produce more valuable call options?

<details>
<summary>Answer</summary>

The option price is independent of $\mu$ because **a perfectly hedged position has no exposure to the stock's drift**.

**The replication argument:** if you hold an option and continuously delta-hedge with the stock, the hedge eliminates all exposure to $\mu$. Two investors who disagree about whether $\mu = 5\%$ or $\mu = 15\%$ will still agree on the option price — because both can hedge it perfectly, and the hedged portfolio earns exactly $r$ regardless of $\mu$.

Formally: under $\mathbb{Q}$ all assets grow at $r$, so the option price is just $e^{-rT}\mathbb{E}^{\mathbb{Q}}[\text{payoff}]$, which involves only $r$, $\sigma$, $S_0$, $K$, $T$ — no $\mu$.

**The intuition:** a higher $\mu$ does mean $S_T$ is larger on average — but under $\mathbb{Q}$ that "optimism" is exactly neutralized by down-weighting those favorable scenarios in the risk-neutral probabilities. The net effect on the price is zero.

</details>

---

**Q3.** What does it mean formally for discounted prices to be $\mathbb{Q}$-martingales? What breaks if they weren't?

<details>
<summary>Answer</summary>

Formally: $\tilde{S}_t = e^{-rt} S_t$ is a $\mathbb{Q}$-martingale if $\mathbb{E}^{\mathbb{Q}}[\tilde{S}_t \mid \mathcal{F}_s] = \tilde{S}_s$ for all $s \leq t$. The discounted price today is the best forecast of the discounted price tomorrow, under $\mathbb{Q}$.

**What breaks if they weren't:** if $e^{-rt} S_t$ had a positive drift under $\mathbb{Q}$, you could borrow at $r$, buy the stock, and earn a riskless profit above $r$ — that is arbitrage. The **First Fundamental Theorem of Asset Pricing** makes this rigorous: a market is arbitrage-free if and only if a risk-neutral measure (equivalent martingale measure) exists. The martingale property IS the mathematical expression of no-arbitrage.

</details>

---

### Level 2 — Quantitative

**Q4.** $S_0 = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 1$ year.

a) Under $\mathbb{Q}$, what is the distribution of $\ln(S_T / S_0)$?
b) Compute $\mathbb{E}^{\mathbb{Q}}[S_T]$.
c) Compute $\mathbb{Q}(S_T > 110)$.

<details>
<summary>Answer</summary>

**a)** Under $\mathbb{Q}$, the stock follows GBM with drift $r$, so:

$$\ln(S_T / S_0) \sim \mathcal{N}\!\left(\left(r - \tfrac{\sigma^2}{2}\right)T,\ \sigma^2 T\right) = \mathcal{N}\!\left((0.05 - 0.02)\times 1,\ 0.04\right) = \mathcal{N}(0.03,\ 0.04)$$

Standard deviation: $\sqrt{0.04} = 0.20$.

**b)** $\mathbb{E}^{\mathbb{Q}}[S_T] = S_0 e^{rT} = 100 \cdot e^{0.05} \approx \$105.13$.

The stock grows at $r$ under $\mathbb{Q}$ (not at $\mu$ — $\mu$ is irrelevant here).

**c)** $\mathbb{Q}(S_T > 110) = \mathbb{Q}(\ln(S_T/100) > \ln 1.1)$

$$= \mathbb{Q}\!\left(Z > \frac{\ln 1.1 - 0.03}{0.20}\right) = \mathbb{Q}\!\left(Z > \frac{0.0953 - 0.03}{0.20}\right) = \mathbb{Q}(Z > 0.327)$$

$$= 1 - \Phi(0.327) \approx 1 - 0.628 = 37.2\%$$

Note: this is the $\mathbb{Q}$-probability of finishing in-the-money, which is related to $N(d_2)$ in the Black-Scholes formula.

</details>

---

**Q5.** $\mu = 12\%$, $r = 4\%$, $\sigma = 25\%$. A path ends with $W_T^P = 0.8$ at $T = 1$.

a) Compute the market price of risk $\lambda$.
b) Compute the Radon-Nikodym weight $Z_T$ for this path.
c) Is this path up-weighted or down-weighted under $\mathbb{Q}$?

<details>
<summary>Answer</summary>

**a)** $\lambda = (\mu - r)/\sigma = (0.12 - 0.04)/0.25 = 0.08/0.25 = 0.32$.

The stock earns 0.32 units of excess return per unit of vol — a Sharpe ratio of 0.32.

**b)** $Z_T = \exp\!\left(-\lambda W_T^P - \tfrac{1}{2}\lambda^2 T\right) = \exp(-0.32 \times 0.8 - 0.5 \times 0.32^2 \times 1)$

$= \exp(-0.256 - 0.0512) = \exp(-0.3072) \approx 0.735$

**c)** Down-weighted: $Z_T \approx 0.735 < 1$. This path has $W_T^P > 0$, meaning the stock moved favorably (above the risk-free rate). Under $\mathbb{Q}$, scenarios with large positive Brownian increments — where the risky asset did well — are down-weighted. The risk-neutral measure "penalizes" scenarios that were too good, shifting the center of mass of the distribution leftward so the mean drift becomes $r$.

</details>

---

### Level 3 — Coding

**Q6.** The implementation simulates $S_T$ under $\mathbb{Q}$ using drift $r$. If you mistakenly used drift $\mu$ instead:

```python
# Bug: using real-world drift instead of r
S_T = S0 * np.exp((mu - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
price = np.exp(-r * T) * np.maximum(S_T - K, 0).mean()
```

Would the computed price be too high, too low, or the same? By approximately how much?

<details>
<summary>Answer</summary>

**Too high** — using $\mu > r$ inflates the simulated stock prices, which inflates the call payoffs.

**Magnitude:** The terminal stock distribution under the wrong simulation has log-mean $(\mu - \sigma^2/2)T$ instead of the correct $(r - \sigma^2/2)T$. The center of the lognormal shifts up by $(\mu - r)T$.

For $\mu = 0.12$, $r = 0.04$, $T = 1$: the wrong simulation overestimates $E[S_T]$ by factor $e^{(\mu-r)T} = e^{0.08} \approx 1.083$. For an at-the-money call, this roughly inflates the price by $\sim 8\%$ of the stock — a large error.

**Why this is wrong:** the risk-neutral pricing formula requires the expectation under $\mathbb{Q}$, where drift = $r$. Using drift = $\mu$ computes an expectation under $\mathbb{P}$ instead, which does NOT give the no-arbitrage price. The correct formula is $V_0 = e^{-rT}\mathbb{E}^{\mathbb{Q}}[\text{payoff}]$ — you must simulate under $\mathbb{Q}$.

</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "The risk-neutral measure describes what investors actually expect" | $\mathbb{Q}$ is a mathematical construct for pricing, not a belief about the world. Real-world beliefs live under $\mathbb{P}$. |
| "Since $\mu$ doesn't appear in option prices, volatility is the only thing that matters" | $r$, $S_0$, $K$, and $T$ also matter — $\mu$ specifically drops out because of hedgeability, not because nothing else matters. |
| "The risk-neutral measure is unique" | Only in complete markets (every payoff replicable). With jumps, stochastic vol without full hedging instruments, or missing assets, multiple risk-neutral measures exist — pricing is no longer unique. |
| "Implied volatility is a $\mathbb{P}$ object" | No — implied vol is the $\sigma$ that makes the BSM $\mathbb{Q}$-price match the market price. It's entirely a $\mathbb{Q}$ construct, even if its numerical value is close to realized vol under $\mathbb{P}$. |

## Related Concepts
- [[Martingales]] — discounted prices are martingales under $\mathbb{Q}$
- [[Girsanov Theorem]] — the mathematical tool for changing from $\mathbb{P}$ to $\mathbb{Q}$
- [[Black-Scholes Model]] — applies this framework to price European options
- [[Geometric Brownian Motion]] — the price process under both measures; only drift changes
- [[Implied Volatility]] — extracted from market prices using the $\mathbb{Q}$ framework

## Sources Used
- Hull — *Options, Futures & Other Derivatives*, ch.13
- Shreve — *Stochastic Calculus for Finance II*, ch.5

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | Hull ch.13 + Shreve II ch.5 |
| 2026-04-11 | QA review: status → evergreen; path wikilink removed; last_reviewed updated | QA pass |
