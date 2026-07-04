---
type: concept
domain: 20-Markets
tags: [derivatives, options, risk]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-11
review_interval_days: 365
sources:
  - "Hull ch.19"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Hedging & Risk → Gap 2: Delta hedging neutralizes direction but leaves other exposures
> **This concept:** Decomposes an option's total risk into distinct, named dimensions (delta, gamma, theta, vega, rho) so each can be measured, monitored, and hedged independently.
> **Alternative approaches to this gap:** none — the Greeks are the universal decomposition; different models (Heston, local vol) change the Greek values but not the framework
> **You need first:** [[Put-Call Parity]], [[Black-Scholes Model]], [[Delta Hedging]]
> **This unlocks:** [[Gamma Scalping]], [[Volatility Surface]], [[Value at Risk]], [[Options Strategies]]

## Why This Exists

**The gap:** After a trader delta-hedges a position, they still have no way to answer: "How much money do I lose if a week passes? If volatility spikes by 5%? If the stock makes a large jump?" Delta hedging eliminates the first-order directional risk, but the position still bleeds from time passing, gains or loses on volatility changes, and gets hurt (or helped) by big moves. Without a systematic way to measure these remaining exposures, risk management is guesswork.

**What came before:** Traders knew options had multiple risk dimensions but tracked them informally — "this book has a lot of gamma" meant something to experienced traders but couldn't be aggregated, reported, or systematically hedged. There was no standard vocabulary or measurement framework.

**What this adds:** A complete set of partial derivatives of the option price with respect to each input: delta (stock price), gamma (rate of change of delta), theta (time), vega (volatility), rho (interest rate). Each Greek has a clear interpretation, can be computed from BSM, and — critically — can be hedged using specific instruments. This turns risk management from art into arithmetic: sum up the Greeks across a book of hundreds of positions, and you know exactly what you're exposed to.

**What it still doesn't solve:** Greeks are local, first-order (or second-order for gamma) approximations — they describe risk at the current market level. A large market move invalidates the Greek approximation. Greeks also don't capture the risk that the vol surface itself shifts in complex ways (vanna, volga, and higher-order Greeks exist but are not standard).

## Math Concepts

All Greeks are partial derivatives of the option price $V(S, t, \sigma, r)$.

**Delta ($\Delta$)** — sensitivity to stock price:

$$\Delta = \frac{\partial V}{\partial S}$$

For a BSM call: $\Delta_{\text{call}} = N(d_1)$, always between 0 and 1.
For a put: $\Delta_{\text{put}} = N(d_1) - 1$, always between −1 and 0.

*Intuition:* if $\Delta = 0.6$, the option moves \$0.60 for every \$1 the stock moves.

---

**Gamma ($\Gamma$)** — rate of change of Delta; second derivative w.r.t. stock:

$$\Gamma = \frac{\partial^2 V}{\partial S^2} = \frac{\partial \Delta}{\partial S}$$

