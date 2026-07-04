---
type: concept
domain: 40-Strategies
tags: [strategy, equity, mean-reversion]
status: math
stability: empirical
confidence: medium
last_reviewed: 2026-04-12
review_interval_days: 30
sources:
  - "Lopez de Prado - Advances in Financial ML"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Alpha → Gap 2: Can we capture mean-reverting spreads systematically across many instruments?
> **This concept:** Statistical arbitrage scales the pairs-trading insight to a portfolio of cointegrated instruments, using PCA and factor residuals to construct market-neutral spread positions at scale.
> **Alternative approaches to this gap:** [[Momentum]], [[Alpha Factor]]
> **You need first:** [[Pairs Trading]], [[Mean Reversion]], [[Factor Models]]
> **This unlocks:** [[Overfitting and Multiple Testing]], [[Regime Detection]]

## Why This Exists

**The gap:** Pairs trading works on individual pairs but is fragile and capital-inefficient; practitioners needed a systematic approach to finding and trading many mean-reverting spreads simultaneously while controlling portfolio-level risk.
**What came before:** Discretionary pairs trading and simple cointegration-based two-asset strategies — effective but limited to a handful of hand-selected pairs with no framework for constructing diversified books.
**What this adds:** PCA-based factor extraction identifies common risk factors across a universe; residual returns from factor models are cross-sectionally mean-reverting spread candidates; portfolio construction netting long/short positions achieves near-market-neutrality; the framework scales to hundreds of positions.
**What it still doesn't solve:** The August 2007 quant meltdown showed that crowded stat arb portfolios unwind simultaneously, creating dangerous correlation in stress scenarios; factor models can misidentify regime-driven moves as mean-reverting; turnover and transaction costs erode theoretical returns significantly.

Imagine two coffee shops on the same street — one charges \$5 for a latte, the other charges \$4.50. Their prices usually track each other closely because they compete for the same customers. If one day Shop A spikes to \$7 while Shop B stays at \$4.50, you'd expect Shop A to come back down (or Shop B to rise) because the gap is temporarily unsustainable.

Statistical arbitrage works the same way with financial instruments. Instead of pure arbitrage (risk-free profit from identical assets mispriced at the same moment), stat arb bets that two *related* assets will revert to their historical price relationship. The word "statistical" is important: this bet might lose. The spread might not revert, or the relationship might break down permanently. That's the risk you're taking in exchange for the expected profit.

The three core questions stat arb asks:
1. Which instruments move together (are "co-integrated")?
2. How far has their relationship diverged right now?
3. How quickly does the relationship typically revert?

Once you can answer all three, you have a tradeable signal: enter when the spread is unusually wide, exit when it normalizes.

## Math Concepts

**Cointegration vs. Correlation**

Two time series $P_1$ and $P_2$ are *correlated* if they move in the same direction. They are *cointegrated* if there exists a linear combination that is *stationary* (mean-reverting). Correlation alone is not enough — the spread can drift arbitrarily far. Cointegration guarantees the spread has a finite variance over time.

Formally: $P_1$ and $P_2$ are I(1) (each has a unit root / random walk) but there exists $\beta$ such that:

$$S_t = P_{1,t} - \beta \cdot P_{2,t}$$

is I(0) (stationary). The parameter $\beta$ is the **hedge ratio**.

**Testing for Cointegration**

- **Engle-Granger two-step**: Regress $P_1$ on $P_2$ via OLS to find $\hat{\beta}$. Test the residuals for a unit root (ADF test). If ADF rejects the null (p < 0.05), the pair is cointegrated.
- **Johansen test**: Multivariate generalization; handles more than 2 assets and estimates the number of cointegrating relationships.

**The Spread as an Ornstein-Uhlenbeck Process**

Once a cointegrated pair is found, model the spread $S_t$ as an Ornstein-Uhlenbeck (OU) process:

$$dS_t = \kappa(\mu - S_t)\,dt + \sigma\,dW_t$$

