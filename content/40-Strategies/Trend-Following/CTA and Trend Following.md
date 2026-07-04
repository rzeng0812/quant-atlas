---
type: concept
domain: 40-Strategies
tags: [strategy, trend-following, cta, momentum]
status: math
stability: empirical
confidence: medium
last_reviewed: 2026-04-18
review_interval_days: 30
sources:
  - "Lempérière et al. - Two Centuries of Trend Following (2014)"
  - "Hurst, Ooi & Pedersen - A Century of Evidence on Trend-Following Investing (AQR, 2017)"
  - "Ilmanen - Expected Returns (2011)"
created: 2026-04-18
---

> [!info] Problem Chain
> **Chain:** Alpha → Gap 1: Is there any evidence of persistent, tradeable patterns?
> **This concept:** CTA / trend following applies the momentum insight time-series and cross-asset — rather than ranking stocks against each other, it asks whether each individual instrument is trending and sizes positions accordingly across 50–100 futures markets.
> **Alternative approaches to this gap:** [[Momentum]], [[Carry Strategies]]
> **You need first:** [[Momentum]], [[Sharpe Ratio]]
> **This unlocks:** [[Alpha Factor]], [[Regime Detection]]

## Why This Exists

**The gap:** Equity momentum (cross-sectional) requires a large investable stock universe and is difficult to apply to macro asset classes like currencies, bonds, and commodities; a time-series framework was needed for systematic macro trading.
**What came before:** Discretionary macro trading by commodity trading advisors — rules-of-thumb, chart reading, and intuition applied across futures markets without a systematic, replicable framework.
**What this adds:** Time-series momentum signal (TSMOM): each instrument's recent return vs. its own history determines position direction and size; risk-parity position sizing equalizes volatility contribution across instruments; cross-asset diversification over 50–100 uncorrelated futures provides the portfolio edge; the strategy has documented positive convexity (positive returns in equity tail events).
**What it still doesn't solve:** Performance in the 2010s was poor as macro trends shortened; the strategy suffers in range-bound, choppy markets where trends reverse before positions can profit; crowding among CTAs means trend reversals increasingly hurt multiple funds simultaneously.

CTA stands for Commodity Trading Advisor — a legal designation from U.S. futures regulation. But in practice, when quants say "CTA," they mean something specific: a systematic, diversified, trend-following hedge fund that trades futures across every major asset class.

The core bet is simple to state: **prices that have been going up tend to keep going up; prices that have been going down tend to keep going down.** Buy the winners, short the losers — not in a single asset class, but simultaneously across equity indices, government bonds, currencies, and commodities. When one market trends sideways, others are trending strongly. The portfolio effect is where the strategy earns its keep.

This is critically different from the momentum factor you see in equity factor investing. Equity momentum (Jegadeesh-Titman) is *cross-sectional*: rank all stocks by their past 12-month return, go long the top decile, short the bottom decile. CTA trend following is *time-series*: for each instrument independently, compare today's price to some moving average and go long or short based on whether you're above or below it. Each instrument is evaluated on its own history, not ranked against other instruments.

Why does it work? Behavioral finance offers several explanations:
- **Anchoring and under-reaction:** Investors are slow to update beliefs; prices undershoot initially and then drift toward fair value over months.
- **Herding:** Institutional flows create momentum as fund managers pile into winning trades.
- **Risk premia:** Trend-following funds provide liquidity and absorb crash risk during dislocations; the premium is compensation for this service.

What makes CTAs special beyond the signal itself is the **diversification**: trading 50–100 uncorrelated futures markets means individual positions are small. The strategy earns its edge from the aggregate, not any single trade. An equity manager might know one sector extremely well; a CTA doesn't need to — it applies the same signal everywhere and collects the diversification premium.

