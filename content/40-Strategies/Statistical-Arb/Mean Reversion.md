---
type: concept
domain: 40-Strategies
tags: [strategy, equity]
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
> **Chain:** Alpha → Gap 1: Is there any evidence of persistent, tradeable patterns?
> **This concept:** Mean reversion documents the short-horizon tendency for prices to reverse toward their equilibrium level — the statistical counterpart to momentum and the foundation for spread-based strategies.
> **Alternative approaches to this gap:** [[Momentum]], [[Pairs Trading]]
> **You need first:** [[Ornstein-Uhlenbeck Process]]
> **This unlocks:** [[Pairs Trading]], [[Statistical Arbitrage]], [[Market Making]]

## Why This Exists

**The gap:** Practitioners needed a rigorous statistical basis for the intuition that stretched prices snap back — and a way to parameterize how quickly, so they could decide whether the reversion was fast enough to trade.
**What came before:** Ad hoc relative-value intuition — traders observed that overextended stocks tended to pull back but had no systematic way to measure reversion speed, set entry/exit thresholds, or construct market-neutral positions.
**What this adds:** The Ornstein-Uhlenbeck model formalizes the reversion process with a speed parameter κ and equilibrium level μ; the half-life formula t₁/₂ = ln(2)/κ tells you whether reversion is fast enough to trade; the Hurst exponent provides a model-free test for mean-reverting behavior (H < 0.5).
**What it still doesn't solve:** Mean reversion can break down permanently (structural breaks, regime changes); the OU parameters estimated historically may not hold out-of-sample; high-frequency reversion is easily crowded out by transaction costs.

Imagine a rubber band stretched between two posts. The further you pull it, the harder it pulls back toward the center. Mean reversion in prices works the same way: when a price moves far from its "natural" level, forces tend to bring it back.

Think about a company's stock price relative to its earnings. If the stock gets wildly overpriced (stretched rubber band), investors sell, analysts downgrade, and momentum slows — pulling the price back down. If it gets too cheap, value investors swoop in, buying it back up. This is mean reversion in a fundamental sense.

But mean reversion shows up in much more mechanical contexts too:
- **Intraday price bounces:** A large sell order temporarily pushes the price below fair value. Market makers and algorithms immediately buy, snapping it back.
- **Volatility mean reversion:** The VIX (fear index) spikes during market panics, then reliably drifts back down to its long-run average.
- **Yield spreads:** Credit spreads between corporate and government bonds widen during risk-off periods, then compress again.
- **Pairs spreads:** The price difference between two related stocks tends to revert (see [[Pairs Trading]]).

The key practical question is: *how fast does it revert?* If it takes 2 years, it's not very tradeable. If it takes 2 days, there's an exploitable signal. The **half-life** of mean reversion tells you this.

## Math Concepts

**Ornstein-Uhlenbeck (OU) Process — the canonical mean-reverting model**

$$dX_t = \kappa(\mu - X_t)\,dt + \sigma\,dW_t$$

| Term | Meaning |
|------|---------|
| $X_t$ | Price (or spread, or log-price) |
| $\kappa > 0$ | Mean-reversion speed — how quickly $X$ is pulled back to $\mu$ |
| $\mu$ | Long-run mean |
| $\sigma$ | Volatility (randomness) |
| $dW_t$ | Standard Brownian motion increment |

In discrete time (daily data):

$$X_t - X_{t-1} = \kappa(\mu - X_{t-1})\Delta t + \sigma\sqrt{\Delta t}\,\varepsilon_t, \quad \varepsilon_t \sim N(0,1)$$

Rearranged as an AR(1) regression:

$$\Delta X_t = a + b X_{t-1} + \varepsilon_t$$

where $b = -\kappa\Delta t$ (negative $b$ = mean-reverting), $a = \kappa \mu \Delta t$.

**Half-life of mean reversion:**

$$t_{1/2} = \frac{\ln 2}{\kappa} = \frac{-\ln 2}{b / \Delta t}$$

