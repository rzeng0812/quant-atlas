---
type: concept
domain: 30-Models
tags: [portfolio, optimization, risk]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-18
review_interval_days: 365
sources:
  - "Markowitz, H. (1952). Portfolio Selection. Journal of Finance, 7(1), 77-91"
  - "Ledoit, O. & Wolf, M. (2004). A well-conditioned estimator for large-dimensional covariance matrices. Journal of Multivariate Analysis"
  - "Black, F. & Litterman, R. (1992). Global Portfolio Optimization. Financial Analysts Journal"
created: 2026-04-18
---

> [!info] Problem Chain
> **Chain:** Hedging & Risk → Gap 4: Measuring risk is not the same as managing it across a portfolio
> **This concept:** Markowitz MVO finds portfolio weights that maximize expected return for a given variance (or minimize variance for a given return), formalizing diversification mathematically.
> **Alternative approaches to this gap:** none (Markowitz is the foundational solution; Gap 5 alternatives address its failures)
> **You need first:** [[Value at Risk]], [[Expected Shortfall]], [[Sharpe Ratio]]
> **This unlocks:** [[Efficient Frontier]], [[CAPM]], [[Factor Models]], [[Risk Parity]], [[Black-Litterman]], [[Hierarchical Risk Parity]]

## Why This Exists

**The gap:** VaR and ES measure risk for a given portfolio, but they say nothing about how to *construct* a portfolio with the best return-to-risk profile. With N risky assets, there are infinitely many ways to allocate capital — which combination is optimal?

**What came before:** Before Markowitz (1952), portfolio construction was largely intuitive — diversify broadly, pick good individual stocks. There was no mathematical framework for answering "how much of each?"

**What this adds:** MVO converts portfolio construction into a solvable optimization problem: minimize portfolio variance for a given expected return (or maximize return for a given variance). This reveals the precise mathematical role of correlation — two assets with negative correlation provide variance reduction beyond what their individual variances suggest. The result is the Efficient Frontier: the set of all optimal portfolios.

**What it still doesn't solve:** The optimization is exquisitely sensitive to the expected return vector $\boldsymbol{\mu}$, which is notoriously hard to estimate. Small errors produce wildly different portfolio weights — making raw MVO practically unusable without modification. Correlations are also unstable across regimes.

You've heard "don't put all your eggs in one basket." But why exactly? And how many baskets? How do you split your eggs?

Markowitz (1952) gave the first mathematical answer. The key insight is about **correlation**. If you own two assets that tend to move in opposite directions — when one zigs, the other zags — then combining them in a portfolio smooths out the ride. You lose some of the upside from each asset individually, but you gain something more valuable: **lower risk without proportionally lower return**.

Think of it like two farmers. Farmer A sells ice cream (profits soar in summer, tanks in winter). Farmer B sells hot chocolate (profits soar in winter, tanks in summer). If you invest in only one, your income is volatile. Invest in both and your combined income is steady year-round — and you haven't given up any *average* income. The correlation between them is negative, and that negative correlation is your friend.

Markowitz formalized this as a precise mathematical problem: given a set of assets with known expected returns and a known covariance matrix (how they move together), find the portfolio weights that:

- **Maximize expected return** for a given level of risk (variance), or equivalently,
- **Minimize variance** for a given level of expected return.

The set of all solutions to this problem — one optimal portfolio for each target return level — traces out a curve in risk-return space called the [[Efficient Frontier]].

## Math Concepts

**Portfolio return and variance.** Let $\mathbf{w} \in \mathbb{R}^n$ be a vector of portfolio weights (fractions of total capital invested in each asset), $\boldsymbol{\mu} \in \mathbb{R}^n$ be expected returns, and $\boldsymbol{\Sigma} \in \mathbb{R}^{n \times n}$ be the covariance matrix of returns.

$$\boxed{E[R_p] = \mathbf{w}^\top \boldsymbol{\mu}}$$