where:
- $\kappa > 0$ — **mean-reversion speed** (larger = faster reversion)
- $\mu$ — **long-run mean** of the spread
- $\sigma$ — **volatility** of the spread
- $W_t$ — standard Brownian motion

**Half-life of mean reversion:**

$$\text{half-life} = \frac{\ln 2}{\kappa}$$

This tells you how long, on average, it takes for the spread to close half the distance to its mean. A half-life of 5 days suggests a holding period of roughly 5–15 days.

**Trading Signal**

Standardize the spread as a z-score:

$$z_t = \frac{S_t - \mu}{\sigma_{S}}$$

Entry: short the spread when $z_t > +2$, long the spread when $z_t < -2$.
Exit: close position when $|z_t| < 0.5$.

**Expected P&L (simplified)**

If you enter at $z = +2$ and exit at $z = 0$, your gross P&L per unit is $2\sigma_S$. Costs (transaction costs, borrow fees, slippage) eat into this.

## Walkthrough

Suppose we find that $\ln(\text{XOM})$ and $\ln(\text{CVX})$ (ExxonMobil and Chevron) are cointegrated with $\hat{\beta} = 0.85$.

**Day 0 (Normal state):** Spread $S = \ln(\text{XOM}) - 0.85\ln(\text{CVX}) = 0.12$. Long-run mean $\mu = 0.10$. $\sigma_S = 0.05$. Z-score = $(0.12 - 0.10)/0.05 = +0.4$. No trade — spread is within normal range.

**Day 5 (XOM jumps on a company-specific news):** XOM rises 3% while CVX is flat. Now $S = 0.21$. Z-score = $(0.21 - 0.10)/0.05 = +2.2$. Signal fires: **short XOM, long CVX** (bet that XOM will fall back relative to CVX, or CVX will rise).

**Day 12 (Reversion):** The spread normalizes. $S = 0.11$. Z-score = $+0.2$. **Exit both legs.** Gross profit = $(2.2 - 0.2) \times 0.05 = 0.10$ (10% of one spread unit).

The pair trade is always **dollar-neutral**: the dollar value of the long position equals the dollar value of the short, so broad market moves cancel out.

## Analysis

**Risks and failure modes:**

- **Spread divergence ("blow-up"):** The biggest risk. The cointegrating relationship breaks down — perhaps XOM and CVX diverge permanently because one gets a huge oil field discovery. You're short the spread and it keeps widening. Stop-losses are critical.
- **Slow reversion / capital lock-up:** The spread reverts, but takes 60 days instead of 10. Your capital is tied up and you earn less than the risk-free rate. Half-life estimation is crucial for position sizing.
- **Crowding:** If dozens of funds are running the same pairs, they all enter the same trade at once, reducing alpha and amplifying drawdowns on exit (everyone rushes for the door simultaneously).
- **Estimation risk:** OLS hedge ratio is estimated on historical data. True $\beta$ may drift over time, causing the "stationary" spread to drift.
- **Transaction costs:** Each leg generates trading costs. High-frequency stat arb is only viable with very low transaction costs (institutional accounts, co-location).

**Alpha decay:** Stat arb has experienced significant alpha decay in equities since the 2000s as it became crowded. Many practitioners have moved to longer holding periods, more assets (portfolio-level stat arb), and alternative data to find less-crowded signals.

## Implementation

