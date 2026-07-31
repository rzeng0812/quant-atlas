---
type: concept
domain: 30-Models
tags: [risk, regulatory, portfolio]
status: math
stability: stable
confidence: high
last_reviewed: 2026-07-30
review_interval_days: 365
sources:
  - "Peysakhovich & Sieradzki, How to Spot Outliers: an Ensemble Anomaly Detection Framework (arXiv:2606.20079v1)"
  - "Vadrevu, A Hybrid Gaussian Process Regression Framework for Stable Volatility-Covariance Estimation (arXiv:2605.17275v1)"
  - "Basel Committee on Banking Supervision — Basel III: Finalising post-crisis reforms (2017)"
  - "BCBS — Minimum capital requirements for market risk (FRTB, 2019)"
created: 2026-07-30
---

> [!info] Problem Chain
> **Chain:** Risk Management → Gap: How much loss-absorbing capital must a bank hold against its trading and lending risks, and how is that requirement enforced and verified?
> **This concept:** Basel capital ratios convert a bank's risk-weighted asset base into a minimum capital requirement, with FRTB defining exactly how market risk itself must be measured for that purpose, and CCAR/DFAST providing an independent scenario-based check.
> **Alternative approaches to this gap:** none — this is the mandated regulatory framework, not one design choice among several
> **You need first:** [[Value at Risk]], [[Expected Shortfall]], [[Stress Testing]]
> **This unlocks:** model risk management, internal model approval, capital optimization strategies

## Why This Exists

**The gap:** Going into 2008, banks looked well-capitalized by their own metrics — regulatory capital ratios were comfortably above the required minimums at nearly every major institution that later failed or required a bailout. The crisis revealed that both the *capital levels* and the *risk models used to compute them* had badly underestimated tail risk, correlation breakdown, and the degree to which banks were interconnected through the same trades, the same collateral chains, and the same funding markets. A bank could be "compliant" on paper and still be one bad quarter from insolvency.

**What came before:** Basel I (1988) used simple, coarse risk weights — a fixed percentage per asset class (0% for sovereigns, 100% for corporate loans) with no sensitivity to how risky a specific exposure actually was. Basel II (2004) refined this with internal-ratings-based credit models and introduced a market-risk capital charge computed from [[Value at Risk]]: a 10-day 99% VaR, multiplied by a regulatory scalar (typically 3, higher if backtesting was poor), converted into a capital number. Basel 2.5 (2009, the post-Lehman patch) added a "stressed VaR" add-on computed over a historical stress window, in a rush to shore up the framework before the full Basel III overhaul was ready.

**What this adds:** Basel III raises both the *quantity* and the *quality* of required capital, centering the framework on CET1 (Common Equity Tier 1) — the highest-loss-absorbing form of capital — rather than looser Tier 1/Tier 2 instruments that had proven to absorb losses poorly in 2008. It also adds a leverage ratio: a simple, non-risk-weighted backstop that catches cases where risk-weighting itself is wrong or gamed. Layered on top, the Fundamental Review of the Trading Book (FRTB) replaced VaR with [[Expected Shortfall]] as the basis for market-risk capital, because ES captures tail severity in a way VaR structurally cannot. And in the US, CCAR/DFAST stress testing adds a yearly, regulator-run check that does not depend on trusting any individual bank's internal model at all.