$$\boxed{\sigma_p^2 = \mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}}$$

**The optimization problem.** For a target return $\mu^*$:

$$\min_{\mathbf{w}} \quad \mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}$$

$$\text{subject to} \quad \mathbf{w}^\top \boldsymbol{\mu} = \mu^*, \quad \mathbf{w}^\top \mathbf{1} = 1$$

Optionally, add $\mathbf{w} \geq \mathbf{0}$ for a **long-only** portfolio (no short selling).

**Closed-form solution (unconstrained, no short-selling restriction).** Using Lagrange multipliers, the solution has a closed form involving the inverse of $\boldsymbol{\Sigma}$. In practice, this is solved numerically with quadratic programming because:

1. The closed form requires $\boldsymbol{\Sigma}^{-1}$, which is ill-conditioned for large $n$
2. Real portfolios have additional constraints (position limits, sector caps, etc.)

**Key quantities:**

| Symbol | Meaning |
|--------|---------|
| $\mathbf{w}^\top \mathbf{1} = 1$ | Weights sum to 1 (fully invested) |
| $\boldsymbol{\Sigma}_{ij}$ | Covariance between assets $i$ and $j$ |
| $\rho_{ij} = \boldsymbol{\Sigma}_{ij} / (\sigma_i \sigma_j)$ | Correlation between assets $i$ and $j$ |
| $\sigma_p = \sqrt{\mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}}$ | Portfolio volatility |

**Two-asset portfolio variance** (useful for intuition):

$$\sigma_p^2 = w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + 2 w_1 w_2 \sigma_1 \sigma_2 \rho_{12}$$

When $\rho_{12} < 0$, the cross term is negative — this is the diversification benefit in action.

## Walkthrough

**Setup.** Two assets:

| Asset | Expected Return $\mu$ | Volatility $\sigma$ |
|-------|----------------------|---------------------|
| A (equity) | 10% | 15% |
| B (bonds) | 6% | 8% |

Correlation between A and B: $\rho = -0.3$. Covariance: $\sigma_{AB} = \rho \cdot \sigma_A \cdot \sigma_B = -0.3 \times 0.15 \times 0.08 = -0.0036$.

**50/50 portfolio:** $w_A = 0.5$, $w_B = 0.5$.

Expected return:
$$E[R_p] = 0.5 \times 10\% + 0.5 \times 6\% = 8\%$$

Portfolio variance:
$$\sigma_p^2 = (0.5)^2(0.15)^2 + (0.5)^2(0.08)^2 + 2(0.5)(0.5)(-0.0036)$$
$$= 0.005625 + 0.0016 + (-0.0018) = 0.005425$$
$$\sigma_p = \sqrt{0.005425} \approx 7.37\%$$

**The key observation:** A weighted average of the two volatilities would be $0.5 \times 15\% + 0.5 \times 8\% = 11.5\%$. But the actual portfolio volatility is only **7.37%** — far below either asset alone, and far below the naive average. That's the power of negative correlation. The portfolio earns 8% return with only 7.37% volatility — better risk-adjusted than either asset by itself.

**Varying the weights.** As you move $w_A$ from 0 to 1, you trace a curve in (volatility, return) space. The shape of this curve is a hyperbola — its upper-left boundary is the [[Efficient Frontier]].

## Analysis

**The assumptions — and why they break:**

| Assumption | Reality |
|------------|---------|
| Returns are normally distributed | Returns have fat tails and negative skew — rare crashes are far more common and severe than normal distribution predicts |
| $\boldsymbol{\mu}$ is known | Expected returns are extremely difficult to estimate; small errors cause large changes in optimal weights |
| $\boldsymbol{\Sigma}$ is stable | Correlations spike toward 1 in crises (diversification vanishes exactly when you need it most) |
| Optimization is stable | The optimizer is numerically ill-conditioned: tiny changes in inputs → large changes in weights ("error maximization") |

