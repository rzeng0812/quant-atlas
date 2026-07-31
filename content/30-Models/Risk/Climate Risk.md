---
type: concept
domain: 30-Models
tags: [risk, portfolio, esg]
status: emerging
stability: emerging
confidence: medium
last_reviewed: 2026-07-30
review_interval_days: 180
sources:
  - "Azzone, Bechi & Sbaiz (2026), Temperature Anomalies and Climate Physical Risk in Portfolio Construction, arXiv:2604.11143v1"
  - "Panda & Saha (2026), Climate Risk Stress Testing in California: A Geospatial Framework for Banking and Climate-Exposed Sectors, arXiv:2604.16716v1"
  - "Palaisti (2026), Climate-Aware Copula Models for Sovereign Rating Migration Risk, arXiv:2604.07567v1"
created: 2026-07-30
---

> [!info] Problem Chain
> **Chain:** Risk Management → Gap: Classical risk models (covariance estimation, VaR, stress testing) treat asset return dependence as stationary and driven by financial/macro factors alone, missing a structurally different, physically-grounded risk source
> **This concept:** Climate risk splits into physical risk — direct damage from weather/temperature events — and transition risk — repricing from policy/technology shifts — and both require extending classical dependence and stress-testing frameworks with climate-specific data and structure
> **Alternative approaches to this gap:** treating climate as just another macro factor in a standard multi-factor model (the naive baseline this literature moves beyond)
> **You need first:** [[Stress Testing]], [[Correlation and Covariance Estimation]]
> **This unlocks:** climate-aware regulatory capital requirements, transition-risk credit modeling

## Why This Exists