**What it still doesn't solve:** The capital ratios and the FRTB market-risk charge are only as good as the models that compute their inputs — RWA, VaR, ES — and those models are built, run, and maintained by the same banks being regulated. This creates an unavoidable validation problem: a bank's internal model can be wrong, stale, or silently broken (a data feed freezing, a valuation engine misconfigured) while still producing numbers that look plausible and get reported to regulators as if correct. Model risk management — the discipline of independently validating and continuously monitoring these internal models — is exactly the gap the anomaly-detection research discussed in [[#Analysis]] below is aimed at closing.

Think of Basel capital ratios like a building code that mandates a minimum foundation depth relative to the building's weight. That's the CET1 ratio: capital (foundation) scaled to risk-weighted assets (building weight). The leverage ratio is a second, cruder check — a flat minimum foundation depth regardless of how the engineer classified the building's weight — because if the weight estimate itself turns out to be wrong, you still want a floor. FRTB is the building code's own definition of *how* to estimate wind and seismic loads (VaR vs. ES is a difference in how conservatively you estimate a "worst case" load). CCAR/DFAST is the independent structural inspector who runs their own stress calculation using the building's blueprints, without trusting the developer's self-reported load calculations at all.

## Math Concepts

**1. The core capital ratio.**

Basel III's central solvency metric is the CET1 ratio:

$$\boxed{\text{CET1 Ratio} = \frac{\text{CET1 Capital}}{\text{RWA}} \geq 4.5\%}$$

**CET1 capital** is common stock plus retained earnings, minus regulatory deductions (goodwill, deferred tax assets, minority interests beyond a threshold) — the capital that absorbs losses first and cannot contractually be avoided, unlike debt-like hybrid instruments.

**RWA (risk-weighted assets)** is the risk-adjusted size of the balance sheet used as the ratio's denominator:

$$\text{RWA} = \text{RWA}_{\text{credit}} + \text{RWA}_{\text{market}} + \text{RWA}_{\text{operational}}$$

- **Credit risk RWA**: $\text{RWA}_{\text{credit}} = \sum_i w_i \cdot E_i$, where $E_i$ is exposure $i$ and $w_i$ is a risk weight (0% for high-grade sovereigns, 20–150% for banks and corporates under the standardized approach, or model-derived under the internal ratings-based, IRB, approach).
- **Market risk RWA**: $\text{RWA}_{\text{market}} = 12.5 \times K_{\text{market}}$, where $K_{\text{market}}$ is the market-risk capital charge (in dollars) and $12.5 = 1/8\%$ converts a capital charge into an RWA-equivalent so it sits in the same denominator as credit RWA. This is exactly where FRTB plugs in: FRTB defines how $K_{\text{market}}$ is computed.
- **Operational risk RWA**: covers losses from failed processes, fraud, and systems — under Basel III's Standardized Measurement Approach, a function of gross income and a firm-specific loss history multiplier.

**Buffers stacked on the 4.5% minimum.** The bare 4.5% CET1 minimum is not the number that matters in practice. Basel III adds:

| Buffer | Size | Purpose |
|---|---|---|
| Capital Conservation Buffer (CCB) | 2.5% of RWA, in CET1 | Built up in good times; breaching it doesn't trigger default, but automatically restricts dividends, buybacks, and discretionary bonus payouts on a sliding scale |
| Countercyclical Buffer (CCyB) | 0–2.5%, set by national regulators | Raised when aggregate credit growth looks excessive, to force capital build-up ahead of a downturn; released in a crisis to free up lending capacity |
| G-SIB surcharge | 1–3.5% additional | Extra capital for globally systemic banks, sized to their systemic footprint (size, interconnectedness, complexity) |

A large systemic bank's *effective* minimum CET1 ratio is therefore often 9–12%, not 4.5% — the headline minimum is a floor beneath a floor. Tier 1 ratio (CET1 + Additional Tier 1) must be $\geq 6\%$ plus the same buffers; Total Capital ratio (Tier 1 + Tier 2) must be $\geq 8\%$ plus buffers.

**2. The leverage ratio — a non-risk-weighted backstop.**

$$\text{Leverage Ratio} = \frac{\text{Tier 1 Capital}}{\text{Total Exposure}} \geq 3\%$$

**Total exposure** is on-balance-sheet assets plus certain off-balance-sheet items (derivatives exposure, securities financing transactions, loan commitments), counted at face value — no risk weighting at all. Every dollar of exposure counts the same whether it is a T-bill or a leveraged loan.

Why keep a crude, unweighted ratio alongside the carefully risk-weighted CET1 ratio? Because RWA is a *modeled* quantity, and models can be wrong in ways that are hard to detect from outside — pre-2008, AAA-rated mortgage-backed securities were assigned very low risk weights that proved catastrophically mistaken. The leverage ratio is a floor that does not depend on the risk-weighting being correct at all; it catches balance-sheet growth that risk models happen to classify as "safe."

This is not a purely theoretical concern — it has direct pricing consequences in markets today. For globally systemic banks, the enhanced supplementary leverage ratio (eSLR) raises the minimum to 5% (a 2% surcharge above the 3% base). As [[FX Spot and Forwards]] documents, the supplementary leverage ratio penalizes *gross* balance-sheet size regardless of how well a position is economically hedged — a matched borrow/lend/swap trade that carries near-zero net risk still consumes leverage-ratio capacity because the legs don't net for SLR purposes. This is the mechanism behind the persistent post-2008 cross-currency basis: banks demand a spread to intermediate low-risk, balance-sheet-intensive trades because the leverage ratio, not the risk-weighted ratio, is often the binding constraint. A bank can look comfortably capitalized on a risk-weighted basis and still be leverage-ratio-constrained.

**3. FRTB: from 10-day 99% VaR to 97.5% Expected Shortfall.**

Basel 2.5's market-risk capital charge was proportional to $\text{VaR}_{99\%,\,10\text{-day}}$ (plus a stressed-VaR add-on). FRTB (finalized 2019, phased in through the 2020s) replaces this with a charge proportional to $\text{ES}_{97.5\%}$, computed not over a single uniform 10-day window but over **liquidity horizons** specific to each risk factor — 10, 20, 40, 60, or 120 days depending on how quickly that risk factor can realistically be hedged or unwound. Equity indices get short liquidity horizons; structured credit and less liquid instruments get long ones. This directly addresses a lesson from 2008: Basel II's flat 10-day assumption implicitly assumed everything could be liquidated in 10 days, which was false for structured credit products that took months to unwind (or could not be unwound at all).

**Why the shift from VaR to ES matters.** [[Value at Risk]] is a quantile — the threshold below which losses stay $\alpha\%$ of the time — and by construction it says nothing about how severe losses are once that threshold is crossed. Two trading books with identical 99% VaR can have wildly different tail severity: one loses a little more than VaR on its worst days, the other loses many multiples of VaR. [[Expected Shortfall]] fixes this by averaging all losses beyond the VaR threshold, and it is a coherent risk measure (it satisfies subadditivity), which VaR is not — meaning ES cannot perversely penalize diversification the way VaR sometimes can. This is precisely the same mathematical argument used to justify Expected Shortfall (there called CVaR) as the training objective in [[Deep Hedging]]: a convex, tail-sensitive, coherent risk measure is required both for well-behaved optimization and for correctly rewarding diversification, and FRTB's regulators reached the identical conclusion for capital adequacy.

FRTB also formalizes desk-level model governance: trading desks using the Internal Models Approach (IMA) must pass ongoing backtesting and a P&L attribution test comparing the desk's risk model P&L to its actual trading P&L. A desk that fails either test loses IMA approval and is pushed onto the much more punitive Standardized Approach (SA) for capital purposes — a direct, capital-cost consequence of model risk failure, and the regulatory hook that makes model risk management commercially, not just theoretically, important.

## Walkthrough

**Setup.** A hypothetical mid-size global bank reports the following at quarter-end:

| Item | Value |
|---|---|
| CET1 capital | \$48B |
| Tier 1 capital | \$55B |
| RWA | \$480B |
| Total leverage exposure | \$1,375B |
| Applicable capital conservation buffer | 2.5% |

**Step 1 — CET1 ratio.**

$$\text{CET1 Ratio} = \frac{\$48\text{B}}{\$480\text{B}} = 10.0\%$$

Required minimum with buffer: $4.5\% + 2.5\% = 7.0\%$. The bank's 10.0% CET1 ratio clears this by 3.0 percentage points — comfortable headroom; no automatic distribution restrictions apply.

**Step 2 — Tier 1 ratio.**

$$\text{Tier 1 Ratio} = \frac{\$55\text{B}}{\$480\text{B}} = 11.46\%$$

Required minimum with buffer: $6\% + 2.5\% = 8.5\%$. Passes by nearly 3 percentage points.

**Step 3 — Leverage ratio.**

$$\text{Leverage Ratio} = \frac{\$55\text{B}}{\$1{,}375\text{B}} = 4.0\%$$

Against the standard 3% minimum, this passes comfortably. **But** if this bank is a G-SIB subject to the enhanced supplementary leverage ratio (eSLR) of 5%, it **fails**: it would need $5\% \times \$1{,}375\text{B} = \$68.75\text{B}$ of Tier 1 capital, a shortfall of $\$68.75\text{B} - \$55\text{B} = \$13.75\text{B}$.

**The point of the walkthrough:** this bank's risk-weighted ratios (CET1, Tier 1) show a well-capitalized institution with several points of headroom above regulatory minimums. Its leverage ratio, evaluated against the standard 3% minimum, also passes. Only when evaluated against the G-SIB eSLR does a binding constraint appear — and that constraint is invisible if you only look at the RWA-based ratios, because it depends entirely on gross balance-sheet size, not on how risky any individual exposure is classified as being. This is exactly the scenario described in [[FX Spot and Forwards]]: a bank in this position has every incentive to shrink low-margin, balance-sheet-intensive but economically low-risk trades (like matched-book FX swaps) to relieve the leverage constraint, even though those trades don't move its RWA-based ratios at all.

## Analysis

**Why model risk management is a first-class regulatory requirement, not an afterthought.** Every number in this note — RWA, the FRTB capital charge, VaR, ES — is the output of an internal model that the regulated bank itself builds, calibrates, and runs. Basel III and FRTB do not just specify formulas; they specify governance requirements for the models that populate those formulas, because a capital framework built on numbers a bank can silently misreport (not through fraud, but through undetected model failure) is not actually a capital framework at all. This is exactly the problem Peysakhovich & Sieradzki (arXiv:2606.20079v1) target: their Ensemble Quality Assessment Framework (EQAF) monitors risk-calculation infrastructure in real time for the kind of failures that don't look like failures — a valuation feed that freezes and repeats yesterday's number, a misconfigured model, a silent data-pipeline break. Using real credit-derivatives data from a major investment bank, they find that an ensemble of complementary outlier-detection methods achieves F1 scores of 61–79%, dramatically outperforming any single statistical method (6–66% F1), and — critically — that purely statistical detection methods systematically **fail to catch "stale-value" anomalies**, where a frozen valuation output is bit-for-bit identical to the prior day's value and therefore statistically indistinguishable from a legitimately unchanged risk number. Only domain-specific deterministic rules layered into the ensemble catch this failure mode. The authors frame this explicitly as a Basel III/FRTB model risk management problem: regulators increasingly require automated, auditable quality controls precisely because a bank's RWA and FRTB capital charge inherit whatever silent errors sit upstream in the risk-calculation pipeline. A capital ratio computed from a stale VaR feed is not conservative or wrong in a predictable direction — it is simply not trustworthy, and no amount of additional capital buffer fixes a broken measurement.

**Why CCAR/DFAST exists as a deliberately independent check.** In the US, the Comprehensive Capital Analysis and Review (CCAR) and Dodd-Frank Act Stress Testing (DFAST) regimes take a structurally different approach from the Basel ratios and FRTB: the Federal Reserve specifies the macroeconomic scenarios (a "severely adverse" scenario each year, defined by unemployment, GDP, asset price paths) and, for the largest banks, runs its own supervisory models against the bank's reported balance sheet and business mix — rather than relying on the bank's own VaR/ES engine to grade itself. This is not [[Stress Testing]] in the sense that note already covers (a bank applying its own scenario shocks to its own book using its own models); it is a regulator-run parallel calculation designed precisely so that a bank cannot pass simply by having a favorably-calibrated internal model. Vadrevu (arXiv:2605.17275v1) frames a large body of current quant-risk research around exactly this target: accurate volatility-covariance estimation for [[Value at Risk]] and [[Expected Shortfall]] "is central to regulatory capital adequacy processes such as ICAAP and CCAR." The paper's own framing of the problem is instructive for what it says about the status quo: GARCH-family and EWMA approaches "suffer from parametric rigidity, distributional assumptions, and numerical instability under stress, leading to systematic underestimation of tail risk" — which is exactly the kind of model risk that CCAR's independent scenario approach, and FRTB's IMA backtesting requirements, are designed to catch. Vadrevu's proposed Gaussian Process Regression–Historical Simulation hybrid achieves a **100% Expected Shortfall backtest pass rate at the portfolio level** across an expanding-window evaluation from 2020–2025 — a concrete example of the kind of methodological work the regulatory regime incentivizes: not a novel risk concept, but a more robust *estimator* of the exact same VaR/ES quantities this note's frameworks mandate be computed, validated, and defended.

**Keeping the three mechanisms distinct.** It is easy to conflate these, and the distinction matters:

| Mechanism | What it governs | Answers the question |
|---|---|---|
| Basel III capital ratios (CET1, Tier 1, leverage) | Capital **adequacy** — how much loss-absorbing capital relative to risk (or gross size) | "Does this bank hold enough capital, steady-state, today?" |
| FRTB | Market-risk **measurement** — how the market-risk piece of RWA/capital charge is computed | "How should market risk itself be quantified for the capital ratio's numerator inputs?" |
| CCAR/DFAST | Independent **stress verification** — regulator-run scenario testing, often with regulator's own models | "Does this bank survive a severe scenario the regulator designed and, partly, calculated itself?" |

A bank can pass its Basel capital ratios and still fail CCAR (if the supervisory stress scenario reveals capital erosion the steady-state ratios don't capture); FRTB compliance affects the market-risk RWA feeding into the capital ratios but is not itself a pass/fail capital test; and neither Basel ratios nor FRTB substitutes for CCAR's value precisely because CCAR is deliberately not dependent on the bank's own model being correct.

## Implementation

```python
from dataclasses import dataclass


@dataclass
class BankBalanceSheet:
    cet1_capital: float          # Common Equity Tier 1 capital ($)
    tier1_capital: float         # Tier 1 capital ($) — CET1 + Additional Tier 1
    rwa: float                   # Risk-weighted assets ($)
    total_leverage_exposure: float  # Total exposure for leverage ratio ($), unweighted


def capital_ratios(bank: BankBalanceSheet) -> dict:
    """Compute the core Basel III solvency ratios from a simplified balance sheet."""
    return {
        "cet1_ratio": bank.cet1_capital / bank.rwa,
        "tier1_ratio": bank.tier1_capital / bank.rwa,
        "leverage_ratio": bank.tier1_capital / bank.total_leverage_exposure,
    }


def check_basel_iii_compliance(
    bank: BankBalanceSheet,
    capital_conservation_buffer: float = 0.025,
    countercyclical_buffer: float = 0.0,
    gsib_surcharge: float = 0.0,
    is_gsib: bool = False,
) -> dict:
    """
    Check a bank's ratios against Basel III minimums plus applicable buffers.
    Returns per-ratio pass/fail plus the headroom (or shortfall) in percentage points.
    """
    ratios = capital_ratios(bank)

    total_buffer = capital_conservation_buffer + countercyclical_buffer + gsib_surcharge

    cet1_minimum = 0.045 + total_buffer
    tier1_minimum = 0.06 + total_buffer
    leverage_minimum = 0.05 if is_gsib else 0.03  # eSLR vs standard SLR

    results = {}
    for name, ratio, minimum in [
        ("cet1_ratio", ratios["cet1_ratio"], cet1_minimum),
        ("tier1_ratio", ratios["tier1_ratio"], tier1_minimum),
        ("leverage_ratio", ratios["leverage_ratio"], leverage_minimum),
    ]:
        results[name] = {
            "value": ratio,
            "minimum_required": minimum,
            "headroom_pp": (ratio - minimum) * 100,
            "pass": ratio >= minimum,
        }

    results["overall_pass"] = all(r["pass"] for r in results.values() if isinstance(r, dict))
    return results


if __name__ == "__main__":
    bank = BankBalanceSheet(
        cet1_capital=48e9,
        tier1_capital=55e9,
        rwa=480e9,
        total_leverage_exposure=1_375e9,
    )

    print("Standard (non-G-SIB) evaluation:")
    for name, result in check_basel_iii_compliance(bank).items():
        if isinstance(result, dict):
            print(
                f"  {name:16s}: {result['value']:.2%}  "
                f"(min {result['minimum_required']:.2%}, "
                f"headroom {result['headroom_pp']:+.2f}pp, "
                f"{'PASS' if result['pass'] else 'FAIL'})"
            )

    print("\nG-SIB evaluation (5% eSLR applies):")
    for name, result in check_basel_iii_compliance(bank, is_gsib=True).items():
        if isinstance(result, dict):
            print(
                f"  {name:16s}: {result['value']:.2%}  "
                f"(min {result['minimum_required']:.2%}, "
                f"headroom {result['headroom_pp']:+.2f}pp, "
                f"{'PASS' if result['pass'] else 'FAIL'})"
            )
```

Output confirms the walkthrough: the CET1 and Tier 1 ratios pass with several points of headroom in both evaluations, the leverage ratio passes the standard 3% minimum, but flips to a **shortfall** once the 5% eSLR is applied — reproducing the exact "RWA ratios look fine, leverage ratio binds" dynamic discussed above.

## Bridge to Quant / ML

The math this note governs was already derived elsewhere in this vault: [[Value at Risk]] and [[Expected Shortfall]] work through the actual VaR and ES calculations, and [[Stress Testing]] works through scenario P&L mechanics. This note is about the *regulatory mandate* that makes computing those quantities correctly, and being able to prove they were computed correctly, a matter of licensed operation rather than best practice. That distinction — "can you compute VaR/ES" versus "can you prove your VaR/ES computation is trustworthy, continuously, in production" — is where a fast-growing subfield of quant risk work now sits.

**Model risk management as an ML/software-engineering discipline.** Validating that a risk model works correctly — not just what it computes, but whether its outputs can be trusted at 4am when a data feed silently breaks — increasingly looks like an applied ML and monitoring problem rather than a pure quant-finance one. Peysakhovich & Sieradzki's ensemble anomaly-detection framework is a direct example: it treats risk-calculation output streams (VaR, ES, sensitivities) as time series to be monitored with an ensemble of unsupervised outlier-detection methods plus deterministic domain rules, explicitly to satisfy the auditable-quality-control expectations Basel III and FRTB place on internal models. This is the same skillset — anomaly detection, drift monitoring, ensemble methods, production ML observability — used to monitor any ML system in production, applied to the specific, regulator-scrutinized domain of bank risk infrastructure. Quant risk teams increasingly need engineers who can build both the VaR/ES model *and* the system that watches the model for silent failure.

**Better estimators as a research target.** Vadrevu's GPR-Historical Simulation hybrid is the complementary half of the same story: rather than monitoring an existing VaR/ES pipeline for failure, it proposes a more robust way to estimate the volatility-covariance matrix feeding VaR/ES in the first place, explicitly benchmarked against ICAAP/CCAR-style backtesting requirements rather than against a generic forecasting metric. This is a useful pattern to recognize across quant-finance ML research generally: the regulatory backtest (does the model's stated confidence level match its observed breach rate over time) is often the actual objective function that matters, even when the paper's headline metric is something more familiar like quadratic loss.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why does Basel III require both a risk-weighted CET1 ratio and a non-risk-weighted leverage ratio? What failure mode does the leverage ratio catch that the CET1 ratio structurally cannot?
<details><summary>Answer</summary>The CET1 ratio scales required capital to the *riskiness* of assets, which is efficient when risk weights are accurate — a bank holding safe assets should need less capital than one holding risky ones. But risk weights are themselves modeled (via standardized tables or internal ratings-based models), and pre-2008 experience showed those models can be badly wrong — AAA-rated mortgage securities were assigned low risk weights that proved catastrophic. If the risk-weighting is wrong, a bank can pass its CET1 ratio comfortably while still being dangerously over-leveraged in dollar terms. The leverage ratio ignores risk weighting entirely and requires a minimum capital cushion against *total* exposure, providing a floor that holds even when the risk models feeding RWA are wrong, miscalibrated, or gamed.</details>

**Q2.** FRTB replaced 99% VaR with 97.5% Expected Shortfall for market-risk capital. Why does this distinction matter specifically for *capital adequacy*, given that VaR remains a commonly reported risk metric elsewhere?
<details><summary>Answer</summary>VaR is a quantile — it identifies a loss threshold but says nothing about how severe losses are once that threshold is breached. For day-to-day risk reporting or setting position limits, that can be acceptable: the threshold itself is informative. But capital adequacy is precisely about surviving the tail — the whole point of holding capital is to absorb losses in the bad scenarios, not the median ones. A capital charge based on VaR could be identical for a portfolio that loses "a bit more than VaR" on bad days and one that loses many multiples of VaR on bad days, even though the second portfolio needs far more capital to survive. Expected Shortfall averages losses beyond the VaR threshold, so it directly captures tail severity, and it is coherent (subadditive), which VaR is not — meaning it cannot perversely reward splitting up a portfolio to appear less risky. For a number whose entire purpose is sizing the buffer against catastrophic loss, tail-severity sensitivity and coherence are not optional properties.</details>

**Q3.** Explain the difference between Basel III capital ratios, FRTB, and CCAR/DFAST. Why can't any one of these substitute for the other two?
<details><summary>Answer</summary>They govern three different things. Basel III capital ratios (CET1, Tier 1, leverage) are capital *adequacy* tests — do you hold enough capital, steady-state, relative to your risk-weighted or gross exposure, today? FRTB is a market-risk *measurement* standard — it defines how the market-risk piece of the capital-ratio numerator's RWA is computed (VaR-based under Basel 2.5, ES-based under FRTB); it is not itself a pass/fail capital test. CCAR/DFAST is an independent, regulator-run *stress verification* exercise — the Fed specifies a severe macro scenario and, for the largest banks, runs its own supervisory models against the bank's book, deliberately not relying on the bank's internal VaR/ES engine to self-grade. A bank can pass steady-state capital ratios computed under a compliant FRTB framework and still fail CCAR, because CCAR is testing resilience to a specific forward-looking scenario the bank didn't choose and, partly, didn't calculate itself. None of the three can substitute for the others because each is designed to catch a different kind of failure: undercapitalization today, mismeasured market risk, and untested (or self-gradeable) forward-looking resilience.</details>

---

### Level 2 — Quantitative

**Q4.** A bank reports: CET1 capital = \$30B, RWA = \$350B, Tier 1 capital = \$36B, total leverage exposure = \$900B. Applicable capital conservation buffer = 2.5%; no countercyclical or G-SIB buffer applies; this is not a G-SIB (3% leverage minimum). Compute the CET1 ratio, Tier 1 ratio, and leverage ratio, and state whether the bank passes all three Basel III minimums.
<details><summary>Answer</summary>

CET1 ratio: $30/350 = 8.57\%$. Required minimum: $4.5\% + 2.5\% = 7.0\%$. **Pass**, headroom $+1.57$pp.

Tier 1 ratio: $36/350 = 10.29\%$. Required minimum: $6\% + 2.5\% = 8.5\%$. **Pass**, headroom $+1.79$pp.

Leverage ratio: $36/900 = 4.0\%$. Required minimum: $3\%$ (non-G-SIB). **Pass**, headroom $+1.0$pp.

All three ratios clear their respective minimums; the bank is Basel III compliant on this simplified balance sheet.</details>

**Q5.** A bank's FRTB-computed market-risk capital charge (97.5% ES over the appropriate liquidity horizons) is \$2.4B. Credit-risk RWA is \$180B and operational-risk RWA is \$20B. (a) Compute the market-risk RWA contribution and total RWA. (b) If the required CET1 ratio (minimum + buffer) is 7%, how much CET1 capital must the bank hold?
<details><summary>Answer</summary>

(a) Market-risk RWA $= 12.5 \times K_{\text{market}} = 12.5 \times \$2.4\text{B} = \$30\text{B}$.

Total RWA $= \$180\text{B} + \$30\text{B} + \$20\text{B} = \$230\text{B}$.

(b) Required CET1 capital $= 7\% \times \$230\text{B} = \$16.1\text{B}$.

Note how the market-risk capital charge, computed under FRTB using ES, flows into RWA via the $\times 12.5$ conversion and then directly scales the dollar amount of CET1 capital the bank must hold — this is the concrete mechanical link between FRTB (a measurement standard) and the CET1 ratio (a capital-adequacy test).</details>

---

### Level 3 — Coding

**Q6.** In `check_basel_iii_compliance`, the leverage minimum is selected with `0.05 if is_gsib else 0.03`, but the CET1 and Tier 1 minimums use the same `total_buffer` regardless of `is_gsib`. Explain why this is a simplification, and describe what you would change to make the function reflect Basel III more accurately for a G-SIB.
<details><summary>Answer</summary>

The simplification is that `total_buffer` is passed in as separate `capital_conservation_buffer`, `countercyclical_buffer`, and `gsib_surcharge` arguments, but nothing in the function *forces* a caller to actually supply a nonzero `gsib_surcharge` when `is_gsib=True` — the G-SIB surcharge (1–3.5% of RWA, sized to the bank's systemic footprint) is being treated as an independent input rather than being derived from `is_gsib` the way the leverage minimum is. A more accurate implementation would either (a) require a `gsib_bucket` parameter (e.g., an integer 1–5 corresponding to the Financial Stability Board's G-SIB bucketing) and look up the corresponding CET1 surcharge internally, mirroring how `is_gsib` directly determines the leverage minimum, or (b) at minimum, assert that `is_gsib=True` implies `gsib_surcharge > 0` so a caller can't silently mark a bank as systemic without applying the corresponding CET1 buffer. The current code is correct as a calculator given consistent inputs but does not enforce the coupling between "is this bank a G-SIB" and "what buffers apply to it" the way real Basel III implementation would.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---|---|
| If a bank's VaR/ES model is regulator-approved, its outputs can be trusted without further checking | Approval is a snapshot, not a permanent guarantee. Models can silently fail in production — stale data feeds, misconfiguration, pipeline breaks — while continuing to output plausible-looking numbers. This is exactly the gap ensemble anomaly-detection frameworks like EQAF target, and it is why Basel III/FRTB increasingly mandate continuous, automated model monitoring rather than one-time approval. |
| A CET1 ratio above 4.5% means the bank meets Basel III requirements | 4.5% is the bare regulatory minimum before buffers. The capital conservation buffer (2.5%), countercyclical buffer (0–2.5%), and G-SIB surcharge (1–3.5% for systemic banks) push the *effective* minimum well above 4.5% for any large institution; falling into the buffer, while not outright noncompliant, triggers automatic restrictions on dividends and buybacks. |
| FRTB is a capital requirement, like the CET1 or leverage ratio | FRTB is a *measurement standard* — it defines how the market-risk capital charge (and hence market-risk RWA) is computed. It is not itself a pass/fail solvency test; it feeds a number into the RWA denominator that the actual capital ratios (CET1, Tier 1, Total) are then tested against. |
| CCAR/DFAST stress tests are redundant with a bank's internal VaR/ES and Basel capital ratios | CCAR uses regulator-specified scenarios and, for the largest banks, partly regulator-run supervisory models, deliberately independent of the bank's own risk engine. Its entire value is that it does not require trusting the bank's internal model — a check the Basel ratios and FRTB, by construction, cannot provide on their own. |

## Related Concepts

- [[Value at Risk]] — the quantile measure Basel 2.5 used for market-risk capital, superseded by ES under FRTB
- [[Expected Shortfall]] — the coherent, tail-sensitive measure FRTB adopted for market-risk capital
- [[Stress Testing]] — the scenario-based technique underlying CCAR/DFAST and banks' own internal stress programs
- [[Correlation and Covariance Estimation]] — the estimation problem underlying both the VaR/ES inputs this framework mandates and the RWA models that feed the capital ratios
- [[Deep Hedging]] — uses the same coherent-risk-measure (CVaR/ES) argument, in an ML optimization context, that motivates FRTB's shift away from VaR

## Sources Used

- Peysakhovich, D., & Sieradzki, R. (2026). *How to Spot Outliers: an Ensemble Anomaly Detection Framework*. arXiv:2606.20079v1 — model risk management / anomaly detection for risk-calculation infrastructure under Basel III/FRTB
- Vadrevu, U. (2026). *A Hybrid Gaussian Process Regression Framework for Stable Volatility-Covariance Estimation: Evidence from Global Equity Indices*. arXiv:2605.17275v1 — VaR/ES estimation targeted at ICAAP/CCAR compliance
- Basel Committee on Banking Supervision (2017). *Basel III: Finalising post-crisis reforms*
- Basel Committee on Banking Supervision (2019). *Minimum Capital Requirements for Market Risk (FRTB)*

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-07-30 | Full content written | Content gap remediation — regulatory capital coverage |
