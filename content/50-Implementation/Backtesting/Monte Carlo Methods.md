---
type: concept
domain: 50-Implementation
tags: [backtesting, statistics, simulation, risk]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-11
review_interval_days: 365
sources:
  - "Lopez de Prado - Advances in Financial ML ch.7-8"
  - "Efron & Hastie - Computer Age Statistical Inference (2016)"
created: 2026-04-11
---

> [!info] Problem Chain
> **Chain:** Pricing/Risk → Pricing Gap 6 Solution B: How do we price exotic options and simulate strategy distributions when closed-form solutions don't exist?
> **This concept:** Monte Carlo simulation is the universal numerical method for generating outcome distributions when analytical solutions are unavailable — covering path-dependent options pricing, strategy performance distributions, and risk measurement.
> **Alternative approaches to this gap:** PDE methods (finite differences), binomial trees, analytical approximations
> **You need first:** [[Geometric Brownian Motion]], [[Backtesting Methodology]]
> **This unlocks:** [[Backtesting Methodology]], [[Overfitting and Multiple Testing]]

## Why This Exists

**The gap:** Most real-world problems in quantitative finance — exotic option pricing, strategy performance distributions, portfolio risk with complex dependencies — don't have closed-form analytical solutions; practitioners needed a general numerical method.
**What came before:** Closed-form models (Black-Scholes for European options, analytical VaR for Gaussian portfolios) that work only under strict assumptions (no path dependence, normal distributions, constant parameters) which rarely hold in practice.
**What this adds:** A simulation framework that handles any stochastic model, any path-dependent payoff, any return distribution — at the cost of computational time; bootstrap resampling provides a non-parametric alternative that makes no distributional assumptions; variance reduction techniques (antithetic variates, control variates, quasi-Monte Carlo) improve efficiency dramatically.
**What it still doesn't solve:** Monte Carlo is computationally intensive (slow for high-dimensional problems); simulation accuracy scales as 1/√N (halving error requires 4× more paths); the quality of output depends entirely on the quality of the assumed stochastic model — garbage in, garbage out.

Imagine you want to know: "If I ran my trading strategy 1,000 times on different possible histories, how often would it succeed?" You can't go back and relive 1,000 different pasts — history happened once. But you can *simulate* many possible histories, each consistent with what we know about how markets behave. That's Monte Carlo.

The name comes from the famous Monte Carlo casino — using randomness as a tool rather than something to bet against. The core idea is disarmingly simple: if you can't solve a problem analytically, draw many random samples from it and observe the distribution of outcomes. The more samples you draw, the closer your estimate gets to the true answer.

In quantitative finance, Monte Carlo is used in at least four distinct settings:

1. **Strategy evaluation:** Rather than testing a strategy on one historical path, simulate many possible return paths and examine the full distribution of Sharpe ratios and drawdowns. This separates skill from luck.

2. **Risk measurement:** Value at Risk (VaR) and Expected Shortfall (ES) can be computed by simulating the distribution of portfolio losses. This handles non-normal returns and complex option-like exposures that closed-form formulas can't capture.

3. **Options pricing:** For exotic options (path-dependent payoffs, stochastic vol, multiple underlyings), Monte Carlo is often the only tractable pricing method.

4. **Permutation testing for overfitting:** Shuffle strategy returns to destroy any real alpha, then measure the distribution of "backtest-inflated" Sharpe ratios under the null. If your real strategy's Sharpe sits in the 95th percentile of this null distribution, that's meaningful evidence — the same logic as a classical hypothesis test but without parametric assumptions.

The two biggest practical advantages of Monte Carlo over analytic methods: (1) it handles any distribution or payoff structure, however complex; (2) it produces a full distribution rather than just a point estimate, so you see the range of possible outcomes, not just the expected one.

---

## Math Concepts

### Monte Carlo Estimator

For a quantity $\mu = E[f(X)]$ where $X$ is a random variable, the Monte Carlo estimator draws $N$ independent samples $X_1, \ldots, X_N$ and computes:

$$\hat{\mu}_N = \frac{1}{N} \sum_{i=1}^{N} f(X_i)$$

By the Law of Large Numbers, $\hat{\mu}_N \to \mu$ as $N \to \infty$.

**Standard error of the estimate:**

$$\text{SE}(\hat{\mu}_N) = \frac{\sigma_f}{\sqrt{N}}$$

where $\sigma_f = \text{std}(f(X))$. To halve the error, quadruple the sample size — the infamous $\sqrt{N}$ convergence rate.

### Geometric Brownian Motion (GBM) — Path Simulation

The standard model for stock price simulation under GBM:

$$dS_t = \mu S_t \, dt + \sigma S_t \, dW_t$$

Discretized for simulation over time steps $\Delta t$:

$$S_{t+\Delta t} = S_t \cdot \exp\!\left[\left(\mu - \frac{\sigma^2}{2}\right)\Delta t + \sigma \sqrt{\Delta t} \cdot Z_t\right]$$

where $Z_t \sim N(0,1)$ i.i.d.

The $\sigma^2/2$ term is the **Ito correction** — it ensures the expected value of $S_t$ grows as $e^{\mu t}$ (not $e^{(\mu + \sigma^2/2)t}$), consistent with the no-arbitrage requirement. Forgetting this term is a common coding mistake.

### Bootstrapping Return Paths

Instead of assuming GBM, resample from the empirical distribution of historical returns:

1. Draw $T$ returns with replacement from the historical return series $\{r_1, \ldots, r_H\}$
2. Compound them: $S_T = S_0 \prod_{t=1}^{T}(1 + r_t^*)$
3. Repeat $N$ times to get the distribution of terminal wealth

**Block bootstrap (for autocorrelated series):** Draw contiguous blocks of $b$ consecutive returns rather than individual returns, preserving short-term autocorrelation structure.

### Permutation Test for Strategy Validity

To test whether a strategy's Sharpe ratio is genuine or a backtest artifact:

1. Record the strategy's actual Sharpe $\hat{SR}_{obs}$ on the original return series.
2. Generate $B$ permutation samples: shuffle (randomly reorder) the return series, breaking any temporal structure, and compute $\hat{SR}_b$ for each.
3. Compute the empirical p-value:
   $$p = \frac{1 + \#\{b : \hat{SR}_b \geq \hat{SR}_{obs}\}}{B + 1}$$
4. If $p < 0.05$, the strategy's Sharpe is unlikely to arise from random ordering alone.

This is a non-parametric test — it makes no assumption about the distribution of returns.

### Value at Risk (VaR) via Monte Carlo

For a portfolio with value $V$ and return distribution $F$, VaR at confidence level $\alpha$ is:

$$\text{VaR}_\alpha = -\text{quantile}(F, 1 - \alpha)$$

Monte Carlo VaR:
1. Simulate $N$ portfolio return paths over the horizon
2. Sort the simulated P&L outcomes
3. $\text{VaR}_{95\%}$ = the loss at the 5th percentile

**Expected Shortfall (CVaR)** — average loss in the worst $(1-\alpha)$ scenarios:

$$\text{ES}_\alpha = -\frac{1}{N(1-\alpha)} \sum_{i: r_i \leq \text{VaR}_\alpha} r_i$$

ES is preferred over VaR because it is coherent (subadditive) and captures the severity of tail losses, not just the threshold.

### Variance Reduction Techniques

Plain Monte Carlo converges slowly ($O(1/\sqrt{N})$). Common variance reduction methods:

| Technique | Idea | Typical speedup |
|---|---|---|
| **Antithetic variates** | For each $Z$, also use $-Z$; the pair is negatively correlated and cancels variance | 2–4× |
| **Control variates** | Subtract a related quantity with known expectation; corrects the mean | 2–10× |
| **Quasi-Monte Carlo (QMC)** | Replace random $Z$'s with low-discrepancy sequences (Sobol, Halton); fills space more uniformly | 10–100× for smooth integrands |
| **Importance sampling** | Sample more heavily from the important (tail) region; reweight estimates | 10–100× for rare events |

---

## Walkthrough

### Simulating Strategy Drawdown Distribution

**Problem:** A momentum strategy has produced a Sharpe ratio of 1.4 over 3 years. What's the probability of a 20% drawdown in the next year?

**Step 1:** Estimate daily return parameters from the 3-year history: $\mu = 0.05\%$/day, $\sigma = 0.8\%$/day.

**Step 2:** Simulate 10,000 one-year (252-day) price paths via GBM.

**Step 3:** For each path, compute the maximum drawdown.

**Step 4:** The fraction of paths with MaxDD $> 20\%$ is the probability estimate.

From a typical simulation: $P(\text{MaxDD} > 20\%) \approx 12\%$ — a non-trivial tail risk even for a good strategy.

**Step 5:** Permutation test. Shuffle the actual 3-year daily returns 10,000 times. Compute Sharpe on each shuffled series. If the actual Sharpe of 1.4 is at the 98th percentile of the null distribution, we have $p \approx 0.02$ — meaningful evidence of genuine alpha.

---

## Analysis

**When Monte Carlo beats analytic formulas:**
- Path-dependent payoffs (Asian options, barrier options, lookback strategies)
- Fat-tailed or skewed return distributions that violate normality
- Multi-asset portfolios with complex correlation structure
- Regime-switching models where GBM is a poor approximation

**Key limitations:**
1. **Model risk:** Monte Carlo is only as good as the model used to simulate paths. GBM misses volatility clustering, jumps, and mean reversion. A garbage-in model gives garbage-in confidence intervals.
2. **Computational cost:** Complex simulations (thousands of paths × thousands of time steps × large portfolios) require significant compute. Variance reduction is essential in practice.
3. **Overfitting the simulation to history:** If simulation parameters are calibrated on in-sample data, permutation tests still suffer from selection bias. The simulation must be calibrated on one period and the test run on another.
4. **Path dependency and autocorrelation:** Simple permutation destroys autocorrelation in returns. Block bootstrap is needed if the strategy exploits momentum or mean-reversion at short horizons.

**The right way to use Monte Carlo in backtesting:**

| Use case | Method |
|---|---|
| Estimate true strategy distribution | Parametric bootstrap (GBM or fitted distribution) |
| Test if Sharpe is real | Permutation test on return series |
| VaR/ES for risk management | Correlated GBM across assets or historical simulation |
| Options pricing with exotic payoffs | GBM (or Heston, SABR) path simulation |
| Confidence intervals on performance metrics | Block bootstrap |

---

## Implementation

```python
import numpy as np
import pandas as pd
from scipy import stats
from typing import Optional


# ─── 1. GBM Path Simulation ─────────────────────────────────────────────────

def simulate_gbm_paths(
    S0: float,
    mu: float,
    sigma: float,
    T: int,
    n_paths: int = 10_000,
    seed: int = 42,
) -> np.ndarray:
    """
    Simulate n_paths GBM price paths over T daily steps.

    Parameters
    ----------
    S0      : initial price
    mu      : daily drift (e.g. 0.0005 for 0.05%/day)
    sigma   : daily volatility (e.g. 0.008 for 0.8%/day)
    T       : number of time steps (days)
    n_paths : number of Monte Carlo paths
    seed    : random seed

    Returns
    -------
    paths : np.ndarray of shape (n_paths, T+1), paths[:, 0] = S0
    """
    rng = np.random.default_rng(seed)
    dt = 1.0  # daily steps

    # Ito-corrected log-returns per step
    log_returns = (
        (mu - 0.5 * sigma**2) * dt
        + sigma * np.sqrt(dt) * rng.standard_normal((n_paths, T))
    )
    # Cumulative log-return paths, prepend 0 for t=0
    log_paths = np.hstack([np.zeros((n_paths, 1)), np.cumsum(log_returns, axis=1)])
    return S0 * np.exp(log_paths)


def max_drawdown_paths(paths: np.ndarray) -> np.ndarray:
    """
    Compute maximum drawdown for each path.

    Returns 1D array of MaxDD values (positive = loss magnitude).
    """
    # Running peak along time axis
    peaks = np.maximum.accumulate(paths, axis=1)
    drawdowns = (paths - peaks) / peaks   # negative values
    return -drawdowns.min(axis=1)         # return as positive fraction


def gbm_risk_analysis(
    mu_annual: float = 0.12,
    sigma_annual: float = 0.18,
    horizon_days: int = 252,
    n_paths: int = 10_000,
    drawdown_threshold: float = 0.20,
) -> dict:
    """
    Monte Carlo risk analysis: VaR, ES, and drawdown distribution.
    """
    # Convert to daily
    mu_daily = mu_annual / 252
    sigma_daily = sigma_annual / np.sqrt(252)

    paths = simulate_gbm_paths(100.0, mu_daily, sigma_daily, horizon_days, n_paths)

    # Terminal returns
    terminal_returns = (paths[:, -1] - paths[:, 0]) / paths[:, 0]

    # Max drawdowns
    mdd = max_drawdown_paths(paths)

    # VaR and ES at 95%
    var_95 = -np.percentile(terminal_returns, 5)
    es_95 = -terminal_returns[terminal_returns <= -var_95].mean()

    return {
        "mean_return": terminal_returns.mean(),
        "std_return": terminal_returns.std(),
        "VaR_95": var_95,
        "ES_95": es_95,
        "median_max_drawdown": np.median(mdd),
        "p_drawdown_exceeds_threshold": (mdd > drawdown_threshold).mean(),
        "n_paths": n_paths,
    }


# ─── 2. Permutation Test for Strategy Validity ──────────────────────────────

def compute_sharpe(returns: np.ndarray, ann_factor: int = 252) -> float:
    """Annualized Sharpe ratio from a daily return array."""
    if returns.std() == 0:
        return 0.0
    return (returns.mean() / returns.std()) * np.sqrt(ann_factor)


def permutation_test_sharpe(
    strategy_returns: np.ndarray,
    n_permutations: int = 5_000,
    seed: int = 42,
) -> dict:
    """
    Non-parametric permutation test: is the observed Sharpe ratio
    statistically significant, or explainable by random reordering?

    Parameters
    ----------
    strategy_returns : 1D array of daily strategy returns
    n_permutations   : number of shuffled samples under H0

    Returns
    -------
    dict with observed Sharpe, null distribution stats, and p-value
    """
    rng = np.random.default_rng(seed)
    obs_sharpe = compute_sharpe(strategy_returns)

    null_sharpes = np.array([
        compute_sharpe(rng.permutation(strategy_returns))
        for _ in range(n_permutations)
    ])

    # One-sided p-value: fraction of nulls >= observed
    p_value = (1 + (null_sharpes >= obs_sharpe).sum()) / (1 + n_permutations)

    return {
        "observed_sharpe": obs_sharpe,
        "null_mean": null_sharpes.mean(),
        "null_std": null_sharpes.std(),
        "null_95th_pct": np.percentile(null_sharpes, 95),
        "p_value": p_value,
        "significant_at_5pct": p_value < 0.05,
        "percentile_rank": (null_sharpes < obs_sharpe).mean() * 100,
    }


# ─── 3. Block Bootstrap ─────────────────────────────────────────────────────

def block_bootstrap_sharpe(
    strategy_returns: np.ndarray,
    block_size: int = 20,
    n_bootstrap: int = 5_000,
    seed: int = 42,
) -> np.ndarray:
    """
    Block bootstrap to estimate the sampling distribution of the Sharpe ratio.
    Preserves short-term autocorrelation by sampling contiguous blocks.

    Parameters
    ----------
    strategy_returns : 1D array of daily returns
    block_size       : length of each block (default 20 days ≈ 1 month)
    n_bootstrap      : number of bootstrap samples

    Returns
    -------
    bootstrap_sharpes : array of Sharpe ratios from each bootstrap sample
    """
    rng = np.random.default_rng(seed)
    T = len(strategy_returns)
    n_blocks = int(np.ceil(T / block_size))

    bootstrap_sharpes = []
    for _ in range(n_bootstrap):
        # Sample block starting indices (with replacement)
        starts = rng.integers(0, T - block_size + 1, size=n_blocks)
        # Stitch blocks together; trim to original length
        sample = np.concatenate([
            strategy_returns[s : s + block_size] for s in starts
        ])[:T]
        bootstrap_sharpes.append(compute_sharpe(sample))

    return np.array(bootstrap_sharpes)


# ─── 4. Monte Carlo VaR with Antithetic Variates ────────────────────────────

def mc_var_antithetic(
    weights: np.ndarray,
    mu: np.ndarray,
    cov: np.ndarray,
    horizon: int = 1,
    n_scenarios: int = 50_000,
    confidence: float = 0.95,
    seed: int = 42,
) -> dict:
    """
    Portfolio VaR/ES using Monte Carlo with antithetic variates.

    Parameters
    ----------
    weights    : portfolio weights (sum to 1)
    mu         : asset mean daily returns (n_assets,)
    cov        : asset return covariance matrix (n_assets, n_assets)
    horizon    : holding period in days
    n_scenarios: number of MC scenarios (actual draws = n_scenarios/2 + antithetics)
    confidence : VaR confidence level (0.95 → 95% VaR)
    """
    rng = np.random.default_rng(seed)
    n_assets = len(weights)
    half = n_scenarios // 2

    # Cholesky decomposition for correlated returns
    L = np.linalg.cholesky(cov * horizon)

    # Standard normal draws (half the scenarios; mirror for antithetics)
    Z = rng.standard_normal((half, n_assets))
    Z_all = np.vstack([Z, -Z])   # antithetic pairs

    # Correlated returns
    returns_matrix = (mu * horizon) + Z_all @ L.T

    # Portfolio P&L (in % terms)
    portfolio_returns = returns_matrix @ weights

    alpha = 1 - confidence
    var = -np.percentile(portfolio_returns, alpha * 100)
    es = -portfolio_returns[portfolio_returns <= -var].mean()

    return {
        "VaR": var,
        "ES": es,
        "confidence": confidence,
        "horizon_days": horizon,
        "n_scenarios": len(portfolio_returns),
    }


# ─── Demo ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # 1. GBM risk analysis
    print("=== GBM Monte Carlo Risk Analysis ===")
    risk = gbm_risk_analysis(
        mu_annual=0.10, sigma_annual=0.18,
        horizon_days=252, n_paths=20_000, drawdown_threshold=0.20
    )
    for k, v in risk.items():
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")

    # 2. Permutation test
    print("\n=== Permutation Test ===")
    np.random.seed(7)
    # Strategy with genuine alpha: +0.04%/day drift on top of noise
    real_returns = np.random.normal(0.0004, 0.01, 756)  # 3 years
    perm_result = permutation_test_sharpe(real_returns, n_permutations=5000)
    print(f"  Observed Sharpe:   {perm_result['observed_sharpe']:.3f}")
    print(f"  Null 95th pct:     {perm_result['null_95th_pct']:.3f}")
    print(f"  p-value:           {perm_result['p_value']:.4f}")
    print(f"  Significant:       {perm_result['significant_at_5pct']}")
    print(f"  Percentile rank:   {perm_result['percentile_rank']:.1f}%")

    # 3. Block bootstrap CI on Sharpe
    print("\n=== Block Bootstrap Sharpe CI ===")
    boot_sharpes = block_bootstrap_sharpe(real_returns, block_size=20, n_bootstrap=5000)
    ci_lo, ci_hi = np.percentile(boot_sharpes, [2.5, 97.5])
    print(f"  Bootstrap Sharpe: mean={boot_sharpes.mean():.3f}, "
          f"95% CI=[{ci_lo:.3f}, {ci_hi:.3f}]")

    # 4. Portfolio VaR
    print("\n=== Portfolio Monte Carlo VaR ===")
    w = np.array([0.4, 0.3, 0.3])
    mu_assets = np.array([0.0004, 0.0003, 0.0005])
    cov_assets = np.array([
        [0.0001, 0.00004, 0.00002],
        [0.00004, 0.00009, 0.00003],
        [0.00002, 0.00003, 0.00012],
    ])
    var_result = mc_var_antithetic(w, mu_assets, cov_assets, horizon=10, n_scenarios=100_000)
    print(f"  10-day 95% VaR:  {var_result['VaR']*100:.2f}%")
    print(f"  10-day 95% ES:   {var_result['ES']*100:.2f}%")
```

---

## Bridge to Quant / ML

**Permutation testing as ML model validation:** The same logic applies when you evaluate an ML model's predictive performance. Instead of shuffling returns, shuffle the label column and measure out-of-sample RMSE or IC under the null. If the true model's IC sits at the 99th percentile of the shuffled-label distribution, you have a principled p-value for predictive power.

**Monte Carlo for hyperparameter uncertainty:** After walk-forward cross-validation, use block bootstrap on the fold-level Sharpe ratios to construct a confidence interval around the strategy's OOS Sharpe. A strategy whose 95% bootstrap CI spans zero is not reliably profitable.

**Path simulation for RL training:** Reinforcement learning agents (see [[Reinforcement Learning Trading]]) cannot be trained on a single historical path — they overfit. Training on GBM-simulated paths (or mean-reverting OU-process paths, regime-switching paths) provides the diversity needed for generalization. The simulation model should be calibrated on training data and validated on OOS price behavior.

**Connection to [[Overfitting and Multiple Testing]]:** The permutation test is the Monte Carlo implementation of the null hypothesis underlying the Deflated Sharpe Ratio. While DSR provides an analytic correction factor, the permutation test makes no distributional assumptions and is robust to non-normality. In practice, both should be run: if they disagree, investigate why.

**Variance reduction in production:** When pricing a book of exotic options, antithetic variates and quasi-Monte Carlo (Sobol sequences) are standard practice. These reduce the number of scenarios needed from millions to tens of thousands for the same accuracy — a critical cost reduction in production systems.

---

## Self-Assessment

### Level 1 — Conceptual

**Q1.** Why is Monte Carlo preferred over analytical formulas for path-dependent options like Asian options or barrier options?
> **A:** Closed-form pricing formulas require specific assumptions (European payoff, no path dependence, constant parameters). Path-dependent options depend on the entire price trajectory — the average price (Asian), or whether a level was ever breached (barrier). Monte Carlo simulates full paths and computes payoffs directly from the simulated path history, handling any payoff structure.

**Q2.** What is the difference between parametric Monte Carlo and bootstrap resampling?
> **A:** Parametric Monte Carlo assumes a stochastic model (e.g., GBM) with specified parameters and draws random samples from it. Bootstrap resampling draws with replacement from actual historical observations — making no distributional assumption but implicitly assuming the future looks like the observed past. Parametric is model-dependent; bootstrap is data-dependent.

**Q3.** What is variance reduction in Monte Carlo, and why does it matter?
> **A:** Variance reduction techniques reduce the standard error of Monte Carlo estimates without increasing the number of paths — making simulation more efficient. Key techniques: antithetic variates (run paired paths with negated random shocks), control variates (use a correlated analytical solution to reduce variance), and quasi-Monte Carlo (use low-discrepancy sequences instead of random numbers).

### Level 2 — Quantitative

**Q4.** You run N = 10,000 Monte Carlo paths to price an option and get a mean price of \$5.42 with standard deviation of \$2.30. What is the 95% confidence interval for the true price?
> **A:** SE = 2.30 / √10,000 = 2.30/100 = \$0.023. 95% CI = 5.42 ± 1.96 × 0.023 = [5.375, 5.465]. To halve the CI width, you'd need 4× the paths (40,000).

**Q5.** A strategy backtest on 5 years of daily returns shows Sharpe = 1.8. You run a permutation test: shuffle the returns 10,000 times and compute the maximum Sharpe in each shuffle. The 95th percentile of max Sharpe from permutations is 1.4. What do you conclude?
> **A:** The observed Sharpe of 1.8 exceeds the 95th percentile of the null distribution (1.4), suggesting the result is unlikely to arise by chance at the 5% level. However, this tests only whether the *specific return sequence* has predictable structure — it doesn't test whether the *signal* would work on unseen data. Monte Carlo permutation gives weak evidence; walk-forward validation gives stronger evidence.

### Level 3 — Coding

**Q6.** Implement a Monte Carlo option pricer for an Asian (arithmetic average) call option using GBM paths.

```python
import numpy as np

def asian_call_monte_carlo(S0: float, K: float, r: float, sigma: float,
                            T: float, n_steps: int, n_paths: int,
                            seed: int = 42) -> tuple:
    """
    Price an arithmetic average Asian call option via Monte Carlo.
    
    Parameters
    ----------
    S0      : initial stock price
    K       : strike price
    r       : risk-free rate (annualized)
    sigma   : volatility (annualized)
    T       : time to expiry (years)
    n_steps : number of time steps in simulation
    n_paths : number of Monte Carlo paths
    seed    : random seed for reproducibility
    
    Returns
    -------
    (price, std_error) : Monte Carlo price estimate and standard error
    """
    # TODO: Implement this using GBM:
    # 1. dt = T / n_steps
    # 2. Simulate n_paths GBM paths with n_steps steps each
    # 3. For each path, compute arithmetic average of S over all steps
    # 4. Payoff = max(avg - K, 0) for each path
    # 5. Discount at risk-free rate: price = exp(-r*T) * mean(payoffs)
    # 6. Return (price, std(payoffs) / sqrt(n_paths))
    pass
```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| More Monte Carlo paths always give better results | Accuracy scales as 1/√N; after ~10,000 paths, additional paths provide diminishing returns — better to use variance reduction techniques |
| Bootstrap resampling doesn't assume a model | Bootstrap assumes the historical observations are representative of the future — it's a different assumption, not assumption-free |
| Monte Carlo simulation tests strategy validity | MC generates distributions *conditional on the model assumptions*; if the model is wrong, so is the distribution |
| Permutation tests prove a strategy works | Permutation tests only test whether in-sample performance is non-random; they don't validate out-of-sample predictability |

## Related Concepts

- [[Backtesting Methodology]] — Monte Carlo permutation tests are a key complement to walk-forward validation
- [[Overfitting and Multiple Testing]] — permutation tests provide a non-parametric version of the DSR test
- [[Almgren-Chriss]] — execution cost models are simulated via Monte Carlo when closed-form solutions don't exist
- [[Regime Detection]] — Monte Carlo path simulation should incorporate regime-switching dynamics for realistic results
- [[Statistical Arbitrage]] — portfolio-level VaR via Monte Carlo captures correlation-dependent tail risks

---

## Sources Used

- Efron, B. & Hastie, T. — *Computer Age Statistical Inference* (2016), ch. 10–11
- Lopez de Prado, M. — *Advances in Financial Machine Learning* (2018), ch. 7–8
- Glasserman, P. — *Monte Carlo Methods in Financial Engineering* (2004)
- Good, P. — *Permutation, Parametric, and Bootstrap Tests of Hypotheses* (2005)

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-11 | Note created and fully written | quality-review (file was missing) |
