---
type: concept
domain: 30-Models
tags: [portfolio, risk, allocation]
status: math
stability: evolving
confidence: medium
last_reviewed: 2026-04-18
review_interval_days: 90
sources:
  - "Roncalli - Introduction to Risk Parity and Budgeting (2013)"
  - "Qian - Risk Parity and Diversification (2011)"
  - "Bridgewater Associates - All Weather Strategy"
created: 2026-04-18
---

> [!info] Problem Chain
> **Chain:** Hedging & Risk → Gap 5: Markowitz is unstable — inputs are unreliable, outputs are extreme
> **This concept:** Risk Parity abandons expected return estimation entirely and allocates capital so that each asset contributes equally to total portfolio risk — making portfolios robust to return estimation error.
> **Alternative approaches to this gap:** [[CAPM]], [[Factor Models]], [[Black-Litterman]], [[Hierarchical Risk Parity]]
> **You need first:** [[Markowitz Mean-Variance Optimization]], [[Correlation and Covariance Estimation]]
> **This unlocks:** [[Hierarchical Risk Parity]]

## Why This Exists

**The gap:** MVO and its improvements (BL, factor models) still require expected return estimates, which are unreliable. Is there a way to build a portfolio that is robust to return uncertainty altogether?

**What came before:** All classical portfolio optimization methods required expected return inputs. Even simple heuristics like equal-weighting ignore the vast differences in volatility across asset classes — a 60/40 portfolio is nominally diversified but 90% equity risk.

**What this adds:** Risk Parity abandons return estimation entirely. It allocates capital so each asset contributes equally to total portfolio risk ($\text{RC}_i = \sigma_P / N$). This is the first purely risk-based allocation method that does not require any return forecast. Bridgewater's All Weather strategy demonstrated this approach could work across different macroeconomic regimes.

**What it still doesn't solve:** Risk Parity almost always requires leverage to bring the bond-heavy portfolio up to target volatility. The critical assumption — that assets diversify each other — fails when correlations converge in crises (2022: both bonds and stocks fell simultaneously). The flat version ignores correlation structure, which HRP addresses.

Here is a surprising fact: the "60/40" portfolio — 60% stocks, 40% bonds — that most retirement accounts are built on is not actually 60/40 in any meaningful sense. Because stocks are roughly 4× more volatile than bonds, the *risk* coming from equities is about 90% of total portfolio risk. The bonds are there, but they barely matter. You might as well hold 90% stocks in a risk sense.

If a major stock market crash happens, a 60/40 portfolio will fall almost as much as a 100% stock portfolio. The 40% in bonds barely cushions the blow.

Risk parity challenges this. The core question it asks: **what if we allocated capital so that each asset class contributed equally to total portfolio risk?** If bonds are 4× less volatile than stocks, you would hold 4× more bonds than stocks. The portfolio would look wildly different from traditional allocation — maybe 10% equities and 60% bonds — but each dollar of risk would be genuinely balanced.

This idea was popularized by Ray Dalio at Bridgewater Associates, who called it the "All Weather" strategy. The intuition: across all economic environments (growth up/down, inflation up/down), some asset class tends to perform well. A risk-balanced portfolio of all of them should deliver smoother returns than any single-dominant portfolio.

**The key trade-off:** true risk parity almost always requires *leverage*. If you hold mostly low-volatility bonds, you need to borrow money to bring total portfolio volatility up to the level an investor expects (say, 10% annualized). This leverage amplifies returns but also amplifies losses, and it is not free — you pay a financing cost.

**Why this matters practically:**
- Simple, rules-based, and transparent.
- Delivers better risk-adjusted returns than 60/40 over long history (1990–2021).
- Was catastrophically tested in 2022, when both stocks and bonds fell simultaneously, eliminating the diversification benefit.

## Math Concepts

**Risk contribution.** Let $\mathbf{w} = (w_1, \ldots, w_N)^T$ be portfolio weights, and $\mathbf{\Sigma}$ be the $N \times N$ covariance matrix of asset returns. Portfolio variance is:

$$\sigma_P^2 = \mathbf{w}^T \mathbf{\Sigma} \mathbf{w}$$

The marginal contribution to risk of asset $i$ is:

$$\text{MCR}_i = \frac{\partial \sigma_P}{\partial w_i} = \frac{(\mathbf{\Sigma} \mathbf{w})_i}{\sigma_P}$$

The *risk contribution* of asset $i$ (how much of total portfolio volatility comes from this asset):

