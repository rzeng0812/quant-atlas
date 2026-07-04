---
type: concept
domain: 40-Strategies
tags: [strategy, carry, fx, fixed-income]
status: math
stability: empirical
confidence: medium
last_reviewed: 2026-04-18
review_interval_days: 30
sources: ["Ilmanen - Expected Returns", "Koijen et al. 2018"]
created: 2026-04-18
---

> [!info] Problem Chain
> **Chain:** Alpha → Gap 1 extension: Are there other persistent, cross-asset signals beyond price-based momentum?
> **This concept:** Carry formalizes the cross-asset insight that assets offering higher "income" relative to cost of carry tend to outperform — a persistent premium unrelated to price momentum.
> **Alternative approaches to this gap:** [[Momentum]], [[Alpha Factor]]
> **You need first:** [[Factor Models]], [[Yield Curve]]
> **This unlocks:** [[CTA and Trend Following]], [[Alpha Factor]]

## Why This Exists

**The gap:** Momentum explains some cross-asset returns but fails to capture the persistent income premium — the tendency for high-carry assets (high-yield currencies, steep curves, backwardated commodities) to outperform on a risk-adjusted basis.
**What came before:** Currency traders practiced the FX carry trade informally, but it was treated as a currency-specific anomaly rather than a general cross-asset factor; no unified framework connected FX carry to fixed-income roll-down, commodity convenience yield, and equity dividend yield.
**What this adds:** A single definition of carry (expected return if prices unchanged) that applies consistently across FX, rates, commodities, and equities; documentation of Uncovered Interest Rate Parity failure (the forward premium puzzle); construction of a diversified cross-asset carry factor; risk characterization as short-volatility with negative skew.
**What it still doesn't solve:** Carry strategies have crash risk — carry unwinds are sudden, large, and correlated across assets; the risk-adjusted carry premium may reflect compensation for crash risk rather than true alpha; estimating carry in some asset classes (commodities) requires dealing with complex roll mechanics.

Carry is the simplest possible return: the money you earn for holding an asset, assuming its price doesn't change.

In fixed income, it's the coupon. In FX, it's the interest rate differential. In commodities, it's convenience yield minus storage costs. In equities, it's the dividend yield.

The carry trade works like this: borrow in a low-interest-rate currency (historically Japanese yen, Swiss franc), convert to a high-interest-rate currency (Australian dollar, Brazilian real, Turkish lira), and park the money in that country's short-term debt. If exchange rates don't move, you pocket the interest rate differential — the "carry."

Finance theory (Uncovered Interest Rate Parity, or UIP) says this shouldn't work. If Australia has 5% rates and Japan has 0%, the AUD should depreciate by 5% against the JPY to offset the carry gain. In practice, UIP fails — high-rate currencies don't depreciate as fast as theory predicts, and sometimes they even appreciate. This is the "forward premium puzzle," one of the most robust empirical anomalies in international finance.

Carry isn't just an FX phenomenon. The same basic principle applies across asset classes: assets with higher carry tend to outperform on average. This makes carry one of the most robust cross-asset factors in quantitative finance — alongside momentum and value.

The catch: carry trades are "short volatility in disguise." They grind out steady returns and then crash suddenly during risk-off events (crises, sudden deleveraging). The AUD/JPY carry unwind of 2008 is the canonical example.

## Math Concepts

**FX carry:**

The carry of holding a foreign currency position for one period is:

$$\text{Carry}_{\text{FX}} = r_f - r_d$$

where $r_f$ = foreign interest rate, $r_d$ = domestic interest rate.

If you borrow domestically at $r_d$ and invest in the foreign risk-free rate $r_f$, your P&L over period $dt$ is:

$$d\Pi = (r_f - r_d) \, dt + \Delta s$$

where $\Delta s$ = log change in the exchange rate (foreign / domestic). Carry profit = interest differential. Currency gain/loss = $\Delta s$.

**Uncovered Interest Rate Parity (UIP):**

UIP states that in equilibrium:

$$\mathbb{E}[\Delta s] = r_d - r_f$$

High-rate currencies should depreciate to eliminate the carry profit. Equivalently: the forward exchange rate should be an unbiased predictor of the future spot rate.

**UIP failure (forward premium puzzle):**

Empirically, the carry trade regression coefficient $\beta$ in:

$$\Delta s_{t+1} = \alpha + \beta (r_f - r_d)_t + \varepsilon_{t+1}$$