**Crisis alpha.** CTAs have a remarkable property: they tend to make money during severe equity bear markets. In 2008, many CTAs were up 15–25% while equity markets fell 40%+. The mechanism: as equity markets begin trending down and bonds trend up (flight to quality), CTAs go short equities and long bonds — often before the crisis is recognized. This property makes CTAs natural portfolio insurance for equity-heavy investors.

## Math Concepts

**Time-series momentum signal.** For instrument $i$, the raw trend signal at time $t$ over lookback $T$:

$$r_{t,T}^i = \frac{P_t^i}{P_{t-T}^i} - 1$$

The position is determined by the sign and magnitude of this signal:

$$\text{position}_{t}^i = \text{sign}(r_{t,T}^i) \cdot \frac{\sigma_{\text{target}}}{\hat{\sigma}_t^i}$$

where $\hat{\sigma}_t^i$ is the estimated annualized daily return volatility of instrument $i$ at time $t$, and $\sigma_{\text{target}}$ is the target per-instrument annualized volatility (typically 15–25% for individual positions).

**Volatility targeting.** This is the defining feature that separates modern CTAs from naive systems. Rather than allocating a fixed dollar amount per instrument, the position is scaled so each instrument contributes a constant *risk* to the portfolio. If bonds are 3x less volatile than equities, you hold 3x more bond contracts.

The volatility estimate is typically an EWMA (Exponentially Weighted Moving Average):

$$\hat{\sigma}_t^2 = (1 - \lambda)\hat{\sigma}_{t-1}^2 + \lambda (r_t - \bar{r})^2$$

with $\lambda = 0.06$ corresponding to approximately a 32-day half-life.

**EWMA crossover signal.** Many CTAs use a moving average crossover rather than raw momentum:

$$\text{signal}_t^i = \text{EWMA}_{\text{slow}}(P_t^i) - \text{EWMA}_{\text{fast}}(P_t^i)$$

Long when price is above its slow moving average (fast > slow implies uptrend), short when below. The crossover provides a smoother entry/exit than pure lookback momentum.

**Portfolio construction.** With $N$ instruments, portfolio volatility $\sigma_P$ is:

$$\sigma_P^2 = \mathbf{w}^T \mathbf{\Sigma} \mathbf{w}$$

where $\mathbf{w}$ is the vector of position weights (already vol-targeted per instrument) and $\mathbf{\Sigma}$ is the covariance matrix of instrument returns. If correlations between instruments are low (the diversification assumption), vol-targeted individual weights produce a portfolio whose total volatility scales as:

$$\sigma_P \approx \sigma_{\text{target}} / \sqrt{N}$$

With $N = 100$ and $\sigma_{\text{target}} = 20\%$ per instrument, portfolio vol $\approx 2\%$ per instrument contribution. Leverage is then applied to bring total portfolio to a target (e.g., 15% annualized vol).

**Sharpe decomposition.** The portfolio Sharpe ratio exceeds individual instrument Sharpe ratios due to diversification:

$$\text{SR}_{\text{portfolio}} \approx \text{SR}_{\text{instrument}} \cdot \sqrt{N \cdot (1 - \bar{\rho})}$$

where $\bar{\rho}$ is the average pairwise correlation. For $N = 50$, $\bar{\rho} = 0.05$: portfolio SR $\approx 6.9 \times \text{SR}_{\text{instrument}}$.

**Fees.** Standard CTA fee structure: 2% management fee + 20% performance fee (the "2 and 20" model). Over long periods, gross SR of $\sim$1.0 becomes net SR of $\sim$0.6 after fees.

## Walkthrough

**Step-by-step: building a simple CTA on 4 asset classes.**

Suppose we have monthly returns for 4 instruments: S&P 500 futures (equity), 10-year T-note futures (bonds), EUR/USD futures (FX), and crude oil futures (commodity).

**Step 1 — Compute 12-month momentum signal.** For each instrument, compute $r_{t,12m}$ = return over prior 12 months. In January 2008, suppose:
- Equity: $r = +3\%$ (mildly positive — long)
- Bonds: $r = +8\%$ (positive — long)
- FX (EUR/USD): $r = +12\%$ (positive — long USD short EUR? Actually long EUR/USD means EUR strengthening)
- Crude oil: $r = +55\%$ (strongly positive — long)

