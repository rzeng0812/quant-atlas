---
type: concept
domain: 60-ML-Finance
tags: [ml-finance, regimes]
status: math
stability: evolving
confidence: medium
last_reviewed: 2026-04-12
review_interval_days: 90
sources:
  - "Lopez de Prado - Advances in Financial ML"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Alpha → Gap 2: Can we capture mean-reverting spreads systematically across many instruments?
> **This concept:** Regime detection identifies latent market states to condition strategy selection, position sizing, and model parameters — addressing the non-stationarity that undermines static strategies.
> **Alternative approaches to this gap:** [[Alpha Factor]] (static), [[Feature Engineering Finance]] (conditional features)
> **You need first:** [[Feature Engineering Finance]], [[Alpha Factor]], [[Backtesting Methodology]]
> **This unlocks:** [[Alpha Factor]], [[Reinforcement Learning Trading]]

## Why This Exists

**The gap:** Static trading strategies assume the return-generating process is stationary, but empirically markets alternate between fundamentally different states (trending, mean-reverting, crisis); a single parameterization fails across regimes.
**What came before:** Single-regime models — CAPM, fixed-parameter momentum strategies — that perform well in some periods and catastrophically in others without any systematic way to detect regime transitions or adapt.
**What this adds:** Hidden Markov Models (HMMs) provide a probabilistic framework for latent regime inference from observed returns or volatility; Gaussian mixture models cluster return distributions into distinct states; online regime inference allows real-time state probability estimation; regime labels as features improve conditional alpha models; risk controls that tighten during identified high-risk regimes reduce drawdowns.
**What it still doesn't solve:** Regime changes are only clearly visible in hindsight — real-time detection lags by the HMM transition probability, creating "regime lag"; with only one realization of history, it's difficult to validate regime models out-of-sample; models that fit historical regimes well may miss novel regime types (e.g., COVID-19 market structure was unlike any prior crisis in the HMM's training data).

Markets do not behave the same way all the time. The stock market in 2017 was calm, trending upward, with volatility near record lows — a "risk-on" regime. The market in March 2020 or October 2008 was panicked, dislocated, with correlations spiking to 1 and volatility exploding — a "crisis" regime.

The problem is that a trading strategy calibrated on 2017 data will perform terribly in 2008, and vice versa. A momentum strategy works beautifully in calm, trending markets and loses catastrophically in volatile reversal regimes. A mean-reversion strategy does the opposite.

Think of it like driving: in clear weather, you drive at highway speed. In a snowstorm, you slow down and change your behavior entirely. A self-driving car that ignores the weather and always drives the same way will crash. Similarly, a trading algorithm that ignores market regimes will blow up when conditions change.

Regime detection asks: **which "state" is the market in right now?** If we can answer that reliably, we can:
1. Switch strategies: use momentum in trending regimes, mean-reversion in oscillating ones
2. Adjust position sizing: reduce risk in crisis regimes
3. Adapt model parameters: use short-history estimates in fast-moving regimes, longer history in stable ones

The hard part: regime changes are only perfectly obvious **in hindsight**. Real-time detection is noisy, delayed, and often wrong. This is why regime detection is one of the most challenging problems in quantitative finance.

## Math Concepts

### Hidden Markov Model (HMM)

The most principled approach. The market has $K$ latent (hidden) states $s_t \in \{1, \ldots, K\}$ that follow a Markov chain. At each time step, the observed return $r_t$ is drawn from a regime-specific distribution.

**Transition matrix** $A$ (K x K):
$$A_{ij} = P(s_t = j \mid s_{t-1} = i)$$

Captures how regimes persist and transition. If $A_{11} = 0.97$, regime 1 is very persistent (expected duration = $1/(1-0.97) = 33$ days).

**Emission distribution** (Gaussian HMM):
$$r_t \mid s_t = k \sim \mathcal{N}(\mu_k, \sigma_k^2)$$

Each regime has its own mean return $\mu_k$ and volatility $\sigma_k$.

**Parameters to estimate:** $A$, $\{\mu_k, \sigma_k\}$, and initial state probabilities $\pi$.

**Inference:**
- **Viterbi algorithm:** find the most likely state sequence $\{s_t\}$ given observed returns (offline, uses future data)
- **Forward-backward algorithm:** compute $P(s_t \mid r_1, \ldots, r_T)$ (offline, smoothed)
- **Filtering:** compute $P(s_t \mid r_1, \ldots, r_t)$ — online, only uses past data

**Training:** Expectation-Maximization (Baum-Welch algorithm) maximizes the likelihood $P(\mathbf{r} \mid \theta)$.

### Gaussian Mixture Model (GMM) Clustering

Fit a mixture of Gaussians to the distribution of feature vectors. Each component is a "regime." Unlike HMM, GMM ignores time ordering.

$$p(\mathbf{x}) = \sum_{k=1}^K \pi_k \mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k)$$

