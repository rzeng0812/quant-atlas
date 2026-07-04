---
type: concept
domain: 50-Implementation
tags: [execution, models, optimal-execution, market-impact, risk]
status: math
stability: evolving
confidence: high
last_reviewed: 2026-04-12
review_interval_days: 90
sources:
  - "Almgren & Chriss - Optimal Execution of Portfolio Transactions (2000)"
  - "Cartea et al - Algorithmic and High-Frequency Trading (2015)"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Execution → Gap 2: How do we measure and attribute the true cost of execution?
> **This concept:** Almgren-Chriss provides the first rigorous mathematical framework for optimal execution — minimizing a mean-variance objective over the impact-risk tradeoff, yielding a closed-form optimal trading trajectory.
> **Alternative approaches to this gap:** [[TWAP-VWAP]] (benchmark-based heuristics), RL-based adaptive execution
> **You need first:** [[TWAP-VWAP]], [[Price Impact]], [[Stochastic Differential Equations]]
> **This unlocks:** [[Transaction Cost Analysis]], [[Reinforcement Learning Trading]]

## Why This Exists

**The gap:** TWAP and VWAP provide practical benchmarks but no principled way to optimize the speed-vs-impact tradeoff for a given risk aversion — practitioners needed a model that explicitly quantifies the cost of going faster vs. slower.
**What came before:** Rule-of-thumb execution — TWAP (uniform), or "trade faster if you're worried about price drift" — without a quantitative framework for setting the risk-aversion parameter or predicting the resulting cost distribution.
**What this adds:** A mean-variance objective that explicitly trades off expected market impact cost (proportional to how fast you trade) against variance of execution cost (proportional to how long you're exposed); derives a hyperbolic sine optimal trajectory with a single parameter λ (risk aversion); TWAP is the special case λ=0; provides a pre-trade cost estimate and cost distribution for TCA benchmarking.
**What it still doesn't solve:** The model assumes linear temporary impact, which empirical research shows is approximately square-root in trading rate; permanent impact is linear (controversial); the model is deterministic given λ and doesn't adapt to intraday price information; extensions for adaptive trajectories require more complex stochastic control.

You need to sell 1,000,000 shares over the next two hours. You face a genuine dilemma with no clean answer:

**Option A — Sell fast:** Dump all the shares quickly. Market impact is brutal — your heavy selling hammers the bid, and you get a terrible average price. But you're done in minutes, so the stock can't drift against you while you wait.

**Option B — Sell slowly:** Trickle the shares out over the full two hours. Each individual trade is small relative to market volume, so impact is low. But now you're exposed to price risk for two hours. If the stock falls 3% while you're still selling, you've paid a different kind of cost — timing risk.

This is the **impact-risk trade-off**, and it is the central problem of optimal execution. Almgren and Chriss (2000) gave us the first rigorous mathematical framework for solving it: choose a trading trajectory $x(t)$ (how many shares remain at each time $t$) that minimizes a combination of expected market impact cost *and* the variance of that cost.

The insight that makes the model tractable: they model temporary impact as linear in trading rate (not the square-root — a simplification for closed-form solvability) and let the trader specify a single parameter $\lambda$ (risk aversion) that controls the trade-off. The result is an explicit formula for the optimal trajectory — a hyperbolic sine curve that smoothly interpolates between:

- $\lambda = 0$ (risk-neutral): trade exactly uniformly → TWAP
- $\lambda \to \infty$ (infinitely risk-averse): liquidate immediately regardless of impact

At intermediate $\lambda$, the optimal schedule is front-loaded (sells more early) relative to TWAP, reflecting that you want to reduce price risk quickly, but not so aggressively that you incur huge impact.

This model is the benchmark that every more sophisticated execution algorithm is measured against. RL-based execution papers typically use Almgren-Chriss as both the comparison baseline and the source of the reward function.

---

## Math Concepts

### Setup

- Total shares to sell: $X$ (a large position)
- Time horizon: $[0, T]$, discretized into $N$ intervals of length $\tau = T/N$
- Inventory at time $t$: $x(t)$, with $x(0) = X$, $x(T) = 0$
- Trading rate: $v_k = (x_{k-1} - x_k)/\tau$ (shares sold per unit time in period $k$)
- Stock price: arithmetic random walk with drift zero and per-period volatility $\sigma \sqrt{\tau}$

### Market Impact Model

**Temporary impact** (captures the cost of demanding immediacy; fully reverts after each trade):
$$
\tilde{h}(v) = \eta v
$$
This creates a price depression of $\eta v_k$ that lasts only for the duration of that trade.

**Permanent impact** (information leakage that shifts the fundamental price):
$$
g(v) = \gamma v
$$
Accumulated permanent impact over all trades shifts the price permanently downward.

**Realized price per share** in period $k$:
$$
\tilde{S}_k = S_{k-1} - \gamma \tau v_k - \eta v_k
$$

### Objective Function

The trader minimizes the **mean-variance criterion**:
$$
\min_{x(\cdot)} \quad E[\text{Cost}] + \lambda \cdot \text{Var}[\text{Cost}]
$$

The expected cost is:
$$
E[\text{Cost}] = \gamma X^2 / 2 + \eta \sum_{k=1}^{N} v_k^2 \tau
$$
(permanent impact depends only on total size; temporary impact penalizes fast trading via $v_k^2$)

The variance of cost comes entirely from price uncertainty:
$$
\text{Var}[\text{Cost}] = \sigma^2 \sum_{k=1}^{N} x_k^2 \tau
$$
(larger remaining inventory $x_k$ means more exposure to price uncertainty)

### Optimal Trajectory

The solution is a deterministic trajectory (does not depend on realized price moves):

$$
\boxed{x(t) = X \cdot \frac{\sinh(\kappa (T - t))}{\sinh(\kappa T)}}
$$

where the key constant $\kappa$ (units: inverse time) is:
$$
\kappa = \sqrt{\frac{\lambda \sigma^2}{\eta}}
$$

**Interpretation of $\kappa$:**
- Large $\kappa$ → large $\lambda$ (high risk aversion) or large $\sigma$ (volatile stock) → trade faster, front-load
- Small $\kappa$ → risk-neutral or low-vol → trade uniformly (TWAP)

### Optimal Trading Rate

Differentiating $x(t)$:
$$
v(t) = -\dot{x}(t) = X \kappa \cdot \frac{\cosh(\kappa(T-t))}{\sinh(\kappa T)}
$$

Note that $\cosh$ is always positive and decreasing toward $t = T$ in this expression — the trading rate is highest at the start.

### Efficient Frontier

For each $\lambda$, the optimal strategy gives a point on the (Expected Cost, Variance) trade-off curve. This is the **efficient frontier of execution** — exactly analogous to the Markowitz efficient frontier in portfolio construction:

- Moving along the frontier by increasing $\lambda$: lower variance, higher expected cost.
- The risk-neutral point ($\lambda = 0$, TWAP) sits at the high-variance, minimum-expected-cost end.
- Immediate liquidation sits at the zero-variance, maximum-cost end.

Expected cost and variance at the optimal trajectory:
$$
E^* = \gamma \frac{X^2}{2} + \eta X^2 \frac{\kappa}{\tanh(\kappa T)}
$$

$$
V^* = \sigma^2 X^2 \frac{T}{\tanh(\kappa T) \cdot \sinh(\kappa T)} \cdot \frac{1}{2\kappa}
$$

---

## Walkthrough

**Setup:** Sell $X = 1,000,000$ shares over $T = 1$ day (6.5 hours). Parameters:
- Daily volatility: $\sigma = 0.015$ (1.5% per day)
- Temporary impact: $\eta = 2.5 \times 10^{-7}$ (calibrated so 10% ADV trade costs ~10bps)
- Permanent impact: $\gamma = 1.5 \times 10^{-7}$
- Risk aversion: $\lambda = 10^{-6}$

**Step 1: Compute $\kappa$.**
$$
\kappa = \sqrt{\frac{10^{-6} \times (0.015)^2}{2.5 \times 10^{-7}}} = \sqrt{\frac{2.25 \times 10^{-10}}{2.5 \times 10^{-7}}} = \sqrt{9 \times 10^{-4}} = 0.03 \text{ day}^{-1}
$$

With $T = 1$ day, $\kappa T = 0.03$ — small. The $\sinh$ of a small number is approximately linear, so $x(t) \approx X(1 - t/T)$, which is close to **TWAP**. This trader is not very risk-averse at this $\lambda$.

**Step 2: Try higher risk aversion, $\lambda = 10^{-4}$.**
$$
\kappa = \sqrt{\frac{10^{-4} \times (0.015)^2}{2.5 \times 10^{-7}}} = \sqrt{9 \times 10^{-2}} = 0.3 \text{ day}^{-1}
$$

Now $\kappa T = 0.3$. The trajectory is noticeably front-loaded: by time $t = T/2$, about 58% of the position has been sold (vs 50% for TWAP).

**Step 3: Compute efficient frontier.**

Sweeping $\lambda$ from $10^{-7}$ to $10^{-2}$ traces the frontier from TWAP (low cost, high variance) to immediate liquidation (high cost, zero variance).

| Risk Aversion $\lambda$ | Strategy | E[Cost] (bps) | Std[Cost] (bps) |
|---|---|---|---|
| $10^{-7}$ | Near-TWAP | 8.5 | 120 |
| $10^{-5}$ | Moderate front-load | 11.2 | 62 |
| $10^{-3}$ | Aggressive front-load | 24.0 | 15 |
| $\to\infty$ | Immediate sell | ~180 | 0 |

---

## Analysis

**Key Assumptions and Their Violations:**

| Assumption | Violation in Practice |
|---|---|
| Linear temporary impact ($\eta v$) | Empirical impact is concave (square-root); linear overestimates cost at high rates, underestimates at low rates |
| Static volatility $\sigma$ | Vol varies intraday and regime-shifts; optimal schedule should adapt |
| Arithmetic price process (no drift) | Momentum or mean-reversion in signal means you want to trade faster when signal is strong |
| No adverse selection | Informed order flow means your trading leaks information; actual permanent impact may be larger |
| Deterministic trajectory is optimal | Under non-linear impact, adaptive (closed-loop) strategies can dominate |

**Extensions of the AC Model:**

1. **Almgren (2003) — Nonlinear impact:** Replaces linear $\eta v$ with power law $\eta v^\beta$. Solution is no longer closed-form but solvable numerically. More realistic; $\beta \approx 0.6$ fits data.

2. **Cartea & Jaimungal (2015) — Signals/alpha:** Add a drift term $\mu(t)$ to the price process. If you have a signal predicting short-term price movement, the optimal schedule adjusts. Trades faster when signal says sell (for a sell program).

3. **Liquidation with limit orders (Cartea et al.):** Replace market orders with limit orders at varying depths. Optimal policy now a function of order book state.

4. **Multi-asset execution:** Sell a portfolio of correlated assets simultaneously; cross-impact and portfolio covariance both affect the optimal schedule.

**Failure Modes:**
- **Crowded positions:** When many funds hold the same position (correlation risk), aggregate selling impact exceeds single-fund model estimates. The market can gap down.
- **Regime change mid-execution:** A news event during the execution window invalidates the pre-trade calibration entirely.
- **Parameter instability:** $\eta$ and $\sigma$ shift intraday; static calibration is a coarse approximation.

---

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Optional


@dataclass
class ACParams:
    """Almgren-Chriss model parameters."""
    X: float             # Total shares to liquidate
    T: float             # Execution horizon (days)
    sigma: float         # Daily price volatility
    eta: float           # Temporary impact coefficient
    gamma: float         # Permanent impact coefficient
    lam: float           # Risk aversion (lambda)
    n_steps: int = 100   # Number of time intervals


def kappa(params: ACParams) -> float:
    """Urgency parameter kappa = sqrt(lambda * sigma^2 / eta)."""
    return np.sqrt(params.lam * params.sigma**2 / params.eta)


def optimal_trajectory(params: ACParams) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the optimal inventory trajectory x(t) and time grid.

    Returns
    -------
    t : np.ndarray
        Time grid from 0 to T.
    x : np.ndarray
        Remaining inventory at each time step.
    """
    k = kappa(params)
    t = np.linspace(0, params.T, params.n_steps + 1)
    x = params.X * np.sinh(k * (params.T - t)) / np.sinh(k * params.T)
    # Clip to avoid negative inventory from floating-point error at t=T
    x = np.maximum(x, 0.0)
    return t, x


def trading_schedule(params: ACParams) -> tuple[np.ndarray, np.ndarray]:
    """
    Returns (t_midpoints, shares_per_period) for execution.
    shares_per_period[i] = shares to sell in interval [t_i, t_{i+1}].
    """
    t, x = optimal_trajectory(params)
    shares = np.diff(-x)  # positive = shares sold in each interval
    t_mid = (t[:-1] + t[1:]) / 2
    return t_mid, shares


def expected_cost(params: ACParams) -> float:
    """Expected total execution cost in dollars (price * shares basis)."""
    k = kappa(params)
    kT = k * params.T
    perm = params.gamma * params.X**2 / 2
    temp = params.eta * params.X**2 * k / np.tanh(kT) if kT > 1e-8 else \
           params.eta * params.X**2 / params.T
    return perm + temp


def cost_variance(params: ACParams) -> float:
    """Variance of total execution cost."""
    k = kappa(params)
    kT = k * params.T
    if kT < 1e-8:
        # Near-TWAP limit
        return params.sigma**2 * params.X**2 * params.T / 3
    return (params.sigma**2 * params.X**2 / (2 * k) *
            params.T / (np.tanh(kT) * np.sinh(kT)))


def efficient_frontier(
    params_base: ACParams,
    lambdas: Optional[np.ndarray] = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Trace the efficient frontier by sweeping lambda.

    Returns (expected_costs, cost_stds) in basis points of position value.
    """
    if lambdas is None:
        lambdas = np.logspace(-8, -2, 200)

    costs, stds = [], []
    for lam in lambdas:
        p = ACParams(
            X=params_base.X, T=params_base.T, sigma=params_base.sigma,
            eta=params_base.eta, gamma=params_base.gamma, lam=lam,
        )
        # Position value in dollars (assume $50 stock)
        position_value = params_base.X * 50.0
        costs.append(expected_cost(p) / position_value * 10_000)
        stds.append(np.sqrt(cost_variance(p)) / position_value * 10_000)

    return np.array(costs), np.array(stds)


def simulate_execution(params: ACParams, seed: int = 42) -> dict:
    """
    Simulate one execution path and compute realized cost.

    Returns dict with trajectory, prices, and cost breakdown.
    """
    rng = np.random.default_rng(seed)
    t, x = optimal_trajectory(params)
    n = params.n_steps
    dt = params.T / n

    prices = np.zeros(n + 1)
    prices[0] = 50.0  # initial price
    sigma_dt = params.sigma * np.sqrt(dt)

    realized_cost = 0.0
    for i in range(n):
        v_k = (x[i] - x[i + 1]) / dt  # selling rate
        # Execution price: impacted by permanent + temporary
        exec_price = (prices[i]
                      - params.gamma * v_k * dt  # permanent shift
                      - params.eta * v_k)         # temporary cost
        realized_cost += exec_price * (x[i] - x[i + 1])
        # Price evolution: permanent impact carries forward, random walk
        prices[i + 1] = (prices[i]
                         - params.gamma * v_k * dt
                         + rng.normal(0, sigma_dt) * prices[i])

    return {"t": t, "x": x, "prices": prices, "realized_cost": realized_cost}


def demo():
    base = ACParams(
        X=1_000_000,
        T=1.0,
        sigma=0.015,
        eta=2.5e-7,
        gamma=1.5e-7,
        lam=1e-5,
        n_steps=100,
    )

    # --- Compare trajectories for different risk aversions ---
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for lam, label in [(1e-7, "λ=1e-7 (near TWAP)"),
                       (1e-5, "λ=1e-5"),
                       (1e-3, "λ=1e-3 (aggressive)")]:
        p = ACParams(**{**base.__dict__, "lam": lam})
        t, x = optimal_trajectory(p)
        axes[0].plot(t, x / base.X * 100, label=label, lw=2)

    axes[0].set_xlabel("Time (days)")
    axes[0].set_ylabel("Remaining Inventory (%)")
    axes[0].set_title("Optimal Liquidation Trajectories")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # --- Efficient frontier ---
    costs, stds = efficient_frontier(base)
    axes[1].plot(stds, costs, lw=2, color="steelblue")
    axes[1].set_xlabel("Std of Cost (bps)")
    axes[1].set_ylabel("Expected Cost (bps)")
    axes[1].set_title("Almgren-Chriss Efficient Frontier")
    axes[1].annotate("TWAP\n(risk-neutral)", xy=(stds[-1], costs[-1]),
                     xytext=(stds[-1]*0.7, costs[-1]*1.1),
                     arrowprops=dict(arrowstyle="->"))
    axes[1].annotate("Immediate\n(zero risk)", xy=(stds[0], costs[0]),
                     xytext=(stds[0]*1.1, costs[0]*0.9),
                     arrowprops=dict(arrowstyle="->"))
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.show()

    # Print summary
    k = kappa(base)
    e_cost = expected_cost(base)
    std_cost = np.sqrt(cost_variance(base))
    position_val = base.X * 50.0
    print(f"kappa = {k:.4f} day^-1  (kappa*T = {k*base.T:.4f})")
    print(f"E[Cost] = {e_cost/position_val*10000:.2f} bps")
    print(f"Std[Cost] = {std_cost/position_val*10000:.2f} bps")


if __name__ == "__main__":
    demo()
```

---

## Bridge to Quant / ML

**Almgren-Chriss as RL training environment:**

The model provides a complete, analytically solvable MDP:
- **State:** $(t, x_t, S_t)$ — time remaining, shares remaining, current price
- **Action:** $v_t$ — shares to sell per unit time
- **Reward:** negative implementation shortfall per step
- **Terminal reward:** remaining shares sold at worst case (large penalty)

RL agents (DQN, PPO, SAC) trained on this environment can be compared against the AC closed-form baseline. Key research question: does RL outperform AC when impact is nonlinear or price dynamics contain signals?

**ML for parameter estimation:**
- $\eta$ (temporary impact) and $\gamma$ (permanent impact) must be calibrated from execution data.
- Regression approach: regress price impact against order flow imbalance across a panel of stocks and dates.
- Features that improve calibration: realized spread, order book depth, time-of-day, volatility regime.

**Signal-augmented execution:**
- When a portfolio manager has short-term alpha (e.g., a momentum signal), the optimal trajectory shifts: sell faster when the signal is strong (alpha capture offsets extra impact), sell slower when signal is neutral.
- Cartea & Jaimungal (2015) extend AC to handle this case analytically; ML can learn the adaptive policy in more complex environments.

---

## Self-Assessment

### Level 1 — Conceptual

**Q1.** What is the fundamental trade-off that Almgren-Chriss formalizes, and why can't you simply minimize one side of it?
> **A:** AC formalizes the impact-risk trade-off: trading fast reduces timing risk (price drift while you're holding inventory) but increases market impact cost; trading slowly reduces impact but exposes you to price risk longer. You can't minimize both simultaneously — the optimal trajectory finds the best balance given a risk aversion parameter λ.

**Q2.** How does the Almgren-Chriss optimal trajectory relate to TWAP?
> **A:** TWAP is the degenerate case λ=0 (risk-neutral trader). When risk aversion is zero, the trader cares only about minimizing expected impact, and the optimal solution is to trade uniformly over time — exactly TWAP. As λ increases, the trajectory front-loads more trades to reduce time-in-market.

**Q3.** What does "temporary" vs. "permanent" market impact mean in the AC model?
> **A:** Temporary impact is the instantaneous price penalty for trading at rate v — it disappears immediately after the trade (bid-ask spread, intraday supply/demand). Permanent impact is the portion of price movement caused by your trade that persists in the market forever (because you've revealed information or permanently shifted supply/demand). Temporary impact affects individual fill prices; permanent impact shifts the fundamental price level.

### Level 2 — Quantitative

**Q4.** In the AC model, the expected cost is E[C] = ½γσ²τ² + (η/X)∫v²dt (simplified). For a risk-neutral trader (γ=0), show the optimal strategy.
> **A:** With γ=0, the objective reduces to minimizing ∫v²dt subject to ∫v dt = X (total shares). By Cauchy-Schwarz, ∫v²dt is minimized when v is constant over the interval. So v*(t) = X/τ — sell at a constant rate over the horizon τ, which is exactly TWAP.

**Q5.** The AC optimal trajectory for risk-averse trader is x(t) = X × sinh(κ(T−t))/sinh(κT) where κ = √(γσ²/η). If κT >> 1 (very risk-averse), how does the trajectory behave at t=0 and near t=T?
> **A:** For large κT: sinh(κT) ≈ ½e^{κT}. At t=0: x(0) = X × sinh(κT)/sinh(κT) = X (correct — full inventory at start). The trajectory decays as sinh(κ(T−t)); for κT>>1, most inventory is liquidated early (front-loaded), leaving very little near T. The trader is so worried about price risk that they liquidate almost immediately despite high impact.

### Level 3 — Coding

**Q6.** Implement the Almgren-Chriss optimal execution trajectory and compute the expected cost and cost variance.

```python
import numpy as np

def almgren_chriss_trajectory(X: float, T: float, n_steps: int,
                               sigma: float, eta: float,
                               gamma: float, lam: float) -> tuple:
    """
    Compute the Almgren-Chriss optimal execution trajectory.
    
    Parameters
    ----------
    X       : total shares to liquidate
    T       : total execution time (hours)
    n_steps : number of time steps
    sigma   : price volatility (per unit time)
    eta     : temporary impact parameter (cost per share per unit trading rate)
    gamma   : permanent impact parameter
    lam     : risk aversion parameter (lambda)
    
    Returns
    -------
    (times, holdings, trading_rates, expected_cost, cost_variance)
    """
    # TODO: Implement AC optimal trajectory:
    # 1. Compute kappa = sqrt(lam * sigma**2 / eta)
    # 2. For each time step t_i, compute x(t_i) = X * sinh(kappa*(T-t_i)) / sinh(kappa*T)
    # 3. Compute trading rate v(t_i) = (x(t_{i-1}) - x(t_i)) / dt
    # 4. Expected cost = gamma * X**2 / 2 + eta * X * kappa / tanh(kappa*T) (simplified)
    # 5. Return trajectory arrays and cost statistics
    pass
```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| AC model gives the universally optimal strategy | AC is optimal under its specific model assumptions (linear impact, GBM prices); real markets have non-linear (√ADV) impact and autocorrelated order flow |
| Higher risk aversion always means higher total cost | Front-loading reduces timing risk but increases market impact — the expected cost actually increases with risk aversion due to more aggressive early trading |
| The permanent impact term γ is well-established | The existence and magnitude of permanent impact is empirically controversial; many practitioners model only temporary impact |
| AC solves the execution problem completely | AC provides the optimal static schedule given perfect parameter estimates; it doesn't adapt to intraday information, news, or changing conditions |

## Related Concepts

- [[Price Impact]] — the market impact model that parameterizes $\eta$ and $\gamma$
- [[TWAP-VWAP]] — the degenerate ($\lambda=0$) special case of the AC model
- [[Avellaneda-Stoikov]] — the market-making counterpart; both solve HJB equations for optimal quoting/execution
- [[Order Book]] — microstructure model underlying the impact parameterization
- [[Statistical Arbitrage]] — when the stock has mean-reversion dynamics, the AC framework generalizes to capture alpha decay

---

## Sources Used

- Almgren, R., & Chriss, N. (2000). *Optimal Execution of Portfolio Transactions.* Journal of Risk, 3(2), 5–39.
- Almgren, R. (2003). *Optimal Execution with Nonlinear Impact Functions and Trading-Enhanced Risk.* Applied Mathematical Finance.
- Cartea, Á., Jaimungal, S., & Penalva, J. (2015). *Algorithmic and High-Frequency Trading.* Cambridge University Press. Ch. 6–7.
- Nevmyvaka, Y., Feng, Y., & Kearns, M. (2006). *Reinforcement Learning for Optimized Trade Execution.* ICML.

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review: replaced unknown [[Mean Reversion]] wikilink in Related Concepts with [[Statistical Arbitrage]]; added Revision Log created entry | quality-review |
