---
type: concept
domain: 50-Implementation
tags: [backtesting, implementation, strategies]
status: math
stability: evolving
confidence: high
last_reviewed: 2026-04-18
review_interval_days: 90
sources:
  - "Lopez de Prado - Advances in Financial ML ch.14"
created: 2026-04-18
---

> [!info] Problem Chain
> **Chain:** Alpha → Gap 2: Can we trust that a strategy's historical performance reflects real alpha rather than data-mining luck?
> **This concept:** Backtesting methodology defines the rigorous process for evaluating a strategy's historical performance while controlling for the many biases — lookahead, survivorship, overfitting — that make backtests flatter than live trading.
> **Alternative approaches to this gap:** Walk-forward testing, paper trading, synthetic data
> **You need first:** [[Sharpe Ratio]], [[Alpha Factor]], [[Overfitting and Multiple Testing]]
> **This unlocks:** [[Monte Carlo Methods]], [[Overfitting and Multiple Testing]]

## Why This Exists

**The gap:** Strategies that look profitable in simulation often fail in live trading; without rigorous methodology, it's impossible to distinguish genuine alpha from data-mining artifacts, lookahead bias, and survivorship bias.
**What came before:** Simple historical simulation — run the strategy on all available data, report the Sharpe ratio — which systematically overstates expected performance due to in-sample optimization and ignored biases.
**What this adds:** A taxonomy of backtesting biases with specific remedies (point-in-time data for survivorship, strict time-ordering for lookahead, walk-forward or k-fold with purging/embargo for overfitting); the deflated Sharpe ratio that adjusts for multiple testing; the CPCV (combinatorial purged cross-validation) framework for estimating realistic performance distributions.
**What it still doesn't solve:** Even rigorous backtests can't account for regime changes not in the historical window; execution assumptions (fill at VWAP, zero market impact) are never perfectly replicable; the fundamental problem of evaluating a strategy on a single historical path remains.

Imagine you've come up with a trading idea: "Buy stocks that have gone up over the last year, because winners tend to keep winning." It sounds plausible. Before risking real money, you test it on historical data. The backtest returns 30% per year with a Sharpe ratio of 2.1. You're excited.

Then you deploy it live, and it loses money.

What happened? Welcome to the central trap of quantitative finance: the backtest is a simulation, not a guarantee. It tells you what *would have* happened if you had followed a rule — but only if you built the simulation correctly. Most backtests are subtly wrong in ways that systematically flatter the strategy. The closer you look, the worse they perform.

There are five classic enemies:

1. **Look-ahead bias** — accidentally using information that wasn't yet available. For example, using today's closing price to make today's trading decision. In real life, you can't know the closing price until the day is over. In code, it's as subtle as missing a single `.shift(1)` on a feature.

2. **Survivorship bias** — only testing on stocks that still exist today. Companies that went bankrupt, got acquired, or were delisted are not in today's stock database. If you test only on today's S&P 500 constituents going back to 2005, you've excluded all the companies that got kicked out or failed. Your universe looks healthier than it actually was.

3. **Overfitting (data snooping)** — testing hundreds of rule variations until one looks good, then reporting only that one. The strategy worked on this historical period by luck, not by skill. It won't generalize.

4. **Transaction cost blindness** — a strategy that trades daily might show a Sharpe of 2.1 before costs and 0.4 after realistic bid-ask spreads and commissions. If you're not modeling costs, you're running a fantasy.

5. **Regime blindness** — the relationship between signal and return changes over time. A strategy that worked brilliantly in 2010–2018 might be based on a regime that no longer exists (zero rates, low volatility, trend-following dominance).

The answer to all five is disciplined backtesting methodology: a structured pipeline, realistic cost models, and strict separation between in-sample development and out-of-sample testing.

## Math Concepts

### The Backtesting Pipeline

A rigorous backtest has six stages, in order:

| Stage | What it does | Key decisions |
|-------|-------------|---------------|
| 1. Universe selection | Which assets, which dates | Avoid survivorship bias; use a point-in-time index membership list |
| 2. Signal generation | Entry/exit rules from features | Ensure all features are lagged to be available at trade time |
| 3. Position sizing | How much capital to allocate | Equal weight vs. volatility-scaled vs. signal-proportional |
| 4. Transaction cost modeling | Bid-ask, market impact, commissions | Critical — see below |
| 5. Performance evaluation | Sharpe, MaxDD, Calmar, etc. | Use deflated Sharpe Ratio (DSR) rather than naive SR |
| 6. Walk-forward validation | IS vs. OOS split | Typically 3:1 IS:OOS ratio by time |