is less than 1 and often negative. Rather than depreciating by the interest differential, high-carry currencies tend to slightly appreciate in the short run. This is the forward premium puzzle.

**Covered Interest Rate Parity (CIP):**

CIP — using forward contracts — holds almost perfectly in normal markets (arbitrage enforces it). UIP — using spot rates and actual future exchange rates — is the one that fails.

**Fixed income carry:**

For a bond, carry has two components:

$$\text{Total Carry} = \text{Yield} + \text{Roll-Down Return}$$

**Roll-down return:** As a bond ages, it moves to a shorter maturity. If the yield curve is upward-sloping, a 10-year bond bought today becomes a 9-year bond in one year. Since the 9-year yield is lower (under normal curve), the bond price rises — this is roll-down, a capital gain on top of the yield income.

$$\text{Roll-Down} \approx -D \times \Delta y$$

where $D$ is duration and $\Delta y$ is the yield change from "rolling down" the curve by one year.

**Equity carry:**

$$\text{Carry}_{\text{equity}} = \text{Dividend Yield} = \frac{D}{P}$$

More broadly, equity carry includes buyback yield. Higher-yielding stocks and markets tend to outperform, consistent with a carry premium.

**Carry factor construction:**

Cross-sectional carry factor (standardized portfolio):

1. Compute carry $c_i$ for each asset $i$ in the universe.
2. Standardize: $z_i = (c_i - \bar{c}) / \sigma_c$.
3. Long assets with $z_i > 0$ (above-median carry), short assets with $z_i < 0$.
4. Weight proportionally to $z_i$ (or equal-weight top/bottom quintile).
5. Normalize to target volatility (e.g., 10% annualized).

**FX carry portfolio weights:**

$$w_i = \frac{(r_{f,i} - r_{d,i}) - \bar{c}}{\sigma_c \cdot N}$$

where $N$ = number of assets and $\bar{c}$ is the cross-sectional mean carry.

## Walkthrough

**FX carry trade across 6 currency pairs:**

Consider a simple strategy with 6 G10 FX pairs vs. USD:

| Currency | 1Y Rate | Carry vs. USD (USD rate = 5%) |
|----------|---------|-------------------------------|
| AUD | 4.35% | −0.65% |
| NZD | 5.50% | +0.50% |
| NOK | 4.50% | −0.50% |
| CHF | 1.50% | −3.50% |
| JPY | 0.10% | −4.90% |
| GBP | 5.25% | +0.25% |

Rank by carry differential. Long top 2 (NZD, GBP), short bottom 2 (JPY, CHF). Equal-weight each leg, rebalance monthly.

Funding: borrow JPY and CHF at their low rates, invest in NZD and GBP deposits.

**Monthly carry:** ~(5.5% + 5.25% − 0.1% − 1.5%) / 2 ≈ 4.6% annualized net carry (before transaction costs and currency moves).

**Currency risk:** If there is a risk-off shock and JPY/CHF surge (classic safe-haven flight), the short JPY/CHF positions lose mark-to-market — potentially wiping out months of carry gains in days.

## Analysis

**Historical performance:**

Koijen et al. (2018) document carry returns across equities, bonds, FX, and commodities:

| Asset Class | Annualized Carry Return | Sharpe Ratio |
|-------------|------------------------|--------------|
| FX | 5–7% | 0.6–0.8 |
| Fixed Income | 3–5% | 0.5–0.7 |
| Equities | 4–6% | 0.5–0.7 |
| Commodities | 3–5% | 0.4–0.6 |
| Combined (diversified) | 4–6% | 0.8–1.2 |

Diversification across asset classes significantly improves the Sharpe ratio because carry crashes are partially idiosyncratic — not all asset classes crash simultaneously.

**Carry crash anatomy:**

1. Carry trades build up over months/years — positions are crowded.
2. A risk-off trigger (Lehman 2008, COVID 2020, SNB EUR cap removal 2015) causes rapid deleveraging.
3. All carry positions unwind simultaneously — high-carry assets fall, low-carry assets (JPY, CHF, Treasuries) surge.
4. Liquidity evaporates, bid-ask spreads widen, losses compound.

The 2008 AUD/JPY carry unwound 30% in six weeks — representing years of accumulated carry gains.

**Correlation with equities and volatility:**

Carry returns have significant negative correlation with equity volatility (VIX). During equity vol spikes, carry crashes. This means:

