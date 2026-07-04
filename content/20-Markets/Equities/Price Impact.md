---
type: concept
domain: 20-Markets
tags: [market-microstructure, impact, liquidity, capacity]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-12
review_interval_days: 365
sources:
  - "Almgren et al - Direct Estimation of Equity Market Impact (2005)"
  - "Kyle - Continuous Auctions and Insider Trading (1985)"
  - "Cartea et al - Algorithmic and High-Frequency Trading (2015)"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Execution → Gap 1: Naive execution destroys value / Gap 2: Need a principled framework for the impact-vs-timing-risk tradeoff
> **This concept:** Quantifies the cost of demanding immediacy — how much a large order moves the price against itself — using the square-root law and distinguishing temporary from permanent impact.
> **Alternative approaches to this gap:** [[Adverse Selection]] (permanent impact via information channel), propagator models (Bouchaud 2004)
> **You need first:** [[Order Book]]
> **This unlocks:** [[Almgren-Chriss]], [[TWAP-VWAP]], [[Transaction Cost Analysis]], [[Avellaneda-Stoikov]]

## Why This Exists

**The gap:** A trader with alpha needs to translate that alpha into executed positions. Naive execution — hitting the market with a large order — immediately erodes the alpha through the cost of moving the price.
**What came before:** Practitioners knew large orders were costly but had no rigorous model for *how* costly. Rules of thumb existed ("don't trade more than 10% of volume"), but there was no principled way to optimize the size-cost tradeoff or compute strategy capacity.
**What this adds:** The square-root law (Almgren et al. 2005) provides a quantitative model: temporary impact scales as $\sigma \eta \sqrt{Q/V}$ — a concave function of order size. This lets a quant compute the expected transaction cost for any execution schedule, determine the maximum strategy capacity before impact eats the alpha, and feed a cost model into an optimization like Almgren-Chriss.
**What it still doesn't solve:** The square-root law uses a single calibrated constant $\eta$ that varies across stocks, venues, and regimes. It does not model intraday volume patterns, cross-impact (trading one stock affecting correlated stocks), or the game-theoretic response of other participants who detect your order flow.

---

## Math Concepts

### Temporary vs Permanent Impact

For a trade of size $Q$ in a stock with ADV $V$ and daily volatility $\sigma$:

**Square-root law (temporary impact):**
$$
h(v) = \sigma \cdot \eta \cdot \sqrt{\frac{Q}{V}}
$$

where $\eta \approx 0.1$ to $0.3$ is an empirically calibrated constant (varies by stock and venue). This is the mid-price move caused by the trade.