**Step 2 — Estimate volatility.** Compute EWMA vol for each instrument over the prior 60 days. Suppose annualized vols: equity 15%, bonds 5%, FX 8%, crude 25%.

**Step 3 — Size positions.** Target per-instrument vol of 20%:
- Equity: $0.20 / 0.15 = 1.33 \times$ leverage
- Bonds: $0.20 / 0.05 = 4.0 \times$ leverage (bonds need lots of leverage to contribute the same risk as equities)
- FX: $0.20 / 0.08 = 2.5 \times$
- Crude: $0.20 / 0.25 = 0.8 \times$

**Step 4 — Apply sign.** All signals are positive, so all positions are long. In 2008, by September this would have shifted: equity signal turns negative (short), bonds remain long. CTA is now naturally positioned as the crisis unfolds.

**Step 5 — Monitor portfolio vol.** Because equity and bonds have low correlation (often negative), the diversified portfolio vol is far below the sum of individual contributions.

## Analysis

**Historical performance.** CTAs have strong empirical evidence going back to 1880 (Lempérière et al., 2014), before futures markets even existed (using spot prices for commodities and currencies). A diversified trend-following strategy produced consistent Sharpe ratios of 0.5–0.8 per year. During 2000–2020, top CTA managers (Man AHL, Winton, Chesapeake) ran net Sharpes of 0.4–0.7.

**Crisis alpha (key differentiator):**

| Period | Equity market | Typical CTA |
|--------|--------------|-------------|
| 2000–2002 (dot-com) | -50% | +20% to +40% |
| 2008 (financial crisis) | -55% | +15% to +30% |
| 2020 (COVID) | -34% then recover | +5% to +15% |
| 2022 (rates + equity) | -20% (equity), -16% (bonds) | +20% to +30% |

**Whipsaw risk.** The primary failure mode. Trend following loses money in choppy, mean-reverting markets. 2009–2011 was painful for CTAs as every incipient trend reversed before they could profit. Choppy markets generate repeated false signals: buy high, sell low, repeatedly. The cost of whipsaw is the "price of admission" for crisis alpha — you must pay in quiet markets to collect in trending ones.

**Crowding.** Large CTAs hold similar positions (everyone is long the same trending markets). This creates risk: when a trend reverses, simultaneous exits by many funds amplify the drawdown. August 2007 "quant quake" and certain 2019 CTA drawdowns reflect crowding-driven unwinds.

**Capacity.** Very high — CTA trades the most liquid futures markets in the world. \$10B+ managers face limited market impact. This is a meaningful advantage over smaller-cap equity strategies.

**Strengths vs. weaknesses:**

| Dimension | Assessment |
|-----------|-----------|
| Evidence base | 200+ years of backtest data across global markets |
| Crisis alpha | Consistent; structural to the strategy |
| Capacity | Very high (liquid futures only) |
| Transparency | Relatively transparent; rules-based |
| Whipsaw losses | Unavoidable; typically 1–3 year drawdown periods |
| Crowding | Growing concern as CTA AUM has scaled |
| Fee drag | 2&20 structure meaningful over long horizons |

## Implementation

