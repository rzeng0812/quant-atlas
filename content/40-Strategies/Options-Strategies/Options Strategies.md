---
type: concept
domain: 40-Strategies
tags: [strategy, options, derivatives]
status: math
stability: empirical
confidence: medium
last_reviewed: 2026-04-18
review_interval_days: 30
sources: ["Hull ch.10-11"]
created: 2026-04-18
---

> [!info] Problem Chain
> **Chain:** Options/Hedging → Hedging/Alpha: How do practitioners use options to hedge positions, express views, and collect premium?
> **This concept:** Multi-leg options strategies provide the toolkit for translating directional, volatility, and hedging views into precisely defined risk/reward profiles that single options cannot achieve.
> **Alternative approaches to this gap:** [[Gamma Scalping]], [[Volatility Arbitrage]]
> **You need first:** [[Option Greeks]], [[Black-Scholes Model]], [[Put-Call Parity]]
> **This unlocks:** [[Gamma Scalping]], [[Volatility Arbitrage]]

## Why This Exists

**The gap:** Single calls and puts provide only blunt directional bets with unlimited or fully-risked outcomes; practitioners needed a richer vocabulary of structures to express nuanced views (bounded moves, range-bound markets, cheap hedges) without accepting the full premium cost of naked options.
**What came before:** Single-leg options trading — buying or selling a call or put — which is capital-intensive and exposes the trader to the full cost of theta decay or directional risk without limiting downside.
**What this adds:** Systematic taxonomy of multi-leg structures — vertical spreads (limit cost while retaining direction), straddles/strangles (pure volatility bets), iron condors (premium collection in range-bound markets), protective puts/covered calls (hedging with income) — each with closed-form payoff profiles and known maximum gain/loss.
**What it still doesn't solve:** Multi-leg strategies are expensive in transaction costs (each leg incurs bid-ask spread); pin risk near expiry can turn defined-risk structures into unhedged exposures; volatility skew means theoretical payoffs assume constant IV across strikes, which doesn't hold in practice.

A single option — a call or a put — is a blunt instrument. You pay a premium, and you either win big or lose the whole premium. Multi-leg options strategies are about sculpting that payoff: combining two or more options to limit your cost, define your risk, profit from a specific view, or collect premium in a range-bound market.

Think of it like this: instead of betting that a stock will definitely go up, you might bet only that it won't fall below \$90 — and you can express that view more cheaply and precisely with a spread than with a naked put. Multi-leg strategies let you trade volatility, direction, and time with surgical precision.

There are three families of strategies covered here:

1. **Directional** — you have a view on which way the stock will move, but want to limit cost and risk.
2. **Volatility plays** — you don't care about direction; you care whether the stock moves a lot or a little.
3. **Hedging** — you own stock and want to protect or monetize it.

## Math Concepts

All payoffs are computed at expiry. Let $S_T$ = stock price at expiry, $K$ = strike, $C(K)$ = call premium, $P(K)$ = put premium. Net premium = sum of premiums paid (positive) minus premiums received (negative).

**Call payoff at expiry:**
$$\text{Payoff}_{\text{call}} = \max(S_T - K, 0)$$

**Put payoff at expiry:**
$$\text{Payoff}_{\text{put}} = \max(K - S_T, 0)$$

**Net P&L at expiry** = payoff − net premium paid.

For each strategy below, all positions are assumed to share the same underlying and expiry $T$ unless noted.

### (1) Bull Call Spread

**Structure:** Long call at $K_1$ (lower strike) + Short call at $K_2$ (higher strike), where $K_1 < K_2$.

The short call partially offsets the cost of the long call. You sacrifice unlimited upside above $K_2$ in exchange for a cheaper entry.

$$\text{Payoff} = \max(S_T - K_1, 0) - \max(S_T - K_2, 0)$$

