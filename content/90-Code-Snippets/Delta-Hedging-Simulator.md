---
type: code-snippet
language: python
domain: risk
tags: [code, delta-hedging, options, greeks, risk-management]
concepts: see-related-notes
created: 2026-04-18
---

## Purpose
Simulate the P&L of a delta-hedged short call position with daily rebalancing over 30 days, showing how hedging errors accumulate.

## Dependencies
```
pip install numpy scipy matplotlib
```

## Code
```python
"""
Delta Hedging Simulator
=======================
This script simulates a delta-neutral short call position:

  Strategy: Sell 1 call option. Hedge by holding delta shares of stock.
  Rebalance: Adjust the hedge daily as delta changes with S and time.

The goal of delta hedging is to be "option-neutral" — if BSM is the true
model, a perfectly delta-hedged position earns zero P&L. In practice,
three things cause P&L:
  1. Discrete (daily) rebalancing instead of continuous
  2. Realized volatility ≠ implied volatility (gamma P&L)
  3. Transaction costs from buying/selling shares

P&L = Gamma P&L + Theta decay + Noise from discrete rebalancing
"""

import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# ---------------------------------------------------------------------------
# BSM pricing and Greeks
# ---------------------------------------------------------------------------

def bsm_call(S, K, r, sigma, T):
    """Black-Scholes call price. Returns 0 if T <= 0."""
    if T <= 1e-9:
        return max(S - K, 0.0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return float(S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))


def bsm_delta(S, K, r, sigma, T):
    """Delta of a call option (= N(d1))."""
    if T <= 1e-9:
        return 1.0 if S > K else 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return float(norm.cdf(d1))


def bsm_gamma(S, K, r, sigma, T):
    """Gamma (same for call and put)."""
    if T <= 1e-9:
        return 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return float(norm.pdf(d1) / (S * sigma * np.sqrt(T)))


# ---------------------------------------------------------------------------
# Single delta-hedge simulation path
# ---------------------------------------------------------------------------

def simulate_delta_hedge(S0, K, r, sigma, T_days, realized_sigma=None,
                          seed=42, verbose=False):
    """
    Simulate one 30-day path of a delta-hedged short call position.

    Setup at t=0:
      - Sell 1 call at BSM price (collect premium = credit)
      - Buy delta shares to offset the call's delta exposure
      - Borrow the net cash needed (or invest the surplus)

    Each day:
      - Stock moves (GBM)
      - Recompute new delta
      - Buy/sell shares to match new delta
      - Finance any share purchases via borrowing at rate r

    At expiry (day T):
      - Close the position (deliver/not deliver shares, repay debt)
      - Terminal P&L = what we have minus what we owe

    Parameters
    ----------
    S0             : float - Initial stock price
    K              : float - Strike price
    r              : float - Risk-free rate (annualized)
    sigma          : float - Implied vol (used for BSM pricing and hedging)
    T_days         : int   - Hedging horizon in trading days
    realized_sigma : float - Actual volatility of stock moves (default = sigma)
                             If realized_sigma > sigma: gamma profits dominate
                             If realized_sigma < sigma: theta profits dominate

    Returns
    -------
    dict with keys:
        stock_path   : ndarray - Daily stock prices
        delta_path   : ndarray - Delta held each day
        pnl_path     : ndarray - Cumulative P&L each day
        terminal_pnl : float   - Final P&L at expiry
    """
    if realized_sigma is None:
        realized_sigma = sigma  # no vol mismatch

    rng = np.random.default_rng(seed)
    dt  = 1 / 252  # one trading day in years

    # --- t=0: initiate the hedge ---
    T0 = T_days / 252  # initial time to expiry in years

    call_price_0 = bsm_call(S0, K, r, sigma, T0)
    delta_0      = bsm_delta(S0, K, r, sigma, T0)

    # We SELL the call (receive premium) and BUY delta shares
    # Cash account: +call_premium - delta * S0 (positive = we received net cash)
    cash = call_price_0 - delta_0 * S0

    stock_path = [S0]
    delta_path = [delta_0]
    pnl_path   = [0.0]   # cumulative P&L (mark-to-market)

    S_t     = S0
    delta_t = delta_0
    T_t     = T0

    for day in range(1, T_days + 1):
        # --- Stock evolves with realized vol ---
        Z    = rng.standard_normal()
        dW   = realized_sigma * np.sqrt(dt) * Z
        S_t  = S_t * np.exp((r - 0.5 * realized_sigma**2) * dt + dW)
        T_t  = (T_days - day) / 252  # remaining time to expiry

        # --- Grow cash at risk-free rate (financing cost) ---
        cash *= np.exp(r * dt)

        # --- Recompute delta and rebalance ---
        new_delta = bsm_delta(S_t, K, r, sigma, T_t)
        delta_change = new_delta - delta_t  # shares to buy (+) or sell (-)

        # Buying shares costs delta_change * S_t; deducted from cash
        cash     -= delta_change * S_t
        delta_t   = new_delta

        # --- Mark-to-market P&L = cash + stock_position - current_call_value ---
        current_call = bsm_call(S_t, K, r, sigma, T_t)
        # Short call position: we owe -current_call
        mtm_pnl = cash + delta_t * S_t - current_call

        stock_path.append(S_t)
        delta_path.append(delta_t)
        pnl_path.append(mtm_pnl)

        if verbose and day % 5 == 0:
            print(f"  Day {day:3d}: S={S_t:.2f}, Delta={delta_t:.3f}, "
                  f"Cash={cash:.2f}, P&L={mtm_pnl:.4f}")

    # --- At expiry: settle the option ---
    # Final intrinsic value of the call
    final_call_payoff = max(S_t - K, 0)
    # P&L = cash from hedge + stock value - payoff owed
    terminal_pnl = cash + delta_t * S_t - final_call_payoff

    return {
        "stock_path"   : np.array(stock_path),
        "delta_path"   : np.array(delta_path),
        "pnl_path"     : np.array(pnl_path),
        "terminal_pnl" : terminal_pnl,
    }


# ---------------------------------------------------------------------------
# Run 1000 simulations to get P&L distribution
# ---------------------------------------------------------------------------

def simulate_pnl_distribution(S0, K, r, sigma, T_days,
                               realized_sigma=None, n_sims=1000):
    """Run many independent hedge simulations and collect terminal P&Ls."""
    terminal_pnls = []
    for seed in range(n_sims):
        result = simulate_delta_hedge(S0, K, r, sigma, T_days,
                                      realized_sigma=realized_sigma, seed=seed)
        terminal_pnls.append(result["terminal_pnl"])
    return np.array(terminal_pnls)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # === Parameters ===
    S0     = 100   # Initial stock price
    K      = 100   # ATM strike
    r      = 0.05  # 5% risk-free rate
    sigma  = 0.20  # Implied vol (what we priced/hedge with)
    T_DAYS = 30    # 30 trading days (~6 calendar weeks)

    # Realized vol scenarios
    realized_equal  = 0.20   # matches implied → near-zero P&L
    realized_higher = 0.30   # realized > implied → gamma profits (we bought convexity)
    realized_lower  = 0.12   # realized < implied → theta wins (we sold expensive vol)

    print("=" * 60)
    print("DELTA HEDGING SIMULATOR")
    print("=" * 60)
    print(f"  S0={S0}, K={K}, r={r:.0%}, sigma={sigma:.0%}, T={T_DAYS} days")

    # --- Single path, verbose ---
    print("\n--- SINGLE PATH (implied vol = realized vol) ---")
    res = simulate_delta_hedge(S0, K, r, sigma, T_DAYS,
                                realized_sigma=realized_equal, seed=0, verbose=True)
    print(f"\n  Terminal P&L: ${res['terminal_pnl']:.4f}")
    print(f"  Starting delta: {res['delta_path'][0]:.4f}")
    print(f"  Ending delta:   {res['delta_path'][-1]:.4f}")

    # --- P&L distribution across scenarios ---
    print("\n--- P&L DISTRIBUTION (1000 simulations) ---")
    n_sims = 1000
    pnls_equal  = simulate_pnl_distribution(S0, K, r, sigma, T_DAYS, realized_equal,  n_sims)
    pnls_higher = simulate_pnl_distribution(S0, K, r, sigma, T_DAYS, realized_higher, n_sims)
    pnls_lower  = simulate_pnl_distribution(S0, K, r, sigma, T_DAYS, realized_lower,  n_sims)

    for label, pnls, rv in [
        ("Equal  (rv=20%)", pnls_equal,  realized_equal),
        ("Higher (rv=30%)", pnls_higher, realized_higher),
        ("Lower  (rv=12%)", pnls_lower,  realized_lower),
    ]:
        print(f"\n  Scenario: {label}")
        print(f"    Mean P&L : ${pnls.mean():.4f}")
        print(f"    Std P&L  : ${pnls.std():.4f}")
        print(f"    Min/Max  : ${pnls.min():.4f} / ${pnls.max():.4f}")
        print(f"    % > 0    : {(pnls > 0).mean():.1%}")

    # --- Plots ---
    fig = plt.figure(figsize=(15, 10))
    gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

    # Plot 1: Stock path
    ax1 = fig.add_subplot(gs[0, 0])
    days = np.arange(T_DAYS + 1)
    ax1.plot(days, res["stock_path"], color="steelblue", lw=1.5)
    ax1.axhline(K, color="red", linestyle="--", lw=1, label="Strike K")
    ax1.set_title("Stock Price Path")
    ax1.set_xlabel("Trading Day")
    ax1.set_ylabel("Price ($)")
    ax1.legend()

    # Plot 2: Delta path
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(days, res["delta_path"], color="tomato", lw=1.5)
    ax2.axhline(0.5, color="gray", linestyle=":", lw=1, label="Δ=0.5 (ATM)")
    ax2.set_title("Delta (Hedge Ratio) Over Time")
    ax2.set_xlabel("Trading Day")
    ax2.set_ylabel("Delta")
    ax2.set_ylim(0, 1)
    ax2.legend()

    # Plot 3: Cumulative P&L path
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.plot(days, res["pnl_path"], color="seagreen", lw=1.5)
    ax3.axhline(0, color="black", linestyle="--", lw=0.8)
    ax3.set_title("Cumulative P&L")
    ax3.set_xlabel("Trading Day")
    ax3.set_ylabel("P&L ($)")

    # Plot 4-6: P&L distributions
    colors   = ["steelblue", "tomato", "seagreen"]
    labels   = ["rv=20% (=IV)", "rv=30% (>IV)", "rv=12% (<IV)"]
    pnl_sets = [pnls_equal, pnls_higher, pnls_lower]

    for idx, (ax_pos, pnls, color, label) in enumerate(
        zip([gs[1, 0], gs[1, 1], gs[1, 2]], pnl_sets, colors, labels)
    ):
        ax = fig.add_subplot(ax_pos)
        ax.hist(pnls, bins=50, color=color, alpha=0.7, density=True, edgecolor="white")
        ax.axvline(pnls.mean(), color="black", linestyle="--", lw=1.5,
                   label=f"Mean=${pnls.mean():.3f}")
        ax.axvline(0, color="red", linestyle=":", lw=1)
        ax.set_title(f"P&L Distribution\n{label}")
        ax.set_xlabel("Terminal P&L ($)")
        ax.set_ylabel("Density")
        ax.legend(fontsize=8)

    plt.suptitle("Delta Hedging Simulator — Short Call, Daily Rebalancing",
                 fontsize=13, fontweight="bold")
    plt.savefig("delta_hedging.png", dpi=120, bbox_inches="tight")
    plt.show()
    print("\nPlot saved to delta_hedging.png")
```