### Return Computation

For a single asset position:

$$R_t = w_t \cdot r_t - c \cdot |\Delta w_t|$$

Where:
- $w_t$ = position weight at time $t$
- $r_t = \log(P_t / P_{t-1})$ = log return
- $c$ = one-way transaction cost (bid-ask spread + commission)
- $|\Delta w_t|$ = turnover (absolute change in position weight)

Portfolio return:

$$R_t^{portfolio} = \sum_{i=1}^{N} w_{i,t} \cdot r_{i,t} - c \sum_{i=1}^{N} |\Delta w_{i,t}|$$

### Key Performance Metrics

**Sharpe Ratio** (annualized):
$$\text{SR} = \frac{E[R_t] - r_f}{\sigma[R_t]} \cdot \sqrt{252}$$

Where $r_f$ is the risk-free rate. A Sharpe above 1.0 is respectable; above 2.0 is suspicious unless you have strong out-of-sample evidence.

**Maximum Drawdown (MaxDD)**:
$$\text{MaxDD} = \max_{t \leq T} \left( \max_{s \leq t} V_s - V_t \right) / \max_{s \leq t} V_s$$

Where $V_t$ is portfolio value at time $t$. MaxDD measures the worst peak-to-trough decline in portfolio history.

**Calmar Ratio**:
$$\text{Calmar} = \frac{\text{Annualized Return}}{|\text{MaxDD}|}$$

A high Calmar (>1) means you earn back your worst drawdown in a year or less.

### Deflated Sharpe Ratio (DSR)

When you have tested $N$ strategies, the best Sharpe from random variation follows:

$$E[\max_N \hat{SR}] \approx \left(1 - \gamma \cdot Z\right) \cdot \sqrt{\frac{\ln N}{\ln \ln N}}$$

The **Deflated Sharpe Ratio** (Bailey & Lopez de Prado, 2014) adjusts the observed Sharpe for:
1. Multiple testing across $N$ strategies
2. Non-normality of returns (skewness $\hat{\gamma}_3$, excess kurtosis $\hat{\gamma}_4$)
3. Backtest length $T$

$$\text{DSR} = \Phi\!\left(\frac{(\hat{SR} - SR^*) \cdot \sqrt{T-1}}{\sqrt{1 - \hat{\gamma}_3 \cdot \hat{SR} + \frac{\hat{\gamma}_4 - 1}{4} \cdot \hat{SR}^2}}\right)$$

Where $SR^*$ is the expected best Sharpe from $N$ trials under the null of no skill, and $\Phi$ is the standard normal CDF. **DSR > 0.95 is the bar for statistical significance.**

### Walk-Forward Validation

The standard guard against overfitting. Divide historical data into sequential blocks:

```
|-------- In-Sample (IS) --------|-- OOS --|
 Fit / Optimize              Test

Slide forward:
|-------- IS (extended) --------|-- OOS --|
                             Test
```

A typical rule: IS window is 3× the OOS window. For example, 3 years IS, 1 year OOS, slide forward by 1 year.

The OOS Sharpe ratio is the honest number. If IS Sharpe >> OOS Sharpe, the strategy is overfit.

**The overfitting ratio:**
$$\text{Overfit Score} = 1 - \frac{SR_{OOS}}{SR_{IS}}$$

Values near 0 = well-generalizing strategy. Values near 1 = in-sample illusion.

### Transaction Cost Modeling

| Cost type | Typical magnitude | Notes |
|-----------|-------------------|-------|
| Bid-ask spread | 1–10 bps (large cap), 10–100 bps (small cap) | Half-spread per trade |
| Commission | 0–5 bps | Near-zero for retail; higher for institutions |
| Market impact | 10–50 bps for \$1M+ orders | Slippage from moving the price |
| Short borrow cost | 25–500 bps/year | For short positions |

For a daily rebalancing strategy with 1-way cost $c = 0.1\%$:

$$\text{Annual cost drag} \approx c \times \text{Average Turnover} \times 252$$

A 100% daily turnover strategy (common in mean-reversion) loses ~50% per year to costs alone at 0.1% per trade. This destroys almost any signal.

## Walkthrough