**The gap:** Classical risk machinery — sample or shrinkage covariance matrices, VaR, historical/hypothetical stress scenarios — assumes that dependence between assets is driven by financial and macroeconomic factors (market beta, rates, credit spreads) and is at least locally stationary. Climate risk breaks both assumptions. It is geographically and sectorally concentrated in ways a standard factor loading does not capture (a wildfire does not care about a firm's sector classification, only its county), and its underlying statistical drivers — temperature anomalies, hazard intensity, drought/flood probability — have persistence, clustering, and tail-dependence properties that differ from financial return statistics. A covariance matrix estimated on daily equity returns has no channel through which "this county is in a very-high wildfire severity zone" or "this sovereign's carbon intensity is rising" can enter.

**What came before:** Practitioner treatment of climate risk was mostly informal — ESG scores, exclusionary screening (divest from "high-carbon" sectors), and static, backward-looking country-level climate-vulnerability indices. These approaches assign a single number to an issuer or country and do not model *how* physical or transition shocks propagate into returns, defaults, or rating migrations, nor how that propagation varies over time or clusters across counterparties.

**What this adds:** Three concrete, rigorous extensions, one per paper grounding this note. Azzone, Bechi & Sbaiz build a **portfolio-construction** input: time-varying, firm/sector-specific climate exposure metrics derived directly from temperature-anomaly data and panel-regression evidence that extreme temperature events depress sectoral equity returns, plugged into a multi-objective optimizer alongside return and variance. Panda & Saha build a **geospatial bank stress-testing framework**: physical hazard maps (wildfire, drought, flood, heat) linked to loan/asset geography, feeding scenario-contingent PD/LGD/EAD credit-loss calculations and a Climate-VaR metric. Palaisti builds a **climate-aware copula** for sovereign credit rating migrations: a time-series copula process (MAGMAR) that lets climate covariates modulate the dependence structure of joint rating-downgrade activity across sovereigns, rather than assuming a static Gaussian dependence.

**What it still doesn't solve:** All three papers are explicit about real limitations. Panda & Saha present a *methodological* framework — the PD and Climate-VaR equations contain unestimated coefficients ($\beta_1,\beta_2,\dots$) "awaiting empirical estimation," and the paper reports no calibrated numeric stress-test outputs. Palaisti finds that climate covariates (carbon intensity) meaningfully improve the *marginal* models of rating-downgrade intensity but provide only "limited incremental explanatory power" once you try to use them to explain the *joint dependence* structure across sovereigns — the aggregate climate proxy is too coarse, or the historical record of climate-driven multi-sovereign downgrade clusters is too short, to identify a distinct climate-dependence effect from the baseline copula. More broadly, this is a young sub-field: there is no multi-decade backtesting record of climate-driven financial crises analogous to the 2008/2020/1997 stress scenarios that anchor classical [[Stress Testing]], so model validation rests on far weaker empirical ground than VaR or credit-risk models built on decades of default and market data.

## Math Concepts

### (a) Temperature anomalies as a portfolio-construction input (Azzone, Bechi & Sbaiz)

The authors first establish, via panel regression on sectoral excess returns, that extreme temperature events are priced:

$$R_{s,k,t} - R_{f,t} = \alpha_s + \beta_{mkt,s}(R_{mkt,t} - R_{f,t}) + \gamma_s B_{k,t} + FE_{month} + FE_{continent} + \varepsilon_{s,k,t}$$

where $B_{k,t}$ is a Bernoulli-type indicator of an extreme temperature anomaly event in region $k$ at time $t$, and $\gamma_s$ is the sector-specific sensitivity to that event. The pooled estimate is $\Gamma = -0.003$ ($p = 0.0096$), and 17 of 23 sectors show statistically significant negative coefficients ($\gamma_s$ ranging from $-0.0026$ to $-0.0139$) — extreme temperature events are a systematic, negatively-priced risk factor for most sectors, not just energy or utilities.

From this the paper builds two portfolio-level metrics. Let $p_{k,t}$ be the *time-varying* probability of an extreme temperature anomaly in region $k$ at time $t$ (so $B_{k,t} \sim \text{Bernoulli}(p_{k,t})$, hence $\text{Var}(B_{k,t}) = p_{k,t}(1-p_{k,t})$), and let $\alpha_k(\mathbf{w})$ be the portfolio's asset-intensity-weighted exposure to region $k$ implied by weights $\mathbf{w}$.

**Climate Risk Exposure (CRE)** — the expected portfolio exposure to extreme climate events:

$$\text{CRE}(\mathbf{w}, t) = \mathbb{E}\left[\sum_k \alpha_k(\mathbf{w}) B_{k,t}\right] = \sum_k \alpha_k(\mathbf{w})\, p_{k,t}$$

**Climate Exposure Volatility (CEV)** — the variance of that exposure, decomposed into an idiosyncratic (geographic dispersion) term and a systemic (cross-region co-movement) term:

$$\text{CEV}(\mathbf{w}, t) = \text{Var}\left(\sum_k \alpha_k(\mathbf{w}) B_{k,t}\right) = \sum_k \alpha_k(\mathbf{w})^2\, p_{k,t}(1-p_{k,t}) + 2\sum_{k<j} \alpha_k(\mathbf{w})\alpha_j(\mathbf{w})\, \text{Cov}(B_{k,t}, B_{j,t})$$

The covariance term uses empirical correlations between continental/regional temperature anomalies — this is the mechanism by which climate risk gets a *dependence structure*, distinct from a static country index.

These metrics feed a **multi-objective portfolio optimization** that extends Markowitz mean-variance with a third objective:

$$\min_{\mathbf{w}} \; F(\mathbf{w}) = \big[f_1(\mathbf{w}),\, f_2(\mathbf{w}),\, f_3(\mathbf{w})\big]^\top, \qquad f_1 = -\mathbf{w}^\top \mathbf{r}, \quad f_2 = \mathbf{w}^\top \Sigma \mathbf{w}, \quad f_3 = \text{CEV}(\mathbf{w})$$

subject to $\sum_i w_i = 1$, $w_i \geq 0$. This is solved numerically (the paper uses Multi-Objective Particle Swarm Optimization — 300 iterations, 500 particles, repository size 400) since there is no closed-form solution once a third, non-quadratic objective is added. Note $\Sigma$ here is the ordinary return covariance matrix — see [[Correlation and Covariance Estimation]]; climate risk enters as an *additional* objective, not a replacement for it.

### (b) Geospatial bank stress testing (Panda & Saha)

The framework is a three-layer architecture connecting physical geography to bank balance sheets:

1. **Hazard measurement** — a hazard intensity score $H_{g,s}$ for geographic unit $g$ (county- or asset-level, sourced from NOAA climate records, CAL FIRE hazard severity layers, property assessor files) under scenario $s$.
2. **Financial exposure mapping** — linking $H_{g,s}$ to the geographic location of loans, collateral, and business concentrations (via HMDA data, bank call reports, municipal finance disclosures).
3. **Balance-sheet transmission** — converting geographic hazard exposure into expected credit losses and mark-to-market repricing.

The core expected-loss equation is the standard credit-risk decomposition, but with a *scenario-contingent* PD:

$$EL_{i,s} = PD_{i,s} \times LGD_{i,s} \times EAD_i$$

$$PD_{i,s} = PD_i^0 \exp\left(\beta_1 H_{g,s} + \beta_2 T_{j,s} + \beta_3 U_g - \beta_4 A_i\right)$$

where $PD_i^0$ is the through-the-cycle baseline PD, $H_{g,s}$ is physical hazard intensity in the borrower's geography, $T_{j,s}$ is transition risk in sector $j$, $U_g$ is local economic fragility, and $A_i$ is the borrower's adaptation capacity (mitigation investment, insurance coverage). The exponential form means each risk driver multiplies the baseline default probability rather than adding to it — hazard and fragility compound, while adaptation capacity partially offsets them.

Aggregating across the book gives a **Climate-VaR**:

$$\text{Climate-VaR}_s = \sum_{i=1}^N w_i\, \Delta V_{i,s} + \lambda \sum_{i=1}^N EL_{i,s}$$

combining mark-to-market repricing $\Delta V_{i,s}$ (e.g., collateral devaluation) with credit-loss impairment, where $\lambda$ converts the credit-loss term into a capital-equivalent unit. The paper defines four stress scenarios — **orderly transition** (gradual policy tightening), **disorderly transition** (abrupt regulation), **physical risk shock** (wildfire/flood/drought event cluster), and a **compound scenario** (physical shock plus tighter financing conditions) — but does not calibrate $\beta_1,\dots,\beta_4$ or $\lambda$ numerically; the paper is explicit that it presents a methodological framework, with numeric stress outputs left for future empirical work.

### (c) Climate-aware copula for sovereign rating migration (Palaisti)

The starting problem is statistical: sovereign rating actions (upgrades/downgrades) are recorded as discrete annual *counts*, which standard continuous copulas cannot model directly. Palaisti's **mixed-difference transformation** maps a discrete count process into a continuous uniform margin via a jittered probability integral transform:

$$U_t = F_D(A_t^-; \vartheta) + V_t\, p_\vartheta(A_t), \qquad t = 1,\dots,T$$

where $A_t$ is the observed count, $F_D(\cdot;\vartheta)$ is the discrete CDF, $p_\vartheta(\cdot)$ its mass function, and $V_t \sim \text{Unif}(0,1)$ i.i.d. auxiliary noise — this makes $\{U_t\}$ marginally uniform on $(0,1)$ while preserving the ordering of migration intensity, so a standard copula can be applied to it.

The dependence process starts from a **MAG(1)** (moving-aggregate) copula:

$$U_t = (h_\theta)^{-1}(W_t, W_{t-1}), \qquad t \in \mathbb{Z}$$

for i.i.d. uniform innovations $\{W_t\}$ and copula $h$-function (conditional distribution) $h_\theta$ with dependence parameter $\theta$. This is extended to **MAGMAR(1,1)**, adding a first-order autoregressive copula layer on top:

$$U_t = (h_\varphi)^{-1}\big((h_\theta)^{-1}(W_t, W_{t-1}),\, U_{t-1}\big), \qquad t \in \mathbb{Z}$$

with full parameter vector $\eta = (\varphi', \theta')' \in \Theta_\varphi \times \Theta_\theta$. The paper establishes consistency and asymptotic normality of the maximum-likelihood estimators of $\eta$.

Climate enters through **two separate channels**, and the paper's central methodological finding is that these two channels do *not* behave the same way:

- **Marginal models:** country-level production-based carbon intensity $C_t$ and its lag $C_{t-1}$ enter as regressors in a Poisson GLM for downgrade intensity — this materially improves the marginal fit.
- **Dependence structure:** in the climate-dependent MAGMAR(1,1), the AR copula parameter is allowed to vary with climate exposure via a bounded transform: $\rho_t = \tanh(\beta_0 + \beta_1 C_{t-1})$, keeping $\rho_t \in (-1,1)$ while letting carbon intensity modulate autoregressive dependence. The MAG component $\theta$ is left homogeneous (time-invariant).

The **Gumbel** copula (parameter $\alpha \geq 1$, asymmetric upper-tail dependence) fits the data far better than Gaussian or Student-$t$ alternatives — Gumbel MAGMAR(1,1) achieves log-likelihood $\approx 5{,}035$ / AIC $\approx -10{,}066$, versus $586$ / $-1{,}171$ for Gumbel MAG(1), $\approx 33$ for a $t$-copula MAGMAR, and $4{,}663$ / $-9{,}324$ for a Markov-copula Gumbel benchmark; a Poisson GLM with climate covariates but no copula dependence structure performs "substantially worse" (log-likelihood $-419$). Gumbel wins because global sovereign rating activity shows pronounced *asymmetric upper-tail clustering* — many sovereigns downgraded together in a small number of high-activity years — which symmetric dependence structures (Gaussian, $t$) cannot represent. But once the extra parameters of the climate-dependent MAGMAR are AIC/BIC-penalized, **climate covariates do not materially improve the dependence fit** over the homogeneous model — the paper's stated conclusion is "limited incremental explanatory power" for the chosen aggregate climate proxy.

## Walkthrough

*This walkthrough uses Panda & Saha's PD/EL/Climate-VaR equations exactly as specified in the paper. Because the paper leaves $\beta_1,\dots,\beta_4$, $\lambda$, and all portfolio-level dollar figures uncalibrated, every numeric input below is illustrative — chosen to be plausible, not taken from the paper.*

**Setup.** A community bank holds a $120M real-estate-secured commercial loan book concentrated in a single California county rated "Very High" on the CAL FIRE Fire Hazard Severity Zone map. Baseline (through-the-cycle) PD for this segment is $PD^0 = 1.5\%$, loss-given-default $LGD = 40\%$, exposure at default $EAD = \$120\text{M}$.

**Baseline expected loss (no climate stress):**

$$EL_{\text{baseline}} = PD^0 \times LGD \times EAD = 0.015 \times 0.40 \times \$120\text{M} = \$720{,}000$$

**Scenario 1 — Physical Risk Shock.** Illustrative hazard/fragility inputs: $H_{g,s} = 1.0$ (normalized peak wildfire severity), $T_{j,s} = 0.2$ (mild transition pressure in a pure physical shock), $U_g = 0.3$ (rural, single-industry county), $A_i = 0.2$ (limited defensible-space mitigation / insurance coverage). Illustrative sensitivities $\beta_1 = 0.9$, $\beta_2 = 0.4$, $\beta_3 = 0.3$, $\beta_4 = 0.5$:

$$\text{exponent} = 0.9(1.0) + 0.4(0.2) + 0.3(0.3) - 0.5(0.2) = 0.90 + 0.08 + 0.09 - 0.10 = 0.97$$

$$PD_{i,s} = 1.5\% \times e^{0.97} \approx 1.5\% \times 2.638 \approx 3.96\%$$

$$EL_{i,s} = 0.0396 \times 0.40 \times \$120\text{M} \approx \$1{,}900{,}000$$

Expected credit loss on this segment roughly **2.6×** under the physical-shock scenario — driven entirely by the multiplicative structure of $PD_{i,s}$, holding $LGD$ and $EAD$ fixed for simplicity.

**Scenario 2 — Compound Scenario** (physical shock plus tighter financing, i.e., $T_{j,s}$ rises to $0.6$, all else equal):

$$\text{exponent} = 0.9(1.0) + 0.4(0.6) + 0.3(0.3) - 0.5(0.2) = 0.90 + 0.24 + 0.09 - 0.10 = 1.13$$

$$PD_{i,s} = 1.5\% \times e^{1.13} \approx 1.5\% \times 3.096 \approx 4.64\% \implies EL_{i,s} \approx \$2{,}227{,}000$$

**Climate-VaR.** Suppose the physical-shock scenario also triggers an illustrative $3\text{M} collateral markdown ($\Delta V_{i,s}$, from reduced liquidity in wildfire-exposed property markets), with $w_i = 1$ (single segment) and $\lambda = 1$:

$$\text{Climate-VaR}_s = \$3.0\text{M} + 1 \times \$1.9\text{M} = \$4.9\text{M}$$

against a baseline credit-only exposure of $\$720\text{K}$ — roughly a **6.8×** increase in the capital-equivalent climate risk attributable to this single concentrated county, illustrating exactly the failure mode the geospatial framework is built to surface: a loan book that looks adequately diversified by sector or borrower count can be severely concentrated by geography.

## Analysis

**What each paper actually covers.** Azzone, Bechi & Sbaiz address pure **physical** risk (temperature anomalies) in the context of long-only equity **portfolio construction**. Panda & Saha address both physical (wildfire/drought/flood/heat) and transition (policy/regulatory) risk in the context of **bank credit-portfolio stress testing**, but the framework is presented without empirical calibration. Palaisti addresses **sovereign credit rating migration**, using carbon intensity as a climate covariate that is more naturally read as a transition-risk exposure proxy (higher-carbon-intensity sovereigns face more repricing risk under decarbonization), tested through a **dependence-modeling** (copula) lens rather than a portfolio- or loan-level lens.

**How this differs methodologically from classical risk modeling:**

1. **Different underlying statistics.** Azzone et al. model temperature anomalies as time-varying Bernoulli events ($B_{k,t}$ with probability $p_{k,t}$) rather than continuous Gaussian shocks — climate hazard indicators are closer to a point-process/extreme-event framework than to the return-distribution framework that underlies [[Correlation and Covariance Estimation]].
2. **Spatially, not sectorally, clustered dependence.** Panda & Saha's hazard intensity $H_{g,s}$ is inherently geographically correlated — adjacent counties share wildfire and drought exposure regardless of the sectors operating there — and compound scenarios (physical shock *plus* financing stress) create a form of tail dependence that a sector/factor covariance matrix has no mechanism to represent.
3. **Asymmetric tail dependence, not just crisis correlation spikes.** [[Stress Testing]] already documents that financial correlations surge toward 1 in a crisis. Palaisti's result is sharper: sovereign rating-downgrade clustering is *structurally* asymmetric (Gumbel massively outperforms symmetric Gaussian/$t$ copulas even outside crisis conditioning), suggesting climate-relevant dependence in credit migration is not simply "normal correlation, but bigger during stress" — it is a different functional shape entirely.
4. **Acute data scarcity for validation.** Palaisti's own finding — that climate covariates help the marginal downgrade models but add little to the *dependence* fit once penalized for extra parameters — is most plausibly a data problem: there have not yet been enough climate-driven, multi-sovereign downgrade clusters in the historical record to separately identify a climate effect on dependence from the baseline copula structure. Panda & Saha's framework has the same issue in a different form: it specifies the *functional form* of scenario-contingent PD but explicitly leaves the coefficients uncalibrated, "awaiting empirical estimation."

**What remains genuinely unresolved.** This is a comparatively young and unstandardized corner of quant risk relative to classical VaR or credit-risk modeling. VaR and stress testing (see [[Stress Testing]]) can validate against a multi-decade catalogue of well-documented financial crises (1987, 1997/98, 2000-02, 2008, 2020); climate risk models cannot — there is no comparable multi-decade record of realized, climate-attributed multi-institution financial losses to backtest against. Regulatory climate-scenario design (in the spirit of NGFS-style scenarios) is itself still maturing. Parameter instability is a real concern: any $\beta$ coefficients calibrated on a short and geographically limited hazard-event history are unlikely to generalize to future, potentially more severe, climate states — precisely the long-horizon transition-risk scenario design problem that makes this harder than backward-looking financial stress testing.

## Implementation

```python
"""
Simplified sketch of a geospatial climate stress test, following the
structure of Panda & Saha (2026) — NOT the paper's actual (uncalibrated)
implementation. Coefficients and dollar amounts below are illustrative.
"""

import numpy as np
import pandas as pd

# ── 1. Loan book with geographic (region) tags ──────────────────────────────
loans = pd.DataFrame([
    {"loan_id": "L001", "region": "county_A_high_wildfire", "ead": 45_000_000, "pd0": 0.012, "lgd": 0.40, "sector": "real_estate", "adapt_capacity": 0.2},
    {"loan_id": "L002", "region": "county_A_high_wildfire", "ead": 30_000_000, "pd0": 0.018, "lgd": 0.45, "sector": "agriculture",  "adapt_capacity": 0.1},
    {"loan_id": "L003", "region": "county_B_low_hazard",    "ead": 60_000_000, "pd0": 0.010, "lgd": 0.35, "sector": "real_estate", "adapt_capacity": 0.6},
    {"loan_id": "L004", "region": "county_C_flood_zone",    "ead": 25_000_000, "pd0": 0.015, "lgd": 0.50, "sector": "agriculture",  "adapt_capacity": 0.3},
])

# ── 2. Hazard severity map, per region, per scenario (H_{g,s}) ─────────────
# Normalized 0 (no hazard) to 1 (peak severity), e.g. from a CAL-FIRE-style
# hazard severity layer or a flood-probability map.
hazard_map = {
    "physical_shock":  {"county_A_high_wildfire": 1.00, "county_B_low_hazard": 0.15, "county_C_flood_zone": 0.80},
    "compound":        {"county_A_high_wildfire": 1.00, "county_B_low_hazard": 0.15, "county_C_flood_zone": 0.80},
    "orderly_transition":   {"county_A_high_wildfire": 0.10, "county_B_low_hazard": 0.05, "county_C_flood_zone": 0.10},
}

# Transition risk by sector, per scenario (T_{j,s})
transition_map = {
    "physical_shock":     {"real_estate": 0.20, "agriculture": 0.20},
    "compound":           {"real_estate": 0.60, "agriculture": 0.60},
    "orderly_transition": {"real_estate": 0.50, "agriculture": 0.35},
}

# Local economic fragility by region (U_g) — static per region for simplicity
fragility_map = {"county_A_high_wildfire": 0.30, "county_B_low_hazard": 0.10, "county_C_flood_zone": 0.25}

# Illustrative sensitivity coefficients (beta_1..beta_4) — NOT from the paper
BETA_HAZARD, BETA_TRANSITION, BETA_FRAGILITY, BETA_ADAPT = 0.9, 0.4, 0.3, 0.5


def scenario_pd(row: pd.Series, scenario: str) -> float:
    """PD_{i,s} = PD_i^0 * exp(b1*H + b2*T + b3*U - b4*A)"""
    H = hazard_map[scenario][row["region"]]
    T = transition_map[scenario][row["sector"]]
    U = fragility_map[row["region"]]
    A = row["adapt_capacity"]
    exponent = BETA_HAZARD * H + BETA_TRANSITION * T + BETA_FRAGILITY * U - BETA_ADAPT * A
    return row["pd0"] * np.exp(exponent)


def run_climate_stress_test(loans: pd.DataFrame, scenarios: list[str]) -> pd.DataFrame:
    results = []
    for scenario in scenarios:
        stressed = loans.copy()
        stressed["pd_stress"] = stressed.apply(lambda r: scenario_pd(r, scenario), axis=1)
        stressed["el_stress"] = stressed["pd_stress"] * stressed["lgd"] * stressed["ead"]
        stressed["el_baseline"] = stressed["pd0"] * stressed["lgd"] * stressed["ead"]
        results.append({
            "scenario": scenario,
            "total_ead": stressed["ead"].sum(),
            "el_baseline": stressed["el_baseline"].sum(),
            "el_stress": stressed["el_stress"].sum(),
            "el_multiplier": stressed["el_stress"].sum() / stressed["el_baseline"].sum(),
        })
    return pd.DataFrame(results).set_index("scenario")


def climate_var(el_stress_total: float, mtm_repricing: float, lam: float = 1.0) -> float:
    """Climate-VaR_s = sum(w_i * dV_i,s) + lambda * sum(EL_i,s), aggregated form."""
    return mtm_repricing + lam * el_stress_total


results = run_climate_stress_test(loans, ["orderly_transition", "physical_shock", "compound"])
print(results.to_string(formatters={
    "total_ead":   lambda x: f"${x:,.0f}",
    "el_baseline": lambda x: f"${x:,.0f}",
    "el_stress":   lambda x: f"${x:,.0f}",
    "el_multiplier": lambda x: f"{x:.2f}x",
}))

# Illustrative collateral markdown under the physical shock (dollar amount,
# not derived from the model — represents a separate valuation input)
mtm_shock = 3_000_000
el_shock = results.loc["physical_shock", "el_stress"]
print(f"\nClimate-VaR (physical_shock): ${climate_var(el_shock, mtm_shock):,.0f}")
```

This sketch keeps the paper's structural insight — that hazard, transition risk, local fragility, and adaptation capacity multiply a baseline PD, and that geography (not sector) is the primary axis of aggregation — while making no claim to reproduce Panda & Saha's (unpublished/uncalibrated) actual coefficients.

## Bridge to Quant / ML

**Extending [[Correlation and Covariance Estimation]].** Palaisti's climate-aware MAGMAR copula is structurally the same move as Ledoit-Wolf shrinkage or factor-model covariance decomposition: take a dependence estimator that is too unstructured (sample covariance / static Gaussian copula) and impose additional structure — here, a time-varying AR parameter $\rho_t = \tanh(\beta_0 + \beta_1 C_{t-1})$ driven by an external covariate, plus an asymmetric-tail (Gumbel) copula family instead of the symmetric Gaussian default. The empirical lesson generalizes: the correct *family* of dependence structure (symmetric vs. asymmetric tail) can matter more than which covariates you feed it.

**Extending [[Stress Testing]].** Panda & Saha's four scenarios (orderly transition, disorderly transition, physical risk shock, compound) are a climate-specific instance of the historical/hypothetical scenario tables in [[Stress Testing]] — the same forward-scenario logic (shock a portfolio's current exposures, read off P&L or expected loss), but with scenarios anchored in physical hazard maps and policy pathways rather than replayed market crises. The Climate-VaR construction is a direct scenario-based analogue of standard VaR, substituting $PD \times LGD \times EAD$ credit-loss components and mark-to-market repricing for a return-distribution quantile.

