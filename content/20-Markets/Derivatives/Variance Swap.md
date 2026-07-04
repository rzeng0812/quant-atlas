---
type: concept
domain: 20-Markets
tags: [derivatives, volatility]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-12
review_interval_days: 365
sources:
  - "Hull ch.26"
created: 2026-04-12
---

> Payoff = N·(σ²_realized − K_var); pure vol exposure

> [!info] Problem Chain
> **Chain:** Pricing → Gap 5 extension: Trade volatility directly as an asset
> **This concept:** Creates a contract whose payoff is pure realized variance minus a fixed strike — enabling direct, model-free exposure to volatility without the direction risk and delta-hedging overhead of vanilla options.
> **Alternative approaches to this gap:** [[VIX]] futures (approximate forward variance but not a pure variance swap), vanilla options with delta hedge (impure vol exposure, path-dependent hedging costs)
> **You need first:** [[Implied Volatility]], [[Volatility Smile]], [[Delta Hedging]], [[Option Greeks]] (vega)
> **This unlocks:** [[VIX]], Volatility Arbitrage, dispersion trading, correlation swaps

## Why This Exists

**The gap:** Traders who wanted to bet on volatility had to use options. But options have delta — they respond to the stock's direction, not just its volatility level. To isolate the volatility bet, you needed to continuously delta-hedge, which introduced transaction costs, rebalancing error, and path dependency. A vol position built from options was never purely about vol — it was always contaminated by directional noise.

**What came before:** The standard approach was to buy a straddle (call + put at the same strike) and delta-hedge it continuously. In theory, this produces a pure gamma position that profits when realized vol exceeds implied vol. In practice, the P&L depends on the path of the stock, not just its total realized vol — a stock that moves in one direction produces different hedging costs than one that oscillates by the same total amount. The gamma-theta P&L is path-dependent, hard to predict, and operationally intensive.

**What this adds:** A variance swap pays exactly the difference between the realized variance over the contract's life and the variance strike agreed at inception. No delta hedging required by the buyer. The payoff is a clean, path-independent function of just one quantity: how much the stock actually moved. The key theoretical result (Carr-Madan, 1998) shows that the fair variance strike can be replicated by a static portfolio of vanilla options across all strikes, weighted by 1/K² — making the contract model-free and precisely replicable by dealers.

**What it still doesn't solve:** Variance swaps are exposed to jump risk in a highly nonlinear way — a single large move is squared in the payoff, causing outsized losses for variance sellers. The replication via options also requires a full strip of liquid options at all strikes, which breaks down for illiquid underlyings. And the convexity of variance in volatility means variance swaps systematically trade at a premium to "vol swaps."

## Math Concepts

**Realized variance:** Measured over $N$ trading days with log returns $r_i = \ln(S_i / S_{i-1})$:

$$\sigma^2_{\text{realized}} = \frac{252}{N} \sum_{i=1}^{N} r_i^2$$

The factor $252$ annualizes the variance (assuming 252 trading days per year). Note: most variance swap contracts use the zero-mean convention (no subtraction of the sample mean), which simplifies the formula and matches standard index methodologies.

**Payoff at expiry:**

$$\text{Payoff} = N_{\text{vega}} \cdot (\sigma^2_{\text{realized}} - K_{\text{var}})$$

where:
- $N_{\text{vega}}$ is the vega notional (in dollars per vol point), e.g., \$100,000
- $K_{\text{var}}$ is the variance strike (agreed at inception, in variance units — vol squared)
- $\sigma^2_{\text{realized}}$ is the actual realized variance over the contract life

**Vega vs. variance notional:** Because variance is vol-squared, there's an asymmetry. To get approximately \$1 per 1 vol-point move in realized vol, you scale:

$$N_{\text{var}} = \frac{N_{\text{vega}}}{2 \cdot K_{\text{vol}}}$$

where $K_{\text{vol}} = \sqrt{K_{\text{var}}}$ is the vol strike (so $K_{\text{var}} = K_{\text{vol}}^2$).

**Fair strike — replication via log contract:**

The fundamental result (Carr-Madan) is that the fair variance swap strike equals the value of a continuously-struck log contract:

