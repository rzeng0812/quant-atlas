---
type: concept
domain: 30-Models
tags: [portfolio, performance]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-12
review_interval_days: 365
sources:
  - "Sharpe (1966), Journal of Business"
  - "Lo (2002), Journal of Portfolio Management — Sharpe ratio statistics"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Hedging & Risk — supporting concept (return per unit risk measurement)
> **This concept:** The Sharpe Ratio answers "how much excess return am I earning per unit of volatility?" — the universal strategy performance metric.
> **Alternative approaches to this gap:** none
> **You need first:** [[Value at Risk]], [[Expected Shortfall]]
> **This unlocks:** [[Kelly Criterion]], [[Markowitz Mean-Variance Optimization]], [[Maximum Drawdown]]

## Why This Exists

**The gap:** Raw return is a useless comparison metric across strategies with different risk levels. A strategy returning 20% with wild swings might be worse than one returning 10% steadily — but there was no agreed way to compare them on a risk-adjusted basis.

**What came before:** Absolute return comparisons (which strategy made more money?) ignored the risk taken to achieve that return. Two strategies could have identical raw returns but completely different risk profiles.

**What this adds:** Sharpe (1966) divided excess return by volatility to create a dimensionless ratio that compares strategies on equal terms regardless of leverage or asset class. The S&P 500 historically scores ~0.5; top quant strategies target 1.5–2.5. It also anchors to financial theory: the Sharpe Ratio is the slope of the Capital Market Line, and maximizing it is mathematically equivalent to Markowitz optimization with a risk-free asset.

**What it still doesn't solve:** Sharpe penalizes upside and downside volatility equally, making it blind to skewness. Strategies can game it by selling options (smooth returns until catastrophic loss) or marking illiquid positions smoothly. It ignores drawdown entirely — two strategies with the same Sharpe can have very different peak-to-trough experiences.

Imagine two investment strategies:
- **Strategy A** returns 20% per year, but its value jumps around wildly — it's up 40% one month and down 25% the next.
- **Strategy B** returns 10% per year with very smooth, steady gains.

Which is better? Strategy A has higher returns, but its wild swings might be unbearable — and they represent real risk of catastrophic loss if you need to withdraw at a bad time. Strategy B is half the return but much calmer. A rational investor should want to know: **how much return am I getting per unit of risk?**

The Sharpe Ratio answers this question. It divides the strategy's *excess return* (return above a risk-free alternative, like T-bills) by the strategy's volatility (standard deviation of returns). Strategy A might have a Sharpe of 0.8 while Strategy B has a Sharpe of 1.2 — meaning Strategy B is actually delivering more return per unit of risk, even though its raw return is lower.

Another way to think about it: the Sharpe Ratio is the slope of the Capital Market Line. It tells you how much the strategy compensates you for each unit of standard deviation you bear. A Sharpe of 2.0 means for every 1% of volatility, you earn 2% of excess return. A higher slope = a better risk-adjusted deal.

The Sharpe Ratio is the most widely used single number for evaluating investment strategies — from hedge funds to academic factor portfolios to ML-based trading systems. It is imperfect, but its simplicity and universality make it indispensable.

## Math Concepts

**Definition.** For portfolio $p$ over a measurement period:

$$\boxed{S_p = \frac{R_p - R_f}{\sigma_p}}$$

| Term | Meaning |
|------|---------|
| $R_p$ | Portfolio's mean return over the period |
| $R_f$ | Risk-free rate (T-bill rate, SOFR, or 0 for simplicity) |
| $\sigma_p$ | Standard deviation of portfolio returns over the same period |

**Annualizing the Sharpe Ratio.** When computed from daily returns:

$$S_{\text{annual}} = \frac{\bar{r}_{\text{daily}} \times 252}{\sigma_{\text{daily}} \times \sqrt{252}} = \frac{\bar{r}_{\text{daily}}}{\sigma_{\text{daily}}} \times \sqrt{252}$$

This uses the square-root-of-time rule: mean scales linearly with time, standard deviation scales with $\sqrt{T}$.

For other frequencies:

| Return frequency | Annualization factor |
|-----------------|---------------------|
| Daily | $\sqrt{252}$ |
| Weekly | $\sqrt{52}$ |
| Monthly | $\sqrt{12}$ |

**Benchmark for Sharpe values:**