Interpretation: on average, half the distance to the mean is closed every $t_{1/2}$ periods.

**Hurst Exponent — diagnostic for mean reversion vs. trending**

The Hurst exponent $H$ characterizes the "memory" of a time series:

| $H$ | Behavior |
|-----|---------|
| $H < 0.5$ | Mean-reverting (anti-persistent) |
| $H = 0.5$ | Random walk (no memory) |
| $H > 0.5$ | Trending (persistent) |

**Estimation via R/S analysis (Rescaled Range):**

For a time series of $n$ observations, compute the rescaled range $R/S$. Under self-similarity:

$$E[R_n/S_n] \approx C \cdot n^H$$

Taking logs: $\ln(R_n/S_n) = \ln C + H \ln n$

Run this regression at multiple time lags $n$ to estimate $H$.

**Variance Ratio Test (alternative Hurst measure):**

$$V(q) = \frac{\text{Var}(X_{t+q} - X_t) / q}{\text{Var}(X_{t+1} - X_t)}$$

- $V(q) < 1$: mean-reverting
- $V(q) = 1$: random walk
- $V(q) > 1$: trending

**ADF Test for stationarity:**

The Augmented Dickey-Fuller test directly tests whether $b = 0$ (null: unit root / random walk) vs. $b < 0$ (mean-reverting). Rejecting the null (p < 0.05) confirms mean reversion.

**Stationary distribution of OU:**

The long-run distribution of $X_t$ is:

$$X_t \sim N\!\left(\mu, \frac{\sigma^2}{2\kappa}\right)$$

This gives the "equilibrium" spread — the range in which the process spends most of its time.

## Walkthrough

**Example: Intraday price mean reversion for a large-cap stock**

You track the 1-minute mid-price of Apple (AAPL) during a single trading day. The stock opens at \$185. You observe the following sequence:

| Time | Price | Deviation from $\mu=185$ | Expected next move |
|------|-------|--------------------------|-------------------|
| 9:30 | 185.00 | 0.00 | None |
| 9:35 | 185.40 | +0.40 | Small down |
| 9:40 | 185.90 | +0.90 | Larger down |
| 9:45 | 186.30 | +1.30 | Strong down signal |
| 9:50 | 185.70 | +0.70 | Still above mean |
| 9:55 | 185.20 | +0.20 | Near mean |
| 10:00 | 185.05 | +0.05 | Essentially reverted |

The price drifted 1.3% above the mean. Mean reversion pulled it back over 25 minutes. The half-life in this example is roughly 15 minutes.

**Fitting the OU model:**

Regress $\Delta X_t$ on $X_{t-1}$ using intraday data:

```
ΔX_t = 0.025 - 0.038 * X_{t-1} + ε_t
     (a=0.025, b=-0.038)
```

$\kappa = -b/\Delta t = 0.038 / (1/390) = 14.8$ per day (390 minutes in a trading day).

Half-life $= \ln(2) / 14.8 \approx 0.047$ days $\approx 11$ minutes. Consistent with the walkthrough above.

**Hurst exponent calculation (same data):**

Computed R/S at lags [10, 20, 50, 100, 200] minutes gives $H \approx 0.31$ — clearly in the mean-reverting regime ($H < 0.5$).

## Analysis

**When does mean reversion fail?**

- **Structural breaks / regime changes:** Interest rate mean reversion worked for decades, then broke during the 2008-2015 period as rates approached zero lower bound. The "long-run mean" shifted permanently. Regularly re-estimate $\mu$ over a rolling window.
- **Fundamental news:** A price that looks like mean reversion might actually be price discovery — the market correctly re-rating the stock. Always think about *why* a price is deviating before assuming it will revert.
- **Illiquidity premium:** In illiquid markets, apparent mean reversion can be a stale-price artifact rather than a real signal.
- **Slow reversion:** If the half-life is 6 months, the strategy requires massive capital to be deployed for a long time. The expected return per unit of capital deployed can be unattractive.

