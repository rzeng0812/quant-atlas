---
type: concept
domain: 30-Models
tags: [derivatives, options, pricing]
status: math
stability: evolving
confidence: high
last_reviewed: 2026-04-18
review_interval_days: 90
sources:
  - "Hull, Options, Futures, and Other Derivatives, ch. 26"
  - "Shreve, Stochastic Calculus for Finance II, ch. 5"
created: 2026-04-18
---

> Payoffs beyond vanilla: path-dependent (Asian, barrier, lookback), digital, and multi-asset options. Mostly priced by Monte Carlo or PDE with modified boundary conditions.

> [!info] Problem Chain
> **Chain:** Pricing → Gap 6: Many contracts have no closed-form solution
> **This concept:** The application domain that motivates Gap 6 — exotic options require path-dependent payoff evaluation that BSM's closed-form cannot provide; demonstrates why numerical methods (Monte Carlo, PDE, binomial tree) exist
> **Alternative approaches to this gap:** [[Numerical Methods PDE]] (Solution A — for 1D barriers, digitals), [[Monte Carlo Methods]] (Solution B — for path-dependent exotics), [[Binomial Tree Model]] (Solution C — for Bermudan exercise)
> **You need first:** [[Black-Scholes Model]], [[Monte Carlo Methods]], [[Numerical Methods PDE]], [[Binomial Tree Model]]
> **This unlocks:** structured products, variance swaps, convertible bonds — any instrument whose payoff depends on the path of the underlying

## Why This Exists

**The gap:** BSM's closed-form formula prices options whose payoff depends only on the stock price at a single future date (S_T). But real hedging needs are messier: a corporate treasurer cares about the average exchange rate over a year, not the rate on one day. A commodity producer wants protection only if prices fall through a disaster threshold. A convertible bond holder wants the right to convert on multiple specific dates. None of these fit BSM's single-date payoff structure.

**What came before:** Vanilla put and call options, priced by BSM, were the primary hedging instruments available. Practitioners needing to hedge average prices or conditional exposures had to approximate these needs with combinations of vanilla options — an imperfect and often expensive solution.

**What this adds:** Exotic options expand the contract space to match real-world hedging needs precisely. Asian options pay on the average price (cheaper, more natural for cash-flow hedgers). Barrier options activate or deactivate based on whether the stock crosses a threshold (cheaper than vanilla puts, matching the intuition "I only need protection in disaster scenarios"). Lookback options give the best possible entry price. The cost is that these contracts cannot be priced by BSM's formula — they require numerical methods: Monte Carlo for path-dependent payoffs, PDE with modified boundary conditions for barriers, backward induction on trees for Bermudan exercise.

**What it still doesn't solve:** Exotic options are far more sensitive to model choice than vanilla options. A barrier option's price depends critically on the assumed vol dynamics near the barrier level — BSM gives one answer, Heston gives another, local vol gives a third. This "model risk" for exotics is much larger than for vanilla options and requires careful model selection and stress-testing.

---

## Math Concepts

### Taxonomy of Exotics

**1. Path-Dependent Options** — payoff depends on the *path* of $S_t$, not just $S_T$

| Type | Payoff | Key Feature |
|------|--------|-------------|
| Asian (arithmetic avg) | $\max\!\left(\frac{1}{N}\sum S_{t_i} - K,\, 0\right)$ | Average reduces variance vs. vanilla |
| Asian (geometric avg) | $\max\!\left(\left(\prod S_{t_i}\right)^{1/N} - K,\, 0\right)$ | Has analytic BSM-style formula |
| Barrier knock-out call | $\max(S_T - K, 0) \cdot \mathbf{1}\{S_t < H\ \forall\, t\}$ | Dies if stock ever hits barrier $H$ |
| Barrier knock-in put | $\max(K - S_T, 0) \cdot \mathbf{1}\{\exists\, t : S_t \leq H\}$ | Only activates if stock hits barrier $H$ |
| Lookback (floating) | $\max(S_T - \min_t S_t,\, 0)$ | Always the best possible entry |
| Lookback (fixed) | $\max(\max_t S_t - K,\, 0)$ | Best price vs. fixed strike |

**2. Digital / Binary Options**

$$\text{Digital call payoff} = \begin{cases} 1 & \text{if } S_T > K \\ 0 & \text{otherwise} \end{cases}$$

