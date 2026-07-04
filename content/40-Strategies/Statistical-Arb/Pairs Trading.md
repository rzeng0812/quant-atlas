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
> **Chain:** Alpha → Gap 1: Is there any evidence of persistent, tradeable patterns?
> **This concept:** Pairs trading is the simplest cointegration-based implementation of the mean-reversion insight — two assets with a shared trend produce a mean-reverting spread.
> **Alternative approaches to this gap:** [[Momentum]], [[Statistical Arbitrage]]
> **You need first:** [[Mean Reversion]], [[Ornstein-Uhlenbeck Process]]
> **This unlocks:** [[Statistical Arbitrage]], [[Overfitting and Multiple Testing]]

## Why This Exists

**The gap:** Practitioners needed a systematic, market-neutral way to exploit the observation that related assets tend to revert to their historical price relationship after diverging.
**What came before:** Discretionary relative-value trading — traders eyeballed related stocks and made judgment calls about when spreads were too wide, with no systematic entry/exit rules and no statistical validation.
**What this adds:** Cointegration testing provides a rigorous criterion for pairing assets; the OU model parameterizes the spread's reversion speed; z-score thresholds give objective entry and exit signals; dollar-neutrality removes market-level directional risk.
**What it still doesn't solve:** Cointegration can break down permanently; the hedge ratio estimated historically may drift; the strategy is vulnerable to crowding-driven simultaneous unwinds (the August 2007 quant meltdown).

Think about Coca-Cola and Pepsi. Both sell sugary drinks. Both face the same input costs (sugar, aluminum, water), the same distribution challenges, and the same consumer tastes. Over any long stretch, if one gets more expensive relative to the other, you'd expect that gap to close — consumers and investors both notice when one looks like a better deal.

Pairs trading turns this observation into a systematic strategy: find two stocks (or ETFs, or futures contracts) that *historically move together*, then bet on the gap closing whenever it gets unusually wide. You simultaneously short the stock that looks *expensive* relative to its partner and long the stock that looks *cheap*. If you're right, both positions make money as prices revert to their historical relationship.

The key word is "historically." The relationship isn't guaranteed forever. If Pepsi suddenly invented a wildly popular new product, the historic relationship might break. That's why this is "statistical" arbitrage — you're betting on probabilities, not certainties.

The simplest version of stat arb is a pairs trade on two stocks. It's market-neutral (your P&L doesn't depend on whether the whole market goes up or down) and has a clear, intuitive logic. That makes it a perfect starting point for learning quantitative strategies.

## Math Concepts

**Step 1 — Find the hedge ratio**

The spread is not simply $P_1 - P_2$. The two stocks likely have different price levels and volatilities. The **hedge ratio** $\beta$ scales one series so the spread is stationary:

$$S_t = \ln P_{1,t} - \beta \cdot \ln P_{2,t}$$

Estimate $\beta$ by regressing $\ln P_1$ on $\ln P_2$ via OLS:

$$\ln P_{1,t} = \alpha + \beta \ln P_{2,t} + \varepsilon_t$$

$\hat{\beta}$ is the OLS slope coefficient. Using log prices ensures the hedge ratio is in percentage-return space (each unit of spread corresponds to a 1% relative mispricing).

**Step 2 — Test for cointegration**

Run the Augmented Dickey-Fuller (ADF) test on the residuals $\hat{\varepsilon}_t$. Null hypothesis: residuals have a unit root (no cointegration). If p-value < 0.05, reject the null — the spread is stationary and the pair is suitable for trading.

**Step 3 — Model the spread as OU**

$$dS_t = \kappa(\mu - S_t)\,dt + \sigma\,dW_t$$

| Parameter | Meaning | How estimated |
|-----------|---------|---------------|
| $\kappa$ | Mean-reversion speed | OLS of $\Delta S_t$ on $S_{t-1}$ |
| $\mu$ | Long-run spread mean | Sample mean of $S_t$ |
| $\sigma$ | Spread volatility | Std dev of OU residuals |

**Half-life:**

$$t_{1/2} = \frac{\ln 2}{\kappa}$$

Rule of thumb: a half-life of 5–30 days is ideal for daily holding periods. Too short means you can't execute fast enough; too long means capital sits idle.

**Step 4 — Trading rule**

Compute the rolling z-score of the spread:

$$z_t = \frac{S_t - \hat{\mu}}{\hat{\sigma}_S}$$