For BSM: $\Gamma = \frac{N'(d_1)}{S \sigma \sqrt{T}}$ (same for calls and puts by put-call parity).

*Intuition:* $\Gamma$ measures how much you need to rebalance your hedge when the stock moves. High $\Gamma$ = expensive to hedge = option is sensitive to large moves.

---

**Theta ($\Theta$)** — sensitivity to time (time decay):

$$\Theta = \frac{\partial V}{\partial t}$$

Usually negative for long options — options lose value as expiry approaches.

*Intuition:* you pay for optionality. Every day that passes, some of that optionality expires. $\Theta \approx -\$10$/day means the option loses \$10 in value overnight, all else equal.

---

**Vega ($\mathcal{V}$)** — sensitivity to volatility:

$$\mathcal{V} = \frac{\partial V}{\partial \sigma}$$

For BSM: $\mathcal{V} = S \sqrt{T} N'(d_1) > 0$ always.

*Intuition:* higher volatility = wider range of possible outcomes = option worth more. Vega is always positive for long options (calls and puts both benefit from higher vol).

---

**Rho ($\rho$)** — sensitivity to interest rate:

$$\rho = \frac{\partial V}{\partial r}$$

Positive for calls (higher $r$ → higher forward price → call worth more). Negative for puts.

*Intuition:* least important Greek for short-dated equity options. Matters more for long-dated options and interest rate derivatives.

---

**Key relationship (from BSM PDE via Ito's Lemma):**

$$\Theta + \frac{1}{2}\sigma^2 S^2 \Gamma + rS\Delta = rV$$

This links all Greeks together — if you know three, the fourth is determined. It's the BSM PDE in Greek notation.

## Walkthrough

For a call: $S=100$, $K=100$, $r=5\%$, $\sigma=20\%$, $T=0.5$ years (at-the-money, 6 months out):

| Greek | Value | Meaning |
|-------|-------|---------|
| $\Delta$ | 0.57 | Option gains \$0.57 per \$1 stock move |
| $\Gamma$ | 0.028 | Delta changes by 0.028 per \$1 move |
| $\Theta$ | −\$12/year ≈ −\$0.033/day | Lose \$0.033/day from time passing |
| $\mathcal{V}$ | 0.28 | Option gains \$0.28 per 1% vol increase |
| $\rho$ | 0.24 | Option gains \$0.24 per 1% rate increase |

## Analysis

- **Gamma–Theta trade-off:** long options have positive $\Gamma$ (benefit from large moves) but negative $\Theta$ (pay time decay). Short options are the reverse. This is the central trade-off in options — you're always paying for gamma with theta or vice versa.
- **Vega risk:** if you're long options, you benefit from rising volatility. Options desks often manage large vega books — sudden vol spikes (crises) cause dramatic P&L swings.
- **Greeks are dynamic:** all Greeks change as $S$, $t$, $\sigma$ change. This is why hedging requires continuous rebalancing (see [[Delta Hedging]]).
- **"Dollar Greeks":** practitioners often use $S \cdot \Delta$ (dollar delta) and $S^2 \Gamma / 100$ (dollar gamma) to normalize Greeks to a fixed notional.

## Implementation

```python
import numpy as np
from scipy.stats import norm

def bsm_greeks(S, K, r, sigma, T, option_type="call"):
    """Compute BSM Greeks for a European option."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    n_d1 = norm.pdf(d1)   # standard normal PDF at d1

    delta = norm.cdf(d1) if option_type == "call" else norm.cdf(d1) - 1
    gamma = n_d1 / (S * sigma * np.sqrt(T))
    vega  = S * np.sqrt(T) * n_d1 / 100        # per 1% vol move
    theta_call = (-(S * n_d1 * sigma) / (2 * np.sqrt(T))
                  - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    theta_put  = (-(S * n_d1 * sigma) / (2 * np.sqrt(T))
                  + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
    theta = theta_call if option_type == "call" else theta_put
    rho_call = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    rho_put  = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100
    rho = rho_call if option_type == "call" else rho_put

    return {"delta": delta, "gamma": gamma, "vega": vega,
            "theta": theta, "rho": rho}

print(bsm_greeks(100, 100, 0.05, 0.20, 0.5))
```

## Bridge to Quant / ML

- Greeks are natural features for ML models predicting option returns — a well-hedged book has near-zero delta but nonzero gamma/vega exposure
- **Gamma scalping** (see [[Gamma Scalping]]) — a pure-vol strategy that profits when realized vol > implied vol
- In ML finance research, Greeks are used as inputs to models predicting when to rebalance hedges dynamically (RL for execution)

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why is gamma described as "what makes delta hedging hard"? What problem does it create for a hedger who rebalances only once per day?
<details>
<summary>Answer</summary>
Delta tells you the hedge ratio right now. Gamma tells you how fast delta changes as the stock moves. A high-gamma option means that after a \$1 move in the stock, your delta has already shifted significantly — so the hedge you put on this morning is wrong by the afternoon. A hedger who rebalances only once per day leaves the position unhedged for those intraday moves. The larger the gamma and the larger the move, the larger the hedging error. This is why options close to expiry (which have very high gamma near the strike) are the most expensive to hedge: they require very frequent rebalancing.
</details>

**Q2.** The gamma-theta trade-off is described as "the central trade-off in options." Explain in plain English why a long option position simultaneously has positive gamma and negative theta, and why these two must coexist.
<details>
<summary>Answer</summary>
A long option benefits from large moves (positive gamma) because as the stock moves toward the strike, the option gains delta, and you profit more from each incremental move. But this "convexity benefit" doesn't come free — you paid a premium for the option that represents the expected gamma profit assuming the stock moves around as much as implied vol suggests. Time decay (theta) is the daily cost of holding that optionality. If the stock just sits still, the option's time value erodes — you paid for the right to benefit from moves, and each passing day with no move is a loss. They coexist because the option's price embeds the expected future gamma profits; if the realized moves are exactly as expected, theta and gamma profits cancel out, leaving zero net P&L.
</details>

**Q3.** Vega is always positive for both calls and puts. Why? What does this tell you about who benefits from a volatility spike?
<details>
<summary>Answer</summary>
Higher volatility means a wider distribution of possible stock prices at expiry — more extreme outcomes become more likely. A call benefits from higher stock prices and is unaffected by lower prices (it just expires worthless). A put benefits from lower stock prices and is unaffected by higher prices. In both cases, fatter tails in the distribution make the option worth more, because more probability mass falls in the profitable region. Both are one-sided bets: they participate in the upside of their direction without the downside. Therefore, any increase in the spread of the distribution helps both. Practically: anyone long options (calls or puts) benefits from a vol spike; anyone short options (the typical market-maker or options seller position) is hurt by rising vol.
</details>

---

### Level 2 — Quantitative

**Q4.** For a call with S = 100, K = 100, r = 5%, σ = 20%, T = 0.5 years, compute delta and gamma. Then estimate the new delta if the stock moves to S = 103. Finally, compute the approximate gamma P&L from that \$3 move.
<details>
<summary>Answer</summary>
d1 = [ln(1) + (0.05 + 0.02) × 0.5] / (0.20 × √0.5) = 0.035 / 0.1414 = 0.2475.
Delta = N(0.2475) ≈ 0.5977.
Gamma = N'(0.2475) / (100 × 0.20 × √0.5) = 0.3867 / (100 × 0.1414) = 0.3867 / 14.14 ≈ 0.0274.

New delta (approximate): 0.5977 + 0.0274 × 3 = 0.5977 + 0.0822 = 0.680.

Gamma P&L = ½ × Γ × (ΔS)² = ½ × 0.0274 × 9 = 0.123 per option. For a long call position, this is a profit of \$0.123 per option from the \$3 move.
</details>

**Q5.** A short option position has Θ = +\$0.05/day (collect \$0.05/day from time decay). The position also has Γ = −0.03. The stock moves \$2 in one day. Compute the net P&L for that day and determine whether the gamma loss or theta gain dominates.
<details>
<summary>Answer</summary>
Theta gain: +\$0.05 (collect time decay for one day).
Gamma P&L: ½ × Γ × (ΔS)² = ½ × (−0.03) × 4 = −\$0.06 (loss, because short gamma).
Net P&L = +0.05 − 0.06 = −\$0.01. The gamma loss slightly dominates the theta gain for a \$2 move.

Breakeven move: set ½ × 0.03 × (ΔS)² = 0.05 → (ΔS)² = 0.05 / 0.015 = 3.33 → ΔS ≈ \$1.83. Moves larger than \$1.83/day cause net losses; moves smaller than \$1.83/day produce net profits.
</details>

---

### Level 3 — Coding

**Q6.** In `bsm_greeks`, vega is computed as `S * np.sqrt(T) * n_d1 / 100`. Why is it divided by 100, and what would happen to the vega output if you removed that division?
<details>
<summary>Answer</summary>
The division by 100 scales vega to represent the dollar change in option value per 1 percentage point (1%) move in volatility, rather than per 1.0 move in sigma (which would be a 100% vol change). If you removed the /100, vega would be 100× larger and represent the P&L for a 100% absolute change in sigma — a useless unit in practice (no option's vol moves from 20% to 120%). The /100 convention matches how traders think: "my vega is \$0.28, so if vol moves from 20% to 21%, I gain \$0.28." This is consistent with the theta output being expressed per 1/365 of a year (one calendar day) rather than per year.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Delta-neutral means risk-free | Delta-neutral only eliminates first-order stock price risk; the position still has gamma, theta, vega, and rho exposure — all of which cause P&L |
| Gamma is only relevant for large moves | Gamma matters for any move; it sets the breakeven daily move where theta collect equals gamma loss. Small frequent moves still interact with gamma |
| Vega and theta always oppose each other | Theta and gamma are the true pair (they cancel in expectation). Vega is independent — it measures exposure to a change in the *level* of implied vol, not to the stock moving |
| Greeks are constant over the option's life | All Greeks change continuously as S, t, and σ change. Delta in particular changes with every tick; gamma peaks near ATM and near expiry; vega peaks at intermediate maturities |

## Related Concepts
- [[Black-Scholes Model]] — the model from which BSM Greeks are derived
- [[Delta Hedging]] — using $\Delta$ to construct a riskless portfolio
- [[Gamma Scalping]] — exploiting $\Gamma$ when realized vol differs from implied
- [[Implied Volatility]] — Vega tells you how much a vol change is worth
- [[Volatility Surface]] — Vega and Vanna describe sensitivity across the surface

## Sources Used
- Hull — *Options, Futures & Other Derivatives*, ch.19

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | Hull ch.19 |
| 2026-04-11 | Fixed broken wikilink `[[60-ML-Finance/]]` in Bridge section (replaced with plain text) | QA review |