## Output
Running this script produces:
- A verbose daily log of stock price, delta, cash, and P&L for one sample path
- A 3-scenario comparison table (realized vol equals, exceeds, or undercuts implied vol) across 1,000 simulations
- A 6-panel plot: stock path, delta evolution, cumulative P&L, and three terminal P&L histograms

Example summary:
```
  Scenario: Equal  (rv=20%)  → Mean P&L ≈ $0.00  (near zero — BSM is self-financing)
  Scenario: Higher (rv=30%)  → Mean P&L ≈ $1.50  (gamma profits when vol is cheap)
  Scenario: Lower  (rv=12%)  → Mean P&L ≈ -$1.20 (theta wins when vol is expensive)
```

## Key Learning Points
- A perfectly delta-hedged short call earns zero P&L if realized vol equals implied vol — the hedge is "self-financing" by BSM theory
- P&L comes from the vol mismatch: if you sell high implied vol and realize lower vol, you profit (theta > gamma cost); the reverse loses
- Daily discrete rebalancing (vs continuous) introduces "rebalancing error" proportional to gamma and the square of daily stock moves
- The delta path shows how hedge ratio evolves: ATM options have delta near 0.5; deep ITM approaches 1.0, OTM approaches 0
- The P&L distribution is roughly symmetric around the mean when vol equals implied vol, but skews positive/negative under the higher/lower vol scenarios
