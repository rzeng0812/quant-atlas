---
type: concept
domain: 30-Models
tags: [risk, portfolio]
status: math
stability: evolving
confidence: high
last_reviewed: 2026-04-12
review_interval_days: 90
sources:
  - "Hull, Options Futures and Other Derivatives, ch. 21"
  - "Jorion, Value at Risk, 3rd ed."
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Hedging & Risk → Gap 3: Need a single number summarizing how bad things can get
> **This concept:** VaR answers "what is the worst loss we will not exceed with X% probability over horizon T?" — a single threshold number for regulatory reporting and position limits.
> **Alternative approaches to this gap:** [[Expected Shortfall]]
> **You need first:** [[Option Greeks]], [[Delta Hedging]]
> **This unlocks:** [[Expected Shortfall]], [[Stress Testing]], [[Factor Models]]

## Why This Exists

**The gap:** Risk managers and regulators needed a single, comparable number that answered "how bad can things get?" across desks, firms, and asset classes. Greeks describe sensitivity at a point; they say nothing about potential losses over a horizon.

**What came before:** The Option Greeks (delta, gamma, vega) gave precise local sensitivities, but they could not be collapsed into a single dollar loss figure for regulatory capital purposes. Different desks used incomparable risk metrics.

**What this adds:** VaR converts the entire loss distribution into one number — the loss threshold exceeded only 1% (or 5%) of the time. This enabled the Basel II capital regime: every bank reports a 10-day 99% VaR, and capital requirements are proportional to it. It made cross-firm risk comparison possible for the first time.

**What it still doesn't solve:** VaR says nothing about how bad losses are *beyond* the threshold. A portfolio losing \$1.1M and a portfolio losing \$50M on bad days can have identical VaR of \$1M. It also violates subadditivity — it can penalize diversification rather than reward it.

Imagine you manage the trading book at a bank. At the end of every day, your boss asks one question: "What is the most we could lose tomorrow?" That is exactly the question Value at Risk (VaR) tries to answer — with one important qualifier: *most of the time*.

Think of it like a flood plain analogy. Engineers say a region has a "100-year flood level" of 10 feet — meaning a flood that bad happens only about 1% of years. They do not promise you will never see 11 feet; they just tell you the threshold that is breached rarely. VaR works the same way. A 1-day 99% VaR of \$1 million means: on any given day, there is a 99% chance you lose *less* than \$1 million. Only 1 day in 100 would you expect to exceed that threshold.

This framing made VaR irresistible to regulators. Basel II required banks to hold capital proportional to their 10-day 99% VaR. It is a single dollar number that management can monitor, compare across desks, and report to regulators. That simplicity is also its biggest weakness — it tells you nothing about how bad things get when you do cross the threshold.

## Math Concepts

**Formal definition.** Let $L$ be the portfolio loss over a horizon $T$ (positive $L$ = money lost). The VaR at confidence level $\alpha$ is:

$$\text{VaR}_\alpha = \inf \{ l \in \mathbb{R} : P(L > l) \leq 1 - \alpha \}$$

Equivalently, it is the $\alpha$-quantile of the loss distribution. At $\alpha = 0.99$, VaR is the 99th percentile of losses — only 1% of outcomes are worse.

**Three calculation methods:**

**1. Historical simulation** — the most transparent approach.
- Collect the last $N$ days of P&L (mark-to-market changes).
- Sort from worst to best.
- VaR at 99% = the loss at the 1st percentile of that sorted history.
- No distributional assumptions. Captures fat tails that were actually observed. But it is fully backward-looking and slow to adapt to regime changes.

**2. Parametric (variance-covariance)** — assumes returns are normally distributed.

$$\text{VaR}_\alpha = -\mu + z_\alpha \cdot \sigma$$

where $\mu$ is the expected P&L (often set to 0 for short horizons), $\sigma$ is the portfolio standard deviation, and $z_\alpha$ is the positive z-score at confidence level $\alpha$ (i.e., $z_\alpha = \Phi^{-1}(\alpha)$, which is positive for $\alpha > 0.5$). VaR is expressed as a positive loss amount.

| Confidence | $\alpha$ | $z_\alpha$ |
|-----------|---------|-----------|
| 95% | 0.95 | 1.645 |
| 99% | 0.99 | 2.326 |
| 99.9% | 0.999 | 3.090 |

Fast and analytically tractable. Breaks down when returns are non-normal (fat tails, skew).

**3. Monte Carlo** — simulate many possible future scenarios (e.g., 100,000 paths), compute P&L for each, then take the appropriate percentile. Most flexible, computationally expensive.

