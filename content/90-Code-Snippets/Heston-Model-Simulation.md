---
type: code-snippet
language: python
domain: pricing
tags: [code, heston, stochastic-volatility, vol-smile, simulation]
concepts: see-related-notes
created: 2026-04-18
---

## Purpose
Simulate the Heston stochastic volatility model using Euler-Maruyama and visualize the implied volatility smile it produces versus flat BSM.

## Dependencies
```
pip install numpy scipy matplotlib
```

## Code
```python
"""
Heston Stochastic Volatility Model Simulation
==============================================
The Heston model extends BSM by letting volatility itself be stochastic:

    dS = mu * S * dt + sqrt(v) * S * dW_S
    dv = kappa * (theta - v) * dt + xi * sqrt(v) * dW_v
    Corr(dW_S, dW_v) = rho

Where:
    v       = instantaneous variance (vol^2)
    kappa   = mean-reversion speed of variance
    theta   = long-run average variance
    xi      = vol-of-vol (volatility of the variance process)
    rho     = correlation between stock and vol shocks
              (typically negative: stocks fall when vol rises)

The Feller condition 2*kappa*theta > xi^2 ensures variance stays positive.
"""

import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# BSM helper for IV extraction
# ---------------------------------------------------------------------------

def bsm_call(S, K, r, sigma, T):
    """Black-Scholes call price. Used to back out implied vol."""
    if sigma <= 0 or T <= 0:
        return max(S - K * np.exp(-r * T), 0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def implied_vol(price, S, K, r, T):
    """Extract implied vol from an option price via Brent's method."""
    intrinsic = max(S - K * np.exp(-r * T), 0)
    if price <= intrinsic + 1e-8:
        return float("nan")
    try:
        return brentq(lambda s: bsm_call(S, K, r, s, T) - price,
                      1e-6, 10.0, xtol=1e-8)
    except ValueError:
        return float("nan")


# ---------------------------------------------------------------------------
# Heston simulation via Euler-Maruyama
# ---------------------------------------------------------------------------

def simulate_heston(S0, v0, mu, kappa, theta, xi, rho, T,
                    n_steps, n_paths, seed=42):
    """
    Simulate Heston model paths using Euler-Maruyama with full truncation.

    Full truncation: max(v, 0) is used wherever variance appears under sqrt
    to prevent blow-ups when variance temporarily goes negative due to
    discretization error.

    Parameters
    ----------
    S0    : float - Initial stock price
    v0    : float - Initial variance (e.g. 0.04 = 20% vol squared)
    mu    : float - Real-world drift of stock
    kappa : float - Mean-reversion speed of variance
    theta : float - Long-run average variance
    xi    : float - Vol of vol (volatility of variance)
    rho   : float - Correlation between stock and variance Brownian motions
    T     : float - Time horizon in years
    n_steps: int  - Number of time steps
    n_paths: int  - Number of Monte Carlo paths
    seed  : int   - Random seed

    Returns
    -------
    S_paths : ndarray (n_steps+1, n_paths) - Stock price paths
    v_paths : ndarray (n_steps+1, n_paths) - Variance paths
    times   : ndarray (n_steps+1,)         - Time grid
    """
    rng = np.random.default_rng(seed)
    dt  = T / n_steps
    times = np.linspace(0, T, n_steps + 1)

    # Correlated Brownian motions via Cholesky decomposition
    # [dW_S, dW_v] = L @ [Z1, Z2] where L is the Cholesky factor of
    # [[1, rho], [rho, 1]]
    Z1 = rng.standard_normal((n_steps, n_paths))
    Z2 = rng.standard_normal((n_steps, n_paths))
    # Correlate: dW_v = rho*dW_S + sqrt(1-rho^2)*Z_indep
    dW_S = Z1
    dW_v = rho * Z1 + np.sqrt(1 - rho**2) * Z2

    S_paths = np.zeros((n_steps + 1, n_paths))
    v_paths = np.zeros((n_steps + 1, n_paths))

    S_paths[0] = S0
    v_paths[0] = v0

    for i in range(n_steps):
        v_plus = np.maximum(v_paths[i], 0)  # full truncation scheme
        sqrt_v = np.sqrt(v_plus)

        # Variance process (CIR / mean-reverting)
        v_paths[i + 1] = (v_paths[i]
                          + kappa * (theta - v_plus) * dt
                          + xi * sqrt_v * np.sqrt(dt) * dW_v[i])

        # Stock price process (log-Euler for numerical stability)
        S_paths[i + 1] = S_paths[i] * np.exp(
            (mu - 0.5 * v_plus) * dt + sqrt_v * np.sqrt(dt) * dW_S[i]
        )

    return S_paths, v_paths, times


# ---------------------------------------------------------------------------
# Heston Monte Carlo call price
# ---------------------------------------------------------------------------

def mc_heston_call(S0, K, r, v0, kappa, theta, xi, rho, T,
                   n_paths=50_000, n_steps=252, seed=42):
    """
    Price a European call via Heston MC simulation.

    Uses risk-neutral drift (mu = r) for pricing.

    Returns
    -------
    price  : float - Call price estimate
    stderr : float - Standard error
    """
    S_paths, _, _ = simulate_heston(
        S0, v0, mu=r, kappa=kappa, theta=theta,
        xi=xi, rho=rho, T=T, n_steps=n_steps, n_paths=n_paths, seed=seed
    )
    S_T = S_paths[-1]
    payoffs = np.maximum(S_T - K, 0)
    discounted = np.exp(-r * T) * payoffs
    return discounted.mean(), discounted.std() / np.sqrt(n_paths)


# ---------------------------------------------------------------------------
# Build vol smile: IV by strike
# ---------------------------------------------------------------------------

def build_vol_smile(S0, r, v0, kappa, theta, xi, rho, T,
                    strikes, n_paths=30_000, n_steps=252):
    """
    For each strike, compute the Heston MC call price and extract
    the implied BSM volatility. This is the 'vol smile'.
    """
    ivs_heston = []
    ivs_flat   = []  # flat BSM baseline (constant vol = sqrt(theta))

    flat_vol = np.sqrt(theta)  # use long-run vol as the BSM benchmark

    for K in strikes:
        # Heston price
        price, _ = mc_heston_call(S0, K, r, v0, kappa, theta, xi, rho, T,
                                  n_paths=n_paths, n_steps=n_steps,
                                  seed=int(K * 100))
        iv = implied_vol(price, S0, K, r, T)
        ivs_heston.append(iv)

        # BSM flat price (same vol for all strikes — no smile)
        bsm_price = bsm_call(S0, K, r, flat_vol, T)
        ivs_flat.append(flat_vol)  # flat by construction

    return ivs_heston, ivs_flat, flat_vol


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # === Heston Parameters ===
    S0    = 100    # Initial stock price
    v0    = 0.04   # Initial variance (20% vol: sqrt(0.04) = 0.20)
    r     = 0.05   # Risk-free rate
    kappa = 2.0    # Mean-reversion speed (higher = faster reversion to theta)
    theta = 0.04   # Long-run variance (same as v0 here, already at LR mean)
    xi    = 0.30   # Vol of vol (how much the vol itself wiggles)
    rho   = -0.70  # Negative: stocks fall when vol rises (leverage effect)
    T     = 0.5    # 6 months to expiry

    print("=" * 60)
    print("HESTON STOCHASTIC VOLATILITY MODEL")
    print("=" * 60)
    print(f"  S0={S0}, v0={v0} (vol={np.sqrt(v0):.0%}), kappa={kappa}")
    print(f"  theta={theta} (LR vol={np.sqrt(theta):.0%}), xi={xi}, rho={rho}")

    # --- Feller Condition ---
    feller_lhs = 2 * kappa * theta
    feller_rhs = xi**2
    feller_ok  = feller_lhs > feller_rhs
    print(f"\n  Feller condition: 2*kappa*theta = {feller_lhs:.4f} > xi^2 = {feller_rhs:.4f}")
    print(f"  Feller satisfied: {feller_ok}")
    if not feller_ok:
        print("  WARNING: Variance can touch zero — Euler scheme may have issues.")

    # --- Simulate paths ---
    print("\n  Simulating 5 sample paths...")
    S_paths, v_paths, times = simulate_heston(
        S0, v0, mu=0.08, kappa=kappa, theta=theta,
        xi=xi, rho=rho, T=T, n_steps=126, n_paths=5
    )
    print(f"  Terminal stock prices: {S_paths[-1].round(2)}")
    print(f"  Terminal volatilities: {np.sqrt(np.maximum(v_paths[-1], 0)).round(4)}")

    # --- ATM price comparison ---
    K_atm = S0
    heston_atm, heston_se = mc_heston_call(
        S0, K_atm, r, v0, kappa, theta, xi, rho, T,
        n_paths=50_000, n_steps=252
    )
    bsm_atm = bsm_call(S0, K_atm, r, np.sqrt(theta), T)

    print(f"\n--- ATM CALL PRICING (K={K_atm}) ---")
    print(f"  Heston MC     : ${heston_atm:.4f}  ± {heston_se:.4f}")
    print(f"  BSM (flat vol): ${bsm_atm:.4f}")

    # --- Vol smile ---
    print("\n  Computing vol smile across strikes (may take ~30 seconds)...")
    strikes = np.array([80, 85, 90, 95, 100, 105, 110, 115, 120])
    ivs_heston, ivs_flat, flat_vol = build_vol_smile(
        S0, r, v0, kappa, theta, xi, rho, T,
        strikes, n_paths=20_000, n_steps=126
    )

    print(f"\n--- VOL SMILE TABLE ---")
    print(f"{'Strike':>8}  {'Heston IV':>10}  {'Flat BSM IV':>12}")
    for K, iv_h, iv_f in zip(strikes, ivs_heston, ivs_flat):
        iv_h_str = f"{iv_h:.2%}" if not np.isnan(iv_h) else "  N/A "
        print(f"{K:>8}  {iv_h_str:>10}  {iv_f:.2%}")

    # --- Plots ---
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Plot 1: Stock price paths
    S_vis, v_vis, t_vis = simulate_heston(
        S0, v0, mu=0.08, kappa=kappa, theta=theta,
        xi=xi, rho=rho, T=T, n_steps=126, n_paths=8
    )
    for i in range(8):
        axes[0].plot(t_vis, S_vis[:, i], lw=0.9, alpha=0.85)
    axes[0].axhline(S0, color="k", linestyle="--", lw=1)
    axes[0].set_title("Heston Stock Price Paths")
    axes[0].set_xlabel("Time (years)")
    axes[0].set_ylabel("Stock Price ($)")

    # Plot 2: Variance (vol^2) paths
    for i in range(8):
        axes[1].plot(t_vis, np.sqrt(np.maximum(v_vis[:, i], 0)) * 100, lw=0.9, alpha=0.85)
    axes[1].axhline(np.sqrt(theta) * 100, color="k", linestyle="--", lw=1.5,
                    label=f"LR vol = {np.sqrt(theta):.0%}")
    axes[1].set_title("Instantaneous Volatility Paths")
    axes[1].set_xlabel("Time (years)")
    axes[1].set_ylabel("Volatility (%)")
    axes[1].legend()

    # Plot 3: Vol smile
    ivs_h_clean = [iv * 100 if not np.isnan(iv) else None for iv in ivs_heston]
    strikes_plot = [strikes[i] for i, iv in enumerate(ivs_h_clean) if iv is not None]
    ivs_h_plot   = [iv for iv in ivs_h_clean if iv is not None]
    ivs_f_plot   = [flat_vol * 100] * len(strikes_plot)

    axes[2].plot(strikes_plot, ivs_h_plot, "o-", color="steelblue",
                 label=f"Heston (rho={rho})", lw=2, ms=6)
    axes[2].plot(strikes, [flat_vol * 100] * len(strikes), "--",
                 color="tomato", label="BSM (flat vol)", lw=1.5)
    axes[2].axvline(S0, color="gray", linestyle=":", lw=1)
    axes[2].set_title("Implied Volatility Smile")
    axes[2].set_xlabel("Strike Price ($)")
    axes[2].set_ylabel("Implied Volatility (%)")
    axes[2].legend()

    plt.tight_layout()
    plt.savefig("heston_simulation.png", dpi=120, bbox_inches="tight")
    plt.show()
    print("\nPlot saved to heston_simulation.png")
```