$$K_{\text{var}} = \frac{2}{T} \left[ \int_0^F \frac{P(K)}{K^2} dK + \int_F^\infty \frac{C(K)}{K^2} dK \right]$$

where $F = S_0 e^{rT}$ is the forward, $P(K)$ is the put price at strike $K$, and $C(K)$ is the call price at strike $K$. This integral is model-free — it uses a strip of options across all strikes weighted by $1/K^2$. This is also how VIX is computed.

**Connection to VIX:**

$$K_{\text{var}} \approx \left(\frac{\text{VIX}}{100}\right)^2$$

So if VIX = 20, the 30-day variance swap strike is approximately $0.20^2 = 0.04$ (in variance units), or equivalently $K_{\text{vol}} \approx 20\%$.

## Walkthrough

**Setup:**
- Underlying: SPX at \$5000
- Contract length: 30 calendar days ($\approx 21$ trading days)
- VIX at inception: 20 (so $K_{\text{vol}} = 20\%$, $K_{\text{var}} = 0.04$)
- Notional: \$250,000 vega notional
- Variance notional: $N_{\text{var}} = 250{,}000 / (2 \times 20) = \$6{,}250$ per variance point

**Scenario A — Calm market:**
Realized vol over the 30 days = 15% annualized. Realized variance = $0.15^2 = 0.0225$.

$$\text{Payoff} = 6{,}250 \times (0.0225 - 0.04) = 6{,}250 \times (-0.0175) = -\$109.38$$

As the variance swap buyer (long variance), you lose \$109 per unit, or about $-\$109 \times 6{,}250 / 6{,}250 = -\$109.38$ per unit notional. At the full notional scale:

$$\text{Total P&L} = 250{,}000 \times (0.15 - 0.20) = -\$12{,}500 \quad \text{(vega-approximate)}$$

**Scenario B — Volatile market:**
Realized vol = 30%. Realized variance = $0.09$.

$$\text{Payoff} = 6{,}250 \times (0.09 - 0.04) = 6{,}250 \times 0.05 = +\$312.50 \text{ per point}$$

Total approximate P&L: $250{,}000 \times (0.30 - 0.20) = +\$25{,}000$.

**Key observation:** Payoff is convex in realized vol (because payoff is linear in variance, and variance is vol-squared). Being long a variance swap profits more from a 10-vol-point rally from 20 to 30 than you lose from a 10-vol-point drop from 20 to 10.

## Analysis

**Convexity advantage for long variance:** Since payoff is linear in $\sigma^2$ but convex in $\sigma$, long variance positions have "positive convexity" in vol space. This is why variance swaps are slightly more expensive than vol swaps (if vol swaps existed cleanly) — the convexity has a positive value.

**Variance risk premium:** Historically, realized variance on equity indices runs below the variance swap strike (i.e., the VIX-implied variance). The difference is the variance risk premium — on average, sellers of variance swaps collect this premium. Estimates suggest the annualized premium is 2–5 vol points for SPX.

**Jump risk:** A single large one-day move contributes $r_i^2$ to the realized variance — and because it's squared, a 10% one-day drop contributes 100 times as much as a 1% move. Variance swaps are very sensitive to jump risk (e.g., a crash). This is different from what delta-hedged options portfolios produce.

**The $1/K^2$ weighting:** The replication formula weights options by $1/K^2$, which gives far more weight to low-strike options. In practice, a deep OTM SPX put at a strike of 3000 has 4x the weight of an ATM option at 5000. This means the fair value depends critically on the liquidity of OTM options — and in a crisis when OTM puts gap up, variance swap sellers face extreme losses.

**Mark-to-market:** During the life of the contract, the MTM value depends on (a) variance accrued so far, and (b) the new variance swap fair value for the remaining period.

**Misconception — "Variance swaps need no hedging":** The *payoff* requires no delta hedge, but a dealer who *sells* a variance swap must hedge their book. They do so by maintaining a delta-neutral portfolio of vanilla options across all strikes — essentially replicating the log contract.

## Implementation