### Step-by-Step: Momentum Backtest, Before and After Costs

**Universe:** 100 US large-cap stocks, 2010–2023.
**Signal:** 12-month momentum (buy top quartile by prior-year return, sell bottom quartile).
**Rebalance:** Monthly.

**Before costs:**
- Mean monthly return: +0.42%
- Monthly Sharpe: +0.35
- Annualized Sharpe: ~2.1 ✓ (looks great)

**Monthly turnover:** ~40% (many stocks rotate in/out quarterly)
**Round-trip cost per trade:** 0.20% (spread + commission + slippage)

**After costs:**
- Cost per month: 40% turnover × 0.20% / 2 = ~0.04% per leg, but it compounds...
- Net monthly return: +0.42% - 0.08% = +0.34%... (but in practice, more like +0.07% for small-caps)

For large-caps, costs are manageable. For small-caps at higher spread:

$$\text{Net Sharpe} = \frac{0.07\%}{1.2\%} \times \sqrt{12} \approx 0.2$$

A Sharpe of 2.1 became 0.4 after realistic costs. This is why the cost model is not optional.

### Detecting Look-Ahead Bias

The most common coding mistake. Example:

```python
# WRONG: uses today's close in today's signal — look-ahead
df['signal'] = df['close'].rolling(20).mean()
df['return'] = df['close'].pct_change().shift(-1)  # tomorrow's return

# RIGHT: yesterday's signal predicts tomorrow's return
df['signal'] = df['close'].rolling(20).mean().shift(1)
df['return'] = df['close'].pct_change().shift(-1)
```

A quick diagnostic: if your backtest has suspiciously round-number performance (e.g., SR = 4.7, MaxDD = 1%), assume look-ahead bias until proven otherwise.

## Analysis

**Common failure modes ranked by subtlety:**

1. **Missing `.shift(1)`** on a feature — the single most common bug. Always shift features by at least one period before using them as signals.

2. **Using end-of-period index constituents** — test on the S&P 500 as-of today, not as-of each historical date. Point-in-time index membership data is sold by Compustat/CRSP but often absent in free datasets.

3. **Ignoring short borrow** — a short-selling strategy that looks profitable might have cost 3–4% annualized in borrow fees. These are invisible unless modeled.

4. **Ignoring execution timing** — if your signal fires on the close, can you actually trade at that close? Many strategies assume you can buy at the signal price. In practice, you trade on the next open or VWAP.

5. **Stationarity assumptions** — market microstructure changed dramatically after 2010 (decimalization, HFT, ETF proliferation). A strategy calibrated on 2000–2010 data is implicitly assuming those microstructural conditions still hold.

**The OOS/IS ratio as a sanity test:**

| OOS/IS Sharpe Ratio | Interpretation |
|--------------------|----------------|
| > 0.8 | Excellent generalization |
| 0.5 – 0.8 | Reasonable — some overfitting |
| 0.2 – 0.5 | Concerning — likely overfit |
| < 0.2 | The backtest found noise, not signal |

## Implementation

