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
  - "Hull, Options Futures and Other Derivatives, ch. 22"
  - "Rockafellar & Uryasev (2000), Journal of Risk"
  - "Basel III FRTB (2019)"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Hedging & Risk → Gap 3: Need a single number summarizing how bad things can get
> **This concept:** ES fixes VaR's blind spot by averaging losses beyond the VaR threshold — asking "given we're in the worst X% of outcomes, how bad is it on average?"
> **Alternative approaches to this gap:** [[Value at Risk]]
> **You need first:** [[Value at Risk]]
> **This unlocks:** [[Markowitz Mean-Variance Optimization]], [[Risk Parity]], [[Stress Testing]]

## Why This Exists

**The gap:** VaR tells you where the loss threshold is but says nothing about how severe losses are beyond it. Two portfolios with identical VaR can have dramatically different actual tail losses — yet VaR assigns them the same risk number.

**What came before:** VaR (Gap 3 Solution A) solved the comparability problem but failed on a key theoretical property: subadditivity. A combined portfolio could have higher VaR than the sum of its parts, meaning VaR could actively penalize diversification.

**What this adds:** ES averages all losses beyond the VaR threshold, giving a tail-sensitive and coherent risk measure. It satisfies subadditivity — merging portfolios can never increase ES. The Rockafellar-Uryasev (2000) result showed ES can be minimized via linear programming, making it directly usable in portfolio optimization. Basel III.5 (FRTB) replaced 99% VaR with 97.5% ES as the regulatory standard.

**What it still doesn't solve:** ES is harder to backtest than VaR (you can't just count threshold breaches). With limited data, the tail average is statistically noisy. It also shares VaR's model risk: if your historical window misses a crisis regime, ES inherits the same blind spot.

[[Value at Risk]] has a specific blind spot: it tells you where the danger zone begins but says nothing about what happens once you enter it. Imagine a flood warning system that tells you "there's a 1% chance of flooding tonight" but gives no information about whether that flood will put 1 inch of water in your basement or wash the whole building away. Both scenarios exceed the threshold — VaR treats them identically.

Expected Shortfall (ES) fixes this by asking a follow-up question: *given that you are having a bad day (worse than VaR), how bad is it on average?* It is the average loss in the worst $1-\alpha$ fraction of outcomes. At 97.5% confidence, ES is the average of the worst 2.5% of days.

Think of it as the difference between knowing the speed limit and knowing the average speed of cars that run the red light. VaR is the speed limit. ES is the average speed of the violators — it captures the actual severity of the tail.

This matters enormously in finance because losses during crises are not just "a bit above VaR" — they can be 5x or 10x VaR. A measure that treats a -\$1.1M day the same as a -\$10M day, when VaR is \$1M, is badly miscalibrated for capital planning.

Basel III.5 (FRTB) replaced the 99% VaR standard with 97.5% ES precisely because ES is a **coherent risk measure** — it respects diversification and does not encourage perverse portfolio construction.

## Math Concepts

**Formal definition.** Let $L$ be portfolio loss (positive = money lost), $\alpha$ be the confidence level. ES (also called CVaR — Conditional Value at Risk, or TVaR — Tail VaR) is:

$$\text{ES}_\alpha = E\left[L \mid L > \text{VaR}_\alpha\right]$$

Equivalently, as an integral over the tail:

$$\text{ES}_\alpha = \frac{1}{1-\alpha} \int_\alpha^1 \text{VaR}_u \, du$$

This integral form is useful: ES is the *average VaR* over all confidence levels from $\alpha$ to 1. It smoothly incorporates the entire tail rather than a single quantile.

**Key properties (coherence axioms):**

ES satisfies all four axioms of a **coherent risk measure** (Artzner et al., 1999):

| Axiom | Meaning | ES satisfies? | VaR satisfies? |
|-------|---------|:---:|:---:|
| Monotonicity | Higher loss $\Rightarrow$ higher risk | Yes | Yes |
| Translation invariance | Adding cash reduces risk by that amount | Yes | Yes |
| Positive homogeneity | Double the position, double the risk | Yes | Yes |
| **Subadditivity** | Risk(A+B) $\leq$ Risk(A) + Risk(B) | **Yes** | **No** |

Subadditivity is the critical one: ES always rewards diversification. A merged portfolio can never have higher ES than the sum of its parts' ES values.

**Parametric ES (normal distribution).** If portfolio P&L is $N(\mu, \sigma^2)$, ES expressed as a positive loss amount is:

$$\text{ES}_\alpha = -\mu + \sigma \cdot \frac{\phi(z_\alpha)}{1 - \alpha}$$

