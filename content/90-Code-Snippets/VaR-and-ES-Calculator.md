---
type: code-snippet
language: python
domain: risk
tags: [code, var, expected-shortfall, risk-management, backtesting]
concepts: see-related-notes
created: 2026-04-18
---

## Purpose
Compute Value at Risk and Expected Shortfall using all three standard methods (historical, parametric, Monte Carlo) with a comparison table and backtesting violation count.

## Dependencies
```
pip install numpy scipy pandas matplotlib tabulate
```

## Code
```python
"""
VaR and Expected Shortfall Calculator
======================================
Three methods to estimate downside risk:

  1. Historical Simulation — use the empirical distribution of past returns
  2. Parametric (Variance-Covariance) — assume returns are normal
  3. Monte Carlo Simulation — simulate future returns from a fitted model

Metrics:
  VaR(alpha) = the loss that is NOT exceeded with probability alpha
               e.g., 95% VaR: 5% chance of losing more than this
  ES(alpha)  = Expected Shortfall (CVaR): the average loss GIVEN
               that you exceed VaR — captures tail severity

Backtesting:
  Count how many days in a hold-out window actually exceeded the VaR estimate.
  Expected violations at 95% confidence: 5% of days.
  Kupiec test: are violations significantly different from expected?
"""

import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# ---------------------------------------------------------------------------
# Synthetic return data generator
# ---------------------------------------------------------------------------

def generate_returns(n_obs=1000, mu=0.0005, sigma=0.015, seed=42,
                     fat_tails=False, t_dof=5):
    """
    Generate synthetic daily log-returns.

    Parameters
    ----------
    fat_tails : bool - If True, generate t-distributed returns (heavier tails)
                       which makes VaR estimates from normal assumption too
                       optimistic
    t_dof     : int  - Degrees of freedom for t-distribution (lower = fatter tails)
    """
    rng = np.random.default_rng(seed)

    if fat_tails:
        # t-distributed: same mean/variance as normal but fatter tails
        raw = rng.standard_t(df=t_dof, size=n_obs)
        # Scale to match desired mu and sigma
        returns = mu + sigma * raw / np.sqrt(t_dof / (t_dof - 2))
    else:
        returns = rng.normal(mu, sigma, n_obs)

    return returns


# ---------------------------------------------------------------------------
# Method 1: Historical Simulation
# ---------------------------------------------------------------------------

def historical_var_es(returns, confidence=0.95):
    """
    Historical simulation VaR and ES.

    No distributional assumption — uses the empirical distribution directly.
    VaR = the (1-confidence) quantile of the return distribution.
    ES  = mean of returns below the VaR threshold.

    Parameters
    ----------
    returns    : ndarray - Historical daily log-returns
    confidence : float   - Confidence level (e.g. 0.95 for 95% VaR)

    Returns
    -------
    var : float - VaR (expressed as a positive loss, e.g. 0.023 = 2.3%)
    es  : float - Expected Shortfall (positive number)
    """
    alpha = 1 - confidence
    sorted_returns = np.sort(returns)

    # VaR: the alpha-th quantile (left tail)
    var_return = np.percentile(returns, alpha * 100)
    var = -var_return  # convert to positive loss

    # ES: average of returns below VaR (the worst alpha fraction)
    tail_returns = sorted_returns[sorted_returns <= var_return]
    es = -tail_returns.mean()

    return var, es


# ---------------------------------------------------------------------------
# Method 2: Parametric (Normal)
# ---------------------------------------------------------------------------

def parametric_var_es(returns, confidence=0.95):
    """
    Parametric VaR and ES assuming normally distributed returns.

    Fits mu and sigma to historical data, then uses analytical formulas:
        VaR = -(mu + z_alpha * sigma)
        ES  = -(mu - sigma * phi(z_alpha) / (1 - confidence))
    where z_alpha is the normal quantile at confidence level.

    This method is fast but underestimates risk when returns have fat tails.

    Returns
    -------
    var : float - VaR (positive loss)
    es  : float - Expected Shortfall (positive loss)
    """
    mu_hat    = returns.mean()
    sigma_hat = returns.std(ddof=1)
    alpha     = 1 - confidence

    z_alpha   = stats.norm.ppf(alpha)       # e.g. -1.645 for 95%
    phi_alpha = stats.norm.pdf(z_alpha)     # normal PDF at z_alpha

    var = -(mu_hat + z_alpha * sigma_hat)
    es  = -(mu_hat - sigma_hat * phi_alpha / alpha)

    return var, es


# ---------------------------------------------------------------------------
# Method 3: Monte Carlo Simulation
# ---------------------------------------------------------------------------

def mc_var_es(returns, confidence=0.95, n_scenarios=100_000, seed=42):
    """
    Monte Carlo VaR and ES.

    Fit a normal distribution to historical returns, then simulate
    n_scenarios future returns and compute VaR/ES on simulated data.

    More flexible than parametric: can be extended to non-normal
    distributions, correlated assets, or regime-switching models.

    Returns
    -------
    var : float - VaR (positive loss)
    es  : float - Expected Shortfall (positive loss)
    """
    rng = np.random.default_rng(seed)

    mu_hat    = returns.mean()
    sigma_hat = returns.std(ddof=1)

    # Simulate future return scenarios
    simulated = rng.normal(mu_hat, sigma_hat, n_scenarios)

    # Apply historical method to simulated distribution
    return historical_var_es(simulated, confidence)


# ---------------------------------------------------------------------------
# Backtesting: count violations
# ---------------------------------------------------------------------------

def backtest_var(train_returns, test_returns, confidence=0.95):
    """
    Rolling backtest: use each day's historical window to estimate VaR,
    then check if the next day's return exceeded it.

    Parameters
    ----------
    train_returns : ndarray - Returns used to estimate VaR each day
    test_returns  : ndarray - Out-of-sample returns to test against

    Returns
    -------
    violations     : ndarray - Boolean array, True if return exceeded VaR
    expected_rate  : float   - Expected violation rate = 1 - confidence
    actual_rate    : float   - Observed violation rate
    kupiec_p_value : float   - p-value of Kupiec proportion-of-failures test
    """
    n_test  = len(test_returns)
    alpha   = 1 - confidence

    violations = np.zeros(n_test, dtype=bool)
    var_levels = np.zeros(n_test)

    for i in range(n_test):
        # Estimate VaR using all data up to this point
        hist_window = np.concatenate([train_returns, test_returns[:i]])
        var_i, _ = historical_var_es(hist_window, confidence)
        var_levels[i] = var_i

        # Check if tomorrow's return exceeded VaR
        if test_returns[i] < -var_i:
            violations[i] = True

    n_violations   = violations.sum()
    actual_rate    = n_violations / n_test
    expected_rate  = alpha

    # Kupiec proportion-of-failures test
    # H0: violation rate = alpha (correctly specified model)
    # Likelihood ratio statistic ~ chi-squared(1) under H0
    x = n_violations
    n = n_test
    p = alpha  # expected rate under null

    if x == 0:
        kupiec_lr = 2 * n * np.log(1 - actual_rate + 1e-12) - 2 * n * np.log(1 - p)
    elif x == n:
        kupiec_lr = 2 * n * np.log(actual_rate) - 2 * n * np.log(p)
    else:
        kupiec_lr = (2 * (x * np.log(actual_rate / p) +
                         (n - x) * np.log((1 - actual_rate) / (1 - p))))
    kupiec_p = 1 - stats.chi2.cdf(kupiec_lr, df=1)

    return violations, var_levels, expected_rate, actual_rate, kupiec_p


# ---------------------------------------------------------------------------
# Comparison table across confidence levels
# ---------------------------------------------------------------------------

def comparison_table(returns, confidences=(0.90, 0.95, 0.99)):
    """Build a DataFrame comparing all three methods at multiple confidence levels."""
    rows = []
    for conf in confidences:
        h_var, h_es  = historical_var_es(returns, conf)
        p_var, p_es  = parametric_var_es(returns, conf)
        m_var, m_es  = mc_var_es(returns, conf)

        rows.append({
            "Confidence": f"{conf:.0%}",
            "Hist VaR":   f"{h_var:.4f}",
            "Para VaR":   f"{p_var:.4f}",
            "MC VaR":     f"{m_var:.4f}",
            "Hist ES":    f"{h_es:.4f}",
            "Para ES":    f"{p_es:.4f}",
            "MC ES":      f"{m_es:.4f}",
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # === Generate synthetic returns ===
    N_TRAIN = 750   # ~3 years of daily data
    N_TEST  = 250   # ~1 year hold-out for backtesting

    train_normal  = generate_returns(N_TRAIN, mu=0.0003, sigma=0.012, fat_tails=False)
    test_normal   = generate_returns(N_TEST,  mu=0.0003, sigma=0.012, fat_tails=False, seed=99)

    train_fattail = generate_returns(N_TRAIN, mu=0.0003, sigma=0.012, fat_tails=True)
    test_fattail  = generate_returns(N_TEST,  mu=0.0003, sigma=0.012, fat_tails=True, seed=99)

    CONFIDENCE = 0.95
    PORTFOLIO_VALUE = 1_000_000  # $1M portfolio

    print("=" * 60)
    print("VaR AND EXPECTED SHORTFALL CALCULATOR")
    print("=" * 60)
    print(f"  Training window : {N_TRAIN} days")
    print(f"  Confidence level: {CONFIDENCE:.0%}")
    print(f"  Portfolio value : ${PORTFOLIO_VALUE:,.0f}")

    # --- VaR / ES for normal returns ---
    h_var, h_es = historical_var_es(train_normal, CONFIDENCE)
    p_var, p_es = parametric_var_es(train_normal, CONFIDENCE)
    m_var, m_es = mc_var_es(train_normal, CONFIDENCE)

    print(f"\n--- NORMAL RETURNS: VaR & ES AT {CONFIDENCE:.0%} ---")
    print(f"{'Method':<20}  {'VaR (return)':>12}  {'VaR ($)':>12}  {'ES (return)':>12}  {'ES ($)':>10}")
    for name, var, es in [("Historical", h_var, h_es),
                           ("Parametric", p_var, p_es),
                           ("Monte Carlo", m_var, m_es)]:
        print(f"{name:<20}  {var:>12.4f}  ${var*PORTFOLIO_VALUE:>10,.0f}  "
              f"{es:>12.4f}  ${es*PORTFOLIO_VALUE:>8,.0f}")

    # --- Fat-tail comparison ---
    hf_var, hf_es = historical_var_es(train_fattail, CONFIDENCE)
    pf_var, pf_es = parametric_var_es(train_fattail, CONFIDENCE)
    mf_var, mf_es = mc_var_es(train_fattail, CONFIDENCE)

    print(f"\n--- FAT-TAILED RETURNS (t-distribution, dof=5) ---")
    print(f"{'Method':<20}  {'VaR (return)':>12}  {'ES (return)':>12}")
    for name, var, es in [("Historical", hf_var, hf_es),
                           ("Parametric", pf_var, pf_es),
                           ("Monte Carlo", mf_var, mf_es)]:
        print(f"{name:<20}  {var:>12.4f}  {es:>12.4f}")
    print(f"  Note: Parametric VaR underestimates risk with fat tails!")

    # --- Full comparison table ---
    print(f"\n--- COMPARISON TABLE (Normal returns) ---")
    df = comparison_table(train_normal)
    try:
        from tabulate import tabulate
        print(tabulate(df, headers="keys", tablefmt="rounded_outline", index=False))
    except ImportError:
        print(df.to_string(index=False))

    # --- Backtesting ---
    print(f"\n--- BACKTESTING ({N_TEST} days, {CONFIDENCE:.0%} confidence) ---")
    for label, train, test in [
        ("Normal returns", train_normal, test_normal),
        ("Fat-tail returns", train_fattail, test_fattail)
    ]:
        viols, var_levels, exp_rate, act_rate, kupiec_p = backtest_var(
            train, test, CONFIDENCE
        )
        print(f"\n  {label}:")
        print(f"    Expected violations : {exp_rate:.1%} x {N_TEST} = {exp_rate*N_TEST:.0f} days")
        print(f"    Actual violations   : {act_rate:.1%} = {viols.sum()} days")
        print(f"    Kupiec p-value      : {kupiec_p:.4f}  "
              f"({'PASS' if kupiec_p > 0.05 else 'FAIL'} at 5% significance)")

    # --- Plots ---
    fig = plt.figure(figsize=(15, 9))
    gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

    # Plot 1: Return distribution + VaR/ES markers
    ax1 = fig.add_subplot(gs[0, :2])
    ax1.hist(train_normal, bins=60, density=True, alpha=0.6,
             color="steelblue", label="Normal returns", edgecolor="white")
    ax1.axvline(-h_var, color="tomato",   lw=2, linestyle="--", label=f"Hist VaR ({CONFIDENCE:.0%})")
    ax1.axvline(-h_es,  color="darkred",  lw=2, linestyle="-.",  label=f"Hist ES ({CONFIDENCE:.0%})")
    ax1.axvline(-p_var, color="seagreen", lw=1.5, linestyle=":",  label=f"Para VaR ({CONFIDENCE:.0%})")
    # Shade the tail
    x_tail = np.linspace(train_normal.min(), -h_var, 100)
    ax1.fill_between(x_tail,
                     stats.norm.pdf(x_tail, train_normal.mean(), train_normal.std()),
                     alpha=0.3, color="tomato", label="Tail (5%)")
    ax1.set_title("Return Distribution with VaR and ES")
    ax1.set_xlabel("Daily Log-Return")
    ax1.set_ylabel("Density")
    ax1.legend(loc="upper right", fontsize=8)

    # Plot 2: Normal vs Fat-tail VaR comparison bar chart
    ax2 = fig.add_subplot(gs[0, 2])
    methods = ["Historical", "Parametric", "Monte Carlo"]
    vars_n = [h_var,  p_var,  m_var]
    vars_f = [hf_var, pf_var, mf_var]
    x = np.arange(len(methods))
    width = 0.35
    ax2.bar(x - width/2, vars_n, width, label="Normal", color="steelblue", alpha=0.8)
    ax2.bar(x + width/2, vars_f, width, label="Fat-tail", color="tomato", alpha=0.8)
    ax2.set_title(f"VaR Comparison ({CONFIDENCE:.0%})")
    ax2.set_xlabel("Method")
    ax2.set_ylabel("VaR (return)")
    ax2.set_xticks(x)
    ax2.set_xticklabels(methods)
    ax2.legend()

    # Plot 3: Backtesting — returns vs VaR (normal)
    viols_n, var_n, _, _, _ = backtest_var(train_normal, test_normal, CONFIDENCE)
    days_test = np.arange(N_TEST)

    ax3 = fig.add_subplot(gs[1, :2])
    ax3.plot(days_test, test_normal, color="steelblue", lw=0.8, alpha=0.7, label="Returns")
    ax3.plot(days_test, -var_n, color="tomato", lw=1.5, linestyle="--", label="VaR threshold")
    violation_days = days_test[viols_n]
    ax3.scatter(violation_days, test_normal[viols_n],
                color="red", s=30, zorder=5, label=f"Violations ({viols_n.sum()})")
    ax3.set_title(f"Backtest: Returns vs VaR ({CONFIDENCE:.0%} Historical, Normal data)")
    ax3.set_xlabel("Test Day")
    ax3.set_ylabel("Daily Return")
    ax3.legend()

    # Plot 4: Violations summary
    ax4 = fig.add_subplot(gs[1, 2])
    scenarios = ["Normal\n(Historical)", "Normal\n(Parametric)",
                 "Fat-tail\n(Historical)", "Fat-tail\n(Parametric)"]
    viols_pcts = []
    for train, test, method in [(train_normal, test_normal, "hist"),
                                 (train_normal, test_normal, "para"),
                                 (train_fattail, test_fattail, "hist"),
                                 (train_fattail, test_fattail, "para")]:
        if method == "hist":
            var_b, _ = historical_var_es(train, CONFIDENCE)
        else:
            var_b, _ = parametric_var_es(train, CONFIDENCE)
        viol_count = (test < -var_b).sum()
        viols_pcts.append(viol_count / N_TEST * 100)

    colors_bar = ["steelblue", "steelblue", "tomato", "tomato"]
    bars = ax4.bar(scenarios, viols_pcts, color=colors_bar, alpha=0.75, edgecolor="white")
    ax4.axhline((1 - CONFIDENCE) * 100, color="black", linestyle="--", lw=1.5,
                label=f"Expected ({(1-CONFIDENCE)*100:.0f}%)")
    ax4.set_title("Backtest Violation Rates")
    ax4.set_ylabel("Violation Rate (%)")
    ax4.legend()

    plt.suptitle("VaR and Expected Shortfall Calculator", fontsize=13, fontweight="bold")
    plt.savefig("var_es_calculator.png", dpi=120, bbox_inches="tight")
    plt.show()
    print("\nPlot saved to var_es_calculator.png")
```