```python
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, coint
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant

# ------------------------------------------------------------------
# 1. Simulate two cointegrated price series for demonstration
# ------------------------------------------------------------------
np.random.seed(42)
n = 500

# Common stochastic trend (the "glue" that keeps them together)
common_trend = np.cumsum(np.random.normal(0, 1, n))

# Each series = common trend + idiosyncratic noise
log_p1 = common_trend + np.random.normal(0, 0.5, n)
log_p2 = 0.85 * common_trend + 0.3 + np.random.normal(0, 0.5, n)

prices = pd.DataFrame({'P1': np.exp(log_p1), 'P2': np.exp(log_p2)})

# ------------------------------------------------------------------
# 2. Test for cointegration (Engle-Granger)
# ------------------------------------------------------------------
score, pvalue, _ = coint(prices['P1'], prices['P2'])
print(f"Cointegration p-value: {pvalue:.4f}")  # Should be < 0.05

# Estimate hedge ratio via OLS on log prices
log_prices = np.log(prices)
X = add_constant(log_prices['P2'].values)
result = OLS(log_prices['P1'].values, X).fit()
beta = result.params[1]
alpha = result.params[0]
print(f"Hedge ratio beta: {beta:.4f}")

# ------------------------------------------------------------------
# 3. Construct the spread and compute z-score
# ------------------------------------------------------------------
spread = log_prices['P1'] - beta * log_prices['P2'] - alpha

# Rolling z-score (use a lookback window to detect regime shifts)
lookback = 60
mu = spread.rolling(lookback).mean()
sigma = spread.rolling(lookback).std()
zscore = (spread - mu) / sigma

# ------------------------------------------------------------------
# 4. Generate trading signals
# ------------------------------------------------------------------
entry_threshold = 2.0
exit_threshold = 0.5

positions = pd.Series(0, index=spread.index)
position = 0  # +1 = long spread, -1 = short spread

for i in range(lookback, len(zscore)):
    z = zscore.iloc[i]
    if position == 0:
        if z > entry_threshold:
            position = -1   # short spread: short P1, long P2
        elif z < -entry_threshold:
            position = 1    # long spread: long P1, short P2
    elif position == 1 and z > -exit_threshold:
        position = 0        # exit long spread
    elif position == -1 and z < exit_threshold:
        position = 0        # exit short spread
    positions.iloc[i] = position

# ------------------------------------------------------------------
# 5. Compute P&L (simplified, ignoring transaction costs)
# ------------------------------------------------------------------
spread_returns = spread.diff()
strategy_returns = positions.shift(1) * spread_returns

cumulative_pnl = strategy_returns.cumsum()

print(f"\nSharpe ratio (annualized): "
      f"{strategy_returns.mean() / strategy_returns.std() * np.sqrt(252):.2f}")
print(f"Total P&L (spread units): {cumulative_pnl.iloc[-1]:.4f}")

# ------------------------------------------------------------------
# 6. Estimate OU half-life
# ------------------------------------------------------------------
spread_lag = spread.shift(1)
delta_spread = spread.diff()
df = pd.DataFrame({'delta': delta_spread, 'lag': spread_lag}).dropna()
res = OLS(df['delta'], add_constant(df['lag'])).fit()
kappa_daily = -res.params['lag']   # mean-reversion speed per day
half_life = np.log(2) / kappa_daily
print(f"\nOU kappa (daily): {kappa_daily:.4f}")
print(f"Half-life of mean reversion: {half_life:.1f} days")
```

## Bridge to Quant / ML

- **Feature engineering:** Z-scores of spreads across many pairs become cross-sectional features in an ML model. You can train a classifier to predict "will this spread revert in the next N days?"
- **Clustering for pair selection:** Use unsupervised ML (k-means, hierarchical clustering) to group stocks into sectors before applying cointegration tests. This reduces the multiple-testing problem from comparing all N*(N-1)/2 pairs.
- **Non-linear relationships:** OLS hedge ratio assumes a linear relationship. Gaussian process regression or neural networks can model non-linear cointegrating relationships.
- **Regime detection:** Use Hidden Markov Models (HMMs) to identify periods of "stable cointegration" vs. "breakdown." Only trade during stable regimes.
- **Lopez de Prado connection:** Bet sizing via the Kelly criterion requires an estimate of the OU parameters ($\kappa$, $\sigma$). The CUSUM filter (from AFML Chapter 2) can be used to label meaningful spread movements as training samples.

## Self-Assessment

### Level 1 — Conceptual

**Q1.** What distinguishes statistical arbitrage from true arbitrage, and why does the word "statistical" matter?
> **A:** True arbitrage is risk-free profit from identical assets mispriced simultaneously; stat arb bets that *related* assets will revert to their historical relationship — but that relationship might not hold, making it a probabilistic bet with genuine loss risk.