$$\text{RC}_i = w_i \cdot \text{MCR}_i = \frac{w_i \cdot (\mathbf{\Sigma} \mathbf{w})_i}{\sigma_P}$$

A key identity: risk contributions sum to total portfolio volatility:

$$\sum_{i=1}^N \text{RC}_i = \sigma_P$$

**Risk parity condition.** Equal risk contribution (ERC) requires:

$$\text{RC}_i = \frac{\sigma_P}{N} \quad \forall i$$

Equivalently, all risk contributions are equal:

$$w_i \cdot (\mathbf{\Sigma} \mathbf{w})_i = w_j \cdot (\mathbf{\Sigma} \mathbf{w})_j \quad \forall i, j$$

**Naive risk parity (inverse volatility weighting).** When correlations between assets are zero or negligible, $(\mathbf{\Sigma} \mathbf{w})_i \approx \sigma_i^2 w_i$, so the risk parity condition simplifies to $w_i \propto 1/\sigma_i$. Normalized:

$$w_i^{\text{naive}} = \frac{1/\sigma_i}{\sum_{j=1}^N 1/\sigma_j}$$

This is the most commonly used approximation. It ignores correlations but works remarkably well in practice because correlations are unstable and noisy to estimate.

**Full optimization (ERC).** The general risk parity solution minimizes the variance of risk contributions:

$$\min_{\mathbf{w}} \sum_{i=1}^N \left(\text{RC}_i - \frac{\sigma_P}{N}\right)^2$$

subject to $\sum_i w_i = 1$, $w_i \geq 0$.

There is no closed-form solution in general — it requires numerical optimization (e.g., `scipy.optimize.minimize`).

**Portfolio volatility targeting.** Once weights $\mathbf{w}^*$ are found, the unlevered portfolio has some volatility $\sigma_P^*$. To achieve a target volatility $\sigma_{\text{target}}$, apply leverage $\ell$:

$$\ell = \frac{\sigma_{\text{target}}}{\sigma_P^*}, \qquad \tilde{w}_i = \ell \cdot w_i^*$$

If $\ell > 1$, the portfolio is levered. Typical risk parity funds target 10–15% annualized portfolio volatility, often requiring $\ell = 2$–$3\times$ on a bond-heavy portfolio.

**Marginal risk parity (risk budgeting generalization).** Instead of equal contributions, assign a budget $b_i$ (with $\sum b_i = 1$) and require $\text{RC}_i = b_i \cdot \sigma_P$. This gives a risk budget portfolio where some assets are allowed more risk than others — e.g., allocate 40% risk to bonds, 30% to equities, 30% to alternatives.

## Walkthrough

**Setup: 3-asset portfolio (equities, bonds, gold).**

Annualized volatilities:
- Equity: $\sigma_1 = 20\%$
- Bonds: $\sigma_2 = 5\%$
- Gold: $\sigma_3 = 15\%$

Assume zero correlations for clarity.

**Step 1 — Naive risk parity weights.**

$$w_1 = \frac{1/0.20}{1/0.20 + 1/0.05 + 1/0.15} = \frac{5}{5 + 20 + 6.67} = \frac{5}{31.67} = 0.158$$

$$w_2 = \frac{20}{31.67} = 0.632, \qquad w_3 = \frac{6.67}{31.67} = 0.210$$

**Step 2 — Compare to equal weight.** Equal weight: 33.3% each.

| Asset | Volatility | Equal weight | Risk parity weight | Dollar weight × Vol |
|-------|-----------|-------------|-------------------|---------------------|
| Equity | 20% | 33.3% | **15.8%** | 3.16% |
| Bonds | 5% | 33.3% | **63.2%** | 3.16% |
| Gold | 15% | 33.3% | **21.0%** | 3.15% |

Risk contributions are now (approximately) equal at ~3.16% each.

**Step 3 — Equal weight risk contributions.**

With equal weight: equity contributes $0.333 \times 0.20 = 6.67\%$, bonds $0.333 \times 0.05 = 1.67\%$, gold $0.333 \times 0.15 = 5.00\%$. Equity dominates completely.

**Step 4 — Portfolio volatility and leverage.**

Naive RP portfolio vol (uncorrelated): $\sigma_P = \sqrt{\sum_i w_i^2 \sigma_i^2} = \sqrt{(0.158 \times 0.20)^2 + (0.632 \times 0.05)^2 + (0.210 \times 0.15)^2}$