| Sharpe Ratio | Interpretation |
|-------------|---------------|
| < 0 | Strategy loses money relative to risk-free rate |
| 0 – 0.5 | Poor. Not worth the risk |
| 0.5 – 1.0 | Mediocre. Roughly buy-and-hold equity market |
| 1.0 – 2.0 | Good. Most successful active strategies fall here |
| 2.0 – 3.0 | Strong. Institutional-quality quant strategy |
| > 3.0 | Exceptional. Likely data-mining or short-lived alpha |

The S&P 500 historically has a Sharpe of about 0.4–0.6 over long periods. Most mutual funds are below this. Top quant hedge funds target 1.5–2.5 in live trading.

**Statistical significance.** The Sharpe Ratio has sampling error. Lo (2002) showed that under i.i.d. normal returns with $T$ observations, the standard error of the estimated Sharpe is approximately:

$$\text{SE}(\hat{S}) \approx \sqrt{\frac{1 + \hat{S}^2 / 2}{T}}$$

For a strategy with Sharpe = 1.0, you need about $T = 500$ daily observations (~2 years) to detect it at the 2-sigma level. Many backtests with attractive Sharpes are not statistically significant.

**Variants of the Sharpe Ratio:**

| Metric | Formula | What it improves |
|--------|---------|-----------------|
| Sharpe Ratio | $(\bar{R} - R_f) / \sigma$ | Baseline |
| **Sortino Ratio** | $(\bar{R} - R_f) / \sigma_{\text{downside}}$ | Only penalizes *downside* volatility |
| **Calmar Ratio** | $\text{Annual Return} / \text{MaxDD}$ | Penalizes drawdown, not vol |
| **Information Ratio** | $(\bar{R}_p - \bar{R}_b) / \sigma_{\text{tracking error}}$ | Active return vs. benchmark |
| **Omega Ratio** | $\int_{\theta}^{\infty}(1-F(r))dr / \int_{-\infty}^{\theta} F(r)dr$ | Captures full distribution shape |

**Sortino Ratio** is preferred when a strategy has positive skew (good upside volatility does not hurt you; only downside matters):

$$\text{Sortino} = \frac{R_p - R_f}{\sigma_{\text{downside}}} \qquad \sigma_{\text{downside}} = \sqrt{E[\min(r - R_f, 0)^2]}$$

**Information Ratio (IR)** is the Sharpe ratio for an *active* strategy measured against a benchmark:

$$IR = \frac{\alpha}{\sigma_{\epsilon}} = \frac{\bar{R}_p - \bar{R}_b}{\text{Tracking Error}}$$

where $\alpha = \bar{R}_p - \bar{R}_b$ is the active return and $\sigma_\epsilon$ is the standard deviation of the difference. This isolates skill from benchmark exposure — critical when evaluating whether a fund manager is adding value above a cheap index fund.

## Walkthrough

**Setup:** A strategy runs for 252 trading days (1 year). We collect daily P&L as percentage returns.

Observations:
- Mean daily return: $\bar{r} = 0.060\%$
- Daily standard deviation: $\sigma = 0.950\%$
- Daily risk-free rate: $r_f = 0.010\%$ (approximately 2.5% annual / 252)

**Step 1 — Daily Sharpe:**
$$S_{\text{daily}} = \frac{0.060\% - 0.010\%}{0.950\%} = \frac{0.050\%}{0.950\%} = 0.0526$$

**Step 2 — Annualize:**
$$S_{\text{annual}} = 0.0526 \times \sqrt{252} = 0.0526 \times 15.87 = \mathbf{0.835}$$

**Step 3 — Annualized returns and vol for context:**
- Annualized mean: $0.060\% \times 252 = 15.12\%$
- Annualized std: $0.950\% \times \sqrt{252} = 15.08\%$

So this strategy returns ~15% per year with ~15% volatility — a Sharpe of about 0.84. Decent, but roughly buy-and-hold equity level.

**Step 4 — Statistical significance:**
$$\text{SE}(\hat{S}) \approx \sqrt{\frac{1 + 0.835^2/2}{252}} = \sqrt{\frac{1.348}{252}} = \sqrt{0.00535} = 0.073$$

t-statistic: $t = 0.835 / 0.073 = 11.4$ — highly significant. With a full year of data and Sharpe of 0.84, the estimate is reliable.

