---
type: concept
domain: 20-Markets
tags: [volatility, options]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-12
review_interval_days: 365
sources:
  - "Hull ch.20"
created: 2026-04-12
---

> U-shape of IV vs strike; fat tails / skew in real distributions

> [!info] Problem Chain
> **Chain:** Pricing → Gap 5: BSM assumes constant σ — real markets show a volatility smile
> **This concept:** Documents the empirical failure of BSM's constant-vol assumption by showing that market-observed implied volatility varies systematically with strike — providing the ground truth that any improved model must reproduce.
> **Alternative approaches to this gap:** [[Implied Volatility]] (the measurement tool), [[Local Volatility]] (deterministic fix), [[Heston Model]] (stochastic vol fix), [[Merton Jump-Diffusion]] (jump-based fix)
> **You need first:** [[Implied Volatility]], [[Black-Scholes Model]], [[Option Greeks]]
> **This unlocks:** [[Volatility Surface]], [[Local Volatility]], [[Heston Model]], [[Variance Swap]], [[Exotic Options]]

## Why This Exists

**The gap:** BSM produces a single option price for a given volatility. But when traders started backing out the implied vol from market prices at different strikes, they found something disturbing: the implied vol was not the same across strikes. Out-of-the-money puts had higher implied vol than at-the-money options. The model was systematically, consistently wrong in a structured way.

**What came before:** Before the 1987 crash, the volatility surface was actually flatter — closer to BSM's prediction. After October 1987 (Black Monday), the equity market crashed 22% in a single day. The options market was permanently repriced: out-of-the-money puts became permanently more expensive as crash insurance demand surged. The flat smile assumption was broken and never recovered.

**What this adds:** The volatility smile (or skew for equities) is the empirical fact that must be explained. It encodes information about the real distribution of stock returns: the steepness of the left wing tells you how much fat-tail risk is priced in relative to lognormal. The smile is not just an academic curiosity — it directly affects the price of any exotic option, the correct delta for vanilla options, and the calibration target for every advanced pricing model.

**What it still doesn't solve:** Documenting the smile does not explain it or model it. The smile changes over time, has its own dynamics, and behaves differently under stress. Three families of models — local vol, stochastic vol, and jump-diffusion — each give different explanations and different predictions for how the smile will evolve when the stock moves.

## Math Concepts

**BSM assumption:** Under BSM, all options on the same underlying with the same expiry should share a single $\sigma$. The IV surface would be perfectly flat.

**Empirical reality:** Define the IV at strike $K$ and expiry $T$ as $\sigma_{\text{IV}}(K, T)$. In practice this is a non-constant surface.

**Moneyness parameterization:** Instead of raw strike $K$, traders often parameterize by log-moneyness:

$$m = \ln(K / F)$$

where $F = S e^{rT}$ is the forward price. At-the-money forward corresponds to $m = 0$.

**Risk-neutral density connection:** The shape of the smile encodes the market-implied probability distribution of the stock price at expiry. By the Breeden-Litzenberger formula, the risk-neutral PDF $q(K)$ is recovered from the call price surface:

$$q(K) = e^{rT} \frac{\partial^2 C}{\partial K^2}$$

A steeper skew (higher IV for low strikes) corresponds to a distribution with a fatter left tail than lognormal.

**Skew (Risk Reversal):** For equities, the standard measure of skew is:

$$\text{Skew} = \sigma_{\text{IV}}(K_{\text{25d put}}) - \sigma_{\text{IV}}(K_{\text{25d call}})$$

where 25-delta put/call refers to the strike at which the option has 25 delta. A positive skew number means puts are priced at higher IV than calls — the typical equity situation.

**Convexity (Butterfly):** Measures how much the wings are elevated above the ATM level:

$$\text{Butterfly} = \frac{\sigma_{\text{IV}}(K_{\text{25d put}}) + \sigma_{\text{IV}}(K_{\text{25d call}})}{2} - \sigma_{\text{IV}}(\text{ATM})$$

**Term structure of ATM volatility:** $\sigma_{\text{IV}}(\text{ATM}, T)$ also varies with expiry — typically upward sloping in calm markets and inverted (short-end vol > long-end) during crises when near-term uncertainty is highest.

## Walkthrough

Suppose SPX is at \$5000 and you observe 1-month options:

| Strike | Moneyness | IV     | Description              |
|--------|-----------|--------|--------------------------|
| 4500   | -10.5%    | 28.0%  | Deep OTM put (crash hedge) |
| 4750   | -5.1%     | 22.5%  | OTM put                  |
| 5000   | 0%        | 18.0%  | ATM                      |
| 5250   | +4.9%     | 16.5%  | OTM call                 |
| 5500   | +9.5%     | 15.5%  | Deep OTM call            |

Observation: IV falls monotonically from left to right. This is the equity **skew** (also called "negative skew" or "downward slope"), not a full symmetric smile.

The 25-delta risk reversal: $22.5\% - 16.5\% = 6.0\%$ — puts are 6 vol points richer than calls.

The 25-delta butterfly: $(22.5\% + 16.5\%) / 2 - 18.0\% = 1.5\%$ — wings are 1.5 vol points above ATM.

For comparison, FX (e.g., EUR/USD) would show:

| Strike | Description | IV    |
|--------|-------------|-------|
| Low    | OTM put     | 10.5% |
| ATM    | ATM         | 9.0%  |
| High   | OTM call    | 10.5% |

Here both wings are elevated symmetrically — the true "smile" shape. This is because currency pairs can crash in either direction; neither side has a special fear premium.

## Analysis

**Why BSM is definitively wrong:** If BSM were correct, IV would be flat across strikes. The existence of a smile is the market falsifying BSM's core assumption daily.

**What causes the equity skew:**
1. *Crash fear / negative skewness of returns:* Historical equity returns are negatively skewed — large drops are more common than large rallies of equal size.
2. *Leverage effect:* As stock prices fall, companies become more leveraged, increasing realized volatility. Expected vol and price level are negatively correlated.
3. *Supply and demand:* Institutions systematically buy OTM puts as tail-risk hedges and sell OTM calls as income (covered calls). Structural demand imbalances persist.

**Smile vs. skew terminology:**
- "Smile" — symmetric U-shape (FX, commodities)
- "Skew" or "smirk" — asymmetric, slopes downward (equities)
- In practice, traders use "smile" loosely to refer to both

**Failure mode — extrapolation:** The smile is only observed at liquid strikes. Extrapolating IV to very deep OTM options can produce negative probabilities in the Breeden-Litzenberger formula if done carelessly. Models like SVI and SABR impose arbitrage-free constraints.

**The smile changes over time:** During the 2020 COVID crash, the left wing of the equity skew steepened dramatically. The smile is itself a time series and has its own dynamics.

**Sticky strike vs. sticky delta:** Two conventions for how the smile moves when the underlying moves. "Sticky delta" assumes the smile is fixed in delta space (ATM always has the same IV). "Sticky strike" assumes the smile is fixed in strike space. These lead to different delta calculations.

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import brentq