$= \sqrt{0.000996 + 0.000998 + 0.000993} = \sqrt{0.002987} \approx 5.47\%$ annualized.

To target 10% portfolio volatility: $\ell = 10\% / 5.47\% = 1.83\times$ leverage.

## Analysis

**When risk parity works well:**
- Normal environments with low correlation between stocks and bonds (typical in 1990–2021).
- Risk-off / flight-to-quality episodes: bonds rally when stocks fall, providing natural diversification.
- Low interest rate environments: levered bond positions produce strong returns as rates fall.

**When risk parity fails:**

The critical assumption is that assets are *diversifying* — that they don't all fall together. When this assumption breaks:

- **2022 scenario:** Rising inflation caused both bonds and stocks to sell off simultaneously. A levered bond-heavy risk parity portfolio was devastated. Bridgewater All Weather was down ~20% in 2022.
- **Leverage financing cost:** In rising-rate environments, the cost of borrowing to lever the bond position increases, directly reducing returns.
- **Volatility estimation lag:** When market volatility spikes suddenly (e.g., March 2020 COVID), EWMA-based vol estimates lag behind reality, causing delayed position reduction and larger drawdowns.

**Risk parity vs. alternatives:**

| Strategy | Key assumption | Works when | Fails when |
|----------|---------------|------------|------------|
| 60/40 | Equity dominance is acceptable | Equities outperform | Equity bear market |
| Equal weight | All assets have equal importance | Assets have similar vols | High vol spread across assets |
| Min variance | Low variance is the goal | Correlations stable | Correlation regime shifts |
| **Risk parity** | Equal risk is optimal diversification | Bonds/stocks uncorrelated | Correlated drawdowns (2022) |
| Mean-variance | Expected returns estimable | Stable distributions | Return estimation error |

**Correlation sensitivity.** Naive RP ignores correlations; full ERC captures them. During crises, correlations between risky assets surge toward 1 (everything falls together), making full ERC unstable. A common solution: use a *shrinkage* estimate of the covariance matrix (e.g., Ledoit-Wolf) or add a regularization term.

## Implementation