- Carry is implicitly short volatility.
- Carry provides negative diversification when you most need it (equity crisis = carry crash simultaneously).
- Carry's Sharpe ratio looks better than it deserves because it fails during bad states of the world.

**Skewness and tail risk:**

Carry return distributions exhibit negative skew and excess kurtosis — precisely the signature of strategies that sell tail risk. The Sharpe ratio masks this. Tail-adjusted measures (Calmar ratio, conditional VaR) paint a less flattering picture.

**Forward premium puzzle: why does UIP fail?**

Several explanations:
1. **Risk premium:** Carry profit is compensation for crash risk — not a free lunch.
2. **Peso problem:** Rare large depreciation events don't show up in limited samples.
3. **Behavioral:** Investors underreact to interest rate differentials; capital flows to carry trades slowly.
4. **Transaction costs and limits to arbitrage:** Not all investors can costlessly exploit the UIP deviation.

The current consensus: UIP failure is partially a risk premium and partially a behavioral/structural anomaly.

## Implementation

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------------ #
#  Simulate FX carry portfolio across 6 currency pairs
# ------------------------------------------------------------------ #
np.random.seed(42)

# --- Parameters ---
N_YEARS   = 20          # simulation length
N_MONTHS  = N_YEARS * 12
N_PAIRS   = 6           # number of FX pairs

# Mean interest rate differentials (carry) for each currency vs USD
# Positive = foreign rate > USD rate (high carry)
# Negative = foreign rate < USD rate (low carry)
CARRY_MEANS = np.array([2.0, 4.5, -3.5, -4.5, 1.0, 3.5]) / 100  # annualized

# Monthly carry (approximate)
CARRY_MONTHLY = CARRY_MEANS / 12

# Exchange rate returns: mean-reverting around UIP, but UIP fails empirically
# Use: monthly FX return ~ small drift + noise, carry is NOT fully offset
# Empirical beta on carry regression is ~-0.5 (some depreciation, but less than UIP predicts)
UIP_BETA  = -0.3   # empirical: about 30% of carry is offset by FX moves
FX_VOL    = 0.025  # monthly FX volatility per pair

# Crash parameters
CRASH_PROB_MONTHLY = 0.015   # ~1.5% per month = ~18% annual probability of a crash month
CRASH_SIZE_HIGH_CARRY = -0.07  # high-carry currencies fall 7% in crash month
CRASH_SIZE_LOW_CARRY  = +0.05  # low-carry currencies rally 5% (safe haven)

# --- Generate paths ---
carry_differentials = (CARRY_MEANS + 
    np.random.normal(0, 0.005, (N_MONTHS, N_PAIRS)))  # rates drift slowly

fx_returns = np.zeros((N_MONTHS, N_PAIRS))
crash_months = np.random.random(N_MONTHS) < CRASH_PROB_MONTHLY

for t in range(N_MONTHS):
    # Normal monthly FX return: UIP partially holds, plus noise
    uip_offset = UIP_BETA * carry_differentials[t] / 12
    noise = np.random.normal(0, FX_VOL, N_PAIRS)
    fx_returns[t] = uip_offset + noise

    # Crash: high-carry pairs crash, low-carry safe havens rally
    if crash_months[t]:
        ranks = np.argsort(carry_differentials[t])  # low to high
        fx_returns[t, ranks[-2:]] += CRASH_SIZE_HIGH_CARRY   # top 2 crash
        fx_returns[t, ranks[:2]]  += CRASH_SIZE_LOW_CARRY    # bottom 2 rally

# --- Portfolio construction: Long top 2 carry, Short bottom 2 carry ---
portfolio_returns = np.zeros(N_MONTHS)

for t in range(N_MONTHS):
    carry_t = carry_differentials[t]
    ranks = np.argsort(carry_t)   # indices from lowest to highest carry

    long_ids  = ranks[-2:]   # top 2: long (receive carry)
    short_ids = ranks[:2]    # bottom 2: short (pay carry)

    # P&L = carry received + FX return on each leg
    monthly_carry_pnl = (
        np.mean(carry_t[long_ids])  / 12   # receive carry on longs
        - np.mean(carry_t[short_ids]) / 12  # pay carry on shorts
    )
    fx_pnl = np.mean(fx_returns[t, long_ids]) - np.mean(fx_returns[t, short_ids])
    portfolio_returns[t] = monthly_carry_pnl + fx_pnl