```python
import numpy as np
import pandas as pd
from scipy import stats
from dataclasses import dataclass, field
from typing import Optional

# ============================================================
# Backtesting Engine
# ============================================================

@dataclass
class BacktestConfig:
    cost_bps: float = 10.0          # one-way transaction cost in basis points
    risk_free_rate: float = 0.04    # annual risk-free rate
    rebalance_freq: str = 'M'       # 'D' daily, 'W' weekly, 'M' monthly
    is_fraction: float = 0.75       # fraction of data used for in-sample


class BacktestEngine:
    """
    Minimal backtesting engine for daily bar data.

    Parameters
    ----------
    prices : DataFrame (dates x tickers), adjusted close prices
    signals : DataFrame (dates x tickers), raw alpha signal (higher = more bullish)
    config  : BacktestConfig
    """

    def __init__(self,
         prices: pd.DataFrame,
         signals: pd.DataFrame,
         config: Optional[BacktestConfig] = None):
self.prices = prices
self.signals = signals
self.cfg = config or BacktestConfig()
self._validate()

    def _validate(self):
assert (self.signals.index <= self.prices.index.max()).all(), \
    "Signal dates exceed price history — check alignment"
# Signals must be available before the return they predict
# signals at t should predict returns from t to t+1
# i.e., return_t = price[t+1]/price[t] - 1

    # --- Position sizing: long-short equal-weight quartile ---

    def _to_positions(self, signal_row: pd.Series) -> pd.Series:
"""Convert a cross-sectional signal into ±1 weights."""
s = signal_row.dropna()
if len(s) < 4:
    return pd.Series(0.0, index=signal_row.index)
q75 = s.quantile(0.75)
q25 = s.quantile(0.25)
pos = pd.Series(0.0, index=s.index)
n_long = (s >= q75).sum()
n_short = (s <= q25).sum()
pos[s >= q75] = 1.0 / n_long if n_long > 0 else 0
pos[s <= q25] = -1.0 / n_short if n_short > 0 else 0
return pos.reindex(signal_row.index).fillna(0.0)

    def run(self) -> pd.DataFrame:
"""
Execute the backtest.

Returns
-------
results : DataFrame with columns:
    gross_return, net_return, turnover, cumulative_net
"""
cost_per_unit = self.cfg.cost_bps / 10_000

# Forward returns: shift prices back by 1 so ret[t] = price[t+1]/price[t]-1
fwd_ret = self.prices.pct_change().shift(-1)

# Resample signals to desired rebalance frequency
if self.cfg.rebalance_freq != 'D':
    signal_resampled = self.signals.resample(self.cfg.rebalance_freq).last().reindex(
        self.signals.index, method='ffill'
    )
else:
    signal_resampled = self.signals

records = []
prev_weights = pd.Series(0.0, index=self.prices.columns)

for date in signal_resampled.index[:-1]:  # skip last (no fwd return)
    sig = signal_resampled.loc[date]
    weights = self._to_positions(sig)
    ret = fwd_ret.loc[date]

    gross = (weights * ret).sum()
    turnover = (weights - prev_weights).abs().sum()
    net = gross - cost_per_unit * turnover

    records.append({
        'date': date,
        'gross_return': gross,
        'net_return': net,
        'turnover': turnover,
    })
    prev_weights = weights

results = pd.DataFrame(records).set_index('date')
results['cumulative_gross'] = (1 + results['gross_return']).cumprod()
results['cumulative_net'] = (1 + results['net_return']).cumprod()
return results

    # --- Performance metrics ---

    def compute_metrics(self, returns: pd.Series, label: str = '') -> dict:
"""Compute annualized performance metrics from a daily return series."""
rf_daily = (1 + self.cfg.risk_free_rate) ** (1/252) - 1
excess = returns - rf_daily
ann_factor = 252

ann_ret = returns.mean() * ann_factor
ann_vol = returns.std() * np.sqrt(ann_factor)
sharpe = excess.mean() / returns.std() * np.sqrt(ann_factor) if returns.std() > 0 else 0

cum = (1 + returns).cumprod()
rolling_max = cum.cummax()
drawdown = (cum - rolling_max) / rolling_max
max_dd = drawdown.min()
calmar = ann_ret / abs(max_dd) if max_dd != 0 else np.nan

t_stat = sharpe / np.sqrt(1 / len(returns))  # simplified SR t-stat

return {
    'label': label,
    'ann_return': round(ann_ret, 4),
    'ann_vol': round(ann_vol, 4),
    'sharpe': round(sharpe, 3),
    'max_drawdown': round(max_dd, 4),
    'calmar': round(calmar, 3),
    't_stat_sr': round(t_stat, 3),
    'n_obs': len(returns),
}

    # --- Walk-forward validation ---

    def walk_forward_validate(self, n_folds: int = 5) -> pd.DataFrame:
"""
Rolling walk-forward cross-validation.

Splits data into n_folds sequential blocks.
For each fold: train on [0..fold], test on [fold+1].
Returns IS and OOS Sharpe per fold.
"""
results = self.run()
n = len(results)
fold_size = n // (n_folds + 1)

rows = []
for k in range(1, n_folds + 1):
    is_end = k * fold_size
    oos_end = min(is_end + fold_size, n)
    is_ret = results['net_return'].iloc[:is_end]
    oos_ret = results['net_return'].iloc[is_end:oos_end]

    is_sr = is_ret.mean() / is_ret.std() * np.sqrt(252) if is_ret.std() > 0 else 0
    oos_sr = oos_ret.mean() / oos_ret.std() * np.sqrt(252) if oos_ret.std() > 0 else 0

    rows.append({
        'fold': k,
        'is_end_date': results.index[is_end - 1],
        'is_sharpe': round(is_sr, 3),
        'oos_sharpe': round(oos_sr, 3),
        'oos_is_ratio': round(oos_sr / is_sr, 3) if is_sr != 0 else np.nan,
    })

return pd.DataFrame(rows)


# ============================================================
# Demo: Momentum strategy with and without costs
# ============================================================

np.random.seed(42)
n_days, n_stocks = 1500, 50
dates = pd.date_range('2018-01-01', periods=n_days, freq='B')
tickers = [f'S{i:02d}' for i in range(n_stocks)]

# Simulate prices with slight momentum built in
rets = np.random.randn(n_days, n_stocks) * 0.01
prices = pd.DataFrame(
    np.exp(np.cumsum(rets, axis=0)),
    index=dates, columns=tickers
)

# Signal: 12-month momentum (lagged 1 day to avoid look-ahead)
signal = (prices / prices.shift(252) - 1).shift(1)

# Run without costs
cfg_nocost = BacktestConfig(cost_bps=0)
bt_nocost = BacktestEngine(prices, signal, cfg_nocost)
res_nocost = bt_nocost.run()

# Run with realistic costs (10 bps one-way)
cfg_cost = BacktestConfig(cost_bps=10)
bt_cost = BacktestEngine(prices, signal, cfg_cost)
res_cost = bt_cost.run()

metrics_nocost = bt_nocost.compute_metrics(res_nocost['gross_return'], 'No Cost')
metrics_cost = bt_cost.compute_metrics(res_cost['net_return'], 'With Costs (10bps)')

print("=== Performance Comparison ===")
for m in [metrics_nocost, metrics_cost]:
    print(f"\n{m['label']}")
    print(f"  Annualized Return : {m['ann_return']:.2%}")
    print(f"  Sharpe Ratio      : {m['sharpe']:.2f}")
    print(f"  Max Drawdown      : {m['max_drawdown']:.2%}")
    print(f"  Calmar Ratio      : {m['calmar']:.2f}")

print("\n=== Walk-Forward Validation ===")
wf = bt_cost.walk_forward_validate(n_folds=4)
print(wf.to_string(index=False))
```