| Metric | Formula |
|--------|---------|
| Net premium paid | $C(K_1) - C(K_2) > 0$ |
| Max profit | $(K_2 - K_1) - (C(K_1) - C(K_2))$ |
| Max loss | $C(K_1) - C(K_2)$ (premium paid) |
| Breakeven | $K_1 + C(K_1) - C(K_2)$ |

**When to use:** Mildly bullish. You believe the stock will rise but not dramatically. Cheaper than buying an outright call.

### (2) Bear Put Spread

**Structure:** Long put at $K_2$ (higher strike) + Short put at $K_1$ (lower strike), where $K_1 < K_2$.

Mirror image of the bull call spread. Profits from a moderate decline.

$$\text{Payoff} = \max(K_2 - S_T, 0) - \max(K_1 - S_T, 0)$$

| Metric | Formula |
|--------|---------|
| Net premium paid | $P(K_2) - P(K_1) > 0$ |
| Max profit | $(K_2 - K_1) - (P(K_2) - P(K_1))$ |
| Max loss | $P(K_2) - P(K_1)$ (premium paid) |
| Breakeven | $K_2 - (P(K_2) - P(K_1))$ |

**When to use:** Mildly bearish. Cheaper than buying an outright put.

### (3) Straddle

**Structure:** Long call + Long put, same strike $K$ and same expiry.

You don't care about direction. You profit from large moves either way. The stock must move enough to recover both premiums.

$$\text{Payoff} = \max(S_T - K, 0) + \max(K - S_T, 0)$$

| Metric | Formula |
|--------|---------|
| Net premium paid | $C(K) + P(K)$ |
| Max profit | Unlimited (up) / $K - \text{net premium}$ (down, floored at 0) |
| Max loss | $C(K) + P(K)$ (if $S_T = K$ exactly) |
| Breakeven (up) | $K + C(K) + P(K)$ |
| Breakeven (down) | $K - C(K) - P(K)$ |

**When to use:** Ahead of earnings, FDA decisions, or any known binary event. You expect large volatility but don't know direction.

### (4) Strangle

**Structure:** Long OTM call at $K_2$ + Long OTM put at $K_1$, where $K_1 < S < K_2$.

Like a straddle but both legs are out-of-the-money. Cheaper to enter, but requires a larger move to profit.

$$\text{Payoff} = \max(S_T - K_2, 0) + \max(K_1 - S_T, 0)$$

| Metric | Formula |
|--------|---------|
| Net premium paid | $C(K_2) + P(K_1)$ |
| Max profit | Unlimited (up) / $K_1 - \text{net premium}$ (down) |
| Max loss | $C(K_2) + P(K_1)$ |
| Breakeven (up) | $K_2 + C(K_2) + P(K_1)$ |
| Breakeven (down) | $K_1 - C(K_2) - P(K_1)$ |

**When to use:** Same as straddle but when you expect a very large move (or when the straddle is too expensive).

### (5) Butterfly Spread

**Structure:** Long 1 call at $K_1$ + Short 2 calls at $K_m$ + Long 1 call at $K_2$, where $K_1 < K_m < K_2$ and $K_m = (K_1 + K_2)/2$.

Profits from low realized volatility. The stock staying near $K_m$ is the best outcome. This is a "bet on calm."

$$\text{Payoff} = \max(S_T - K_1, 0) - 2\max(S_T - K_m, 0) + \max(S_T - K_2, 0)$$

| Metric | Formula |
|--------|---------|
| Net premium paid | $C(K_1) - 2C(K_m) + C(K_2)$ (usually small positive) |
| Max profit | $(K_m - K_1) - \text{net premium}$ (achieved at $S_T = K_m$) |
| Max loss | Net premium paid |
| Breakeven (low) | $K_1 + \text{net premium}$ |
| Breakeven (high) | $K_2 - \text{net premium}$ |

**When to use:** You believe the stock will stay near its current price through expiry. A low-cost, defined-risk way to short volatility.

### (6) Iron Condor