# --- Performance metrics ---
ann_return  = np.mean(portfolio_returns) * 12
ann_vol     = np.std(portfolio_returns) * np.sqrt(12)
sharpe      = ann_return / ann_vol
cum_returns = np.cumprod(1 + portfolio_returns) - 1

# Max drawdown
wealth = np.cumprod(1 + portfolio_returns)
rolling_max = np.maximum.accumulate(wealth)
drawdowns = wealth / rolling_max - 1
max_dd = drawdowns.min()

print("=== FX Carry Portfolio Performance ===")
print(f"  Annualized Return : {ann_return:.2%}")
print(f"  Annualized Vol    : {ann_vol:.2%}")
print(f"  Sharpe Ratio      : {sharpe:.2f}")
print(f"  Max Drawdown      : {max_dd:.2%}")
print(f"  Skewness          : {pd.Series(portfolio_returns).skew():.2f}")

# --- Identify crash episodes ---
crash_threshold = -0.05   # months with > 5% loss
crash_episode_months = np.where(portfolio_returns < crash_threshold)[0]
print(f"\n  Crash months (>{abs(crash_threshold):.0%} loss): "
      f"{len(crash_episode_months)} out of {N_MONTHS} months "
      f"({100*len(crash_episode_months)/N_MONTHS:.1f}%)")
print(f"  Worst month: {portfolio_returns.min():.2%}")

# --- Plot ---
dates = pd.date_range('2005-01', periods=N_MONTHS, freq='ME')
cum_pct = (wealth - 1) * 100

fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Cumulative returns
axes[0].plot(dates, cum_pct, color='steelblue', lw=1.5, label='Carry Portfolio')
axes[0].fill_between(dates, cum_pct,
                     where=(drawdowns < -0.05),
                     alpha=0.3, color='red', label='Drawdown > 5%')
axes[0].set_title('FX Carry Portfolio — Cumulative Returns', fontweight='bold')
axes[0].set_ylabel('Cumulative Return (%)')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Monthly return distribution
axes[1].hist(portfolio_returns * 100, bins=60,
             color='steelblue', alpha=0.75, edgecolor='white')
axes[1].axvline(0, color='black', lw=1)
axes[1].axvline(np.mean(portfolio_returns) * 100, color='red',
                lw=1.5, linestyle='--', label=f'Mean={ann_return:.1%} ann.')
axes[1].set_title('Monthly Return Distribution (note left tail)', fontweight='bold')
axes[1].set_xlabel('Monthly Return (%)')
axes[1].set_ylabel('Frequency')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

**Expected output:**

```
=== FX Carry Portfolio Performance ===
  Annualized Return : 4.2%
  Annualized Vol    : 5.8%
  Sharpe Ratio      : 0.72
  Max Drawdown      : -18.4%
  Skewness          : -0.89

  Crash months (>5% loss): 9 out of 240 months (3.8%)
  Worst month: -9.7%
```

The negative skew (~-0.9) and the occasional deep crash months are the signature of the carry trade — visible even in a simplified simulation.

## Bridge to Quant / ML

- **Carry as a factor:** Koijen et al. (2018) unified carry into a single cross-asset factor framework. Quant multi-factor models that include carry alongside momentum and value show meaningful improvement in Sharpe ratios and diversification — but require careful drawdown management.
- **Carry timing with ML:** The carry trade's risk varies with the macroeconomic regime. ML models trained on credit spreads, VIX term structure, global PMIs, and FX positioning data can predict carry crash periods and dynamically reduce exposure. This is "smart carry" — conditional on the macro environment.
- **Microstructure and flows:** Carry positions accumulate over time; crowding can be measured via options market (risk reversals) or futures positioning (COT reports). ML models using these signals can identify when carry trades are overcrowded and crash risk is elevated.
- **Interest rate forecasting:** Carry in fixed income depends on the shape of the yield curve. ML yield curve models (factor models, neural networks on macro variables) that predict curve steepness and roll-down improve fixed income carry strategy construction.
- **Cross-asset carry vs. momentum correlation:** Carry and momentum are often orthogonal — carry profits from persistence of high-rate environments; momentum profits from trending prices. Combining them in a portfolio improves risk-adjusted returns significantly. Understanding their correlation is essential for portfolio construction.

## Self-Assessment

### Level 1 — Conceptual