| Signal | Condition | Action |
|--------|-----------|--------|
| Short spread | $z_t > +2$ | Short $P_1$, Long $P_2$ (in $\beta$ ratio) |
| Long spread | $z_t < -2$ | Long $P_1$, Short $P_2$ (in $\beta$ ratio) |
| Exit | $\|z_t\| < 0.5$ | Close both legs |
| Stop-loss | $\|z_t\| > 3$ | Close both legs (spread diverging) |

**Dollar neutrality:** If you long \$10,000 of $P_1$, you short $\$10,000 \cdot \beta \cdot (P_2/P_1)$ of $P_2$, so the position is dollar-neutral.

**Expected Sharpe (rough estimate):**

Assuming a fair OU process with half-life $t_{1/2}$, you can expect roughly $\sqrt{252/t_{1/2}}$ round trips per year. Each trip earns approximately $1.5\sigma_S$ (entry at $\pm 2$, exit at 0, assuming normal distribution). The Sharpe ratio after costs depends heavily on $\sigma_S$ relative to transaction costs.

## Walkthrough

**Setting up the trade:**

Suppose we run a pairs trade on Coca-Cola (KO) and Pepsi (PEP).

- Estimated hedge ratio: $\hat{\beta} = 0.92$
- Long-run spread mean: $\hat{\mu} = 0.08$
- Spread std dev: $\hat{\sigma}_S = 0.04$
- Estimated half-life: 12 days

**Spread history (last 5 trading days):**

| Day | ln(KO) | ln(PEP) | Spread S | Z-score |
|-----|--------|---------|----------|---------|
| Mon | 3.72 | 3.95 | 3.72 - 0.92*3.95 = 0.086 | +0.15 |
| Tue | 3.74 | 3.96 | 0.099 | +0.47 |
| Wed | 3.79 | 3.96 | 0.154 | +1.85 |
| Thu | 3.82 | 3.96 | 0.184 | **+2.60** |
| Fri | 3.83 | 3.97 | 0.188 | **+2.70** |

On Thursday, the z-score exceeds +2. KO looks expensive relative to PEP.

**Trade entry (Thursday close):**
- Short \$10,000 of KO
- Long \$9,200 of PEP (= \$10,000 * 0.92 * hedge adjustment)
- Net delta: ~\$0 (market neutral)

**10 trading days later:**

KO earnings were in line with expectations, PEP also fine. The gap closes.

| Day | Spread S | Z-score | Position |
|-----|----------|---------|---------|
| +5 | 0.145 | +1.6 | Hold |
| +8 | 0.105 | +0.6 | Hold |
| +10 | 0.085 | +0.1 | **Exit** (|z| < 0.5) |

**P&L:**
- KO short: entered at \$10,000, covered at roughly \$9,850 (KO fell ~1.5%). Profit: **+\$150**.
- PEP long: entered at \$9,200, exited at roughly \$9,215 (PEP roughly flat). Profit: **+\$15**.
- Total gross P&L: **~\$165** on \$19,200 committed capital = ~0.86% gross return over 10 days.
- Less transaction costs (say \$20 round-trip per leg): net P&L ~\$125 = 0.65%.

## Analysis

**What kills the alpha?**

- **Cointegration breakdown:** The most dangerous risk. If KO and PEP diverge permanently (e.g., one loses a major market, new competitor disrupts only one of them), the spread never reverts. Always impose a maximum holding period (e.g., 2× the half-life) and a stop-loss (e.g., $|z| > 4$).
- **Hedge ratio instability:** $\hat{\beta}$ estimated on historical data may shift. OLS is sensitive to outliers. Use rolling regression windows or Kalman filter for dynamic hedge ratios.
- **Crowding:** Pairs trading became a well-known strategy in the 2000s. In August 2007 ("quant meltdown"), crowded pairs strategies unwound simultaneously across many funds, amplifying losses for everyone. If 20 funds are long PEP / short KO at the same time, any forced liquidation cascades.
- **Execution risk:** The two legs must be executed near-simultaneously, especially for volatile stocks. Leg risk — executing one side but not the other — can leave you with unintended directional exposure.
- **Short-selling constraints:** Borrowing the short leg has a cost (borrow fee). In some situations, shares aren't available to borrow at all. This can make the trade infeasible even if the signal is valid.

**Pair selection issues:**
- With $N$ stocks, there are $N(N-1)/2$ possible pairs. Testing all pairs inflates false positive rates (multiple testing problem). Use economic logic to narrow candidates before statistical testing.
- Pairs can look cointegrated in-sample by chance. Use out-of-sample validation periods.

