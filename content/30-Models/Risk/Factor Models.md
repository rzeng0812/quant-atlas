---
type: concept
domain: 30-Models
tags: [risk, portfolio, alpha]
status: math
stability: evolving
confidence: high
last_reviewed: 2026-04-12
review_interval_days: 90
sources:
  - "Fama & French (1993), Journal of Financial Economics"
  - "Barra Risk Models, MSCI documentation"
  - "Cochrane, Asset Pricing, ch. 9"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Hedging & Risk → Gap 5: Markowitz is unstable — inputs are unreliable, outputs are extreme
> **This concept:** Factor Models decompose returns into shared systematic drivers (market, size, value, momentum) plus idiosyncratic noise, reducing the covariance estimation problem from $N \times N$ to far fewer parameters.
> **Alternative approaches to this gap:** [[CAPM]], [[Risk Parity]], [[Black-Litterman]], [[Hierarchical Risk Parity]]
> **You need first:** [[CAPM]], [[Markowitz Mean-Variance Optimization]], [[Correlation and Covariance Estimation]]
> **This unlocks:** [[Black-Litterman]], [[Risk Parity]], [[Hierarchical Risk Parity]], [[Stress Testing]]

## Why This Exists

**The gap:** CAPM uses one factor (the market), but empirically fails to explain the cross-section of returns. Additionally, MVO requires an $N \times N$ covariance matrix — for 500 assets, that is 125,000 parameters from limited data, producing a noisy, near-singular matrix.

**What came before:** CAPM showed that one factor (the market) drives most of stock return variance. But it left systematic return anomalies (size, value, momentum) unexplained, and it did not address the covariance estimation problem for large portfolios.

**What this adds:** Factor Models generalize CAPM to K factors: each asset's return is a linear combination of K systematic drivers plus idiosyncratic noise. This simultaneously fixes both problems: (a) Fama-French 3/5 factors explain more of the cross-section of expected returns; (b) decomposing $\Sigma = B\Sigma_F B^\top + D$ reduces the estimation problem from 125,000 parameters to $\sim$25 + 500, making covariance tractable.

**What it still doesn't solve:** The "factor zoo" (400+ documented factors) creates severe overfitting and multiple testing problems. Factor exposures change over time; static betas estimated from one regime misforecast another. Correlations still spike in crises regardless of factor structure.

Imagine you are trying to understand why your portfolio went up 3% last Tuesday. You could say "the market went up 2.5% and your stocks went up 3%, so you did a bit better." That is a one-factor model. But stocks also have persistent patterns: small companies tend to move together, "cheap" (value) stocks tend to move together, and stocks that have been winning recently tend to keep winning for a while. Factor models decompose returns into these shared drivers.

Here is the key insight: **most of what makes stocks move is not unique to the individual company — it is shared across many companies.** The overall market explains roughly 30-60% of an individual stock's variance. Add size, value, and momentum and you can explain 50-70%. The residual — the part factor models *cannot* explain — is where a stock picker's skill (alpha) lives.

Think of it like a recipe for stock returns. The ingredients (factors) are market beta, size tilt, value tilt, and momentum. The recipe says how much of each ingredient goes into this particular stock (factor loadings or betas). Whatever is left over after the recipe is accounted for is the stock's unique, idiosyncratic flavor — its alpha.

This decomposition is useful for two purposes:
1. **Risk management:** Understand where your portfolio's variance is actually coming from. If 80% of your risk is just market beta, you're paying active management fees for a glorified index fund.
2. **Alpha isolation:** Strip out all factor exposure to see if you have genuine skill, or just a smart-sounding way to hold small-cap value stocks.

## Math Concepts

**The factor model equation.** For asset $i$ at time $t$:

$$r_{i,t} = \alpha_i + \sum_{j=1}^{K} \beta_{ij} F_{j,t} + \epsilon_{i,t}$$

| Term | Name | Meaning |
|------|------|---------|
| $r_{i,t}$ | Return | Excess return of asset $i$ over the risk-free rate |
| $\alpha_i$ | Alpha | Constant average return not explained by factors (the "skill") |
| $\beta_{ij}$ | Factor loading | Sensitivity of asset $i$ to factor $j$ |
| $F_{j,t}$ | Factor return | Return of factor $j$ at time $t$ |
| $\epsilon_{i,t}$ | Residual | Idiosyncratic, uncorrelated with all factors |