```python
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# ── 1. Define assets ───────────────────────────────────────────────────────
assets = ["Equity", "Bonds", "Gold"]
vols   = np.array([0.20, 0.05, 0.15])   # annualized volatility

# Correlation matrix (mild diversification)
corr = np.array([
    [1.00, -0.20,  0.05],
    [-0.20,  1.00, -0.10],
    [ 0.05, -0.10,  1.00],
])
cov = np.outer(vols, vols) * corr       # covariance matrix

# ── 2. Risk contribution functions ────────────────────────────────────────
def portfolio_vol(w: np.ndarray, cov: np.ndarray) -> float:
    return float(np.sqrt(w @ cov @ w))

def risk_contributions(w: np.ndarray, cov: np.ndarray) -> np.ndarray:
    """RC_i = w_i * (Sigma @ w)_i / sigma_P"""
    pv  = portfolio_vol(w, cov)
    mrc = (cov @ w) / pv   # marginal risk contributions
    return w * mrc

# ── 3. Naive risk parity (inverse volatility, ignores correlations) ────────
w_naive = (1 / vols) / np.sum(1 / vols)

# ── 4. Full ERC optimization (equal risk contributions) ───────────────────
def erc_objective(w: np.ndarray, cov: np.ndarray) -> float:
    """Minimize variance of risk contributions (deviation from equal share)."""
    rc   = risk_contributions(w, cov)
    pv   = portfolio_vol(w, cov)
    n    = len(w)
    target_rc = pv / n
    return float(np.sum((rc - target_rc) ** 2))

n = len(assets)
w0 = np.ones(n) / n   # equal-weight starting point

result = minimize(
    erc_objective,
    w0,
    args=(cov,),
    method="SLSQP",
    bounds=[(0.0, 1.0)] * n,
    constraints={"type": "eq", "fun": lambda w: np.sum(w) - 1.0},
    options={"ftol": 1e-12, "maxiter": 1000}
)
w_erc = result.x

# ── 5. 60/40 and equal weight benchmarks ─────────────────────────────────
w_60_40   = np.array([0.60, 0.40, 0.00])
w_eq      = np.ones(n) / n

# ── 6. Risk contribution breakdown ────────────────────────────────────────
portfolios = {
    "60/40":        w_60_40,
    "Equal Weight": w_eq,
    "Naive RP":     w_naive,
    "Full ERC":     w_erc,
}

print(f"{'Portfolio':<15} | {'Equity':>8} {'Bonds':>8} {'Gold':>8} | {'Port Vol':>9} | Risk Contribs (%)")
print("-" * 80)
for name, w in portfolios.items():
    pv   = portfolio_vol(w, cov)
    rc   = risk_contributions(w, cov)
    rc_pct = rc / pv * 100  # as % of total vol
    print(f"{name:<15} | {w[0]:>8.1%} {w[1]:>8.1%} {w[2]:>8.1%} | {pv:>9.1%} | "
          f"Eq:{rc_pct[0]:>5.1f}% Bd:{rc_pct[1]:>5.1f}% Au:{rc_pct[2]:>5.1f}%")

# ── 7. Simulate cumulative returns ────────────────────────────────────────
np.random.seed(42)
n_months = 360   # 30 years

# Asset returns: mild positive drift
drifts = np.array([0.008, 0.003, 0.004])  # monthly
L_chol = np.linalg.cholesky(cov / 12)     # monthly covariance
monthly_returns = np.random.randn(n_months, n) @ L_chol.T + drifts

target_annual_vol = 0.10
def levered_port_returns(w: np.ndarray, monthly_returns: np.ndarray, target_vol: float) -> np.ndarray:
    """Apply leverage to achieve target_vol."""
    unlevered_vol = portfolio_vol(w, cov)
    leverage = target_vol / unlevered_vol
    port_r = monthly_returns @ w * leverage
    return port_r

cum_returns = {}
for name, w in portfolios.items():
    r = levered_port_returns(w, monthly_returns, target_annual_vol)
    cum_returns[name] = np.cumprod(1 + r)

# ── 8. Performance metrics ─────────────────────────────────────────────────
def sharpe(port_r: np.ndarray) -> float:
    return float(np.mean(port_r) / np.std(port_r) * np.sqrt(12))

def max_dd(cum: np.ndarray) -> float:
    peak = np.maximum.accumulate(cum)
    return float(np.min((cum - peak) / peak))

print(f"\n{'Portfolio':<15} {'Ann. Sharpe':>12} {'Max DD':>10} {'Final Value':>12}")
print("-" * 55)
for name, w in portfolios.items():
    r   = levered_port_returns(w, monthly_returns, target_annual_vol)
    cum = np.cumprod(1 + r)
    print(f"{name:<15} {sharpe(r):>12.2f} {max_dd(cum):>10.1%} ${cum[-1]:>10.2f}")

# ── 9. 2022-style stress test: bonds and equities both fall ───────────────
print("\n=== Stress Test: 2022-style (bonds and equities both fall) ===")
stress_returns = monthly_returns.copy()
stress_returns[240:252, 0] = -0.035   # equity down ~3.5%/mo for 12 months → ~-35%
stress_returns[240:252, 1] = -0.015   # bonds down ~1.5%/mo for 12 months → ~-17%
stress_returns[240:252, 2] =  0.010   # gold roughly flat/slightly positive

for name, w in portfolios.items():
    r   = levered_port_returns(w, stress_returns, target_annual_vol)
    cum = np.cumprod(1 + r[240:252])
    print(f"  {name:<15}: crisis period return = {cum[-1]-1:.1%}")
```

## Bridge to Quant / ML

**Risk parity as a baseline.** In quantitative portfolio construction, naive risk parity (inverse volatility weighting) is frequently used as a simple, robust benchmark. Before deploying a complex ML-based optimizer, practitioners check: does the ML model beat inverse-vol weighting? This sets a realistic bar, since naive RP often outperforms mean-variance out-of-sample due to its insensitivity to noisy expected-return estimates.

**Covariance estimation.** The hardest problem in risk parity is estimating the covariance matrix reliably. Options used in practice:
- **Ledoit-Wolf shrinkage:** Shrinks the sample covariance toward a structured prior (e.g., equal-correlation matrix), reducing estimation error.
- **Factor models:** Decompose covariance via factors (market, size, value), estimating factor covariances which are more stable than asset-level covariances.
- **DCC-GARCH:** Dynamic Conditional Correlation models that let correlations change over time — important in risk parity because correlations between stocks and bonds shifted dramatically in 2022.

**ML extensions:**
- Train a neural network to predict next-month volatility (better than EWMA in some regimes) and feed it into the inverse-vol weights.
- Use an RL agent to learn dynamic risk allocations that respond to regime signals.
- Hierarchical risk parity (HRP, Lopez de Prado 2016): uses hierarchical clustering on the correlation matrix to define an allocation that is robust to correlation estimation error — a data-science native approach that sidesteps matrix inversion entirely.