## Implementation

```python
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint, adfuller
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# 1. Simulate a cointegrated pair (KO / PEP stand-ins)
# ------------------------------------------------------------------
np.random.seed(7)
n = 750  # ~3 years of daily data

common = np.cumsum(np.random.normal(0, 0.8, n))   # shared macro trend

log_ko  = common + np.random.normal(0, 0.3, n) + 3.72
log_pep = 0.92 * common + 0.3 + np.random.normal(0, 0.3, n) + 3.95

prices = pd.DataFrame({
    'KO':  np.exp(log_ko),
    'PEP': np.exp(log_pep)
})

# ------------------------------------------------------------------
# 2. Estimate hedge ratio via OLS
# ------------------------------------------------------------------
log_p = np.log(prices)
X = add_constant(log_p['PEP'].values)
ols_result = OLS(log_p['KO'].values, X).fit()
beta  = ols_result.params[1]
alpha = ols_result.params[0]

print(f"Hedge ratio beta: {beta:.4f}")
print(f"Intercept alpha: {alpha:.4f}")

# Test cointegration
_, pval, _ = coint(log_p['KO'], log_p['PEP'])
print(f"Cointegration p-value: {pval:.4f}  {'PASS' if pval < 0.05 else 'FAIL'}")

# ------------------------------------------------------------------
# 3. Compute spread and z-score
# ------------------------------------------------------------------
spread = log_p['KO'] - beta * log_p['PEP'] - alpha

lookback = 60  # rolling window for mean and std

mu_roll    = spread.rolling(lookback).mean()
sigma_roll = spread.rolling(lookback).std()
zscore     = (spread - mu_roll) / sigma_roll

# ------------------------------------------------------------------
# 4. Estimate OU parameters
# ------------------------------------------------------------------
dS    = spread.diff().dropna()
S_lag = spread.shift(1).dropna()

ou_res  = OLS(dS, add_constant(S_lag)).fit()
kappa   = -ou_res.params.iloc[1]          # mean-reversion speed (per day)
half_life = np.log(2) / kappa

print(f"\nOU kappa (per day): {kappa:.4f}")
print(f"Half-life: {half_life:.1f} trading days")

# ------------------------------------------------------------------
# 5. Generate signals and simulate P&L
# ------------------------------------------------------------------
ENTRY = 2.0
EXIT  = 0.5
STOP  = 3.5

position = 0
positions = []

for i in range(len(zscore)):
    z = zscore.iloc[i]
    if np.isnan(z):
        positions.append(0)
        continue

    if position == 0:
        if z > ENTRY:
            position = -1   # short KO, long PEP
        elif z < -ENTRY:
            position = 1    # long KO, short PEP
    elif position == 1:
        if z > -EXIT or z < -STOP:
            position = 0    # exit or stop out
    elif position == -1:
        if z < EXIT or z > STOP:
            position = 0

    positions.append(position)

positions = pd.Series(positions, index=zscore.index)

# Spread P&L (long spread = long KO leg, short PEP leg in beta ratio)
spread_daily_ret = spread.diff()
strategy_ret     = positions.shift(1) * spread_daily_ret

cum_pnl     = strategy_ret.cumsum()
n_trades    = (positions.diff().abs() > 0).sum() // 2
total_days  = strategy_ret.dropna().shape[0]
annualized_sharpe = (
    strategy_ret.mean() / strategy_ret.std() * np.sqrt(252)
    if strategy_ret.std() > 0 else 0
)

print(f"\nNumber of round-trip trades: {n_trades}")
print(f"Annualized Sharpe (gross, no costs): {annualized_sharpe:.2f}")
print(f"Total spread P&L: {cum_pnl.iloc[-1]:.4f}")

# ------------------------------------------------------------------
# 6. (Optional) Plot spread and signals
# ------------------------------------------------------------------
# fig, axes = plt.subplots(2, 1, figsize=(12, 8))
# zscore.plot(ax=axes[0], label='Z-score')
# axes[0].axhline(ENTRY,  color='r', linestyle='--', label='Entry (+2)')
# axes[0].axhline(-ENTRY, color='g', linestyle='--', label='Entry (-2)')
# axes[0].axhline(EXIT,   color='orange', linestyle=':')
# axes[0].legend()
# cum_pnl.plot(ax=axes[1], label='Cumulative P&L (spread units)')
# axes[1].legend()
# plt.tight_layout()
# plt.show()
```