Assign observation to regime $k^* = \arg\max_k P(k \mid \mathbf{x})$.

### Threshold-Based Regimes

Simple, transparent, and widely used in practice:

| Signal | Low regime | High regime |
|--------|-----------|-------------|
| VIX | < 20 (low vol) | > 30 (crisis) |
| 200-day MA | Price above (bull) | Price below (bear) |
| 2s10s | > 0 (normal) | < 0 (inverted) |

### Hurst Exponent

The Hurst exponent $H$ characterizes the memory of a time series:

$$H = \frac{\log(R/S)}{\log(T)}$$

Where $R/S$ is the rescaled range over $T$ observations.

- $H > 0.5$: trending (persistent) — momentum strategies work
- $H = 0.5$: random walk — no predictability
- $H < 0.5$: mean-reverting — mean-reversion strategies work

The Hurst exponent is a **soft regime indicator** — it tells you about the current microstructure without requiring discrete regime labels.

## Walkthrough

### 2-State HMM on S&P 500 Returns

We fit a 2-state Gaussian HMM to daily S&P 500 log returns. We expect to find:
- **State 0:** Bull market — positive mean, low volatility
- **State 1:** Bear/crisis — negative or near-zero mean, high volatility

After fitting, we compute:
- The Viterbi path (most likely state sequence, for analysis)
- The filtered state probabilities (usable online for trading)

Typical fitted parameters on S&P 500 (2000-2020):
- State 0 (Bull): $\mu_0 \approx +0.07\%/\text{day}$, $\sigma_0 \approx 0.7\%$
- State 1 (Bear): $\mu_1 \approx -0.15\%/\text{day}$, $\sigma_1 \approx 2.2\%$
- $A_{00} \approx 0.98$ (bull is persistent), $A_{11} \approx 0.97$ (crisis is also persistent)

## Analysis

**Key challenges:**

1. **Detection lag:** By the time enough data confirms a regime change, much of the move has already happened. The forward algorithm only knows a regime changed after it has persisted.

2. **Label instability:** HMM regimes depend on initialization and can be relabeled across model re-fits. State 0 today may be called State 1 tomorrow after adding new data.

3. **Overfitting the number of states:** More states always improve in-sample likelihood but may not generalize. Use BIC/AIC to select $K$ or cross-validate.

4. **Non-Gaussian returns:** Real returns have fat tails, especially in crisis regimes. Gaussian HMM will underestimate crisis probability. Use Student-t emissions for robustness.

5. **Spurious regimes:** Clustering on raw returns without robust feature engineering can produce regimes that are artifacts of the data rather than genuine market states.

**When each method works best:**
| Method | Strengths | Weaknesses |
|--------|-----------|------------|
| HMM | Captures persistence, principled | Computationally heavier, Gaussian assumption |
| GMM | Simple, fast | Ignores temporal structure |
| Threshold | Transparent, easy to explain | Arbitrary cutoffs, no uncertainty estimate |
| Hurst | Continuous, no discrete labels needed | Needs long window to estimate reliably |

## Implementation

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from hmmlearn import hmm
from sklearn.preprocessing import StandardScaler

