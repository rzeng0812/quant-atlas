---
type: concept
domain: 30-Models
tags: [risk, stress-testing, portfolio]
status: math
stability: evolving
confidence: high
last_reviewed: 2026-04-18
review_interval_days: 90
sources:
  - "Hull, Options Futures and Other Derivatives, ch. 22"
  - "Basel Committee, Principles for Sound Stress Testing Practices (2009)"
  - "Jorion, Value at Risk, 3rd ed."
created: 2026-04-18
---

> [!info] Problem Chain
> **Chain:** Hedging & Risk — supporting concept (scenario-based risk beyond statistical tail measures)
> **This concept:** Stress Testing applies specific crisis scenarios (historical or hypothetical) to current portfolio weights to reveal risks invisible to VaR/ES — non-linear exposures, correlation breakdown, and crowded trade dynamics.
> **Alternative approaches to this gap:** none
> **You need first:** [[Value at Risk]], [[Expected Shortfall]], [[Factor Models]]
> **This unlocks:** none (terminal supporting concept)

## Why This Exists

**The gap:** VaR and ES are calibrated on historical return distributions under normal-to-moderately-bad conditions. During actual crises, volatility doubles or triples, correlations surge toward 1 (destroying diversification), and liquidity evaporates — all simultaneously. The historical distribution badly underestimates crisis severity.

**What came before:** Statistical tail measures (VaR, ES) captured the "normal bad day" tail but were blind to structural breaks. The 2008 financial crisis was a discontinuity relative to prior data — no amount of historical simulation would have predicted it from pre-2007 returns.

**What this adds:** Stress Testing applies specific crisis scenarios directly to current portfolio weights, bypassing distributional assumptions entirely. Both historical replays (what would my portfolio have lost in 2008?) and hypothetical shocks (what if rates rise 200bp AND equities fall 30%) are used. Regulatory stress tests (Basel, Dodd-Frank) mandate specific scenarios.

**What it still doesn't solve:** Stress tests are backward-looking — the next crisis will differ from historical scenarios. Scenario selection involves subjective judgment. Point-in-time P&L estimates ignore path dependency (margin calls, forced liquidations during the crisis). Testing too few scenarios creates false confidence.

[[Value at Risk]] and [[Expected Shortfall]] are calibrated on the historical distribution of returns. They tell you about normal bad days — the kind of losses you might see in an average rough quarter. What they cannot tell you is what happens when the world breaks.

Think of a stress test like a building inspection. Standard safety ratings tell you how the building performs under typical loads — a busy workday, a mild storm. A stress test asks: what happens in an earthquake? In a hurricane? The distribution of everyday loads tells you almost nothing about structural failure modes.

In finance, the "earthquakes" are crises: the 2008 global financial crisis, the COVID-19 crash of March 2020, the dot-com bust of 2000–2002, Black Monday in October 1987, the 1997 Asian currency crisis. These events are not in the tail of a normal distribution — they are in a different distribution entirely. During crises, volatility doubles or triples, correlations collapse toward 1 (assets that normally offset each other suddenly fall together), and liquidity evaporates. A portfolio that VaR deems "safe" can lose 30% in two weeks.

Regulators recognized this gap after 2008 and now require banks to formally stress test their portfolios against specific scenarios. For quant strategies, stress testing reveals hidden risk concentrations, crowded trades, and assumptions baked into factor models that only hold in calm markets.

Stress testing does not replace VaR or ES — it complements them. Together they form a complete risk picture: VaR/ES for the everyday tail, stress tests for the extraordinary tail.

## Math Concepts

There are three main approaches to stress testing.

**1. Historical scenario replay**

Take the actual daily returns observed during a crisis period. Apply those returns to your *current* portfolio weights. The portfolio P&L under that historical scenario is:

$$\text{P\&L}_{\text{stress}} = \sum_{i=1}^{N} w_i \cdot r_i^{\text{crisis}}$$

where $w_i$ is the current dollar position in asset $i$ and $r_i^{\text{crisis}}$ is the return of asset $i$ during the crisis window.

The key insight: the crisis returns are applied to *today's* portfolio, not the portfolio that existed during the crisis. You are asking "how would I do in 2008 if I had my current positions?" This is more useful than historical P&L of the actual portfolio.