## Bridge to Quant / ML

- **Kalman filter for dynamic hedge ratio:** The static OLS $\hat{\beta}$ can become stale. A Kalman filter treats $\beta_t$ as a hidden state that evolves over time, updating in real-time as new prices arrive. This is a common improvement in production pairs strategies.
- **Feature engineering from the spread:** The z-score itself, its rate of change (momentum of the spread), and the recent half-life estimate are natural features for an ML classifier predicting "will this spread revert in $k$ days?"
- **Pair selection at scale:** With 500 stocks, testing all 124,750 pairs is feasible but noisy. ML clustering (DBSCAN on factor exposures, or word embeddings of business descriptions) can pre-screen candidates before running cointegration tests.
- **Alternative data for regime detection:** News sentiment on one leg but not the other can signal when a cointegrating relationship is about to break — a signal to exit or avoid the trade.
- **Risk decomposition:** The spread P&L can be decomposed into common factor (market, sector, style) and idiosyncratic components. Lopez de Prado's "de-noising" techniques (via random matrix theory) can be applied to the covariance matrix of pairs to find the most stable relationships.

## Self-Assessment

Work through these before looking at the answers. Cover the answer block, write your response, then check.

---

### Level 1 — Conceptual

**Q1.** Why do we use *log* prices rather than raw prices when constructing the spread?

<details>
<summary>Answer</summary>

Log prices put the hedge ratio $\beta$ in percentage-return space. If $\ln P_1 = \beta \ln P_2 + \varepsilon$, then a 1-unit change in $\ln P_2$ corresponds to $\beta$% of relative movement. Using raw prices means $\beta$ depends on the arbitrary *price levels* of each stock (a \$500 stock vs. a \$50 stock), which makes it unstable and hard to interpret.

</details>

---

**Q2.** What is the difference between *correlation* and *cointegration*? Why does pairs trading require cointegration, not just correlation?

<details>
<summary>Answer</summary>

**Correlation** measures whether two series move in the same *direction* at each point in time. It says nothing about whether they stay close together in the long run.

**Cointegration** means a linear combination of two non-stationary series is stationary — i.e., the spread $S_t = \ln P_1 - \beta \ln P_2$ is mean-reverting. The two series may wander far, but they wander *together*.

Two stocks can be highly correlated but not cointegrated: they both go up on good market days and down on bad days (high correlation), but one drifts steadily higher relative to the other forever (no cointegration). If you tried to trade the spread, it would never revert and you'd hold the position indefinitely. Pairs trading *requires* cointegration because that guarantees the spread will return to its historical mean.

</details>

---

**Q3.** What does the half-life of an OU process tell you practically as a trader? What happens if the half-life is 3 days? 3 years?

<details>
<summary>Answer</summary>

The half-life $t_{1/2} = \ln(2) / \kappa$ tells you how long it takes, on average, for half the distance from the mean to be closed. Practically:

- **3 days:** The spread reverts very fast. You need to trade frequently and size positions so transaction costs don't eat the signal. Viable as a higher-frequency strategy.
- **30 days:** Ideal range for most daily-frequency stat arb. You'll turn over positions roughly monthly, with manageable transaction costs.
- **3 years:** The spread barely reverts on any tradeable timescale. Capital is tied up for years waiting for a reversion that may never come in the investment horizon. Not practically tradeable.

Rule of thumb: **5–30 trading days** is the sweet spot for daily execution.

</details>

---

**Q4.** You enter a short spread position (short $P_1$, long $P_2$) when z-score = +2.5. Three weeks later the z-score is +3.8. What should you do, and why?

<details>
<summary>Answer</summary>

**Stop out — close both legs.**

The z-score has moved *further* from zero, not toward it. This is the danger sign: the spread may be diverging permanently (cointegration breakdown) rather than reverting. The stop-loss threshold (commonly z > 3.0 or z > 3.5) exists precisely for this scenario.

Holding on because "it will revert eventually" is the #1 mistake in pairs trading. If the cointegrating relationship has broken (e.g., a fundamental event affecting only one stock), there is no reversion — and you've added more risk, not less.

</details>

---

### Level 2 — Quantitative

**Q5.** You have the following regression output from regressing $\ln(\text{KO})$ on $\ln(\text{PEP})$:

```
Intercept (α):  0.15
Slope (β):      0.88
Residual std:   0.042
```