# --- 2-State Gaussian HMM ---

def fit_hmm_regime_model(returns: pd.Series, n_states: int = 2, n_iter: int = 200):
    """
    Fit a Gaussian HMM to a return series.
    
    Parameters
    ----------
    returns  : pd.Series of daily log returns
    n_states : number of hidden states (regimes)
    n_iter   : EM iterations
    
    Returns
    -------
    model         : fitted GaussianHMM
    viterbi_states: array of most likely state at each time (offline)
    state_probs   : array (T x K) of state probabilities
    """
    X = returns.values.reshape(-1, 1)   # hmmlearn expects (T, n_features)

    model = hmm.GaussianHMM(
        n_components=n_states,
        covariance_type='diag',
        n_iter=n_iter,
        random_state=42
    )
    model.fit(X)

    # Viterbi: best state sequence using all data (use for analysis, not live trading)
    viterbi_states = model.predict(X)

    # Smoothed state probabilities: P(s_t | all observations)
    state_probs = model.predict_proba(X)

    return model, viterbi_states, state_probs


def identify_regime_labels(model, viterbi_states, returns):
    """
    Auto-label states as 'bull' or 'bear' by mean return.
    Convention: higher mean return = bull.
    """
    means = model.means_.flatten()
    bull_state = np.argmax(means)
    bear_state = np.argmin(means)

    labels = np.where(viterbi_states == bull_state, 'bull', 'bear')

    print("Regime parameters:")
    for k in range(model.n_components):
        label = 'bull' if k == bull_state else 'bear'
        mu = model.means_[k, 0] * 252       # annualized
        # covars_ shape for 'diag' is (n_components, n_features); index with [k, 0]
        sigma = np.sqrt(model.covars_[k, 0]) * np.sqrt(252)
        print(f"  State {k} ({label}): ann. mu={mu:.2%}, ann. sigma={sigma:.2%}")

    print(f"\nTransition matrix:\n{model.transmat_}")

    return labels, bull_state, bear_state


def plot_regimes(returns, viterbi_states, state_probs, bull_state):
    """Visualize price, regimes, and state probabilities."""
    cum_ret = (1 + returns).cumprod()
    bear_state = 1 - bull_state   # for 2-state only

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

    # Plot cumulative return with regime shading
    ax1.plot(returns.index, cum_ret.values, 'k-', lw=1, label='Cumulative Return')
    bull_mask = viterbi_states == bull_state
    ax1.fill_between(
        returns.index,
        cum_ret.values.min(), cum_ret.values.max(),
        where=~bull_mask, alpha=0.25, color='red', label='Bear Regime'
    )
    ax1.set_ylabel('Cumulative Return')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot state probability over time
    ax2.plot(returns.index, state_probs[:, bear_state], 'r-', lw=1,
             label=f'P(Bear Regime)')
    ax2.axhline(0.5, color='gray', linestyle='--', alpha=0.5)
    ax2.set_ylabel('P(Bear Regime)')
    ax2.set_xlabel('Date')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.suptitle('2-State HMM Regime Detection', fontsize=12)
    plt.tight_layout()
    plt.savefig('hmm_regimes.png', dpi=150)
    plt.show()


# --- Hurst Exponent ---

def hurst_exponent(ts: np.ndarray, max_lag: int = 100) -> float:
    """
    Estimate the Hurst exponent using the R/S method.
    
    H > 0.5: trending
    H = 0.5: random walk
    H < 0.5: mean-reverting
    """
    lags = range(2, max_lag)
    tau = [np.std(np.subtract(ts[lag:], ts[:-lag])) for lag in lags]
    # Fit log(std) ~ H * log(lag)
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return poly[0]   # slope = Hurst exponent


# --- Threshold-based regime ---

def vix_regime(vix_series: pd.Series,
               low_thresh: float = 20,
               high_thresh: float = 30) -> pd.Series:
    """
    Simple VIX threshold regime:
    0 = calm (VIX < low_thresh)
    1 = elevated
    2 = crisis (VIX > high_thresh)
    """
    regime = pd.Series(1, index=vix_series.index)
    regime[vix_series < low_thresh] = 0
    regime[vix_series > high_thresh] = 2
    return regime