**Key assumptions:**
- $E[\epsilon_{i,t}] = 0$: residuals have zero mean
- $\text{Cov}(\epsilon_{i,t}, F_{j,t}) = 0$: residuals are uncorrelated with factors
- $\text{Cov}(\epsilon_{i,t}, \epsilon_{k,t}) = 0$ for $i \neq k$: residuals are pairwise uncorrelated (the factor structure explains all cross-asset covariance)

**Portfolio variance decomposition.** For a portfolio with weights $\mathbf{w}$:

$$\sigma_P^2 = \underbrace{\mathbf{w}^\top B \Sigma_F B^\top \mathbf{w}}_{\text{systematic/factor variance}} + \underbrace{\mathbf{w}^\top D \mathbf{w}}_{\text{idiosyncratic variance}}$$

where $B$ is the $N \times K$ matrix of factor loadings, $\Sigma_F$ is the $K \times K$ factor covariance matrix, and $D$ is a diagonal matrix of residual variances $\sigma_{\epsilon_i}^2$.

This factored form is what makes large portfolio covariance tractable: instead of estimating an $N \times N$ matrix (e.g., 500×500 for the S&P 500 = 125,000 parameters), you estimate a $K \times K$ factor covariance (perhaps 5×5 = 25 parameters) plus $N$ individual residual variances.

**Fama-French 3-Factor Model (1993).** The canonical academic factor model:

$$r_i - r_f = \alpha_i + \beta_i^{Mkt}(R_m - r_f) + \beta_i^{SMB} \cdot SMB + \beta_i^{HML} \cdot HML + \epsilon_i$$

| Factor | Abbreviation | Construction | Economic intuition |
|--------|-------------|-------------|-------------------|
| Market excess return | $R_m - r_f$ | Market return minus T-bill | Compensation for bearing market risk |
| Small Minus Big | SMB | Return of small-cap portfolio minus large-cap portfolio | Size premium (small firms are riskier/less liquid) |
| High Minus Low | HML | High book/price portfolio minus low book/price portfolio | Value premium (cheap stocks are riskier/distressed) |

**Fama-French 5-Factor (2015) adds:**
- **RMW** (Robust Minus Weak): profitability factor
- **CMA** (Conservative Minus Aggressive): investment factor

**Carhart 4-Factor (1997) adds to FF3:**
- **MOM** (Momentum): past winners minus past losers (12-month return excluding last month)

**Estimating betas.** Run OLS regression of excess stock returns on factor returns:

$$\hat{\boldsymbol{\beta}}_i = (F^\top F)^{-1} F^\top r_i$$

where $F$ is the $T \times K$ matrix of factor returns (time series) and $r_i$ is the $T \times 1$ vector of stock returns.

**Information Ratio after factor adjustment:**

$$IR = \frac{\hat{\alpha}_i}{\sigma_{\epsilon_i}}$$

This is the "pure alpha" per unit of idiosyncratic risk — a factor-neutral measure of skill.

## Walkthrough

**Goal:** Estimate Fama-French 3-factor loadings for a single stock (e.g., AAPL), then decompose its variance.

