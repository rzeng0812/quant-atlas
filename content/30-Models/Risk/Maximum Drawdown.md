---
type: concept
domain: 30-Models
tags: [risk, portfolio, performance]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-12
review_interval_days: 365
sources:
  - "Magdon-Ismail & Atiya (2004), Quantitative Finance"
  - "Bailey & Lopez de Prado (2012), Journal of Portfolio Management"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Hedging & Risk — supporting concept (path-dependent risk of an equity curve)
> **This concept:** Maximum Drawdown measures the largest peak-to-trough decline an investor would have experienced — capturing sustained loss risk that volatility-based metrics like Sharpe Ratio completely ignore.
> **Alternative approaches to this gap:** none
> **You need first:** [[Sharpe Ratio]], [[Value at Risk]]
> **This unlocks:** [[Stress Testing]]

## Why This Exists

**The gap:** Sharpe Ratio and volatility-based metrics are path-blind — they describe the distribution of returns but say nothing about sequences of losses. A strategy with the same annual return and volatility can feel completely different depending on whether losses are scattered randomly or cluster into sustained losing streaks.

**What came before:** Sharpe Ratio was the primary performance metric. It would rate two strategies identically if they had the same mean and variance, even if one had a 22% sustained drawdown while the other oscillated ±3% continuously.

**What this adds:** Maximum Drawdown measures the worst peak-to-trough decline the portfolio experienced — the most economically relevant risk metric for investors who might need to liquidate, who face margin calls, or who simply cannot psychologically tolerate sustained losses. It directly determines when risk limits are triggered and leverage is cut.

**What it still doesn't solve:** MaxDD is path-dependent and non-additive — you cannot decompose portfolio MaxDD into asset contributions. It is strongly sensitive to the measurement window and dominated by a single worst episode. It has no forward-looking interpretation: historical MaxDD is a lower bound on future MaxDD.

Here is something volatility-based metrics like the [[Sharpe Ratio]] completely miss: the experience of living through a losing streak.

Imagine two strategies with identical Sharpe ratios. Strategy A loses 3% one month, gains it back the next, alternating like clockwork. Strategy B has a year where it falls steadily from its peak — down 5%, down 8%, down 15%, down 22% before recovering. Both might have the same annual return and volatility. But almost every real investor would quit Strategy B. The psychological and economic pain of watching your account fall 22% from its high — and not knowing whether it will keep falling or ever recover — is qualitatively different from symmetric, rapid oscillations.

Maximum Drawdown (MaxDD) measures exactly this: **the largest peak-to-trough decline an investor would have experienced if they entered at the worst possible time and exited at the worst trough.** It is the most gut-wrenching number in a strategy tearsheet.

Think of it as the "worst sustained loss" metric. If you had started investing in this strategy at its highest point before the worst period, how much of your money would you have lost at the bottom? That is MaxDD.

Why does this matter beyond psychology? It matters because:
1. Investors redeem from funds during drawdowns, forcing managers to sell into weakness.
2. Risk limits and margin calls are triggered by drawdown, not volatility.
3. The time to recover from a drawdown ("time underwater") can exceed an investor's patience horizon.
4. Leverage amplifies drawdown non-linearly — a 50% drawdown requires a 100% gain to recover.

## Math Concepts

**Formal definition.** Let $V_t$ be the portfolio value (or cumulative return index) at time $t$ over $t \in \{0, 1, \ldots, T\}$. The drawdown at time $t$ is:

$$DD_t = \frac{\max_{s \leq t} V_s - V_t}{\max_{s \leq t} V_s}$$

The Maximum Drawdown is:

$$\text{MaxDD} = \max_{t \in [0,T]} DD_t = \max_{t \in [0,T]} \frac{\max_{s \leq t} V_s - V_t}{\max_{s \leq t} V_s}$$

This is always a non-negative number between 0 and 1 (or 0% and 100%). A MaxDD of 0.30 means the portfolio fell 30% from some prior peak.

**Calmar Ratio.** The most common drawdown-based performance metric:

$$\text{Calmar} = \frac{\text{Annualized Return}}{\text{MaxDD}}$$

Higher is better. A Calmar of 1.0 means you earn your MaxDD back each year. Calmar > 2 is considered strong. Typical hedge fund benchmarks target Calmar > 1.