**Time horizon matters dramatically:**
- Minutes-to-hours: strongest mean reversion signal (driven by order flow imbalances and market microstructure)
- Days-to-weeks: moderate, driven by fundamentals and sentiment extremes
- Months-to-years: weak, risks of regime change outweigh the signal

**Mean reversion vs. momentum — the same coin:**

These aren't opposites; they operate at different timescales on the same instruments:
- Short-term (< 1 week): mean-reverting
- Medium-term (1 month – 12 months): momentum
- Long-term (> 3-5 years): value/mean-reverting again

A good quant model can exploit both.

## Implementation

```python
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant

# ------------------------------------------------------------------
# 1. Simulate an OU process for demonstration
# ------------------------------------------------------------------
np.random.seed(42)

kappa_true  = 0.15   # mean-reversion speed per day
mu_true     = 100.0  # long-run mean
sigma_true  = 1.5    # volatility
dt          = 1.0    # daily timestep
n           = 500    # 500 trading days (~2 years)

X = np.zeros(n)
X[0] = mu_true

for t in range(1, n):
    drift = kappa_true * (mu_true - X[t-1]) * dt
    shock = sigma_true * np.sqrt(dt) * np.random.normal()
    X[t]  = X[t-1] + drift + shock

series = pd.Series(X, name='price')

# ------------------------------------------------------------------
# 2. ADF test — confirm mean reversion
# ------------------------------------------------------------------
adf_result = adfuller(series, autolag='AIC')
print(f"ADF Statistic: {adf_result[0]:.4f}")
print(f"ADF p-value:   {adf_result[1]:.4f}  "
      f"{'Mean-reverting (reject unit root)' if adf_result[1] < 0.05 else 'Random walk'}")

# ------------------------------------------------------------------
# 3. Fit OU parameters via AR(1) regression
# ------------------------------------------------------------------
delta_X = series.diff().dropna()
X_lag   = series.shift(1).dropna()

reg = OLS(delta_X, add_constant(X_lag)).fit()
a   = reg.params['const']
b   = reg.params['price']

kappa_est  = -b / dt
mu_est     = a / (kappa_est * dt)
sigma_est  = reg.resid.std() / np.sqrt(dt)
half_life  = np.log(2) / kappa_est

print(f"\nOU parameter estimates:")
print(f"  kappa (reversion speed): {kappa_est:.4f}  (true: {kappa_true})")
print(f"  mu (long-run mean):      {mu_est:.4f}  (true: {mu_true})")
print(f"  sigma (volatility):      {sigma_est:.4f}  (true: {sigma_true})")
print(f"  half-life:               {half_life:.2f} days")

# ------------------------------------------------------------------
# 4. Hurst exponent via R/S analysis
# ------------------------------------------------------------------
def hurst_rs(ts, min_lag=10, max_lag=None, n_lags=20):
    """
    Estimate Hurst exponent via Rescaled Range (R/S) analysis.
    Returns H and the (log_n, log_rs) arrays used in the regression.
    """
    ts = np.array(ts)
    if max_lag is None:
        max_lag = len(ts) // 2

    lags = np.unique(np.logspace(
        np.log10(min_lag), np.log10(max_lag), n_lags
    ).astype(int))

    rs_values = []
    for lag in lags:
        # Split series into non-overlapping sub-series of length lag
        n_windows = len(ts) // lag
        if n_windows < 2:
            continue
        rs_list = []
        for w in range(n_windows):
            sub = ts[w * lag:(w + 1) * lag]
            mean_sub = sub.mean()
            deviation = np.cumsum(sub - mean_sub)
            R = deviation.max() - deviation.min()
            S = sub.std(ddof=1)
            if S > 0:
                rs_list.append(R / S)
        if rs_list:
            rs_values.append((lag, np.mean(rs_list)))

    if len(rs_values) < 4:
        return None, None, None

    lags_arr = np.array([x[0] for x in rs_values])
    rs_arr   = np.array([x[1] for x in rs_values])

    log_lags = np.log(lags_arr)
    log_rs   = np.log(rs_arr)

    reg_rs = OLS(log_rs, add_constant(log_lags)).fit()
    H = reg_rs.params[1]

    return H, log_lags, log_rs

H, log_lags, log_rs = hurst_rs(series.values)
label = "Mean-reverting" if H < 0.45 else ("Trending" if H > 0.55 else "Random walk")
print(f"\nHurst exponent H: {H:.4f}  ({label})")

# ------------------------------------------------------------------
# 5. Variance ratio test at multiple horizons
# ------------------------------------------------------------------
def variance_ratio(series, q):
    """VR(q) = Var(q-period return) / (q * Var(1-period return))"""
    ret1  = series.diff().dropna()
    retq  = series.diff(q).dropna()
    vr    = (retq.var() / q) / ret1.var()
    return vr

print("\nVariance ratio test:")
for q in [2, 5, 10, 20, 40]:
    vr = variance_ratio(series, q)
    direction = "mean-rev" if vr < 0.95 else ("trending" if vr > 1.05 else "random")
    print(f"  VR({q:2d}) = {vr:.4f}  [{direction}]")

# ------------------------------------------------------------------
# 6. Simple mean-reversion trading signal
# ------------------------------------------------------------------
lookback = 30
mu_roll    = series.rolling(lookback).mean()
sigma_roll = series.rolling(lookback).std()
zscore     = (series - mu_roll) / sigma_roll

# Signal: long when z < -1.5, short when z > +1.5, exit at 0
position = pd.Series(0.0, index=series.index)
pos = 0
for i in range(lookback, len(zscore)):
    z = zscore.iloc[i]
    if pos == 0:
        if z < -1.5:
            pos = 1
        elif z > 1.5:
            pos = -1
    elif pos == 1 and z >= 0:
        pos = 0
    elif pos == -1 and z <= 0:
        pos = 0
    position.iloc[i] = pos

daily_ret  = series.diff()
strat_ret  = position.shift(1) * daily_ret
cum_pnl    = strat_ret.cumsum()
sharpe     = strat_ret.mean() / strat_ret.std() * np.sqrt(252)

print(f"\nMean-reversion strategy Sharpe: {sharpe:.2f}")
print(f"Cumulative P&L: {cum_pnl.iloc[-1]:.4f}")
```