# --- Usage Example (synthetic data) ---
np.random.seed(42)
n = 2000

# Simulate bull and bear regimes
state_seq = np.zeros(n, dtype=int)
state_seq[500:700] = 1    # bear
state_seq[1200:1400] = 1  # bear

ret = np.where(
    state_seq == 0,
    np.random.normal(0.0004, 0.007, n),   # bull: +0.04%/day, 0.7% vol
    np.random.normal(-0.0008, 0.020, n)   # bear: -0.08%/day, 2.0% vol
)
dates = pd.date_range('2015-01-01', periods=n, freq='B')
returns = pd.Series(ret, index=dates)

# Fit HMM
model, viterbi, probs = fit_hmm_regime_model(returns, n_states=2)
labels, bull, bear = identify_regime_labels(model, viterbi, returns)
plot_regimes(returns, viterbi, probs, bull)

# Hurst exponent
H = hurst_exponent(returns.values)
print(f"\nHurst exponent: {H:.4f}")
print(f"  -> {'Trending' if H > 0.55 else ('Mean-reverting' if H < 0.45 else 'Random walk')}")
```

## Bridge to Quant / ML

**Strategy switching:** The most direct application is to fit a separate model for each regime and select the active model based on current regime probability. For example, a momentum model in bull regimes and a low-volatility defensive model in bear regimes.

**Risk management:** Reduce position sizes (multiply by $1 - P(\text{bear})$) as bear probability rises. This is a smooth, probabilistic risk management approach rather than a binary on/off switch.

**Feature for downstream models:** Regime probabilities (or the Hurst exponent rolling estimate) are valuable features in [[Feature Engineering Finance]] pipelines. They let ML models condition on market state without explicitly knowing the regime model architecture.

**Connection to [[Yield Curve]]:** The 2s10s yield curve inversion is itself a regime indicator — an inverted curve indicates a macro regime shift. Similarly, credit spreads widening above certain thresholds signal stress regimes. Macro regime signals like these have longer lead times (months) than volatility-based signals.

**HMM in practice:** The biggest practical issue is **regime mislabeling across re-fits**. Professional implementations sort states by volatility (ascending) at each refit to maintain consistent labeling. They also use rolling window refits with careful out-of-sample validation.

**Deep learning approaches:** LSTMs and transformers can implicitly learn regime structure without explicit HMM fitting. However, HMM has the advantage of interpretability and principled uncertainty quantification.

## Self-Assessment

### Level 1 — Conceptual

**Q1.** What is a Hidden Markov Model and why is the "hidden" part critical for financial applications?
> **A:** An HMM models an observable sequence (returns, volatility) as generated by a hidden (latent) state sequence. The hidden states (market regimes) are never directly observed — we only see their emissions. This is critical because market regimes aren't labeled in real time; we must infer them from noisy observable signals, and the HMM framework provides a principled probabilistic inference mechanism (Viterbi, Baum-Welch).

**Q2.** What is the "regime lag" problem, and what is its practical consequence for trading?
> **A:** Regime lag: because the HMM transitions probabilistically, the model's posterior probability of a regime change takes several observations to accumulate. A crisis that began Monday may only be identified with high confidence by Thursday. By then, the worst of the initial move has already occurred. Practical consequence: regime-based risk controls activate too late to prevent initial losses; they're more useful for sustaining reduced risk during a regime than for catching the initial transition.

**Q3.** How can regime detection improve a momentum strategy?
> **A:** Momentum crashes occur when markets sharply reverse — typically during crisis-to-recovery transitions. A regime model that identifies "crisis" or "reversal" regimes can reduce or eliminate momentum exposure during these periods, cutting the tail risk that makes momentum one of the most dangerous factor crashes. Conversely, increasing momentum exposure during confirmed "trending" regimes improves risk-adjusted returns.

### Level 2 — Quantitative

**Q4.** A 2-state HMM is fitted with estimated transition matrix P = [[0.95, 0.05], [0.10, 0.90]] (rows = current state, columns = next state). If the market is currently in state 0 (low-vol), what is the probability of still being in state 0 after 10 periods?
> **A:** P^10 can be computed via eigendecomposition. The stationary distribution is π₀ = 0.10/(0.05+0.10) = 0.67, π₁ = 0.33. After 10 steps from state 0, the probability is approximately: π₀ + (P₀₀ − π₀)(λ₂)^10, where λ₂ = 1 − 0.05 − 0.10 = 0.85. P(state 0 at t=10 | state 0 at t=0) ≈ 0.67 + (1−0.67) × 0.85^10 ≈ 0.67 + 0.33 × 0.197 ≈ 0.735.

**Q5.** Why does k-means clustering on return volatility produce different regimes than HMM, and which tends to be more appropriate for regime-conditional trading?
> **A:** K-means assigns each observation independently to the nearest centroid, ignoring temporal structure. Two consecutive days of high volatility are treated identically to two non-consecutive high-vol days. HMM explicitly models state persistence (transition probabilities), giving regime assignments that respect the fact that market states tend to persist. For trading, HMM regimes are more meaningful because they capture the autocorrelated nature of market conditions.

### Level 3 — Coding

**Q6.** Implement a 2-state HMM regime detector using the hmmlearn library and plot the inferred regime probabilities over time.

```python
import numpy as np
import pandas as pd

