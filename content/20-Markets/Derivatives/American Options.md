---
type: concept
domain: 20-Markets
tags: [derivatives, options]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-11
review_interval_days: 365
sources:
  - "Hull ch.12"
  - "Hull ch.13"
created: 2026-04-18
---

> [!info] Problem Chain
> **Chain:** Pricing → Gap 6: Many contracts have no closed-form solution
> **This concept:** Applies the binomial tree numerical method to the specific problem of early exercise, where the option holder must decide at each node whether to exercise or continue holding.
> **Alternative approaches to this gap:** [[Binomial Tree Model]] (Solution C — discrete lattice used here), [[Numerical Methods PDE]] (Solution A — finite difference), [[Monte Carlo Methods]] with Longstaff-Schwartz (Solution B)
> **You need first:** [[Black-Scholes Model]], [[Binomial Tree Model]], [[Put-Call Parity]]
> **This unlocks:** [[Exotic Options]], [[Binomial Tree Model]] (deeper usage), Longstaff-Schwartz Monte Carlo

## Why This Exists

**The gap:** The overwhelming majority of listed equity options in the real world are American-style — they can be exercised on any day before expiry. But the Black-Scholes formula only prices European options. Practitioners needed a way to price the contracts they were actually trading.

**What came before:** BSM gave the European option price with a closed-form formula. For American options, practitioners knew the price must be at least as high as the European price (you have at least as much flexibility), but there was no formula to say by how much. Early exercise adds an infinite-dimensional decision problem — at every moment in time, the holder can exercise or hold — which cannot be collapsed into a single formula.

**What this adds:** By breaking time into discrete steps, the binomial tree converts the continuous-time "exercise or hold" decision into a finite backward-induction problem. At each node, you compare the immediate exercise value (intrinsic value) to the continuation value (discounted expected future value). Take the maximum. Working backward from expiry gives the price today. This is simple, exact within the lattice, and directly identifies the early exercise boundary — the stock price below which you should exercise immediately.

**What it still doesn't solve:** The binomial tree becomes impractical for options on multiple assets or options whose payoff depends on the path (not just the current stock price). Longstaff-Schwartz Monte Carlo solves these cases by using regression to estimate continuation values, but at the cost of higher computational complexity.

## Math Concepts

### Value Inequality

American options are always worth at least as much as their European counterparts:

$$C_{\text{Am}} \geq C_{\text{Eu}}, \qquad P_{\text{Am}} \geq P_{\text{Eu}}$$

The difference $C_{\text{Am}} - C_{\text{Eu}}$ (or $P_{\text{Am}} - P_{\text{Eu}}$) is the **early exercise premium**.

### Early Exercise of Calls (Non-Dividend Stock)

It is **never optimal** to early-exercise an American call on a non-dividend paying stock.

**Intuitive argument:** suppose you hold an ITM call ($S > K$) and think about exercising early to capture $S - K$. What do you give up?

1. **Time value of the strike:** you pay $K$ today, but if you wait, you only need $K$ at expiry — meaning you hold onto $K \cdot e^{r \cdot \text{remaining}}$ in cash interest.
2. **Downside protection:** the call protects you if the stock falls below $K$. If you exercise now and the stock crashes, you've lost that protection.
3. **Upside:** you still get all the upside by waiting (the call participates fully above $K$).

Formally: $C_{\text{Am}} = C_{\text{Eu}}$ for non-dividend stocks. The American call is worth the same as the European call — the early exercise feature has zero value.

**Exception — dividends:** if the stock pays a dividend, the stock price drops on the ex-dividend date. Exercising just *before* the ex-dividend date lets you capture the dividend. This can make early exercise optimal for American calls on dividend-paying stocks.

### Early Exercise of Puts

Early exercise of an American put **can be optimal** when the put is sufficiently deep in-the-money.

**Why:** suppose $S = 1$ (stock nearly worthless) and $K = 100$. The put is worth $99$ intrinsic value. If you exercise now, you get $99$ in cash, which starts earning interest immediately. The maximum you can ever collect is $100$ (if the stock goes to zero). The interest on $99$ over the remaining time may exceed the additional $1$ you could gain — so exercise now.

The **critical stock price** $S^*(t)$ is the stock price below which early exercise is optimal. It is a function of time: as expiry approaches, $S^*(t)$ rises toward $K$.

### The Free Boundary Problem

Mathematically, pricing an American put is a **free boundary problem**: we simultaneously solve for the option price $V(S, t)$ and the unknown exercise boundary $S^*(t)$.

In the continuation region ($S > S^*(t)$): the option satisfies the BSM PDE:

$$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS \frac{\partial V}{\partial S} - rV = 0$$