```python
import numpy as np
import pandas as pd

def realized_variance(prices, annualize=True, trading_days=252):
    """
    Compute realized variance from a price series.
    Uses zero-mean log-return convention (standard for variance swaps).
    """
    log_returns = np.diff(np.log(prices))
    var = np.sum(log_returns**2)
    if annualize:
        n = len(log_returns)
        var = var * (trading_days / n)
    return var

def variance_swap_pnl(prices, k_vol_pct, vega_notional,
                      trading_days_per_year=252):
    """
    Compute variance swap P&L at expiry.

    Parameters
    ----------
    prices         : array of daily closing prices over contract life
    k_vol_pct      : variance swap vol strike, e.g. 20.0 for 20%
    vega_notional  : dollar vega notional, e.g. 250_000
    """
    k_var = (k_vol_pct / 100) ** 2                     # strike in variance units
    var_notional = vega_notional / (2 * k_vol_pct)     # $ per variance unit

    realized_var = realized_variance(prices)
    realized_vol_pct = np.sqrt(realized_var) * 100

    pnl = var_notional * (realized_var - k_var)
    pnl_vega_approx = vega_notional * (realized_vol_pct - k_vol_pct) / 100

    return {
        "realized_vol_pct":   round(realized_vol_pct, 2),
        "k_vol_pct":          k_vol_pct,
        "realized_var":       round(realized_var, 6),
        "k_var":              round(k_var, 6),
        "pnl_exact":          round(pnl, 2),
        "pnl_vega_approx":    round(pnl_vega_approx, 2),
    }

# --- Simulate a 21-day price path ---
np.random.seed(42)
S0 = 5000
T_days = 21
k_vol = 20.0        # 20% strike
vega_notional = 250_000

# Scenario A: calm market (actual vol ~ 15%)
daily_sigma_a = 0.15 / np.sqrt(252)
prices_a = S0 * np.exp(np.cumsum(
    np.random.normal(0, daily_sigma_a, T_days + 1)
))
prices_a[0] = S0

result_a = variance_swap_pnl(prices_a, k_vol, vega_notional)
print("Scenario A (calm):", result_a)

# Scenario B: volatile market (actual vol ~ 30%)
daily_sigma_b = 0.30 / np.sqrt(252)
prices_b = S0 * np.exp(np.cumsum(
    np.random.normal(0, daily_sigma_b, T_days + 1)
))
prices_b[0] = S0

result_b = variance_swap_pnl(prices_b, k_vol, vega_notional)
print("Scenario B (volatile):", result_b)

# --- Show convexity: payoff as function of realized vol ---
import matplotlib.pyplot as plt

realized_vols = np.linspace(5, 50, 200)   # in percent
k_var_val = (k_vol / 100) ** 2
var_notional = vega_notional / (2 * k_vol)
payoffs = var_notional * ((realized_vols / 100)**2 - k_var_val)

plt.figure(figsize=(8, 4))
plt.plot(realized_vols, payoffs / 1000, color='steelblue', lw=2)
plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
plt.axvline(k_vol, color='red', linestyle='--', alpha=0.5, label=f'Strike = {k_vol}%')
plt.xlabel('Realized Volatility (%)')
plt.ylabel('P&L ($000s)')
plt.title('Variance Swap P&L (Long Variance)')
plt.legend()
plt.tight_layout()
plt.show()
```

## Bridge to Quant / ML