## Bridge to Quant / ML

**Backtesting is the last gate before capital deployment.** In the ML pipeline, all feature engineering and model training happens to produce a signal. The backtest tests whether that signal, translated into actual trades with realistic costs and constraints, makes money.

**The IS/OOS split in ML vs. backtesting:** ML train/test splits and IS/OOS splits are conceptually identical — both test generalization. The difference is that in finance, **time ordering is sacred**: you can never use future data to train or evaluate, because that's the one direction causality actually runs. Random train-test splits are invalid for sequential financial data.

**The Sharpe ratio as ML metric:** In supervised ML, we optimize cross-entropy or MSE. In backtesting, the analog is the Sharpe ratio of the resulting strategy. A model with better predictive accuracy (RMSE) does not always produce higher Sharpe — the timing and magnitude of errors matters enormously.

**Backtest as adversarial audit:** Once you have a backtest that looks good, your job is to *break it*: find the assumption that, if wrong, destroys performance. Ask: What if costs are 2× higher? What if I can only execute at the next open? What if I remove the last bull market from the sample?

## Self-Assessment

### Level 1 — Conceptual

**Q1.** What is lookahead bias, and why is it so insidious?
> **A:** Lookahead bias occurs when a backtest uses information that wasn't available at the time a decision would have been made (e.g., using end-of-day closing price to generate a signal that supposedly triggers a trade at that same closing price). It's insidious because it's often introduced subtly — e.g., index membership data as of today applied retroactively, or financial statement data before it was actually released.

**Q2.** What is survivorship bias, and what kind of database error causes it?
> **A:** Survivorship bias occurs when the historical universe includes only firms that survived to today, excluding companies that went bankrupt or were delisted. A database built from today's index constituents retroactively will have only "survivors" — making mean-reversion and momentum strategies appear to work better than they do because the worst performers were removed.

**Q3.** What is the difference between a walk-forward test and a traditional train/test split for a trading strategy?
> **A:** A traditional train/test split tests on a single held-out period, which may be unrepresentative. Walk-forward testing rolls the training window forward in time, testing on each successive out-of-sample period, giving a more realistic distribution of performance across different market regimes.

### Level 2 — Quantitative

