---
type: concept
domain: 40-Strategies
tags: [derivatives, options, strategies]
status: math
stability: empirical
confidence: high
last_reviewed: 2026-04-12
review_interval_days: 90
sources:
  - "Hull ch.19"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Options/Hedging → Hedging Gap 2: How do traders hedge the volatility exposure of options books?
> **This concept:** Gamma scalping is the implementation of dynamic delta hedging — it operationalizes the Black-Scholes hedge by showing how continuous rebalancing converts the option's gamma exposure into a bet on realized vs. implied volatility.
> **Alternative approaches to this gap:** [[Volatility Arbitrage]], variance swaps
> **You need first:** [[Option Greeks]], [[Black-Scholes Model]], [[Delta Hedging]]
> **This unlocks:** [[Volatility Arbitrage]], [[Reinforcement Learning Trading]]

## Why This Exists

**The gap:** Options traders holding long gamma positions needed a systematic protocol for converting the option's curvature into realized cash flows — turning the theoretical Black-Scholes hedge into a practical trading strategy.
**What came before:** Static option positions — buy a call, hold to expiry — which provides directional exposure but doesn't isolate the volatility component; delta hedging existed theoretically but wasn't understood as a strategy for trading volatility itself.
**What this adds:** The insight that a delta-hedged option's P&L depends only on the difference between realized and implied volatility; the gamma-theta tradeoff: each rebalancing captures ½Γ(ΔS)² but loses θ·Δt in time decay; the breakeven daily move formula σ_break = σ_imp × √(Δt) makes the tradeoff explicit; the strategy is the most direct way to trade pure volatility.
**What it still doesn't solve:** Discrete hedging introduces path dependency — the order of moves matters; transaction costs from frequent rebalancing can eliminate the realized vol edge; the strategy has no predictive view on which direction vol will surprise; and large gap moves between rebalances create unhedged directional exposure.