```python
import numpy as np
import pandas as pd

np.random.seed(42)

# ── 1. Simulate returns for 4 asset classes ────────────────────────────────
# Simple correlated returns with embedded trend structure
T = 240  # 20 years of monthly returns
n_assets = 4
asset_names = ["Equity", "Bonds", "FX", "Commodity"]

# Create trending regimes: asset returns have autocorrelation (persistent trends)
autocorr = 0.15  # monthly autocorrelation of returns
vols = np.array([0.04, 0.015, 0.025, 0.06])  # monthly vols

# Correlation matrix (diversified: low cross-asset correlations)
corr_matrix = np.array([
    [1.00, -0.20,  0.10,  0.20],
    [-0.20,  1.00, -0.10, -0.15],
    [ 0.10, -0.10,  1.00,  0.05],
    [ 0.20, -0.15,  0.05,  1.00],
])
cov_matrix = np.outer(vols, vols) * corr_matrix
L = np.linalg.cholesky(cov_matrix)

raw_shocks = np.random.randn(T, n_assets)
iid_returns = raw_shocks @ L.T

# Add autocorrelation to simulate trending behavior
returns = np.empty_like(iid_returns)
returns[0] = iid_returns[0]
for t in range(1, T):
    returns[t] = autocorr * returns[t-1] + np.sqrt(1 - autocorr**2) * iid_returns[t]

# Add mean drift (equity/commodity positive expected return)
drifts = np.array([0.007, 0.003, 0.001, 0.004])  # monthly
returns += drifts[np.newaxis, :]

# ── 2. Compute trend signals (12-month lookback) ───────────────────────────
lookback = 12  # months

def compute_momentum_signal(returns: np.ndarray, lookback: int) -> np.ndarray:
    """Returns sign of trailing 12-month return (+1 long, -1 short)."""
    T, N = returns.shape
    signals = np.zeros((T, N))
    prices  = np.cumprod(1 + returns, axis=0)
    for t in range(lookback, T):
        r_12m = prices[t] / prices[t - lookback] - 1
        signals[t] = np.sign(r_12m)
    return signals

signals = compute_momentum_signal(returns, lookback)

# ── 3. Volatility targeting ────────────────────────────────────────────────
vol_target_per_asset = 0.20 / np.sqrt(12)  # 20% annualized per asset → monthly

def compute_ewma_vol(returns: np.ndarray, halflife: int = 3) -> np.ndarray:
    """Monthly EWMA volatility with given halflife in months."""
    lam = 1 - np.exp(-np.log(2) / halflife)
    T, N = returns.shape
    vol = np.zeros((T, N))
    vol[0] = np.abs(returns[0])
    for t in range(1, T):
        vol[t] = np.sqrt((1 - lam) * vol[t-1]**2 + lam * returns[t]**2)
    return np.maximum(vol, 1e-6)

ewma_vol = compute_ewma_vol(returns, halflife=3)

# Position = signal × (target_vol / estimated_vol)
positions = signals * (vol_target_per_asset / ewma_vol)

# ── 4. Portfolio returns ───────────────────────────────────────────────────
# Equal weight across assets (positions already vol-targeted)
# Portfolio return at t = sum of position[t-1] * return[t]
port_returns = np.sum(np.roll(positions, 1, axis=0) * returns, axis=1)
port_returns[:lookback+1] = 0  # no signal in warmup

# Buy-and-hold benchmarks
bh_returns = returns.mean(axis=1)  # equal-weight buy-and-hold

# Individual asset CTA (single instrument)
asset_cta = {asset_names[i]: np.roll(positions[:, i], 1) * returns[:, i] for i in range(n_assets)}

# ── 5. Performance metrics ─────────────────────────────────────────────────
def annualized_sharpe(rets: np.ndarray, periods_per_year: int = 12) -> float:
    r = rets[lookback+1:]
    return float(r.mean() / r.std() * np.sqrt(periods_per_year))

def max_drawdown(rets: np.ndarray) -> float:
    cum = np.cumprod(1 + rets)
    peak = np.maximum.accumulate(cum)
    dd   = (cum - peak) / peak
    return float(dd.min())

print("=== CTA Performance Summary ===")
print(f"{'Strategy':<20} {'Ann.Sharpe':>10} {'Max DD':>10}")
print("-" * 42)
print(f"{'CTA Portfolio':<20} {annualized_sharpe(port_returns):>10.2f} {max_drawdown(port_returns[lookback+1:]):>10.2%}")
print(f"{'Buy-and-Hold':<20} {annualized_sharpe(bh_returns):>10.2f} {max_drawdown(bh_returns[lookback+1:]):>10.2%}")
for name, r in asset_cta.items():
    print(f"{'CTA '+name:<20} {annualized_sharpe(r):>10.2f} {max_drawdown(r[lookback+1:]):>10.2%}")

# ── 6. Crisis alpha illustration ───────────────────────────────────────────
# Simulate an equity bear market: override equity returns months 100-115
crisis_returns = returns.copy()
crisis_returns[100:116, 0] = -0.06  # equity down 6%/month for 16 months → ~60% drawdown
crisis_signals  = compute_momentum_signal(crisis_returns, lookback)
crisis_vol      = compute_ewma_vol(crisis_returns)
crisis_positions = crisis_signals * (vol_target_per_asset / crisis_vol)
crisis_port     = np.sum(np.roll(crisis_positions, 1, axis=0) * crisis_returns, axis=1)
crisis_equity   = crisis_returns[:, 0]

cum_cta_crisis    = np.cumprod(1 + crisis_port[lookback:])
cum_equity_crisis = np.cumprod(1 + crisis_equity[lookback:])

print(f"\nCrisis period (months 100-116):")
print(f"  Equity cumulative return: {cum_equity_crisis[100-lookback:116-lookback][-1]-1:.2%}")
print(f"  CTA portfolio cumulative: {cum_cta_crisis[100-lookback:116-lookback][-1]-1:.2%}")
# CTA should be positive (shorts equity, long bonds) while equity is deeply negative
```

