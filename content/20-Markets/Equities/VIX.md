---
type: concept
domain: 20-Markets
tags: [volatility, markets, risk]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-12
review_interval_days: 365
sources:
  - "Hull ch.26"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Risk / Pricing → Gap 5: BSM assumes constant σ — real markets show a volatility smile
> **This concept:** Provides a model-free market consensus measure of 30-day implied variance by aggregating information across all SPX option strikes, bypassing the need to assume any particular vol model.
> **Alternative approaches to this gap:** [[Implied Volatility]] (model-dependent, single-strike), [[Variance Swap]] (directly tradeable form of the same quantity)
> **You need first:** [[Black-Scholes Model]], [[Implied Volatility]], [[Variance Swap]]
> **This unlocks:** [[Volatility Surface]], regime classification, volatility targeting, VIX futures/ETF strategies

> CBOE 30-day implied vol index; model-free via variance swaps

## Why This Exists

**The gap:** Implied volatility from any single BSM inversion gives you the market's vol estimate only for one strike and one expiry. Different strikes give different implied vols (the volatility smile), so there is no single "market vol" reading from a single option.
**What came before:** Practitioners would quote the at-the-money implied vol as a rough proxy for market fear. But this ignored the rich information embedded in the full smile — particularly in the out-of-the-money puts, which price tail risk and tend to be the most sensitive barometer of market anxiety.
**What this adds:** The VIX formula, derived from the Carr-Madan log-contract replication of a variance swap, weights options by $1/K^2$ across all available strikes. This aggregation extracts the entire volatility smile's information into a single number that equals the fair strike of a 30-day variance swap — a model-free, cross-strike consensus on expected variance.
**What it still doesn't solve:** VIX is a 30-day fixed-horizon measure only. It does not capture the term structure of volatility (realized by VVIX or VIX futures), is exclusively for SPX (each asset needs its own measure), and can understate true variance when discrete jumps occur (the log-contract replication assumes continuous paths).

## Math Concepts

**VIX definition (conceptual):**

$$\text{VIX} = 100 \times \sqrt{\frac{2}{T} \left[\sum_{i: K_i < F} \frac{\Delta K_i}{K_i^2} e^{rT} P(K_i) + \sum_{i: K_i \geq F} \frac{\Delta K_i}{K_i^2} e^{rT} C(K_i)\right]}$$

where:
- $T$ = time to expiry (in years, targeting 30 calendar days)
- $F$ = forward price of SPX: $F = S_0 e^{rT}$
- $K_i$ = strike of the $i$-th option in the strip
- $\Delta K_i$ = spacing between adjacent strikes (usually $\Delta K_i = (K_{i+1} - K_{i-1})/2$)
- $P(K_i)$ = mid-price of OTM put at strike $K_i$ (used for $K_i < F$)
- $C(K_i)$ = mid-price of OTM call at strike $K_i$ (used for $K_i \geq F$)
- $r$ = risk-free rate (typically derived from T-bill yields)

**The $1/K^2$ weighting** is the key: each option's contribution is inversely proportional to the square of its strike. This is exactly the weighting that arises from the log-contract replication of a variance swap (Carr-Madan). Low-strike puts receive far higher weight than high-strike calls.

**Interpolation between expiries:** CBOE uses options at two expiries bracketing 30 days (near-term and next-term), then interpolates:

$$\text{VIX}^2 = 100^2 \times \left[T_1 \sigma_1^2 \cdot \frac{N_{T_2} - N_{30}}{N_{T_2} - N_{T_1}} + T_2 \sigma_2^2 \cdot \frac{N_{30} - N_{T_1}}{N_{T_2} - N_{T_1}}\right] \times \frac{252}{30}$$

where $\sigma_1^2, \sigma_2^2$ are the variance swap fair values at the two expiries, $N_T$ is the number of minutes to expiry.

**Relationship to variance swaps:**

$$\left(\frac{\text{VIX}}{100}\right)^2 \approx K_{\text{var}}^{30\text{d}}$$

The squared VIX (divided by 100) is the fair strike of a 30-day variance swap on SPX.

**Model-free property:** The formula makes no assumption about the distributional form of stock returns. It is derived from static replication and holds under any continuous semimartingale model (with caveats for jumps).

## Walkthrough

Suppose we have a simplified strip of 5 SPX options with $S = 5000$, $r = 0.05$, $T = 30/365$:

| Strike $K_i$ | Type | Mid Price | $\Delta K_i$ | Contribution $\frac{\Delta K_i}{K_i^2} e^{rT} \cdot \text{Price}$ |
|---|---|---|---|---|
| 4500 | Put | 18.50 | 250 | $\frac{250}{4500^2} \times 1.004 \times 18.50 = 2.30 \times 10^{-4}$ |
| 4750 | Put | 7.20 | 250 | $\frac{250}{4750^2} \times 1.004 \times 7.20 = 8.00 \times 10^{-5}$ |
| 5000 | Call+Put avg | 45.80 | 250 | $\frac{250}{5000^2} \times 1.004 \times 45.80 = 4.60 \times 10^{-4}$ |
| 5250 | Call | 6.10 | 250 | $\frac{250}{5250^2} \times 1.004 \times 6.10 = 5.53 \times 10^{-5}$ |
| 5500 | Call | 2.40 | 250 | $\frac{250}{5500^2} \times 1.004 \times 2.40 = 1.99 \times 10^{-5}$ |

Sum $\approx 8.32 \times 10^{-4}$.

$$\sigma^2 = \frac{2}{T} \times 8.32 \times 10^{-4} = \frac{2}{0.0822} \times 8.32 \times 10^{-4} \approx 0.0202$$

$$\text{VIX} \approx 100 \times \sqrt{0.0202} \approx 14.2$$

(This is a toy example with only 5 strikes; the real VIX uses hundreds.)

**Historical benchmarks:**

| VIX Level | Market Regime |
|-----------|--------------|
| < 12 | Extreme complacency |
| 12–20 | Normal, low-vol |
| 20–30 | Elevated concern |
| 30–40 | High stress / correction |
| > 40 | Crisis / panic (COVID 2020: 85, GFC 2008: 80) |

## Analysis

**VIX is forward-looking, not backward-looking:** VIX uses option prices, which reflect expectations. It is not the same as realized volatility, which measures what actually happened. On average VIX runs above realized vol (variance risk premium).

**Mean reversion:** VIX is strongly mean-reverting. It spikes in crises but reliably falls back to the 15–20 range over months. This mean reversion is what makes strategies like selling VIX futures (short volatility) profitable on average — but with catastrophic drawdown risk.

**VIX is not a tradeable instrument:** You cannot buy spot VIX. You trade VIX via futures, ETFs (VXX, UVXY), or VIX options. VIX futures are priced via the term structure and generally trade at a premium to spot VIX (contango) — which is costly for long-vol holders and profitable for short-vol holders who harvest the roll.

**The $1/K^2$ left-tail sensitivity:** Because OTM puts get heavy weight, VIX spikes sharply when put prices surge — even if realized vol hasn't moved yet. This is why VIX tends to "lead" realized volatility in a sell-off.

**Limitations:**
- VIX covers only the next 30 days; it says nothing about 3-month or 1-year volatility.
- Jump gaps in the underlying that aren't reflected in continuous option prices can cause VIX to understate true variance (the log-contract replication is exact only for continuous paths).
- VIX is for SPX only; each index (VVIX, VXN for Nasdaq, OVX for oil) has its own equivalent.

**Common misconception — "VIX predicts crashes":** VIX is elevated during crashes because option buyers demand protection — but it spikes after the crash begins, not before. Low VIX before a crash is not safety; it's complacency.

## Implementation