Common historical scenarios to replay:

| Scenario | Period | Key shock |
|----------|--------|-----------|
| Global Financial Crisis | Sep–Dec 2008 | Credit, equity, vol |
| COVID crash | Feb–Mar 2020 | Equity, rates, oil |
| Dot-com bust | Mar 2000–Oct 2002 | Growth equity |
| Black Monday | Oct 19, 1987 | Equity -22% in one day |
| 1997 Asian crisis | Jul–Dec 1997 | EM FX, contagion |
| European sovereign debt | May–Jun 2010 | EUR, peripheral spreads |
| Taper tantrum | May–Jun 2013 | Rates, EM |
| Russia/LTCM | Aug–Sep 1998 | Credit, EM, liquidity |

**2. Hypothetical (factor shock) scenarios**

Rather than replaying history, you manually specify shocks to key risk factors simultaneously:

$$\text{P\&L}_{\text{stress}} = \sum_{k=1}^{K} \frac{\partial V}{\partial F_k} \cdot \Delta F_k$$

where $F_k$ are the risk factors (equity index, interest rates, credit spreads, FX, volatility) and $\Delta F_k$ are the hypothesized shocks.

Standard hypothetical scenarios every quant should run:

| Scenario | Factor shocks |
|----------|--------------|
| Equity crash | S&P 500 −30%, VIX +25 pts |
| Rate shock (parallel) | All maturities +200 bp |
| Credit crisis | IG spreads +200 bp, HY +500 bp |
| Liquidity crisis | Bid-ask spreads ×10, asset correlations → 1 |
| Stagflation | Rates +150 bp, equity −20%, oil +50% |
| Dollar spike | USD +15% vs all currencies |

**3. Reverse stress testing**

Forward stress testing asks: "Given this scenario, what is my loss?"  
Reverse stress testing asks: "What scenario would cause me to lose $X?" or "What would have to happen for our firm to become insolvent?"

Formally, find the minimum-norm scenario $\Delta \mathbf{F}$ such that:

$$\sum_{k} \frac{\partial V}{\partial F_k} \cdot \Delta F_k = -L^*$$