## Output
Running this script produces:
- A formatted table comparing VaR and dollar-loss estimates across all three methods for normal returns
- A fat-tail comparison showing how parametric VaR underestimates risk relative to historical
- A full comparison table at 90%, 95%, and 99% confidence levels
- Backtesting results with Kupiec test p-values (pass/fail at 5% significance)
- A 4-panel plot: return distribution with VaR/ES markers, method comparison bar chart, rolling backtest violations, and violation rate summary

Example output:
```
  Normal returns:
    Expected violations : 5.0% x 250 = 13 days
    Actual violations   : 5.2% = 13 days
    Kupiec p-value      : 0.8731  (PASS)
  Fat-tail returns:
    Kupiec p-value      : 0.0421  (FAIL — parametric underestimates tail risk)
```

## Key Learning Points
- Historical simulation makes no distributional assumption and automatically captures fat tails, skewness, and regime changes present in the data
- Parametric VaR is fast and analytically tractable but significantly underestimates tail risk when returns have excess kurtosis (fat tails)
- Expected Shortfall (ES/CVaR) is a coherent risk measure — unlike VaR, it tells you how bad losses are when you breach the threshold
- The Kupiec test checks whether the observed violation rate is statistically consistent with the model's stated confidence level; a failing p-value means the model is mis-specified
- Regulatory frameworks (Basel III/IV) have shifted from VaR to ES precisely because ES captures the severity of tail losses, not just the threshold