## Output
Running this script produces:
- Feller condition check printed with pass/fail status
- Terminal stock prices and instantaneous volatilities for 5 sample paths
- ATM call price comparison: Heston MC vs flat BSM
- A vol smile table showing implied vol by strike (Heston produces a skew/smile; BSM is flat)
- A 3-panel plot: stock price paths, instantaneous vol paths, and the implied vol smile

Example vol smile output (with rho = -0.70):
```
 Strike   Heston IV  Flat BSM IV
     80      25.3%       20.0%
    100      20.1%       20.0%
    120      16.8%       20.0%
```
The negative rho creates a downward skew (higher IV for low strikes) — the famous "volatility skew."

## Key Learning Points
- Heston allows variance to be stochastic, driven by a mean-reverting CIR process; kappa controls how fast vol snaps back to its long-run level theta
- Negative rho (stock and vol negatively correlated) generates a downward vol skew, matching empirically observed equity markets ("leverage effect")
- The Feller condition 2κθ > ξ² guarantees the variance process stays strictly positive; if violated, numerical truncation is needed
- Full truncation (replacing negative variance with zero) is a practical fix for Euler discretization errors in the CIR variance process
- The vol smile is empirical evidence that BSM's constant-vol assumption is wrong; stochastic vol models like Heston reproduce the smile naturally