**Scaling VaR across horizons.** Under the square-root-of-time rule (i.i.d. normal returns):

$$\text{VaR}_{T\text{-day}} = \text{VaR}_{1\text{-day}} \times \sqrt{T}$$

This is a common regulatory approximation. It breaks down when returns are autocorrelated or fat-tailed.

**Key non-property: VaR is NOT subadditive.** A coherent risk measure should satisfy: risk of a combined portfolio $\leq$ sum of individual risks. VaR can violate this. Two positions each with VaR = \$100 could have a combined VaR of \$250. This means VaR can *discourage* diversification in certain cases.

## Walkthrough

**Setup:** A portfolio has daily returns with mean $\mu = 0$ and standard deviation $\sigma = \$200{,}000$.

**Parametric 1-day 99% VaR:**
$$\text{VaR}_{99\%} = -0 + 2.326 \times \$200{,}000 = \$465{,}200$$

Interpretation: On 99 out of 100 trading days, we expect to lose less than \$465,200.

**Historical simulation example:**

Suppose we have 500 days of P&L data. Sort ascending (most negative first):
- Day rank 1 (worst): -\$850,000
- Day rank 2: -\$710,000
- Day rank 3: -\$620,000
- Day rank 4: -\$580,000
- Day rank 5: -\$490,000
- ...

At 99% confidence with 500 observations, the 1% tail contains 5 observations. The 99% VaR = the 5th-worst loss = **\$490,000** (as a positive number representing a loss).

Note: the parametric and historical methods give different answers because historical data has fat tails — extreme events are more common than a normal distribution predicts.

**10-day scaling (Basel II style):**
$$\text{VaR}_{10\text{-day}} = \$465{,}200 \times \sqrt{10} = \$1{,}470{,}800$$

## Analysis

**Strengths:**
- Single intuitive number — easy to communicate to non-technical stakeholders.
- Fast to compute parametrically; only requires portfolio sigma.
- Widely standardized — Basel II/III compliance, cross-firm comparisons.
- Historical simulation requires no distribution assumption.

**Weaknesses:**
- Not coherent: violates subadditivity, so portfolio VaR can exceed sum of parts.
- Tells you nothing about the severity of losses *beyond* the threshold (tail shape blindness).
- Parametric VaR systematically underestimates tail risk in equity returns (fat tails, negative skew).
- Historical simulation is backward-looking: if 2008 is not in your window, it is not in your VaR.
- Sensitive to choice of confidence level and horizon — easy to game by changing parameters.
- Does not account for liquidity: a \$10M position may have a 2-week liquidation horizon, not 1 day.

**Known failure modes:**
- **Procyclicality:** Low volatility periods produce low VaR, encouraging leverage. When vol spikes, VaR spikes and forces deleveraging — amplifying the crisis.
- **Model risk:** Banks using the same parametric model face correlated risk limits; everyone sells at once.
- **Cliff effect:** Two strategies with identical VaR can have radically different tail behavior.

**Regulatory evolution:** Basel II used 10-day 99% VaR. Basel III.5 (FRTB, Fundamental Review of the Trading Book) replaced VaR with 97.5% [[Expected Shortfall]], which is coherent and better captures tail risk.

## Implementation