**Inputs (monthly data, 60 months):**
- $r_{AAPL}$: AAPL monthly excess return (vs T-bill)
- $Mkt-Rf$: Market excess return (e.g., CRSP value-weighted index minus T-bill)
- $SMB$: Small minus Big portfolio return (from Ken French's data library)
- $HML$: High minus Low portfolio return (from Ken French's data library)

**OLS regression output (hypothetical):**

| Parameter | Estimate | t-stat |
|-----------|----------|--------|
| $\alpha$ | +0.52%/month | 2.1 |
| $\beta_{Mkt}$ | 1.18 | 12.4 |
| $\beta_{SMB}$ | -0.32 | -3.1 |
| $\beta_{HML}$ | -0.48 | -4.7 |
| $R^2$ | 0.61 | — |

**Interpretation:**
- $\beta_{Mkt} = 1.18$: AAPL amplifies market moves by 18%. When the market is up 1%, AAPL is up 1.18%.
- $\beta_{SMB} = -0.32$: Negative SMB beta — AAPL behaves like a large-cap stock (makes sense: it's a mega-cap).
- $\beta_{HML} = -0.48$: Negative HML beta — AAPL is a growth stock (high price-to-book), which is the opposite of value.
- $\alpha = +0.52\%$: After stripping out all three factor exposures, AAPL earned 0.52% per month of "pure" alpha.
- $R^2 = 0.61$: 61% of AAPL's return variance is explained by these three factors. 39% is idiosyncratic.

**Variance decomposition (hypothetical):**

Suppose monthly $\sigma_{AAPL} = 8\%$, so $\sigma^2_{AAPL} = 64\%^2 = 0.0064$.
- Factor variance = $R^2 \times \sigma^2 = 0.61 \times 0.0064 = 0.0039$ (i.e., $\sigma_{factor} \approx 6.3\%$)
- Idiosyncratic variance = $(1 - R^2) \times \sigma^2 = 0.39 \times 0.0064 = 0.0025$ (i.e., $\sigma_{\epsilon} \approx 5.0\%$)

## Analysis

**Strengths:**
- Dramatically reduces the dimension of the covariance estimation problem.
- Cleanly separates systematic risk (compensated? — debated) from idiosyncratic risk (where alpha lives).
- Fama-French factors are freely available (Ken French data library) and widely used as benchmarks.
- Foundation for most commercial risk models (Barra, Axioma, Northfield).

**Weaknesses:**
- Factor choice is partly empirical, partly theoretical — the list keeps growing (there are now 400+ documented "factors" in the literature, the "factor zoo").
- OLS betas are estimated from historical data and are unstable over time (beta drift).
- The residual independence assumption is often violated in practice (sectors exhibit correlated idiosyncratic moves during stress).
- Factor models explain average covariance, not tail covariance. Correlations spike in crises.

**Known failure modes:**
- **Factor crowding:** When many quant funds load on the same factors (e.g., momentum), an unwind can create factor crashes — losses that look idiosyncratic in the model but are actually highly correlated across funds.
- **Look-ahead bias:** Fama-French style portfolios are constructed using end-of-year data; when backtesting, ensure you use only point-in-time data.
- **Structural breaks:** The value premium has been weak since 2010. Static factor loadings estimated from 1990-2010 will mismatch the 2010-2024 regime.
- **Missing factors:** Industry effects, country effects (in global portfolios), liquidity effects are often not captured by a simple 3- or 5-factor model.

**Commercial vs. academic models:**
- Academic (FF3, FF5, Carhart): transparent, free, good for research.
- Commercial (Barra USE4, Axioma): 60+ factors including industries, countries, technical factors. Paid, black-box, but calibrated for real-world risk management.

## Implementation

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# ── 1. Load Fama-French 3-Factor Data ─────────────────────────────────────
# In practice: download from https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
# Here we simulate synthetic data for illustration.

np.random.seed(42)
T = 120  # 10 years of monthly data

# Simulate factor returns (roughly calibrated to historical means/vols)
mkt_rf = np.random.normal(0.008, 0.045, T)  # ~8% annual excess return, 15% vol
smb    = np.random.normal(0.002, 0.030, T)  # ~2.4% annual, 10% vol
hml    = np.random.normal(0.003, 0.028, T)  # ~3.6% annual, 9.7% vol

# True loadings for a hypothetical growth stock
true_alpha    =  0.004  # 0.4%/month alpha
true_beta_mkt =  1.20
true_beta_smb = -0.30
true_beta_hml = -0.45
residual_vol  =  0.04   # 4%/month idiosyncratic vol

stock_returns = (
    true_alpha
    + true_beta_mkt * mkt_rf
    + true_beta_smb * smb
    + true_beta_hml * hml
    + np.random.normal(0, residual_vol, T)
)

factors = pd.DataFrame({'Mkt-RF': mkt_rf, 'SMB': smb, 'HML': hml})
returns = pd.Series(stock_returns, name='Stock')

# ── 2. OLS Regression to Estimate Factor Loadings ─────────────────────────
from numpy.linalg import lstsq

# Add intercept column for alpha
X = np.column_stack([np.ones(T), factors.values])
coeffs, residuals, rank, sv = lstsq(X, returns.values, rcond=None)

alpha_hat    = coeffs[0]
beta_mkt_hat = coeffs[1]
beta_smb_hat = coeffs[2]
beta_hml_hat = coeffs[3]

fitted   = X @ coeffs
resid    = returns.values - fitted
ss_res   = np.sum(resid**2)
ss_tot   = np.sum((returns.values - returns.mean())**2)
r_squared = 1 - ss_res / ss_tot

print("Factor Model OLS Results:")
print(f"  Alpha        : {alpha_hat:.4f} ({alpha_hat*12:.2%} annualized)")
print(f"  Beta (Market): {beta_mkt_hat:.3f}")
print(f"  Beta (SMB)   : {beta_smb_hat:.3f}")
print(f"  Beta (HML)   : {beta_hml_hat:.3f}")
print(f"  R-squared    : {r_squared:.3f}")

# ── 3. Variance Decomposition ──────────────────────────────────────────────
total_var      = np.var(returns.values, ddof=1)
idio_var       = np.var(resid, ddof=1)
systematic_var = total_var - idio_var
systematic_pct = systematic_var / total_var

print(f"\nVariance Decomposition:")
print(f"  Total variance     : {total_var:.6f}  (annualized vol: {np.sqrt(total_var*12):.2%})")
print(f"  Systematic (factor): {systematic_var:.6f}  ({systematic_pct:.1%})")
print(f"  Idiosyncratic      : {idio_var:.6f}  ({1-systematic_pct:.1%})")

# ── 4. Rolling Beta Estimation ─────────────────────────────────────────────
window = 36  # 3-year rolling window
rolling_betas = []
for start in range(T - window + 1):
    end   = start + window
    X_w   = np.column_stack([np.ones(window), factors.values[start:end]])
    r_w   = returns.values[start:end]
    b, _, _, _ = lstsq(X_w, r_w, rcond=None)
    rolling_betas.append({'t': end, 'alpha': b[0], 'beta_mkt': b[1], 'beta_smb': b[2], 'beta_hml': b[3]})

rolling_df = pd.DataFrame(rolling_betas)

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for ax, col, true_val, label in zip(
    axes.flat,
    ['alpha', 'beta_mkt', 'beta_smb', 'beta_hml'],
    [true_alpha, true_beta_mkt, true_beta_smb, true_beta_hml],
    ['Alpha', 'Market Beta', 'SMB Beta', 'HML Beta']
):
    ax.plot(rolling_df['t'], rolling_df[col], label='Rolling estimate')
    ax.axhline(true_val, color='red', linestyle='--', label=f'True: {true_val:.3f}')
    ax.set_title(f'Rolling {label} (36-month window)')
    ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig('rolling_betas.png', dpi=150)
plt.show()

# ── 5. Portfolio Factor Exposure ───────────────────────────────────────────
# For a portfolio with weights, compute net factor exposures
# Assume we have estimated betas for N assets

N = 20
np.random.seed(7)
# Simulate beta matrix: shape (N, K) where K=3 factors
B = np.random.normal([1.0, 0.0, 0.0], [0.4, 0.5, 0.5], size=(N, 3))
# Random equal-weight portfolio
w = np.ones(N) / N

# Portfolio factor exposures = weighted sum of asset betas
portfolio_betas = B.T @ w
print(f"\nEqual-weight portfolio factor exposures:")
print(f"  Market beta: {portfolio_betas[0]:.3f}")
print(f"  SMB beta   : {portfolio_betas[1]:.3f}")
print(f"  HML beta   : {portfolio_betas[2]:.3f}")

# Factor covariance (from historical factor data)
F_matrix = np.column_stack([mkt_rf, smb, hml])
Sigma_F  = np.cov(F_matrix.T)

# Portfolio systematic variance
sys_var_portfolio = portfolio_betas @ Sigma_F @ portfolio_betas
print(f"  Systematic monthly vol: {np.sqrt(sys_var_portfolio):.2%}")
```

## Bridge to Quant / ML

**Quant equity strategies.** Most systematic long/short equity strategies are built entirely in factor space:
- **Factor-neutral alpha:** Take signals, build a portfolio, then hedge out all factor exposures (market, size, value, sector) using futures or short positions. What remains is pure idiosyncratic return — pure alpha.
- **Factor investing / Smart Beta:** Build portfolios that deliberately tilt toward well-compensated factors (value, momentum, quality). This is the foundation of MSCI factor ETFs, AQR, and DFA.

**Risk attribution.** A portfolio's daily P&L can be decomposed: "Factor contribution today: -0.5% from market, +0.1% from momentum. Idiosyncratic contribution: +0.3%. Total: -0.1%." This is how risk managers identify whether a loss came from bad macro timing (factor) or bad stock selection (idiosyncratic).

**ML connections:**
- **PCA as factor discovery:** Principal Component Analysis on a returns matrix produces "statistical factors" — the top eigenvectors that explain the most variance. These are data-driven analogs of the Fama-French factors.
- **Autoencoders for nonlinear factors:** Deep autoencoders can learn nonlinear latent factor structures that outperform linear PCA in explaining cross-sectional return variance.
- **IPCA (Instrumented PCA):** Extends PCA by allowing factor loadings to vary as a function of observable firm characteristics (size, B/M, momentum). State-of-the-art in academic asset pricing as of 2024.
- **Regularized regression:** In high-dimensional factor models (many factors, potentially more than observations), ridge/lasso regression prevents overfitting when estimating betas.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** What is the economic intuition behind the Small Minus Big (SMB) and High Minus Low (HML) factors in the Fama-French model?
<details><summary>Answer</summary>**SMB (Small Minus Big):** Small-cap stocks historically earn higher returns than large-cap stocks after controlling for market beta. The economic story: small companies face higher distress risk, are less liquid, and receive less analyst coverage — investors demand a risk premium for bearing these risks. Mechanically, SMB is constructed as the average return of small-cap portfolios minus large-cap portfolios, capturing this size-related risk premium.

**HML (High Minus Low):** "High" and "Low" refer to the book-to-market ratio (book value / market price). High book-to-market = value stocks (cheap). Low book-to-market = growth stocks (expensive). Value stocks historically earn higher returns — the value premium. The economic story: value stocks are in some sense "distressed" (the market prices them low relative to assets), and investors require extra return to hold financially fragile companies. Mechanically, HML is long value and short growth portfolios.</details>

**Q2.** Why does decomposing the covariance matrix as $\Sigma = B\Sigma_F B^\top + D$ (factor structure) reduce the estimation problem dramatically for large portfolios?
<details><summary>Answer</summary>For $N = 500$ assets, the full covariance matrix has $N(N+1)/2 = 125,250$ parameters to estimate. With $K = 5$ factors, the factor structure requires: (a) $N \times K = 2,500$ factor loading estimates (the $B$ matrix); (b) $K(K+1)/2 = 15$ entries of the factor covariance $\Sigma_F$; (c) $N = 500$ diagonal entries for idiosyncratic variance $D$. Total: ~3,015 parameters — about 40× fewer. Each factor covariance parameter can be estimated from 252 observations with high precision ($K \ll T$). The factored matrix is also guaranteed positive definite by construction, avoiding the near-singular problems of large sample covariance matrices.</details>

**Q3.** What is the "factor zoo" problem, and why does it threaten the scientific validity of factor investing?
<details><summary>Answer</summary>Harvey, Liu, and Zhu (2016) documented 316 published factors (as of 2014), with hundreds more since. Each was documented as statistically significant in its own paper. The factor zoo problem: with hundreds of simultaneous tests, many factors pass the 5% significance threshold purely by chance (multiple testing). If you test 300 hypotheses at 5% significance, you expect 15 false discoveries even if none are real. True factors should be: (a) economically motivated; (b) robust to different time periods and geographies; (c) significant at much stricter thresholds (t > 3.0 after multiple-testing correction). Most factors in the zoo fail these tests. Alpha decay is the market evidence: documented factors are quickly arbitraged away once known.</details>

---

### Level 2 — Quantitative

**Q4.** A stock's monthly returns are regressed on Fama-French 3 factors. Results: $\alpha = 0.3\%/\text{month}$, $\beta_{\text{mkt}} = 1.1$, $\beta_{\text{SMB}} = 0.4$, $\beta_{\text{HML}} = -0.5$, $R^2 = 0.62$, monthly vol = 7%. (a) What does $\beta_{\text{SMB}} = 0.4$ mean for this stock? (b) What is the annualized alpha? (c) What fraction of monthly variance is idiosyncratic? (d) What is the idiosyncratic monthly vol?
<details><summary>Answer</summary>

(a) $\beta_{\text{SMB}} = 0.4$ means the stock has positive exposure to the size factor — it behaves like a small-cap stock. When small caps outperform large caps by 1%, this stock tends to earn an extra 0.4%.

(b) Annualized alpha: $\alpha_{\text{annual}} = 0.3\% \times 12 = \mathbf{3.6\%/\text{year}}$

(c) Idiosyncratic fraction: $1 - R^2 = 1 - 0.62 = \mathbf{38\%}$

(d) Total monthly variance: $(0.07)^2 = 0.0049$

Idiosyncratic variance: $0.38 \times 0.0049 = 0.001862$

Idiosyncratic monthly vol: $\sqrt{0.001862} = \mathbf{4.32\%/\text{month}}$</details>

**Q5.** A portfolio holds 40% in stock A ($\beta_{\text{mkt}}^A = 1.2$, $\beta_{\text{SMB}}^A = 0.5$) and 60% in stock B ($\beta_{\text{mkt}}^B = 0.8$, $\beta_{\text{SMB}}^B = -0.3$). The market factor monthly vol is 4.5% and the SMB factor monthly vol is 2.5%. The market-SMB correlation is $-0.1$. What is the portfolio's systematic monthly variance (ignoring idiosyncratic terms)?
<details><summary>Answer</summary>

Portfolio factor betas (weighted sum):
- $\beta_{\text{mkt}}^P = 0.4(1.2) + 0.6(0.8) = 0.48 + 0.48 = 0.96$
- $\beta_{\text{SMB}}^P = 0.4(0.5) + 0.6(-0.3) = 0.20 - 0.18 = 0.02$

Factor covariance matrix: $\Sigma_F = \begin{pmatrix}\sigma_{\text{mkt}}^2 & \rho\sigma_{\text{mkt}}\sigma_{\text{SMB}} \\ \cdot & \sigma_{\text{SMB}}^2\end{pmatrix} = \begin{pmatrix}0.002025 & -0.001125 \\ -0.001125 & 0.000625\end{pmatrix}$

Systematic variance: $\mathbf{b}^\top \Sigma_F \mathbf{b}$ where $\mathbf{b} = (0.96, 0.02)^\top$:

$= (0.96)^2(0.002025) + (0.02)^2(0.000625) + 2(0.96)(0.02)(-0.001125)$

$= 0.001868 + 0.00000025 - 0.0000432 = \mathbf{0.001825}$

Systematic monthly vol: $\sqrt{0.001825} = \mathbf{4.27\%/\text{month}}$</details>

---

### Level 3 — Coding

**Q6.** The implementation uses `numpy.linalg.lstsq` for the factor regression rather than `sklearn.linear_model.LinearRegression`. What is the advantage of `lstsq` in this context, and how would you extend the rolling beta code to detect a structural break (a regime change in beta)?
<details><summary>Answer</summary>

`lstsq` solves the normal equations directly via SVD, handling near-singular designs robustly and returning the rank of the system — useful for diagnosing multicollinear factors. `LinearRegression` is a higher-level wrapper that also uses SVD internally but doesn't expose rank information. For factor model work, `lstsq` gives more direct control and is slightly faster when calling thousands of regressions (e.g., for each asset in a 500-stock universe).

To detect structural breaks in beta, use the **Chow test**: split the sample at a candidate break date $t^*$, run separate regressions before and after, and test whether the coefficients differ significantly using an F-test:
```python
from scipy import stats
# Estimate restricted model (pooled) and unrestricted (split)
ss_restricted = np.sum(resid_pooled**2)
ss_unrestricted = np.sum(resid_before**2) + np.sum(resid_after**2)
k = 4  # number of parameters (alpha + 3 betas)
F = ((ss_restricted - ss_unrestricted) / k) / (ss_unrestricted / (T - 2*k))
p_value = 1 - stats.f.cdf(F, dfn=k, dfd=T-2*k)
```
Alternatively, plot the CUSUM (cumulative sum of recursive residuals) — a sharp departure from zero signals a structural break without specifying the break date in advance.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Factor exposure to SMB guarantees a return premium | Factor premia are ex-ante expectations, not realized guarantees. The SMB premium has been near zero since 2010 in US equities. |
| Idiosyncratic risk is truly zero-correlation across stocks | The factor model assumes zero idiosyncratic covariance. In practice, industry effects and macro events create correlated residuals, especially in crises. |
| More factors always improve the model | More factors risk overfitting. Each additional factor adds parameters and requires statistical justification. The $R^2$ will always increase with more factors, but out-of-sample prediction may worsen. |
| Alpha measured from factor models is pure skill | Alpha is only as "pure" as the factor model is complete. Omitting a true risk factor makes its premium look like alpha. |

## Related Concepts

- [[Value at Risk]] — factor models provide the covariance structure needed for parametric VaR
- [[Expected Shortfall]] — factor-based covariance feeds directly into parametric ES
- [[Sharpe Ratio]] — factor-adjusted alpha is the numerator of the information ratio
- [[Kelly Criterion]] — optimal sizing uses factor model estimates of alpha and variance

## Sources Used

- Fama, E. F., & French, K. R. (1993). Common risk factors in the returns on stocks and bonds. *Journal of Financial Economics*, 33(1), 3-56
- Carhart, M. M. (1997). On persistence in mutual fund performance. *Journal of Finance*, 52(1), 57-82
- Cochrane, J. H. (2009). *Asset Pricing*, revised ed., ch. 9 — factor models and the cross-section of returns
- MSCI Barra. *Factor Models for Risk Management* (product documentation)

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review: no issues found | quality review |