**ML angle.** All three papers depend on non-traditional geospatial and text/count data — temperature-anomaly series, CAL FIRE hazard severity layers, NOAA climate records, property assessor and HMDA records, sovereign carbon-intensity panels. This is the same category of problem as [[Alternative Data]]: point-in-time alignment (was a hazard-severity layer or carbon-intensity estimate actually available at decision time, or backfilled/revised later?), coverage gaps (hazard maps are far more granular for some counties/countries than others), and the need to fuse heterogeneous geospatial, tabular, and count data into model-ready features. Satellite and remote-sensing hazard layers are a specific instance of the "satellite/geospatial" alternative-data category, applied here to risk measurement rather than alpha generation.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Define physical risk and transition risk in climate finance. Which of the three grounding papers addresses each, and which addresses both?
<details><summary>Answer</summary>Physical risk is the direct financial impact of climate hazards — extreme temperature, wildfire, drought, flood, heat stress — damaging assets, disrupting operations, or raising default probabilities. Transition risk is the financial impact of the *policy and technology response* to climate change — carbon pricing, regulation, stranded assets, market repricing of high-carbon exposures — independent of whether any physical damage occurs. Azzone, Bechi & Sbaiz address pure physical risk (temperature anomalies affecting equity sector returns). Palaisti's covariate (carbon intensity) is a transition-risk proxy, applied to sovereign credit migration. Panda & Saha explicitly model both: their PD equation includes separate hazard intensity ($H_{g,s}$, physical) and transition risk ($T_{j,s}$) terms, and their four scenarios include both "orderly/disorderly transition" and "physical risk shock" cases.</details>