where $L^*$ is the loss threshold (e.g., half the firm's capital). This is an inverse problem — you work backward from the disaster to the cause. Regulators increasingly require reverse stress testing as a complement to forward scenarios.

**Correlation breakdown**

A key feature of crises is that asset correlations spike toward 1. A "diversified" portfolio with normal pairwise correlations of 0.2–0.4 suddenly has correlations of 0.8–0.9. The stress P&L can be estimated using a crisis correlation matrix $\Sigma_{\text{crisis}}$ instead of the calm-period estimate:

$$\text{VaR}_{\text{stress}} = z_\alpha \cdot \sqrt{\mathbf{w}^\top \Sigma_{\text{crisis}} \mathbf{w}}$$

## Walkthrough

**Portfolio:** Long \$1M S&P 500 (via SPY), long \$500K 10-year Treasury bond (via TLT). Normal times: correlation ≈ −0.3 (bonds rally when equities fall — classic diversification).

**Historical scenario: 2008 crisis (Sep–Dec 2008)**

During the 2008 financial crisis, both assets fell together — the "flight to safety" initially failed as liquidity dried up globally:

- SPY return: approximately −38%
- TLT return: approximately +30% (eventually recovered as Fed acted)

*Simple replay:*
$$\text{P\&L} = \$1{,}000{,}000 \times (-0.38) + \$500{,}000 \times (+0.30) = -\$380{,}000 + \$150{,}000 = -\$230{,}000$$

The portfolio loses 15.3% overall — significant but manageable if hedged.

**Historical scenario: March 2020 (COVID crash)**

In the sharpest part of the crash (Feb 20 – Mar 23, 2020):

- SPY: approximately −34%
- TLT: approximately +20% (then briefly fell as even Treasuries were sold in the liquidity panic)

$$\text{P\&L} = \$1{,}000{,}000 \times (-0.34) + \$500{,}000 \times (+0.20) = -\$340{,}000 + \$100{,}000 = -\$240{,}000$$

**Key insight: diversification held in both cases** — but only because Treasuries eventually rallied. In a stagflation scenario (rates rise AND equities fall), the bond holding would amplify losses instead of offsetting them.

**Hypothetical scenario: rate shock + equity crash**

Suppose rates rise 200 bp (TLT falls ~17%) AND equities fall 20%:

$$\text{P\&L} = \$1{,}000{,}000 \times (-0.20) + \$500{,}000 \times (-0.17) = -\$200{,}000 - \$85{,}000 = -\$285{,}000$$

This scenario — stagflation — shows the bond position switching from hedge to additional loss.

## Analysis

**What stress testing reveals that VaR misses:**

1. **Correlation instability.** VaR assumes stable correlations estimated from recent history. Stress tests expose portfolios that are "diversified" only in calm regimes.

2. **Crowded trades.** If a strategy is widely deployed (e.g., risk parity, momentum), everyone unwinds simultaneously in a crisis, amplifying losses far beyond VaR estimates.

3. **Non-linear exposures.** Options, structured products, and leveraged ETFs have convex payoffs — their behavior in large moves cannot be extrapolated from small-move VaR.

4. **Liquidity gaps.** VaR assumes you can liquidate at mid-prices. In a crisis, bid-ask spreads can widen 10× and positions that took weeks to build may need to be unwound in hours at terrible prices.

**Limitations:**

- Historical scenarios are backward-looking; the next crisis will be different in important ways.
- Hypothetical scenarios require subjective judgment — which shocks to model, how large.
- Stress P&L is point-in-time; it does not capture path dependency or the cost of margin calls during the crisis.
- Risk of "scenario anchoring": if you only test the 2008 scenario, you may miss risks not present in 2008 (e.g., a tech sector concentration that did not exist then).

**Regulatory context:**

- Basel III requires banks to run internal stress tests and maintain capital buffers adequate for stress scenarios.
- Dodd-Frank (US) and the ECB's EBA stress tests mandate annual supervisory stress testing at major banks.
- Regulators specify the scenarios; banks must demonstrate they can survive them without systemic intervention.

## Implementation

```python
import numpy as np
import pandas as pd

# ── 1. Define scenario shocks ──────────────────────────────────────────────
# Each scenario is a dict mapping asset ticker to return shock
SCENARIOS = {
    "GFC_2008": {
        "SPY": -0.38,   # S&P 500 (Sep-Dec 2008)
        "TLT": +0.30,   # 20yr Treasury
        "GLD": +0.05,   # Gold
        "HYG": -0.25,   # High yield bonds
    },
    "COVID_Mar2020": {
        "SPY": -0.34,
        "TLT": +0.20,
        "GLD": +0.04,
        "HYG": -0.22,
    },
    "Rate_Shock_200bp": {
        "SPY": -0.12,   # historical equity sensitivity to +200bp
        "TLT": -0.17,   # duration ~17 for 20yr bond
        "GLD": -0.05,   # real rates rise, gold falls
        "HYG": -0.08,   # credit spreads widen modestly
    },
    "Stagflation": {
        "SPY": -0.20,
        "TLT": -0.17,   # both fall — the worst case for 60/40
        "GLD": +0.15,   # gold is a stagflation hedge
        "HYG": -0.15,
    },
    "Equity_Crash_30pct": {
        "SPY": -0.30,
        "TLT": +0.15,
        "GLD": +0.08,
        "HYG": -0.20,
    },
}

# ── 2. Current portfolio positions (in dollars) ──────────────────────────
portfolio = {
    "SPY": 1_000_000,   # long $1M equities
    "TLT":   500_000,   # long $500k long-duration Treasuries
    "GLD":   200_000,   # long $200k gold
    "HYG":   300_000,   # long $300k high yield
}
total_nav = sum(portfolio.values())  # $2,000,000

# ── 3. Stress test function ───────────────────────────────────────────────
def run_stress_test(
    portfolio: dict[str, float],
    scenarios: dict[str, dict[str, float]],
) -> pd.DataFrame:
    """
    Apply each scenario's shocks to the current portfolio.
    Returns a DataFrame with P&L and return for each scenario.
    """
    results = []
    for scenario_name, shocks in scenarios.items():
        pnl = 0.0
        pnl_by_asset = {}
        for asset, position in portfolio.items():
            shock = shocks.get(asset, 0.0)
            asset_pnl = position * shock
            pnl += asset_pnl
            pnl_by_asset[asset] = asset_pnl
        results.append({
            "scenario": scenario_name,
            "total_pnl": pnl,
            "pct_return": pnl / total_nav,
            **{f"pnl_{k}": v for k, v in pnl_by_asset.items()},
        })
    return pd.DataFrame(results).set_index("scenario")

results = run_stress_test(portfolio, SCENARIOS)
print(f"Portfolio NAV: ${total_nav:,.0f}\n")
print("Stress Test Results:")
print(results[["total_pnl", "pct_return"]].to_string(
    formatters={
        "total_pnl": lambda x: f"${x:>12,.0f}",
        "pct_return": lambda x: f"{x:>8.1%}",
    }
))

# ── 4. Correlation breakdown demonstration ────────────────────────────────
# Show how "diversification benefit" evaporates in crisis
import matplotlib.pyplot as plt

# Normal-period correlation matrix (SPY, TLT, GLD, HYG)
corr_normal = np.array([
    [ 1.00, -0.30,  0.05,  0.70],  # SPY
    [-0.30,  1.00,  0.10, -0.15],  # TLT
    [ 0.05,  0.10,  1.00,  0.00],  # GLD
    [ 0.70, -0.15,  0.00,  1.00],  # HYG
])

# Crisis-period correlation matrix (all assets highly correlated)
corr_crisis = np.array([
    [ 1.00, -0.05,  0.40,  0.90],  # SPY
    [-0.05,  1.00, -0.10,  0.05],  # TLT (loses its hedge quality)
    [ 0.40, -0.10,  1.00,  0.35],  # GLD
    [ 0.90,  0.05,  0.35,  1.00],  # HYG (moves with equities)
])

assets = ["SPY", "TLT", "GLD", "HYG"]
weights = np.array([w / total_nav for w in portfolio.values()])

# Annualized vol estimates per asset
vols = np.array([0.18, 0.14, 0.16, 0.12])

# Portfolio volatility under normal vs crisis correlations
sigma_normal = np.diag(vols)
cov_normal = sigma_normal @ corr_normal @ sigma_normal
cov_crisis = sigma_normal @ corr_crisis @ sigma_normal

port_vol_normal = np.sqrt(weights @ cov_normal @ weights)
port_vol_crisis = np.sqrt(weights @ cov_crisis @ weights)

print(f"\nPortfolio volatility (normal correlations): {port_vol_normal:.1%}")
print(f"Portfolio volatility (crisis correlations):  {port_vol_crisis:.1%}")
print(f"Volatility multiplier in crisis:             {port_vol_crisis/port_vol_normal:.2f}x")

# ── 5. Reverse stress test: find the break-even loss scenario ─────────────
# What uniform equity shock wipes out 20% of NAV?
target_loss = -0.20 * total_nav  # -$400,000

# Only equity position (simplified)
equity_position = portfolio["SPY"]
required_return = target_loss / equity_position
print(f"\nReverse stress test:")
print(f"  To lose 20% of NAV (${-target_loss:,.0f}) via equity alone:")
print(f"  Required SPY return: {required_return:.1%}")
```

## Bridge to Quant / ML

**Strategy robustness.** Before deploying a quant strategy, stress testing it against historical crises answers a critical question: does the strategy survive? A momentum strategy that works beautifully in normal markets may have devastating drawdowns in March 2020 or 2008. Running the strategy's backtest through crisis windows separately (not just in aggregate) reveals regime-specific fragility.

**Risk budgeting.** Stress test P&L can be decomposed by position or factor, just like VaR contribution. This identifies which positions drive the worst-case outcomes and informs position sizing and hedging.

**ML connections:**
- Stress testing can be framed as out-of-distribution (OOD) detection: crisis periods are OOD samples relative to the normal-regime training distribution. ML models trained on normal-market data will systematically misprice risk in these regimes.
- Adversarial scenario generation: generative models (VAE, GAN) can be used to generate plausible stress scenarios beyond the historical record — synthetic crises that explore the space of extreme but coherent market moves.
- Regime detection models ([[Regime Detection]]) can trigger automatic stress testing when market microstructure signals a transition toward a crisis-like state.

**Factor models and stress.** A factor model decomposes portfolio variance as $\Sigma = B F B^\top + D$. Stress testing within this framework means shocking the factor returns $\Delta \mathbf{f}$ and computing $\Delta P = \mathbf{w}^\top B \Delta \mathbf{f}$. This allows you to test factor-specific scenarios (e.g., "value factor crashes") without specifying shocks to every individual asset.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** What fundamental limitation of VaR and ES motivates stress testing? Why can't a sufficiently extreme VaR (e.g., 99.99%) substitute for stress testing?
<details><summary>Answer</summary>VaR and ES are calibrated on the *observed* historical distribution of returns. They cannot capture: (a) events outside the historical window (the 2008 crisis was unprecedented when it happened); (b) structural breaks where volatility, correlations, and liquidity change simultaneously and discontinuously; (c) non-linear exposures (options, structured products) that have convex payoffs in large moves.

Even 99.99% VaR cannot substitute because: it still extrapolates from the same historical distribution, just further into the tail. A 99.99% VaR might be \$5M on a normally distributed portfolio — but if a Black Swan event causes \$50M loss through a mechanism not present in the historical data (e.g., a bond market liquidity freeze that has never happened), the VaR tells you nothing about it. Stress testing is scenario-based rather than distribution-based, which is why it captures these structural risks.</details>

**Q2.** Explain the difference between historical scenario replay and hypothetical scenario testing. What is the key advantage of each?
<details><summary>Answer</summary>**Historical scenario replay:** Takes actual returns from a specific crisis period (e.g., 2008: Sep–Dec) and applies them to today's portfolio weights. Key advantage: the scenario is internally consistent — the correlated moves across assets actually happened together in a coherent way. The equity crash, credit spread widening, vol spike, and FX moves of 2008 occurred simultaneously with realistic magnitude and co-movement.

**Hypothetical scenarios:** Manually specify factor shocks (e.g., rates +200bp AND equity -30%). Key advantage: you can test scenarios that have never occurred historically but are plausible — e.g., a stagflation scenario combining high rates with falling equities, which is rare in post-1990 data. You can also test portfolio-specific risks (e.g., a concentration in a single sector that 2008 didn't specifically stress).</details>

**Q3.** What is reverse stress testing, and why have regulators increasingly required it alongside forward stress tests?
<details><summary>Answer</summary>Forward stress testing asks: "Given scenario X, what is my loss?" Reverse stress testing asks: "What scenario would cause me to lose amount $L$ (e.g., become insolvent)?" — working backward from the disaster to identify its causes. Regulators require it because: (1) it forces firms to explicitly identify their break points — what combination of events is existentially threatening; (2) it discovers scenarios the firm hadn't thought to test forward — the reverse optimization may reveal unexpected vulnerabilities; (3) it answers the regulator's real concern: "Under what conditions does this firm need a bailout?" Forward tests show you survived known scenarios; reverse tests reveal unknown scenarios that could cause failure.</details>

---

### Level 2 — Quantitative

**Q4.** A portfolio holds \$2M in SPY (equities) and \$1M in TLT (long-duration bonds). In a "rate shock + equity decline" scenario: SPY falls 15%, TLT falls 12% (duration ~17, rates up ~70bp). What is the portfolio P&L and return?
<details><summary>Answer</summary>

P&L from equities: $\$2{,}000{,}000 \times (-0.15) = -\$300{,}000$

P&L from bonds: $\$1{,}000{,}000 \times (-0.12) = -\$120{,}000$

Total P&L: $-\$300{,}000 - \$120{,}000 = \mathbf{-\$420{,}000}$

Total portfolio NAV: $\$3{,}000{,}000$

Portfolio return: $-420{,}000 / 3{,}000{,}000 = \mathbf{-14.0\%}$

This is the "stagflation-light" scenario — both assets falling, which eliminates the diversification benefit. Under normal conditions (equities -15%, bonds +8%), the bond hedge would have offset much of the equity loss.</details>

**Q5.** A portfolio has current vol of 12% annually under normal correlations. In a crisis, asset correlations all double (e.g., 0.3 → 0.6) while individual asset vols stay constant. By what approximate factor does portfolio vol increase? (Assume the portfolio is equally weighted across 4 assets each with vol 20%.)
<details><summary>Answer</summary>

For an equal-weight portfolio of $N$ assets each with vol $\sigma$ and uniform pairwise correlation $\rho$:

$$\sigma_P = \sigma\sqrt{\frac{1 + (N-1)\rho}{N}}$$

Normal ($\rho = 0.3$): $\sigma_P = 0.20\sqrt{(1 + 3 \times 0.3)/4} = 0.20\sqrt{1.9/4} = 0.20\sqrt{0.475} = 0.20 \times 0.689 = \mathbf{13.8\%}$

Crisis ($\rho = 0.6$): $\sigma_P = 0.20\sqrt{(1 + 3 \times 0.6)/4} = 0.20\sqrt{2.8/4} = 0.20\sqrt{0.70} = 0.20 \times 0.837 = \mathbf{16.7\%}$

Vol increases by factor $16.7\% / 13.8\% = \mathbf{1.21\times}$ (21% increase). At $\rho = 0.9$ (full correlation crisis): $\sigma_P = 0.20\sqrt{3.7/4} = 19.2\%$ — nearly the individual asset vol, confirming diversification has nearly vanished.</details>

---

### Level 3 — Coding

**Q6.** The implementation stores scenarios as dictionaries mapping tickers to return shocks. Describe how you would extend this to a **factor-based stress test** framework where scenarios are defined as factor shocks (e.g., market -30%, rates +200bp) and portfolio exposures are captured via a factor model — rather than per-asset shocks.
<details><summary>Answer</summary>

Factor-based stress testing structure:

```python
# Step 1: Define factor-level shocks
factor_scenarios = {
    "Equity_Crash": {"market": -0.30, "credit_spread": +0.03, "vol": +0.25},
    "Rate_Shock":   {"rates_10yr": +0.02, "market": -0.10},
}

# Step 2: Estimate portfolio factor exposures (from factor model)
# portfolio_factor_exposures: {factor_name: portfolio_dollar_sensitivity}
portfolio_exposures = {
    "market": 1_800_000,   # $1.8M DV01 to market factor
    "rates_10yr": -500_000, # -$500K per 100bp (duration)
    "credit_spread": 300_000,
    "vol": -200_000,        # short vol via options
}

# Step 3: Compute P&L per scenario
for scenario_name, shocks in factor_scenarios.items():
    pnl = sum(portfolio_exposures.get(f, 0) * shock 
              for f, shock in shocks.items())
    print(f"{scenario_name}: ${pnl:,.0f}")
```

Advantages: (a) scenarios are defined once in factor space and apply to any portfolio via its factor exposures; (b) new assets require only estimating their factor betas, not new per-asset shock definitions; (c) factor-level scenarios are more economically intuitive and easier to calibrate to historical crises.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Passing historical stress tests means the portfolio is safe | Historical scenarios are backward-looking. The next crisis will have a different configuration. Passing 2008 stress test doesn't protect against a 2022-style stagflation shock. |
| Stress testing only matters for banks | Any leveraged strategy or concentrated portfolio can suffer crisis losses far beyond VaR. Stress testing is standard practice for hedge funds, asset managers, and pension funds. |
| Worst historical scenario is the worst possible scenario | Historical data is a small sample of possible crises. Reverse stress testing and adversarial scenario generation explore the space of plausible but unobserved disasters. |
| Stress P&L equals actual crisis loss | Stress P&L is a static calculation. Actual crisis losses include path dependency, margin calls, forced liquidations at bad prices, and bid-ask spread widening. |

## Related Concepts

- [[Value at Risk]] — the standard risk measure that stress testing supplements
- [[Expected Shortfall]] — the tail average that stress testing scenarios can be compared against
- [[Maximum Drawdown]] — path-dependent measure of crisis impact on a strategy
- [[Factor Models]] — natural framework for specifying and decomposing factor-level stress shocks
- [[Correlation and Covariance Estimation]] — crisis-period correlation matrices are the heart of stress scenarios

## Sources Used

- Hull, J. (2022). *Options, Futures and Other Derivatives*, 11th ed., ch. 22 — stress testing overview
- Basel Committee on Banking Supervision (2009). *Principles for Sound Stress Testing Practices and Supervision*
- Jorion, P. (2006). *Value at Risk*, 3rd ed. — scenario analysis and stress testing chapters
- BCBS (2019). *Minimum Capital Requirements for Market Risk (FRTB)* — regulatory stress testing standards

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | initial build |