## Self-Assessment

Work through these before looking at the answers.

---

### Level 1 — Conceptual

**Q1.** In the OU equation $dX_t = \kappa(\mu - X_t)\,dt + \sigma\,dW_t$, what happens to the process if $\kappa = 0$? What if $\kappa < 0$?

<details>
<summary>Answer</summary>

- **$\kappa = 0$:** The drift term disappears completely: $dX_t = \sigma\,dW_t$. This is a pure Brownian motion — a random walk with no tendency to revert. The process has no memory and wanders indefinitely. There is no trading signal.

- **$\kappa < 0$:** The drift term *amplifies* deviations instead of correcting them: $dX_t = |\kappa|(X_t - \mu)\,dt + \sigma\,dW_t$. The further $X$ is from $\mu$, the harder it gets pushed *away*. This is an explosive, unstable process that diverges to $\pm\infty$. In practice, a price series with estimated $\hat{b} > 0$ in the AR(1) regression means you shouldn't trade it for mean reversion.

The key requirement is $\kappa > 0$ (equivalently $b < 0$ in the AR(1)), which is exactly what the ADF test checks.

</details>

---

**Q2.** The Hurst exponent and the ADF test both detect mean reversion. When would you prefer one over the other?

<details>
<summary>Answer</summary>

**ADF test:**
- Tests a specific null hypothesis: "the series has a unit root (random walk)." Binary outcome: reject or don't reject.
- Works best for detecting *cointegrated* or *strongly stationary* series.
- Gives a clean p-value, but it's sensitive to the choice of lags and can have low power in short samples.