## Analysis

**Strengths:**
- Dimensionless: can compare a bond strategy to an equity strategy to a crypto strategy on equal footing.
- Universally understood in finance — an immediate communication shorthand.
- Simple to compute from a returns series.
- Directly links to [[Kelly Criterion]]: $f^* = S/\sigma$ — high Sharpe strategies warrant larger Kelly fractions.

**Weaknesses:**
- **Assumes normality:** Sharpe penalizes all volatility equally — upside and downside. A strategy with strong positive skew (many small losses, occasional huge gains) looks worse than it is.
- **Ignores higher moments:** Two strategies with identical mean and volatility can have very different skewness and kurtosis. Sharpe treats them the same.
- **Sensitive to return frequency:** Computing Sharpe from monthly returns vs. daily returns for the same strategy can give different annualized values if returns are autocorrelated.
- **Does not capture drawdown:** A strategy can have a good Sharpe but a brutal [[Maximum Drawdown]] — the Sharpe says nothing about how long you might spend underwater.
- **Gaming:** Strategies can inflate Sharpe by selling options (collect premium = higher mean, until the rare catastrophic loss), or by using mark-to-model pricing with smooth P&L.
- **Look-ahead bias in backtests:** Overfitting can produce unrealistically high historical Sharpes.

**Known failure modes:**
- **Autocorrelation inflation:** If a portfolio is illiquid or marked-to-model (e.g., private equity, some hedge fund strategies), P&L is artificially smooth. The reported Sharpe is inflated because volatility appears lower than the true economic risk.
- **Short volatility strategies:** Selling options or credit protection collects steady premium → high daily Sharpe. But the distribution has massive negative tail risk (rare but catastrophic loss). VIX spike in Feb 2018 wiped out several short-vol products with seemingly excellent Sharpe histories.
- **Period selection:** Sharpe depends heavily on which years you include. The S&P 500 Sharpe in 2017 was ~3.8 (abnormally calm); in 2022 it was deeply negative.

## Implementation