where $\phi(\cdot)$ is the standard normal PDF, $z_\alpha = \Phi^{-1}(\alpha)$ is the $\alpha$-quantile of the standard normal, and $\Phi^{-1}$ is the inverse CDF. The $-\mu$ term reflects that a positive expected P&L reduces the tail loss, while $\sigma \cdot \phi(z_\alpha)/(1-\alpha)$ captures the tail severity.

At 97.5% confidence with $\mu = 0$: $z_{0.975} = 1.960$, $\phi(1.960) = 0.0584$, so:
$$\text{ES}_{97.5\%} = \sigma \cdot \frac{0.0584}{0.025} = 2.338\sigma$$

Compare to VaR$_{97.5\%} = 1.960\sigma$ (when $\mu = 0$) — ES is always larger than VaR (it is the average of everything worse than VaR).

**Relationship between VaR and ES:**

$$\text{ES}_\alpha \geq \text{VaR}_\alpha \quad \text{always}$$

The gap between them grows with tail heaviness. For a normal distribution the gap is modest; for a power-law distribution it can be enormous.

**Basel III.5 standard:** 97.5% ES (approximately equivalent in capital terms to 99% VaR for normal distributions, but better-behaved in stress scenarios).

## Walkthrough

**Setup:** We have 200 days of historical P&L. Mean daily P&L = 0, standard deviation = \$500,000.

**Step 1 — Sort the data.** Arrange all 200 P&L observations from worst to best. The worst 5% = bottom 10 observations (200 × 0.025 = 5 for 97.5% ES).

Suppose the 5 worst days show losses of:
- Day 1 (worst): -\$2,300,000
- Day 2: -\$1,800,000
- Day 3: -\$1,500,000
- Day 4: -\$1,200,000
- Day 5: -\$1,050,000

**Step 2 — Compute VaR.** The 97.5% VaR is the 2.5th percentile. With 200 observations, the 5th-worst day gives VaR = \$1,050,000.

**Step 3 — Compute ES.** Average of all observations worse than VaR:

$$\text{ES}_{97.5\%} = \frac{2{,}300{,}000 + 1{,}800{,}000 + 1{,}500{,}000 + 1{,}200{,}000 + 1{,}050{,}000}{5} = \frac{7{,}850{,}000}{5} = \$1{,}570{,}000$$

So while VaR says "threshold is \$1.05M," ES says "when you cross that threshold, expect to lose \$1.57M on average." The tail has 50% more severity than the threshold alone would suggest.

**Parametric check:** With $\sigma = \$500{,}000$ and $\mu = 0$ (so $-\mu = 0$):
$$\text{ES}_{97.5\%} = 0 + 500{,}000 \times 2.338 = \$1{,}169{,}000$$

The parametric estimate is lower because the normal distribution underestimates fat tails — common in real financial data.

## Analysis

**Strengths:**
- Coherent: satisfies subadditivity, rewards diversification properly.
- Captures tail severity, not just tail threshold.
- More stable than single-quantile VaR (averages over a range of tail outcomes).
- Regulatory standard under Basel III.5/FRTB.
- Better optimization properties: ES can be minimized using linear programming (Rockafellar & Uryasev 2000), which VaR cannot.

**Weaknesses:**
- Harder to backtest than VaR. VaR backtesting is simple: count breaches. ES backtesting requires estimating the average of unobserved tail outcomes, which demands more data and specialized tests (e.g., Acerbi-Szekely tests).
- Still assumes a specific historical window or distribution — tail estimates with limited data are noisy.
- Computationally more involved for complex portfolios (especially Monte Carlo).
- Does not fully resolve model risk: if your simulation misses a fat tail (e.g., no 2008 in the sample), ES inherits the same blind spot.

**Known failure modes:**
- **Sparse tails:** With only 250 trading days, 1% tail = 2-3 observations. Averaging 2 numbers is statistically unstable.
- **Non-stationarity:** Historical ES breaks down when the regime shifts (e.g., vol regime change between 2017 and 2018).
- **Joint tail dependence:** ES of individual assets does not easily compose into portfolio ES when assets exhibit tail correlation (they tend to crash together).

**Comparison table:**

| Property | VaR | ES |
|----------|-----|-----|
| Subadditive | No | Yes |
| Tail-sensitive | No | Yes |
| Easy to backtest | Yes | No |
| Regulatory use | Basel II | Basel III.5 |
| Optimization-friendly | No | Yes (LP) |

## Implementation