In the exercise region ($S \leq S^*(t)$): $V = K - S$ (hold the intrinsic value).

Boundary conditions at $S^*(t)$:

$$V(S^*, t) = K - S^* \quad \text{(value matching)}$$
$$\frac{\partial V}{\partial S}\bigg|_{S^*} = -1 \quad \text{(smooth pasting)}$$

There is no closed-form solution for the American put. Numerical methods are required.

### Put-Call Parity (American)

Unlike European options, put-call parity becomes an **inequality**:

$$S_0 - K \leq C_{\text{Am}} - P_{\text{Am}} \leq S_0 - K e^{-rT}$$

### Pricing Methods

| Method | Notes |
|--------|-------|
| Binomial tree | Standard; exact within the lattice; $O(N^2)$ nodes |
| Finite difference (PDE) | Crank-Nicolson; more accurate per step; requires PDE discretization |
| Longstaff-Schwartz (LSM) | Monte Carlo; regress continuation values on basis functions; scales to high dimensions |
| Barone-Adesi-Whaley | Analytical approximation for American puts; fast but approximate |

### Bermudan Options

A **Bermudan option** is exercisable only on a discrete set of dates (e.g., monthly). It is intermediate between European (one exercise date) and American (continuous). Priced by the same backward-induction logic on a tree, but early exercise is only checked at specified nodes.

## Walkthrough

**Setup:** American put, $S_0 = 100$, $K = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 1$ year, $N = 4$ steps ($\Delta t = 0.25$).

Using CRR: $u = e^{0.20\sqrt{0.25}} = 1.1052$, $d = 1/u = 0.9048$, $p = \frac{e^{0.05 \times 0.25} - 0.9048}{1.1052 - 0.9048} = \frac{1.0126 - 0.9048}{0.2004} = 0.5379$.

**At each node the American put checks:**

$$V_{i,j} = \max\!\left(\underbrace{e^{-r\Delta t}[p \cdot V_{i+1,j+1} + (1-p) \cdot V_{i+1,j}]}_{\text{continuation}},\; \underbrace{K - S_{i,j}}_{\text{exercise}}\right)$$

**Where early exercise triggers:** for nodes where $S$ is very low (deep ITM), the intrinsic value $K - S$ exceeds the continuation value. At those nodes, the option is exercised early — this is where $S < S^*(t)$.

**American vs European put:**

| | European Put | American Put |
|--|-------------|-------------|
| Price (ATM) | $\approx 5.57$ | $\approx 6.09$ |
| Deep ITM ($S=70$) | $\approx 28.0$ | $\approx 30.0$ |
| Very deep ITM ($S=50$) | $\approx 47.1$ | $\approx 50.0$ (exercise immediately) |

The early exercise premium grows as the put goes deeper in-the-money. For very deep ITM puts, the American put approaches its intrinsic value $K - S$ because you should exercise immediately.

**The early exercise boundary:** there exists a time-varying critical price $S^*(t)$ — below it, exercise immediately; above it, hold. For this parameter set, $S^*(0) \approx 76$ (exercise if stock drops to 76 or below today). As time passes and expiry approaches, $S^*$ rises toward $K$.

## Analysis

**American calls on dividend stocks:** early exercise just before the ex-dividend date can be optimal. The rationale: exercising gives you the stock, which is about to pay a dividend. If that dividend exceeds the time value you sacrifice, exercise is optimal. This is why many listed equity options are American — the dividend optionality has real value.

**Put-call parity violation:** the American inequality $S_0 - K \leq C_{\text{Am}} - P_{\text{Am}} \leq S_0 - K e^{-rT}$ means you cannot infer one price from the other (as you can for European options via [[Put-Call Parity]]). Each must be priced independently.

**Early exercise boundary properties:**
- $S^*(T) = K \cdot \min(1, r/q)$ at expiry (where $q$ is dividend yield; for no dividends, $S^*(T) = K$ for puts)
- $S^*(t)$ is monotonically non-decreasing as $t \to T$ (the boundary moves up as expiry approaches)
- The boundary depends on $r$, $\sigma$, and $T$: higher $r$ encourages earlier exercise of puts (cash received sooner is more valuable), higher $\sigma$ discourages early exercise (more remaining optionality)

**Longstaff-Schwartz (LSM):** for multi-factor or path-dependent American options, binomial trees become impractical. LSM uses Monte Carlo: simulate many stock paths, then at each exercise date regress continuation values against option state, and use the regression to decide whether to exercise. The idea: $\mathbb{E}[\text{future payoff} \mid S_t]$ is approximated by a polynomial regression on $S_t$.

