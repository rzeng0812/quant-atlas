---
type: concept
domain: 40-Strategies
tags: [strategy, microstructure, HFT]
status: math
stability: empirical
confidence: medium
last_reviewed: 2026-04-12
review_interval_days: 30
sources:
  - "Cartea et al - Algorithmic and HFT"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Execution → Gap 3: How do liquidity providers optimally quote in a limit order book?
> **This concept:** Market making defines the economic structure of liquidity provision — the spread, adverse selection, and inventory tradeoffs that determine whether providing quotes is profitable.
> **Alternative approaches to this gap:** [[Avellaneda-Stoikov]], [[TWAP-VWAP]]
> **You need first:** [[Order Book]], [[Adverse Selection]]
> **This unlocks:** [[Avellaneda-Stoikov]], [[Transaction Cost Analysis]]

## Why This Exists

**The gap:** As markets moved from specialist/dealer systems to electronic limit order books, practitioners needed a conceptual and mathematical framework for why market makers quote, how they price adverse selection risk, and how they manage inventory.
**What came before:** Specialist and dealer systems where designated market makers were obligated to quote — a regulatory and institutional structure, not an economic optimization framework.
**What this adds:** The Glosten-Milgrom and Kyle models formalize the adverse selection cost; the bid-ask spread is derived as the market maker's break-even condition between informed and uninformed flow; inventory risk (Amihud, Ho-Stoll) provides a second component of the spread; together these explain empirically observed spread patterns and guide electronic market making.
**What it still doesn't solve:** Models assume stationary order flow; real markets have toxicity clustering, regime changes, and flash crashes; the model doesn't address latency competition (who's fastest to cancel in response to news) which dominates modern electronic market making.

Imagine you run a currency exchange kiosk at an airport. You buy dollars at \$1.28 per euro and sell dollars at \$1.32 per euro. Every time a traveler comes to you, you make \$0.04 on the transaction — that's the spread. You don't care whether the dollar is going up or down over the week; you just want lots of travelers coming through, each paying you a small fee for the service of immediate exchange.

A financial market maker does exactly this — at the millisecond scale. They post a *bid* (price to buy) and an *ask* (price to sell) simultaneously, and they profit from the **bid-ask spread** when customers transact at their quotes. The market maker provides *liquidity* to the market: anyone who wants to trade immediately can do so, because the market maker is always there with a quote.

But there's a danger the airport kiosk doesn't face: some of your "customers" are not ordinary travelers. They are people who just heard that the dollar is about to crash because of a government announcement, and they're rushing to exchange before anyone else knows. When you sell dollars to that person, you'll soon find the dollar is worth far less than what you charged them. You were **adversely selected** — you traded with someone who knew more than you.

This is the fundamental tension of market making:
- **Revenue:** collect the bid-ask spread from uninformed traders
- **Cost:** lose money to informed traders who know something you don't

The art of market making is quoting tight enough spreads to attract order flow, while managing the risk that some of that order flow is toxic (informed).

## Math Concepts

**Basic P&L identity**

For a market maker over $N$ trades:

$$\text{P\&L} = \underbrace{\frac{s}{2} \cdot N}_{\text{spread revenue}} - \underbrace{\lambda \cdot Q^2}_{\text{inventory/adverse selection cost}}$$

where $s$ is the spread, $N$ is trade count, $\lambda$ is the price impact coefficient, and $Q$ is inventory (net position). The first term is revenue; the second is cost.

**Avellaneda-Stoikov Model**

The canonical academic model for optimal market making. The mid-price follows a random walk:

$$dS_t = \sigma\,dW_t$$

The market maker maximizes expected terminal wealth minus inventory penalty:

$$V(x, q, s, t) = \max_{r^b, r^a} E\!\left[x_T + q_T S_T - \gamma q_T^2 \sigma^2 (T-t)\right]$$

where:
- $x$ — cash balance
- $q$ — inventory (number of shares held)
- $r^b, r^a$ — distances of bid/ask from mid-price
- $\gamma$ — risk aversion parameter
- $T$ — horizon

The optimal quotes (distance from mid) are approximately:

$$r^{b*} = r^{a*} \approx \frac{\gamma \sigma^2 (T-t)}{2} + \frac{1}{\kappa} \ln\!\left(1 + \frac{\gamma}{\kappa}\right)$$

And the *inventory-adjusted* mid-price (the market maker skews their quotes based on inventory):

$$q^* = S - q \cdot \gamma \sigma^2 (T-t)$$

If the market maker is long (q > 0), they shade their bid and ask *down* to attract sellers and reduce inventory. If short (q < 0), they shade up.

**Spread components (microstructure theory)**

The observed bid-ask spread has three components:

$$s = s_{\text{order processing}} + s_{\text{inventory}} + s_{\text{adverse selection}}$$

- **Order processing cost:** Fixed operational cost per transaction. Flat cost.
- **Inventory cost:** Compensation for holding directional exposure. Proportional to $\sigma$ and inventory holding time.
- **Adverse selection cost:** Compensation for trading with informed counterparties. This is the dominant component in modern markets.

**Fill rate and Poisson arrivals**

Market makers model order arrivals as Poisson processes. At a given quote level, the arrival rate of market orders that fill the maker's quote decreases with quote distance from mid:

$$\lambda(r) = A e^{-\kappa r}$$

where $A$ is the base arrival rate and $\kappa$ controls how sensitive order flow is to price distance. A tighter spread ($r$ small) = more fills but worse adverse selection. A wider spread ($r$ large) = fewer fills but better adverse selection protection.

**Expected P&L per trade (simplified)**

$$E[\text{P\&L per trade}] = \frac{s}{2} - \alpha \cdot E[\text{adverse move}]$$

where $\alpha$ is the fraction of trades that are "informed" and the adverse move is the price change after the trade. Profitable market making requires:

$$\frac{s}{2} > \alpha \cdot E[\text{adverse move}]$$

## Walkthrough

**Snapshot: a market maker quoting AAPL**

Current AAPL mid-price: $\$185.00$. Market maker parameters:
- Risk aversion: $\gamma = 0.1$
- Mid-price volatility: $\sigma = \$0.50$/min
- Remaining session: $T-t = 60$ minutes
- Inventory: $q = +50$ shares (long — want to reduce)

**Step 1 — Compute symmetric spread (ignoring inventory):**

$$r^* = \frac{\gamma \sigma^2 (T-t)}{2} = \frac{0.1 \times 0.25 \times 60}{2} = \$0.75$$

Symmetric quotes: bid $184.25$, ask $185.75$. But this is very wide — in practice, competition from other market makers forces spreads much tighter.

**Step 2 — Inventory skew:**

$$\text{Skew} = q \cdot \gamma \sigma^2 (T-t) = 50 \times 0.1 \times 0.25 \times 60 = \$75$$

This is large because inventory is large. The market maker adjusts their *reservation price* (mid) downward by \$75. Then re-quotes:
- Reservation mid: $185.00 - 0.75 = $184.25$ (per share adjustment scaled appropriately)
- Adjusted bid: $183.88$, ask: $184.63$

The lower ask (relative to true mid) attracts buyers, helping the MM unload their long inventory.

**Step 3 — Trade arrival:**

A market order arrives to buy 100 shares. The ask is hit at \$184.63.

- MM now sells 100 shares (reduces long from +50 to -50).
- Revenue per share: ask - mid = $184.63 - 184.25 = $0.38 half-spread.
- Gross revenue: \$38.

If the next 5 minutes bring no adverse price move, the MM can rebuy at the bid, pocketing \$0.76 round-trip per share.

**Adverse selection scenario:**

Right after the market maker sells at the ask, AAPL announces a product recall. Price drops to \$182. The buyer (informed trader) immediately profits \$2.63/share. The MM is now short at \$184.63 with the stock at \$182 — actually a small profit, but had the MM been long, they'd have lost \$2.63 per share. The MM was lucky here, but on average, after an informed trade, the price moves *against* their position.

## Analysis

**Risk and failure modes:**

- **Inventory accumulation ("position creep"):** If order flow is one-sided (e.g., everyone is selling in a declining market), the MM accumulates a large long position just as prices fall. Inventory limits and aggressive skewing are critical.
- **Adverse selection ("toxic flow"):** High-frequency informed traders can pick off stale quotes. The MM must update quotes faster than HFT predators can exploit them. This drives the technological arms race in HFT market making.
- **Quote stuffing / latency arbitrage:** Competitors can detect your quotes and trade against you before you can update. Co-location and low-latency infrastructure directly drive P&L.
- **Market regime change:** In fast markets (news events, economic data releases), the MM's model of volatility becomes stale instantly. Many MMs cancel all quotes during the minute surrounding major announcements (FOMC, NFP, etc.).
- **Competition compressing spreads:** As more market makers compete, spreads compress toward zero. Alpha per trade falls. Revenue comes from volume — the high-frequency arms race.

**The speed arms race:**

Modern equity market making at US exchanges requires microsecond response times. FPGA (field-programmable gate array) hardware, co-location at exchange data centers, and fiber/microwave communication networks have made this a capital-intensive technology business. Many strategies that worked in 2010 are no longer viable without significant infrastructure investment.

## Implementation

```python
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import List, Tuple

# ------------------------------------------------------------------
# Simplified Avellaneda-Stoikov market maker simulation
# ------------------------------------------------------------------

@dataclass
class MarketMakerParams:
    gamma: float = 0.1          # risk aversion
    sigma: float = 0.5          # mid-price volatility (per step)
    kappa: float = 1.5          # order arrival sensitivity to spread distance
    A: float = 140.0            # base order arrival rate (orders per time step)
    dt: float = 1.0             # time step
    T: float = 390.0            # total session length (time steps)
    inventory_limit: int = 200  # max absolute inventory before force-exit


def simulate_market_maker(params: MarketMakerParams, seed: int = 42) -> pd.DataFrame:
    """
    Simulate a simplified market maker following Avellaneda-Stoikov logic.
    Returns a DataFrame with the session record.
    """
    np.random.seed(seed)
    p = params

    # State
    mid = 100.0     # initial mid-price
    inventory = 0   # net shares held
    cash = 0.0      # cash balance

    records = []

    for t in range(int(p.T)):
        time_remaining = p.T - t

        # --- 1. Update mid-price (random walk) ---
        mid += p.sigma * np.random.normal()

        # --- 2. Compute optimal spread distance ---
        # AS formula: r* = (gamma * sigma^2 * time_remaining) / 2
        #               + (1/kappa) * ln(1 + gamma/kappa)
        r_spread = (
            (p.gamma * p.sigma**2 * time_remaining) / 2
            + (1 / p.kappa) * np.log(1 + p.gamma / p.kappa)
        )
        # Clip to a reasonable range
        r_spread = np.clip(r_spread, 0.05, 2.0)

        # --- 3. Inventory skew: adjust reservation mid ---
        reservation_mid = mid - inventory * p.gamma * p.sigma**2 * time_remaining

        # --- 4. Compute bid and ask ---
        bid = reservation_mid - r_spread
        ask = reservation_mid + r_spread

        # --- 5. Simulate order arrivals (Poisson) ---
        # Distance from true mid to our quotes
        delta_bid = mid - bid   # positive: bid is below mid
        delta_ask = ask - mid   # positive: ask is above mid

        # Arrival rate decreases exponentially with distance from mid
        lambda_bid = p.A * np.exp(-p.kappa * delta_bid) * p.dt
        lambda_ask = p.A * np.exp(-p.kappa * delta_ask) * p.dt

        # Sample number of bid/ask fills (Poisson)
        fills_at_bid = np.random.poisson(lambda_bid)   # MM buys at bid
        fills_at_ask = np.random.poisson(lambda_ask)   # MM sells at ask

        # --- 6. Update inventory and cash ---
        inventory += fills_at_bid - fills_at_ask
        cash      += fills_at_ask * ask - fills_at_bid * bid

        # --- 7. Inventory limit — forced liquidation at mid ---
        forced_trade = 0
        if abs(inventory) > p.inventory_limit:
            forced_trade = -inventory   # sell/buy back to zero
            cash += forced_trade * mid  # execute at mid (worst case)
            inventory = 0

        records.append({
            'time': t,
            'mid': mid,
            'bid': bid,
            'ask': ask,
            'spread': ask - bid,
            'inventory': inventory,
            'cash': cash,
            'pnl': cash + inventory * mid,  # mark-to-market P&L
            'fills_bid': fills_at_bid,
            'fills_ask': fills_at_ask,
            'forced_trade': forced_trade,
        })

    df = pd.DataFrame(records)
    return df


# --- Run simulation ---
params = MarketMakerParams(gamma=0.05, sigma=0.3, kappa=2.0, A=100, T=390)
session = simulate_market_maker(params, seed=99)

final_pnl       = session['pnl'].iloc[-1]
avg_spread      = session['spread'].mean()
total_fills     = session['fills_bid'].sum() + session['fills_ask'].sum()
max_inventory   = session['inventory'].abs().max()
forced_trades   = (session['forced_trade'] != 0).sum()

print(f"Session P&L:          ${final_pnl:.2f}")
print(f"Average spread:       ${avg_spread:.4f}")
print(f"Total fills:          {total_fills}")
print(f"Max inventory:        {max_inventory} shares")
print(f"Forced liquidations:  {forced_trades}")
print(f"\nBreakdown:")
print(f"  Final cash:         ${session['cash'].iloc[-1]:.2f}")
print(f"  Final inventory:    {session['inventory'].iloc[-1]} shares @ ${session['mid'].iloc[-1]:.2f}")

# ------------------------------------------------------------------
# Spread decomposition helper
# ------------------------------------------------------------------

def adverse_selection_cost(trades_df: pd.DataFrame,
                            mid_col='mid',
                            side_col='side',   # +1=buy, -1=sell
                            horizon=5) -> float:
    """
    Estimate adverse selection cost as E[mid_{t+h} - mid_t | buy at t].
    Positive = price moved against the MM (MM sold, price rose).
    """
    buys = trades_df[trades_df[side_col] == 1].index
    adverse_moves = []
    for i in buys:
        if i + horizon < len(trades_df):
            move = trades_df.loc[i + horizon, mid_col] - trades_df.loc[i, mid_col]
            adverse_moves.append(move)
    return np.mean(adverse_moves) if adverse_moves else 0.0
```

## Bridge to Quant / ML

- **Toxicity detection / VPIN:** VPIN (Volume-synchronized Probability of Informed trading) estimates the fraction of order flow that is informed. An ML classifier trained on recent order flow features (volume imbalance, trade size distribution, speed of arrivals) can predict when adverse selection risk is elevated — and the MM should widen spreads or pull quotes.
- **Optimal quoting as reinforcement learning:** The MM's quoting problem is naturally framed as an MDP. The state is (inventory, time remaining, recent order flow), the action is (bid/ask distance from mid), and the reward is P&L. Deep RL agents (PPO, SAC) have been trained on historical LOB data to learn dynamic quoting strategies.
- **Feature engineering from order flow:** Imbalance between bid-fills and ask-fills over short windows is a strong predictor of short-term price direction — the core of market microstructure ML research.
- **Price prediction from book state:** The current state of the [[Order Book]] (depth imbalance, bid/ask queue sizes) is predictive of short-term mid-price moves. Market makers use these predictions to skew their reservation price before the market moves.

## Self-Assessment

### Level 1 — Conceptual

**Q1.** What are the two components of the bid-ask spread according to microstructure theory?
> **A:** (1) Adverse selection component: compensation for trading against informed investors who have private information; (2) Inventory/order-processing component: compensation for holding unwanted inventory risk and the operational cost of quoting.

**Q2.** What is "adverse selection" in market making and why can't the market maker avoid it by simply widening the spread?
> **A:** Adverse selection means filling orders from traders with superior information, which causes losses when the price moves against the market maker after the trade. Widening the spread reduces adverse selection exposure but also drives away uninformed (profitable) flow — the market maker must balance between the two.

**Q3.** What does "toxicity" of order flow mean, and how can a market maker detect it?
> **A:** Flow toxicity = the proportion of informed/directional traders in the order flow. High toxicity means more adverse selection losses. Markers include: order imbalance (one-sided flow), accelerating trades in one direction, trades arriving faster than usual, and VPIN (volume-synchronized probability of informed trading) above a threshold.

### Level 2 — Quantitative

**Q4.** Using the Glosten-Milgrom model framework: if the probability of an informed trader is μ, the asset value is either V_H or V_L with equal probability, and informed traders always trade correctly, what is the minimum half-spread the market maker must charge?
> **A:** Half-spread = μ × (V_H - V_L) / 2. The market maker prices so that expected profit from uninformed flow (1-μ) × half-spread equals expected loss to informed flow μ × (V_H - V_L)/2. This gives the breakeven spread as a function of information asymmetry.

**Q5.** A market maker quotes a 2-tick spread and fills 10,000 trades per day. If 15% of trades are from informed traders and each informed trade costs 5 ticks on average, what is the daily P&L?
> **A:** Revenue from uninformed: 0.85 × 10,000 × 1 tick = 8,500 ticks. Loss from informed: 0.15 × 10,000 × (5 - 1) ticks = 6,000 ticks. Net = 2,500 ticks per day. If tick = $0.01, net = $25/day — very thin margins that require volume.

### Level 3 — Coding

**Q6.** Implement a simple order flow toxicity estimator (VPIN approximation): compute the volume-imbalance ratio over fixed-volume buckets and output a rolling VPIN estimate.

```python
import numpy as np
import pandas as pd

def compute_vpin(trades: pd.DataFrame, bucket_size: int = 1000,
                 n_buckets: int = 50) -> pd.Series:
    """
    Compute VPIN (Volume-synchronized Probability of Informed trading) estimate.
    
    Parameters
    ----------
    trades      : DataFrame with columns ['volume', 'side'] where side = +1 (buy) or -1 (sell)
    bucket_size : number of shares per volume bucket
    n_buckets   : number of most recent buckets to average
    
    Returns
    -------
    vpin : Series of VPIN estimates aligned to bucket boundaries
    """
    # TODO: Implement this function
    # Steps:
    # 1. Group trades into equal-volume buckets of size bucket_size
    # 2. For each bucket, compute buy volume V_B and sell volume V_S
    # 3. Order imbalance for bucket i = |V_B_i - V_S_i|
    # 4. VPIN = rolling mean of |V_B - V_S| / bucket_size over n_buckets
    # 5. Return VPIN series indexed by bucket number
    pass
```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Market makers only profit from the spread | They also lose to informed traders; the net P&L depends on the balance between spread capture and adverse selection losses |
| Wider spreads always mean more profit | Wider spreads deter uninformed flow; if you widen too much, volume drops and you earn less total |
| High-frequency market makers are just faster | Speed matters primarily for adverse selection avoidance (cancel before informed trader fills you), not just for more fills |
| Market making is risk-free | Inventory accumulation, adverse selection, and technological failures all create significant risk |

## Related Concepts

- [[Order Book]] — the venue where market maker quotes live
- [[Adverse Selection]] — the primary cost/risk for market makers
- [[Mean Reversion]] — the short-term price behavior that makes the MM's model reasonable
- [[Statistical Arbitrage]] — a related strategy at longer timescales

## Sources Used

- Cartea, A., Jaimungal, S., & Penalva, J. — *Algorithmic and High-Frequency Trading* (2015)
- Avellaneda, M. & Stoikov, S. — "High-Frequency Trading in a Limit Order Book" (2008), *Quantitative Finance*
- Glosten, L. R. & Milgrom, P. R. — "Bid, Ask and Transaction Prices in a Specialist Market" (1985), *Journal of Financial Economics*

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