**Recovery time (time underwater).** For each drawdown episode, define:
- **Drawdown start:** the date of the previous peak
- **Drawdown trough:** the date of the maximum loss within the episode
- **Recovery date:** the first date the portfolio returns to the prior peak
- **Duration:** number of periods from start to recovery (or to present if not yet recovered)

**Sterling Ratio.** Variant of Calmar that uses average of the worst annual drawdowns instead of the single maximum:

$$\text{Sterling} = \frac{\text{Annualized Return}}{\text{Avg of worst } k \text{ drawdowns}}$$

Less sensitive to a single extreme event than Calmar.

**Underwater curve.** Plot $-DD_t$ over time — visually shows all drawdown periods simultaneously. Essential in strategy tearsheets.

**Theoretical MaxDD for random walks.** For a Brownian motion with drift $\mu$ and volatility $\sigma$ over horizon $T$, the expected MaxDD grows as $O(\sigma\sqrt{T})$ for zero-drift processes. With positive drift, MaxDD is bounded. This gives intuition: in the long run, higher Sharpe strategies have lower relative drawdowns.

**Annualized Maximum Drawdown** is not a standard concept (MaxDD is path-dependent and does not decompose by year), but **rolling MaxDD** — computed over a trailing window — shows how the worst drawdown has evolved over time.

## Walkthrough

**Setup:** A strategy's cumulative return index (starting at 100) over 10 periods:

| Period | Portfolio Value | Running Peak | Drawdown |
|--------|----------------|--------------|---------|
| 0 | 100.0 | 100.0 | 0.0% |
| 1 | 105.0 | 105.0 | 0.0% |
| 2 | 112.0 | 112.0 | 0.0% |
| 3 | 108.0 | 112.0 | 3.6% |
| 4 | 103.0 | 112.0 | 8.0% |
| 5 | 97.0  | 112.0 | 13.4% |
| 6 | 94.0  | 112.0 | **16.1%** |
| 7 | 99.0  | 112.0 | 11.6% |
| 8 | 107.0 | 112.0 | 4.5% |
| 9 | 115.0 | 115.0 | 0.0% |
| 10 | 113.0 | 115.0 | 1.7% |

**Step 1:** Running peak = cumulative maximum of portfolio value.

**Step 2:** Drawdown at each point = (peak - value) / peak.

**Step 3:** MaxDD = maximum drawdown = 16.1% at period 6.

**Drawdown episode:**
- Peak date: period 2 (value = 112.0)
- Trough date: period 6 (value = 94.0)
- Recovery date: period 9 (value returns above 112.0 at period 9 = 115.0)
- Duration: 7 periods (periods 2 through 9)

**Calmar Ratio calculation:**
- Annualized return (rough): suppose the 10 periods represent 1 year → return = (115/100) - 1 ≈ 15% (using period 9 before the second dip)
- Calmar = 0.15 / 0.161 = **0.93** — just below 1.0, which is mediocre.

## Analysis

**Strengths:**
- Psychologically realistic — captures what actually drives investor redemptions and manager terminations.
- Path-dependent: penalizes strategies with long losing streaks even if mean and vol look fine.
- No distributional assumptions.
- Directly relevant to leverage decisions: MaxDD determines how much leverage causes ruin.
- Essential for stress-testing: "what is the worst this strategy has ever done?"

**Weaknesses:**
- Strongly path-dependent: a strategy run starting one month later might show a dramatically different MaxDD.
- Not additive across assets: cannot easily decompose portfolio MaxDD into constituent contributions.
- Sensitive to the measurement window — using 5 years of data vs. 10 years can give very different MaxDD for the same strategy.
- Single extreme event dominates: MaxDD is a worst-case metric; it can be "fooled" by a single bad period that does not repeat.
- No forward-looking meaning: historical MaxDD does not predict future MaxDD, especially if market conditions have changed.

**Known failure modes:**
- **Regime change:** A strategy with MaxDD of 8% during low-volatility 2012-2019 might have MaxDD of 40% in a crisis period. Historical MaxDD is a lower bound on future MaxDD.
- **Survivorship bias in tearsheets:** Strategies that had severe drawdowns and were shut down never make it into performance databases. Observed MaxDDs in hedge fund indices are understated.
- **Autocorrelated drawdowns:** In trending markets, drawdowns are larger and longer than i.i.d. models predict. Risk models that assume i.i.d. returns underestimate expected MaxDD.