```python
import numpy as np
import pandas as pd
from scipy import stats

# ── 1. Generate synthetic daily P&L data ──────────────────────────────────
np.random.seed(42)
n_days = 500
# Fat-tailed returns: use Student-t with df=4 degrees of freedom
daily_pnl = stats.t.rvs(df=4, loc=0, scale=200_000, size=n_days)

# ── 2. Historical Simulation VaR ──────────────────────────────────────────
def var_historical(pnl: np.ndarray, confidence: float = 0.99) -> float:
    """
    Returns VaR as a positive number (loss amount).
    At 99% confidence, 1% of days are worse than this.
    """
    # VaR is the negative of the alpha-quantile of P&L
    # (low P&L = big loss; we want the threshold at the bottom 1%)
    return float(-np.percentile(pnl, (1 - confidence) * 100))

var_99_hist = var_historical(daily_pnl, 0.99)
var_95_hist = var_historical(daily_pnl, 0.95)
print(f"Historical 99% VaR: ${var_99_hist:,.0f}")
print(f"Historical 95% VaR: ${var_95_hist:,.0f}")

# ── 3. Parametric (Normal) VaR ────────────────────────────────────────────
def var_parametric(sigma: float, mu: float = 0.0, confidence: float = 0.99) -> float:
    """
    Assumes normal distribution.
    VaR = -(mu - z * sigma)  expressed as a positive loss.
    """
    z = stats.norm.ppf(1 - confidence)   # z is negative, e.g., -2.326 at 99%
    return float(-(mu + z * sigma))      # flip sign so loss is positive

sigma_est = np.std(daily_pnl, ddof=1)
var_99_param = var_parametric(sigma_est, confidence=0.99)
print(f"\nParametric 99% VaR: ${var_99_param:,.0f}")
print(f"  (sigma estimate: ${sigma_est:,.0f})")

# ── 4. Scale to multi-day horizon (square-root-of-time rule) ──────────────
def scale_var(var_1day: float, horizon_days: int) -> float:
    """
    Approximate T-day VaR from 1-day VaR.
    Assumes i.i.d. normal returns -- use with caution.
    """
    return var_1day * np.sqrt(horizon_days)

var_10day = scale_var(var_99_param, 10)
print(f"\n10-day 99% VaR (scaled): ${var_10day:,.0f}")

# ── 5. Backtesting: count VaR breaches ───────────────────────────────────
# A breach occurs when actual loss exceeds VaR
losses = -daily_pnl  # flip sign: positive = loss
breaches = np.sum(losses > var_99_param)
expected_breaches = n_days * 0.01
print(f"\nVaR Backtesting (99% parametric over {n_days} days):")
print(f"  Observed breaches : {breaches}")
print(f"  Expected breaches : {expected_breaches:.1f}")
print(f"  Breach rate       : {breaches/n_days:.2%}")

# ── 6. Visualize the loss distribution with VaR threshold ────────────────
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(-daily_pnl / 1e6, bins=50, color='steelblue', alpha=0.7, label='Daily P&L (loss)')
ax.axvline(var_99_hist / 1e6, color='red',    linestyle='--', label=f'Hist 99% VaR: ${var_99_hist/1e6:.2f}M')
ax.axvline(var_99_param / 1e6, color='orange', linestyle='--', label=f'Param 99% VaR: ${var_99_param/1e6:.2f}M')
ax.set_xlabel('Loss ($M)')
ax.set_ylabel('Frequency')
ax.set_title('Loss Distribution with VaR Thresholds')
ax.legend()
plt.tight_layout()
plt.savefig('var_distribution.png', dpi=150)
plt.show()
```

## Bridge to Quant / ML

**Portfolio management:** VaR is used to set position limits. A desk with a \$5M daily VaR limit must reduce positions if estimated VaR exceeds that threshold. This creates a direct link between risk models and trade execution.

**Risk budgeting:** Decompose portfolio VaR into contributions by asset or strategy. Assets that add more VaR than their expected return justifies are candidates for reduction.

**ML connections:**
- Quantile regression naturally estimates VaR: train a model with the pinball loss at quantile $\alpha$ and you directly predict the $\alpha$-th percentile of the loss distribution.
- Time-series models (GARCH) are often used to produce dynamic volatility estimates $\sigma_t$ for parametric VaR, feeding a time-varying $\sigma$ rather than a constant.
- Conformal prediction in ML uses a similar logic: instead of "99% chance loss is less than X," conformal intervals say "99% coverage of true label by the prediction interval."

**Regulatory context:** Any firm subject to Basel III must report VaR (even though ES is now the primary capital metric). Understanding VaR is prerequisite for understanding the FRTB framework.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why was VaR adopted by regulators rather than the Option Greeks, even though Greeks are more mathematically precise?
<details><summary>Answer</summary>Greeks are local sensitivities — they describe how risk changes at a specific point, not how bad things can get over a horizon. Regulators needed a single comparable dollar loss number across all desks and firms. VaR collapses the entire loss distribution into one threshold number, enabling the Basel II capital regime to set capital proportional to a standardized metric.</details>

**Q2.** What does it mean for VaR to be "not subadditive," and why is this a problem?
<details><summary>Answer</summary>Subadditivity means the risk of a combined portfolio should be no greater than the sum of the individual risks — risk should not increase from diversification. VaR can violate this: two portfolios each with VaR = \$100 could have a combined VaR of \$250. This means a merged portfolio looks riskier than its parts, which perversely discourages diversification. It also means risk limits set in terms of VaR can be gamed by splitting a single position across legal entities.</details>

**Q3.** A portfolio has a 1-day 99% VaR of \$500,000. What does this statement mean precisely, and what does it NOT tell you?
<details><summary>Answer</summary>It means: on any given trading day, there is a 99% probability the portfolio loses less than \$500,000. Equivalently, only 1 day in 100 should exceed this threshold. It does NOT tell you: (a) how bad losses are on those 1-in-100 days — they could be \$501,000 or \$50,000,000; (b) whether the distribution is symmetric or skewed; (c) what happens during a systemic crisis not represented in the historical data used to compute VaR.</details>

