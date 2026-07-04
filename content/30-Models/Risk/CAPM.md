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
  - "Sharpe, W.F. (1964). Capital asset prices: A theory of market equilibrium under conditions of risk. Journal of Finance, 19(3), 425-442"
  - "Fama, E.F. & French, K.R. (1992). The Cross-Section of Expected Stock Returns. Journal of Finance, 47(2), 427-465"
  - "Lintner, J. (1965). The Valuation of Risk Assets and the Selection of Risky Investments. Review of Economics and Statistics"
created: 2026-04-18
---

> [!info] Problem Chain
> **Chain:** Hedging & Risk → Gap 5: Markowitz is unstable — inputs are unreliable, outputs are extreme
> **This concept:** CAPM asks "if all investors do MVO, what is the equilibrium?" — answering that expected return should depend only on beta (systematic risk), since idiosyncratic risk can be freely diversified away.
> **Alternative approaches to this gap:** [[Factor Models]], [[Risk Parity]], [[Black-Litterman]], [[Hierarchical Risk Parity]]
> **You need first:** [[Markowitz Mean-Variance Optimization]], [[Efficient Frontier]]
> **This unlocks:** [[Factor Models]], [[Black-Litterman]]

## Why This Exists

**The gap:** MVO tells you how to build an optimal portfolio given expected returns, but it does not say what those expected returns *should be* in equilibrium. If all investors are rational, what expected return should each asset offer?

**What came before:** Markowitz and the Efficient Frontier described the problem and the solution structure, but each investor still needed their own return estimates. There was no theory of what returns were "fair" given risk.

**What this adds:** CAPM derives equilibrium expected returns from first principles. If all investors do MVO with the same beliefs and the risk-free asset is available, they all hold the same risky portfolio — the market portfolio. This means: (a) only systematic risk (beta) earns a premium, because idiosyncratic risk can be diversified away for free; (b) the market portfolio is the tangency portfolio; (c) alpha is the deviation from CAPM prediction — the residual that defines excess skill.

**What it still doesn't solve:** CAPM is empirically rejected. Small-cap stocks and value stocks earn more than their beta predicts (Fama-French 1992). Beta alone cannot explain the cross-section of returns. The market portfolio is theoretically the universe of all assets, but is proxied in practice by imperfect indices (Roll's critique). Factor Models generalize CAPM to address these failures.

Start from a thought experiment. Suppose *every investor* on Earth reads Markowitz's paper and follows it — they all build the mean-variance optimal portfolio. What happens?

If everyone is holding the same optimally diversified portfolio, then in equilibrium, **the market portfolio** (every asset, weighted by its market capitalization) *must* be the optimal portfolio. Because if everyone holds the same thing, and that thing has to sum to the market, then the market itself is optimal.

Now ask: if the market is the optimal portfolio, what should any individual stock's expected return be? CAPM answers this with a beautifully clean result: **an asset's expected return depends on exactly one thing — its sensitivity to the market**.

Why only that? Because in a world where everyone is diversified, **idiosyncratic risk doesn't matter**. The unique wobbles of a single stock get averaged away when you hold hundreds of them. The only risk you *can't* diversify away is the risk that moves the whole market — recessions, interest rate shocks, pandemics. That's called **systematic risk**, and the market compensates you for bearing it. But it doesn't pay you for risk you could have eliminated for free just by diversifying.

A stock's sensitivity to market moves is called **beta** ($\beta$). A stock with $\beta = 1.5$ tends to move 1.5x as much as the market — it amplifies systematic risk. CAPM says that stock's expected return should be correspondingly higher. A stock with $\beta = 0.5$ is cushioned from market swings and earns proportionally less.

Any return a stock earns *above* what CAPM predicts, given its beta, is called **alpha** ($\alpha$). Alpha is the holy grail in quant finance — it means the asset is earning more than its risk warrants.

## Math Concepts

**The CAPM equation (Security Market Line):**

$$\boxed{E[R_i] = R_f + \beta_i \cdot (E[R_m] - R_f)}$$

| Term | Meaning |
|------|---------|
| $E[R_i]$ | Expected return of asset $i$ |
| $R_f$ | Risk-free rate (e.g., T-bill rate) |
| $E[R_m]$ | Expected return of the market portfolio |
| $E[R_m] - R_f$ | **Market risk premium** — excess return for bearing market risk |
| $\beta_i$ | Asset's sensitivity to market returns |

