---
type: concept
domain: 60-ML-Finance
tags: [ml-finance, features]
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
> **Chain:** Alpha → Gap 3: Can we find signals that aren't yet crowded into existing factor premia?
> **This concept:** Feature engineering translates the domain knowledge of quantitative finance into the language of machine learning — constructing stationary, informative, non-redundant input features from raw financial data for ML models.
> **Alternative approaches to this gap:** [[Alpha Factor]] (direct factor research), [[Alternative Data]]
> **You need first:** [[Alpha Factor]], [[Alternative Data]], [[Backtesting Methodology]]
> **This unlocks:** [[Regime Detection]], [[Reinforcement Learning Trading]], [[Overfitting and Multiple Testing]]

## Why This Exists

**The gap:** Raw financial data (prices, volumes, fundamentals) is non-stationary, autocorrelated, and in forms that violate assumptions of standard ML models; transforming this data into suitable features is a prerequisite for any supervised or unsupervised ML application.
**What came before:** Direct application of simple technical indicators or fundamental ratios as inputs without systematic treatment of stationarity, cross-sectional normalization, or information leakage — leading to models that look good in-sample but fail out-of-sample.
**What this adds:** A systematic pipeline: fractionally differentiated prices for stationarity with memory preservation; cross-sectional and time-series z-scoring for normalization; structural break detection before feature computation; the triple barrier labeling method for sample generation; meta-labeling to distinguish signal from bet-sizing decisions.
**What it still doesn't solve:** Feature engineering is domain-dependent and requires iteration; most engineered features have significant correlation (multicollinearity), requiring regularization or feature selection; the curse of dimensionality means adding features without rigorous selection can harm performance.

Imagine handing a machine learning model the raw daily closing price of Apple stock — just a column of numbers like 150, 152, 149, 155... What can it actually learn from this? Very little, directly. The raw price carries information, but it's encoded in a way that's practically invisible to most ML algorithms.

The price level is not informative — Apple at \$150 today and Apple at \$150 in 2010 are completely different situations (splits, inflation, market cap changes). The absolute volume traded today means nothing without knowing if that's high or low for that stock. A company's P/E ratio of 20 is cheap in one sector and expensive in another.

Feature engineering is the art and science of transforming raw financial data into signals that ML models can actually learn from. Every choice you make — how to normalize, which transformations to apply, how far back to look, how to handle missing data — determines whether your model finds real patterns or artifacts.

The single most dangerous mistake in financial ML is **look-ahead bias**: accidentally using information that wasn't available at the time of the prediction. A feature that uses next month's earnings to predict this month's return will look brilliant in backtest and be worthless in production.

## Math Concepts

### Stationarity Requirement

ML models assume features are drawn from a stationary distribution (stable mean and variance over time). Raw prices are not stationary — they trend and their scale changes over time.

**Transformations to achieve stationarity:**

| Raw Data | Transformation | Result |
|----------|----------------|--------|
| Price $P_t$ | Log return: $r_t = \log(P_t/P_{t-1})$ | Approximately stationary |
| Volume $V_t$ | Z-score: $(V_t - \mu_V)/\sigma_V$ | Normalized to context |
| Spread | Divide by midprice | Dimensionless relative spread |
| P/E ratio | Cross-sectional z-score by sector | Removes sector baseline |

### Cross-Sectional vs. Time-Series Normalization

**Time-series normalization:** subtract rolling mean, divide by rolling std. Each asset is normalized relative to its own history.

$$\tilde{f}_{i,t} = \frac{f_{i,t} - \mu_i(t, \tau)}{\sigma_i(t, \tau)}$$

Where $\mu_i(t, \tau)$ and $\sigma_i(t, \tau)$ are computed over a window $\tau$.

**Cross-sectional normalization:** at each date, normalize each asset relative to the cross-section of all assets.

$$\tilde{f}_{i,t} = \frac{f_{i,t} - \mu_t(\mathbf{f})}{\sigma_t(\mathbf{f})}$$

For cross-sectional equity prediction (ranking stocks), cross-sectional normalization is essential. For time-series prediction (forecasting one asset), time-series normalization is used.

### Feature Categories

**1. Technical / Price-Volume Features**

Momentum:
$$\text{Mom}(k) = \frac{P_t}{P_{t-k}} - 1$$

Realized volatility over window $\tau$:
$$\sigma_t = \sqrt{\frac{252}{\tau} \sum_{i=1}^{\tau} r_{t-i}^2}$$

RSI (Relative Strength Index):
$$\text{RSI} = 100 - \frac{100}{1 + \frac{\text{avg gain}_{14}}{\text{avg loss}_{14}}}$$