**Hierachical Risk Parity (HRP) connection.** Lopez de Prado's HRP algorithm (from *Advances in Financial ML*, ch. 16) is directly motivated by the failure modes of traditional risk parity under large, noisy covariance matrices. HRP applies k-means or Ward linkage clustering, then uses bisective allocation — no matrix inversion required. It is empirically more stable than ERC in high-dimensional portfolios.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why is a 60/40 portfolio not "60/40" in any meaningful risk sense?
<details><summary>Answer</summary>Because stocks have roughly 3–4× the volatility of bonds, the 60% allocation in equities contributes approximately 88–92% of total portfolio risk, and the 40% in bonds contributes only 8–12%. So the "40/60" split of capital corresponds to a "90/10" split of risk. Risk Parity challenges this by asking: what allocation would make each asset class contribute equally to total portfolio risk? The answer looks like 10–15% equities / 60–70% bonds — the opposite of 60/40 — requiring leverage on the bond side to bring total portfolio volatility to a usable level.</details>

**Q2.** Explain the difference between "naive risk parity" (inverse volatility weighting) and "full ERC" (equal risk contribution). When does naive outperform full ERC?
<details><summary>Answer</summary>**Naive risk parity** weights $w_i \propto 1/\sigma_i$ — this achieves equal risk contribution only when all asset correlations are zero. It ignores off-diagonal terms in the covariance matrix.

**Full ERC** solves the optimization $\min_w \sum_i (RC_i - \sigma_P/N)^2$ subject to weights summing to 1, capturing correlations exactly.

Naive outperforms full ERC when: (a) correlations are near zero (no cross-terms to capture); (b) the correlation matrix is estimated with noise — fitting correlations adds estimation error that worsens out-of-sample performance; (c) the portfolio rebalances frequently, where naive's simplicity reduces transaction costs; (d) the correlation matrix is unstable over time. In practice, naive RP is a strong baseline and full ERC provides limited additional benefit except when correlations are large and stable.</details>

**Q3.** In 2022, Risk Parity strategies suffered large losses even though they are "diversified." What assumption broke, and what does this reveal about the limitations of diversification-based strategies?
<details><summary>Answer</summary>The critical assumption that broke: bonds and equities have low or negative correlation. Risk Parity depends on this relationship — it overweights bonds precisely because bonds historically offset equity losses. In 2022, rising inflation caused the Fed to hike rates aggressively, which simultaneously: (a) hurt equity valuations (higher discount rates); (b) crushed bond prices (rising yields = falling bond prices). Both major asset classes fell together for the first time since the 1970s stagflation. A levered bond-heavy RP portfolio was devastated. This reveals: diversification-based strategies do not protect against regimes where the correlation structure itself changes. The "risk" of Risk Parity is regime risk — the stability of the stock-bond correlation.</details>

---

### Level 2 — Quantitative

**Q4.** Four assets with volatilities: Asset 1 (30%), Asset 2 (10%), Asset 3 (20%), Asset 4 (15%). Assume zero correlations. Compute the naive risk parity weights and verify that the risk contributions are approximately equal.
<details><summary>Answer</summary>

Inverse volatilities: $1/0.30 = 3.33$, $1/0.10 = 10$, $1/0.20 = 5$, $1/0.15 = 6.67$

Sum: $3.33 + 10 + 5 + 6.67 = 25$

Weights: $w_1 = 3.33/25 = 13.3\%$, $w_2 = 10/25 = 40.0\%$, $w_3 = 5/25 = 20.0\%$, $w_4 = 6.67/25 = 26.7\%$

Risk contributions (zero correlation: $RC_i = w_i \sigma_i$, normalized by $\sigma_P$):

$RC_1 \propto 0.133 \times 0.30 = 0.0400$, $RC_2 \propto 0.400 \times 0.10 = 0.0400$, $RC_3 \propto 0.200 \times 0.20 = 0.0400$, $RC_4 \propto 0.267 \times 0.15 = 0.0400$

All equal at 0.04 — confirming equal risk contribution at zero correlation. Portfolio vol: $\sigma_P = \sqrt{\sum w_i^2\sigma_i^2} = \sqrt{4 \times 0.0016} = \sqrt{0.0064} = 8.0\%$</details>