**Hurst exponent:**
- Measures the *degree* of mean reversion on a continuous scale ($H \in (0,1)$). Tells you not just *whether* a series is mean-reverting but *how strongly*.
- Better for comparing two mean-reverting series ("$H=0.3$ is much more strongly mean-reverting than $H=0.45$").
- Useful for long-memory processes where ADF (which tests short-memory structure) may give misleading results.
- More robust over short windows but estimates can be noisy.

**In practice:** run both. Use ADF for the binary go/no-go decision (is this tradeable?) and use $H$ for ranking and comparing candidates (which pairs/instruments are *most* mean-reverting?).

</details>

---

**Q3.** You observe a stock whose price has been above its 60-day moving average for 45 consecutive days. A colleague says "it must revert soon — it's been up there for so long." What is wrong with this reasoning?

<details>
<summary>Answer</summary>

This is the **gambler's fallacy** applied to markets. A random walk has no memory — the probability of reverting tomorrow is the same regardless of how long the price has been elevated. Time spent above the mean is *not* evidence of imminent reversion.

For true mean reversion (OU process), the *magnitude* of the deviation matters, not the *duration*. The reversion force is proportional to $\kappa(\mu - X_t)$: a large deviation creates a strong pull, a small deviation creates a weak pull. If the stock has been 1% above the mean for 45 days, the pull is still only proportional to that 1% gap.

Before assuming reversion, you must check: (a) is the series actually mean-reverting (ADF)? (b) has the long-run mean $\mu$ itself shifted upward (regime change)? Forty-five days above the mean might simply mean the equilibrium moved.

</details>

---

**Q4.** What is the relationship between the ADF test and the OLS AR(1) regression $\Delta X_t = a + bX_{t-1} + \varepsilon_t$? Specifically, what quantity is the ADF test statistic, and what is its null hypothesis?

<details>
<summary>Answer</summary>

The ADF test statistic is the **t-statistic on the coefficient $b$** from the OLS regression $\Delta X_t = a + bX_{t-1} + \varepsilon_t$ (plus augmentation lags for serial correlation).

- **Null hypothesis ($H_0$): $b = 0$** — the series is a random walk (unit root). No mean reversion.
- **Alternative ($H_1$): $b < 0$** — the series is mean-reverting (stationary). $b < 0$ means past deviations are corrected.

The ADF distribution is *not* a standard t-distribution under $H_0$ (because you're testing a unit root, which puts you at the boundary of the stationarity region). Special critical values (Dickey-Fuller tables) must be used. Importantly: a larger negative ADF statistic is *stronger* evidence of mean reversion, even though you're comparing against a non-standard distribution.

</details>

---

### Level 2 — Quantitative

**Q5.** You run the AR(1) regression and get $a = 0.30$, $b = -0.06$, with $\Delta t = 1$ day.

a) What is $\kappa$?
b) What is the long-run mean $\mu$?
c) What is the half-life?
d) If $X_t = 106$ and $\mu = 100$, what is the expected value of $X_{t+1}$?

<details>
<summary>Answer</summary>

**a)** $\kappa = -b/\Delta t = 0.06$ per day.

**b)** From $a = \kappa\mu\Delta t$: $\mu = a/(\kappa \Delta t) = 0.30/(0.06 \times 1) = 5.0$.

Wait — $\mu = 5$? That seems low for a price. This is correct mathematically given $a=0.30$, $\kappa=0.06$. In practice, $\mu$ is often estimated directly as the sample mean of $X_t$ rather than from the regression coefficients, because the regression intercept absorbs level effects. The regression is primarily used to estimate $\kappa$ (the speed, $b$) not $\mu$ (the level, derived from $a$). Use $\mu = \bar{X}$ from the data directly.

**c)** $t_{1/2} = \ln(2)/\kappa = 0.693/0.06 \approx 11.6$ trading days.

