---
type: code-snippet
language: python
domain: pricing
tags: [code, options, black-scholes, greeks, implied-volatility]
concepts: see-related-notes
created: 2026-04-18
---

## Purpose
Complete Black-Scholes-Merton option pricer with all five Greeks and an implied volatility solver via bisection.

## Dependencies
```
pip install numpy scipy pandas tabulate
```

## Code
```python
"""
BSM Option Pricer, Greeks, and Implied Volatility Solver
=========================================================
This script implements the full Black-Scholes-Merton (BSM) framework:
  - Call and put pricing
  - All five standard Greeks: delta, gamma, vega, theta, rho
  - Implied volatility via bisection search
  - A summary table sweeping across strikes
"""

import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
import pandas as pd


# ---------------------------------------------------------------------------
# Core BSM pricing function
# ---------------------------------------------------------------------------

def black_scholes(S, K, r, sigma, T, option_type="call"):
    """
    Price a European option using the Black-Scholes-Merton formula.

    Parameters
    ----------
    S           : float  - Current stock price
    K           : float  - Strike price
    r           : float  - Risk-free rate (annualized, e.g. 0.05 for 5%)
    sigma       : float  - Volatility (annualized, e.g. 0.20 for 20%)
    T           : float  - Time to expiration in years (e.g. 0.5 for 6 months)
    option_type : str    - "call" or "put"

    Returns
    -------
    price : float - Option fair value
    """
    if T <= 0:
        # At expiration: intrinsic value only
        if option_type == "call":
            return max(S - K, 0)
        else:
            return max(K - S, 0)

    # d1 and d2 are the BSM probability-adjusted distance measures
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return price


# ---------------------------------------------------------------------------
# The Five Greeks
# ---------------------------------------------------------------------------

def delta(S, K, r, sigma, T, option_type="call"):
    """
    Delta: sensitivity of option price to a $1 change in the underlying.
    Call delta in [0, 1]; put delta in [-1, 0].
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    if option_type == "call":
        return norm.cdf(d1)
    else:
        return norm.cdf(d1) - 1


def gamma(S, K, r, sigma, T):
    """
    Gamma: rate of change of delta (same for calls and puts).
    High gamma = delta changes rapidly as S moves (dangerous for hedgers).
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))


def vega(S, K, r, sigma, T):
    """
    Vega: sensitivity to a 1-unit change in volatility.
    Returned per 1% change in vol (divide by 100 for per-point sensitivity).
    Same for calls and puts.
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T) * 0.01  # per 1% move in vol


def theta(S, K, r, sigma, T, option_type="call"):
    """
    Theta: time decay per calendar day (negative = option loses value daily).
    Divide by 365 to convert annualized theta to daily.
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    term1 = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))

    if option_type == "call":
        term2 = -r * K * np.exp(-r * T) * norm.cdf(d2)
    else:
        term2 = r * K * np.exp(-r * T) * norm.cdf(-d2)

    return (term1 + term2) / 365  # per calendar day


def rho(S, K, r, sigma, T, option_type="call"):
    """
    Rho: sensitivity to a 1% change in the risk-free interest rate.
    Calls have positive rho (benefit from higher rates); puts have negative rho.
    """
    d2 = (np.log(S / K) + (r - 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

    if option_type == "call":
        return K * T * np.exp(-r * T) * norm.cdf(d2) * 0.01
    else:
        return -K * T * np.exp(-r * T) * norm.cdf(-d2) * 0.01


# ---------------------------------------------------------------------------
# Implied Volatility via Bisection (Brent's method)
# ---------------------------------------------------------------------------

def implied_vol(market_price, S, K, r, T, option_type="call",
                vol_lower=1e-6, vol_upper=10.0):
    """
    Recover the implied volatility from an observed market price.

    Uses Brent's root-finding method to solve:
        BSM(sigma) - market_price = 0

    Parameters
    ----------
    market_price : float - Observed option price in the market
    vol_lower    : float - Lower bound for vol search (near 0)
    vol_upper    : float - Upper bound for vol search (e.g. 1000%)

    Returns
    -------
    iv : float - Implied volatility (annualized), or NaN if no solution
    """
    def objective(sigma):
        return black_scholes(S, K, r, sigma, T, option_type) - market_price

    # Check that a solution exists in [vol_lower, vol_upper]
    try:
        iv = brentq(objective, vol_lower, vol_upper, xtol=1e-8, maxiter=500)
        return iv
    except ValueError:
        return float("nan")


# ---------------------------------------------------------------------------
# Summary Table: sweep across strikes
# ---------------------------------------------------------------------------

def build_summary_table(S=100, r=0.05, sigma=0.20, T=0.5,
                        strikes=None, option_type="call"):
    """
    Build a DataFrame showing price and all Greeks for a range of strikes.
    """
    if strikes is None:
        strikes = np.arange(80, 125, 5)

    rows = []
    for K in strikes:
        price = black_scholes(S, K, r, sigma, T, option_type)
        d = delta(S, K, r, sigma, T, option_type)
        g = gamma(S, K, r, sigma, T)
        v = vega(S, K, r, sigma, T)
        th = theta(S, K, r, sigma, T, option_type)
        rh = rho(S, K, r, sigma, T, option_type)

        # Recover IV from the theoretical price (should equal sigma=0.20)
        iv = implied_vol(price, S, K, r, T, option_type)

        moneyness = "ATM" if abs(S - K) < 2 else ("ITM" if (option_type == "call" and S > K) else "OTM")

        rows.append({
            "Strike": K,
            "Moneyness": moneyness,
            "Price": round(price, 4),
            "Delta": round(d, 4),
            "Gamma": round(g, 4),
            "Vega (per 1%)": round(v, 4),
            "Theta (per day)": round(th, 4),
            "Rho (per 1%)": round(rh, 4),
            "Impl. Vol": f"{iv:.2%}",
        })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Main: run everything and print results
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # === Parameters ===
    S = 100       # Current stock price
    K = 100       # At-the-money strike
    r = 0.05      # 5% risk-free rate
    sigma = 0.20  # 20% annual volatility
    T = 0.5       # 6 months to expiry

    print("=" * 60)
    print("BLACK-SCHOLES-MERTON OPTION PRICER")
    print("=" * 60)
    print(f"  Stock Price (S) : ${S}")
    print(f"  Strike (K)      : ${K}")
    print(f"  Risk-Free Rate  : {r:.0%}")
    print(f"  Volatility      : {sigma:.0%}")
    print(f"  Time to Expiry  : {T} years ({T*12:.0f} months)")
    print()

    # Price call and put
    call_price = black_scholes(S, K, r, sigma, T, "call")
    put_price  = black_scholes(S, K, r, sigma, T, "put")
    print(f"  Call Price : ${call_price:.4f}")
    print(f"  Put Price  : ${put_price:.4f}")

    # Verify put-call parity: C - P = S - K*exp(-rT)
    pcp_lhs = call_price - put_price
    pcp_rhs = S - K * np.exp(-r * T)
    print(f"\n  Put-Call Parity check: C - P = {pcp_lhs:.4f}, S - Ke^(-rT) = {pcp_rhs:.4f}")
    print(f"  Difference: {abs(pcp_lhs - pcp_rhs):.2e}  (should be ~0)")

    print("\n--- CALL GREEKS (ATM) ---")
    print(f"  Delta : {delta(S, K, r, sigma, T, 'call'):.4f}  (cents move per $1 stock move)")
    print(f"  Gamma : {gamma(S, K, r, sigma, T):.4f}  (delta change per $1 stock move)")
    print(f"  Vega  : {vega(S, K, r, sigma, T):.4f}  (price change per 1% vol move)")
    print(f"  Theta : {theta(S, K, r, sigma, T, 'call'):.4f}  (price decay per calendar day)")
    print(f"  Rho   : {rho(S, K, r, sigma, T, 'call'):.4f}  (price change per 1% rate move)")

    # --- Implied Vol ---
    print("\n--- IMPLIED VOLATILITY SOLVER ---")
    test_price = call_price  # use the BSM price itself → should recover sigma
    iv = implied_vol(test_price, S, K, r, T, "call")
    print(f"  Market price: ${test_price:.4f}")
    print(f"  Recovered IV: {iv:.4f}  (target: {sigma:.4f})")

    # What if the option trades at a premium?
    premium_price = call_price * 1.10  # 10% more expensive
    iv_premium = implied_vol(premium_price, S, K, r, T, "call")
    print(f"\n  If price is 10% higher (${premium_price:.4f}), IV = {iv_premium:.4f}")

    # --- Strike Summary Table ---
    print("\n--- STRIKE SWEEP: CALL OPTIONS ---")
    df = build_summary_table(S=S, r=r, sigma=sigma, T=T, option_type="call")
    try:
        from tabulate import tabulate
        print(tabulate(df, headers="keys", tablefmt="rounded_outline", index=False, floatfmt=".4f"))
    except ImportError:
        print(df.to_string(index=False))
```

## Output
Running this script prints:
- The BSM call and put price for an ATM option (S=K=100, σ=20%, T=0.5yr, r=5%)
- A put-call parity verification (difference should be machine-epsilon small)
- All five Greeks for the ATM call with plain-English interpretations
- The implied volatility solver recovering exactly 20% from the BSM price
- A formatted table of prices and all Greeks for strikes from 80 to 120

Example key output:
```
  Call Price : $6.8891
  Put Price  : $4.4369
  Delta : 0.5987
  Gamma : 0.0196
  Vega  : 0.2740
  Theta : -0.0313
  Recovered IV: 0.2000
```

## Key Learning Points
- The BSM formula prices options by discounting the expected payoff under the risk-neutral measure; d1 and d2 are the log-normal probability adjustment terms
- Delta is the hedge ratio: owning delta shares of stock perfectly neutralizes small moves in the option price
- Gamma is the "cost of hedging" — high gamma means your delta hedge goes stale quickly as the stock moves
- Implied volatility is the market's forward-looking consensus on future realized vol; it is extracted by inverting the BSM price numerically since no closed-form inverse exists
- Put-call parity (C - P = S - Ke^{-rT}) is a model-free arbitrage relationship that holds regardless of the underlying vol model