**Permanent impact** (Kyle's lambda formulation):
$$
\Delta p^{\text{perm}} = \lambda \cdot Q
$$

where $\lambda$ is estimated from order flow regressions. Permanent impact is *linear* in size — each share carries the same price discovery cost.

**Full Almgren impact model:**

For a sell program of size $X$ over time horizon $T$, with trading rate $v(t) = \dot{x}(t)$:

$$
\text{Temporary: } \tilde{h}(v) = \epsilon \cdot \text{sgn}(v) + \eta \left(\frac{v}{V}\right)^{\beta}
$$

$$
\text{Permanent: } g(v) = \gamma \left(\frac{v}{V}\right)^{\alpha}
$$

Empirical studies find $\beta \approx 0.6$ (the "3/5 power law") and often approximate as $\beta = 0.5$ for tractability.

### Participation Rate and Impact Cost

Let the participation rate be $\rho = Q / (V \cdot T)$ where $T$ is the execution period in days.

**Cost as fraction of trade value (in bps):**
$$
\text{Impact}(\rho) \approx \sigma \cdot \eta \cdot \sqrt{\rho}
$$

So if $\sigma = 1.5\%$ per day, $\eta = 0.2$, and $\rho = 0.10$ (10% ADV):
$$
\text{Impact} = 0.015 \times 0.2 \times \sqrt{0.10} \approx 9.5 \text{ bps}
$$

### Bid-Ask Spread Component

Even with zero market impact, you pay half the spread on each trade. Total realized cost (implementation shortfall) is:

$$
\text{IS} = \underbrace{\frac{s}{2}}_{\text{half-spread}} + \underbrace{h(Q/V)}_{\text{impact}} + \underbrace{\text{timing risk}}_{\text{price drift}}
$$

### Capacity Formula

Given alpha (annualized) $\alpha$ and impact function, the capacity $C^*$ is roughly the notional where impact cost per round trip equals the expected alpha:

$$
\alpha \approx 2 \cdot \text{Impact}(C^* / \text{ADV}) \implies C^* \approx \frac{\alpha^2}{\eta^2 \sigma^2} \cdot \text{ADV}
$$

---

## Walkthrough

**Setup:** You manage a momentum strategy that turns over its \$100M book every 10 trading days. The target stock trades \$500M per day (ADV = \$500M). Daily volatility = 1.5%. Use \$\eta = 0.2$.

**Step 1: Participation rate.**

$Q = \$100M$, execution horizon = 10 days, so daily buy rate = \$10M/day.

$\rho = 10M / 500M = 0.02$ (2% of ADV).

**Step 2: Impact per trade.**

$$
h = 0.015 \times 0.2 \times \sqrt{0.02} = 0.015 \times 0.2 \times 0.141 \approx 4.2 \text{ bps}
$$

**Step 3: Annual impact cost.**

With 10-day holding period, the strategy makes about 25 round trips per year. Each round trip has two legs (buy + sell), so:

$$
\text{Annual impact} = 2 \times 4.2 \text{ bps} \times 25 = 210 \text{ bps} = 2.1\%
$$

If the gross alpha is 5%, net alpha after impact = 2.9%. Still positive — the strategy has capacity at \$100M.

**Step 4: At what size does the strategy break even?**

At $C^*$, annual impact $\approx$ gross alpha of 5%:

$2 \times 25 \times 0.015 \times 0.2 \times \sqrt{C^* / 500M} = 0.05$

Solving: $C^* \approx \$285M$ notional. Above that, the strategy destroys value.

---

## Analysis

**Key Assumptions:**

| Assumption | Reality |
|---|---|
| Square-root law is universal | Constant $\eta$ varies 3x across stocks/venues/market conditions |
| Temporary impact fully reverts | Partial reversion is common; reversion speed matters |
| Impact is symmetric (buy = sell) | Directional pressure creates asymmetry |
| ADV is stable | During stress events, ADV spikes but impact worsens |

**Failure Modes:**

- **Crowding**: Multiple funds trading the same signal amplify impact beyond single-fund models. The industry's aggregate $\rho$ is what matters, not yours.
- **Non-stationarity**: $\eta$ calibrated in normal markets underestimates crisis impact.
- **Concave returns to scale confusion**: Sub-linear impact tempts funds to grow. But the marginal impact of the last dollar grows as AUM rises, even if average impact looks fine.

**Extensions:**

- **Propagator models** (Bouchaud 2004): Model impact as a kernel that decays over time — captures the crossover between temporary and permanent.
- **Volume prediction**: Replace ADV with predicted volume (using intraday patterns) for finer-grained scheduling.
- **Cross-impact**: Trading one stock moves correlated stocks via hedger activity.

---

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

# ─── Square-root impact model ───────────────────────────────────────────────

def impact_bps(
    order_size_usd: float,
    adv_usd: float,
    daily_vol: float,
    eta: float = 0.20,
) -> float:
    """
    Estimate one-way price impact in basis points using the square-root law.

    Parameters
    ----------
    order_size_usd : float
        Size of the order in USD.
    adv_usd : float
        Average daily volume in USD.
    daily_vol : float
        Daily return volatility (e.g. 0.015 for 1.5%).
    eta : float
        Market impact coefficient (empirically ~0.1 to 0.3).

    Returns
    -------
    float
        Estimated impact in basis points (1 bp = 0.0001).
    """
    participation_rate = order_size_usd / adv_usd
    impact = daily_vol * eta * np.sqrt(participation_rate)
    return impact * 10_000  # convert to bps


# ─── Strategy capacity analysis ─────────────────────────────────────────────

def strategy_capacity(
    gross_alpha_annual: float,
    holding_period_days: int,
    adv_usd: float,
    daily_vol: float,
    eta: float = 0.20,
) -> dict:
    """
    Find the notional where round-trip impact consumes all gross alpha.

    Returns dict with capacity in USD and supporting diagnostics.
    """
    # annual turnover: each position is held for holding_period_days
    # assume full portfolio turns over each holding period
    turnovers_per_year = 252 / holding_period_days

    # binary search for capacity where 2 * impact * turnovers = gross_alpha
    lo, hi = 1e6, 10 * adv_usd
    for _ in range(60):
        mid = (lo + hi) / 2
        imp = impact_bps(mid, adv_usd, daily_vol, eta) / 10_000
        annual_cost = 2 * imp * turnovers_per_year
        if annual_cost < gross_alpha_annual:
            lo = mid
        else:
            hi = mid

    capacity = (lo + hi) / 2
    imp_at_cap = impact_bps(capacity, adv_usd, daily_vol, eta)

    return {
        "capacity_usd": capacity,
        "participation_rate_at_cap": capacity / adv_usd,
        "impact_per_leg_bps": imp_at_cap,
        "annual_turnovers": turnovers_per_year,
    }


# ─── Plot impact vs participation rate ──────────────────────────────────────

def plot_impact_curve(adv_usd: float = 500e6, daily_vol: float = 0.015):
    rhos = np.linspace(0.001, 0.30, 500)
    sizes = rhos * adv_usd
    impacts = [impact_bps(s, adv_usd, daily_vol) for s in sizes]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(rhos * 100, impacts, lw=2, color="#1f77b4")
    ax.axvline(10, ls="--", color="gray", label="10% ADV")
    ax.axhline(10, ls=":", color="red", label="10 bps threshold")
    ax.set_xlabel("Participation Rate (%)")
    ax.set_ylabel("Impact (bps)")
    ax.set_title("Square-Root Impact vs Participation Rate\n"
                 f"ADV=${adv_usd/1e6:.0f}M, σ={daily_vol*100:.1f}%/day")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    return fig


# ─── Example run ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Single trade
    imp = impact_bps(order_size_usd=50e6, adv_usd=500e6, daily_vol=0.015)
    print(f"Impact for $50M order (10% of $500M ADV): {imp:.1f} bps")

    # Capacity analysis
    result = strategy_capacity(
        gross_alpha_annual=0.05,   # 5% gross alpha
        holding_period_days=10,
        adv_usd=500e6,
        daily_vol=0.015,
    )
    print(f"\nStrategy capacity: ${result['capacity_usd']/1e6:.0f}M")
    print(f"Participation rate at capacity: {result['participation_rate_at_cap']*100:.1f}%")
    print(f"Impact per leg at capacity: {result['impact_per_leg_bps']:.1f} bps")

    # Plot
    plot_impact_curve()
    plt.show()
```

---

## Bridge to Quant / ML

**ML for impact estimation:**
- Features: order size, normalized by ADV, intraday volume forecasts, volatility regime, bid-ask spread, order book depth.
- Target: realized implementation shortfall on historical executions.
- Models: gradient-boosted trees work well; neural networks overfit without large proprietary datasets.
- Watch for: selection bias (you only observe your own executions, not counterfactual prices).

**RL for execution:** Models like Almgren-Chriss provide a baseline trajectory. Reinforcement learning agents (e.g., PPO or DQN) can learn adaptive policies that condition on real-time order book state — outperforming static schedules in non-stationary markets. [[Almgren-Chriss]] provides the training objective (minimize IS subject to risk constraint).

**Impact in backtesting:**
- Naive backtests assume you trade at the close price with no friction — this drastically overstates alpha.
- Realistic backtests apply per-trade impact using the square-root model, adjusted for participation rate.
- Even better: use slippage models calibrated to your own historical execution data.

---

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** What is the difference between temporary and permanent price impact? Which one is associated with informed trading?
<details><summary>Answer</summary>Temporary impact is the transient price move caused by demanding immediacy — once you stop trading, market makers step back in and prices partially recover (like a foam cushion rebounding). Permanent impact is the lasting price change that remains after you finish — it occurs because your trading revealed genuine information about the asset's value, causing other market participants to permanently reprice. Permanent impact is associated with informed trading: if you are trading on a signal, the market infers from your order flow that the current price is too low (for buys), and re-prices upward permanently.</details>

**Q2.** Why does the square-root law have a concave (sub-linear) relationship between order size and impact? What does this imply about strategy scalability?
<details><summary>Answer</summary>Impact grows as $\sqrt{Q/V}$ because liquidity is not fully elastic. As you consume the order book, you deplete progressively deeper (cheaper) liquidity layers, but fresh limit orders arrive over time to replenish shallow layers. The replenishment rate caps the marginal impact of each additional share, producing a concave curve. For strategy scalability, this means: doubling AUM multiplies impact by $\sqrt{2} \approx 1.41$, so costs grow faster than linearly when measured as a fraction of capacity. Beyond the breakeven capacity $C^*$, the marginal alpha of each additional dollar is negative.</details>

**Q3.** What is "crowding" in the context of market impact, and why does a single fund's private impact model fail when crowding is present?
<details><summary>Answer</summary>Crowding means multiple funds are trading the same signal and executing in the same direction at the same time. A single fund's impact model is calibrated on its own trading — it measures $\rho = Q_{own}/V$, the fund's own participation rate. But when 10 funds are all buying the same stock simultaneously, the aggregate order flow is far larger than any one fund's model sees. The true effective participation rate is much higher, impact is amplified, and the square-root law underestimates actual transaction costs. The fund's capacity estimate is overstated when crowding is ignored.</details>

---

### Level 2 — Quantitative

**Q4.** A strategy has gross alpha of 8% per year, holding period 5 days, and trades in a stock with ADV = \$200M, daily vol = 1.8%, \$\eta = 0.2$. What is the strategy capacity?
<details><summary>Answer</summary>Annual turnovers = 252/5 = 50.4. At breakeven capacity $C^*$: $2 \times 50.4 \times \text{Impact}(C^*/\text{ADV}) = 0.08$. Impact per leg $= 0.018 \times 0.2 \times \sqrt{C^*/200M}$. Solving: $2 \times 50.4 \times 0.018 \times 0.2 \times \sqrt{C^*/200M} = 0.08$ → $0.3629 \times \sqrt{C^*/200M} = 0.08$ → $\sqrt{C^*/200M} = 0.2204$ → $C^*/200M = 0.04857$ → $C^* \approx \$9.7M$. The strategy has relatively low capacity because of the short holding period (high turnover).</details>

**Q5.** Using the square-root law with $\sigma = 1.5\%$/day and $\eta = 0.2$, compute the one-way impact in bps for participation rates of 1%, 5%, 10%, and 20%. Comment on the sub-linear scaling.
<details><summary>Answer</summary>$\text{Impact} = 0.015 \times 0.2 \times \sqrt{\rho} \times 10000$ bps. At 1% ($\rho=0.01$): $0.003 \times 0.1 \times 10000 = 3.0$ bps. At 5%: $0.003 \times 0.2236 \times 10000 = 6.7$ bps. At 10%: $0.003 \times 0.3162 \times 10000 = 9.5$ bps. At 20%: $0.003 \times 0.4472 \times 10000 = 13.4$ bps. Doubling from 5% to 10% adds 2.8 bps; doubling from 10% to 20% adds 3.9 bps. The incremental cost grows sub-linearly — but it still grows, so marginal cost is always positive.</details>

---

### Level 3 — Coding

**Q6.** The `strategy_capacity` function uses binary search to find the breakeven capacity. Why is binary search valid here (what property of the impact function guarantees a unique crossing point)?
<details><summary>Answer</summary>The annual impact cost $= 2 \times \text{turnovers} \times \sigma \eta \sqrt{C/\text{ADV}}$ is a strictly increasing, continuous function of $C$ (the square root is monotonically increasing). The gross alpha $\alpha$ is a constant. Since impact starts at 0 when $C=0$ and grows without bound, while alpha is fixed, there is exactly one crossing point $C^*$ where they are equal. This guarantees the binary search converges to a unique root. The `lo`/`hi` bounds are initialized at \$1M (well below breakeven for any realistic \$\alpha\$) and \$10 \times \text{ADV}$ (well above — no strategy can profitably trade its entire ADV daily).</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Impact is linear in order size | Impact scales as $\sqrt{Q/V}$ — sub-linear. Doubling order size increases cost by ~41%, not 100%. |
| Temporary impact fully reverts | Partial reversion is typical; the reversion speed and fraction vary across stocks and conditions. |
| Low average participation rate means the strategy is safe to scale | Marginal impact grows as you scale even with low average $\rho$; and crowding can make effective $\rho$ much higher than your own. |
| You can measure your own alpha net of impact from backtests | Naive backtests trade at mid or close price. You must explicitly apply an impact model to get realistic net alpha. |

## Related Concepts

- [[Order Book]] — where impact originates; depth at each price level determines the cost of demanding liquidity
- [[Adverse Selection]] — permanent impact is one face of adverse selection from the market maker's perspective
- [[Almgren-Chriss]] — optimal execution model that explicitly minimizes impact cost + timing risk
- [[TWAP-VWAP]] — standard benchmarks that spread impact over time
- [[Avellaneda-Stoikov]] — market maker models impact via adverse selection into their spread
- [[Statistical Arbitrage]] — capacity constraints from impact are why stat-arb funds have AUM limits
- [[Mean Reversion]] — impact can create artificial mean reversion in your own P&L

---

## Sources Used

- Almgren, R., Thum, C., Hauptmann, E., & Li, H. (2005). *Direct Estimation of Equity Market Impact.* Risk.
- Kyle, A. S. (1985). *Continuous Auctions and Insider Trading.* Econometrica, 53(6), 1315–1335.
- Bouchaud, J.-P., Gefen, Y., Potters, M., & Wyart, M. (2004). *Fluctuations and Response in Financial Markets.* Quantitative Finance.
- Cartea, Á., Jaimungal, S., & Penalva, J. (2015). *Algorithmic and High-Frequency Trading.* Cambridge University Press.

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review: added missing Revision Log created entry | quality-review |