**The garbage-in-garbage-out problem.** Markowitz optimization is famously sensitive to input estimates. A small upward bias in one asset's expected return causes the optimizer to go heavily overweight in it. This makes naive mean-variance portfolios unstable and hard to use in practice.

**Practical fixes:**

- **Ledoit-Wolf shrinkage:** Instead of using the sample covariance matrix $\hat{\boldsymbol{\Sigma}}$ (which is noisy for large $n$), shrink it toward a structured target (e.g., constant-correlation matrix): $\hat{\boldsymbol{\Sigma}}_{\text{shrunk}} = (1-\alpha)\hat{\boldsymbol{\Sigma}} + \alpha \mathbf{F}$. This reduces estimation error dramatically.
- **Black-Litterman model:** Rather than directly using noisy $\hat{\boldsymbol{\mu}}$, start from CAPM-implied equilibrium returns as a prior and blend in your own views with a Bayesian update. Produces much more stable, sensible portfolios.
- **Constrain the weights:** Hard caps on individual positions (e.g., no more than 10% in any single asset) prevent extreme allocations.
- **Risk parity:** An alternative that abandons return estimation entirely and focuses only on equalizing risk contributions across assets.

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# ── Setup: 3 assets ──────────────────────────────────────────────────────────
mu = np.array([0.10, 0.06, 0.08])         # expected returns
sigma = np.array([0.15, 0.08, 0.12])      # volatilities

# Correlation matrix
corr = np.array([
    [1.00, -0.30,  0.10],
    [-0.30,  1.00,  0.20],
    [0.10,  0.20,  1.00]
])

# Covariance matrix: Sigma_ij = rho_ij * sigma_i * sigma_j
Sigma = np.outer(sigma, sigma) * corr

n = len(mu)
rf = 0.03  # risk-free rate

# ── Helper functions ─────────────────────────────────────────────────────────
def portfolio_return(w):
    return w @ mu

def portfolio_vol(w):
    return np.sqrt(w @ Sigma @ w)

def neg_sharpe(w):
    excess = portfolio_return(w) - rf
    vol = portfolio_vol(w)
    return -excess / vol if vol > 1e-8 else 0.0

# ── 1. Minimum variance portfolio ────────────────────────────────────────────
constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
bounds = [(0, 1)] * n  # long-only

result_gmv = minimize(
    lambda w: portfolio_vol(w),
    x0=np.ones(n) / n,
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)
w_gmv = result_gmv.x
print(f"Global Minimum Variance Portfolio:")
print(f"  Weights: {w_gmv.round(3)}")
print(f"  Return:  {portfolio_return(w_gmv):.2%}")
print(f"  Vol:     {portfolio_vol(w_gmv):.2%}")
print(f"  Sharpe:  {(portfolio_return(w_gmv)-rf)/portfolio_vol(w_gmv):.3f}")

# ── 2. Maximum Sharpe (tangency) portfolio ───────────────────────────────────
result_msr = minimize(
    neg_sharpe,
    x0=np.ones(n) / n,
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)
w_msr = result_msr.x
print(f"\nMaximum Sharpe (Tangency) Portfolio:")
print(f"  Weights: {w_msr.round(3)}")
print(f"  Return:  {portfolio_return(w_msr):.2%}")
print(f"  Vol:     {portfolio_vol(w_msr):.2%}")
print(f"  Sharpe:  {(portfolio_return(w_msr)-rf)/portfolio_vol(w_msr):.3f}")

# ── 3. Trace the efficient frontier ──────────────────────────────────────────
target_returns = np.linspace(mu.min(), mu.max(), 100)
frontier_vols = []

for target in target_returns:
    cons = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
        {'type': 'eq', 'fun': lambda w, t=target: portfolio_return(w) - t}
    ]
    res = minimize(
        lambda w: portfolio_vol(w),
        x0=np.ones(n) / n,
        method='SLSQP',
        bounds=bounds,
        constraints=cons
    )
    frontier_vols.append(res.fun if res.success else np.nan)