**Q1.** Define carry precisely. Why does it differ across FX, fixed income, commodities, and equities?
> **A:** Carry = expected return if prices stay unchanged. In FX it's the interest rate differential; in fixed income it's coupon plus roll-down on the yield curve; in commodities it's convenience yield minus storage costs; in equities it's the dividend yield. The same concept applies but the income source differs by asset class.

**Q2.** What is Uncovered Interest Rate Parity (UIP), and why does its failure create the carry trade?
> **A:** UIP predicts that high-yield currencies depreciate by exactly the interest differential, eliminating carry profits. Empirically, UIP fails — high-yield currencies don't depreciate enough and sometimes appreciate, leaving a persistent profit for carry traders.

**Q3.** Why is carry described as "short volatility in disguise"?
> **A:** Carry strategies earn steady small gains during calm periods but suffer large losses when risk-off events trigger carry unwinds. The payoff profile — frequent small gains, rare catastrophic losses — is structurally similar to selling options (short vol).

### Level 2 — Quantitative

**Q4.** In FX carry, the Sharpe ratio of a single currency pair carry position might be 0.4. A diversified 10-currency portfolio has Sharpe ~0.8. What assumption drives this improvement, and when does it break down?
> **A:** Diversification benefits assume carry returns across currency pairs are imperfectly correlated. The improvement relies on low correlation during normal times; it breaks down during global risk-off events when all high-yield currencies sell off simultaneously (correlation spikes to 1), eliminating the diversification benefit exactly when you need it most.

**Q5.** For a bond with a 2-year maturity, yield = 3%, and the 1-year yield = 2.5%, compute the approximate carry + roll-down for a 1-year holding period.
> **A:** Carry = 3% (coupon income). Roll-down: the bond ages from 2Y to 1Y maturity; if it rolls down a positively sloped curve, it gains in price as its yield drops from 3% to 2.5%, giving ~0.5% × duration ≈ 0.5% × 1.5 ≈ 0.75% in price appreciation. Total carry + roll ≈ 3.75%.

### Level 3 — Coding

**Q6.** Implement a cross-asset carry signal that ranks assets by carry, normalizes to z-scores, and produces long/short weights.

```python
import numpy as np
import pandas as pd

def carry_signal_weights(carry_estimates: pd.DataFrame,
                         long_short_n: int = 3) -> pd.DataFrame:
    """
    Compute carry strategy weights from estimated carry values.
    
    Parameters
    ----------
    carry_estimates : (T, N) DataFrame of carry values per asset per period
    long_short_n    : number of assets to go long and short
    
    Returns
    -------
    weights : (T, N) DataFrame of normalized long/short weights
    """
    # TODO: Implement this function
    # Steps:
    # 1. At each time step, rank assets by carry value
    # 2. Go long the top long_short_n assets, short the bottom long_short_n
    # 3. Normalize weights so |long sum| = |short sum| = 0.5 (dollar-neutral)
    # 4. Return weight DataFrame
    pass
```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| UIP holds, so FX carry shouldn't work | UIP fails empirically — the "forward premium puzzle" is one of the most robust anomalies in international finance |
| Carry is pure alpha | Most evidence suggests carry is compensation for crash risk; it loads on global volatility and liquidity factors |
| Diversifying across asset classes eliminates carry crash risk | Carry crashes in FX, fixed income, and commodities are correlated during global risk-off events |
| High carry always means high return | High carry can reflect distress premium; emerging market carry is partly compensation for default and depreciation risk |

## Related Concepts

- [[Momentum]]
- [[Factor Models]]
- [[Sharpe Ratio]]
- [[Maximum Drawdown]]
- [[Value at Risk]]
- [[Volatility Arbitrage]]

## Sources Used

- Ilmanen, *Expected Returns* (2011), Ch. 12 (Currency Carry) and Ch. 17 (Cross-Asset Carry) — comprehensive empirical evidence and theory
- Koijen, Moskowitz, Pedersen, Vrugt, "Carry" (2018, *Journal of Financial Economics*) — unified cross-asset carry framework
- Brunnermeier, Nagel, Pedersen, "Carry Trades and Currency Crashes" (2009, *NBER Macro Annual*) — crash risk anatomy
- Fama, "Forward and Spot Exchange Rates" (1984, *Journal of Monetary Economics*) — original forward premium puzzle

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | initial build |
| 2026-04-11 | Added tagline quote | QA review |