Today's log prices: $\ln(\text{KO}) = 3.84$, $\ln(\text{PEP}) = 4.01$.

Compute the spread $S$ and z-score. Should you enter a trade?

<details>
<summary>Answer</summary>

**Spread:**
$$S = \ln(\text{KO}) - \hat{\beta} \cdot \ln(\text{PEP}) - \hat{\alpha}$$
$$S = 3.84 - 0.88 \times 4.01 - 0.15$$
$$S = 3.84 - 3.5288 - 0.15 = 0.1612$$

**Long-run mean of spread** $\hat{\mu}$: when the residual is zero, $S = \hat{\alpha} + 0 = 0.15$. (The intercept is the expected spread when $\ln P_2$ is zero in normalized space — but practically, $\hat{\mu}$ is estimated as the sample mean of $S_t$ over the history, not the intercept alone. The intercept absorbs the level difference. For this problem, use $\hat{\mu} = 0.15$ as given.)

**Z-score:**
$$z = \frac{S - \hat{\mu}}{\hat{\sigma}} = \frac{0.1612 - 0.15}{0.042} = \frac{0.0112}{0.042} \approx 0.27$$

**No trade.** Z = 0.27 is nowhere near the ±2 entry threshold. The spread is close to its mean — no signal.

</details>

---

**Q6.** You run an AR(1) regression on daily spread changes and get:

$$\Delta S_t = 0.012 - 0.045 \cdot S_{t-1} + \varepsilon_t$$

a) What is the estimated $\kappa$?
b) What is the half-life in trading days?
c) Is this within the tradeable range?

<details>
<summary>Answer</summary>

**a)** From the AR(1) form: $b = -\kappa \Delta t$, with $\Delta t = 1$ day.

$$\kappa = -b = -(-0.045) = 0.045 \text{ per day}$$

**b)** Half-life:
$$t_{1/2} = \frac{\ln 2}{\kappa} = \frac{0.693}{0.045} \approx 15.4 \text{ trading days}$$

**c) Yes** — 15 days is comfortably in the 5–30 day sweet spot. This spread reverts in approximately 3 weeks, making it suitable for daily-rebalanced stat arb.

</details>

---

**Q7.** Your pairs strategy has:
- Entry at z = ±2.0, exit at z = ±0.5
- Spread std dev $\hat{\sigma} = 0.05$ (log-price units)
- Each round trip generates a gross spread profit of approximately $1.5 \hat{\sigma}$
- Transaction costs: 0.15% per leg (4 legs per round trip)
- You execute 20 round trips per year

Is the strategy profitable net of costs? What's the rough annual Sharpe?

<details>
<summary>Answer</summary>

**Gross profit per trade:**
$$\approx 1.5 \times 0.05 = 0.075 \text{ (log-price units, \textasciitilde 7.5\%)}$$

**Transaction cost per round trip:** 4 legs × 0.15% = 0.60% = 0.006

**Net profit per trade:** $0.075 - 0.006 = 0.069$

**Annual net profit:** $20 \times 0.069 = 1.38$ (log-price units)

**Annual volatility:** The spread std per trade is $\hat{\sigma} = 0.05$. With 20 trades, assuming independence:
$$\sigma_{\text{annual}} \approx 0.05 \times \sqrt{20} \approx 0.224$$

**Rough Sharpe:**
$$\text{SR} \approx \frac{1.38}{0.224} \approx 6.1$$

This looks unrealistically high because the trades are *not* independent (capital is constantly at work) and real strategies face many frictions not modeled here. In practice, well-run pairs strategies achieve Sharpe ratios of 1–2. This exercise shows the *theoretical* edge before crowding, correlation, and model risk.

</details>

---

### Level 3 — Coding

**Q8.** The implementation above uses a static (rolling-window) z-score. A known improvement is a **Kalman filter** for a dynamic hedge ratio $\beta_t$. Without coding it fully, explain:
- What state variable does the Kalman filter track?
- What does the "measurement equation" look like?
- What does the "transition equation" look like?
- Why is this better than rolling OLS?

<details>
<summary>Answer</summary>

**State variable:** $\beta_t$ — the time-varying hedge ratio.

**Measurement equation** (what we observe):
$$\ln P_{1,t} = \alpha + \beta_t \ln P_{2,t} + \varepsilon_t, \quad \varepsilon_t \sim N(0, R)$$

This says: today's log price of $P_1$ equals the current hedge ratio times $P_2$'s log price, plus noise.