**d)** Expected next value:
$$E[X_{t+1}] = X_t + \kappa(\mu - X_t)\Delta t = 106 + 0.06 \times (100 - 106) \times 1 = 106 - 0.36 = 105.64$$

The model predicts the price will fall by 0.36 units — pulled toward $\mu = 100$.

</details>

---

**Q6.** The stationary distribution of an OU process is $X_t \sim N(\mu, \sigma^2/2\kappa)$. Given $\mu = 100$, $\sigma = 2.0$, $\kappa = 0.10$:

a) What is the long-run variance?
b) Within what price range would you expect the process to spend 95% of its time?
c) If you enter a mean-reversion trade when $X_t = 104$, what is the probability (in long-run terms) that the process is at or above 104?

<details>
<summary>Answer</summary>

**a)** Long-run variance: $\sigma^2_\infty = \sigma^2/(2\kappa) = 4.0/(0.20) = 20.0$. Long-run std dev = $\sqrt{20} \approx 4.47$.

**b)** 95% interval: $\mu \pm 1.96 \times \sigma_\infty = 100 \pm 1.96 \times 4.47 = [91.2, 108.8]$.

**c)** Z-score of $X=104$: $z = (104 - 100)/4.47 = 0.895$.
$P(X \geq 104) = 1 - \Phi(0.895) \approx 1 - 0.815 = 18.5\%$.

So 104 is not a particularly extreme value for this process. You might want to wait for a more extreme deviation — say $z > 1.5$ or $z > 2$ — before entering. At $z = 2$: $X = 100 + 2 \times 4.47 = 108.9$, $P(X \geq 108.9) \approx 2.3\%$ — a genuinely unusual event.

</details>

---

### Level 3 — Coding

**Q7.** The Hurst exponent implementation above uses R/S analysis. Write a brief explanation of what each of the following steps does and *why*:

```python
sub = ts[w * lag:(w + 1) * lag]
mean_sub = sub.mean()
deviation = np.cumsum(sub - mean_sub)
R = deviation.max() - deviation.min()
S = sub.std(ddof=1)
```

<details>
<summary>Answer</summary>

```python
sub = ts[w * lag:(w + 1) * lag]
# Takes a non-overlapping sub-window of length `lag`.
# We repeat this for multiple windows and average, reducing estimation noise.

mean_sub = sub.mean()
# The mean of the sub-series. We subtract this to make the sub-series zero-mean
# before computing the cumulative sum — this is the "de-meaned" series.

deviation = np.cumsum(sub - mean_sub)
# Cumulative sum of de-meaned values. This is the "cumulative deviation" from the mean.
# If the series is trending (persistent), this will drift far from zero.
# If the series is mean-reverting, it will oscillate back and forth near zero.

R = deviation.max() - deviation.min()
# Range of the cumulative deviation = how far the series "explored" from its mean.
# A random walk grows as sqrt(lag); a mean-reverting series grows slower.

S = sub.std(ddof=1)
# Standard deviation of the raw sub-series, used to normalize R.
# R/S removes the effect of volatility level — you want to measure the *shape*
# of the wandering, not how volatile the series is.
```

The intuition: $R/S$ grows as $n^H$. A mean-reverting series (small $H$) has a small range $R$ even over long windows, because it keeps snapping back to the mean instead of wandering. A trending series ($H > 0.5$) has a large $R$ because cumulative deviations keep compounding in the same direction.

</details>

---

**Q8.** The simple mean-reversion signal in the code uses a fixed lookback of 30 days and fixed thresholds of ±1.5 for entry and 0 for exit. What three things would you test first in a rigorous backtest to improve this?

<details>
<summary>Answer</summary>

1. **Adaptive lookback based on half-life:** Use 2–3× the estimated half-life as the rolling window (see Pairs Trading Q9 for implementation sketch). A fixed 30-day window may be too long for fast-reverting series and too short for slow ones.