```python
import numpy as np
import pandas as pd
from scipy import stats

# ── 1. Synthetic fat-tailed P&L data ──────────────────────────────────────
np.random.seed(42)
n_days = 500
# Student-t with df=5: fatter tails than normal, realistic for equities
daily_pnl = stats.t.rvs(df=5, loc=0, scale=500_000, size=n_days)

# ── 2. Historical Simulation ES ───────────────────────────────────────────
def es_historical(pnl: np.ndarray, confidence: float = 0.975) -> tuple[float, float]:
    """
    Compute ES and VaR from historical P&L observations.
    Returns (ES, VaR) as positive loss amounts.
    
    ES = average loss in the worst (1-confidence) fraction of days.
    """
    losses = -pnl  # flip: positive = loss
    threshold = np.percentile(losses, confidence * 100)  # VaR threshold
    tail_losses = losses[losses > threshold]             # losses exceeding VaR
    es = float(np.mean(tail_losses)) if len(tail_losses) > 0 else threshold
    return es, float(threshold)

es_97, var_97 = es_historical(daily_pnl, 0.975)
es_99, var_99 = es_historical(daily_pnl, 0.990)

print("Historical Simulation:")
print(f"  97.5% VaR: ${var_97:>12,.0f}   ES: ${es_97:>12,.0f}")
print(f"  99.0% VaR: ${var_99:>12,.0f}   ES: ${es_99:>12,.0f}")

# ── 3. Parametric ES (Normal assumption) ──────────────────────────────────
def es_parametric_normal(sigma: float, mu: float = 0.0, confidence: float = 0.975) -> tuple[float, float]:
    """
    Closed-form ES under normality.
    ES_alpha = mu + sigma * phi(z_alpha) / (1 - alpha)
    where phi is the standard normal PDF at the alpha-quantile.
    """
    z_alpha = stats.norm.ppf(confidence)            # e.g., 1.96 at 97.5%
    phi_z   = stats.norm.pdf(z_alpha)               # PDF at that quantile
    var     = -(mu + stats.norm.ppf(1 - confidence) * sigma)
    es      = -(mu - sigma * phi_z / (1 - confidence))
    return float(es), float(var)

sigma_hat = np.std(daily_pnl, ddof=1)
es_p97, var_p97 = es_parametric_normal(sigma_hat, confidence=0.975)
print(f"\nParametric Normal (sigma=${sigma_hat:,.0f}):")
print(f"  97.5% VaR: ${var_p97:>12,.0f}   ES: ${es_p97:>12,.0f}")

# ── 4. ES via integral of VaR (numerical, works for any distribution) ──────
def es_integral(pnl: np.ndarray, confidence: float = 0.975, n_grid: int = 1000) -> float:
    """
    ES = (1/(1-alpha)) * integral from alpha to 1 of VaR_u du
    Approximated by averaging VaR across a fine grid of confidence levels.
    """
    alphas = np.linspace(confidence, 1.0 - 1e-6, n_grid)
    vars_   = [-np.percentile(pnl, u * 100) for u in alphas]
    return float(np.mean(vars_))

es_integral_val = es_integral(daily_pnl, 0.975)
print(f"\nIntegral method 97.5% ES: ${es_integral_val:,.0f}")

# ── 5. ES as an LP objective (Rockafellar-Uryasev formulation) ─────────────
# CVaR can be minimized as a convex objective:
#   ES_alpha(L) = min_{z} { z + (1/(1-alpha)) * E[max(L-z, 0)] }
# This is the foundation for ES-based portfolio optimization.
# For demonstration, compute it numerically:
def es_rockafellar_uryasev(pnl: np.ndarray, confidence: float = 0.975) -> float:
    """
    Rockafellar-Uryasev formula: efficient for optimization.
    Minimizes over threshold z: z + mean(max(-pnl - z, 0)) / (1-alpha)
    """
    losses = -pnl
    alpha = confidence
    from scipy.optimize import minimize_scalar
    
    def objective(z):
        return z + np.mean(np.maximum(losses - z, 0)) / (1 - alpha)
    
    result = minimize_scalar(objective, bounds=(losses.min(), losses.max()), method='bounded')
    return float(result.fun)

es_ru = es_rockafellar_uryasev(daily_pnl, 0.975)
print(f"Rockafellar-Uryasev 97.5% ES: ${es_ru:,.0f}")

# ── 6. Backtesting ES (simplified Acerbi-Szekely style) ────────────────────
def backtest_es(pnl: np.ndarray, es_estimate: float, confidence: float = 0.975) -> dict:
    """
    Simple ES backtest: compare average tail loss to ES estimate.
    Z-score indicates whether realized tail losses are above model predictions.
    """
    losses = -pnl
    var_threshold = np.percentile(losses, confidence * 100)
    tail_mask  = losses > var_threshold
    tail_losses = losses[tail_mask]
    
    realized_es   = np.mean(tail_losses)
    n_tail        = len(tail_losses)
    se_realized   = np.std(tail_losses, ddof=1) / np.sqrt(n_tail) if n_tail > 1 else np.nan
    z_score       = (realized_es - es_estimate) / se_realized if se_realized > 0 else np.nan
    
    return {
        "n_tail_observations": n_tail,
        "realized_ES": realized_es,
        "model_ES": es_estimate,
        "z_score": z_score,
        "verdict": "PASS" if abs(z_score) < 1.96 else "FAIL"
    }

bt = backtest_es(daily_pnl, es_97, 0.975)
print(f"\nES Backtest: {bt}")
```