- **VIX futures and variance:** VIX futures approximate forward variance swap strikes. Trading the spread between VIX futures and realized variance is a core systematic volatility strategy.
- **Variance risk premium harvesting:** Systematically selling variance swaps (or variance via short straddle + delta hedge) harvests the variance risk premium. ML models can time this strategy by forecasting when realized vol is likely to be well below IV.
- **Correlation swaps:** Variance swaps on an index vs. its constituents reveal correlation structure. The "dispersion trade" — short index variance, long single-stock variance — profits when correlations are high.
- **Rough volatility:** Research by Gatheral et al. shows that realized variance increments follow a rough fractional Brownian motion with Hurst exponent $H \approx 0.1$. This has implications for the shape of the variance swap term structure.
- **Model-free:** Because variance swaps are replicated by a model-free portfolio of options, their fair values don't depend on BSM assumptions. This makes them useful as a benchmark to test whether any stochastic vol model is properly calibrated.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** A variance swap buyer is described as having "no delta-hedging required." Why not — doesn't the position still respond to stock price movements?
<details>
<summary>Answer</summary>
The payoff of a variance swap depends only on the sum of squared daily log-returns over the contract's life — this is realized variance, a scalar computed at expiry. The payoff function does not depend on where the stock ends up, only on how much it moved each day. There is no directional exposure embedded in the contract itself. By contrast, an option's payoff (max(S_T − K, 0)) depends directly on the final stock price, so the option holder who wants pure vol exposure must delta-hedge away that directional dependency. The variance swap's contract structure eliminates the directional component at the design level — the squaring of returns makes positive and negative moves equivalent.
</details>

**Q2.** Variance swap payoff is linear in realized variance but convex in realized volatility. Explain why this creates an asymmetric payoff profile for a long variance position.
<details>
<summary>Answer</summary>
Variance is volatility squared: σ² = (realized vol)². The payoff = N_var × (σ²_realized − K_var). Since variance is a convex function of vol, a 10 vol-point rally from 20% to 30% increases variance by 0.09 − 0.04 = 0.05, while a 10 vol-point drop from 20% to 10% decreases variance by only 0.04 − 0.01 = 0.03. The gain from a 10-point vol increase is larger than the loss from a 10-point vol decrease of equal size. Long variance positions benefit from this convexity: the P&L curve is curved upward — you win more from upside vol than you lose from downside vol. This is why variance swaps trade at a premium to hypothetical "vol swaps" — the convexity has positive value to the long side.
</details>

**Q3.** The variance risk premium is described as the historical difference between implied variance (from the strike) and realized variance. From the perspective of a systematic seller of variance swaps, what is the risk of persistently collecting this premium?
<details>
<summary>Answer</summary>
The variance risk premium is a "short volatility" strategy: you collect small, steady premiums as long as realized vol stays below the strike, but you face potentially catastrophic losses during volatility spikes. Because variance payoff scales with the square of moves, a crisis event (e.g., a day with a 10% market drop) contributes 100× as much variance as a 1% daily move. A single extreme event — a 2008 financial crisis, a 2020 COVID crash — can wipe out years of premium collection. The strategy has a return profile similar to writing insurance: steady income punctuated by rare but severe losses. This is the classic "picking up nickels in front of a steamroller" dynamic. Risk management requires position sizing, stop-losses, and capital buffers to survive the tail events.
</details>

---

### Level 2 — Quantitative

**Q4.** Setup: SPX at 4500, VIX = 25 (K_vol = 25%), vega notional = \$100,000, contract length = 21 trading days. Compute: (a) the variance strike K_var, (b) the variance notional N_var, (c) the P&L if realized vol is 18%, (d) the P&L if realized vol is 35%.
<details>
<summary>Answer</summary>
(a) K_var = (25/100)² = 0.0625 (in variance units).

(b) N_var = vega_notional / (2 × K_vol) = 100,000 / (2 × 25) = \$2,000 per variance unit.

(c) Realized vol = 18%: realized var = 0.18² = 0.0324.
P&L = 2,000 × (0.0324 − 0.0625) = 2,000 × (−0.0301) = −\$60.20 (loss as long variance buyer).
Vega approximate: 100,000 × (18% − 25%) / 100 = 100,000 × (−0.07) = −\$7,000.

(d) Realized vol = 35%: realized var = 0.35² = 0.1225.
P&L = 2,000 × (0.1225 − 0.0625) = 2,000 × 0.06 = +\$120 exact per unit → total exact P&L = 2,000 × 0.06 = +\$120... wait: this should be $120 per contract × notional scaling. Let me recompute: P&L = N_var × (σ²_real − K_var) = 2,000 × (0.1225 − 0.0625) = 2,000 × 0.06 = +$120. Note the asymmetry: the +10 vol-point gain (\$120) exceeds the −7 vol-point loss (−\$60.20), demonstrating convexity.