## Implementation

```python
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt


def bsm_price(S, K, r, sigma, T, option_type="put"):
    """BSM European option price."""
    if T <= 0:
        return max(K - S, 0) if option_type == "put" else max(S - K, 0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def binomial_american_put(S, K, r, sigma, T, N):
    """
    American put price via CRR binomial tree.
    Returns (price, early_exercise_nodes_count).
    """
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u
    p = (np.exp(r * dt) - d) / (u - d)
    discount = np.exp(-r * dt)

    # Terminal payoffs
    j = np.arange(N + 1)
    S_T = S * (u ** j) * (d ** (N - j))
    V = np.maximum(K - S_T, 0.0)

    early_exercise_count = 0

    for i in range(N - 1, -1, -1):
        S_now = S * (u ** np.arange(i + 1)) * (d ** (i - np.arange(i + 1)))
        continuation = discount * (p * V[1:i+2] + (1 - p) * V[0:i+1])
        intrinsic = np.maximum(K - S_now, 0.0)
        early_ex = intrinsic > continuation
        early_exercise_count += np.sum(early_ex)
        V = np.where(early_ex, intrinsic, continuation)

    return V[0], early_exercise_count


def early_exercise_boundary(K, r, sigma, T, N):
    """
    Find the early exercise boundary S*(t) at each time step.
    Returns array of (time, critical_price) pairs.
    """
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u
    p = (np.exp(r * dt) - d) / (u - d)
    discount = np.exp(-r * dt)

    # Build full price tree and value tree
    # S_tree[i][j] = S at step i, j up-moves
    j_max = N + 1
    S_tree = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        for j in range(i + 1):
            S_tree[i, j] = K * (u ** j) * (d ** (i - j))  # normalised to K

    # Actually build relative to S=100
    S0 = 100.0
    for i in range(N + 1):
        for j in range(i + 1):
            S_tree[i, j] = S0 * (u ** j) * (d ** (i - j))

    V = np.maximum(K - S_tree[N, :N+1], 0.0)
    boundary = []

    for i in range(N - 1, -1, -1):
        continuation = discount * (p * V[1:i+2] + (1 - p) * V[0:i+1])
        intrinsic = np.maximum(K - S_tree[i, :i+1], 0.0)
        V_new = np.where(intrinsic > continuation, intrinsic, continuation)

        # Find boundary: highest S where intrinsic > continuation
        exercise_mask = intrinsic > continuation
        if np.any(exercise_mask):
            critical_S = np.max(S_tree[i, :i+1][exercise_mask])
        else:
            critical_S = 0.0
        boundary.append((i * dt, critical_S))

        V = V_new

    boundary.reverse()
    return boundary


# ── 1. Compare European vs American put prices ───────────────────────────────
print("European vs American Put Prices (K=100, r=5%, sigma=20%, T=1yr)")
print(f"{'S':>6} {'EU Put':>10} {'AM Put':>10} {'Premium':>10}")
S_vals = [50, 60, 70, 80, 90, 100, 110, 120]
N = 200
for S_val in S_vals:
    eu = bsm_price(S_val, 100, 0.05, 0.20, 1.0, "put")
    am, _ = binomial_american_put(S_val, 100, 0.05, 0.20, 1.0, N)
    print(f"{S_val:>6} {eu:>10.4f} {am:>10.4f} {am-eu:>10.4f}")

print()

# ── 2. ATM: compare with different time horizons ──────────────────────────────
print("ATM American vs European put (S=K=100) across maturities:")
print(f"{'T':>8} {'EU Put':>10} {'AM Put':>10} {'Premium':>10}")
for T_val in [0.25, 0.5, 1.0, 2.0]:
    eu = bsm_price(100, 100, 0.05, 0.20, T_val, "put")
    am, _ = binomial_american_put(100, 100, 0.05, 0.20, T_val, N)
    print(f"{T_val:>8.2f} {eu:>10.4f} {am:>10.4f} {am-eu:>10.4f}")

print()

# ── 3. Early exercise boundary ────────────────────────────────────────────────
boundary = early_exercise_boundary(100, 0.05, 0.20, 1.0, N=50)
times = [b[0] for b in boundary]
crits = [b[1] for b in boundary]

print("Early exercise boundary S*(t) — exercise put if S < S*(t):")
print(f"{'Time':>8} {'S*(t)':>10}")
for t, c in boundary[::10]:
    print(f"{t:>8.3f} {c:>10.4f}")

# Uncomment to plot:
# plt.figure(figsize=(8, 4))
# plt.plot(times, crits, "b-", lw=2)
# plt.axhline(100, color="gray", linestyle="--", label="Strike K=100")
# plt.xlabel("Time (years)")
# plt.ylabel("Critical Stock Price S*(t)")
# plt.title("American Put Early Exercise Boundary")
# plt.legend()
# plt.tight_layout()
# plt.savefig("american_put_boundary.png", dpi=150)
```