---

### Level 2 — Quantitative

**Q4.** A portfolio has mean daily P&L = \$0 and daily standard deviation = \$300,000. Compute the parametric 1-day VaR at 95% and 99% confidence. Then compute the 10-day 99% VaR using the square-root-of-time rule.
<details><summary>Answer</summary>

Parametric VaR formula: $\text{VaR}_\alpha = -\mu + z_\alpha \cdot \sigma$

At 95%: $z_{0.95} = 1.645$
$$\text{VaR}_{95\%} = 0 + 1.645 \times \$300{,}000 = \$493{,}500$$

At 99%: $z_{0.99} = 2.326$
$$\text{VaR}_{99\%} = 0 + 2.326 \times \$300{,}000 = \$697{,}800$$

10-day scaling: $\text{VaR}_{10\text{-day}} = \$697{,}800 \times \sqrt{10} = \$697{,}800 \times 3.162 = \$2{,}206{,}000$

Note the 10-day rule assumes i.i.d. normal returns. For fat-tailed returns or autocorrelation, this understates the true 10-day VaR.</details>

**Q5.** You have 400 days of historical P&L data. The 4 worst daily losses are: $1,200,000; $950,000; $820,000; $710,000. What is the historical simulation 99% VaR?
<details><summary>Answer</summary>

At 99% confidence with 400 observations, the 1% tail contains $400 \times 0.01 = 4$ observations.

The historical simulation 99% VaR is the 4th-worst loss = **\$710,000**.

(The VaR threshold is the loss at the boundary of the tail — the worst loss you should expect to stay within 99% of the time. Losses on the 4 worst days exceed this threshold.)

Note: if the question asked for the 1st-worst-loss-included VaR using a strict quantile definition, some implementations take VaR as the loss at rank $\lceil n(1-\alpha) \rceil = 4$, which gives \$710,000, while others use rank 4 directly. The key point is the VaR is in the range \$710{,}000–1{,}200{,}000$ depending on interpolation convention.</details>

---

### Level 3 — Coding

**Q6.** The code uses `stats.norm.ppf(1 - confidence)` to get the z-score, then negates it to produce a positive VaR. Walk through why this sign convention is correct, and identify one change you would make to the `var_historical` function to make it return a negative number (a loss) rather than a positive number.
<details><summary>Answer</summary>

`stats.norm.ppf(1 - confidence)` at confidence = 0.99 gives `ppf(0.01) = -2.326` — a negative z-score, since we want the left tail. Multiplying by $\sigma$ and subtracting $\mu$ gives a negative number (a loss). Negating it produces a positive VaR representing the loss magnitude.

To return a negative number (signed loss) from `var_historical`, change:
```python
return float(-np.percentile(pnl, (1 - confidence) * 100))
```
to:
```python
return float(np.percentile(pnl, (1 - confidence) * 100))
```
This returns the raw percentile of the P&L distribution — which is negative for losses — without flipping the sign.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| VaR tells you the maximum you can lose | VaR is a threshold, not a maximum. On the 1% of days that exceed 99% VaR, losses can be many times larger. |
| Higher confidence VaR is always safer | Higher confidence VaR is a wider loss threshold — it's a different question, not a safer portfolio. |
| VaR from different firms are directly comparable | Only if they use the same confidence level, horizon, and methodology. Parametric vs. historical VaR for the same portfolio can differ substantially. |
| The square-root-of-time rule is always valid | It assumes i.i.d. normal returns. It fails with autocorrelated returns, fat tails, or illiquid positions. |

## Related Concepts

- [[Expected Shortfall]] — fixes VaR's coherence failure; standard in Basel III.5
- [[Factor Models]] — used to decompose portfolio variance into factor/idiosyncratic components before computing VaR
- [[Sharpe Ratio]] — complementary performance metric; VaR is a loss metric, Sharpe is a return/risk ratio
- [[Maximum Drawdown]] — path-dependent risk measure; captures sustained losses VaR ignores

## Sources Used

- Hull, J. (2022). *Options, Futures and Other Derivatives*, 11th ed., ch. 21 — VaR estimation methods
- Jorion, P. (2006). *Value at Risk*, 3rd ed. — comprehensive reference for historical, parametric, Monte Carlo
- Basel Committee on Banking Supervision (2019). *Minimum Capital Requirements for Market Risk (FRTB)*

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review: fixed parametric VaR sign convention (formula now VaR = -μ + z·σ as positive loss); updated walkthrough notation | quality review |