**Q4.** The Deflated Sharpe Ratio (DSR) adjusts the observed Sharpe for multiple testing. If a fund tests N = 100 strategies and reports the best Sharpe of 1.8, the trials have average Sharpe of 0 and variance of 1, and T = 252 daily observations, what is the minimum benchmark Sharpe for this to be considered statistically significant?
> **A:** The expected maximum Sharpe from N i.i.d. trials is approximately E[max] ≈ Φ⁻¹(1 − 1/N) + other terms. For N=100, Φ⁻¹(0.99) ≈ 2.33, so the benchmark Sharpe is around 2.3+. A reported Sharpe of 1.8 is below this threshold and likely a statistical artifact rather than genuine alpha.

**Q5.** A strategy's backtest shows Sharpe = 2.0 on 2 years of data (T = 504 daily returns). Compute the 95% confidence interval for the true Sharpe ratio, given the standard error formula SE(SR) ≈ √(1/T × (1 + SR²/2)).
> **A:** SE = √(1/504 × (1 + 2.0)) = √(3/504) = √0.00595 ≈ 0.0771. 95% CI = 2.0 ± 1.96 × 0.0771 = [1.849, 2.151]. The interval is relatively tight because 2 years of daily data gives decent power, but a Sharpe of 2.0 for any real strategy should still be viewed skeptically.

### Level 3 — Coding

**Q6.** Implement a walk-forward validation framework: for each fold, train on a window, test on a gap (embargo), and collect out-of-sample performance metrics.

```python
import numpy as np
import pandas as pd
from typing import Callable

def walk_forward_validation(returns: pd.Series, signal_fn: Callable,
                             train_window: int, test_window: int,
                             embargo: int = 5) -> pd.DataFrame:
    """
    Walk-forward backtesting with an embargo gap to prevent leakage.
    
    Parameters
    ----------
    returns     : daily return series
    signal_fn   : function(train_returns) -> signal for test period
    train_window : length of training window (in days)
    test_window  : length of each out-of-sample test window
    embargo     : gap between train end and test start (prevents data leakage)
    
    Returns
    -------
    results : DataFrame with ['fold', 'train_start', 'train_end', 'test_start',
                               'test_end', 'sharpe', 'total_return'] per fold
    """
    # TODO: Implement walk-forward validation:
    # 1. Iterate: fold_start, fold_start + train_window, ..., until end of series
    # 2. For each fold: train on [fold_start : fold_start + train_window]
    # 3. Skip embargo days after train end
    # 4. Test on [train_end + embargo : train_end + embargo + test_window]
    # 5. Compute Sharpe and total return for test period
    # 6. Return DataFrame of results across all folds
    pass
```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| A high backtest Sharpe means the strategy will work live | Backtests systematically overstate expected performance due to lookahead bias, survivorship bias, and overfitting |
| Out-of-sample testing fully validates a strategy | If the strategy was developed using the same broad data universe, even "out-of-sample" may be contaminated by implicit data leakage |
| More data always improves backtesting reliability | Old data may not be representative (regime changes, structural breaks); more data with fewer relevant observations can be worse than shorter, more relevant windows |
| Transaction costs are a minor adjustment | For high-turnover strategies, transaction costs routinely consume 30–100% of gross alpha; they must be modeled explicitly and conservatively |

## Related Concepts

- [[Sharpe Ratio]] — the primary performance metric; understand it before trusting any backtest
- [[Alpha Factor]] — the signal inputs to the backtest
- [[Overfitting and Multiple Testing]] — why a good backtest might still be a false positive
- [[Statistical Arbitrage]] — pairs/cross-sectional strategies with their own backtest subtleties
- [[Monte Carlo Methods]] — Monte Carlo permutation tests complement walk-forward for overfitting diagnosis

## Sources Used

- Lopez de Prado, M. — *Advances in Financial Machine Learning* (2018), ch. 14
- Bailey, D. & Lopez de Prado, M. — *The Deflated Sharpe Ratio* (2014)
- Chan, E. — *Quantitative Trading* (2009), ch. 3
- Jansen, S. — *Machine Learning for Algorithmic Trading* (2020)

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | initial build |
| 2026-04-11 | QA review: removed duplicate/unknown wikilinks ([[Maximum Drawdown]], [[Momentum]]); replaced with [[Monte Carlo Methods]] and [[Sharpe Ratio]] | quality-review |
| 2026-04-18 | Renamed "Implementation (Python)" → "Implementation" for section consistency | review |