**Q5.** A risk parity fund targets 10% annualized portfolio volatility. The unlevered portfolio has volatility of 4.5%. (a) What leverage ratio is needed? (b) If borrowing costs 3% per year and the unlevered portfolio returns 5%, what is the levered return and levered Sharpe (assume risk-free rate = 3%)?
<details><summary>Answer</summary>

(a) Leverage: $\ell = 10\% / 4.5\% = \mathbf{2.22\times}$

(b) Levered return: $r_{\text{lev}} = \ell \times r_{\text{unlev}} - (\ell - 1) \times r_{\text{borrow}}$
$= 2.22 \times 5\% - 1.22 \times 3\% = 11.1\% - 3.66\% = \mathbf{7.44\%}$

Levered Sharpe: $(7.44\% - 3\%) / 10\% = 4.44\% / 10\% = \mathbf{0.44}$

Note: leverage does not change the Sharpe ratio in a frictionless world (both numerator and denominator scale by $\ell$). Here the Sharpe is slightly degraded by the borrowing cost spread (borrow at 3% = risk-free, so in this case no degradation beyond the pass-through). In practice, borrowing costs exceed the risk-free rate, reducing the levered Sharpe below the unlevered Sharpe.</details>

---

### Level 3 — Coding

**Q6.** The ERC optimization minimizes the sum of squared deviations of risk contributions from the equal target. This is a non-convex optimization. Describe an alternative formulation that is convex and therefore has guaranteed convergence, and explain the trade-off.
<details><summary>Answer</summary>

An alternative convex formulation (Roncalli 2013): instead of minimizing $\sum_i (RC_i - \sigma_P/N)^2$, solve:

$$\min_w \mathbf{w}^\top\boldsymbol{\Sigma}\mathbf{w} - \frac{1}{N}\sum_i \ln(w_i)$$

The log-barrier term $-\frac{1}{N}\sum_i \ln(w_i)$ penalizes small weights (prevents zero allocations) and creates a smooth, strictly convex objective. The solution converges to the ERC portfolio for long-only portfolios with positive correlations.

**Trade-off:** The log-barrier formulation only works for long-only portfolios (since $\ln(w_i)$ requires $w_i > 0$). The original sum-of-squared-deviations formulation can in principle handle general risk budgets and short positions, though it requires careful initialization. For practical long-only risk parity, the log-barrier is preferred for its convergence guarantees and faster computation.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Risk Parity has no expected return assumptions | Correct for naive RP. But full ERC and levered RP implicitly assume the risk premium per unit of risk is equal across asset classes — which is itself a return assumption. |
| Risk Parity is safer than 60/40 | Risk Parity may have lower volatility when correlations are favorable, but it requires leverage and is exposed to correlation regime changes that 60/40 is not. 2022 showed it can lose more than 60/40. |
| Inverse volatility weighting is optimal | It is optimal only when correlations are zero. With nonzero correlations, it can significantly deviate from true equal risk contribution. |
| Leverage makes risk parity inherently dangerous | Leverage is a tool, not a problem in itself. The risk is borrowing cost risk and margin call risk during crises. Many institutional RP funds have delivered strong Sharpe ratios over 20-year horizons despite using 2-3× leverage. |

## Related Concepts

- [[Markowitz Mean-Variance Optimization]] — the classical alternative; requires return estimates that risk parity deliberately avoids
- [[Factor Models]] — covariance decomposition that improves risk estimation in risk parity
- [[Sharpe Ratio]] — risk parity targets better risk-adjusted returns vs. 60/40
- [[Correlation and Covariance Estimation]] — the core statistical challenge in full ERC
- [[Kelly Criterion]] — a related framework for optimal sizing; Kelly is growth-optimal, risk parity is diversification-optimal
- [[Efficient Frontier]] — risk parity portfolios typically appear near the efficient frontier when correlations are favorable

## Sources Used

- Roncalli, T. (2013). *Introduction to Risk Parity and Budgeting*. CRC Press
- Qian, E. (2011). Risk parity and diversification. *Journal of Investing*, 20(1), 119–127
- Asness, C., Frazzini, A., & Pedersen, L. H. (2012). Leverage aversion and risk parity. *Financial Analysts Journal*, 68(1), 47–59
- Lopez de Prado, M. (2016). Building diversified portfolios that outperform out-of-sample. *Journal of Portfolio Management*, 42(4), 59–69
- Bridgewater Associates. *The All Weather Story*. [Internal white paper, summarized in public materials]

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | initial build |