Bollinger Band z-score (how many std from 20-day MA):
$$\text{BB}_t = \frac{P_t - \text{MA}_{20}(P_t)}{\sigma_{20}(P_t)}$$

MACD:
$$\text{MACD} = \text{EMA}_{12}(P) - \text{EMA}_{26}(P)$$
$$\text{Signal} = \text{EMA}_9(\text{MACD})$$

**2. Microstructure Features**

Bid-ask spread:
$$\text{Spread}_t = \frac{\text{Ask}_t - \text{Bid}_t}{\text{Mid}_t}$$

Order flow imbalance (OFI) — net buy vs. sell volume:
$$\text{OFI}_t = \frac{V_t^{buy} - V_t^{sell}}{V_t^{buy} + V_t^{sell}}$$

Amihud illiquidity ratio:
$$\text{ILLIQ}_t = \frac{|r_t|}{V_t}$$

**3. Fundamental Features**

All must be **point-in-time**: use the fiscal period end date + filing delay (e.g., 45 days for 10-Q) to avoid look-ahead bias.

- P/E = Price / Trailing 12m EPS
- P/B = Price / Book value per share
- Earnings surprise = (Actual EPS - Consensus) / |Consensus|
- Sales growth YoY
- Return on equity (ROE)

**4. Alternative Data Features**

- NLP sentiment scores from earnings call transcripts, news
- Web search trends (normalized)
- Credit card transaction growth (from data vendors)
- Satellite imagery (store parking lot counts, oil tank levels)

**5. Derived / Statistical Features**

Hurst exponent (see [[Regime Detection]]):
$$H_t = \text{computed over rolling window}$$

Return autocorrelation:
$$\rho_k = \text{corr}(r_t, r_{t-k})$$

Skewness and kurtosis of return distribution over rolling window.

### Forward-Fill and Alignment

Financial data arrives asynchronously. Fundamental data updates quarterly; price data updates daily. The standard approach:

1. Compute each feature on its native frequency
2. Forward-fill (ffill) to daily frequency — propagate the last known value forward
3. Shift features by at least 1 day (or 1 period) to prevent look-ahead
4. Align all features on the same calendar (using `reindex`)

### Label Construction

For supervised ML, the target label is typically:

**Forward return:** $y_t = r_{t+h} = \log(P_{t+h}/P_t)$

**Metalabeling (Lopez de Prado):** Instead of directly predicting return sign or magnitude, predict whether a primary strategy's signal will be profitable: $y_t \in \{0, 1\}$.

**Triple Barrier Method:** Label each observation with the outcome of the first barrier hit (take-profit, stop-loss, or time-based exit).

## Walkthrough

### Cross-Sectional Equity Alpha Feature Pipeline

Given: daily prices, volumes, quarterly fundamentals for 500 stocks.

Goal: produce a feature matrix for each month-end date, ready for an ML model.

Steps:
1. Compute raw features (momentum, volatility, RSI, P/E) for all stocks
2. Merge price-based (daily) and fundamental (quarterly, forward-filled) data
3. Apply point-in-time constraints (fundamental data lagged by filing delay)
4. Winsorize each feature at 1st/99th percentile
5. Cross-sectional z-score within GICS sector
6. Stack into (dates x stocks x features) array — the feature tensor

Key pitfalls to verify:
- No NaN propagated from incorrect joins
- Fundamental features are filed at $t-45$ days minimum
- No prices from after the prediction date used in any feature

## Analysis

**The most common mistakes:**

1. **Look-ahead bias:** Using `df.shift(-1)` backwards — putting tomorrow's price into today's feature. Even subtle forms: using survival-bias-free price history but only backtesting on current index constituents.

2. **Survivorship bias:** Only training on stocks that are in the index today. Stocks that went bankrupt or were delisted are excluded, making every strategy look better.

3. **Non-stationarity leakage:** Using raw P/E level as a feature without sector-neutralization. The feature encodes sector (tech has high P/E) more than individual stock signal.

4. **Data snooping:** Generating 200 features, testing all, and reporting only the best ones without multiple-testing correction.