Imagine you own a spring-loaded trap: the more the mouse moves — in either direction — the more forcefully the spring fires. Options work like that trap. When you buy an option and then delta-hedge it (neutralize your exposure to the stock's direction), you end up with a position that profits whenever the stock makes a large move, regardless of which direction. The catch is that holding the option costs you money every day it doesn't move — this is "time decay" or theta. So gamma scalping is essentially a daily race: the stock moves (generating profit from gamma) vs. time passing (generating loss from theta). If the stock moves a lot — more than what the option was priced assuming — you win. If the stock barely moves, theta bleeds you dry. In other words: you are betting that actual (realized) volatility will exceed the implied volatility you paid for when you bought the option. You don't care whether the stock goes up or down. This is the most direct way to trade pure volatility.

## Math Concepts

**Delta:** The sensitivity of the option price $V$ to the underlying price $S$:

$$\Delta = \frac{\partial V}{\partial S}$$

For a call option under BSM: $\Delta_{\text{call}} = N(d_1)$, where $0 < \Delta < 1$.

**Gamma:** The rate of change of delta with respect to $S$ — the curvature of the option's value:

$$\Gamma = \frac{\partial^2 V}{\partial S^2} = \frac{\partial \Delta}{\partial S}$$

Under BSM: $\Gamma = \frac{n(d_1)}{S \sigma \sqrt{T}}$. Gamma is always positive for long options (calls or puts). It is highest for at-the-money options near expiry.

**Theta:** Time decay — how much the option's value falls per unit time:

$$\Theta = \frac{\partial V}{\partial t}$$

For a long option position, $\Theta < 0$ (you lose money each day the stock doesn't move enough).

**The fundamental P&L identity (Taylor expansion):**

Over a small time interval $dt$ with a stock move $dS$:

$$dV \approx \Delta \cdot dS + \frac{1}{2}\Gamma \cdot (dS)^2 + \Theta \cdot dt$$

After delta-hedging (we sell $\Delta$ shares, so the $\Delta \cdot dS$ term is cancelled):

$$\text{P\&L}_{\text{hedged}} = \frac{1}{2}\Gamma \cdot (dS)^2 + \Theta \cdot dt$$

This is the core equation of gamma scalping.

**P&L in terms of realized vs. implied vol:**

Using $dS = S \cdot dW$ with $(dS)^2 \approx S^2 \sigma_{\text{realized}}^2 \, dt$, and substituting the BSM expression for theta:

$$\text{P\&L} = \frac{1}{2}\Gamma S^2 (\sigma_{\text{realized}}^2 - \sigma_{\text{implied}}^2) \, dt$$

This is the key result. Integrated over the life of the option:

$$\text{Total P\&L} = \frac{1}{2} \int_0^T \Gamma_t S_t^2 (\sigma_{\text{realized},t}^2 - \sigma_{\text{implied}}^2) \, dt$$

- If $\sigma_{\text{realized}} > \sigma_{\text{implied}}$: long gamma wins.
- If $\sigma_{\text{realized}} < \sigma_{\text{implied}}$: long gamma loses; short gamma wins.

**Break-even move:** The daily stock move needed to exactly offset one day of theta. For a long ATM straddle:

$$\text{Break-even daily move} \approx \sigma_{\text{implied}} \sqrt{\frac{1}{252}}$$

For $\sigma = 20\%$, this is $20\% / \sqrt{252} \approx 1.26\%$ per day.

## Walkthrough

**Setup:**
- Stock $S = 100$, ATM call with $K = 100$, $T = 30$ days, IV = 20%, $r = 0\%$
- BSM call price $\approx \$2.28$
- $\Delta = 0.5$, $\Gamma = 0.0637$ per dollar, $\Theta = -\$0.038$ per day

**Day 0:** Buy 1 call, sell 0.5 shares to delta-hedge. Net cost = $\$2.28 - 0.5 \times 100 = -\$47.72$ (net cash position).

**Day 1, Scenario A — Stock moves up $+2\%$ to $102$:**

- Gamma P&L: $\frac{1}{2} \times 0.0637 \times (2)^2 = \frac{1}{2} \times 0.0637 \times 4 = \$0.127$
- Theta loss: $-\$0.038$
- Net P&L: $\$0.127 - \$0.038 = +\$0.089$

Re-hedge: new delta at $S=102$ is approximately $0.5 + 0.0637 \times 2 \approx 0.627$. Sell an additional $0.127$ shares at 102 to re-neutralize delta. This "sell high" action locks in profit.

**Day 1, Scenario B — Stock moves only $+0.5\%$ to $100.5$:**

- Gamma P&L: $\frac{1}{2} \times 0.0637 \times (0.5)^2 = \$0.008$
- Theta loss: $-\$0.038$
- Net P&L: $-\$0.030$

The move was too small to cover theta. Long gamma loses on quiet days.

**Break-even check:** $\sqrt{2 \times 0.038 / 0.0637} = \sqrt{1.193} \approx 1.09$. A move of $\$1.09$ (1.09%) is needed to break even — consistent with $20\% / \sqrt{252} \approx 1.26\%$.

## Analysis

**Path dependence:** Total P&L from gamma scalping is path-dependent. Even if the average realized vol over the period equals implied vol, you can still lose money because of when the large moves occur (gamma is smaller far from ATM). Two traders with identical average realized vol but different paths can have very different P&L.

**Re-hedging frequency:** Continuous hedging is the theoretical ideal but is impossible in practice (transaction costs). Practitioners hedge at fixed time intervals (e.g., daily, hourly) or when delta drifts beyond a threshold (band hedging). Less frequent rebalancing increases variance of P&L but reduces costs.

**The gamma-theta tradeoff is strike- and time-dependent:**
- Near-expiry ATM options have maximum gamma (and maximum theta per gamma)
- Deep OTM options have low gamma — not worth scalping
- The ratio $\Theta / \Gamma$ equals $-\frac{1}{2} S^2 \sigma^2$ — directly encoding the BSM break-even

**Short gamma (selling options):** The mirror strategy — sell an option, buy $\Delta$ shares. You collect theta every day but pay when large moves occur. This is profitable when realized vol < IV. Many professional market makers are structurally short gamma and hedge dynamically.

**Volatility convexity:** Because gamma scalping payoff is proportional to $(dS)^2$, it has convex exposure to realized vol. A 10% move earns 4x the P&L of a 5% move, not 2x.

**Failure modes:**
- Jumps: A gap open (e.g., overnight earnings surprise of 15%) is handled poorly if you re-hedge only daily — you miss the local gamma profit within the gap.
- Transaction costs: Frequent rebalancing on a low-gamma position can erode all profits.
- Wrong direction of VRP: If you bought the option when IV was very high, realized vol may not cover the premium — the correct comparison is always realized vol vs. your purchase IV, not the current IV.

## Implementation

```python
import numpy as np
from scipy.stats import norm

# --- BSM Greeks ---
def bsm_greeks(S, K, r, T, sigma):
    """Return call price, delta, gamma, theta."""
    if T <= 0:
        price = max(S - K, 0)
        return price, 1.0 if S > K else 0.0, 0.0, 0.0

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    delta = norm.cdf(d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    # Theta in $ per calendar day (divide by 365)
    theta = (- S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
             - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365

    return price, delta, gamma, theta


def gamma_scalp_simulation(S0=100, K=100, r=0.0, T_days=30,
                           sigma_implied=0.20, sigma_realized=0.25,
                           hedge_freq_days=1, n_sims=1000, seed=42):
    """
    Simulate gamma scalping P&L over the life of an ATM call option.

    Parameters
    ----------
    sigma_implied  : IV at option purchase (sets option premium and BSM greeks)
    sigma_realized : actual daily vol used to generate the stock path
    hedge_freq_days: how often to re-delta-hedge (in trading days)
    """
    np.random.seed(seed)
    T = T_days / 365
    dt = 1 / 365  # one calendar day
    n_steps = T_days

    pnl_list = []

    for sim in range(n_sims):
        S = S0
        t = T
        # Buy call, delta hedge at inception
        price0, delta0, _, _ = bsm_greeks(S, K, r, t, sigma_implied)
        cash = -price0 + delta0 * S   # cash from selling delta shares
        shares = -delta0              # short shares (negative = we sold them)
        option_value = price0

        for step in range(1, n_steps + 1):
            # Generate stock move
            daily_return = np.random.normal(0, sigma_realized / np.sqrt(252))
            dS = S * daily_return
            S_new = S + dS
            t_new = max(T - step * dt, 0)

            # Update option value
            if t_new > 0:
                option_new, delta_new, gamma, theta = bsm_greeks(
                    S_new, K, r, t_new, sigma_implied)
            else:
                option_new = max(S_new - K, 0)
                delta_new = 1.0 if S_new > K else 0.0

            # P&L from stock position
            cash += shares * (S_new - S) * (-1)  # shares is negative
            # Wait — let's track more carefully:
            # We are: long 1 call, short delta shares
            # Stock P&L from short shares: -delta * dS  (but delta is already negative)
            # Re-do cleanly:

            S = S_new
            option_value = option_new

            # Re-hedge at specified frequency
            if step % hedge_freq_days == 0 or t_new == 0:
                delta_old = -shares  # delta we currently have hedged
                delta_new_hedge = delta_new
                # Buy/sell (delta_new - delta_old) shares to re-hedge
                trade = delta_new_hedge - delta_old
                cash -= trade * S   # pay for new shares
                shares = -delta_new_hedge

        # Unwind at expiry
        final_pnl = option_value + cash + shares * S
        pnl_list.append(final_pnl)

    pnl_arr = np.array(pnl_list)
    return pnl_arr


# --- Run simulation ---
import matplotlib.pyplot as plt

# Case 1: realized vol > implied vol (long gamma should profit)
pnl_high_rv = gamma_scalp_simulation(
    sigma_implied=0.20, sigma_realized=0.25, n_sims=2000)

# Case 2: realized vol < implied vol (long gamma loses)
pnl_low_rv = gamma_scalp_simulation(
    sigma_implied=0.20, sigma_realized=0.15, n_sims=2000)

print("=== Realized vol 25% vs IV 20% (long gamma wins) ===")
print(f"  Mean P&L:   ${np.mean(pnl_high_rv):.3f}")
print(f"  Median P&L: ${np.median(pnl_high_rv):.3f}")
print(f"  Std Dev:    ${np.std(pnl_high_rv):.3f}")

print("\n=== Realized vol 15% vs IV 20% (long gamma loses) ===")
print(f"  Mean P&L:   ${np.mean(pnl_low_rv):.3f}")
print(f"  Median P&L: ${np.median(pnl_low_rv):.3f}")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].hist(pnl_high_rv, bins=60, color='steelblue', alpha=0.7, edgecolor='white')
axes[0].axvline(0, color='red', lw=1.5)
axes[0].set_title('P&L: Realized 25% vs IV 20%')
axes[0].set_xlabel('P&L ($)')

axes[1].hist(pnl_low_rv, bins=60, color='coral', alpha=0.7, edgecolor='white')
axes[1].axvline(0, color='red', lw=1.5)
axes[1].set_title('P&L: Realized 15% vs IV 20%')
axes[1].set_xlabel('P&L ($)')

plt.tight_layout()
plt.show()

# --- Daily break-even move ---
sigma_implied = 0.20
S, K, r, T = 100, 100, 0.0, 30/365
_, _, gamma, theta = bsm_greeks(S, K, r, T, sigma_implied)
breakeven_move = np.sqrt(-2 * theta / gamma)   # theta is negative
print(f"\nDaily break-even stock move: ${breakeven_move:.2f} "
      f"({breakeven_move/S*100:.2f}%)")
```

## Bridge to Quant / ML

- **Realized vol forecasting:** The profit of gamma scalping is determined entirely by the spread $\sigma_{\text{realized}} - \sigma_{\text{implied}}$. Any ML model that forecasts realized volatility can be used to decide when to buy vs. sell options. GARCH, HAR-RV, and transformer-based vol models all target this.
- **Variance risk premium:** On average, IV > realized vol for equity indices. Short gamma (selling options and delta-hedging) is a systematic positive-carry strategy, analogous to collecting an insurance premium. ML can improve timing — avoid being short gamma when a VIX spike is imminent.
- **Options market making:** Market makers who quote options are structurally short gamma. Their entire risk management revolves around managing gamma and theta across their book, adjusting hedge ratios continuously.
- **Connection to variance swaps:** A replicating portfolio of continuously delta-hedged options across all strikes produces a payoff equal to a variance swap. Gamma scalping with a single ATM option is a concentrated, path-dependent approximation of this.
- **Reinforcement learning:** RL agents trained on options hedging problems learn policies that approximate gamma scalping — rebalancing to manage delta while trading off transaction costs against P&L variance. This is an active research area.

## Self-Assessment

### Level 1 — Conceptual

**Q1.** Explain the gamma-theta relationship in a delta-hedged long option position.
> **A:** Long gamma means the position profits from large moves in the underlying (rebalancing generates cash flows). Long theta costs money every day as time passes (time decay). They are two sides of the same position: you cannot have the upside of gamma without paying for theta. The question is whether daily moves exceed the breakeven.

**Q2.** What determines the breakeven daily move for a gamma scalping position?
> **A:** The breakeven daily move is approximately σ_imp × √(1/252) × S — the implied daily standard deviation. If realized daily moves exceed this, gamma profits exceed theta losses. If moves are smaller, theta bleeds you dry. The strategy profits only if RV > IV on average over the holding period.

**Q3.** Why does the frequency of delta rebalancing matter, and what is the trade-off?
> **A:** More frequent rebalancing better captures gamma P&L and keeps delta exposure small; but each rebalance incurs transaction costs. The optimal frequency balances the residual delta risk of infrequent hedging against the transaction cost drag of too-frequent hedging. In liquid markets, once-per-day rebalancing is common.

### Level 2 — Quantitative

**Q4.** A delta-hedged ATM call has Γ = 0.05 (per dollar), σ_imp = 20% annually. What is the P&L from gamma if the stock moves +\$2 in one day?
> **A:** Gamma P&L ≈ ½ × Γ × (ΔS)² = ½ × 0.05 × 4 = \$0.10. Compare to theta = −σ²S²Γ/(2) × Δt = −(0.04 × S² × 0.05)/2 × (1/252) — exact numbers depend on S, but the principle is that the move must be large enough to overcome daily theta.

**Q5.** The BSM P&L identity for a discrete-hedged option over interval Δt is: dP&L = ½Γ(ΔS)² − θΔt. Given Γ = 0.02, ΔS = 3, θ = −0.05, Δt = 1 day = 1/252: is the position profitable over this period?
> **A:** Gamma gain = ½ × 0.02 × 9 = \$0.09. Theta loss = 0.05 × (1/252) ≈ \$0.000198. Net = $0.09 − $0.0002 ≈ +\$0.0898. Yes, profitable. The move of \$3 dominated theta for this day. Over many days with smaller moves, theta would dominate.

### Level 3 — Coding

**Q6.** Implement a gamma scalping P&L simulation: simulate N days of stock price paths and compute the cumulative P&L from daily delta rebalancing of a long ATM call.

```python
import numpy as np

def gamma_scalping_pnl(S0: float, sigma_imp: float, sigma_real: float,
                        T: float, dt: float, n_paths: int = 1000) -> np.ndarray:
    """
    Simulate gamma scalping P&L for a long ATM call with daily delta hedging.
    
    Parameters
    ----------
    S0          : initial stock price
    sigma_imp   : implied volatility (used to price option and compute Greeks)
    sigma_real  : realized volatility (used to simulate actual stock moves)
    T           : time to expiry (in years)
    dt          : hedging interval (e.g., 1/252 for daily)
    n_paths     : number of Monte Carlo paths
    
    Returns
    -------
    total_pnl : array of shape (n_paths,) with final cumulative P&L per path
    """
    # TODO: Implement this simulation:
    # 1. For each path, simulate stock price with sigma_real using GBM
    # 2. At each step, compute BSM delta using sigma_imp (the "wrong" vol)
    # 3. Track hedge position: buy/sell delta × shares at each step
    # 4. At expiry, settle the option payoff and close hedge
    # 5. Compute net P&L = option payoff + hedge cash flows - initial option cost
    # Hint: use scipy.stats.norm.cdf for N(d1) to compute BSM delta
    pass
```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Gamma scalping is risk-free if RV > IV | Discrete hedging introduces path dependency; even with RV > IV on average, specific paths can lose money |
| You must rebalance continuously | Practical gamma scalping rebalances at fixed intervals or when delta drifts past a threshold; continuous rebalancing is theoretical |
| Gamma scalping eliminates all directional risk | It eliminates *expected* directional risk; unhedged gap moves between rebalances still create directional P&L |
| The strategy is always profitable if you buy cheap vol | Transaction costs from hedging can consume the entire vol spread; liquidity and bid-ask on the option must be considered |

## Related Concepts

- [[Implied Volatility]]
- [[Variance Swap]]
- [[Volatility Smile]]
- [[VIX]]
- [[Black-Scholes Model]]
- [[Option Greeks]]

## Sources Used

- Hull, *Options, Futures, and Other Derivatives*, Ch. 19 (The Greek Letters) — gamma, theta, delta-hedging mechanics
- Hull, Ch. 17 (Options on Stock Indices and Currencies) for context
- Wilmott, *Paul Wilmott on Quantitative Finance*, Vol. 1, Ch. 7 (Gamma and delta hedging)

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | Hull + initial build |
| 2026-04-12 | Note created | bootstrap |
| 2026-04-11 | QA review: fixed [[Greeks]] → [[Option Greeks]] | quality review |