```python
import numpy as np
import pandas as pd
from scipy import stats

# ── 1. Basic Sharpe from daily returns ────────────────────────────────────
def sharpe_ratio(returns: np.ndarray, rf_daily: float = 0.0,
                 annualize: bool = True, trading_days: int = 252) -> float:
    """
    Compute annualized Sharpe Ratio from daily excess returns.
    
    Args:
        returns: array of daily returns (as decimals, e.g., 0.005 = 0.5%)
        rf_daily: daily risk-free rate (default 0)
        annualize: whether to annualize (multiply by sqrt(trading_days))
        trading_days: number of trading days per year (default 252)
    """
    excess = returns - rf_daily
    if np.std(excess, ddof=1) == 0:
        return 0.0
    s = np.mean(excess) / np.std(excess, ddof=1)
    if annualize:
        s *= np.sqrt(trading_days)
    return float(s)

# ── 2. Sortino Ratio ──────────────────────────────────────────────────────
def sortino_ratio(returns: np.ndarray, rf_daily: float = 0.0,
                  annualize: bool = True, trading_days: int = 252) -> float:
    """
    Sortino Ratio: penalizes only downside volatility.
    Uses semi-deviation below the target (risk-free rate).
    """
    excess = returns - rf_daily
    downside = excess[excess < 0]
    if len(downside) == 0:
        return np.inf
    downside_std = np.sqrt(np.mean(downside ** 2))  # root mean squared downside dev
    if downside_std == 0:
        return np.inf
    s = np.mean(excess) / downside_std
    if annualize:
        s *= np.sqrt(trading_days)
    return float(s)

# ── 3. Information Ratio ──────────────────────────────────────────────────
def information_ratio(portfolio_returns: np.ndarray,
                      benchmark_returns: np.ndarray,
                      annualize: bool = True, trading_days: int = 252) -> float:
    """
    Information Ratio = active return / tracking error.
    Measures skill relative to a benchmark (e.g., S&P 500).
    """
    active = portfolio_returns - benchmark_returns
    te = np.std(active, ddof=1)  # tracking error
    if te == 0:
        return 0.0
    ir = np.mean(active) / te
    if annualize:
        ir *= np.sqrt(trading_days)
    return float(ir)

# ── 4. Statistical significance of Sharpe estimate (Lo 2002) ─────────────
def sharpe_se(sharpe_annual: float, n_obs: int, freq: str = 'daily') -> dict:
    """
    Standard error and t-stat for an annualized Sharpe estimate.
    Based on Lo (2002) approximation under i.i.d. normal returns.
    
    For non-normal returns, SE is larger — this is a lower bound.
    """
    se = np.sqrt((1 + sharpe_annual**2 / 2) / n_obs)
    t_stat = sharpe_annual / se
    p_value = 2 * (1 - stats.norm.cdf(abs(t_stat)))
    return {'sharpe': sharpe_annual, 'se': se, 't_stat': t_stat,
            'p_value': p_value, 'significant_5pct': p_value < 0.05}

# ── 5. Demo: compare two strategies ──────────────────────────────────────
np.random.seed(42)
n = 252 * 3  # 3 years of daily data

# Strategy A: high return, high vol, slight negative skew (sells options)
r_A = np.concatenate([
    np.random.normal(0.0008, 0.007, n - 5),
    np.array([-0.05, -0.06, -0.04, -0.03, -0.05])   # rare tail events
])

# Strategy B: moderate return, moderate vol, slight positive skew
r_B = np.random.normal(0.0004, 0.005, n)
r_B += 0.0002 * (np.random.exponential(1, n) - 1)   # positive skew

rf_daily = 0.025 / 252  # 2.5% annual risk-free rate

print("Strategy Comparison:")
print(f"{'Metric':<25} {'Strategy A':>15} {'Strategy B':>15}")
print("-" * 55)

metrics = {
    'Ann. Return':   [f"{np.mean(r_A)*252:.2%}", f"{np.mean(r_B)*252:.2%}"],
    'Ann. Volatility':[f"{np.std(r_A,ddof=1)*np.sqrt(252):.2%}", f"{np.std(r_B,ddof=1)*np.sqrt(252):.2%}"],
    'Sharpe':        [f"{sharpe_ratio(r_A, rf_daily):.3f}", f"{sharpe_ratio(r_B, rf_daily):.3f}"],
    'Sortino':       [f"{sortino_ratio(r_A, rf_daily):.3f}", f"{sortino_ratio(r_B, rf_daily):.3f}"],
    'Skewness':      [f"{stats.skew(r_A):.3f}", f"{stats.skew(r_B):.3f}"],
    'Excess Kurtosis':[f"{stats.kurtosis(r_A):.3f}", f"{stats.kurtosis(r_B):.3f}"],
}

for metric, (vA, vB) in metrics.items():
    print(f"{metric:<25} {vA:>15} {vB:>15}")

# Statistical significance
for name, r in [('Strategy A', r_A), ('Strategy B', r_B)]:
    s = sharpe_ratio(r, rf_daily)
    sig = sharpe_se(s, len(r))
    print(f"\n{name} Sharpe significance: t={sig['t_stat']:.2f}, p={sig['p_value']:.4f}, "
          f"{'SIGNIFICANT' if sig['significant_5pct'] else 'NOT SIGNIFICANT'}")

# ── 6. Rolling Sharpe (visualize strategy stability) ──────────────────────
import matplotlib.pyplot as plt

window = 63  # ~3 months

def rolling_sharpe(r: np.ndarray, window: int, rf: float = 0.0) -> np.ndarray:
    result = np.full(len(r), np.nan)
    for i in range(window, len(r)):
        result[i] = sharpe_ratio(r[i-window:i], rf, annualize=True)
    return result

rs_A = rolling_sharpe(r_A, window, rf_daily)
rs_B = rolling_sharpe(r_B, window, rf_daily)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(rs_A, label='Strategy A (rolling Sharpe)', alpha=0.8, color='steelblue')
ax.plot(rs_B, label='Strategy B (rolling Sharpe)', alpha=0.8, color='green')
ax.axhline(1.0, color='black', linestyle='--', linewidth=0.8, label='Sharpe=1')
ax.axhline(0.0, color='red',   linestyle='--', linewidth=0.8, label='Sharpe=0')
ax.set_title(f'Rolling {window}-Day Sharpe Ratio')
ax.set_xlabel('Trading Day')
ax.set_ylabel('Annualized Sharpe')
ax.legend()
plt.tight_layout()
plt.savefig('rolling_sharpe.png', dpi=150)
plt.show()
```