**Q2.** Why can't a standard Gaussian copula capture what Palaisti's empirical results show about sovereign rating migration, and what does the Gumbel MAGMAR(1,1) specification add that a Gaussian copula cannot?
<details><summary>Answer</summary>Global sovereign rating activity shows pronounced *asymmetric upper-tail clustering* — many sovereigns get downgraded together in a small number of high-activity years, but this clustering does not show a symmetric mirror image on the upgrade side. A Gaussian copula has symmetric tail dependence (in fact, zero asymptotic tail dependence), so it structurally cannot represent "extreme joint downgrade years are much more likely than the correlation coefficient alone would predict." The Gumbel copula has non-zero upper-tail dependence by construction — it directly encodes the probability that many countries have high downgrade activity simultaneously. Empirically, Gumbel MAGMAR(1,1) achieved log-likelihood ≈5,035 versus far lower values for Gaussian/t-copula alternatives, confirming the asymmetric-tail structure is what the data actually exhibit.</details>

**Q3.** In Panda & Saha's PD equation, $PD_{i,s} = PD_i^0 \exp(\beta_1 H_{g,s} + \beta_2 T_{j,s} + \beta_3 U_g - \beta_4 A_i)$, explain why adaptation capacity $A_i$ enters with a negative sign while the other three terms are positive.
<details><summary>Answer</summary>Hazard intensity ($H$), transition risk ($T$), and local economic fragility ($U$) are all risk-*increasing* — higher wildfire exposure, tighter regulation, or a more fragile local economy should raise the probability of default relative to the baseline. Adaptation capacity ($A$) is risk-*mitigating* — a borrower with defensible-space investment, flood-proofing, insurance coverage, or diversified income sources is better able to absorb a climate shock without defaulting. Because $PD_{i,s}$ is multiplicative (exponential of a linear combination), a positive $A_i$ with a negative coefficient $-\beta_4 A_i$ pulls the exponent down, partially offsetting the hazard and transition terms — modeling adaptation as a genuine risk offset rather than treating all borrowers in a hazard zone as equally exposed.</details>