## Bridge to Quant / ML

**Portfolio optimization with ES.** The Rockafellar-Uryasev (2000) formulation rewrites ES minimization as a linear program. This means you can build a minimum-ES portfolio — analogous to minimum-variance (Markowitz) but using the tail as the objective. This is widely used in risk parity and tail-risk hedging strategies.

**Regulatory capital (FRTB):** Banks must compute ES at 97.5% over multiple liquidity horizons (10-day for liquid products, 60-day for illiquid). The capital charge is directly proportional to ES. Understanding ES is prerequisite for working in any bank risk or trading desk.

**ML connections:**
- **Quantile regression extended:** ES = integral of quantile regression predictions over the tail. A neural network trained to predict multiple quantiles (via pinball loss) can compute ES by averaging predictions above the VaR quantile.
- **Tail risk in reinforcement learning:** RL agents trained on financial simulations can use ES as the penalty term in the reward function: maximize $E[R] - \lambda \cdot \text{ES}(R)$, which directly trades off mean return against tail risk.
- **Distributional RL (IQN, QR-DQN):** These models learn the full return distribution, enabling direct computation of ES without a parametric assumption.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why does subadditivity matter for a risk measure used in portfolio construction?
<details><summary>Answer</summary>A subadditive risk measure satisfies: Risk(A+B) ≤ Risk(A) + Risk(B). This means combining two portfolios can never increase risk, which correctly reflects diversification. A non-subadditive measure like VaR can produce paradoxes where splitting a portfolio across entities appears to reduce risk without any actual diversification — creating incentives for regulatory arbitrage. For portfolio optimization, only subadditive measures reward diversification appropriately. ES is subadditive; VaR is not.</details>

**Q2.** Explain the integral definition of ES: $\text{ES}_\alpha = \frac{1}{1-\alpha} \int_\alpha^1 \text{VaR}_u \, du$. What is the intuition behind averaging VaR across confidence levels?
<details><summary>Answer</summary>VaR at level $u$ is the loss threshold at the $u$-th quantile. For $u$ ranging from $\alpha$ to 1, you are computing VaR at every possible confidence level in the tail. Averaging these gives the "expected VaR" across the entire tail region — or equivalently, the expected loss conditional on being in the worst $(1-\alpha)$ fraction of outcomes. This integral formulation is useful because it shows ES is a smooth aggregation of quantile information, not just a single point — making it more stable and richer in tail information than VaR alone.</details>

**Q3.** Why is ES harder to backtest than VaR, and what kind of test is used?
<details><summary>Answer</summary>VaR backtesting is simple: count how many days the loss exceeded the VaR threshold and compare to the expected frequency (e.g., 1% of days for 99% VaR). ES backtesting is harder because you need to estimate the *average* loss in the tail, not just count exceedances. This requires observing multiple tail events and averaging them — which is statistically noisy with limited data. The Acerbi-Szekely (2014) tests are the standard approach: they compare the empirical tail average to the model ES estimate and construct a Z-score, but require hundreds of tail observations to be reliable.</details>

---

### Level 2 — Quantitative

**Q4.** A portfolio has mean daily P&L = \$0 and daily standard deviation \$\sigma = \$400{,}000$. Compute the parametric 97.5% ES under the normal distribution assumption. Compare it to the parametric 97.5% VaR.
<details><summary>Answer</summary>

Parametric ES formula (with $\mu = 0$): $\text{ES}_{97.5\%} = \sigma \cdot \frac{\phi(z_{0.975})}{1 - 0.975}$

$z_{0.975} = 1.960$, $\phi(1.960) = 0.0584$

$$\text{ES}_{97.5\%} = \$400{,}000 \times \frac{0.0584}{0.025} = \$400{,}000 \times 2.338 = \$935{,}200$$