**Practical guidelines:**
- MaxDD > 50%: requires a 100% gain to recover. Effectively requires starting over psychologically and often practically (margin calls, redemptions).
- MaxDD > 25%: most institutional investors will redeem.
- MaxDD < 10%: considered low-volatility, conservative.
- For a strategy targeting Sharpe = 1.5 with 15% vol, a rule of thumb is MaxDD ≈ 2× annual vol = 30% over a long horizon.

## Implementation

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ── 1. Core MaxDD computation ──────────────────────────────────────────────
def max_drawdown(returns: np.ndarray) -> float:
    """
    Compute Maximum Drawdown from a series of returns (not cumulative).
    Returns a positive number representing the worst peak-to-trough decline.
    
    E.g., MaxDD of 0.20 means the portfolio fell 20% from a prior peak.
    """
    # Build cumulative wealth index (starting at 1.0)
    cum_returns = np.cumprod(1 + returns)
    # Running peak (expanding max)
    running_peak = np.maximum.accumulate(cum_returns)
    # Drawdown at each point
    drawdowns = (running_peak - cum_returns) / running_peak
    return float(np.max(drawdowns))

def drawdown_series(returns: np.ndarray) -> np.ndarray:
    """Return the full drawdown time series (underwater curve)."""
    cum_returns  = np.cumprod(1 + returns)
    running_peak = np.maximum.accumulate(cum_returns)
    return (running_peak - cum_returns) / running_peak

# ── 2. Calmar Ratio ────────────────────────────────────────────────────────
def calmar_ratio(returns: np.ndarray, trading_days: int = 252) -> float:
    """
    Calmar Ratio = Annualized Return / Maximum Drawdown
    Higher is better. Values > 1 mean you recover MaxDD each year.
    """
    ann_return = np.mean(returns) * trading_days
    mdd        = max_drawdown(returns)
    if mdd == 0:
        return np.inf
    return float(ann_return / mdd)

# ── 3. Drawdown episodes: trough, duration, recovery ──────────────────────
def drawdown_episodes(returns: np.ndarray) -> pd.DataFrame:
    """
    Identify all distinct drawdown episodes with:
    - start (peak date), trough (lowest point), recovery (return to peak)
    - drawdown magnitude and duration
    """
    cum   = np.cumprod(1 + returns)
    peak  = np.maximum.accumulate(cum)
    dd    = (peak - cum) / peak
    
    episodes = []
    in_dd    = False
    start_i  = None
    
    for i in range(len(dd)):
        if not in_dd and dd[i] > 0.001:  # enter drawdown (> 0.1% to filter noise)
            in_dd   = True
            start_i = i - 1 if i > 0 else 0
            trough_i = i
            trough_dd = dd[i]
        elif in_dd:
            if dd[i] > trough_dd:
                trough_i  = i
                trough_dd = dd[i]
            if dd[i] < 0.001:  # recovered
                episodes.append({
                    'start':    start_i,
                    'trough':   trough_i,
                    'recovery': i,
                    'max_dd':   trough_dd,
                    'duration': i - start_i,
                    'recovery_time': i - trough_i
                })
                in_dd = False
    
    # Handle ongoing drawdown at end of series
    if in_dd:
        episodes.append({
            'start':    start_i,
            'trough':   trough_i,
            'recovery': None,
            'max_dd':   trough_dd,
            'duration': len(dd) - start_i,
            'recovery_time': None
        })
    
    return pd.DataFrame(episodes)

# ── 4. Demonstration ───────────────────────────────────────────────────────
np.random.seed(42)
n = 252 * 5  # 5 years

# Simulate a realistic strategy with fat tails and occasional crashes
base_returns = np.random.normal(0.0005, 0.01, n)
# Add two crash episodes
crash1 = np.zeros(n)
crash1[300:320] = -0.025   # ~50% annualized loss for 3 weeks
crash2 = np.zeros(n)
crash2[800:850] = -0.015   # sustained 5-week drawdown
returns = base_returns + crash1 + crash2