---

### Level 2 — Quantitative

**Q4.** Using $PD_{i,s} = PD_i^0 \exp(\beta_1 H_{g,s} + \beta_2 T_{j,s} + \beta_3 U_g - \beta_4 A_i)$ with $PD_i^0 = 2.0\%$, $\beta_1=0.9$, $\beta_2=0.4$, $\beta_3=0.3$, $\beta_4=0.5$, $H_{g,s}=0.7$, $T_{j,s}=0.3$, $U_g=0.4$, $A_i=0.5$, $LGD=45\%$, $EAD=\$80\text{M}$: compute the stressed expected loss and compare it to the baseline expected loss.
<details><summary>Answer</summary>

Exponent: $0.9(0.7) + 0.4(0.3) + 0.3(0.4) - 0.5(0.5) = 0.63 + 0.12 + 0.12 - 0.25 = 0.62$

$PD_{i,s} = 2.0\% \times e^{0.62} \approx 2.0\% \times 1.859 \approx 3.72\%$

$EL_{\text{stress}} = 0.0372 \times 0.45 \times \$80\text{M} \approx \$1{,}338{,}000$

$EL_{\text{baseline}} = 0.020 \times 0.45 \times \$80\text{M} = \$720{,}000$

Multiplier: $1{,}338{,}000 / 720{,}000 \approx \mathbf{1.86\times}$ — the exponential PD adjustment nearly doubles expected credit loss on this segment under the stress scenario, driven mainly by hazard intensity and local fragility outweighing this borrower's above-average adaptation capacity.</details>

