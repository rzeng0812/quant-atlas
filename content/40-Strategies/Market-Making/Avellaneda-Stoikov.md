---
type: concept
domain: 40-Strategies
tags: [strategy, market-making, HFT, inventory-risk, stochastic-control]
status: math
stability: evolving
confidence: high
last_reviewed: 2026-04-12
review_interval_days: 90
sources:
  - "Avellaneda & Stoikov - High-Frequency Trading in a Limit Order Book (2008)"
  - "Cartea et al - Algorithmic and High-Frequency Trading (2015)"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Execution → Gap 3: How do liquidity providers optimally quote in a limit order book?
> **This concept:** Avellaneda-Stoikov derives the market maker's optimal bid/ask quotes as closed-form functions of inventory, time, and risk aversion — the first rigorous stochastic control solution to the optimal quoting problem.
> **Alternative approaches to this gap:** [[Market Making]] (heuristic spread rules), reinforcement learning policies
> **You need first:** [[Market Making]], [[Stochastic Differential Equations]], [[Ornstein-Uhlenbeck Process]]
> **This unlocks:** [[Reinforcement Learning Trading]], [[Transaction Cost Analysis]]

## Why This Exists

**The gap:** Practitioners quoting in electronic markets had heuristic rules for adjusting spreads with inventory and time but no principled framework — they couldn't systematically optimize the trade-off between spread revenue, adverse selection, and inventory risk.
**What came before:** Ad hoc market making — quote fixed spreads, manually adjust when inventory gets large, no formal treatment of the time dimension or risk aversion; the Ho-Stoll model (1981) provided a static precursor but no dynamic solution.
**What this adds:** A stochastic control formulation where the market maker maximizes expected terminal utility; derives the reservation price r(s,q,t) = s − qγσ²(T−t) (mid tilted by inventory); and the optimal spread δ = γσ²(T−t) + (2/γ)ln(1 + γ/k) (independent of inventory); provides closed-form solutions implementable in production.
**What it still doesn't solve:** The model assumes Poisson order arrival with intensity that decays exponentially in spread distance — a strong assumption; it doesn't model adverse selection explicitly; the model is static in parameters and doesn't adapt to regime changes or flow toxicity shifts.

Imagine you run a currency exchange booth at an airport. You buy euros from travelers at \$1.05 and sell euros at \$1.07. The \$0.02 spread is your profit. You don't care which direction the euro moves — you just want to see lots of transactions. Every trade earns you the spread.

That's the ideal version of market making. The real version has a problem: **inventory risk**.

Suppose 20 travelers in a row want to sell you euros. Now you're sitting on a mountain of euros. If the euro suddenly depreciates, all that inventory is worth less. You're not a market maker anymore — you're an involuntary speculator. To avoid this, you need to **adjust your quotes** to discourage more buying from you and encourage selling to you. You make your sell price (ask) cheaper and your buy price (bid) more expensive — you lean against your inventory.

Now add a second problem: **adverse selection**. Some travelers know something you don't — maybe a news event is about to crater the euro. They want to sell to you *before* the price moves. You'll fill all their orders happily, accumulate inventory, and then watch the price gap down against you. This is the market maker's nightmare: you earn the spread on uninformed flow but get picked off by informed flow.

The **Avellaneda-Stoikov model** (2008) is the canonical mathematical treatment of this problem. It derives the market maker's optimal bid and ask prices as explicit functions of:
1. Current mid-price
2. Current inventory position
3. Risk aversion
4. Time remaining in the trading session
5. Volatility (which determines both adverse selection risk and inventory risk)

The key result is remarkably clean: the optimal quotes are symmetric around a **reservation price** that tilts away from mid depending on inventory. If you're long, you shade your quotes down (to attract sellers); if short, you shade up. The spread around the reservation price depends on risk aversion and volatility.

---

## Math Concepts

### Setup