## Bridge to Quant / ML

**ML applied to trend following.** The core signal (moving average crossover, momentum sign) is simple and robust. But ML is applied at the margins:
- **Feature engineering:** Combining short, medium, and long lookback signals with ML weights (gradient boosted trees trained to predict optimal signal combination).
- **Regime-conditioned sizing:** Train a classifier to identify trending vs. choppy regimes, then scale positions down in choppy regimes to reduce whipsaw losses.
- **Signal blending:** Combine price-based trend with alternative signals (carry, value) using ML meta-models.

**Behavioral links.** CTA trend following is one of the most academically studied strategies. Moskowitz, Ooi & Pedersen (2012) showed time-series momentum has a Sharpe of ~1.0 after costs across 55 instruments from 1985–2012. The strategy is robust to parameter choices — nearly any reasonable lookback (1–12 months) and any reasonable vol targeting scheme produces similar risk-adjusted returns.

**Connection to options.** A long trend-following position has a convex payoff profile reminiscent of a long straddle: it makes money when markets move strongly in *either* direction. This is why it tends to perform during crises — large directional moves are exactly what it profits from. The cost of admission is the premium lost during mean-reverting periods, analogous to theta decay on an options position.

## Self-Assessment

### Level 1 — Conceptual

**Q1.** What is the difference between cross-sectional momentum (Jegadeesh-Titman) and time-series momentum (CTA)?
> **A:** Cross-sectional momentum ranks assets against each other and longs top/shorts bottom; time-series momentum evaluates each asset independently against its own history, going long if it's trending up and short if trending down regardless of how other assets are performing.

**Q2.** Why is diversification across 50–100 futures markets central to the CTA edge rather than a nice-to-have?
> **A:** Any single market may not trend for months; diversification ensures that while some markets chop, others are trending strongly. The Sharpe ratio comes from aggregating many individually weak but uncorrelated signals — the portfolio effect is where the strategy earns its keep.

**Q3.** Why do CTAs tend to perform well during equity market crashes?
> **A:** Crashes involve large, sustained directional moves — exactly what trend following profits from. CTAs hold short equity positions as markets fall, and they often have long bond positions as bonds rally in flight-to-safety. The convex payoff (large gains in trending disasters) is the reason CTAs are called "crisis alpha."

### Level 2 — Quantitative