```python
import numpy as np

def compute_vix_simplified(strikes, option_prices, option_types,
                           S, r, T_years):
    """
    Compute VIX-style model-free implied variance from a strip of options.

    Parameters
    ----------
    strikes       : array of strike prices (sorted ascending)
    option_prices : array of mid-prices (OTM convention: puts below F, calls above)
    option_types  : array of 'P' or 'C'
    S             : current underlying price
    r             : risk-free rate (continuously compounded)
    T_years       : time to expiry in years
    """
    F = S * np.exp(r * T_years)   # forward price
    discount = np.exp(r * T_years)

    strikes = np.array(strikes, dtype=float)
    option_prices = np.array(option_prices, dtype=float)

    # Compute delta_K for each strike (trapezoidal spacing)
    n = len(strikes)
    delta_K = np.zeros(n)
    delta_K[0]    = strikes[1] - strikes[0]           # first point
    delta_K[-1]   = strikes[-1] - strikes[-2]         # last point
    delta_K[1:-1] = (strikes[2:] - strikes[:-2]) / 2  # interior points

    # Sum: sum_i (delta_K_i / K_i^2) * e^(rT) * Price_i
    contrib = (delta_K / strikes**2) * discount * option_prices
    sigma_sq = (2 / T_years) * np.sum(contrib)

    # Adjustment for the forward not being exactly on a strike
    # (K0 is the first strike below F — simplified: use F itself)
    K0 = strikes[np.searchsorted(strikes, F) - 1]
    adjustment = ((F / K0) - 1) ** 2
    sigma_sq -= adjustment / T_years

    vix = 100 * np.sqrt(max(sigma_sq, 0))
    return vix, sigma_sq

# --- Toy example ---
strikes      = [4500, 4750, 5000, 5250, 5500]
prices       = [18.50, 7.20, 45.80, 6.10, 2.40]   # OTM convention
types        = ['P',   'P',  'P',   'C',  'C']     # (ATM averaged into put side)
S            = 5000
r            = 0.05
T            = 30 / 365

vix_estimate, var_estimate = compute_vix_simplified(strikes, prices, types, S, r, T)
print(f"VIX estimate:    {vix_estimate:.2f}")
print(f"Variance strike: {var_estimate:.6f}")
print(f"Implied vol:     {np.sqrt(var_estimate)*100:.2f}%")

# --- Historical VIX analysis using yfinance (requires: pip install yfinance) ---
try:
    import yfinance as yf
    import pandas as pd
    import matplotlib.pyplot as plt

    vix = yf.download("^VIX", start="2015-01-01", end="2024-12-31", progress=False)
    spx = yf.download("^GSPC", start="2015-01-01", end="2024-12-31", progress=False)

    # Compute 30-day realized vol for SPX
    spx_rv = spx["Close"].pct_change().rolling(21).std() * np.sqrt(252) * 100

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

    ax1.plot(spx["Close"], color='steelblue', lw=1.2, label='SPX')
    ax1.set_ylabel('SPX Level')
    ax1.legend()

    ax2.plot(vix["Close"], color='red', lw=1.2, alpha=0.8, label='VIX (IV)')
    ax2.plot(spx_rv, color='navy', lw=1.2, alpha=0.7, label='SPX 30d Realized Vol')
    ax2.set_ylabel('Volatility (%)')
    ax2.set_xlabel('Date')
    ax2.legend()
    ax2.set_title('VIX vs Realized Vol — Variance Risk Premium')
    plt.tight_layout()
    plt.show()

    # Average variance risk premium
    vrp = vix["Close"].shift(21) - spx_rv
    print(f"\nAverage VRP (VIX - Realized, lagged): {vrp.mean():.2f} vol pts")

except ImportError:
    print("Install yfinance for the historical analysis: pip install yfinance")
```

## Bridge to Quant / ML

- **VIX as a feature:** VIX level and VIX term structure slope are among the most powerful features in equity return prediction models. High VIX periods tend to precede above-average returns (risk premium) but also above-average drawdowns.
- **Volatility targeting:** Many risk-managed strategies scale equity exposure inversely with realized or implied vol. VIX or SPX realized vol is the denominator — when vol is high, reduce position sizes.
- **VIX futures carry:** The VIX futures curve is usually in contango (futures above spot VIX). Systematically rolling short VIX futures harvests this carry but has severe left-tail risk. ML can predict when contango is "safe" vs. about to invert.
- **VVIX:** The VIX of VIX — measures vol-of-vol. Elevated VVIX signals that even VIX's own movement is uncertain, a higher-order fear signal.
- **Regime detection:** Simple HMM or clustering models on (VIX level, VIX change, realized vol) reproduce many known market regimes (bull, bear, crisis). VIX is the most information-dense single variable for regime classification.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why is VIX described as "model-free" whereas a single implied volatility is not?
<details><summary>Answer</summary>A single implied volatility is computed by inverting the Black-Scholes formula — you assume BSM is the correct model, then back out the $\sigma$ that makes the model price match the market price. The result is model-dependent: a different model (e.g., Heston) would give a different implied vol for the same option price. VIX, by contrast, is computed from a static replication argument (the log-contract / variance swap). It aggregates option prices across all strikes using the $1/K^2$ weighting derived from no-arbitrage — no assumption is made about the specific stochastic process for the stock. Any continuous semimartingale model gives the same VIX from the same option prices.</details>

**Q2.** Why do OTM puts receive much higher weight than OTM calls in the VIX formula? What does this imply about what VIX is really measuring?
<details><summary>Answer</summary>The $1/K^2$ weighting means that lower-strike options get far more weight than higher-strike options. In the VIX formula, OTM puts have strikes $K < F$ (low K → high $1/K^2$ weight), while OTM calls have strikes $K > F$ (high K → low weight). This means VIX is heavily influenced by the price of downside protection. When put prices surge (investors paying for crash protection), VIX spikes sharply. In effect, VIX is more a "left-tail fear gauge" than a symmetric volatility measure — it tends to jump more when the market falls than when it rises.</details>