**Beta:**

$$\beta_i = \frac{\text{Cov}(R_i, R_m)}{\text{Var}(R_m)} = \frac{\sigma_{i,m}}{\sigma_m^2}$$

Beta measures how much the asset co-moves with the market. Equivalently, it is the slope coefficient in the OLS regression:

$$R_i = \alpha_i + \beta_i R_m + \epsilon_i$$

where $\epsilon_i$ is the idiosyncratic (diversifiable) return component.

**Alpha:**

$$\alpha_i = \text{Actual return} - \text{CAPM-predicted return} = R_i - [R_f + \beta_i(R_m - R_f)]$$

An asset with $\alpha > 0$ is outperforming on a risk-adjusted basis. Finding assets (or strategies) with persistent positive alpha is the entire business of active investing.

**Decomposing total risk:**

$$\underbrace{\sigma_i^2}_{\text{total risk}} = \underbrace{\beta_i^2 \sigma_m^2}_{\text{systematic risk}} + \underbrace{\sigma_{\epsilon_i}^2}_{\text{idiosyncratic risk}}$$

CAPM says only the systematic portion earns a premium.

**The Security Market Line (SML):** In a plot of $(\beta, E[R])$, the SML is a straight line from $(0, R_f)$ through $(1, E[R_m])$. All assets should lie on this line in equilibrium. Assets above the SML have positive alpha (underpriced); assets below have negative alpha (overpriced).

| Beta value | Interpretation |
|-----------|----------------|
| $\beta = 0$ | Risk-free rate only; no market exposure (e.g., T-bills) |
| $\beta = 1$ | Moves with the market (e.g., an index fund) |
| $\beta > 1$ | Amplifies market moves; higher return expected (e.g., tech growth stocks) |
| $\beta < 0$ | Negatively correlated with market (rare; e.g., some gold, VIX products) |

## Walkthrough

**Setup:** $R_f = 3\%$, $E[R_m] = 8\%$, market risk premium = $5\%$. A stock has $\beta = 1.5$.

**Step 1 — CAPM expected return:**

$$E[R_i] = 3\% + 1.5 \times (8\% - 3\%) = 3\% + 7.5\% = 10.5\%$$

CAPM says: given this stock's market sensitivity, a rational investor should demand 10.5% expected return to hold it.

**Step 2 — Actual return:** The stock returned 12% over the period.

**Step 3 — Alpha:**

$$\alpha = 12\% - 10.5\% = +1.5\%$$

This stock earned 1.5% more than CAPM says it should have, given its risk. That excess is alpha — either the stock was mispriced, or CAPM is missing something.

**Step 4 — Estimating beta from data:** Regress weekly stock returns on market returns over 3 years:

```
R_stock = alpha + beta * R_market + epsilon
```

The OLS slope estimate $\hat{\beta}$ is the empirical beta. The $R^2$ of this regression tells you what fraction of the stock's variance is explained by market risk (systematic) vs. idiosyncratic.

## Analysis

**CAPM is empirically rejected — but conceptually indispensable.**

Fama and French (1992) showed that beta alone does *not* explain the cross-section of stock returns. Small-cap stocks earn higher returns than CAPM predicts (the "size premium"). Value stocks (low price-to-book) earn more than growth stocks (the "value premium"). Neither is captured by beta.

This led to [[Factor Models]]:

| Model | Factors | Year |
|-------|---------|------|
| CAPM | Market (1 factor) | 1964 |
| Fama-French 3-factor | Market + Size (SMB) + Value (HML) | 1993 |
| Carhart 4-factor | + Momentum (MOM) | 1997 |
| Fama-French 5-factor | + Profitability (RMW) + Investment (CMA) | 2015 |

Despite being empirically flawed, CAPM remains the standard framework for:

1. **Cost of capital estimation** — corporations use CAPM to compute their required rate of return for project valuation (DCF analysis).
2. **Alpha measurement** — even multifactor models use CAPM logic; alpha is always "return unexplained by risk".
3. **Conceptual foundation** — the intuition that diversifiable risk earns no premium is correct and deeply important, even if the single-factor version is incomplete.

**Key limitations:**