**Structure:** Short OTM call at $K_3$ + Long OTM call at $K_4$ + Short OTM put at $K_2$ + Long OTM put at $K_1$, where $K_1 < K_2 < S < K_3 < K_4$.

You collect net premium and profit as long as the stock stays between $K_2$ and $K_3$. The long wings ($K_1$, $K_4$) cap your maximum loss.

$$\text{Net premium received} = C(K_3) - C(K_4) + P(K_2) - P(K_1)$$

| Metric | Formula |
|--------|---------|
| Net premium received | See above (positive) |
| Max profit | Net premium received (stock stays in $[K_2, K_3]$) |
| Max loss (upside breach) | $(K_4 - K_3) - \text{net premium}$ |
| Max loss (downside breach) | $(K_2 - K_1) - \text{net premium}$ |
| Breakeven (up) | $K_3 + \text{net premium}$ |
| Breakeven (down) | $K_2 - \text{net premium}$ |

**When to use:** Sideways, range-bound markets with elevated IV. Popular in index options (SPX, NDX). The premium collected is highest when implied vol is high — so you're selling expensive "insurance."

### (7) Protective Put

**Structure:** Long 100 shares + Long put at strike $K$.

This is portfolio insurance. You own the stock for upside but buy a put to set a floor on how much you can lose.

$$\text{P\&L} = (S_T - S_0) + \max(K - S_T, 0) - P(K)$$

| Metric | Formula |
|--------|---------|
| Net premium paid | $P(K)$ |
| Max profit | Unlimited (stock goes up) |
| Max loss | $S_0 - K + P(K)$ |
| Breakeven | $S_0 + P(K)$ |

**When to use:** You own a stock position and want to protect against a sharp downside move. The strike $K$ sets your "insurance deductible."

### (8) Covered Call

**Structure:** Long 100 shares + Short call at strike $K$.

You collect premium by selling upside above $K$. The trade-off: you cap your gains if the stock rallies past $K$. Generates income on a flat or mildly bullish position.

$$\text{P\&L} = (S_T - S_0) - \max(S_T - K, 0) + C(K)$$

| Metric | Formula |
|--------|---------|
| Net premium received | $C(K)$ |
| Max profit | $(K - S_0) + C(K)$ |
| Max loss | $S_0 - C(K)$ (stock goes to zero) |
| Breakeven | $S_0 - C(K)$ |

**When to use:** You hold a stock and expect it to be flat or mildly up. Selling calls is a systematic income strategy widely used by long-only funds.

## Walkthrough

**Iron Condor example with real numbers:**

- Stock: $S = 100$, 30 DTE (days to expiry)
- Short put at $K_2 = 95$ (collect $P(95) = \$1.00$)
- Long put at $K_1 = 90$ (pay $P(90) = \$0.40$)
- Short call at $K_3 = 105$ (collect $C(105) = \$1.00$)
- Long call at $K_4 = 110$ (pay $C(110) = \$0.40$)
- Net premium received: $\$1.00 - \$0.40 + \$1.00 - \$0.40 = \$1.20$ per share

If stock stays between 95 and 105 at expiry: keep the full $\$1.20$.

Max loss if stock blows through either wing: $(5.00 - 1.20) = \$3.80$ per share.

**Breakeven:** Below $93.80$ or above $106.20$.

Probability of profit ≈ 60–70% (for typical SPX 1-sigma wings), but losses when they occur are ~3x the average gain. This is the inherent asymmetry of premium-selling strategies.

## Analysis

**Volatility matters more than direction:** For most options strategies, the key input is implied volatility (IV). Straddles/strangles lose money in low-vol environments even if the stock moves. Iron condors collected under low IV may not compensate for the risk. Rule of thumb: buy volatility strategies when IV is low (cheap insurance), sell volatility strategies when IV is high (expensive premium).