A digital call is a bet on $S_T > K$. Its risk-neutral price equals the risk-neutral probability $Q(S_T > K)$, discounted:

$$V_{\text{digital}} = e^{-rT} \cdot \mathcal{N}(d_2)$$

where $d_2$ is the standard BSM $d_2 = \frac{\ln(S/K) + (r - \frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}$.

**3. Multi-Asset Options**

- **Basket option:** payoff on a weighted average of $n$ assets
- **Spread option:** payoff on $\max(S_1 - S_2 - K, 0)$ — used in energy markets (crack spread)
- **Quanto option:** payoff in a foreign currency but measured in domestic

**4. Time / Exercise Exotics**

- **Bermudan option:** can exercise on a discrete set of dates (between European and American)
- **Compound option:** an option on an option (e.g., a call on a call)
- **Chooser option:** holder can choose at time $t^*$ whether it is a call or put

### Pricing Methods

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| Monte Carlo | Path-dependent, multi-asset | Flexible, scalable | Slow convergence ($1/\sqrt{N}$), no early exercise |
| PDE / FDM | 1D, American, barriers | Fast, handles early exercise | Hard to extend beyond 2 assets |
| Closed form | Geometric-average Asian, digital, some barriers | Exact, instant | Only works for specific payoffs |
| Fourier / characteristic functions | Affine models (Heston) | Very fast for vanilla + some exotics | Requires characteristic function |

### Closed Form: Barrier Option (Down-and-Out Call)

For a down-and-out call with barrier $H < S_0$, $H < K$, under BSM assumptions, the price is:

$$C_{\text{out}} = C_{\text{BSM}} - \left(\frac{H}{S_0}\right)^{2r/\sigma^2 - 1} \cdot C_{\text{BSM}}\!\left(H^2/S_0, K, r, \sigma, T\right)$$

The exact formula uses the reflection principle on Brownian motion. For most practitioners, numerical methods are more robust than memorizing this formula.

### Parity: Knock-In + Knock-Out = Vanilla

A fundamental identity: if you hold both a knock-in and a knock-out barrier option with the same parameters, you own a vanilla option. This is because exactly one of them will be active at expiry:

$$C_{\text{knock-in}} + C_{\text{knock-out}} = C_{\text{vanilla}}$$

This lets you price one from the other if you have either a formula or a numerical price for the vanilla.

---

## Walkthrough

### Case 1: Asian Call — Cheaper than Vanilla

Suppose $S_0 = 100$, $K = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 1$ year, monthly averaging (12 dates).

- Vanilla European call (BSM): approximately $\$10.45$
- Asian call (arithmetic average): approximately $\$6.00 - \$7.00$

**Why cheaper?** The arithmetic average of a random process has lower volatility than the process itself. A portfolio that is diversified in time has less variance. So the Asian option's effective volatility is roughly $\sigma / \sqrt{3} \approx 11.5\%$ (a rough approximation), giving a lower option price.

**Used by:** corporate FX desks, commodity hedgers — they naturally care about average prices, not spot on one date.

### Case 2: Barrier Option — Cheaper Downside Protection

Suppose you want a put with $K = 100$, but you believe the stock will only need protection if it falls below $H = 80$. A **knock-in put** (only activates below $H = 80$) costs significantly less than a vanilla put. You give up protection in the scenario where the stock falls gradually to, say, 85 and never breaches 80 — but that scenario may be unlikely enough to accept.

### Case 3: Digital Call — Pure Probability Bet

A digital call paying $\$1$ if $S_T > 100$ is a direct bet on the probability of the stock being above strike at expiry. This is related to the *delta* of a vanilla call (in fact, the digital call is the derivative of the vanilla call price with respect to $K$). Dealers use this in structured products to create step-payoff certificates.

---

## Analysis

### Risk and Greeks of Exotics

Exotic options have unusual, sometimes violent, Greek profiles:

- **Barrier options near the barrier:** delta and gamma blow up as $S_t \to H$. The knock-out delta can flip sign abruptly — hedging is extremely difficult near the barrier.
- **Digital options near expiry:** delta spikes to infinity as $S_T \to K$ at expiry — the payoff jumps from 0 to 1 over an infinitesimal move. In practice, dealers approximate digitals with tight call spreads to manage this.
- **Lookback options:** always expensive — they give you the most favorable price on the entire path. Premium is roughly $2\times$ the vanilla for similar parameters.

### Model Sensitivity

Exotic prices are far more sensitive to model assumptions than vanillas:

- **Barrier options** are sensitive to the assumed local volatility surface (not just the at-the-money vol). A flat BSM vol is often inadequate — use [[Local Volatility]] or [[Heston Model]] for barrier pricing.
- **Asian options** are sensitive to volatility term structure and correlation assumptions for multi-asset versions.
- **Lookback options** are sensitive to the *continuity* assumption: continuous-path lookback vs. discrete observation gives different prices.

### Practical Usage

| Exotic Type | Who Uses It | Why |
|-------------|-------------|-----|
| Asian | Corporates, commodity hedgers | Average price = average cash flow |
| Barrier | Insurance sellers, structured products | Lower premium, conditional protection |
| Digital | Structured products, credit derivatives | Binary payout profiles |
| Lookback | Very expensive; mainly theoretical / retail structured notes | "Best price" guarantee |
| Bermudan | Callable bonds, mortgage prepayment | Periodic exercise rights |
| Basket | Index-linked products, fund replication | Exposure to a portfolio |

---

## Implementation

```python
import numpy as np
from scipy.stats import norm

# ─── Setup: Common BSM Parameters ─────────────────────────────────────────────

S0     = 100.0   # initial stock price
K      = 100.0   # strike
r      = 0.05    # risk-free rate
sigma  = 0.20    # volatility
T      = 1.0     # time to expiry (years)
H      = 85.0    # barrier level (for barrier option)
N_paths = 200_000
N_steps = 252    # daily steps
rng = np.random.default_rng(42)

dt = T / N_steps


# ─── Simulate GBM Paths ───────────────────────────────────────────────────────

def simulate_gbm_paths(S0, r, sigma, T, N_steps, N_paths, rng):
    """Return array of shape (N_paths, N_steps+1) of stock prices."""
    Z = rng.standard_normal((N_paths, N_steps))
    log_increments = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
    log_paths = np.concatenate(
        [np.zeros((N_paths, 1)), np.cumsum(log_increments, axis=1)], axis=1
    )
    return S0 * np.exp(log_paths)


S_paths = simulate_gbm_paths(S0, r, sigma, T, N_steps, N_paths, rng)
S_T = S_paths[:, -1]  # terminal prices


# ─── BSM Vanilla Call (benchmark) ────────────────────────────────────────────

def bsm_call(S, K, r, sigma, T):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)

vanilla_analytic = bsm_call(S0, K, r, sigma, T)
vanilla_mc = np.exp(-r*T) * np.mean(np.maximum(S_T - K, 0))
print(f"Vanilla call  — Analytic: {vanilla_analytic:.4f}  MC: {vanilla_mc:.4f}")


# ─── Asian Call (arithmetic average) ─────────────────────────────────────────

S_avg = np.mean(S_paths, axis=1)  # arithmetic average of each path
asian_payoffs = np.maximum(S_avg - K, 0)
asian_price = np.exp(-r*T) * np.mean(asian_payoffs)
print(f"Asian call    — MC price:  {asian_price:.4f}  (vanilla={vanilla_analytic:.4f})")


# ─── Knock-Out Barrier Call (down-and-out) ────────────────────────────────────

min_prices = np.min(S_paths, axis=1)       # minimum price on each path
survived   = (min_prices > H).astype(float)  # 1 if never hit barrier
barrier_payoffs = np.maximum(S_T - K, 0) * survived
barrier_price = np.exp(-r*T) * np.mean(barrier_payoffs)
print(f"Barrier call  — MC price:  {barrier_price:.4f}  (barrier H={H}, vanilla={vanilla_analytic:.4f})")


# ─── Digital Call ─────────────────────────────────────────────────────────────

digital_mc = np.exp(-r*T) * np.mean((S_T > K).astype(float))
d2 = (np.log(S0/K) + (r - 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
digital_analytic = np.exp(-r*T) * norm.cdf(d2)
print(f"Digital call  — Analytic: {digital_analytic:.4f}  MC: {digital_mc:.4f}")


# ─── Compare All Prices ───────────────────────────────────────────────────────

import matplotlib.pyplot as plt

labels  = ["Vanilla", "Asian (avg)", "Knock-Out Barrier\n(H=85)", "Digital (×10)"]
prices  = [vanilla_analytic, asian_price, barrier_price, digital_analytic * 10]
colors  = ["steelblue", "darkorange", "green", "purple"]

plt.figure(figsize=(9, 5))
bars = plt.bar(labels, prices, color=colors, edgecolor="black", width=0.5)
plt.ylabel("Option Price ($)")
plt.title("Exotic Options vs Vanilla — MC Prices\n(S=100, K=100, r=5%, σ=20%, T=1yr)")
for bar, price in zip(bars, prices):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
             f"${price:.2f}", ha="center", fontsize=10)
plt.ylim(0, max(prices) * 1.2)
plt.tight_layout()
plt.savefig("exotic_options_prices.png", dpi=150)
plt.show()
```

**Expected output order:** Vanilla > Asian > Knock-Out Barrier > Digital (scaled). The Asian and barrier options are materially cheaper than vanilla — illustrating their value as hedging instruments.

---

## Bridge to Quant / ML

- **Monte Carlo is the primary tool:** Most exotic payoffs cannot be expressed as a PDE boundary condition in closed form. [[Monte Carlo Methods]] handles them all by simulating paths. The accuracy tradeoff: $N$ paths gives $O(1/\sqrt{N})$ error.
- **Variance reduction matters:** For expensive exotics (lookbacks, high-dimensional baskets), raw Monte Carlo is too slow. Antithetic variates, control variates (use vanilla as control), quasi-Monte Carlo (Sobol sequences) are standard variance reduction techniques.
- **PDE for American exotics:** [[Numerical Methods PDE|Finite difference methods]] price barrier options via modified boundary conditions (set $V = 0$ on the barrier grid points). American exotic options (Bermudan) use the early exercise condition at each grid point.
- **Greeks via bump-and-reprice or pathwise:** For exotic options, analytic Greeks are unavailable. Traders use finite difference bumping (re-run the MC with $S_0 + \epsilon$) or the **pathwise differentiation** method for pathwise-differentiable payoffs.
- **Structured products:** Banks engineer products with exotic payoff profiles — principal-protected notes, autocallables — by combining vanilla and exotic options. Understanding exotic pricing is essential for structuring.
- **Neural network pricing:** Approximate exotic option prices with neural networks (Deep Hedging, Neural SDE). Input: $(S_0, K, T, \sigma, \text{barrier})$. Output: price. Fast inference for real-time risk management. See [[Deep Hedging]].

---

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why is an Asian option cheaper than a vanilla call with the same strike and maturity? When would a hedger specifically prefer an Asian option over a vanilla?
<details>
<summary>Answer</summary>
An Asian option is cheaper because it pays on the average of the stock price over multiple dates rather than the terminal price. Averaging reduces variance: the average of a random process is smoother (lower standard deviation) than the process itself at any single point. Lower effective volatility → lower option price via any pricing model. Mathematically, Var(average of correlated paths) < Var(single terminal price) for any positively correlated process.

A hedger specifically prefers an Asian option when their actual economic exposure is to an average price, not a spot price on one day. Examples: a corporate treasurer converting monthly revenues in foreign currency (exposed to the average FX rate over the year, not the rate on December 31); a commodity consumer who buys oil every month at market price (exposed to the average oil price over the period); an airline hedging quarterly jet fuel costs. Buying vanilla options for these exposures creates basis risk (the option pays off based on spot on one day while the exposure is spread over many days). Asian options eliminate this mismatch.
</details>

**Q2.** Explain the knock-in + knock-out = vanilla parity relationship intuitively. Why must this hold?
<details>
<summary>Answer</summary>
For a given set of parameters (same strike K, same barrier H, same maturity T), exactly one of three mutually exclusive things can happen by expiry: (1) the stock never hits the barrier and the knock-out call is alive, or (2) the stock hits the barrier at some point and the knock-out call is dead but the knock-in call activates. There is no scenario where both are alive or both are dead. Therefore, at any expiry, holding both a knock-in and knock-out call is identical to holding a vanilla call: you always have exactly one active call regardless of what the stock does.

Since holding (knock-in + knock-out) always produces exactly the same payoff as holding a vanilla, they must have the same price — or you have an arbitrage. This means you can price one from the other: C_knock-in = C_vanilla − C_knock-out. If you have a Monte Carlo price for the vanilla (BSM) and the knock-out (by checking whether the barrier was hit on each path), you immediately get the knock-in price for free.
</details>

**Q3.** Why do barrier options have violent delta and gamma behavior near the barrier, and why does this create hedging difficulties that vanilla options don't have?
<details>
<summary>Answer</summary>
For a knock-out call approaching expiry, as S → H from above: the option is almost dead (it will cease to exist if the stock touches H), so its value plummets toward zero as S approaches H. But a vanilla call at the same strike still has positive value when S is near H. The option's delta near the barrier captures a sudden transition: delta can change sign from positive (stock above barrier, option alive) to zero (stock at barrier, option dies). Near barrier and expiry, delta can spike dramatically and then flip — a very high gamma that is impossible to hedge continuously. In extreme cases, the gamma of a barrier option near expiry can be orders of magnitude larger than a vanilla's gamma.

For a trader, this means: near the barrier, small stock moves require enormous portfolio adjustments to stay delta-hedged. The transaction costs of rebalancing can exceed the option's P&L. In practice, dealers hedge by keeping a buffer zone around the barrier and accepting residual gamma risk, or by hedging with other barrier options. This is fundamentally different from vanilla options where gamma is well-behaved everywhere.
</details>

---

### Level 2 — Quantitative

**Q4.** A corporate treasurer wants to hedge a 1-year EUR/USD exposure where she will receive euros monthly (12 payments). Her total exposure is €12M (€1M/month). She is comparing two strategies: (A) buy a vanilla put on €12M struck at 1.08 USD/EUR, or (B) buy an Asian put on the same notional, same strike, same maturity. If the current spot is 1.10 and 1-year vol is 8%, calculate qualitatively why strategy B is cheaper and what the treasurer gives up.
<details>
<summary>Answer</summary>
**Why Asian is cheaper:**

The vanilla put (A) protects against the worst case: if EUR/USD is below 1.08 on the single expiry date, she gets the full put payoff. But her actual exposure is to the average of 12 monthly rates, not the rate on one day.

The arithmetic average of 12 monthly EUR/USD observations has a standard deviation of approximately σ/√k, where k ≈ 12 is the number of averaging points (for uniformly sampled averages of a GBM). This gives effective vol ≈ 8%/√3 ≈ 4.6% (the exact formula gives σ/√3 for continuous averaging in GBM). Lower effective vol → significantly cheaper put price.

Using BSM with σ_eff ≈ 4.6% vs 8% for the same strike and maturity:
- Vanilla put (BSM, 8%): approximately \$0.014 per EUR notional
- Asian put (effective vol ~4.6%): approximately \$0.007 per EUR notional
Total saving on €12M: roughly \$84,000 in premium.

**What she gives up:**

If EUR/USD crashes to 1.00 for 10 of the 12 months but spikes to 1.20 in months 11 and 12, the average might be 1.04. The vanilla put (based on last day) would pay nothing if the spot is 1.09 on expiry day, while the Asian put pays based on the 1.04 average. The Asian can protect her when the vanilla doesn't, and vice versa — the trade-off depends on the path. The Asian option perfectly matches her economic exposure (monthly cash flows) while the vanilla leaves basis risk.
</details>

**Q5.** A down-and-out call has parameters: S=100, K=100, H=85, r=5%, σ=20%, T=1 year. Using Monte Carlo, you run 100,000 paths and find that 15,000 paths hit the barrier H=85 during the year. The vanilla call prices at \$10.45. What is the approximate price of the down-and-out call, and what is the price of the corresponding down-and-in call?
<details>
<summary>Answer</summary>
From Monte Carlo: 15,000 of 100,000 paths (15%) hit the barrier. The remaining 85,000 paths survive.

The knock-out call receives its vanilla payoff only on surviving paths. The MC price of the knock-out call is approximately the discounted average payoff on the 85,000 surviving paths. As a rough approximation (assuming surviving paths have similar average payoff to all paths — this is an approximation, since paths that stay above 85 tend to be higher paths):

MC knock-out price ≈ vanilla payoff on surviving fraction × probability of surviving
≈ $10.45 × 0.85 ≈ **$8.88** (rough estimate)

More precisely, you'd compute the actual average of max(S_T − K, 0) on surviving paths and discount it. The barrier kills some in-the-money paths (those that hit 85 then recovered above 100), so the true knock-out price depends on the correlation between survival and payoff.

Using knock-in + knock-out parity:
C_knock-in = C_vanilla − C_knock-out ≈ $10.45 − $8.88 = **\$1.57**

The down-and-in call is cheap (\$1.57 vs \$10.45 vanilla) because it only activates if the stock drops to 85 — a disaster scenario where the stock is likely below the strike at expiry anyway.
</details>

---

### Level 3 — Coding

**Q6.** In the Monte Carlo implementation, `S_paths` simulates all N_paths × N_steps prices upfront using vectorized numpy operations. For the barrier option, `min_prices = np.min(S_paths, axis=1)` finds the minimum over the entire path. What would go wrong with this "full path storage" approach for very large simulations (e.g., 10M paths × 10,000 steps), and what is the standard memory-efficient alternative?
<details>
<summary>Answer</summary>
The full path storage approach creates an array of shape (N_paths, N_steps+1). For 10M paths × 10,000 steps with float64 values: 10M × 10,001 × 8 bytes ≈ 800 GB. This far exceeds available RAM and is completely infeasible in practice.

The standard memory-efficient alternative is to track only the running statistics needed for the payoff, not the full path:

For a knock-out barrier call, you only need: (1) the terminal price S_T and (2) whether the minimum price ever dropped below H. You can compute both in a loop over time steps, keeping only the current price vector (size N_paths) and a boolean "still alive" mask (size N_paths):

```python
S_cur = np.full(N_paths, S0)
alive = np.ones(N_paths, dtype=bool)
for step in range(N_steps):
    Z = rng.standard_normal(N_paths)
    S_cur = S_cur * np.exp((r - 0.5*sigma²)*dt + sigma*√dt*Z)
    alive &= (S_cur > H)  # kill paths that hit barrier
payoffs = np.maximum(S_cur - K, 0) * alive
```

Memory: 2 arrays of N_paths floats ≈ 160 MB for 10M paths. This is the standard approach for path-dependent Monte Carlo: identify the minimal sufficient statistics (terminal price, running max/min, sum for Asian) and track only those, discarding each step's intermediate values.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Exotic options are primarily speculative instruments used by hedge funds | Most exotic options volume comes from corporate hedgers and structured product issuers. Asian options are used for commodity and FX hedging; barriers are embedded in retail structured products and insurance products. They exist to match natural hedging needs, not speculation. |
| You can price any exotic option with BSM by adjusting the vol | Exotic prices depend on the entire dynamics of the vol surface, not just the ATM vol. A barrier option priced with BSM flat vol gives a different answer than one priced with local vol or Heston — sometimes materially different. Model risk for exotics is far larger than for vanilla options. |
| Monte Carlo is always the right tool for exotic options | Monte Carlo is the most flexible tool but is slow for 1D problems and cannot naturally handle American exercise without Longstaff-Schwartz regression. PDE (finite difference) is often faster and more accurate for 1D barrier options and American exotics. Choosing the method depends on dimensionality, path-dependence, and exercise features. |
| Lookback options are worth infinite value since they give the best possible price | Lookback options give the best price over a finite set of observation dates — not continuous monitoring of an infinite-precision price. They are expensive (roughly 2× vanilla) but bounded by the range of possible price movements over the option's life. |

## Related Concepts

- [[Black-Scholes Model]] — the foundation; exotics extend or break BSM assumptions
- [[Monte Carlo Methods]] — primary numerical pricing tool for path-dependent exotics
- [[Numerical Methods PDE]] — alternative for 1D problems; required for American exotics
- [[Delta Hedging]] — dramatically harder for exotics, especially near barriers
- [[American Options]] — the simplest "exotic" (early exercise); template for Bermudan
- [[Local Volatility]] — needed for barrier option pricing consistent with the vol surface
- [[Heston Model]] — stochastic vol pricing of exotics

---

## Sources Used

- Hull, J.C. (2022). *Options, Futures, and Other Derivatives*, 11th ed. Ch. 26. Pearson.
- Shreve, S.E. (2004). *Stochastic Calculus for Finance II*. Ch. 5–7. Springer.
- Haug, E.G. (2007). *The Complete Guide to Option Pricing Formulas*, 2nd ed. McGraw-Hill.
- Glasserman, P. (2003). *Monte Carlo Methods in Financial Engineering*. Springer. (Standard reference for MC pricing of path-dependent options.)

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | initial build |
| 2026-04-18 | Fixed wikilink `[[60-ML-Finance/Deep-Hedging]]` → `[[Deep Hedging]]` (path prefix removed) | review |