**Q3.** A trader says "VIX is at 12, which is historically very low, so the market is safe and I can buy stocks without worry." What is wrong with this reasoning?
<details><summary>Answer</summary>There are two errors. First, VIX measures *expected* volatility, not realized volatility — a low VIX reflects that current option prices are cheap, which may simply mean investors are complacent. Some of the worst crashes (1987, 2018 vol blow-up) occurred when VIX was at or near historical lows. Second, VIX tends to spike after a crash begins, not before — it is contemporaneous with fear, not a leading indicator of safety. Low VIX is complacency, not safety; it actually raises the risk of a volatility spike because short-volatility positions tend to be crowded at low VIX levels, and their unwinding amplifies any sell-off.</details>

---

### Level 2 — Quantitative

**Q4.** VIX is currently at 20. What is the market's implied 30-day variance, and what daily return volatility does this imply?
<details><summary>Answer</summary>VIX = 20 means annualized vol is 20%. The implied 30-day variance: $(\text{VIX}/100)^2 = (0.20)^2 = 0.04$ (annualized). For 30 days: $\sigma^2_{30d} = 0.04 \times 30/252 \approx 0.004762$, so $\sigma_{30d} = 6.90\%$ over the 30-day period. Daily volatility: $\sigma_{daily} = 0.20/\sqrt{252} \approx 1.26\%$. So the market expects daily moves of about ±1.26% (one standard deviation) over the next month.</details>

**Q5.** In the toy VIX walkthrough with 5 strikes (sum of contributions $= 8.32 \times 10^{-4}$, $T = 30/365$), verify the VIX calculation.
<details><summary>Answer</summary>$\sigma^2 = \frac{2}{T} \times \text{sum} = \frac{2}{30/365} \times 8.32 \times 10^{-4} = \frac{2 \times 365}{30} \times 8.32 \times 10^{-4} = 24.333 \times 8.32 \times 10^{-4} = 0.02025$. Then $\text{VIX} = 100 \times \sqrt{0.02025} = 100 \times 0.1423 = 14.2$. This confirms the walkthrough result. Note that in practice the forward-correction term ($((F/K_0)-1)^2/T$) is usually small and was omitted in this toy example.</details>

---

### Level 3 — Coding

**Q6.** The `compute_vix_simplified` function computes a VIX estimate from a strip of options. What refinements would be needed to match the official CBOE VIX methodology exactly?
<details><summary>Answer</summary>Several refinements are needed: (1) **Two expiry interpolation:** CBOE uses options at two expiries bracketing 30 days (near-term $T_1$ and next-term $T_2$) and interpolates $\text{VIX}^2 = w_1 \sigma_1^2 + w_2 \sigma_2^2$ where the weights are based on minutes to expiry. The simplified function only handles one expiry. (2) **Forward price precision:** CBOE derives $F$ from put-call parity using the pair of put/call options at each strike, not from $Se^{rT}$ directly. (3) **$K_0$ selection:** The first strike below $F$ (not $F$ itself) is used as $K_0$ in the correction term. (4) **Termination condition:** Contributions are included until two consecutive zero-bid options are encountered — then truncated. (5) **OTM selection:** Uses OTM puts below $F$ and OTM calls above $F$, with the ATM strike averaged using both put and call prices.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| VIX predicts market crashes before they happen | VIX is contemporaneous with fear, not a leading indicator. It spikes during a crash, not before. Low pre-crash VIX reflects complacency, not safety. |
| You can trade "spot VIX" directly | Spot VIX is not tradeable. VIX is traded via futures, options on VIX, or VIX ETFs (VXX, UVXY). These instruments track VIX imperfectly due to futures roll costs. |
| VIX = realized volatility of the S&P 500 | VIX is implied (forward-looking) not realized (backward-looking). On average, VIX runs 3–5 vol points above subsequent realized vol (the variance risk premium). |
| High VIX means the market expects a crash | VIX measures expected volatility — moves in either direction. High VIX means large moves are expected, not necessarily downward moves specifically. |

## Related Concepts

- [[Implied Volatility]]
- [[Variance Swap]]
- [[Volatility Smile]]
- [[Gamma Scalping]]
- [[Black-Scholes Model]]

## Sources Used

- Hull, *Options, Futures, and Other Derivatives*, Ch. 26 (Model-free volatility and variance swaps)
- CBOE VIX White Paper (2009, updated 2019): official methodology document
- Carr & Wu (2006), "A Tale of Two Indices"

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | Hull + initial build |
| 2026-04-12 | Note created | bootstrap |
| 2026-04-11 | QA review: no issues found | quality review |