- Mid-price process: $dS_t = \sigma\, dW_t$ (arithmetic Brownian motion, no drift for simplicity)
- Inventory at time $t$: $q_t$ (positive = long, negative = short), in shares
- Cash at time $t$: $X_t$
- Time horizon: $[0, T]$ (end-of-day, when inventory must be unwound)
- Market maker posts bid $S^b$ and ask $S^a$; spread is $\delta = S^a - S^b$
- Orders arrive as Poisson processes with intensity depending on distance from mid:
  - Ask filled at rate $\lambda^a(\delta^a) = A e^{-\kappa \delta^a}$
  - Bid filled at rate $\lambda^b(\delta^b) = A e^{-\kappa \delta^b}$
  - where $\delta^a = S^a - S$ and $\delta^b = S - S^b$ are the half-spreads

### Objective

Maximize expected exponential utility of terminal wealth:
$$
\max_{\delta^a, \delta^b} \mathbb{E}\left[-e^{-\gamma(X_T + q_T S_T)}\right]
$$

where $\gamma$ is the absolute risk-aversion coefficient. The terminal wealth includes: accumulated cash from fills ($X_T$) plus the mark-to-market value of remaining inventory ($q_T S_T$).

### Value Function and HJB Equation

Using the ansatz $u(x, q, s, t) = -\exp(-\gamma(x + \theta(q, s, t)))$, the problem reduces to solving a Hamilton-Jacobi-Bellman (HJB) equation. The key function $\theta$ satisfies:

$$
\frac{\partial\theta}{\partial t} + \frac{\sigma^2}{2}\frac{\partial^2\theta}{\partial s^2} - \frac{\gamma \sigma^2}{2}\left(\frac{\partial\theta}{\partial s}\right)^2 + H(q, \partial_s\theta) = 0
$$

where $H$ captures the optimal spread choice via the Poisson arrival terms.

### Reservation Price

The key result: the market maker's **indifference price** (the mid-price they would accept zero spread to trade at) is:

$$
\boxed{r(q, t) = S - q \cdot \gamma \cdot \sigma^2 \cdot (T - t)}
$$

**Intuition:** The reservation price tilts away from mid proportional to:
- $q$ — inventory position (more long → tilt down, attract sellers)
- $\gamma$ — risk aversion (more risk-averse → stronger tilt)
- $\sigma^2$ — volatility (riskier stock → stronger tilt)
- $(T-t)$ — time remaining (more time left → larger tilt, because risk accumulates)

At $t = T$ (end of day), $r = S$ regardless of inventory: you must accept the market price.

### Optimal Spread

The optimal total bid-ask spread (full spread = ask minus bid):

$$
\boxed{\delta^* = \gamma \sigma^2 (T - t) + \frac{2}{\gamma} \ln\!\left(1 + \frac{\gamma}{\kappa}\right)}
$$

**Breaking this down:**
- First term $\gamma \sigma^2 (T-t)$: **inventory risk premium** — wider spread needed to compensate for the risk of holding inventory longer. Shrinks to zero at end of day.
- Second term $\frac{2}{\gamma}\ln(1 + \gamma/\kappa)$: **adverse selection spread** — compensation for the risk of trading with an informed counterparty. Does not depend on time; it is the structural cost of market making.

### Optimal Bid and Ask

The quotes are placed symmetrically around the *reservation price* (not the mid-price!):

$$
S^a = r + \frac{\delta^*}{2} = S - q\gamma\sigma^2(T-t) + \frac{\delta^*}{2}
$$

$$
S^b = r - \frac{\delta^*}{2} = S - q\gamma\sigma^2(T-t) - \frac{\delta^*}{2}
$$

When $q = 0$ (flat inventory), both quotes are centered on the true mid. When $q > 0$ (long), both quotes shift down — you quote a lower ask to sell faster and a lower bid to discourage more buying.

---

## Walkthrough

**Setup:** Market making on a stock with $S = \$100$, $\sigma = 0.02$ (2% daily vol), $\gamma = 0.1$, $\kappa = 1.5$, $T = 1$ day, current time $t = 0$ (start of day).

**Step 1: Compute optimal total spread at $t = 0, q = 0$.**

$$
\delta^* = 0.1 \times (0.02)^2 \times 1.0 + \frac{2}{0.1}\ln\!\left(1 + \frac{0.1}{1.5}\right)
$$

$$
= 0.1 \times 0.0004 + 20 \times \ln(1.0667)
$$

$$
= 0.00004 + 20 \times 0.0645 \approx 0.00004 + 1.29 \approx 1.29 \text{ cents}
$$

