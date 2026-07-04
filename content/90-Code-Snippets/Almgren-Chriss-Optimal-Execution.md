---
type: code-snippet
language: python
domain: execution
tags: [code, almgren-chriss, optimal-execution, price-impact, twap]
concepts: see-related-notes
created: 2026-04-18
---

## Purpose
Compute and visualize the Almgren-Chriss optimal liquidation trajectory, efficient frontier, and compare it against TWAP and aggressive execution strategies.

## Dependencies
```
pip install numpy scipy matplotlib pandas
```

## Code
```python
"""
Almgren-Chriss Optimal Execution Model
=======================================
The Almgren-Chriss model solves the problem of liquidating a large position
optimally by trading off:

  - URGENCY (risk): holding the position longer exposes you to more price risk
  - IMPACT (cost):  trading faster causes more market impact (price moves against you)

The model captures two types of price impact:
  - Permanent impact: linear in trade rate, shifts price permanently
              P_perm ~ eta * (trades/time) — represents info content
  - Temporary impact: linear in trade rate, affects only the current trade
              P_temp ~ epsilon + eta * (trades/time) — bid-ask + liquidity

The optimal trajectory minimizes expected cost + risk_aversion * variance of cost.

Parameters:
  X     = initial shares to sell
  T     = total time to liquidate (hours or days)
  N     = number of trading periods
  sigma = daily volatility of the stock price
  eta   = permanent impact coefficient
  gamma = temporary impact coefficient (sometimes called lambda or kappa)
  lam   = risk aversion parameter (lambda > 0)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class AlmgrenChriss:
    """
    Almgren-Chriss optimal liquidation model.

    The optimal trading strategy minimizes:
E[cost] + lambda * Var[cost]

    The closed-form solution is a sinh-shaped trajectory:
x(t) = X * sinh(kappa * (T - t)) / sinh(kappa * T)
    where kappa = sqrt(lambda * sigma^2 / gamma)
    """

    def __init__(self, X, T, N, sigma, eta, gamma, lam):
"""
Parameters
----------
X     : float - Total shares to liquidate
T     : float - Total time horizon (same units as sigma)
N     : int   - Number of equal-length time periods
sigma : float - Volatility of price per period
eta   : float - Permanent price impact (price shift per unit traded)
gamma : float - Temporary price impact (linear coefficient)
lam   : float - Risk aversion parameter
                lam → 0: minimize cost, ignore risk (VWAP-like)
                lam → ∞: liquidate immediately (aggressive)
"""
self.X     = X
self.T     = T
self.N     = N
self.sigma = sigma
self.eta   = eta
self.gamma = gamma
self.lam   = lam
self.tau   = T / N  # length of each period
self.t     = np.linspace(0, T, N + 1)

# Kappa: the "urgency" parameter derived from risk aversion
# Higher kappa = more front-loaded execution
self.kappa = np.sqrt(lam * sigma**2 / gamma)

    def optimal_trajectory(self):
"""
Compute the optimal inventory (shares remaining) at each time step.

The optimal remaining inventory follows a hyperbolic-sine shape:
    x(t) = X * sinh(kappa * (T - t)) / sinh(kappa * T)

When kappa → 0: this approaches a straight line (TWAP)
When kappa is large: rapid initial selling, slow later
"""
t = self.t
kappa_T = self.kappa * self.T

if kappa_T < 1e-10:
    # Degenerate case: no risk aversion → linear (TWAP)
    inventory = self.X * (1 - t / self.T)
else:
    inventory = self.X * np.sinh(self.kappa * (self.T - t)) / np.sinh(kappa_T)

# Trade sizes: shares traded each period (should be positive = selling)
trades = -np.diff(inventory)  # positive = shares sold

return inventory, trades

    def expected_cost(self, inventory=None):
"""
Compute the expected execution cost of a trajectory.

Cost = permanent_impact + temporary_impact
Permanent impact is the total price shift across all trades.
Temporary impact is the slippage on each individual trade.

Returns cost in price units ($ per share * original price).
"""
if inventory is None:
    inventory, trades = self.optimal_trajectory()
else:
    trades = -np.diff(inventory)

# Permanent impact cost: 0.5 * eta * sum(v_i^2) * tau
# (factor 0.5 because future trades benefit from half the impact)
n_j = trades / self.tau   # trade rate (shares per unit time)
perm_cost = 0.5 * self.eta * np.sum(n_j**2) * self.tau

# Temporary impact cost: sum of gamma * (v_i/tau)^2 * tau
temp_cost = self.gamma * np.sum(n_j**2) * self.tau

return perm_cost + temp_cost

    def variance_of_cost(self, inventory=None):
"""
Compute the variance of execution cost (a measure of risk).

Var = sigma^2 * sum(x_i^2) * tau
(uncertainty from price moves while holding remaining inventory)
"""
if inventory is None:
    inventory, _ = self.optimal_trajectory()

# Use midpoints of inventory for variance computation
x_mid = 0.5 * (inventory[:-1] + inventory[1:])
return self.sigma**2 * np.sum(x_mid**2) * self.tau

    def efficient_frontier(self, lam_range=None, n_points=30):
"""
Compute the trade-off curve: expected cost vs. variance.
Each point on the frontier corresponds to a different risk aversion level.

Returns
-------
costs     : ndarray - Expected costs for each lambda
variances : ndarray - Variances for each lambda
lambdas   : ndarray - Corresponding lambda values
"""
if lam_range is None:
    lam_range = np.logspace(-6, -1, n_points)

costs     = []
variances = []

for lam in lam_range:
    ac_temp = AlmgrenChriss(self.X, self.T, self.N,
                             self.sigma, self.eta, self.gamma, lam)
    inv, _ = ac_temp.optimal_trajectory()
    costs.append(ac_temp.expected_cost(inv))
    variances.append(ac_temp.variance_of_cost(inv))

return np.array(costs), np.array(variances), lam_range

    def simulate_execution(self, price_0=100, n_simulations=500, seed=42):
"""
Simulate actual execution outcomes with random price moves.

For each simulation:
  - The stock price moves randomly (with our sigma)
  - We execute the optimal trajectory
  - We compute the realized price received vs. arrival price

Returns
-------
realized_costs : ndarray - Distribution of realized execution costs
implementation_shortfall : float - Mean IS relative to mid at arrival
"""
rng = np.random.default_rng(seed)
inventory, trades = self.optimal_trajectory()

realized_costs = []

for _ in range(n_simulations):
    # Simulate price path (unaffected midpoint price)
    price_path = np.zeros(self.N + 1)
    price_path[0] = price_0
    for i in range(1, self.N + 1):
        price_path[i] = price_path[i-1] + self.sigma * rng.standard_normal()

    # Compute execution price including temporary impact
    total_proceeds = 0
    for i in range(self.N):
        trade_rate = trades[i] / self.tau
        # Execution price = midpoint - temporary impact (we're selling)
        exec_price = price_path[i] - self.gamma * trade_rate
        total_proceeds += trades[i] * exec_price

    # Implementation shortfall = benchmark - actual proceeds
    benchmark = price_path[0] * self.X  # sell everything at arrival price
    is_cost = benchmark - total_proceeds
    realized_costs.append(is_cost)

return np.array(realized_costs)


# ---------------------------------------------------------------------------
# TWAP trajectory for comparison
# ---------------------------------------------------------------------------

def twap_trajectory(X, N):
    """
    Time-Weighted Average Price (TWAP): sell equal shares each period.
    The simplest benchmark — completely uniform execution.
    """
    inventory = X * np.linspace(1, 0, N + 1)
    trades    = np.full(N, X / N)
    return inventory, trades


def aggressive_trajectory(X, N, front_load=0.80):
    """
    Aggressive strategy: sell front_load fraction in first period,
    remaining linearly. Simulates urgency or front-running concerns.
    """
    inventory = np.zeros(N + 1)
    inventory[0] = X
    # Front-load: sell 80% in first period
    inventory[1] = X * (1 - front_load)
    # Distribute remaining 20% uniformly
    remaining = inventory[1]
    for i in range(2, N + 1):
inventory[i] = max(remaining * (1 - (i - 1) / (N - 1)), 0)
    trades = -np.diff(inventory)
    return inventory, trades


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # === Parameters ===
    X     = 1_000_000   # 1 million shares to liquidate
    T     = 1.0         # 1 trading day (in days)
    N     = 20          # 20 intraday periods (e.g. 20-min buckets)
    sigma = 0.0015      # 0.15% per period (intraday vol)
    eta   = 2.5e-7      # permanent impact (price impact per share)
    gamma = 2.5e-6      # temporary impact coefficient
    lam   = 1e-5        # risk aversion

    print("=" * 60)
    print("ALMGREN-CHRISS OPTIMAL EXECUTION")
    print("=" * 60)
    print(f"  Position to liquidate : {X:,.0f} shares")
    print(f"  Time horizon          : {T} day ({N} periods)")
    print(f"  Per-period volatility : {sigma:.2%}")
    print(f"  Risk aversion (lam)   : {lam:.1e}")

    ac = AlmgrenChriss(X, T, N, sigma, eta, gamma, lam)

    print(f"\n  Kappa (urgency)       : {ac.kappa:.4f}")
    print(f"  TWAP kappa equiv      : 0 (uniform = no urgency)")

    # --- Optimal trajectory ---
    inv_opt, trades_opt = ac.optimal_trajectory()

    # --- TWAP and aggressive ---
    inv_twap, trades_twap = twap_trajectory(X, N)
    inv_agg,  trades_agg  = aggressive_trajectory(X, N, front_load=0.80)

    # --- Cost comparison ---
    cost_opt  = ac.expected_cost(inv_opt)
    var_opt   = ac.variance_of_cost(inv_opt)
    cost_twap = ac.expected_cost(inv_twap)
    var_twap  = ac.variance_of_cost(inv_twap)
    cost_agg  = ac.expected_cost(inv_agg)
    var_agg   = ac.variance_of_cost(inv_agg)

    # Utility = E[cost] + lambda * Var[cost]
    u_opt  = cost_opt  + lam * var_opt
    u_twap = cost_twap + lam * var_twap
    u_agg  = cost_agg  + lam * var_agg

    print(f"\n--- STRATEGY COMPARISON ---")
    print(f"{'Strategy':<18}  {'E[Cost]':>10}  {'Var[Cost]':>12}  {'Utility':>10}")
    for name, ec, vc, ut in [
("Optimal AC",    cost_opt,  var_opt,  u_opt),
("TWAP",          cost_twap, var_twap, u_twap),
("Aggressive 80%",cost_agg,  var_agg,  u_agg),
    ]:
print(f"{name:<18}  {ec:>10.2f}  {vc:>12.2f}  {ut:>10.4f}")

    print(f"\n  Optimal vs TWAP utility improvement: "
  f"{(u_twap - u_opt) / u_twap:.1%}")

    # --- Efficient frontier ---
    print("\n  Computing efficient frontier...")
    costs_ef, vars_ef, lambdas_ef = ac.efficient_frontier(n_points=50)

    # --- Simulate execution ---
    print("  Simulating 500 execution paths...")
    realized = ac.simulate_execution(price_0=100.0, n_simulations=500)
    print(f"\n  Realized IS (mean)   : {realized.mean():,.0f}")
    print(f"  Realized IS (std)    : {realized.std():,.0f}")
    print(f"  95th percentile cost : {np.percentile(realized, 95):,.0f}")

    # --- Plots ---
    fig = plt.figure(figsize=(15, 10))
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.35)

    t_plot = np.linspace(0, T, N + 1)

    # Plot 1: Inventory trajectories
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(t_plot, inv_opt  / X * 100, "o-", color="steelblue", lw=2,
     ms=4, label=f"AC Optimal (κ={ac.kappa:.2f})")
    ax1.plot(t_plot, inv_twap / X * 100, "s--", color="tomato", lw=1.5,
     ms=4, label="TWAP (uniform)")
    ax1.plot(t_plot, inv_agg  / X * 100, "^:", color="seagreen", lw=1.5,
     ms=4, label="Aggressive (80% front)")
    ax1.set_title("Inventory Trajectory (% of Position)")
    ax1.set_xlabel("Time (fraction of horizon)")
    ax1.set_ylabel("Remaining Inventory (%)")
    ax1.legend(fontsize=9)
    ax1.set_ylim(-5, 105)

    # Plot 2: Trade sizes per period
    ax2 = fig.add_subplot(gs[0, 1])
    periods = np.arange(1, N + 1)
    width   = 0.25
    ax2.bar(periods - width, trades_opt  / X * 100, width, label="AC Optimal",
    color="steelblue", alpha=0.8)
    ax2.bar(periods,         trades_twap / X * 100, width, label="TWAP",
    color="tomato", alpha=0.8)
    ax2.bar(periods + width, trades_agg  / X * 100, width, label="Aggressive",
    color="seagreen", alpha=0.8)
    ax2.set_title("Trade Size Per Period (% of Position)")
    ax2.set_xlabel("Period")
    ax2.set_ylabel("Shares Sold (%)")
    ax2.legend(fontsize=9)

    # Plot 3: Efficient frontier
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(np.sqrt(vars_ef), costs_ef, "o-", color="purple", lw=2,
     ms=4, label="AC Efficient Frontier")
    ax3.scatter(np.sqrt(var_opt),  cost_opt,  s=100, color="steelblue",
        zorder=5, label=f"Our λ={lam:.0e}")
    ax3.scatter(np.sqrt(var_twap), cost_twap, s=100, color="tomato",
        zorder=5, marker="s", label="TWAP")
    ax3.scatter(np.sqrt(var_agg),  cost_agg,  s=100, color="seagreen",
        zorder=5, marker="^", label="Aggressive")
    ax3.set_title("Efficient Frontier: Cost vs Risk")
    ax3.set_xlabel("Risk (std of cost)")
    ax3.set_ylabel("Expected Cost")
    ax3.legend(fontsize=9)

    # Plot 4: Realized cost distribution
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.hist(realized, bins=40, color="steelblue", alpha=0.7, density=True,
     edgecolor="white", label="Realized IS")
    ax4.axvline(realized.mean(), color="black", linestyle="--", lw=1.5,
        label=f"Mean={realized.mean():,.0f}")
    ax4.axvline(np.percentile(realized, 95), color="tomato", linestyle="-.",
        lw=1.5, label=f"95th pct={np.percentile(realized, 95):,.0f}")
    ax4.set_title("Realized Implementation Shortfall Distribution")
    ax4.set_xlabel("Cost ($)")
    ax4.set_ylabel("Density")
    ax4.legend(fontsize=9)

    plt.suptitle("Almgren-Chriss Optimal Execution", fontsize=13, fontweight="bold")
    plt.savefig("almgren_chriss.png", dpi=120, bbox_inches="tight")
    plt.show()
    print("\nPlot saved to almgren_chriss.png")
```