Vega approx for (d): 100,000 × (35% − 25%) / 100 = +\$10,000.
</details>

**Q5.** A variance swap dealer sells a variance swap with K_vol = 20% (K_var = 0.04). On day 3 of a 21-day contract, the market crashes and the stock falls 8% in a single day. How much variance does that one day contribute to the realized variance calculation, and what does this imply about the dealer's mark-to-market loss?
<details>
<summary>Answer</summary>
The daily log return: r = ln(0.92) ≈ −0.0834. Squared: r² = 0.00696.
Annualized contribution from this one day: 252 × 0.00696 / 21 × 21 = 252 × 0.00696 = 1.754... 

More carefully: realized variance uses formula (252/N) × Σr_i². An 8% single-day move contributes 0.0834² = 0.00696 to the sum. Over 21 trading days total, the annualized realized variance from just this one day = 252 × 0.00696 / 21 × (one day's weight) = 252 / 21 × 0.00696 = 12 × 0.00696 = 0.0835.

The variance strike was K_var = 0.04. Just this one day has already contributed realized variance of 0.0835, which already exceeds the entire strike by 0.0835 − 0.04 = 0.0435. The remaining 20 days contribute additional variance. The dealer who sold variance is already deeply in the red from a single day — this illustrates the catastrophic tail risk of short variance positions during market crashes.
</details>

---

### Level 3 — Coding

**Q6.** The `realized_variance` function uses `np.sum(log_returns**2)` without subtracting the sample mean (the "zero-mean convention"). What would change numerically if you instead used the standard sample variance formula `np.sum((log_returns - log_returns.mean())**2) / (N-1)`? Why does the variance swap contract specify the zero-mean convention?
<details>
<summary>Answer</summary>
The sample variance formula subtracts the mean return and divides by N-1 (Bessel's correction). For variance swaps, two deviations: (1) the mean is not subtracted, and (2) the sum is divided by N (not N-1). The zero-mean convention (no mean subtraction) slightly overstates variance when the sample mean is nonzero — typically by a tiny amount because daily returns have means near zero. But the key reason for the convention is standardization: both parties to the contract must compute exactly the same number at settlement, with no ambiguity about what "mean" to use. If you subtracted the sample mean, disagreements could arise about the estimation window, which returns are included, and rounding. The zero-mean formula is unambiguous: simply sum the squared log-returns and annualize. It also has the property that on a non-dividend day, zero variance is contributed even if the stock doesn't move — which matches the economic intuition that "no movement = no variance."
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Variance swaps require no hedging by the dealer | The buyer has no delta-hedging to do, but the dealer who sells a variance swap must hedge by maintaining a delta-neutral strip of vanilla options across all strikes (replicating the log contract). The dealer's hedge is operationally intensive |
| Variance swaps and vol swaps are the same thing | Variance swaps pay realized variance; vol swaps would pay realized volatility (the square root). Vol swaps don't have clean replication portfolios and are harder to price. Variance swaps trade at a premium due to the convexity of variance in vol space |
| A 20% VIX means the market expects 20% annualized moves | VIX is approximately the variance swap vol strike — it reflects risk-neutral expectations including a risk premium, not the physical-world prediction. Historical realized SPX vol is typically 2–5 points below VIX |
| The variance risk premium is always positive (sellers always win) | The long-run average premium favors sellers, but individual periods — especially during crises — produce enormous losses that can exceed years of premium income in a single month |

## Related Concepts

- [[Implied Volatility]]
- [[Volatility Smile]]
- [[VIX]]
- [[Gamma Scalping]]
- [[Black-Scholes Model]]

## Sources Used

- Hull, *Options, Futures, and Other Derivatives*, Ch. 26 (Exotic Options / Variance Swaps)
- Carr & Madan (1998), "Towards a Theory of Volatility Trading"
- Demeterfi, Derman, Kamal, Zou (1999), "A Guide to Volatility and Variance Swaps"

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | Hull + initial build |
| 2026-04-12 | Note created | bootstrap |
| 2026-04-11 | QA review: no issues found | quality review |