- Assumes investors have homogeneous expectations (same beliefs about $\boldsymbol{\mu}$ and $\boldsymbol{\Sigma}$) — unrealistic.
- Market portfolio is unobservable; in practice the S&P 500 or a broad index is used as a proxy (Roll's critique, 1977).
- Beta is estimated from historical data, but forward-looking beta may differ.
- Linear: assumes the relationship between stock and market returns is linear, which fails in tail events.

## Implementation

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# ── Simulate stock and market returns ────────────────────────────────────────
np.random.seed(42)
n = 252 * 3  # 3 years of daily data

true_beta = 1.5
rf_daily  = 0.03 / 252       # 3% annual risk-free rate
mkt_mean  = 0.08 / 252       # 8% annual market return

# Market returns
r_market = np.random.normal(mkt_mean, 0.01, n)

# Stock returns: alpha + beta * market + idiosyncratic noise
true_alpha_daily = 0.015 / 252   # 1.5% annual alpha
r_stock = (true_alpha_daily
           + true_beta * r_market
           + np.random.normal(0, 0.012, n))  # idiosyncratic noise

# ── 1. Estimate beta via OLS ─────────────────────────────────────────────────
# Excess returns (above risk-free)
excess_mkt   = r_market - rf_daily
excess_stock = r_stock  - rf_daily

slope, intercept, r_value, p_value, se = stats.linregress(excess_mkt, excess_stock)

beta_hat  = slope
alpha_hat = intercept * 252   # annualized

print("── CAPM Regression Results ──────────────────────")
print(f"Estimated beta:   {beta_hat:.4f}  (true: {true_beta})")
print(f"Estimated alpha:  {alpha_hat:.2%} annualized  (true: {true_alpha_daily*252:.2%})")
print(f"R²:               {r_value**2:.3f}  ({r_value**2:.1%} of variance explained by market)")
print(f"p-value (beta):   {p_value:.2e}")

# ── 2. CAPM-predicted return vs actual ───────────────────────────────────────
e_rm = np.mean(r_market) * 252   # realized annualized market return
e_rf = rf_daily * 252

capm_predicted = e_rf + beta_hat * (e_rm - e_rf)
actual_return  = np.mean(r_stock) * 252
realized_alpha = actual_return - capm_predicted

print(f"\nActual annualized return:   {actual_return:.2%}")
print(f"CAPM predicted return:      {capm_predicted:.2%}")
print(f"Realized alpha:             {realized_alpha:.2%}")

# ── 3. Security Market Line plot ──────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left panel: regression scatter (characteristic line)
ax = axes[0]
beta_range = np.linspace(excess_mkt.min(), excess_mkt.max(), 100)
ax.scatter(excess_mkt, excess_stock, alpha=0.2, s=5, color='steelblue', label='Daily returns')
ax.plot(beta_range, intercept + slope * beta_range, 'r-', linewidth=2,
        label=f'OLS fit: β={beta_hat:.3f}, α={alpha_hat:.2%}/yr')
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.set_xlabel('Excess Market Return')
ax.set_ylabel('Excess Stock Return')
ax.set_title('Characteristic Line (Beta Estimation)')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Right panel: Security Market Line
ax = axes[1]
betas = np.linspace(-0.5, 2.5, 100)
sml_returns = e_rf + betas * (e_rm - e_rf)

ax.plot(betas, sml_returns, 'k-', linewidth=2, label='Security Market Line (SML)')
ax.scatter(beta_hat, actual_return, color='red', s=120, zorder=5,
           label=f'Our stock (α={realized_alpha:.2%})')
ax.scatter(1.0, e_rm, color='blue', s=80, marker='^', zorder=5, label='Market portfolio')
ax.scatter(0.0, e_rf, color='green', s=80, marker='s', zorder=5, label='Risk-free asset')

ax.set_xlabel('Beta (β)')
ax.set_ylabel('Expected Return (annualized)')
ax.set_title('Security Market Line')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('capm_analysis.png', dpi=150)
plt.show()

# ── 4. Risk decomposition ─────────────────────────────────────────────────────
total_var      = np.var(r_stock, ddof=1)
systematic_var = beta_hat**2 * np.var(r_market, ddof=1)
idio_var       = total_var - systematic_var

print(f"\n── Risk Decomposition ───────────────────────────")
print(f"Total variance:       {total_var:.6f}  (vol = {np.sqrt(total_var)*np.sqrt(252):.2%}/yr)")
print(f"Systematic variance:  {systematic_var:.6f}  ({systematic_var/total_var:.1%} of total)")
print(f"Idiosyncratic var:    {idio_var:.6f}  ({idio_var/total_var:.1%} of total)")
```

## Bridge to Quant / ML

**Alpha is the currency of quant finance.** Every systematic trading strategy can be framed as an attempt to find positive alpha relative to some benchmark model. CAPM is the simplest benchmark; [[Factor Models]] are more demanding benchmarks. A strategy with high Sharpe but zero alpha (all return explained by beta) isn't really adding value — it's just levered market exposure.

**Factor models generalize CAPM.** The Fama-French model is literally CAPM with more betas: $E[R_i] = R_f + \beta_{\text{mkt}} \lambda_{\text{mkt}} + \beta_{\text{size}} \lambda_{\text{size}} + \beta_{\text{value}} \lambda_{\text{value}} + \ldots$. Modern ML factor models use hundreds of characteristics to estimate expected returns, but the structure is identical.

**Beta estimation in ML pipelines.** Time-varying beta (the market relationship isn't constant) is estimated with Kalman filters, rolling windows, or LSTM models. Predicted beta feeds directly into risk models used by portfolio optimizers.

**CAPM as a null hypothesis.** In quantitative research, CAPM-adjusted returns (residuals $\epsilon_i$ from the characteristic line regression) are the input to many ML models. Stripping out beta exposure ensures the model is hunting for true alpha, not leveraged market beta in disguise.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why does CAPM say idiosyncratic (company-specific) risk earns no premium, while systematic (market) risk does?
<details><summary>Answer</summary>Idiosyncratic risk is diversifiable — if you hold a sufficiently large portfolio, company-specific shocks cancel out (some stocks have good news, others have bad, and the average is smooth). Because you can eliminate this risk for free just by holding more stocks, the market will not compensate you for bearing it: any asset offering a premium for idiosyncratic risk would be immediately bought until the premium vanished. Systematic risk (market beta) cannot be diversified away — when the whole market falls, every stock falls. Since you cannot escape it, the market must compensate you for bearing it. This is the equity risk premium ($E[R_m] - R_f$).</details>

**Q2.** What is "alpha" in the CAPM framework, and why is finding persistent alpha considered so difficult?
<details><summary>Answer</summary>Alpha is the return earned above what CAPM predicts given beta: $\alpha = R_i - [R_f + \beta_i(R_m - R_f)]$. It represents return that cannot be explained by market exposure — pure excess skill or mispricing. Finding persistent alpha is difficult because: (1) markets are competitive — any systematic mispricing attracts capital, which drives out the anomaly; (2) estimated alpha from historical data is statistically noisy (low signal-to-noise ratio); (3) many measured "alphas" turn out to be exposure to factor risks not in CAPM (size, value, momentum) that simply looked like skill when only beta was controlled for.</details>

**Q3.** Explain Roll's (1977) critique of CAPM tests. Why can CAPM never be truly tested?
<details><summary>Answer</summary>Roll's critique: the theoretical market portfolio in CAPM includes *every* investable asset — all stocks, bonds, real estate, human capital, etc. In practice, we proxy it with an index like the S&P 500, which represents only a fraction of true wealth. Any test of CAPM is actually a joint test of the model AND the proxy used for the market portfolio. If CAPM appears to fail, it could be because the model is wrong — or because our proxy is inadequate. Since the true market portfolio is unobservable, CAPM is untestable in its strict form. This means all empirical results on CAPM (including Fama-French's rejection) are conditional on the specific market proxy used.</details>

---

### Level 2 — Quantitative

**Q4.** A stock has $\beta = 1.3$. The risk-free rate is $R_f = 2\%$ and the market risk premium is $E[R_m] - R_f = 6\%$. (a) What is the CAPM-predicted expected return? (b) If the stock actually returned 11% last year, what is its realized alpha? (c) Decompose the stock's variance: if the stock's total annual vol is 28% and the market annual vol is 16%, what fraction of variance is systematic?
<details><summary>Answer</summary>

(a) CAPM expected return: $E[R_i] = R_f + \beta \cdot (E[R_m] - R_f) = 2\% + 1.3 \times 6\% = 2\% + 7.8\% = \mathbf{9.8\%}$

(b) Realized alpha: $\alpha = 11\% - 9.8\% = \mathbf{+1.2\%}$

(c) Systematic variance: $\beta^2 \sigma_m^2 = (1.3)^2 (0.16)^2 = 1.69 \times 0.0256 = 0.04326$

Total variance: $(0.28)^2 = 0.0784$

Systematic fraction: $0.04326 / 0.0784 = \mathbf{55.2\%}$

Idiosyncratic fraction: $44.8\%$. This is what can be diversified away in a large portfolio. ($R^2$ of the regression = 55.2%.)</details>

**Q5.** Three stocks have betas: Stock A ($\beta = 0.8$), Stock B ($\beta = 1.2$), Stock C ($\beta = 1.6$). Risk-free rate = 3%, market return = 8%. (a) Plot the expected returns on the Security Market Line. (b) If Stock C actually has expected return 14%, is it above or below the SML? Is it overpriced or underpriced?
<details><summary>Answer</summary>

(a) SML: $E[R] = 3\% + \beta \times (8\% - 3\%) = 3\% + 5\% \beta$

- Stock A: $3\% + 5\%(0.8) = \mathbf{7.0\%}$
- Stock B: $3\% + 5\%(1.2) = \mathbf{9.0\%}$
- Stock C: $3\% + 5\%(1.6) = \mathbf{11.0\%}$

(b) Stock C's actual expected return is 14% but CAPM predicts only 11%. It plots **above** the SML.

Above the SML = positive alpha = the stock offers more return than its risk warrants = **underpriced** (the market is not pricing in all the excess return). In equilibrium, investors would buy it, driving the price up and the expected return back down to the SML.</details>

---

### Level 3 — Coding

**Q6.** The code estimates beta via OLS regression of stock excess returns on market excess returns. Describe two ways that OLS beta estimation is biased or inconsistent in practice, and for each, describe a more robust alternative.
<details><summary>Answer</summary>

**Bias 1 — Errors-in-variables (measurement error in the market return):** The market return itself is estimated from an imperfect proxy. When the independent variable is measured with error, OLS produces a downward-biased (attenuated) beta estimate. **Fix:** Use Errors-in-Variables regression, or use multiple market proxies and IV estimation.

**Bias 2 — Time-varying beta:** Beta is not constant over time. A stock's market sensitivity changes with leverage, business conditions, and market regimes. OLS beta from a 3-year window averages over different regimes and produces a stale estimate. **Fix:** Use a Kalman filter to estimate time-varying beta dynamically, or use EWMA-weighted regression that gives more weight to recent observations. The code's rolling beta section hints at this: the rolling estimates visibly drift around the true value.

Bonus: **non-synchronous trading bias** — for illiquid stocks, returns are measured at bid/ask bounces or stale prices, introducing autocorrelation in residuals and biasing beta estimates. Fix: use Dimson (1979) aggregated beta, regressing on lagged market returns as well as contemporaneous.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| CAPM beta captures all risk | Beta only captures systematic (market) risk. Factor exposures (value, size, momentum) contribute to expected returns that CAPM misses. |
| A stock with alpha > 0 is always a buy | Alpha is estimated with noise. Statistical significance requires years of data. "Positive alpha" in a short backtest is usually noise. |
| Low-beta stocks are safe | Low-beta stocks have less market sensitivity, but they can still have large idiosyncratic risk (high stock-specific events). |
| The market portfolio is the S&P 500 | The market portfolio in theory includes all risky assets globally — stocks, bonds, real estate, private equity, human capital. S&P 500 is a narrow proxy. |

## Related Concepts

- [[Factor Models]] — extensions that add size, value, momentum, profitability as additional risk factors
- [[Markowitz Mean-Variance Optimization]] — the foundation CAPM builds on; MVO for all investors implies CAPM equilibrium
- [[Efficient Frontier]] — CAPM implies the market portfolio sits on the efficient frontier
- [[Sharpe Ratio]] — the CAPM SML slope equals the market Sharpe; individual alpha measures excess Sharpe

## Sources Used

- Sharpe, W. F. (1964). Capital asset prices: A theory of market equilibrium under conditions of risk. *Journal of Finance*, 19(3), 425–442
- Lintner, J. (1965). The valuation of risk assets and the selection of risky investments in stock portfolios and capital budgets. *Review of Economics and Statistics*, 47(1), 13–37
- Fama, E. F. & French, K. R. (1992). The cross-section of expected stock returns. *Journal of Finance*, 47(2), 427–465
- Roll, R. (1977). A critique of the asset pricing theory's tests. *Journal of Financial Economics*, 4(2), 129–176

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | initial build |
| 2026-04-11 | QA review: renamed "Implementation (Python)" → "Implementation"; removed non-vault wikilink [[Alpha Factor]] | quality review |