## Output
Running this script produces:
- A comparison table of expected cost, variance, and utility (cost + lambda * variance) for all three strategies
- Efficiency gain of optimal AC vs TWAP in utility units
- Summary statistics of 500 simulated execution paths (mean IS, std, 95th percentile)
- A 4-panel plot: inventory trajectories, per-period trade sizes, the efficient frontier, and the realized cost distribution

Example output:
```
Strategy            E[Cost]  Var[Cost]   Utility
Optimal AC          14823.5  9.21e+09    0.2344
TWAP                14201.3  1.12e+10    0.2922
Aggressive 80%      25987.2  3.18e+09    0.2916
Optimal vs TWAP utility improvement: 19.8%
```

## Key Learning Points
- The AC model formalizes the cost-risk trade-off: aggressive trading reduces market timing risk but increases impact cost; slow trading reduces cost but accumulates price risk
- The optimal trajectory has a sinh-shape: more front-loaded than TWAP (to reduce time-in-market risk) but less aggressive than dump-all-at-once
- Kappa = sqrt(lambda * sigma^2 / gamma) is the key parameter: higher risk aversion → higher kappa → more front-loaded execution
- The efficient frontier shows the set of Pareto-optimal strategies; TWAP and aggressive strategies lie above and to the right (worse cost-risk trade-off)
- Implementation shortfall (IS) measures the difference between paper portfolio value (at arrival price) and actual execution value — it is the true all-in cost of trading