For comparison, parametric 97.5% VaR: $\text{VaR}_{97.5\%} = 1.960 \times \$400{,}000 = \$784{,}000$

ES is 19% larger than VaR at the same confidence level. The gap would be much larger with fat-tailed returns, because ES averages over more severe tail losses.</details>

**Q5.** You have 500 days of historical P&L. The 12 worst days (sorted worst to best) show losses of: $3.2M, $2.8M, $2.4M, $2.1M, $1.9M, $1.7M, $1.6M, $1.5M, $1.4M, $1.3M, $1.25M, $1.2M. Compute: (a) 97.5% historical VaR; (b) 97.5% historical ES.
<details><summary>Answer</summary>

With 500 observations at 97.5% confidence: tail contains $500 \times 0.025 = 12.5 \approx 12$ or 13 observations depending on convention. Using 12 tail observations:

(a) **97.5% VaR** = the loss at the boundary of the tail. The 12th-worst loss = **\$1.2M** (the edge of the 12-observation tail).

(b) **97.5% ES** = average of the 12 worst losses:

$$\text{ES} = \frac{3.2 + 2.8 + 2.4 + 2.1 + 1.9 + 1.7 + 1.6 + 1.5 + 1.4 + 1.3 + 1.25 + 1.2}{12} = \frac{22.35}{12} = \$1.863\text{M}$$

ES is 55% larger than VaR — the tail has significant severity beyond the threshold.</details>

---

### Level 3 — Coding

**Q6.** The `es_parametric_normal` function computes both ES and VaR. Explain the formula `var = -(mu + stats.norm.ppf(1 - confidence) * sigma)`. Then describe how you would modify this function to compute ES under a Student-t distribution instead of normal, and why this matters for equity portfolios.
<details><summary>Answer</summary>

`stats.norm.ppf(1 - confidence)` at 97.5% gives `ppf(0.025) = -1.96` (the left tail quantile). Multiplying by sigma gives the 2.5th percentile of the P&L distribution (negative). The leading negative sign flips it to a positive loss amount. So VaR = $-(μ + z_{low} \cdot σ)$ = $-μ + |z| \cdot σ$.

For Student-t ES: replace `stats.norm.ppf` with `stats.t.ppf(df=df)` and replace `stats.norm.pdf` with `stats.t.pdf(df=df)` in the PDF evaluation. The closed-form t-distribution ES is:

$$\text{ES}_\alpha^{(t)} = \sigma \cdot \frac{f_t(t_\alpha)}{1-\alpha} \cdot \frac{\nu + t_\alpha^2}{\nu - 1}$$

where $f_t$ is the t-PDF, $t_\alpha$ is the $\alpha$-quantile of the t-distribution, and $\nu$ is degrees of freedom.

This matters because equity returns have fat tails (kurtosis >> 3). A normal-based ES underestimates tail severity by 20–50% for realistic equity return distributions. The t-distribution with $\nu = 4$–$6$ degrees of freedom is a better empirical fit.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| ES is always 2× VaR | The ratio ES/VaR depends on the tail shape. Under normality it's about 1.2–1.4x; under fat tails it can be 2–5x. |
| ES eliminates model risk | ES still depends on the accuracy of the return distribution. A model that misses a fat tail gives understated ES. |
| Higher confidence ES is always better | 99.9% ES requires estimating a very sparse tail. With limited data, it has huge estimation error and can be less useful than 97.5% ES. |
| ES cannot be optimized directly | False. The Rockafellar-Uryasev (2000) formulation makes ES minimization a linear program — more tractable than VaR optimization. |

## Related Concepts

- [[Value at Risk]] — the threshold metric that ES averages beyond
- [[Factor Models]] — factor decomposition reveals which factors drive the tail
- [[Maximum Drawdown]] — path-dependent tail risk; complements ES for strategy evaluation
- [[Sharpe Ratio]] — mean/vol ratio; ignores the tail that ES captures

## Sources Used

- Hull, J. (2022). *Options, Futures and Other Derivatives*, 11th ed., ch. 22
- Rockafellar, R. T., & Uryasev, S. (2000). Optimization of conditional value-at-risk. *Journal of Risk*, 2(3), 21-41
- Artzner, P. et al. (1999). Coherent measures of risk. *Mathematical Finance*, 9(3), 203-228
- Basel Committee on Banking Supervision (2019). *Minimum Capital Requirements for Market Risk (FRTB)*

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review: fixed parametric ES sign convention (formula now ES = -μ + σ·φ(z)/(1-α) as positive loss, consistent with implementation); updated walkthrough | quality review |