2. **Asymmetric thresholds:** Instead of a fixed ±1.5 entry and 0 exit, optimize the entry/exit jointly as a function of transaction costs. The optimal entry threshold is higher when costs are higher — you need a wider deviation to justify the round-trip cost. This is derivable from the OU expected value formula.

3. **Walk-forward validation with proper train/test splits:** The code tests on the same data used to estimate $\kappa$ and $\mu$. In a real backtest, you'd use a training window to estimate parameters and a held-out test window to evaluate signals, rolling forward in time. Without this, in-sample overfitting inflates apparent Sharpe by 30–50%.

Bonus: add a regime filter — apply the strategy only when the ADF p-value computed over a rolling window is below 0.05. In non-stationary periods, suppress all signals.

</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "A high ADF statistic means strong mean reversion" | The ADF *t-statistic* should be *very negative* (e.g., -3.5 or lower) to reject the unit root. A large positive ADF statistic is actually evidence *against* mean reversion. |
| "Mean reversion and momentum are opposites; you must choose one" | They coexist at different timescales on the same instrument. Mean reversion dominates intraday and at very long horizons; momentum dominates at 1–12 month horizons. |
| "The OU half-life is a forecast of when the trade will close" | It's an *expected* time for half the deviation to close, in the long run. Any individual trade can revert in 1 day or take 3× the half-life. The half-life is a distributional property, not a deterministic forecast. |
| "If I re-estimate $\mu$ frequently, my strategy will always have a fresh signal" | Re-estimating $\mu$ too frequently can lead to a "chasing" effect — you declare the new price level to be the mean, and no signal is ever generated. There's a bias-variance tradeoff in how often you update $\mu$. |
| "A Hurst exponent of exactly 0.5 means the series is a perfect random walk" | $H=0.5$ is consistent with a random walk, but R/S estimation is noisy. A measured $H$ of 0.46–0.54 on a finite sample is statistically indistinguishable from a true random walk at typical sample sizes. Use confidence intervals. |

## Bridge to Quant / ML

- **Feature for ML models:** The OU z-score is a directly usable feature. Pair with momentum features and let an ML model weight them by market regime.
- **Target labeling:** Lopez de Prado's triple-barrier method is especially natural for mean reversion: the expected "take profit" barrier is the mean, and the "stop loss" barrier is some multiple of $\sigma_S$ beyond entry.
- **Regime detection:** Use a Hidden Markov Model or structural break tests (CUSUM, Chow test) to detect when a price series transitions from mean-reverting to trending. Only apply mean-reversion strategies in the appropriate regime.
- **Fractional differentiation:** Lopez de Prado advocates using fractional differencing to make a time series stationary (for ML input) while preserving as much memory as possible. The Hurst exponent guides how much differencing is needed: if $H$ is close to 0.5, little differencing is needed; if $H = 1$ (pure random walk), full first differencing is required.
- **Microstructure application:** Mean reversion at the tick level (order flow imbalance mean-reverting) is fundamental to market-making algorithms. See [[Market Making]] and [[Order Book]].

## Related Concepts

- [[Statistical Arbitrage]] — exploits mean reversion in spreads between instruments
- [[Pairs Trading]] — models the spread as an OU process explicitly
- [[Ornstein-Uhlenbeck Process]] — the canonical continuous-time model for mean-reverting dynamics
- [[Momentum]] — the opposing force at medium timescales
- [[Market Making]] — profits from short-term mean reversion in order flow
- [[Order Book]] — microstructure context for intraday mean reversion

## Sources Used

- Lopez de Prado, M. — *Advances in Financial Machine Learning* (2018), Chapters 2, 5
- Chan, E. — *Algorithmic Trading: Winning Strategies and Their Rationale* (2013)
- Uhlenbeck, G. E. & Ornstein, L. S. — "On the Theory of Brownian Motion" (1930)

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | Added [[Ornstein-Uhlenbeck Process]] to Related Concepts | QA review |
