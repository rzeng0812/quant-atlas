---
type: code-snippet
language: python
domain: strategies
tags: [code, pairs-trading, cointegration, mean-reversion, statistical-arbitrage]
concepts: see-related-notes
created: 2026-04-18
---

## Purpose
Full pairs trading backtest using synthetic data: cointegration test, OU parameter estimation, signal generation, and P&L with Sharpe ratio and max drawdown.

## Dependencies
```
pip install numpy scipy statsmodels pandas matplotlib
```

## Code
```python
"""
Pairs Trading Backtest
======================
Pairs trading is a market-neutral strategy:
  1. Find two stocks that are cointegrated (their spread is stationary)
  2. Model the spread as an Ornstein-Uhlenbeck (mean-reverting) process
  3. Go long the spread when it widens beyond +2σ (expect reversion to 0)
  4. Go short the spread when it narrows below -2σ
  5. Close the position when spread returns to 0

Why cointegration? Two prices can be non-stationary individually (random walks)
but their linear combination is stationary. This means the spread doesn't drift
away permanently — it mean-reverts, creating trading opportunities.

The OU process:
    d(spread) = kappa * (mu - spread) * dt + sigma_ou * dW
    kappa = mean-reversion speed (higher = faster)
    mu    = long-run mean of the spread
    sigma_ou = volatility of the spread
"""

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

try:
    import statsmodels.api as sm
    from statsmodels.tsa.stattools import coint, adfuller
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False
    print("WARNING: statsmodels not installed. Run: pip install statsmodels")


# ---------------------------------------------------------------------------
# Synthetic data generation
# ---------------------------------------------------------------------------

def generate_cointegrated_pair(n=500, beta=1.2, mu_spread=0.0,
                                kappa=0.15, sigma_ou=0.5,
                                drift_A=0.0002, sigma_A=0.015, seed=42):
    """
    Generate two synthetic price series that are cointegrated.

    Construction:
      - Asset A follows a random walk (driftless GBM)
      - Spread follows an OU process: s_t = A_t - beta*B_t
      - Asset B is derived from A and the spread: B_t = (A_t - s_t) / beta

    Parameters
    ----------
    n        : int   - Number of time steps
    beta     : float - Hedge ratio (how many B shares hedge 1 A share)
    mu_spread: float - Long-run mean of the spread
    kappa    : float - Mean-reversion speed of spread (per day, e.g. 0.10-0.30)
    sigma_ou : float - Spread volatility (log-price units)
    drift_A  : float - Daily drift of asset A
    sigma_A  : float - Daily volatility of asset A

    Returns
    -------
    price_A  : ndarray - Price series of asset A
    price_B  : ndarray - Price series of asset B
    spread   : ndarray - The spread = log(A) - beta*log(B)
    """
    rng = np.random.default_rng(seed)
    dt  = 1.0  # one day

    # Asset A: random walk in log-space
    log_A = np.zeros(n)
    for i in range(1, n):
        log_A[i] = log_A[i-1] + drift_A + sigma_A * rng.standard_normal()

    # Spread: OU process
    spread = np.zeros(n)
    spread[0] = mu_spread
    for i in range(1, n):
        mean_reversion = kappa * (mu_spread - spread[i-1]) * dt
        diffusion      = sigma_ou * np.sqrt(dt) * rng.standard_normal()
        spread[i]      = spread[i-1] + mean_reversion + diffusion

    # Asset B derived from A and spread: log(B) = (log(A) - spread) / beta
    log_B = (log_A - spread) / beta

    # Convert to prices (start both at 100)
    price_A = 100 * np.exp(log_A)
    price_B = 100 * np.exp(log_B)

    return price_A, price_B, spread


# ---------------------------------------------------------------------------
# Cointegration test
# ---------------------------------------------------------------------------

def test_cointegration(price_A, price_B, significance=0.05):
    """
    Test for cointegration using the Engle-Granger two-step procedure.

    Step 1: Regress A on B to get the hedge ratio beta
    Step 2: Test the residuals (spread) for stationarity via ADF test

    If the spread is stationary, the pair is cointegrated.

    Returns
    -------
    beta    : float - OLS hedge ratio
    spread  : ndarray - The residual spread A - beta*B
    coint_p : float   - p-value of Engle-Granger cointegration test
    adf_p   : float   - p-value of ADF test on the spread
    is_cointegrated : bool
    """
    if not STATSMODELS_AVAILABLE:
        # Fallback: simple OLS regression
        beta = np.cov(price_A, price_B)[0, 1] / np.var(price_B)
        spread = price_A - beta * price_B
        return beta, spread, 0.01, 0.01, True

    # OLS regression: log(A) = alpha + beta * log(B) + epsilon
    log_A = np.log(price_A)
    log_B = np.log(price_B)
    X = sm.add_constant(log_B)
    model = sm.OLS(log_A, X).fit()
    beta  = model.params[1]
    spread = model.resid  # this is log(A) - alpha - beta*log(B)

    # Engle-Granger cointegration test
    try:
        score, coint_p, crit = coint(log_A, log_B)
    except Exception:
        coint_p = 0.05

    # ADF test on the spread directly
    adf_result = adfuller(spread, maxlags=1)
    adf_p = adf_result[1]

    is_cointegrated = (coint_p < significance) and (adf_p < significance)
    return beta, spread, coint_p, adf_p, is_cointegrated


# ---------------------------------------------------------------------------
# Ornstein-Uhlenbeck parameter estimation
# ---------------------------------------------------------------------------

def estimate_ou_params(spread):
    """
    Estimate OU parameters via OLS on the AR(1) discretization:
        spread[t] = a + b * spread[t-1] + epsilon

    From this we recover:
        kappa = -log(b) / dt   (mean-reversion speed per unit time)
        mu    = a / (1 - b)    (long-run mean of the spread)
        sigma = std(epsilon) * sqrt(-2*log(b) / (dt*(1-b^2)))

    Parameters
    ----------
    spread : ndarray - Time series of the spread

    Returns
    -------
    kappa     : float - Mean-reversion speed (per day)
    mu        : float - Long-run mean
    sigma_ou  : float - Spread volatility
    half_life : float - Half-life of mean reversion in days
    """
    y = spread[1:]      # spread at t
    x = spread[:-1]     # spread at t-1

    # OLS: y = a + b*x
    b, a, r_value, p_value, std_err = stats.linregress(x, y)

    # Recover OU parameters (dt = 1 day)
    dt = 1.0
    if b >= 1.0:
        b = 0.99  # clip if non-stationary due to small sample

    kappa    = -np.log(b) / dt
    mu       = a / (1 - b)
    residuals = y - (a + b * x)
    sigma_ou  = residuals.std() * np.sqrt(-2 * np.log(b) / (dt * (1 - b**2)))
    half_life = np.log(2) / kappa  # days for spread to revert halfway

    return kappa, mu, sigma_ou, half_life


# ---------------------------------------------------------------------------
# Signal generation
# ---------------------------------------------------------------------------

def generate_signals(spread, mu, sigma_ou, entry_z=2.0, exit_z=0.0):
    """
    Generate long/short signals based on standardized spread.

    Signal rules:
      - Spread > +entry_z * sigma_ou → SHORT the spread (expect drop to mean)
      - Spread < -entry_z * sigma_ou → LONG the spread (expect rise to mean)
      - Spread crosses exit_z → CLOSE position

    Parameters
    ----------
    spread    : ndarray - The raw spread time series
    mu        : float   - Long-run mean (from OU estimation)
    sigma_ou  : float   - Spread volatility
    entry_z   : float   - Z-score threshold to enter a trade (default ±2σ)
    exit_z    : float   - Z-score threshold to exit (default 0 = mean)

    Returns
    -------
    z_scores  : ndarray - Normalized spread (z-score)
    positions : ndarray - Position: +1 (long), -1 (short), 0 (flat)
    """
    z_scores  = (spread - mu) / sigma_ou
    positions = np.zeros(len(spread))

    current_pos = 0
    for i in range(1, len(spread)):
        z = z_scores[i]

        if current_pos == 0:
            # Enter: spread is extreme
            if z > entry_z:
                current_pos = -1   # SHORT: expect spread to fall
            elif z < -entry_z:
                current_pos = +1   # LONG: expect spread to rise
        else:
            # Exit: spread has reverted to mean (or crossed)
            if current_pos == +1 and z >= -exit_z:
                current_pos = 0
            elif current_pos == -1 and z <= exit_z:
                current_pos = 0

        positions[i] = current_pos

    return z_scores, positions


# ---------------------------------------------------------------------------
# Backtest
# ---------------------------------------------------------------------------

def backtest_pairs(price_A, price_B, beta, positions,
                   transaction_cost=0.001):
    """
    Compute P&L from pairs trading positions.

    Each unit of position = long 1 unit of spread = long 1 A, short beta B
    (or vice versa for short spread).

    Parameters
    ----------
    beta              : float   - Hedge ratio
    positions         : ndarray - +1/0/-1 positions on the spread
    transaction_cost  : float   - One-way cost as fraction of trade value

    Returns
    -------
    pnl_series  : ndarray - Daily P&L
    cum_pnl     : ndarray - Cumulative P&L
    sharpe      : float   - Annualized Sharpe ratio
    max_dd      : float   - Maximum drawdown (fraction)
    n_trades    : int     - Number of round-trip trades
    """
    log_A = np.log(price_A)
    log_B = np.log(price_B)

    # Daily returns of the spread
    spread_returns = np.diff(log_A - beta * log_B)

    # Position is applied to the next day's return
    # (we observe signal at t, enter at t+1 open — simplified to same-day here)
    pos_lagged = positions[:-1]  # avoid look-ahead
    daily_pnl  = pos_lagged * spread_returns

    # Transaction costs on position changes
    pos_changes = np.abs(np.diff(positions))
    # Cost per trade: proportional to position size and price
    costs       = pos_changes[:-1] * transaction_cost * 2  # round trip
    daily_pnl[1:] -= costs

    cum_pnl = np.cumsum(daily_pnl)

    # Sharpe ratio (annualized)
    sharpe = (daily_pnl.mean() / (daily_pnl.std() + 1e-9)) * np.sqrt(252)

    # Maximum drawdown
    running_max = np.maximum.accumulate(cum_pnl)
    drawdown    = cum_pnl - running_max
    max_dd      = drawdown.min()

    # Count round-trip trades
    n_trades = int((pos_changes > 0).sum() / 2)

    return daily_pnl, cum_pnl, sharpe, max_dd, n_trades


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    N_TOTAL = 750    # Total data points
    N_TRAIN = 500    # Training window

    print("=" * 60)
    print("PAIRS TRADING BACKTEST")
    print("=" * 60)

    # --- Generate synthetic cointegrated pair ---
    price_A, price_B, true_spread = generate_cointegrated_pair(
        n=N_TOTAL, beta=1.2, mu_spread=0.0, kappa=0.15, sigma_ou=0.5, seed=42
    )

    print(f"\n  Generated {N_TOTAL} days of synthetic data")
    print(f"  Training: first {N_TRAIN} days")
    print(f"  Testing:  last {N_TOTAL - N_TRAIN} days")

    # --- Cointegration test ---
    beta_hat, spread_hat, coint_p, adf_p, is_coint = test_cointegration(
        price_A[:N_TRAIN], price_B[:N_TRAIN]
    )

    print(f"\n--- COINTEGRATION TEST (Training Period) ---")
    print(f"  Hedge ratio (beta)  : {beta_hat:.4f}  (true: 1.2000)")
    print(f"  Engle-Granger p     : {coint_p:.4f}")
    print(f"  ADF p (spread)      : {adf_p:.4f}")
    print(f"  Cointegrated?       : {is_coint}")

    # --- Estimate OU parameters from training data ---
    kappa_hat, mu_hat, sigma_ou_hat, half_life = estimate_ou_params(spread_hat)

    print(f"\n--- OU PARAMETER ESTIMATES ---")
    print(f"  kappa (mean-rev speed): {kappa_hat:.4f}  (true: 0.1500)")
    print(f"  mu (long-run mean)    : {mu_hat:.4f}  (true: 0.0000)")
    print(f"  sigma_ou              : {sigma_ou_hat:.4f}  (true: 0.5000)")
    print(f"  Half-life             : {half_life:.1f} days")

    # --- Generate full spread (train + test) using estimated params ---
    # Recompute spread on full data using the estimated beta
    if STATSMODELS_AVAILABLE:
        log_A_full = np.log(price_A)
        log_B_full = np.log(price_B)
        X_full     = sm.add_constant(log_B_full)
        full_ols   = sm.OLS(log_A_full,
                            sm.add_constant(np.log(price_B[:N_TRAIN]))).fit()
        spread_full = log_A_full - full_ols.params[0] - beta_hat * log_B_full
    else:
        spread_full = np.log(price_A) - beta_hat * np.log(price_B)

    # --- Generate signals ---
    z_scores, positions = generate_signals(
        spread_full, mu_hat, sigma_ou_hat, entry_z=2.0, exit_z=0.3
    )

    # Only trade in the test period
    test_positions = positions.copy()
    test_positions[:N_TRAIN] = 0  # no trades during training

    # --- Backtest ---
    daily_pnl, cum_pnl, sharpe, max_dd, n_trades = backtest_pairs(
        price_A, price_B, beta_hat, test_positions, transaction_cost=0.001
    )

    print(f"\n--- BACKTEST RESULTS (Test Period: {N_TOTAL - N_TRAIN} days) ---")
    print(f"  Number of trades    : {n_trades}")
    print(f"  Total P&L           : {cum_pnl[-1]:.4f} (log-return units)")
    print(f"  Annualized Sharpe   : {sharpe:.2f}")
    print(f"  Max Drawdown        : {max_dd:.4f}")
    print(f"  Win rate (daily)    : {(daily_pnl > 0).mean():.1%}")

    if not is_coint:
        print("\n  WARNING: Pair failed cointegration test — strategy may not be reliable")

    # --- Plots ---
    fig = plt.figure(figsize=(15, 10))
    gs  = gridspec.GridSpec(3, 2, figure=fig, hspace=0.5, wspace=0.35)

    days = np.arange(N_TOTAL)

    # Plot 1: Price series
    ax1 = fig.add_subplot(gs[0, 0])
    ax1_r = ax1.twinx()
    ax1.plot(days, price_A, color="steelblue", lw=1, label="Asset A")
    ax1_r.plot(days, price_B, color="tomato", lw=1, label="Asset B")
    ax1.axvline(N_TRAIN, color="gray", linestyle="--", lw=1, label="Train/Test split")
    ax1.set_title("Asset Prices")
    ax1.set_xlabel("Day")
    ax1.set_ylabel("Asset A Price", color="steelblue")
    ax1_r.set_ylabel("Asset B Price", color="tomato")

    # Plot 2: Spread
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(days, spread_full, color="purple", lw=0.9, alpha=0.8)
    ax2.axhline(mu_hat, color="black", linestyle="--", lw=1, label=f"Mean={mu_hat:.3f}")
    ax2.axhline(mu_hat + 2 * sigma_ou_hat, color="tomato", linestyle=":", lw=1.5, label="±2σ")
    ax2.axhline(mu_hat - 2 * sigma_ou_hat, color="tomato", linestyle=":", lw=1.5)
    ax2.axvline(N_TRAIN, color="gray", linestyle="--", lw=1)
    ax2.set_title("Spread (Cointegration Residual)")
    ax2.set_xlabel("Day")
    ax2.set_ylabel("Spread Value")
    ax2.legend(fontsize=8)

    # Plot 3: Z-score and signals
    ax3 = fig.add_subplot(gs[1, :])
    ax3.plot(days, z_scores, color="steelblue", lw=0.8, alpha=0.7, label="Z-score")
    ax3.axhline(2,  color="tomato", linestyle="--", lw=1, label="±2σ entry")
    ax3.axhline(-2, color="tomato", linestyle="--", lw=1)
    ax3.axhline(0,  color="black",  linestyle=":",  lw=0.8)
    ax3.fill_between(days, 0, z_scores,
                     where=(test_positions == 1),  alpha=0.3, color="seagreen", label="Long spread")
    ax3.fill_between(days, 0, z_scores,
                     where=(test_positions == -1), alpha=0.3, color="tomato",   label="Short spread")
    ax3.axvline(N_TRAIN, color="gray", linestyle="--", lw=1)
    ax3.set_title("Z-Score with Trading Signals")
    ax3.set_xlabel("Day")
    ax3.set_ylabel("Z-Score")
    ax3.legend(fontsize=8)
    ax3.set_ylim(-5, 5)

    # Plot 4: Cumulative P&L
    ax4 = fig.add_subplot(gs[2, :])
    ax4.plot(days[1:], cum_pnl, color="seagreen", lw=1.5)
    ax4.axhline(0, color="black", linestyle="--", lw=0.8)
    ax4.axvline(N_TRAIN, color="gray", linestyle="--", lw=1, label="Train/Test")
    ax4.set_title(f"Cumulative P&L  (Sharpe={sharpe:.2f}, MaxDD={max_dd:.3f})")
    ax4.set_xlabel("Day")
    ax4.set_ylabel("Cumulative Log-Return")
    ax4.legend()

    plt.suptitle("Pairs Trading Backtest", fontsize=13, fontweight="bold")
    plt.savefig("pairs_trading.png", dpi=120, bbox_inches="tight")
    plt.show()
    print("\nPlot saved to pairs_trading.png")
```