**The role of the vol surface:** Different strikes have different IVs (the volatility smile/skew). OTM puts on equity indices are expensive because of skew — buyers of protective puts pay a volatility premium. This makes bear put spreads (buying OTM puts) structurally expensive, and iron condors (selling OTM puts) structurally lucrative for the seller.

**Greeks summary by strategy:**

| Strategy | Delta | Gamma | Theta | Vega |
|----------|-------|-------|-------|------|
| Bull call spread | + | + (near $K_1$) | − | + |
| Straddle | ~0 | + | − | + |
| Iron condor | ~0 | − | + | − |
| Protective put | + | + | − | + |
| Covered call | + (reduced) | − | + | − |

**Bid-ask spreads:** Multi-leg strategies pay the bid-ask spread on each leg. An iron condor with 4 legs on a wide-market stock can be expensive to enter cleanly. Use limit orders and be patient.

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------ #
#  Payoff diagram for any combination of options at expiry
# ------------------------------------------------------------------ #

def option_payoff(S_T, strike, opt_type, position, premium):
    """
    Compute the P&L at expiry for a single option leg.

    Parameters
    ----------
    S_T      : array of stock prices at expiry
    strike   : option strike price
    opt_type : 'call' or 'put'
    position : +1 for long, -1 for short
    premium  : option premium (positive number, price paid or received)

    Returns
    -------
    pnl : array of P&L values at each S_T
    """
    if opt_type == 'call':
        intrinsic = np.maximum(S_T - strike, 0)
    else:
        intrinsic = np.maximum(strike - S_T, 0)

    # Long pays premium upfront; short receives premium
    pnl = position * intrinsic - position * premium
    return pnl


def payoff_diagram(legs, S_range=None, title="Options Strategy Payoff"):
    """
    Plot terminal P&L for a multi-leg options strategy.

    Parameters
    ----------
    legs : list of dicts, each with keys:
        - 'strike'   : float
        - 'type'     : 'call' or 'put'
        - 'position' : +1 (long) or -1 (short)
        - 'premium'  : float (option price)
    S_range : tuple (S_min, S_max) or None (auto)
    title   : string
    """
    # Auto-range: center on average strike ± 30%
    avg_strike = np.mean([leg['strike'] for leg in legs])
    if S_range is None:
        S_range = (avg_strike * 0.70, avg_strike * 1.30)

    S_T = np.linspace(S_range[0], S_range[1], 500)
    total_pnl = np.zeros_like(S_T)

    fig, ax = plt.subplots(figsize=(10, 5))

    for leg in legs:
        pnl = option_payoff(
            S_T,
            strike=leg['strike'],
            opt_type=leg['type'],
            position=leg['position'],
            premium=leg['premium']
        )
        total_pnl += pnl
        lbl = (f"{'Long' if leg['position']==1 else 'Short'} "
               f"{leg['type'].capitalize()} K={leg['strike']:.0f}")
        ax.plot(S_T, pnl, lw=1, linestyle='--', alpha=0.5, label=lbl)

    ax.plot(S_T, total_pnl, lw=2.5, color='black', label='Net P&L')
    ax.axhline(0, color='grey', lw=0.8, linestyle=':')
    ax.fill_between(S_T, total_pnl, 0,
                    where=(total_pnl >= 0), alpha=0.15, color='green')
    ax.fill_between(S_T, total_pnl, 0,
                    where=(total_pnl < 0),  alpha=0.15, color='red')
    ax.set_xlabel('Stock Price at Expiry ($)')
    ax.set_ylabel('P&L ($)')
    ax.set_title(title)
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------------ #
#  Example 1: Straddle — long call + long put, K=100
# ------------------------------------------------------------------ #
straddle_legs = [
    {'strike': 100, 'type': 'call', 'position': +1, 'premium': 3.50},
    {'strike': 100, 'type': 'put',  'position': +1, 'premium': 3.40},
]
payoff_diagram(straddle_legs, title="Long Straddle (K=100)")