frontier_vols = np.array(frontier_vols)

# ── 4. Simulate random portfolios (feasible set) ─────────────────────────────
np.random.seed(42)
n_sim = 5000
rand_weights = np.random.dirichlet(np.ones(n), size=n_sim)  # sum-to-1
rand_returns = rand_weights @ mu
rand_vols    = np.array([portfolio_vol(w) for w in rand_weights])
rand_sharpes = (rand_returns - rf) / rand_vols

# ── 5. Plot ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 7))

sc = ax.scatter(rand_vols, rand_returns, c=rand_sharpes, cmap='viridis',
                alpha=0.4, s=8, label='Random portfolios')
plt.colorbar(sc, ax=ax, label='Sharpe Ratio')

ax.plot(frontier_vols, target_returns, 'r-', linewidth=2.5, label='Efficient Frontier')

ax.scatter(portfolio_vol(w_gmv), portfolio_return(w_gmv),
           color='blue', s=120, zorder=5, marker='*', label='Min Variance')
ax.scatter(portfolio_vol(w_msr), portfolio_return(w_msr),
           color='gold', s=120, zorder=5, marker='*', label='Max Sharpe (Tangency)')

# Capital Market Line: from rf through tangency portfolio
vol_range = np.linspace(0, 0.20, 100)
cml_slope = (portfolio_return(w_msr) - rf) / portfolio_vol(w_msr)
ax.plot(vol_range, rf + cml_slope * vol_range, 'k--', linewidth=1.5,
        label=f'Capital Market Line (slope={cml_slope:.2f})')