**Transition equation** (how $\beta_t$ evolves):
$$\beta_t = \beta_{t-1} + \eta_t, \quad \eta_t \sim N(0, Q)$$

A random walk — $\beta$ drifts slowly over time. The ratio $Q/R$ controls how responsive the estimate is: large $Q$ means $\beta$ can change fast (noisy but reactive); small $Q$ means $\beta$ changes slowly (stable but lags).

**Why better than rolling OLS:**
- Rolling OLS treats all observations in the window equally and discards everything outside it. A Kalman filter weights recent observations more heavily via the Kalman gain, responding *smoothly* to changes in $\beta_t$.
- Avoids the "window cliff" artifact — in rolling OLS, dropping an old outlier from the window can suddenly shift $\hat{\beta}$ discontinuously.
- Provides a confidence interval on $\beta_t$ at each point in time (the Kalman covariance matrix), which rolling OLS doesn't give naturally.

</details>

---

**Q9.** The code above uses a fixed rolling window of 60 days for the z-score. Write pseudocode (or real code) for a simple improvement: **adaptive window selection** based on the estimated half-life.

<details>
<summary>Answer</summary>

```python
def adaptive_zscore(spread, min_window=20, max_window=120, hl_multiplier=3.0):
    """
    Compute z-score using a window = hl_multiplier * half_life,
    clamped to [min_window, max_window].
    """
    zscores = pd.Series(np.nan, index=spread.index)

    for i in range(max_window, len(spread)):
        # Use last 120 days to estimate OU parameters
        window_data = spread.iloc[max(0, i - 120):i]
        dS    = window_data.diff().dropna()
        S_lag = window_data.shift(1).dropna()

        try:
            reg = OLS(dS, add_constant(S_lag)).fit()
            b   = reg.params.iloc[1]
            kappa = max(-b, 1e-6)          # must be positive
            half_life = np.log(2) / kappa
        except Exception:
            half_life = 30                 # fallback

        # Set window = 3x half-life, clamped
        lookback = int(np.clip(hl_multiplier * half_life, min_window, max_window))

        sub = spread.iloc[i - lookback:i]
        mu  = sub.mean()
        sig = sub.std()
        if sig > 0:
            zscores.iloc[i] = (spread.iloc[i] - mu) / sig

    return zscores
```

**Why this works:** A 5-day half-life spread is very noisy — using a 60-day window includes "ancient" history that's no longer relevant. Adapting the window to 3× the half-life ensures you capture enough observations for a stable estimate while staying as fresh as possible.

</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "High correlation means the pair is suitable for trading" | Correlation ≠ cointegration. Two correlated series can diverge permanently. Always run ADF on the spread. |
| "If the spread widens, I should add to my position (average in)" | Dangerous. Widening spread could be cointegration breakdown. Follow your stop-loss rules. |
| "The z-score entry threshold should always be ±2" | The optimal threshold depends on the half-life and transaction costs. Fast-reverting, cheap-to-trade pairs can use tighter thresholds; slow-reverting pairs need wider entries. |
| "Dollar-neutral means market-neutral" | Dollar-neutral eliminates market beta *on average*. If $P_1$ has high beta and $P_2$ has low beta, you still have residual market exposure. True market neutrality requires matching betas, not just dollars. |
| "Pairs trading is risk-free arbitrage" | It is *statistical* arbitrage — you're betting on probabilities. Cointegration can break. It's not true arbitrage; losses are possible and have historically been severe during market stress. |

## Related Concepts

- [[Statistical Arbitrage]] — the broader framework pairs trading is an instance of
- [[Mean Reversion]] — the underlying statistical behavior the spread exploits
- [[Ornstein-Uhlenbeck Process]] — the continuous-time stochastic process that models the spread dynamics
- [[Market Making]] — another mean-reversion strategy at finer timescales
- [[Adverse Selection]] — execution risk when the other side is informed
- [[Order Book]] — where the two legs get executed

## Sources Used

- Lopez de Prado, M. — *Advances in Financial Machine Learning* (2018)
- Vidyamurthy, G. — *Pairs Trading: Quantitative Methods and Analysis* (2004)
- Gatev, E., Goetzmann, W. N., & Rouwenhorst, K. G. — "Pairs Trading: Performance of a Relative Value Arbitrage Rule" (2006), *Review of Financial Studies*

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | Added [[Ornstein-Uhlenbeck Process]] to Related Concepts | QA review |