# ------------------------------------------------------------------ #
#  Example 2: Iron Condor
#  Short put K=95, Long put K=90, Short call K=105, Long call K=110
# ------------------------------------------------------------------ #
iron_condor_legs = [
    {'strike': 90,  'type': 'put',  'position': +1, 'premium': 0.40},  # long put wing
    {'strike': 95,  'type': 'put',  'position': -1, 'premium': 1.00},  # short put
    {'strike': 105, 'type': 'call', 'position': -1, 'premium': 1.00},  # short call
    {'strike': 110, 'type': 'call', 'position': +1, 'premium': 0.40},  # long call wing
]
payoff_diagram(iron_condor_legs, title="Iron Condor (Profit zone: 95–105)")

# ------------------------------------------------------------------ #
#  Example 3: Bull Call Spread — long K=95 call, short K=105 call
# ------------------------------------------------------------------ #
bull_spread_legs = [
    {'strike': 95,  'type': 'call', 'position': +1, 'premium': 6.00},
    {'strike': 105, 'type': 'call', 'position': -1, 'premium': 1.50},
]
payoff_diagram(bull_spread_legs, title="Bull Call Spread (K=95/105)")

# ------------------------------------------------------------------ #
#  Tabulate key metrics for each strategy
# ------------------------------------------------------------------ #
def spread_metrics(K_low, K_high, C_low, C_high, strategy='bull_call'):
    """Quick calculator for spreads."""
    net_premium = C_low - C_high
    max_profit = (K_high - K_low) - net_premium
    max_loss = net_premium
    breakeven = K_low + net_premium
    print(f"\n{strategy.upper()}")
    print(f"  Net premium paid : ${net_premium:.2f}")
    print(f"  Max profit       : ${max_profit:.2f}")
    print(f"  Max loss         : ${max_loss:.2f}")
    print(f"  Breakeven        : ${breakeven:.2f}")

spread_metrics(95, 105, 6.00, 1.50, strategy='bull call spread')
```

## Bridge to Quant / ML

- **Strategy selection as a classification problem:** Given features (IV rank, days to expiry, earnings date, realized/implied vol spread), an ML model can classify which strategy family is appropriate — premium-selling (iron condor) when IV is high, premium-buying (straddle) when IV is low.
- **Payoff engineering:** Multi-leg strategies are used to construct structured products with custom payoff profiles. Understanding how to decompose any payoff into a combination of calls and puts is the foundation of static replication theory.
- **Volatility smile arbitrage:** The butterfly spread price is directly related to the risk-neutral probability density at the middle strike. Pricing butterflies across strikes reads the market's implied probability distribution. This is the basis of Breeden-Litzenberger, widely used in quant modeling.
- **Delta hedging multi-leg books:** A portfolio of iron condors has a complex gamma/vega surface. Risk systems aggregate Greeks across all legs and strikes; this requires understanding how multi-leg payoffs compose.
- **Backtest considerations:** Realistic backtests of options strategies require bid-ask spread modeling, slippage on multi-leg orders, and handling of pin risk near expiry. Many "profitable" strategy backtests evaporate once transaction costs are included.

## Self-Assessment

### Level 1 — Conceptual

**Q1.** What is the key difference between a bull call spread and a naked long call in terms of risk/reward?
> **A:** A naked long call has unlimited upside but costs more premium (full theta risk). A bull call spread caps the upside at K₂ − K₁ but reduces the net premium paid (sell the higher strike call to partially finance the lower strike buy), lowering the breakeven and reducing maximum loss.

**Q2.** Why does a long straddle profit from volatility regardless of direction, while a long strangle is cheaper but requires a larger move?
> **A:** A straddle buys ATM call + put; any move larger than the total premium paid generates profit from either leg. A strangle buys OTM call + OTM put at lower combined premium, but the stock must move further (past both strikes) before profitability; cheaper entry, but higher movement threshold.

**Q3.** What is "pin risk" in options strategies, and when is it most dangerous?
> **A:** Pin risk occurs when the stock closes near a strike at expiration — the position holder may be uncertain whether they'll be assigned. For example, in a short iron condor: if the stock pins at the short call strike, you may or may not be assigned, creating undefined overnight exposure. Most dangerous on expiration Friday for short-dated positions.

### Level 2 — Quantitative

**Q4.** You buy a call spread: long the \$100 call at \$5, short the \$110 call at \$2. What is the maximum gain, maximum loss, and breakeven at expiry?
> **A:** Net premium = $5 − $2 = \$3. Max gain = (\$110 − $100) − $3 = $7 (when S_T ≥ $110). Max loss = $3 (when S_T ≤ $100). Breakeven = $100 + $3 = \$103.

**Q5.** An iron condor is short the \$95 put, long the \$90 put, short the \$110 call, long the \$115 call. If net premium received = \$2, what are the max gain, max loss, and breakeven prices?
> **A:** Max gain = \$2 (collected premium, when stock stays between \$95 and \$110). Max loss = (\$95 − $90) − $2 = \$3 on the put side or (\$115 − $110) − $2 = \$3 on the call side. Lower breakeven = \$95 − $2 = $93; upper breakeven = $110 + $2 = \$112.

### Level 3 — Coding

**Q6.** Implement payoff calculation for the four core multi-leg strategies: bull call spread, iron condor, straddle, and protective put.

```python
import numpy as np