With zero inventory and starting at mid: $S^b = \$99.994$, $S^a = \$100.006$.

**Step 2: After accumulating $q = +500$ shares of inventory (long).**

Reservation price shift:
$$
r = 100 - 500 \times 0.1 \times 0.0004 \times 1.0 = 100 - 0.02 = \$99.98
$$

With the same spread $\delta^* \approx 1.29$ cents:
$$
S^b = 99.98 - 0.00645 = \$99.974 \quad S^a = 99.98 + 0.00645 = \$99.986
$$

Both quotes shifted down by 2 cents. The ask is now \$99.986 instead of \$100.006 — the market maker is offering a cheaper sell price to attract buyers and reduce the long inventory.

**Step 3: Repeat at $t = 0.75$ (75% through the day), still $q = +500$.**

$$
r = 100 - 500 \times 0.1 \times 0.0004 \times 0.25 = 100 - 0.005 = \$99.995
$$

Inventory spread term: $0.1 \times 0.0004 \times 0.25 = 0.00001$ — tiny.

As the day winds down, the inventory adjustment vanishes because there is less time for the position to hurt you. The quotes converge back toward mid.

**Spread dynamics summary:**

| Time | Inventory | Reservation Price | Bid | Ask |
|---|---|---|---|---|
| $t=0$ | $q=0$ | $100.00 | $99.994$ | $100.006$ |
| $t=0$ | $q=+500$ | $99.98$ | $99.974$ | $99.986$ |
| $t=0.75$ | $q=+500$ | $99.995$ | $99.989$ | $100.001$ |
| $t=1.0$ | any | $S$ | $S - \delta^*/2$ | $S + \delta^*/2$ |

---

## Analysis

**Key Assumptions and Their Violations:**

| Assumption | Reality |
|---|---|
| Poisson arrivals with exponential intensity | Order arrival clustering; heavy tails; regime shifts |
| Arithmetic Brownian motion for price | Log-normal is standard; microstructure noise is not BM |
| Single market maker | Competition from other MMs compresses spreads |
| No queue position | Priority in the order book is crucial in practice |
| Homogeneous order size | Large orders and small orders have very different adverse selection |

**Model Extensions:**

1. **Cartea & Jaimungal (2013) — Running inventory penalty:** Add a term $\phi q^2 dt$ to the cost function to penalize large inventory continuously (not just at terminal time). Results in more aggressive rebalancing throughout the day.

2. **Stoikov (2009) — Market depth:** Generalize to posting limit orders at multiple price levels simultaneously; optimal depth distribution across the book.

3. **Guilbaud & Pham (2013) — Discrete price grid:** Model the tick structure explicitly; can't post at arbitrary prices. Solutions are jump processes.

4. **Adverse selection modeling (Glosten-Milgrom):** Replace the reduced-form Poisson intensity with a structural model that distinguishes informed and uninformed order flow. $\kappa$ becomes a function of the information environment.

**Failure Modes:**
- **Inventory explosion during momentum:** A fast-trending market means one side of quotes keeps filling while the other doesn't. AC model mitigates but does not eliminate this.
- **Parameter misestimation:** $\kappa$ is notoriously hard to calibrate; small errors cause either too-tight spreads (gets picked off) or too-wide spreads (no fills).
- **Cross-asset hedging:** Real market makers hedge correlated assets simultaneously; single-asset AS model misses cross-gamma effects.

---

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field


@dataclass
class ASParams:
    """Avellaneda-Stoikov model parameters."""
    S0: float = 100.0        # Initial mid-price
    sigma: float = 0.02      # Daily price volatility
    gamma: float = 0.1       # Absolute risk aversion
    kappa: float = 1.5       # Order arrival sensitivity to spread
    A: float = 1.0           # Baseline arrival intensity
    T: float = 1.0           # Session length (days)
    dt: float = 1.0 / 252 / 6.5 / 60  # 1-minute steps in a trading day