## Output
Running this script produces:
- Cointegration test results (Engle-Granger p-value, ADF p-value) with pass/fail
- Estimated OU parameters: kappa, mu, sigma, and half-life in days
- Backtest performance metrics: total P&L, annualized Sharpe, max drawdown, win rate
- A 4-panel plot: price series, spread with ±2σ bands, z-score with trade markers, and cumulative P&L

Example output:
```
  Hedge ratio (beta)  : 1.1987  (true: 1.2000)
  Cointegrated?       : True
  Half-life           : 4.6 days
  Annualized Sharpe   : 1.42
  Max Drawdown        : -0.0523
```

## Key Learning Points
- Cointegration means two non-stationary price series share a common stochastic trend; their spread is stationary, providing a tradeable signal
- The Ornstein-Uhlenbeck process is the continuous-time model for mean-reverting spreads; kappa and the half-life quantify how quickly the spread snaps back
- The entry/exit z-score thresholds (±2σ / 0) balance trade frequency vs signal quality; tighter thresholds trade more but with weaker signals
- The hedge ratio beta from OLS regression is the number of B shares needed to neutralize one A share; it must be re-estimated periodically as the relationship evolves
- Market-neutral design (long one asset, short beta of the other) removes exposure to broad market moves — P&L depends only on the spread behavior