mdd    = max_drawdown(returns)
calmar = calmar_ratio(returns)
sharpe = np.mean(returns) / np.std(returns, ddof=1) * np.sqrt(252)
ann_r  = np.mean(returns) * 252

print(f"Strategy Metrics:")
print(f"  Annualized Return : {ann_r:.2%}")
print(f"  Sharpe Ratio      : {sharpe:.2f}")
print(f"  Maximum Drawdown  : {mdd:.2%}")
print(f"  Calmar Ratio      : {calmar:.2f}")

episodes = drawdown_episodes(returns)
if len(episodes) > 0:
    print(f"\nTop 3 Drawdown Episodes:")
    top3 = episodes.nlargest(3, 'max_dd')[['start', 'trough', 'recovery', 'max_dd', 'duration']]
    print(top3.to_string(index=False))

# ── 5. Visualize: Cumulative returns + underwater curve ───────────────────
cum_ret = np.cumprod(1 + returns)
dd_curve = drawdown_series(returns)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [2, 1]})

# Top panel: cumulative returns
ax1.plot(cum_ret, color='steelblue', linewidth=1.5, label='Portfolio Value')
ax1.set_ylabel('Portfolio Value (indexed to 1.0)')
ax1.set_title('Cumulative Returns and Drawdown')
ax1.legend()
ax1.grid(alpha=0.3)

# Bottom panel: underwater curve
ax2.fill_between(range(len(dd_curve)), -dd_curve * 100, 0,
                 color='red', alpha=0.4, label='Drawdown (%)')
ax2.axhline(-mdd * 100, color='darkred', linestyle='--',
            label=f'Max Drawdown: {mdd:.1%}')
ax2.set_ylabel('Drawdown (%)')
ax2.set_xlabel('Trading Day')
ax2.legend()
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('drawdown_chart.png', dpi=150)
plt.show()

# ── 6. Rolling MaxDD ───────────────────────────────────────────────────────
window = 252  # 1-year rolling window

def rolling_max_drawdown(returns: np.ndarray, window: int) -> np.ndarray:
    """Compute MaxDD over a rolling window."""
    result = np.full(len(returns), np.nan)
    for i in range(window, len(returns)):
        result[i] = max_drawdown(returns[i-window:i])
    return result