def reservation_price(S: float, q: float, t: float, p: ASParams) -> float:
    """
    Market maker's indifference price given inventory q and time t.

    Parameters
    ----------
    S : float  Current mid-price
    q : float  Current inventory (positive = long)
    t : float  Current time (0 to T)
    p : ASParams

    Returns
    -------
    float  Reservation price in dollars
    """
    return S - q * p.gamma * p.sigma**2 * (p.T - t)


def optimal_spread(t: float, p: ASParams) -> float:
    """
    Full bid-ask spread (ask - bid) under the optimal policy.
    Note: does not depend on inventory q.
    """
    inventory_term = p.gamma * p.sigma**2 * (p.T - t)
    adverse_selection_term = (2 / p.gamma) * np.log1p(p.gamma / p.kappa)
    return inventory_term + adverse_selection_term


def optimal_quotes(
    S: float, q: float, t: float, p: ASParams
) -> tuple[float, float]:
    """
    Compute optimal bid and ask prices.

    Returns (bid, ask).
    """
    r = reservation_price(S, q, t, p)
    half_spread = optimal_spread(t, p) / 2
    return r - half_spread, r + half_spread


def simulate_market_making(p: ASParams, seed: int = 42) -> dict:
    """
    Simulate one trading session with the AS strategy.

    Returns dict with time series of prices, inventory, PnL, and quotes.
    """
    rng = np.random.default_rng(seed)
    n_steps = int(p.T / p.dt)
    sigma_dt = p.sigma * np.sqrt(p.dt)

    # Storage
    S = np.zeros(n_steps + 1)
    q = np.zeros(n_steps + 1)
    cash = np.zeros(n_steps + 1)
    bids = np.zeros(n_steps)
    asks = np.zeros(n_steps)
    spreads = np.zeros(n_steps)

    S[0] = p.S0

    for i in range(n_steps):
        t = i * p.dt
        bid, ask = optimal_quotes(S[i], q[i], t, p)
        bids[i] = bid
        asks[i] = ask
        half_spread = (ask - bid) / 2
        spreads[i] = ask - bid

        # Poisson arrival probabilities in this time step
        p_ask = 1 - np.exp(-p.A * np.exp(-p.kappa * half_spread) * p.dt)
        p_bid = 1 - np.exp(-p.A * np.exp(-p.kappa * half_spread) * p.dt)

        # Check if ask or bid was hit
        ask_hit = rng.random() < p_ask
        bid_hit = rng.random() < p_bid

        # Update cash and inventory
        q[i + 1] = q[i]
        cash[i + 1] = cash[i]
        if ask_hit:  # Buyer hits our ask (we sell)
            q[i + 1] -= 1
            cash[i + 1] += ask
        if bid_hit:  # Seller hits our bid (we buy)
            q[i + 1] += 1
            cash[i + 1] -= bid

        # Price evolution
        S[i + 1] = S[i] + rng.normal(0, sigma_dt) * S[i]

    # Terminal PnL: mark inventory to market
    pnl = cash + q * S
    t_grid = np.linspace(0, p.T, n_steps + 1)

    return {
        "t": t_grid,
        "S": S,
        "q": q,
        "cash": cash,
        "pnl": pnl,
        "bids": bids,
        "asks": asks,
        "spreads": spreads,
    }


def plot_simulation(result: dict, p: ASParams) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
    t = result["t"]
    n = len(result["bids"])
    t_mid = t[:n]

    # Price and quotes
    axes[0].plot(t, result["S"], color="black", lw=1, label="Mid-price")
    axes[0].plot(t_mid, result["bids"], color="green", lw=0.8, alpha=0.7, label="Bid")
    axes[0].plot(t_mid, result["asks"], color="red", lw=0.8, alpha=0.7, label="Ask")
    axes[0].set_ylabel("Price ($)")
    axes[0].set_title("Avellaneda-Stoikov: Quotes and Mid-Price")
    axes[0].legend(fontsize=8)
    axes[0].grid(alpha=0.3)

    # Inventory
    axes[1].fill_between(t, result["q"], alpha=0.4, color="steelblue")
    axes[1].axhline(0, color="black", lw=0.8)
    axes[1].set_ylabel("Inventory (shares)")
    axes[1].set_title("Inventory Path")
    axes[1].grid(alpha=0.3)

    # PnL
    axes[2].plot(t, result["pnl"] - result["pnl"][0], color="purple", lw=1.5)
    axes[2].axhline(0, color="black", lw=0.8)
    axes[2].set_ylabel("P&L ($)")
    axes[2].set_xlabel("Time (days)")
    axes[2].set_title("Cumulative P&L (mark-to-market)")
    axes[2].grid(alpha=0.3)

    plt.tight_layout()
    plt.show()