**Q5.** Using Azzone, Bechi & Sbaiz's CEV formula, $\text{CEV}(\mathbf{w},t) = \sum_k \alpha_k(\mathbf{w})^2 p_{k,t}(1-p_{k,t}) + 2\sum_{k<j}\alpha_k(\mathbf{w})\alpha_j(\mathbf{w})\,\text{Cov}(B_{k,t},B_{j,t})$, compute CEV for a two-region portfolio with $\alpha_1 = 0.6$, $\alpha_2 = 0.4$, $p_{1,t} = 0.20$, $p_{2,t} = 0.10$, and $\text{Cov}(B_{1,t}, B_{2,t}) = 0.03$.
<details><summary>Answer</summary>

Idiosyncratic term: $\alpha_1^2 p_1(1-p_1) + \alpha_2^2 p_2(1-p_2) = (0.6)^2(0.20)(0.80) + (0.4)^2(0.10)(0.90)$

$= 0.36 \times 0.16 + 0.16 \times 0.09 = 0.0576 + 0.0144 = 0.0720$

Systemic term: $2\,\alpha_1\alpha_2\,\text{Cov}(B_1,B_2) = 2(0.6)(0.4)(0.03) = 0.0144$

$\text{CEV} = 0.0720 + 0.0144 = \mathbf{0.0864}$