ax.set_xlabel('Portfolio Volatility (σ)', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title('Markowitz Efficient Frontier (3-Asset Example)', fontsize=14)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('efficient_frontier.png', dpi=150)
plt.show()
```

## Bridge to Quant / ML

**Factor models and covariance.** The biggest practical challenge in MVO is estimating $\boldsymbol{\Sigma}$ for large portfolios (e.g., 500 stocks). A $500 \times 500$ sample covariance matrix requires 2 years of daily data just to be non-singular — and it's still extremely noisy. [[Factor Models]] solve this by decomposing $\boldsymbol{\Sigma} = \mathbf{B}\boldsymbol{\Sigma}_F\mathbf{B}^\top + \mathbf{D}$ (systematic + idiosyncratic), reducing the estimation problem to far fewer parameters.

**Risk parity as an alternative.** Risk parity ignores $\boldsymbol{\mu}$ entirely (since it's too hard to estimate) and instead allocates so that each asset contributes equally to total portfolio risk. Less optimal in theory but much more robust in practice.

**ML for covariance estimation.** Recent research uses neural networks, random matrix theory denoising, and graph neural networks to estimate cleaner covariance matrices from noisy historical data. The covariance structure in turn feeds directly into MVO.

**Differentiable portfolio optimization.** End-to-end learning pipelines now embed the Markowitz optimization as a differentiable layer (e.g., `cvxpylayers`), allowing ML models to be trained with portfolio Sharpe ratio as the direct objective.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Two assets each have volatility of 20%. What correlation between them minimizes portfolio variance when held 50/50? What is the minimum-variance portfolio variance at this correlation?
<details><summary>Answer</summary>Minimum portfolio variance is achieved when correlation is as negative as possible — ideally $\rho = -1$. At $\rho = -1$ and equal weights, the two assets perfectly offset each other and the portfolio variance is zero: $\sigma_p^2 = (0.5)^2(0.20)^2 + (0.5)^2(0.20)^2 + 2(0.5)(0.5)(-1)(0.20)(0.20) = 0.01 + 0.01 - 0.02 = 0$. In practice, correlations are never perfectly -1, so the reduction is partial — but the principle holds: negative correlation is the source of diversification benefit.</details>

**Q2.** Why does Markowitz optimization behave like an "error maximizer" when expected returns are poorly estimated?
<details><summary>Answer</summary>The optimizer treats expected returns as exact inputs and aggressively tilts toward assets with the highest estimated return. If one asset's true expected return is 8% but is estimated as 10% due to noise, the optimizer allocates heavily to it — exactly in the direction of the estimation error. The mathematical term is "error maximization": the quadratic program amplifies small differences in $\boldsymbol{\mu}$ into large differences in portfolio weights. Michaud (1989) called this property the key practical failure of MVO — it mistakes estimation noise for genuine return differences.</details>

**Q3.** What is the difference between the Global Minimum Variance portfolio and the Tangency portfolio? Under what conditions are they the same?
<details><summary>Answer</summary>The Global Minimum Variance (GMV) portfolio has the lowest possible variance of all portfolios — it ignores expected returns entirely. The Tangency portfolio has the highest Sharpe ratio — it maximizes (expected return − risk-free rate) / volatility. They differ whenever assets have different expected returns; the tangency portfolio tilts toward higher-return assets relative to GMV. They converge when all assets have the same expected return (all the action is in the risk-minimization), or equivalently when $r_f$ equals the GMV portfolio's return (the CML is tangent at the GMV point).</details>

---

### Level 2 — Quantitative

**Q4.** Three assets: Asset 1 ($\mu=10\%$, $\sigma=15\%$), Asset 2 ($\mu=6\%$, $\sigma=8\%$), Asset 3 ($\mu=8\%$, $\sigma=12\%$). Correlation between Asset 1 and 2 is $-0.30$, all other pairs have correlation $0$. Compute the variance and volatility of an equal-weight portfolio.
<details><summary>Answer</summary>

Equal weights: $w_1 = w_2 = w_3 = 1/3$.

Portfolio variance:
$$\sigma_p^2 = w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + w_3^2\sigma_3^2 + 2w_1w_2\sigma_{12}$$

where $\sigma_{12} = \rho_{12}\sigma_1\sigma_2 = (-0.30)(0.15)(0.08) = -0.0036$.

$$\sigma_p^2 = (1/3)^2(0.15)^2 + (1/3)^2(0.08)^2 + (1/3)^2(0.12)^2 + 2(1/3)(1/3)(-0.0036)$$

$$= (1/9)(0.0225 + 0.0064 + 0.0144) + 2(1/9)(-0.0036)$$

$$= (1/9)(0.0433) - (2/9)(0.0036) = 0.004811 - 0.000800 = \mathbf{0.004011}$$

$$\sigma_p = \sqrt{0.004011} = \mathbf{6.33\%}$$

Weighted average of individual vols: $(15\%+8\%+12\%)/3 = 11.67\%$. The actual portfolio vol (6.33%) is far below due to diversification.</details>

**Q5.** You are told the covariance matrix for two assets is $\boldsymbol{\Sigma} = \begin{pmatrix} 0.04 & -0.01 \\ -0.01 & 0.01 \end{pmatrix}$ and $\boldsymbol{\mu} = (0.10, 0.05)^\top$. Compute the minimum variance portfolio weights (without the return constraint, just minimize variance subject to weights summing to 1).
<details><summary>Answer</summary>

The closed-form GMV solution: $\mathbf{w}_{\text{GMV}} = \frac{\boldsymbol{\Sigma}^{-1}\mathbf{1}}{\mathbf{1}^\top\boldsymbol{\Sigma}^{-1}\mathbf{1}}$.

First compute $\boldsymbol{\Sigma}^{-1}$. For a 2×2 matrix $\begin{pmatrix}a&b\\b&c\end{pmatrix}$: inverse = $\frac{1}{ac-b^2}\begin{pmatrix}c&-b\\-b&a\end{pmatrix}$.

Determinant: $0.04 \times 0.01 - (-0.01)^2 = 0.0004 - 0.0001 = 0.0003$.

$$\boldsymbol{\Sigma}^{-1} = \frac{1}{0.0003}\begin{pmatrix}0.01&0.01\\0.01&0.04\end{pmatrix} = \begin{pmatrix}33.33&33.33\\33.33&133.33\end{pmatrix}$$

$\boldsymbol{\Sigma}^{-1}\mathbf{1} = \begin{pmatrix}33.33+33.33\\33.33+133.33\end{pmatrix} = \begin{pmatrix}66.67\\166.67\end{pmatrix}$

Sum: $66.67 + 166.67 = 233.33$.

$$w_1 = 66.67/233.33 = \mathbf{0.286}, \quad w_2 = 166.67/233.33 = \mathbf{0.714}$$

The minimum variance portfolio puts 28.6% in Asset 1 and 71.4% in Asset 2. Asset 2 dominates because it has much lower variance, and the negative correlation further reduces portfolio variance.</details>

---

### Level 3 — Coding

**Q6.** The implementation traces the efficient frontier by solving a constrained optimization for each target return level. What is a faster alternative approach that avoids solving a separate optimization for every point on the frontier, and what is its key limitation in practice?
<details><summary>Answer</summary>

The **two-fund separation theorem** provides a faster approach: every efficient portfolio is a linear combination of the GMV portfolio and the Tangency portfolio. So you only need to solve two optimizations (GMV and Tangency), then trace the frontier by varying the mixing weight $\lambda$:

```python
w_frontier = lambda_val * w_gmv + (1 - lambda_val) * w_tangency
```

As $\lambda$ varies from 1 (all GMV) to 0 (all Tangency) and beyond (levered tangency), you trace the entire frontier analytically.

**Key limitation:** This requires the unrestricted (short-selling allowed) case. With long-only constraints ($w_i \geq 0$), the two-fund separation no longer holds — the frontier has "kinks" where different assets enter or exit the portfolio at binding constraints. In this case, you must solve the QP for each target return, as the code does with `scipy.optimize.minimize`.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| MVO produces the "best" portfolio | MVO produces the best portfolio *given the inputs*. With noisy $\boldsymbol{\mu}$, it often produces the worst portfolio out-of-sample due to error amplification. |
| Diversification always helps | Diversification helps only when assets are not perfectly correlated. During crises, correlations surge toward 1, eliminating the benefit exactly when needed most. |
| The covariance matrix is the easy part | For large portfolios ($N > 100$), estimating a stable covariance matrix is the hardest part. Shrinkage and factor models exist specifically to address this. |
| Equal-weight is always dominated by MVO | Empirically, equal-weight portfolios often outperform MVO out-of-sample because they avoid the estimation error in $\boldsymbol{\mu}$. |

## Related Concepts

- [[Efficient Frontier]] — the curve of optimal portfolios produced by this optimization
- [[CAPM]] — the equilibrium model that emerges when all investors do MVO
- [[Factor Models]] — decompose $\boldsymbol{\Sigma}$ to make MVO tractable at scale
- [[Sharpe Ratio]] — MVO with a risk-free asset is equivalent to maximizing the Sharpe ratio
- [[Kelly Criterion]] — related optimal sizing criterion; shares the variance-penalization intuition

## Sources Used

- Markowitz, H. (1952). Portfolio Selection. *Journal of Finance*, 7(1), 77–91
- Ledoit, O. & Wolf, M. (2004). A well-conditioned estimator for large-dimensional covariance matrices. *Journal of Multivariate Analysis*, 88(2), 365–411
- Black, F. & Litterman, R. (1992). Global Portfolio Optimization. *Financial Analysts Journal*, 48(5), 28–43

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | initial build |
| 2026-04-11 | QA review: renamed "Implementation (Python)" → "Implementation" for section consistency | quality review |