def spread_sensitivity(p: ASParams) -> None:
    """Plot how spread components change over the trading session."""
    t_grid = np.linspace(0, p.T, 200)
    inv_terms = p.gamma * p.sigma**2 * (p.T - t_grid)
    as_term = (2 / p.gamma) * np.log1p(p.gamma / p.kappa)
    total = inv_terms + as_term

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.stackplot(
        t_grid * 6.5,  # convert to hours
        [inv_terms * 100, np.full_like(t_grid, as_term * 100)],
        labels=["Inventory risk spread", "Adverse selection spread"],
        colors=["steelblue", "coral"],
        alpha=0.7,
    )
    ax.set_xlabel("Time (hours into session)")
    ax.set_ylabel("Spread (cents on $100 stock)")
    ax.set_title("Optimal Spread Components Over Time")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    p = ASParams(sigma=0.02, gamma=0.1, kappa=1.5, A=140.0, dt=1/(252*390))
    result = simulate_market_making(p)

    print(f"Final inventory: {result['q'][-1]:.0f} shares")
    print(f"Total P&L: ${result['pnl'][-1] - result['pnl'][0]:.2f}")
    print(f"Initial spread: {optimal_spread(0, p)*100:.3f} cents")
    print(f"  -- inventory term: {p.gamma*p.sigma**2*p.T*100:.3f} cents")
    print(f"  -- adverse selection: {2/p.gamma*np.log1p(p.gamma/p.kappa)*100:.3f} cents")

    plot_simulation(result, p)
    spread_sensitivity(p)
```

---

## Bridge to Quant / ML

**RL for market making:**
The AS model gives a clean analytical baseline, but real order flow is not Poisson, prices are not BM, and the market maker competes with other HFT firms. RL agents (especially actor-critic methods) trained on historical or simulated LOB data can learn policies that adapt to:
- Autocorrelated order flow (momentum in arrivals)
- Non-stationary $\kappa$ (order sensitivity varies by time-of-day)
- Queue position effects (priority in the book)

The AS framework provides the state space, action space, and reward signal for RL formulations.

**ML for parameter estimation:**
- $\kappa$ (how fast order arrival drops with distance from mid): estimate from order book snapshot data by regressing fill rates against quote distance.
- $\sigma$ intraday: realized variance estimators (e.g., Parkinson or Bipower Variation) computed on high-frequency data.
- Adverse selection detection: classify arriving orders as informed vs. uninformed using features like order size, time-of-day, pre-trade price drift. Adjust $\gamma$ dynamically.

**Deep market making:**
- State: order book snapshot (L2 depth at multiple price levels) + own inventory + time features
- Action: bid/ask offsets from mid
- The AS model's reservation price idea generalizes: any deep net that predicts the optimal center of quotes is learning a nonlinear version of $r(q, t)$.

---

## Self-Assessment

### Level 1 — Conceptual

**Q1.** What is the "reservation price" in the Avellaneda-Stoikov model, and why does it differ from the mid-price?
> **A:** The reservation price r = s − qγσ²(T−t) is the market maker's indifference price — the price at which they're neutral between buying and selling given their current inventory q. When q > 0 (long inventory), r < s; the market maker shades quotes downward to attract sellers and reduce inventory exposure.

**Q2.** Why does the AS optimal spread increase as time-to-close T−t decreases?
> **A:** Wait — it actually decreases with time-to-close. As T−t shrinks, the inventory risk component γσ²(T−t) falls (less time for inventory to cause P&L harm), so the market maker can afford to quote tighter spreads. Near close, the spread collapses. At the start of the session, spreads are wide.

**Q3.** What practical limitation does the AS model have regarding adverse selection?
> **A:** The AS model treats all order flow as uninformed Poisson arrivals with known intensity. It doesn't model the possibility that some flow carries private information — adverse selection — which is a major real-world cost. Extensions like Cartea-Jaimungal add adverse selection terms, but the base AS model ignores it.

### Level 2 — Quantitative

**Q4.** Given σ = 0.02 (price vol per unit time), γ = 0.1 (risk aversion), T−t = 1 hour, k = 1.5 (order book depth parameter), current inventory q = +3 lots, and mid-price s = 100, compute the reservation price and the optimal bid/ask quotes.
> **A:** r = 100 − (3)(0.1)(0.0004)(1) = 100 − 0.00012 ≈ 99.9999 ≈ 100 (tiny effect at this scale). Half-spread δ/2 = γσ²(T−t)/2 + (1/γ)ln(1 + γ/k) = (0.1×0.0004×1)/2 + (1/0.1)ln(1 + 0.1/1.5) ≈ 0.00002 + 0.066 ≈ 0.066. Bid = r − δ/2 ≈ 99.934; Ask = r + δ/2 ≈ 100.066.

**Q5.** In the AS model, why is the optimal spread δ* independent of inventory q while the reservation price depends on q?
> **A:** The spread controls the rate of order arrivals (and thus fill probability), which is determined by market parameters (vol, risk aversion, order book depth) — not by current inventory. Inventory affects *where* to center the quotes (reservation price) but not *how wide* to set them. The two degrees of freedom are separated: reservation price handles inventory management, spread size handles profitability.

### Level 3 — Coding

**Q6.** Implement the Avellaneda-Stoikov optimal quotes: compute reservation price and optimal bid/ask given model parameters and current state.

```python
import numpy as np