## Bridge to Quant / ML

- **Reinforcement learning for exercise:** deciding when to exercise an American option is a sequential decision problem — state = $(S_t, t, \text{Greeks})$, action = exercise or hold, reward = option payoff. This maps directly to the RL framework. Neural-network approaches (like deep BSDE and deep LSM) replace polynomial regression with neural net regression for the continuation value.
- **Longstaff-Schwartz in practice:** LSM is the industry standard for pricing Bermudan and American options in complex models (stochastic vol, multi-asset). The regression step — estimating $\mathbb{E}[\text{payoff} \mid \text{state}]$ — is a standard supervised learning problem, making it a natural point of contact between quant finance and ML.
- **Calibration with American options:** when fitting stochastic vol models (Heston, SABR) to listed equity options, the observed options are mostly American. Calibration routines must price American options in the inner loop, making it computationally intensive — a key motivation for ML-accelerated pricing (surrogate models).

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** It is never optimal to early-exercise an American call on a non-dividend-paying stock. Explain the three things you give up by exercising early.
<details>
<summary>Answer</summary>
(1) Time value of the strike: if you exercise now and pay K today, you forgo the interest you could have earned on K until expiry. If you wait, you only need to have K at expiry — meaning you keep that cash invested until then. The present value of K is less than K, so waiting is always cheaper. (2) Downside protection: by exercising, you convert from owning a call to owning the stock. If the stock subsequently crashes below K, you absorb the full loss. The unexercised call is protected — it simply expires worthless, capping your downside. (3) Upside is unchanged: exercising gives you the stock, which still participates fully in any rally above K. But you could achieve the same exposure by waiting. Since you give up (1) and (2) while gaining nothing extra, early exercise is never rational without dividends.
</details>

**Q2.** Under what conditions does early exercise of an American put become optimal? Give an economic intuition.
<details>
<summary>Answer</summary>
Early exercise of an American put becomes optimal when the put is sufficiently deep in-the-money and the interest rate is high. The intuition: a deep ITM put is worth approximately K − S. By exercising today, you receive K − S in cash, which immediately starts earning interest at rate r. The maximum additional value you can gain by waiting is only S more (if the stock goes to zero), but you already have nearly that. Formally, if S is very small (stock nearly worthless), the interest earned on the exercise proceeds over the remaining life of the option exceeds the remaining optionality. Higher interest rates accelerate this: the sooner you can put cash to work, the more valuable early exercise becomes. Mathematically, the early exercise boundary S*(t) is the stock price below which this trade-off tips in favor of exercise.
</details>

**Q3.** The Longstaff-Schwartz method uses regression to estimate continuation values. Why does this work, and why is it needed for high-dimensional problems where the binomial tree fails?
<details>
<summary>Answer</summary>
Longstaff-Schwartz (LSM) simulates many stock price paths and at each exercise date works backward: for each in-the-money path, it asks "what is the expected future payoff if I continue holding?" — the continuation value. Since this expectation is unknown, it approximates it by regressing the future realized payoffs on the current state variables (e.g., polynomial functions of the stock price). The regression gives a function that estimates E[future payoff | current state] from the simulated data. Then at each node, if the intrinsic value exceeds the estimated continuation value, exercise.

This works for high-dimensional problems (many underlyings) because simulation scales linearly with the number of dimensions — you simulate each underlying independently. A binomial tree would require a full lattice over all underlyings: a 2-asset problem needs a 2D tree (N² nodes), a 3-asset problem needs N³ nodes. LSM keeps the grid dimension fixed (you always simulate forward paths) regardless of how many state variables there are.
</details>

---

### Level 2 — Quantitative

**Q4.** American put: S = 90, K = 100, r = 5%, σ = 20%, T = 1 year. Use the result from the note that the early exercise boundary at t=0 is approximately S* ≈ 76 for similar parameters. Since S = 90 > S* = 76, should you exercise immediately? If not, how much is the early exercise premium worth?
<details>
<summary>Answer</summary>
Since S = 90 > S* ≈ 76, you should NOT exercise immediately — the stock is above the early exercise boundary, so the continuation value exceeds the intrinsic value.