def bsm_call(S, K, r, T, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def implied_vol(market_price, S, K, r, T):
    """Bisection solver for IV."""
    try:
        return brentq(
            lambda sigma: bsm_call(S, K, r, T, sigma) - market_price,
            1e-6, 5.0, xtol=1e-8
        )
    except ValueError:
        return np.nan

# --- Simulate a skewed vol surface using a simple parameterization ---
# In practice this would come from market data.
def parametric_iv(K, S=5000, atm_vol=0.18, skew=-0.30, convexity=0.05):
    """
    Simple quadratic smile in log-moneyness space.
    skew < 0 means lower strikes have higher IV (equity skew).
    """
    m = np.log(K / S)   # log-moneyness
    return atm_vol + skew * m + convexity * m**2

strikes = np.linspace(4000, 6000, 200)
ivs = parametric_iv(strikes)

plt.figure(figsize=(9, 5))
plt.plot(strikes, ivs * 100, color='steelblue', lw=2)
plt.axvline(5000, color='gray', linestyle='--', alpha=0.5, label='ATM (S=5000)')
plt.xlabel('Strike')
plt.ylabel('Implied Volatility (%)')
plt.title('Equity Volatility Skew (SPX-like)')
plt.legend()
plt.tight_layout()
plt.show()

# --- Extract risk reversal and butterfly at 25-delta ---
S, r, T = 5000, 0.05, 1/12

# Find 25-delta put and call strikes
def delta_call(K, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# Approximate: find K where delta ≈ 0.25 (call) and 0.75 (call = put 0.25 delta)
# Use the parametric smile
from scipy.optimize import brentq as br

K_25c = br(lambda K: delta_call(K, parametric_iv(K)) - 0.25, 5000, 7000)
K_25p = br(lambda K: delta_call(K, parametric_iv(K)) - 0.75, 3000, 5000)

iv_25c = parametric_iv(K_25c)
iv_25p = parametric_iv(K_25p)
iv_atm = parametric_iv(S)

print(f"ATM IV:        {iv_atm*100:.2f}%")
print(f"25d Call IV:   {iv_25c*100:.2f}%  (K={K_25c:.0f})")
print(f"25d Put IV:    {iv_25p*100:.2f}%  (K={K_25p:.0f})")
print(f"Risk Reversal: {(iv_25p - iv_25c)*100:.2f} vol pts")
print(f"Butterfly:     {((iv_25p + iv_25c)/2 - iv_atm)*100:.2f} vol pts")
```

## Bridge to Quant / ML

- **Skew as a fear gauge:** The steepness of the equity skew measures how much the market fears a crash. Strategies that short skew (sell OTM puts, buy ATM vol) harvest the skew premium when crashes don't materialize.
- **Vol surface calibration:** Quant desks calibrate stochastic vol models (SABR, Heston, rough Bergomi) to the observed smile. The smile is the ground truth that the model must reproduce.
- **Exotic pricing:** Products like barrier options, cliquets, and variance swaps all depend critically on the smile/skew — you can't price them correctly with a single BSM sigma.
- **ML on the smile:** The IV surface is a high-dimensional time series. PCA decomposition typically reveals 3 factors: level (parallel shift), skew (tilt), and curvature (smile convexity). These factors can be used as features in trading models.
- **Replication cost:** The smile reveals the cost of replicating any payoff via vanilla options — the Breeden-Litzenberger formula makes the smile equivalent to the risk-neutral distribution itself.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why did the equity volatility skew become permanent after 1987, when it was relatively flat before? What changed in the options market's behavior?
<details>
<summary>Answer</summary>
Before 1987, options market participants broadly trusted the lognormal BSM model. The crash of October 19, 1987 — a 22% single-day drop — was a 25-standard-deviation event under lognormal assumptions: essentially impossible. After this, institutional investors permanently repriced the tail risk of equities. Portfolio managers who had been unprotected in 1987 demanded crash insurance in the form of OTM puts. This structural demand for OTM puts — as tail-risk hedges — became a permanent feature of the market. Simultaneously, investors who sold OTM calls as "covered call" income generation created structural supply of the right wing. The imbalance between high put demand and natural call selling has persisted ever since, keeping the left wing of the skew elevated relative to BSM's flat prediction.
</details>

**Q2.** Equity markets have a skew (left wing elevated), while FX markets have a symmetric smile. Explain the economic reason for this difference.
<details>
<summary>Answer</summary>
In equity markets, there is a directional asymmetry: crashes (large downward moves) are more common and more violent than rallies of equal size. Companies with falling stock prices become more leveraged, which increases their volatility further (the leverage effect). And institutional investors systematically need downside protection for equity portfolios, creating sustained demand for OTM puts. None of these apply symmetrically. In FX markets, a currency pair can crash in either direction — the USD can crash against EUR just as easily as EUR can crash against USD. There is no structural "crash direction." Both OTM puts and OTM calls are demanded as hedges depending on which direction each participant is exposed to, creating symmetric demand that elevates both wings equally.
</details>

**Q3.** The Breeden-Litzenberger formula says the second derivative of the call price with respect to strike gives the risk-neutral density. What does a steeper equity skew (higher IV for low strikes) imply about the market's risk-neutral distribution compared to lognormal?
<details>
<summary>Answer</summary>
A steeper skew means OTM puts are more expensive than BSM predicts. Since call prices are higher at low strikes than BSM would predict, the second derivative ∂²C/∂K² — which gives the risk-neutral density q(K) — has more mass at low values of K than the lognormal distribution. Equivalently, the market's implied distribution has a fatter left tail (more probability of large drops) and potentially a thinner right tail (less probability of extreme rallies) than lognormal. In other words, the market is pricing a negatively skewed distribution with excess kurtosis — the same qualitative shape as empirically observed equity returns. The smile is the market collectively acknowledging that BSM's lognormal assumption understates crash risk.
</details>

---

### Level 2 — Quantitative

**Q4.** Using the parametric IV model in the note: σ_IV(K) = 0.18 − 0.30 × ln(K/5000) + 0.05 × [ln(K/5000)]². Compute the IV at strikes K = 4750, K = 5000, and K = 5250. Then compute the 25-delta risk reversal as IV(K_25d put) − IV(K_25d call), approximating the 25-delta put strike as K = 4750 and the 25-delta call strike as K = 5250.
<details>
<summary>Answer</summary>
At K = 4750: m = ln(4750/5000) = ln(0.95) = −0.0513.
σ = 0.18 − 0.30 × (−0.0513) + 0.05 × (−0.0513)² = 0.18 + 0.01539 + 0.000132 = 0.1955 ≈ 19.6%.

At K = 5000: m = 0. σ = 0.18 − 0 + 0 = 18.0%.

At K = 5250: m = ln(5250/5000) = ln(1.05) = 0.0488.
σ = 0.18 − 0.30 × 0.0488 + 0.05 × (0.0488)² = 0.18 − 0.01464 + 0.000119 = 0.1655 ≈ 16.5%.

25-delta risk reversal (approximate) = IV(K_25d put) − IV(K_25d call) = 19.6% − 16.5% = 3.1 vol points. Puts are richer than calls by 3.1 vol points.
</details>

**Q5.** The butterfly spread is defined as [IV(K_25d put) + IV(K_25d call)]/2 − IV(ATM). Using the values from Q4 (K_25d put IV = 19.6%, K_25d call IV = 16.5%, ATM IV = 18.0%), compute the butterfly. What does a positive butterfly mean in terms of the distribution?
<details>
<summary>Answer</summary>
Butterfly = (19.6% + 16.5%) / 2 − 18.0% = 36.1% / 2 − 18.0% = 18.05% − 18.0% = 0.05 vol points. In this parametric model, the butterfly is nearly zero — the skew is mostly linear rather than curved.

A positive butterfly means the wing options (OTM puts and calls) are expensive relative to ATM options — both tails are elevated. This implies the market's risk-neutral distribution has excess kurtosis (fat tails on both sides) relative to lognormal: the distribution has a higher peak (more probability near the mean) and fatter tails than a normal curve of the same variance. For a larger butterfly, the distribution resembles a mixture: mostly calm moves but occasional large jumps in either direction.
</details>

---

### Level 3 — Coding

**Q6.** The `parametric_iv` function in the note uses `m = np.log(K / S)` for log-moneyness with `S = 5000`. In a real implementation you'd use the forward price F = S × e^{rT} instead of S. Why does this matter, and what error does using spot instead of forward introduce?
<details>
<summary>Answer</summary>
The smile is conventionally parameterized around the forward price F = S × e^{rT}, not the spot price S, because the forward is the "fair" expected future stock price under the risk-neutral measure — it is where an ATM forward option is struck. When r > 0 and T > 0, F > S. If you use spot instead of forward, the "ATM point" of your smile (where m = 0) is anchored to the current spot price, but the market's ATM point is actually at the forward. For a 1-year option with r = 5%, F ≈ 1.051 × S, so the forward ATM is 5% higher than the spot. Using spot vs. forward shifts the entire smile by this amount. For short-dated options or low rates, the error is small; for long-dated options (2–5 years) or high rates, the error is material — you'd be computing the wrong ATM level, wrong risk reversal, and wrong butterfly values.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| The smile means BSM is "a little bit wrong" | The smile is a systematic, persistent, and large deviation from BSM. Equity OTM puts routinely trade at 5–10 vol points above ATM — this is not a rounding error |
| A flat smile means the market agrees with BSM | A flat smile means the market happens to price all strikes at the same vol today — it says nothing about whether GBM is the right model. Local vol and stochastic vol models can both produce flat smiles |
| The smile is the same for all asset classes | Equities have a left skew; FX has a symmetric smile; commodities often have a right skew (fear of supply spikes); interest rates have a hump. The shape encodes the specific crash direction feared by each market |
| The smile is stable over time | The smile is itself a time series. The skew steepens dramatically during market stress (VIX spikes). Using a static smile for long-horizon risk management is dangerous |

## Related Concepts

- [[Implied Volatility]]
- [[Volatility Surface]]
- [[Black-Scholes Model]]
- [[Variance Swap]]
- [[VIX]]
- [[Gamma Scalping]]

## Sources Used

- Hull, *Options, Futures, and Other Derivatives*, Ch. 20 (Volatility Smiles)
- Hull, Ch. 19 for IV context

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | Hull + initial build |
| 2026-04-12 | Note created | bootstrap |
| 2026-04-11 | QA review: added [[Volatility Surface]] to Related Concepts | quality review |