**Q2.** Why do practitioners use factor-model residuals rather than raw prices as the input to cointegration tests?
> **A:** Raw prices reflect both common factor exposures (market, sector) and idiosyncratic movements. Using factor residuals isolates the idiosyncratic spread, making the mean-reversion test more powerful and the resulting strategy more market-neutral.

**Q3.** What is the "crowding problem" in stat arb, and why did it manifest so violently in August 2007?
> **A:** Many quant funds run similar stat arb books; when one fund deleverages, its trades move spreads against all similar funds, triggering further forced unwinding — a positive feedback loop. August 2007 saw this cascade across the entire stat arb industry simultaneously.

### Level 2 — Quantitative

**Q4.** Given a portfolio of N spread positions each with OU half-life τ and annual volatility σ, how does diversification affect portfolio Sharpe ratio as N grows?
> **A:** If positions are uncorrelated, portfolio Sharpe grows as √N × (single-spread Sharpe); in practice, factor residuals have residual correlation, so gains are less than √N. The benefit comes from law-of-large-numbers averaging of independent mean-reversion bets.

**Q5.** The PCA-based stat arb procedure extracts k factors. How do you choose k, and what happens if k is too small vs. too large?
> **A:** Too few factors leave common systematic risk in the "residual" spread, so positions appear mean-reverting but carry hidden beta; too many factors over-explain the data and leave insufficient idiosyncratic variation to trade. Standard approach: use factors explaining 80–90% of variance, or cross-validate by holding out a test period.

### Level 3 — Coding

**Q6.** Implement a PCA-based stat arb signal generator: fit PCA on a log-return matrix, reconstruct the systematic component, compute residuals, and generate z-score entry signals.

```python
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def statarb_zscore_signals(log_returns: np.ndarray, n_factors: int = 5,
                           lookback: int = 60) -> np.ndarray:
    """
    Compute cross-sectional z-scores of PCA residuals for stat arb entry signals.
    
    Parameters
    ----------
    log_returns : (T, N) array of log returns for N assets over T periods
    n_factors   : number of PCA factors to remove
    lookback    : rolling window for mean/std of residuals
    
    Returns
    -------
    z_scores : (T, N) array; signal > 2 → short, < -2 → long
    """
    # TODO: Implement this function
    # Steps:
    # 1. Fit PCA on the full log_returns matrix (standardize first)
    # 2. Project returns onto n_factors principal components
    # 3. Reconstruct systematic component and subtract to get residuals
    # 4. Compute rolling z-score of each residual series
    # 5. Return z-score matrix — negative z-score = likely to revert up (long signal)
    pass
```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Stat arb is risk-free because it's "arbitrage" | The "statistical" qualifier means it can lose; cointegration relationships break |
| More PCA factors always improves neutrality | Too many factors over-fit and destroy the tradeable spread signal |
| Factor-neutral means market-neutral | Factor models have estimation error; residual market exposure persists |
| A high in-sample Sharpe guarantees live performance | Stat arb is highly susceptible to overfitting via parameter selection on historical data |

## Related Concepts

- [[Pairs Trading]] — the simplest two-asset form of stat arb
- [[Mean Reversion]] — the underlying price behavior stat arb exploits
- [[Ornstein-Uhlenbeck Process]] — the continuous-time model used to characterize the mean-reverting spread
- [[Market Making]] — another strategy that monetizes mean-reversion at microstructure level
- [[Order Book]] — execution venue for the two legs
- [[Adverse Selection]] — risk that your counterparty is informed (relevant to execution)

## Sources Used

- Lopez de Prado, M. — *Advances in Financial Machine Learning* (2018), Chapters 2, 3, 17
- Engle, R. F. & Granger, C. W. J. — "Co-integration and Error Correction" (1987), *Econometrica*
- Vidyamurthy, G. — *Pairs Trading: Quantitative Methods and Analysis* (2004)

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | Added [[Ornstein-Uhlenbeck Process]] to Related Concepts | QA review |