From the walkthrough table, the American put at S = 90 (which is close to the "ATM" case): the early exercise premium is approximately AM_put − EU_put. Using the results in the note for S close to 100 (ATM), the premium is about $0.52 (≈ $6.09 − \$5.57). For S = 90, the premium would be somewhat larger as the put is more in-the-money and early exercise becomes more tempting. The put is deep enough to have meaningful early exercise premium but not so deep that you should act immediately. As S falls toward 76, the premium shrinks (because you're approaching the point where exercising makes sense) and eventually the American put approaches its intrinsic value of K − S = \$24.
</details>

**Q5.** In the CRR binomial tree with S = 100, K = 100, r = 5%, σ = 20%, Δt = 0.25 years: compute u, d, and the risk-neutral probability p. If after one down-move S = 90.48, compute the intrinsic value of the put and explain why checking intrinsic vs. continuation matters at this node.
<details>
<summary>Answer</summary>
u = e^{σ√Δt} = e^{0.20 × 0.5} = e^{0.10} = 1.1052.
d = 1/u = 0.9048.
p = (e^{rΔt} − d) / (u − d) = (e^{0.0125} − 0.9048) / (1.1052 − 0.9048) = (1.0126 − 0.9048) / 0.2004 = 0.1078 / 0.2004 = 0.5379.

After one down-move: S = 100 × 0.9048 = 90.48.
Intrinsic value of the put = max(100 − 90.48, 0) = \$9.52.

At this node, we compare $9.52 (exercise now) to the continuation value: discount × [p × V_uu + (1−p) × V_ud]. If the stock is on a path toward deep ITM territory, the continuation value could be less than $9.52 — meaning the holder should exercise now and take the \$9.52 cash rather than waiting. The early exercise check is mandatory at every node; skipping it would undervalue the American option.
</details>

---

### Level 3 — Coding

**Q6.** In `binomial_american_put`, the terminal payoffs are computed as `V = np.maximum(K - S_T, 0.0)` where `S_T = S * (u**j) * (d**(N-j))`. The backward induction then uses vectorized operations. Why does the inner loop run backward (from `N-1` to `0`) rather than forward, and what would happen to the early exercise logic if it ran forward instead?
<details>
<summary>Answer</summary>
The backward direction is required because the early exercise decision at any node depends on the continuation value — the expected future payoff from that node onward. Continuation value can only be computed once you already know the option values at all future nodes. The algorithm must start at the terminal nodes (where values are known: the option payoff at expiry), then work backward in time, at each step using already-computed future values to calculate the present continuation value.

If the loop ran forward, you would encounter nodes whose continuation values are not yet computed — you'd have to reference "future" array entries that still contain the initial terminal payoffs, producing nonsense values. The early exercise check `intrinsic > continuation` would compare the intrinsic value against incorrect (terminal) continuation estimates rather than the actual discounted future values, causing systematic errors in the exercise boundary and the option price. Forward induction works for computing stock prices on the tree (those only depend on past moves) but not for option values (which depend on future payoffs).
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| American options are always worth more than European options | American ≥ European always holds, but for calls on non-dividend stocks the two are equal — the early exercise feature has zero value. The premium exists only for puts and for calls on dividend-paying stocks |
| You should exercise a deep ITM American option immediately | Even deep ITM options have remaining time value. The correct decision depends on the early exercise boundary S*(t) — exercise only if S < S*(t), which varies with time and parameters |
| Put-call parity holds for American options | It holds only as an inequality: S − K ≤ C_Am − P_Am ≤ S − Ke^{-rT}. The equality breaks because the put and call may have different optimal exercise strategies |
| More tree steps always improve accuracy proportionally | Binomial tree accuracy improves as O(1/N) — you need 4× more steps for 2× better accuracy. Beyond N ≈ 1000, the improvement is marginal and finite difference methods are more efficient |

## Related Concepts
- [[Binomial Tree Model]] — the primary numerical pricing method for American options; backward induction implements the exercise decision
- [[Black-Scholes Model]] — gives the European option price; American call on non-dividend stock equals BSM call; no closed form for American put
- [[Put-Call Parity]] — holds exactly for European options but only as an inequality for American options
- [[Option Greeks]] — Delta of an American put is larger (in magnitude) than the European put in the early-exercise region
- [[Delta Hedging]] — American options require the same delta-hedging framework, but the delta changes at the exercise boundary

## Sources Used
- Hull — *Options, Futures & Other Derivatives*, ch.12, ch.13

---

## Revision Log
| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | Hull ch.12, ch.13 |
| 2026-04-11 | Fixed risk-neutral probability $p$ in 4-step walkthrough (was 0.5636, corrected to 0.5379); removed unused `S_range` parameter from `early_exercise_boundary` function signature and call site | QA review |
| 2026-04-18 | Renamed "Implementation (Python)" → "Implementation" for section consistency | review |