def fit_regime_hmm(returns: pd.Series, n_regimes: int = 2,
                   n_iter: int = 100, random_state: int = 42) -> pd.DataFrame:
    """
    Fit a Hidden Markov Model to returns and extract regime probabilities.
    
    Parameters
    ----------
    returns      : daily return series
    n_regimes    : number of hidden states (typically 2 or 3)
    n_iter       : maximum EM iterations for fitting
    random_state : reproducibility seed
    
    Returns
    -------
    regimes : DataFrame with columns ['regime_0_prob', 'regime_1_prob', 'regime_label']
              where regime_label is the argmax state at each date
    """
    # TODO: Implement using hmmlearn:
    # from hmmlearn import hmm
    # 1. Reshape returns to (T, 1) feature matrix
    # 2. Fit GaussianHMM with n_regimes components
    # 3. Use model.predict_proba() for soft regime probabilities
    # 4. Sort regimes by volatility (regime 0 = low-vol, regime 1 = high-vol)
    # 5. Return DataFrame with regime probabilities and label
    pass
```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Regime detection provides advance warning of regime changes | Regime detection is primarily reactive — it identifies the current regime from recent data, typically with lag; it doesn't predict regime changes before they occur |
| More regimes always improves the model | With more regimes, the model can overfit to historical noise; 2–3 regimes are usually sufficient and interpretable for practical applications |
| Once a regime is detected, the strategy should fully switch | Regime probabilities are continuous; a hard switch at 50% threshold is suboptimal; better to scale position sizes proportionally to regime confidence |
| HMM regimes correspond directly to "bull/bear markets" | HMM regimes are statistical constructs identified from the model's emission parameters; they may not align with common narrative market labels |

## Related Concepts

- [[Alpha Factor]] — factor performance is regime-dependent
- [[Feature Engineering Finance]] — regime probabilities as ML features
- [[Reinforcement Learning Trading]] — RL policy should adapt to regime
- [[Statistical Arbitrage]] — regime shifts invalidate pair correlations; regime detection is a key risk control

## Sources Used

- Lopez de Prado, M. - *Advances in Financial Machine Learning* (2018), ch. 17
- Rabiner, L. - *A Tutorial on Hidden Markov Models* (1989)
- Hamilton, J. - *A New Approach to the Economic Analysis of Nonstationary Time Series* (1989)

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review: fixed Python bug (covars_ indexing for diag covariance); replaced unknown wikilinks [[Yield Curve]] and [[Hurst Exponent]] with [[Statistical Arbitrage]] | quality-review |