**Q4.** A CTA trades 60 futures markets each scaled to 1% annualized volatility contribution. If average pairwise correlation between positions is 0.05, what is the approximate annualized portfolio volatility?
> **A:** Portfolio variance = N × σ² + N(N-1) × ρ × σ² = 60 × 0.01² + 60×59 × 0.05 × 0.01² ≈ 0.006 + 0.1770 = 0.183%; portfolio vol ≈ √(0.00183) ≈ 4.3%. Low individual position sizes + low correlations produce a portfolio vol much lower than naive N × 1% = 60%.

**Q5.** The time-series momentum signal for a single instrument is sign(r_{t-12,t-1}) × (1/σ_t). Why is the volatility scaling term 1/σ_t included?
> **A:** Without vol scaling, high-volatility markets would dominate the portfolio. Dividing by realized volatility equalizes each position's risk contribution regardless of the instrument's inherent vol, implementing risk-parity sizing within the trend signal.

### Level 3 — Coding

**Q6.** Implement a simple time-series momentum strategy: for each instrument, compute the sign of the trailing 12-month return, scale position by inverse volatility, and compute portfolio returns.

```python
import numpy as np
import pandas as pd

def tsmom_positions(prices: pd.DataFrame, lookback: int = 252,
                    vol_window: int = 60, target_vol: float = 0.01) -> pd.DataFrame:
    """
    Compute time-series momentum positions scaled by volatility.
    
    Parameters
    ----------
    prices      : (T, N) DataFrame of asset prices
    lookback    : lookback window for trend signal (in trading days)
    vol_window  : window for realized volatility estimation
    target_vol  : target annualized volatility per position
    
    Returns
    -------
    positions : (T, N) DataFrame of scaled position sizes
    """
    # TODO: Implement this function
    # Steps:
    # 1. Compute log returns from prices
    # 2. Compute trailing lookback-day return for the trend signal
    # 3. Compute rolling vol_window-day realized vol (annualized)
    # 4. Position = sign(trend) × (target_vol / realized_vol)
    # 5. Return positions (NaN where insufficient history)
    pass
```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| CTA is the same as equity momentum | CTA is time-series (each vs. its own history); equity momentum is cross-sectional (ranking stocks against each other) |
| Diversification across markets eliminates trend-following risk | Correlation spikes during trend reversals; diversification helps in normal times but not during whipsaws |
| CTA is "always long volatility" | CTAs benefit from *trending* volatility events but suffer in sudden mean-reverting spikes; they are long convexity, not short-vol sellers |
| Past trend-following performance guarantees future returns | The strategy has faced headwinds as macro trends shortened in 2010s; capacity constraints and crowding are real risks |

## Related Concepts

- [[Momentum]] — the underlying market anomaly that CTA exploits
- [[Mean Reversion]] — the opposing force; what kills CTA in choppy markets
- [[Sharpe Ratio]] — the primary performance metric; portfolio diversification boosts it
- [[Maximum Drawdown]] — whipsaw risk creates significant drawdowns
- [[Factor Models]] — CTA returns can be partially explained by trend factor
- [[Carry Strategies]] — a complementary strategy that performs when trend struggles
- [[Statistical Arbitrage]] — a mean-reversion counterpart to trend following

## Sources Used

- Lempérière, Y., Deremble, C., Seager, P., Potters, M., & Bouchaud, J. P. (2014). Two centuries of trend following. *Journal of Investment Strategies*, 3(3), 41–61
- Hurst, B., Ooi, Y. H., & Pedersen, L. H. (2017). *A Century of Evidence on Trend-Following Investing*. AQR Capital Management
- Moskowitz, T., Ooi, Y. H., & Pedersen, L. H. (2012). Time series momentum. *Journal of Financial Economics*, 104(2), 228–250
- Ilmanen, A. (2011). *Expected Returns: An Investor's Guide to Harvesting Market Rewards*. Wiley. Ch. 13
- Greyserman, A., & Kaminski, K. (2014). *Trend Following with Managed Futures*. Wiley

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | initial build |