rolling_mdd = rolling_max_drawdown(returns, window)

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(rolling_mdd * 100, color='darkred', linewidth=1.5)
ax.fill_between(range(len(rolling_mdd)), rolling_mdd * 100, 0, alpha=0.3, color='red')
ax.set_title(f'Rolling {window}-Day Maximum Drawdown')
ax.set_xlabel('Trading Day')
ax.set_ylabel('Max Drawdown over trailing year (%)')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('rolling_drawdown.png', dpi=150)
plt.show()
```

## Bridge to Quant / ML

**Risk limits and circuit breakers.** Most systematic trading desks have a MaxDD-based kill switch: if the strategy exceeds a pre-specified drawdown (e.g., 10%), it is automatically paused for review. This is not Sharpe-based — it is purely path-dependent.

**Portfolio construction.** Target-MaxDD optimization: given a set of strategies, allocate weights to minimize the combined portfolio's expected MaxDD subject to a return target. This is an alternative to mean-variance optimization that directly controls the metric investors care about.

**Calmar as a selection criterion.** When comparing strategies that have passed the Sharpe threshold, Calmar ratio is often the tiebreaker. Two strategies with Sharpe = 1.5 but Calmar = 0.8 vs. Calmar = 2.5 are very different investments.

**ML connections:**
- **Objective function:** Some RL-trained trading agents use MaxDD as a direct penalty term in reward: $r_t = \text{P&L}_t - \lambda \cdot DD_t$. This trains the agent to be aware of drawdown, not just raw return.
- **Sequence model evaluation:** When evaluating time-series forecasting models for trading, rolling MaxDD in backtests is a more realistic metric than aggregate Sharpe because it reflects the experience of a trader following the model in real time.
- **Walk-forward robustness:** A model that has Sharpe = 2.0 in sample but MaxDD = 40% in a single out-of-sample month is likely overfit. Walk-forward MaxDD provides a conservative estimate of real-world risk.
- **Regime clustering:** K-means or HMM clustering on return distributions can identify regimes with historically high drawdown probability, enabling pre-emptive position reduction.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why does a 50% maximum drawdown require a 100% gain to recover, and what does this asymmetry imply for leverage decisions?
<details><summary>Answer</summary>If a portfolio falls from \$100 to \$50 (50% drawdown), it needs to go from \$50 back to \$100 — a 100% gain on the reduced base. The asymmetry comes from the multiplicative nature of returns: a -50% followed by a +50% leaves you at \$75, not \$100. $(1 - 0.5)(1 + 0.5) = 0.75$.

For leverage decisions: leverage amplifies drawdown dramatically. A 2× leveraged strategy with underlying drawdown of 30% experiences a portfolio drawdown of ~60% (approximately). A 60% drawdown requires a 150% gain to recover. This is why risk management practitioners treat MaxDD as the primary constraint on leverage — Kelly-sized positions based purely on expected return don't account for the survivability of the path.</details>

**Q2.** Two strategies have Sharpe = 1.5 over 5 years. Strategy A had MaxDD of 8%; Strategy B had MaxDD of 35%. As a portfolio manager at an institutional fund with investor redemption rights, which would you prefer, and what additional information would you want?
<details><summary>Answer</summary>Strategy A is strongly preferable in an institutional context. A MaxDD of 35% would likely trigger investor redemptions and potentially a mandate termination before recovery — the Sharpe over 5 years would never be realized by the investors who left at the trough. Institutional investors typically have drawdown tolerances of 15–25%, above which they redeem.

Additional information wanted: (1) Was Strategy B's MaxDD a single extreme event or sustained? Duration matters — a 35% drawdown with 2-month recovery is very different from one with 2-year recovery. (2) What caused the drawdown — systematic factor exposure or strategy-specific? A factor drawdown is more likely to recur. (3) Does the Sharpe account for the full 5-year period including the drawdown, or was it cherry-picked from the recovery period?</details>

**Q3.** Why is the "time underwater" (duration of a drawdown) often more important than the drawdown magnitude for real investors?
<details><summary>Answer</summary>Investors have finite patience and often have obligations that require portfolio liquidity at specific times. A 20% drawdown that lasts 2 weeks is tolerable; a 20% drawdown that lasts 3 years tests every investor's conviction to the breaking point — most will redeem before recovery. Additionally: (1) career risk — portfolio managers are evaluated on rolling performance windows; being "underwater" for 3 years ends careers regardless of eventual recovery; (2) pension funds and endowments have fixed spending requirements that force selling at depressed prices during long drawdowns; (3) margin-based strategies face margin calls during extended drawdowns even if they would eventually recover.</details>

---

### Level 2 — Quantitative

**Q4.** A strategy's cumulative wealth index evolves as follows (indexed to 100): 100, 108, 115, 122, 114, 106, 99, 103, 111, 118. Compute: (a) MaxDD; (b) the drawdown episode details (peak, trough, recovery, duration); (c) Calmar ratio assuming this represents 1 year of data.
<details><summary>Answer</summary>

Running peak at each period: 100, 108, 115, **122**, **122**, **122**, **122**, **122**, **122**, 122...wait, 118 < 122, so peak stays 122.

Drawdowns: 0, 0, 0, 0, (122-114)/122=6.6%, (122-106)/122=13.1%, (122-99)/122=**18.9%**, (122-103)/122=15.6%, (122-111)/122=9.0%, (122-118)/122=3.3%

(a) **MaxDD = 18.9%** at period 7 (value = 99)

(b) Episode: Peak at period 4 (value=122), Trough at period 7 (value=99), Not yet recovered by period 10 (value=118 < 122). Duration so far: 6 periods. Recovery time: not yet achieved.

(c) Annual return: $(118/100) - 1 = 18\%$ (using period 10; note portfolio hasn't returned to peak 122).

Calmar = 18% / 18.9% = **0.95** — slightly below 1.0, indicating the return barely covers the MaxDD. A Calmar of 1 is considered adequate; below 1 is mediocre.</details>

**Q5.** Strategy X has MaxDD = 25% and Calmar ratio = 0.8. Strategy Y has MaxDD = 40% and Calmar ratio = 1.6. (a) What is each strategy's annualized return? (b) If you add 2× leverage to Strategy Y, what is the approximate new MaxDD and new Calmar?
<details><summary>Answer</summary>

(a) Annual return = Calmar × MaxDD:
- Strategy X: $0.8 \times 25\% = \mathbf{20\%/\text{year}}$
- Strategy Y: $1.6 \times 40\% = \mathbf{64\%/\text{year}}$

(b) 2× leverage on Strategy Y:
- Levered return ≈ $2 \times 64\% - 1 \times r_{\text{borrow}}$ ≈ ~124% (assuming small borrowing cost)
- Levered MaxDD ≈ $2 \times 40\% = 80\%$ (leverage approximately doubles drawdown in a simple model, though in reality drawdown amplification with leverage is slightly worse)
- New Calmar ≈ $124\% / 80\% = \mathbf{1.55}$

The Calmar ratio decreases slightly because MaxDD amplification with leverage is worse than linear (a 40% drawdown on a levered position can trigger margin calls that force selling at the worst time, worsening actual drawdown beyond 80%).</details>

---

### Level 3 — Coding

**Q6.** The `drawdown_episodes` function tracks drawdowns by scanning through the time series in a loop. For a 10-year daily series (2,520 days), this is fast. But for a Monte Carlo simulation with 100,000 paths, looping over each path would be slow. Describe how you would vectorize MaxDD computation across many paths simultaneously using NumPy.
<details><summary>Answer</summary>

```python
def max_drawdown_vectorized(returns_matrix: np.ndarray) -> np.ndarray:
    """
    Compute MaxDD for each path (column) in a matrix.
    returns_matrix: shape (T, n_paths)
    Returns: MaxDD for each path, shape (n_paths,)
    """
    # Cumulative wealth: shape (T, n_paths)
    cum = np.cumprod(1 + returns_matrix, axis=0)
    # Running peak: expanding max along time axis
    running_peak = np.maximum.accumulate(cum, axis=0)
    # Drawdown matrix
    drawdowns = (running_peak - cum) / running_peak
    # MaxDD per path: max over time
    return np.max(drawdowns, axis=0)