def avellaneda_stoikov_quotes(s: float, q: int, t: float, T: float,
                               sigma: float, gamma: float, k: float) -> tuple:
    """
    Compute optimal bid and ask quotes under the Avellaneda-Stoikov model.
    
    Parameters
    ----------
    s     : current mid-price
    q     : current inventory (positive = long, negative = short)
    t     : current time
    T     : terminal time (e.g., end of trading session)
    sigma : price volatility (per unit time)
    gamma : risk aversion parameter (> 0)
    k     : order book depth parameter (arrival rate decay)
    
    Returns
    -------
    (bid, ask) : optimal bid and ask prices
    """
    # TODO: Implement using the AS closed-form formulas:
    # reservation_price = s - q * gamma * sigma**2 * (T - t)
    # half_spread = (gamma * sigma**2 * (T - t)) / 2 + (1/gamma) * log(1 + gamma/k)
    # bid = reservation_price - half_spread
    # ask = reservation_price + half_spread
    pass
```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| The AS model fully solves optimal market making | It ignores adverse selection, assumes Poisson arrivals, and has constant parameters — a starting point, not a production system |
| Inventory adjustment means changing the spread width | Inventory adjustment changes the *center* (reservation price), not the width; the spread width is set by risk/aversion and market depth |
| The optimal spread is always positive | For very low risk aversion (γ→0) and high order book depth, the spread approaches a minimum; it can't be negative (that would mean posting at a loss) |
| AS immediately generalizes to multi-asset market making | Multi-asset extensions require cross-inventory correlations and are significantly more complex; the single-asset solution doesn't extend trivially |

## Related Concepts

- [[Market Making]] — overview of the broader market making strategy
- [[Order Book]] — the LOB is the environment in which the AS model operates
- [[Adverse Selection]] — the structural cost that drives the second term of the optimal spread
- [[Price Impact]] — closely related: filling large orders impacts the price, asymmetrically affecting the MM
- [[Almgren-Chriss]] — sister model for execution; both solve HJB PDEs for optimal quoting/trading
- [[Avellaneda-Stoikov]] is extended to multi-asset market making, but those extensions are outside this note

---

## Sources Used

- Avellaneda, M., & Stoikov, S. (2008). *High-Frequency Trading in a Limit Order Book.* Quantitative Finance, 8(3), 217–224.
- Cartea, Á., Jaimungal, S., & Penalva, J. (2015). *Algorithmic and High-Frequency Trading.* Cambridge University Press. Ch. 10.
- Gueant, O. (2017). *The Financial Mathematics of Market Liquidity.* CRC Press.

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | Added tagline quote after frontmatter | QA review |