Roughly 17% of the total CEV comes from the cross-region covariance term — a portfolio that looks diversified by weight alone (0.6/0.4 split) still carries meaningful systemic climate-exposure volatility if the two regions' extreme-event probabilities are positively correlated.</details>

---

### Level 3 — Coding

**Q6.** In the `Implementation` code above, `scenario_pd` looks up hazard, transition, and fragility values from dictionaries keyed by region and sector. What happens if a new loan is added whose `region` is not a key in `hazard_map[scenario]`, and how would you make the function fail safely (or explicitly) rather than silently?
<details><summary>Answer</summary>As written, `hazard_map[scenario][row["region"]]` raises a `KeyError` if the region is missing from the hazard map for that scenario — this is actually the safer failure mode (loud and immediate) compared to, say, `.get(region, 0.0)`, which would silently treat an unmapped region as zero hazard and understate its stressed PD. In a production geospatial stress-testing pipeline this matters a lot: a bank's loan book will routinely include regions not yet covered by the hazard-severity data vendor, and defaulting missing regions to "no hazard" would systematically understate portfolio-level Climate-VaR exactly for the geographies the data pipeline has failed to cover. The correct fix is to validate coverage explicitly — e.g., assert that `set(loans["region"]) <= set(hazard_map[scenario].keys())` before running the stress test, and raise a descriptive error (or flag the loan as "hazard data unavailable") rather than either crashing uninformatively or silently zero-filling.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Climate risk in quant finance means ESG scoring and exclusionary screening | ESG scores and divestment are informal, backward-looking heuristics with no explicit risk-propagation mechanism. The frameworks here are rigorous statistical/econometric models — panel regressions linking temperature anomalies to returns, PD equations driven by hazard maps, and copulas modeling joint rating-migration dependence — that quantify *how* climate exposure changes prices, losses, or default correlations. |
| Physical risk and transition risk are the same thing, or interchangeable | Physical risk (direct damage from weather/climate events) and transition risk (repricing from policy/technology shifts) have different transmission channels, different time horizons, and can point in different directions for the same asset — e.g., a fossil-fuel property could face low physical risk but high transition risk, or vice versa. Panda & Saha model them as separate terms in the PD equation precisely because they don't move together. |
| Climate-aware copulas / stress tests are just standard models with a "climate factor" bolted on | Palaisti's central finding is the opposite of "bolt-on works": adding a climate covariate to the *marginal* models helps, but the same covariate adds little to the *dependence* structure once properly penalized — showing that naively treating climate as an extra macro factor in a standard model understates how differently climate-driven dependence actually behaves (asymmetric tail clustering, not a linear factor loading). |
| These frameworks are production-ready with validated parameters | Panda & Saha's stress-testing equations are presented with unestimated coefficients "awaiting empirical estimation" — no calibrated numeric loss outputs are reported. This is a young field without the multi-decade backtesting record that anchors classical VaR and credit-risk models. |