5. **Point-in-time failure:** Quarterly earnings are often restated. Using restated data (as-of today's Compustat) rather than as-reported data inflates backtest returns.

**Feature importance ≠ predictive power:** Tree-based feature importance can be misleading for correlated features (see Strobl et al.). Use permutation importance or SHAP values instead.

**The feature-engineering treadmill:** As more quants use the same features, alpha decays. Good feature engineering requires either finding new data sources (alternative data) or computing existing data in novel ways.

## Implementation

```python
import numpy as np
import pandas as pd
from scipy import stats

# ============================================================
# Full Feature Engineering Pipeline for Cross-Sectional Equity
# ============================================================

class FinancialFeaturePipeline:
    """
    Constructs a panel of financial features for cross-sectional
    equity ML with proper temporal alignment and normalization.
    """

    def __init__(self, winsor_quantile: float = 0.01):
self.winsor_q = winsor_quantile

    # --- Technical features ---

    def momentum(self, prices: pd.DataFrame,
         lookback: int = 252, skip: int = 21) -> pd.DataFrame:
"""12-1 month momentum (skip most recent month)."""
return prices.shift(skip) / prices.shift(lookback) - 1

    def realized_vol(self, prices: pd.DataFrame, window: int = 21) -> pd.DataFrame:
"""Annualized realized volatility over rolling window."""
log_ret = np.log(prices / prices.shift(1))
return log_ret.rolling(window).std() * np.sqrt(252)

    def rsi(self, prices: pd.DataFrame, period: int = 14) -> pd.DataFrame:
"""Relative Strength Index."""
delta = prices.diff()
gain = delta.clip(lower=0).rolling(period).mean()
loss = (-delta.clip(upper=0)).rolling(period).mean()
rs = gain / loss.replace(0, np.nan)
return 100 - 100 / (1 + rs)

    def bollinger_zscore(self, prices: pd.DataFrame, window: int = 20) -> pd.DataFrame:
"""How many std deviations from rolling mean."""
ma = prices.rolling(window).mean()
std = prices.rolling(window).std()
return (prices - ma) / std.replace(0, np.nan)

    def macd_signal(self, prices: pd.DataFrame,
            fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
"""MACD signal line."""
ema_fast = prices.ewm(span=fast, adjust=False).mean()
ema_slow = prices.ewm(span=slow, adjust=False).mean()
macd = ema_fast - ema_slow
return macd - macd.ewm(span=signal, adjust=False).mean()

    def amihud_illiquidity(self, prices: pd.DataFrame,
                   volumes: pd.DataFrame, window: int = 21) -> pd.DataFrame:
"""
Amihud (2002) illiquidity: |return| / dollar volume.
Higher = less liquid = harder to trade.
"""
log_ret = np.log(prices / prices.shift(1)).abs()
dollar_vol = prices * volumes
daily_illiq = log_ret / dollar_vol.replace(0, np.nan)
return daily_illiq.rolling(window).mean() * 1e6   # scale for readability

    # --- Fundamental features (with look-ahead protection) ---

    def merge_fundamentals(self,
                    price_dates: pd.DatetimeIndex,
                    fund_df: pd.DataFrame,
                    filing_lag_days: int = 45) -> pd.DataFrame:
"""
Merge quarterly fundamentals into daily panel with proper filing lag.

Parameters
----------
price_dates     : daily trading calendar
fund_df         : DataFrame with columns [ticker, fiscal_end_date, pe_ratio, roe, ...]
filing_lag_days : minimum days after fiscal period end before data is available

Returns
-------
daily_fund : DataFrame (dates x tickers x fundamental features)
"""
# Shift fundamental data availability by filing lag
fund_df = fund_df.copy()
fund_df['available_date'] = fund_df['fiscal_end_date'] + pd.Timedelta(days=filing_lag_days)

# For each ticker, create a daily time-series by forward-filling
result_frames = {}
for ticker, group in fund_df.groupby('ticker'):
    group = group.set_index('available_date').sort_index()
    # Reindex to daily, forward-fill (never look ahead)
    daily = group.reindex(price_dates, method='ffill')
    result_frames[ticker] = daily

return pd.concat(result_frames, axis=1)

    # --- Normalization ---

    def winsorize(self, df: pd.DataFrame) -> pd.DataFrame:
"""Clip at winsor_q / (1 - winsor_q) percentiles cross-sectionally."""
def _clip_row(row):
    lo = row.quantile(self.winsor_q)
    hi = row.quantile(1 - self.winsor_q)
    return row.clip(lo, hi)
return df.apply(_clip_row, axis=1)

    def cross_sectional_zscore(self, df: pd.DataFrame) -> pd.DataFrame:
"""Normalize each row (date) to mean=0, std=1."""
return df.apply(lambda row: (row - row.mean()) / row.std(), axis=1)

    def sector_zscore(self, df: pd.DataFrame, sectors: pd.Series) -> pd.DataFrame:
"""Z-score within sector to remove sector-level effects."""
result = df.copy()
for date in df.index:
    row = df.loc[date].dropna()
    for sector in sectors[row.index].unique():
        mask = sectors[row.index] == sector
        tickers = row.index[mask]
        sector_vals = row[tickers]
        if sector_vals.std() > 0:
            result.loc[date, tickers] = (
                (sector_vals - sector_vals.mean()) / sector_vals.std()
            )
return result

    # --- Pipeline runner ---

    def build_feature_matrix(self,
                      prices: pd.DataFrame,
                      volumes: pd.DataFrame,
                      sectors: pd.Series) -> dict:
"""
Build the full feature matrix.

Returns dict of feature_name -> normalized DataFrame (dates x tickers).
"""
features = {}

raw = {
    'momentum_12_1':    self.momentum(prices),
    'realized_vol_21':  self.realized_vol(prices),
    'rsi_14':           self.rsi(prices),
    'bollinger_z':      self.bollinger_zscore(prices),
    'macd_signal':      self.macd_signal(prices),
    'amihud_illiq':     self.amihud_illiquidity(prices, volumes),
}

for name, raw_feat in raw.items():
    # 1. Shift by 1 day to prevent look-ahead (predict t+1 using t features)
    feat = raw_feat.shift(1)
    # 2. Winsorize
    feat = self.winsorize(feat)
    # 3. Sector z-score
    feat = self.sector_zscore(feat, sectors)
    features[name] = feat

return features


# --- Diagnostic: check for look-ahead bias ---

def check_lookahead(feature: pd.DataFrame, forward_return: pd.DataFrame,
            lag: int = 0) -> float:
    """
    Check for unintended look-ahead by correlating feature at t with
    returns at t-lag (if this correlation is high, there's a problem).
    """
    shifted_ret = forward_return.shift(lag)
    ics = []
    for date in feature.index[252:]:
try:
    f = feature.loc[date].dropna()
    r = shifted_ret.loc[date].dropna()
    common = f.index.intersection(r.index)
    if len(common) < 20:
        continue
    ic, _ = stats.spearmanr(f[common], r[common])
    ics.append(ic)
except Exception:
    continue
    return np.nanmean(ics)


# Quick sanity demo (synthetic data)
np.random.seed(0)
n_d, n_s = 600, 50
dates   = pd.date_range('2022-01-01', periods=n_d, freq='B')
tickers = [f'S{i:02d}' for i in range(n_s)]
prices  = pd.DataFrame(
    np.exp(np.cumsum(np.random.randn(n_d, n_s) * 0.01, axis=0)),
    index=dates, columns=tickers
)
volumes = pd.DataFrame(
    np.random.lognormal(15, 0.5, (n_d, n_s)),
    index=dates, columns=tickers
)
sectors = pd.Series(
    np.random.choice(['Tech', 'Fin', 'Health'], n_s),
    index=tickers
)

pipeline = FinancialFeaturePipeline()
features = pipeline.build_feature_matrix(prices, volumes, sectors)

print("Feature matrix shapes:")
for name, feat in features.items():
    non_nan = feat.notna().sum().sum()
    print(f"  {name}: {feat.shape}, valid cells: {non_nan}")
```

## Bridge to Quant / ML

**Features as alpha factors:** The normalized, sector-neutralized technical features described here are exactly the [[Alpha Factor]] inputs. Feature engineering and factor construction are the same process — different vocabularies for the same activity.

**Tree models vs. linear models:** Gradient boosting (XGBoost, LightGBM) handles correlated features and nonlinear interactions well. Linear models (ridge regression, Lasso) require more careful feature orthogonalization. PCA/ICA on the factor set is a common preprocessing step for linear models.

**Time-series cross-validation:** Never use a random train-test split on financial data. Use **expanding window** or **walk-forward** cross-validation: train on 2000-2010, test on 2011; train on 2000-2011, test on 2012; etc. Random splits cause data leakage from future to past.

**Feature decay:** Technical features based on price and volume are increasingly commoditized. The edge is in alternative data (satellite, NLP, credit card) and in novel feature combinations. Monitor IC decay over time — a falling ICIR signals that a feature is being arbitraged away.

**Regime conditioning:** The same feature may have different predictive power in different regimes. Interactions between [[Regime Detection]] regime labels and features are powerful — e.g., momentum × (1 if bull regime) — and capture regime-conditional alpha.

## Self-Assessment

### Level 1 — Conceptual

**Q1.** Why is raw price an unsuitable feature for most ML models, and what transformation makes it suitable?
> **A:** Raw price is non-stationary (has a unit root) — a model trained on prices from \$50–\$100 may not generalize to prices at \$200. First differences (log returns) achieve stationarity but lose long-range memory. Fractional differentiation (order d between 0 and 1) balances stationarity with memory preservation — the key innovation from Lopez de Prado.

**Q2.** What is "information leakage" in feature engineering and how does the embargo technique prevent it?
> **A:** Information leakage occurs when features computed on overlapping windows contaminate train/test splits — e.g., a 20-day rolling feature at the test start date includes data from the training period. Embargo adds a gap between training end and test start equal to the feature lookback window, ensuring no overlapping data contaminates out-of-sample evaluation.

**Q3.** What is meta-labeling in Lopez de Prado's framework, and why is it more sophisticated than standard labeling?
> **A:** Meta-labeling decouples the direction prediction (from a primary model) from the position-sizing decision. A secondary meta-label model learns when to act on the primary signal and how large to size the position. This addresses the fact that a signal may have high accuracy but variable effect size — sizing conservatively when the model is uncertain improves risk-adjusted returns.

### Level 2 — Quantitative

**Q4.** You compute a 20-day rolling mean return as a feature. If you have N=500 training samples and your test starts immediately after, what is the minimum embargo period needed, and how many effective training samples does this cost you?
> **A:** Minimum embargo = 20 days (the feature lookback). You lose 20 samples from the end of training (to create the gap) + any samples whose labels overlap with the embargo period. For daily data, this removes roughly 20-40 samples from training. At N=500, this is a 4-8% cost — significant for small datasets.

**Q5.** A momentum feature (12-month log return) has IC = 0.06 against 1-month forward returns. A volume-normalized momentum feature (12-month return / trailing vol) has IC = 0.09. What does this improvement suggest, and what risk does the normalization introduce?
> **A:** The vol-normalization improves IC by adjusting for varying signal magnitude across stocks — high-vol stocks have larger raw returns but not necessarily more predictive momentum. The improvement suggests risk-adjusting the feature removes noise. Risk: vol estimates have their own estimation error, especially for recent regime changes; the normalized feature may have higher parameter sensitivity.

### Level 3 — Coding

**Q6.** Implement fractional differentiation for a price series: compute the weights for fractional differencing order d and apply to generate a stationary but memory-preserving feature.

```python
import numpy as np
import pandas as pd

def fractional_diff(series: pd.Series, d: float,
                    threshold: float = 1e-5) -> pd.Series:
    """
    Apply fractional differentiation to preserve memory while achieving stationarity.
    
    Parameters
    ----------
    series    : time series of prices (or any non-stationary series)
    d         : differentiation order (0 < d < 1 for fractional; d=1 is standard diff)
    threshold : minimum weight magnitude — truncates the infinite weight series
    
    Returns
    -------
    fracdiff_series : fractionally differentiated series (same index, NaN at start)
    """
    # TODO: Implement fractional differentiation:
    # 1. Compute weights: w_k = product_{j=0}^{k-1} (d - j) / (j + 1), for k = 0, 1, 2, ...
    #    w_0 = 1, w_k = w_{k-1} * (d - k + 1) / k
    # 2. Stop when |w_k| < threshold (weights decay for 0 < d < 1)
    # 3. Apply weights as convolution: fracdiff[t] = sum_k w_k * series[t-k]
    # 4. Return series with NaN for initial observations where window is incomplete
    pass
```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| More features always improve model performance | More features increase the curse of dimensionality and overfitting risk; feature selection is as important as feature creation |
| Z-scoring features is always appropriate | Cross-sectional z-scoring is appropriate for cross-sectional signals; time-series z-scoring is appropriate for absolute-level features; mixing these introduces errors |
| Standard train/test splits work for financial time series | Overlapping features and autocorrelated returns require purging and embargo — standard k-fold CV is biased in financial settings |
| Feature importance from tree models identifies real alpha | Feature importance measures in-sample correlation; features that appear important may be overfitted to noise; validate with out-of-sample IC |

## Related Concepts

- [[Alpha Factor]] — factor construction is a special case of feature engineering
- [[Regime Detection]] — regime labels as features; regime-conditional normalization
- [[Reinforcement Learning Trading]] — features are the state representation for the RL agent
- [[Overfitting and Multiple Testing]] — feature selection from large sets is itself a multiple testing problem

## Sources Used

- Lopez de Prado, M. - *Advances in Financial Machine Learning* (2018), ch. 4-8
- Kakushadze, Z. & Serur, J. - *151 Trading Strategies* (2018)
- Amihud, Y. - *Illiquidity and Stock Returns* (2002)

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review: replaced unknown wikilink [[Yield Curve]] with [[Overfitting and Multiple Testing]] | quality-review |