## Bridge to Quant / ML

**Strategy evaluation pipeline.** In any quant shop, Sharpe is the primary gatekeeping metric for a new strategy: historical backtest Sharpe must clear a minimum threshold (often 1.5–2.0 net of costs) before a strategy reaches production.

**Sharpe in optimization.** The Markowitz mean-variance optimization, when the risk-free asset is available, maximizes the Sharpe Ratio of the tangency portfolio. So portfolio construction = Sharpe maximization.

**Kelly connection:** The Kelly fraction $f^* = \mu/\sigma^2 = S/\sigma$ — maximizing Sharpe directly maximizes the Kelly fraction for a fixed volatility.

**ML connections:**
- **Objective function:** Many ML trading models use Sharpe ratio (or a differentiable proxy) as their training objective instead of MSE. Directly optimizing the metric you care about aligns training with deployment goals.
- **Differentiable Sharpe:** Define $S = \mu_r / \sigma_r$ where $\mu_r, \sigma_r$ are running mean and std of predicted P&L. This is differentiable and can be used as a PyTorch/JAX loss.
- **Walk-forward validation:** Rolling Sharpe across out-of-sample windows is the standard ML model validation technique for trading strategies — analogous to cross-validation.
- **Regime detection:** Sharpe deterioration in rolling windows is an early warning signal for regime change and strategy deactivation.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why does the Sharpe Ratio use *excess* return (return minus risk-free rate) rather than raw return in its numerator?
<details><summary>Answer</summary>The risk-free rate is the return available with zero risk. Any investor can earn it by holding T-bills. The Sharpe Ratio measures skill at earning return *above* this baseline per unit of risk taken. Using raw return would unfairly penalize strategies in high-rate environments (where even cash earns well) and would make comparisons across time periods with different rate regimes meaningless. Excess return correctly isolates the compensation for bearing volatility.</details>

**Q2.** A strategy has a Sharpe Ratio of 2.5 computed from monthly returns and annualized by multiplying by $\sqrt{12}$. If the monthly returns are positively autocorrelated (good months tend to follow good months), is the true annualized Sharpe higher or lower than 2.5? Explain.
<details><summary>Answer</summary>Lower. The annualization factor $\sqrt{12}$ assumes i.i.d. returns — that each month is independent. With positive autocorrelation, the monthly Sharpe underestimates monthly risk because autocorrelated series have lower measured variance than their true economic risk. When returns are positively autocorrelated, the annual variance is greater than $12 \times \text{monthly variance}$, so the true denominator is larger. Equivalently: autocorrelated strategies (like private equity or smoothly-marked hedge funds) report artificially high Sharpe ratios. Lo (2002) provides the autocorrelation correction.</details>

**Q3.** Two strategies both have annualized Sharpe = 1.2. Strategy A sells out-of-the-money put options on the S&P 500; Strategy B runs a diversified equity long-short. Which is likely to be the better risk-adjusted investment? Why does the Sharpe Ratio fail to distinguish them?
<details><summary>Answer</summary>Strategy B is likely better. Strategy A collects steady option premium, producing smooth positive returns and low measured volatility — until the rare equity crash, when it loses catastrophically. This negative skewness is invisible to the Sharpe Ratio, which treats upside and downside volatility identically. The Sharpe of 1.2 for Strategy A is inflated by the option premium and the lack of a large realized drawdown in the sample period. To distinguish them, you need tail-sensitive metrics (ES, Sortino Ratio) or direct examination of skewness and kurtosis.</details>

---

### Level 2 — Quantitative

**Q4.** A strategy has mean daily return $\bar{r} = 0.045\%$ and daily standard deviation $\sigma = 0.80\%$. The daily risk-free rate is $r_f = 0.008\%$. Compute: (a) the annualized Sharpe Ratio; (b) the standard error of this estimate (Lo 2002 formula); (c) the t-statistic testing whether Sharpe > 0.
<details><summary>Answer</summary>

(a) Daily Sharpe: $S_{\text{daily}} = (0.045\% - 0.008\%) / 0.80\% = 0.037\% / 0.80\% = 0.04625$

Annualized: $S_{\text{annual}} = 0.04625 \times \sqrt{252} = 0.04625 \times 15.875 = \mathbf{0.734}$