```

Key: `np.maximum.accumulate(cum, axis=0)` vectorizes the running-peak computation across all paths simultaneously — the bottleneck in the serial loop. This runs 100–1000× faster than a Python loop because all operations are in NumPy's C backend. For 100,000 paths of 252 days each, the vectorized version runs in ~100ms vs. ~100 seconds for a pure Python loop.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| MaxDD is a forward-looking risk measure | MaxDD is purely backward-looking — it describes the historical worst case. Future MaxDD can easily exceed historical MaxDD, especially after regime changes. |
| Two strategies with the same MaxDD have similar risk | MaxDD captures magnitude but not duration or frequency. A 20% MaxDD lasting 3 years is far more damaging than a 20% MaxDD lasting 2 months. |
| Reducing volatility always reduces MaxDD | Not necessarily. A strategy with low daily volatility but strong positive autocorrelation (trending losses) can have a larger MaxDD than a higher-vol strategy with i.i.d. returns. |
| MaxDD cannot be decomposed by asset | True for the portfolio level. Individual asset drawdown metrics can be computed separately, but they don't add up to portfolio MaxDD due to path dependency across assets. |

## Related Concepts

- [[Sharpe Ratio]] — misses path dependence; Calmar ratio = return / MaxDD is the drawdown-aware complement
- [[Kelly Criterion]] — Kelly fraction implicitly assumes you can bear the variance; MaxDD shows whether the variance is actually bearable in practice
- [[Value at Risk]] — day-level loss; MaxDD is sustained multi-period loss; both needed for full risk picture
- [[Expected Shortfall]] — tail severity of daily losses; MaxDD is tail severity of sustained drawdown paths

## Sources Used

- Magdon-Ismail, M., & Atiya, A. F. (2004). Maximum drawdown. *Risk*, 17(10), 99-102
- Bailey, D. H., & Lopez de Prado, M. (2012). The Sharpe ratio efficient frontier. *Journal of Risk*, 15(2), 3-44

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review: no issues found | quality review |