def options_payoffs(S_T: np.ndarray, strategy: str, **kwargs) -> np.ndarray:
    """
    Compute net payoff at expiry for common multi-leg options strategies.
    
    Parameters
    ----------
    S_T      : array of stock prices at expiry
    strategy : one of 'bull_call_spread', 'iron_condor', 'straddle', 'protective_put'
    **kwargs : strategy-specific parameters (strikes, premiums)
    
    Returns
    -------
    payoff : net payoff at each S_T (after accounting for premiums paid/received)
    """
    # TODO: Implement each strategy payoff:
    # bull_call_spread: kwargs = {K1, K2, C1, C2} (long K1 call, short K2 call)
    # iron_condor: kwargs = {Kp1, Kp2, Kc1, Kc2, net_premium} (short put spread + short call spread)
    # straddle: kwargs = {K, call_premium, put_premium} (long call + long put at same strike)
    # protective_put: kwargs = {K, put_premium, stock_cost} (long stock + long put)
    # Use np.maximum for option payoff legs
    pass
```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Defined-risk strategies are always safer | Selling credit spreads has defined maximum loss but that loss can be 100% of buying power; "defined" ≠ "small" |
| A straddle needs the stock to move a lot to profit | It needs to move MORE than the total premium paid; ATM options are expensive, so the breakeven move can be large |
| Greeks don't matter for defined-risk strategies | All multi-leg strategies have net Greeks; an iron condor has negative vega — rising IV hurts it even before expiry |
| Multi-leg orders always fill at the mid-price | Bid-ask spread on each leg compounds; complex orders often fill worse than theoretical mid, especially in illiquid names |

## Related Concepts

- [[Volatility Arbitrage]] — exploits the spread between implied and realized volatility using delta-hedged options
- [[Option Greeks]]
- [[Black-Scholes Model]]
- [[Delta Hedging]]
- [[Gamma Scalping]]
- [[Implied Volatility]]
- [[Volatility Smile]]

## Sources Used

- Hull, *Options, Futures, and Other Derivatives*, Ch. 10 (Trading Strategies Involving Options) — bull/bear spreads, straddles, strangles, butterflies
- Hull, Ch. 11 (Binomial Trees) for payoff intuition
- Natenberg, *Option Volatility and Pricing* — practical strategy construction and vol considerations

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | initial build |
| 2026-04-11 | Added tagline quote; added [[Volatility Arbitrage]] to Related Concepts | QA review |