(b) Lo (2002) SE with $T = 252$ observations:
$$\text{SE} = \sqrt{\frac{1 + S_{\text{annual}}^2/2}{T}} = \sqrt{\frac{1 + 0.734^2/2}{252}} = \sqrt{\frac{1 + 0.269}{252}} = \sqrt{\frac{1.269}{252}} = \sqrt{0.00504} = 0.071$$

(c) t-statistic: $t = 0.734 / 0.071 = \mathbf{10.3}$

Strongly significant (well above 2.0). With a full year of data at Sharpe = 0.73, the signal is reliable.</details>

**Q5.** Strategy A: annualized return 18%, annualized vol 20%, max drawdown 35%. Strategy B: annualized return 12%, annualized vol 10%, max drawdown 15%. Risk-free rate = 3%. Compute Sharpe and Calmar ratios for both. Which strategy is preferable and why might the answer depend on the investor?
<details><summary>Answer</summary>

**Strategy A:** Sharpe = (18% - 3%) / 20% = 0.75. Calmar = 18% / 35% = 0.51.

**Strategy B:** Sharpe = (12% - 3%) / 10% = 0.90. Calmar = 12% / 15% = 0.80.

Strategy B wins on both metrics — higher Sharpe and much higher Calmar. 

For a leveraged investor, B could be levered 2× to achieve 21% return with 20% vol and ~30% max drawdown — comparable to A's return at better Sharpe. For an unleveraged investor focused on smooth compounding, B is clearly superior. A might only be preferred if the investor has a specific return target that B cannot reach even with leverage, or if the 3-year period for A's data captured unusually good conditions and the Sharpe would normalize downward.</details>

---

### Level 3 — Coding

**Q6.** The rolling Sharpe implementation uses a nested loop over a 63-day window. For a 10-year dataset (2,520 days), this runs the loop ~2,457 times. Describe how you would vectorize this computation using Pandas rolling functions, and explain why the annualization step must use $\sqrt{252}$ even when the window is 63 days (not 252 days).
<details><summary>Answer</summary>

Vectorized with Pandas:
```python
import pandas as pd
returns = pd.Series(r_A)
rf = 0.0
window = 63
rolling_mean = (returns - rf).rolling(window).mean()
rolling_std = (returns - rf).rolling(window).std()
rolling_sharpe = rolling_mean / rolling_std * np.sqrt(252)
```

The annualization uses $\sqrt{252}$ even for a 63-day window because: the window computes a 63-day *estimate* of the daily Sharpe (mean and std per day within the window). To express this as an annualized quantity, you scale up as if the daily statistics held for a full year. This is consistent with how the full-sample Sharpe is computed — it is always the annualized Sharpe of the underlying daily return distribution, regardless of the estimation window length. Using $\sqrt{63}$ instead would give a "quarterly Sharpe" with a different scale, making rolling windows non-comparable to the reported annual Sharpe.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| A higher Sharpe is always better | Not if it's achieved via negative-skew strategies (option selling, credit). Check skewness and tail metrics. |
| Sharpe measures absolute return quality | It measures return per unit of *measured* volatility — which can be artificially low in illiquid or smoothly-marked portfolios. |
| Monthly Sharpe × √12 = annual Sharpe exactly | Only under i.i.d. returns. With autocorrelation, the annualized number can be significantly different from the true annual Sharpe. |
| Sharpe > 1 means the strategy is good | Context-dependent. For daily-traded equities, Sharpe > 1 is good. For low-frequency macro, 0.7 might be excellent. Compare to relevant peer benchmarks. |

## Related Concepts

- [[Kelly Criterion]] — $f^* = S/\sigma$; Sharpe is the key input to optimal sizing
- [[Maximum Drawdown]] — Calmar ratio = return / MaxDD; captures what Sharpe misses about path dependence
- [[Factor Models]] — Information Ratio is the factor-adjusted Sharpe for active managers
- [[Expected Shortfall]] — tail-aware complement to Sharpe; captures the distribution shape Sharpe ignores

## Sources Used

- Sharpe, W. F. (1966). Mutual fund performance. *Journal of Business*, 39(1), 119-138
- Lo, A. W. (2002). The statistics of Sharpe ratios. *Financial Analysts Journal*, 58(4), 36-52

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review: no issues found | quality review |