## Related Concepts

- [[Stress Testing]] — climate stress testing is a specific scenario-design discipline within this general framework; Panda & Saha's four scenarios are climate-specific analogues of the historical/hypothetical scenario tables used in classical stress testing
- [[Correlation and Covariance Estimation]] — climate-aware copulas are a structural extension of dependence modeling, conceptually parallel to how shrinkage and factor decomposition extend the sample covariance matrix
- [[Alternative Data]] — geospatial hazard layers, satellite imagery, and property/loan geolocation data feeding climate risk models are a specialized category of alternative data with the same point-in-time and coverage challenges
- [[Factor Models]] — the naive baseline this literature moves beyond: treating climate as just another macro factor, which the panel-regression evidence on sector-specific, time-varying temperature sensitivity suggests understates the risk
- [[Value at Risk]] — Climate-VaR is a scenario-based, credit-loss-driven analogue of standard parametric VaR rather than a return-distribution quantile

## Sources Used

- Azzone, M., Bechi, C., & Sbaiz, G. (2026). *Temperature Anomalies and Climate Physical Risk in Portfolio Construction*. arXiv:2604.11143v1 [q-fin.PM, q-fin.RM]
- Panda, S. N., & Saha, A. (2026). *Climate Risk Stress Testing in California: A Geospatial Framework for Banking and Climate-Exposed Sectors*. arXiv:2604.16716v1 [cs.CE, q-fin.RM]
- Palaisti, M. (2026). *Climate-Aware Copula Models for Sovereign Rating Migration Risk*. arXiv:2604.07567v1 [stat.ME, math.PR, q-fin.RM, q-fin.ST]

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-07-30 | Full content written | Content gap remediation — climate risk coverage |
