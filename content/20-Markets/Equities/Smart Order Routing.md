---
type: concept
domain: 20-Markets
tags: [microstructure, execution]
status: math
stability: stable
confidence: high
last_reviewed: 2026-07-30
review_interval_days: 365
sources:
  - "Ratliff-Crain, E., Van Oort, C. M., Koehler, M. T. K., & Tivnan, B. F. — Testing replication for an agent-based model of market fragmentation and latency arbitrage (2026), arXiv:2604.20067v1"
  - "Wah & Wellman (2016) — Latency Arbitrage, Market Fragmentation, and Efficiency: A Two-Market Model"
  - "SEC Regulation NMS (2005)"
created: 2026-07-30
---

> [!info] Problem Chain
> **Chain:** Market Structure → Gap: The same stock trades simultaneously on many competing venues with different fees, liquidity, and latency — a single order needs to decide not just when to trade (execution scheduling) but where
> **This concept:** Smart order routing algorithms decide how to split and sequence an order across venues to minimize total execution cost, given that venue fragmentation creates both beneficial price competition and exploitable cross-venue latency gaps
> **Alternative approaches to this gap:** Trading only on a single primary venue (simpler, but forgoes price improvement and liquidity available elsewhere — the pre-Reg-NMS baseline)
> **You need first:** [[Order Book]], [[Price Impact]], [[Adverse Selection]]
> **This unlocks:** cross-venue latency arbitrage strategies, dark pool venue selection

## Why This Exists

**The gap:** Since Regulation NMS (2005) in the US (and MiFID in Europe), equity trading is no longer concentrated on a single exchange. The same share of stock trades simultaneously on 10+ lit exchanges, dozens of dark pools and ATSs, and broker internalizers — each with its own fee schedule (maker/taker rebates that vary venue-to-venue), its own displayed and hidden liquidity, and its own latency to reach from any given point of origin. An order no longer has one obvious destination.

**What came before:** Before fragmentation, "where to trade" wasn't a decision — there was effectively one consolidated exchange (or a small number of regional exchanges with a dominant primary listing venue), and all execution-strategy effort went into *when* to trade (see [[TWAP-VWAP]], [[Almgren-Chriss]]). Early post-fragmentation practice was often a crude static rule: "always route first to the primary listing exchange," or a fixed percentage split across a handful of venues, ignoring real-time price, fee, and latency differences.

**What this adds:** Smart order routing (SOR) treats venue selection as its own optimization problem, layered on top of execution scheduling. Given a child order to release right now, an SOR algorithm dynamically evaluates the quoted price, fee/rebate, expected fill probability, and latency-driven risk at each candidate venue, and splits/sequences the order to minimize expected all-in cost subject to available liquidity. Because venues compete for order flow, fragmentation on its own is a source of *price improvement* — a router that shops across venues can systematically do better than one locked into a single destination.

**What it still doesn't solve:** The same fragmentation that creates competition also requires quotes across venues to be kept synchronized over finite-speed network links. Whenever one venue's price moves before another venue's quote catches up, a latency gap opens that a fast trader can exploit risklessly — this is *latency arbitrage*, and it is a direct structural cost of fragmentation, not a bug in any one venue's design. Whether the net effect of fragmentation on overall market quality (execution speed, investor welfare, price efficiency) is positive or negative turns out to be a genuinely contested empirical question. The most careful evidence available — an independent replication of the canonical agent-based model of this exact tradeoff — finds that the answer is highly sensitive to modeling assumptions that don't have an obviously "correct" choice. "Fragmentation is good" and "fragmentation is bad" are both defensible conclusions depending on details that are easy to get wrong, or to specify differently than the original researchers intended, without anyone realizing it. This note treats that unresolved tension as a first-class fact, not a footnote.

## Math Concepts

**1. Venue-selection cost model**

For a child order of size $q_v$ routed to venue $v$, the expected execution cost combines the quoted price, the venue's fee or rebate, and a latency-driven adverse-selection penalty for venues whose quotes may be stale relative to the fastest participants:

$$
\mathbb{E}[C_v(q_v)] = q_v \Big[\, \underbrace{P_v}_{\text{quoted price}} + \underbrace{f_v}_{\text{fee (}f_v<0\text{ = rebate)}} + \underbrace{(1-\pi_v)\,\kappa}_{\text{expected re-route cost of the unfilled portion}} + \underbrace{\delta_v}_{\text{latency-driven adverse-selection cost}} \Big]
$$

where $\pi_v \in [0,1]$ is the probability the order actually fills at venue $v$ (near 1 for a lit venue's displayed top-of-book; well below 1 for a dark pool, which offers no execution guarantee), $\kappa$ is the incremental cost of sweeping the unfilled residual to the next venue, and $\delta_v \geq 0$ is the expected cost of trading against a quote at $v$ that updates slowly relative to the fastest participants in the market (see part 2 below — this is exactly the loss a slow counterparty absorbs when a latency arbitrageur trades against a stale quote).

The router's problem, for a parent order of total size $Q$ arriving at $n$ venues with available liquidity $L_v$:

$$
\min_{\{q_v\}} \; \sum_{v=1}^{n} \mathbb{E}[C_v(q_v)] \quad \text{s.t.} \quad \sum_{v=1}^n q_v = Q, \quad 0 \le q_v \le L_v
$$

Because $\mathbb{E}[C_v(q_v)]$ is (to first order) linear in $q_v$ per unit of effective cost $P_v + f_v + (1-\pi_v)\kappa + \delta_v$, this is a transportation-style linear program: the cost-minimizing solution greedily fills the cheapest venue's available liquidity first, then the next-cheapest, and so on (a waterfall allocation) — see [[#Implementation]]. In reality venue cost is *not* flat in $q_v$ (a lit venue's price rises as you walk its book — see [[Order Book]], [[Price Impact]]), which is the main way this toy model diverges from a production SOR.

**2. Latency arbitrage mechanism (Wah & Wellman's two-market model, as replicated)**

The canonical formalization of the fragmentation/latency tradeoff comes from Wah & Wellman's (2016) two-market agent-based model, later independently replicated by Ratliff-Crain et al. The essential mechanism: a price-moving event occurs on venue $A$ at time $t_0$, shifting its price by $\Delta$. Venue $B$'s posted quote is not instantaneously aware of this — it reflects the *pre-shock* price until the cross-venue propagation latency $\tau$ elapses (the time for order flow / price information to travel from $A$ to $B$, e.g. via a slower consolidated feed versus a fast direct feed). A trader whose own message latency $\ell$ satisfies $\ell < \tau$ can:

1. Observe the shock on $A$ at $t_0$.
2. Route an order to $B$ that arrives before $\tau$ elapses.
3. Trade against $B$'s stale quote — buying at the old (now too-low) ask if $\Delta>0$, or selling at the old (now too-high) bid if $\Delta<0$ — for whatever depth $L_B^{\text{stale}}$ is still resting at that price.

The profit is capped by whichever binds first: the trader's desired size $Q_{\text{arb}}$, or the depth actually available at the stale quote:

$$
\Pi_{\text{arb}} = |\Delta| \cdot \min\!\big(Q_{\text{arb}},\, L_B^{\text{stale}}\big), \qquad \text{realizable iff } \ell < \tau
$$

This profit is, by construction, risk-free conditional on being fast enough — it is a pure transfer extracted from whoever was resting at the stale quote on $B$ (typically slower liquidity providers or uninformed background traders), funded entirely by the existence of a nonzero propagation latency $\tau>0$ between fragmented venues. If price shocks of this kind arrive as a Poisson process with rate $\lambda$ and mean absolute size $\mathbb{E}[|\Delta|]$, the arbitrageur's expected profit rate is approximately:

$$
\frac{\mathbb{E}[\Pi_{\text{arb}}]}{T} \approx \lambda \cdot \mathbb{E}[|\Delta|] \cdot \min\!\big(Q_{\text{arb}}, \bar L_B\big)
$$

— a standing "latency tax" that scales with how volatile the market is ($\lambda$, $|\Delta|$) and how long venues stay desynchronized ($\tau$, via which participants qualify as "fast enough").

**3. Sensitivity of the qualitative conclusion to the ZI "greedy strategy" (the replication paper's central finding)**

Wah & Wellman's model populates the background market with zero-intelligence (ZI) traders extended with a "greedy strategy" for routing: rather than mechanically using one fixed venue, a ZI trader evaluates both venues' current prices and routes toward the more favorable one. Ratliff-Crain et al. show that the model's headline qualitative conclusions — does fragmentation speed up or slow down execution, does it raise or lower trader welfare — are **not** invariant to how exactly this greedy rule is implemented. Write the aggregate outcome as a function of the routing rule $g$ and the fragmentation regime $F$ (fragmented vs. single consolidated market):

$$
\text{sign}\left(\frac{\partial\, T_{\text{exec}}(g, F)}{\partial F}\right), \qquad \text{sign}\left(\frac{\partial\, W(g, F)}{\partial F}\right)
$$

Under the original paper's implied interpretation of $g$, fragmentation's effect on execution time and welfare comes out one way; under an alternative, equally defensible interpretation of the same "greedy" rule, Ratliff-Crain et al. find fragmentation **decreases** execution times in *all* experiments and **increases** trader welfare in *most* experiments — the sign of both partial derivatives above flips depending on a modeling choice about agent behavior, not on any change to the market-structure parameters themselves ($\tau$, number of venues, fee structure). This is the paper's central methodological warning: a headline claim like "fragmentation harms execution quality" can be an artifact of one under-specified line in an agent's decision rule.

## Walkthrough

**Part A - Latency arbitrage profit.** Venue $A$ experiences a price shock of $\Delta = \$0.05$ (a large marketable order lifts the offer). The propagation latency to venue $B$'s quote is $\tau = 2\text{ms}$. A colocated fast trader has message latency $\ell = 0.3\text{ms} \ll \tau$, so the arbitrage window is exploitable. Venue $B$ has $L_B^{\text{stale}} = 500$ shares resting at the pre-shock price; the fast trader wanted to trade $Q_{\text{arb}} = 1{,}000$ shares.

$$
\Pi_{\text{arb}} = \$0.05 \times \min(1{,}000,\, 500) = \$0.05 \times 500 = \$25
$$

Only 500 of the desired 1,000 shares are captured — the arbitrage is capped by the depth resting at the stale quote, not by the trader's own capacity. The $25 is extracted risk-free from whoever was resting on $B$ at that price.

**Part B - Routing a 10,000-share buy order.** National best bid/offer is $50.00 \times \$50.02$. Three candidate venues:

| Venue | Price | Fee (taker) | Displayed/expected liquidity | Fill probability | Notes |
|---|---|---|---|---|---|
| A (lit) | \$50.02 | +\$0.0015/sh | 6,000 sh at this level | 0.98 | reliable, but walks the book beyond 6,000 |
| B (dark pool) | \$50.01 (midpoint) | −\$0.0005/sh (rebate) | ~3,000 sh (uncertain) | 0.60 | no execution guarantee |
| C (lit, quote known to lag) | \$50.015 | +\$0.0010/sh | 1,200 sh | 0.90 | elevated latency-arb exposure, $\delta_C = \$0.02$/sh |

*Route entirely to A:* the first 6,000 shares fill at \$50.02; the remaining 4,000 must walk to the next level, \$50.04.

$$
\bar P = \frac{6{,}000(50.02) + 4{,}000(50.04)}{10{,}000} = \frac{300{,}120 + 200{,}160}{10{,}000} = \$50.028
$$

Total cost $= 10{,}000 \times 50.028 + 10{,}000\times0.0015 = \$500{,}280 + \$15 = \$500{,}295$.

*Split across venues (avoiding C, the stale-quote venue, entirely — the SOR ranks by all-in effective cost $P_v+f_v+\delta_v$ and C is never competitive once its adverse-selection cost is priced in):*

- Send 3,000 to B. Expected fill $= 0.60 \times 3{,}000 = 1{,}800$ shares at $50.01 - 0.0005 = \$50.0095$: cost $= 1{,}800 \times 50.0095 = \$90{,}017.10$. The 1,200-share expected shortfall reroutes to A.
- Route the remaining $10{,}000-1{,}800=8{,}200$ to A: first 6,000 at \$50.02, next 2,200 walk to \$50.04.
  $$
  \bar P_A = \frac{6{,}000(50.02)+2{,}200(50.04)}{8{,}200} = \frac{300{,}120+110{,}088}{8{,}200} \approx \$50.0254
  $$
  Cost $= 8{,}200 \times 50.0254 + 8{,}200 \times 0.0015 \approx \$410{,}208.28 + \$12.30 = \$410{,}220.58$.

Total split-routing cost $\approx \$90{,}017.10 + \$410{,}220.58 = \$500{,}237.68$, versus $\$500{,}295$ for routing entirely to A - a saving of about **\$57**, or roughly **1.15 bps** on the notional. Modest per order, but this is exactly the margin SOR is fighting for at scale, and it is realized only because the router exploited venue competition (B's midpoint price and rebate) while explicitly steering the order *away* from venue C, whose better headline price ($50.015$ < A's $50.02$) is more than offset by its latency-driven adverse-selection cost.

## Analysis

**The reproducibility problem in market-microstructure ABMs.** Ratliff-Crain et al. set out to independently replicate Wah & Wellman's (2016) model and found that faithful replication was hindered by missing implementation details and limited quantitative reporting in the original paper — details as basic as exact parameterizations and distributional assumptions were not fully specified in the published text. This is not a criticism specific to Wah & Wellman; it is a structural feature of a lot of published agent-based market-structure research, where a compact paper cannot fully specify every line of simulation logic, and where reviewers rarely demand released, runnable code as a condition of publication. The lesson generalizes well beyond this one paper: treat any single agent-based-modeling result in market microstructure as provisional until you can either reproduce it from a full spec/codebase or bound it with your own sensitivity analysis.

**Relational equivalence, not quantitative alignment.** To make replication rigorous despite the missing details, Ratliff-Crain et al. ran more simulation trials than the original study and used bootstrap confidence intervals to test quantitative alignment properly — a methodological upgrade the original paper's reporting didn't support on its own. Combining the paper's text with a codebase the original authors later released for a follow-up study, they achieved *relational equivalence* for most metrics (the replicated model moves in the same direction as the original — e.g., more latency arbitrage opportunity as $\tau$ grows) but explicitly *reject quantitative alignment* whenever latency is non-zero. In other words: even reproducing the original authors' own model, with their own released code, the exact magnitudes don't come back out. For anyone trying to use a published ABM result to calibrate real routing logic — e.g., "latency arbitrage costs us roughly X bps in this fragmentation regime" — this is a hard stop. The direction of an effect from a published market-structure ABM is usable; the specific number is not, without independent empirical measurement against your own venue set and latency profile.

**The greedy-strategy sensitivity as a general caution.** The most consequential finding is that the paper's own qualitative takeaways about fragmentation and latency arbitrage are sensitive to the specifics of a single design choice — how the ZI background traders' "greedy" venue-selection rule is interpreted. Under the alternative interpretation Ratliff-Crain et al. test, fragmentation decreases execution times in all experiments and increases trader welfare in most experiments — a result that, read on its own, would support "fragmentation is good for market quality." Read next to the original paper's framing, which emphasizes latency arbitrage as a cost of fragmentation, the two readings sit in tension without either being wrong on its own terms. Neither interpretation of the greedy rule is obviously the "correct" one; both are plausible readings of an underspecified strategy description. The right conclusion is not "fragmentation is good" or "fragmentation is bad" — it's that the sign of fragmentation's welfare effect in this class of model is not a robust, load-bearing fact you can extract from one paper. Anyone using agent-based market-structure results to argue for or against a specific market-structure policy (e.g., speed bumps, consolidated tape reform, minimum quote life rules) should demand the same sensitivity analysis Ratliff-Crain et al. performed before trusting the headline direction of the result.

## Implementation

```python
from dataclasses import dataclass
from typing import List


@dataclass
class Venue:
    name: str
    price: float                     # quoted price for this side of the trade
    fee: float                       # taker fee per share (negative = rebate)
    liquidity: int                   # displayed / expected available size
    fill_prob: float                 # probability a marketable order fills there
    adverse_selection_cost: float = 0.0   # extra expected cost from stale/slow quotes

    @property
    def effective_cost(self) -> float:
        """All-in expected cost per share if the order fills at this venue."""
        return self.price + self.fee + self.adverse_selection_cost


def smart_order_route(order_size: int, venues: List[Venue]) -> dict:
    """
    Greedy cost-minimizing allocator across fragmented venues.

    Ranks venues by all-in effective cost per share (price + fee +
    latency-driven adverse-selection cost), then waterfalls the order into
    the cheapest venue first. Each venue's *expected* fill is
    liquidity * fill_prob; any expected shortfall cascades to the next-
    cheapest venue -- mirroring how a real SOR sprays IOC child slices and
    immediately reroutes whatever doesn't fill.

    Simplification: treats each venue's cost as flat regardless of size
    routed to it (no book-walking within a venue). A production router
    must instead treat cost as convex in size per venue -- see the
    Level 3 Self-Assessment question below.
    """
    remaining = order_size
    allocation = {}
    total_cost = 0.0

    for v in sorted(venues, key=lambda v: v.effective_cost):
        if remaining <= 0:
            break
        expected_fillable = min(remaining, int(v.liquidity * v.fill_prob))
        if expected_fillable <= 0:
            continue
        allocation[v.name] = expected_fillable
        total_cost += expected_fillable * v.effective_cost
        remaining -= expected_fillable

    filled = order_size - remaining
    return {
        "allocation": allocation,
        "filled": filled,
        "unfilled": remaining,
        "total_cost": total_cost,
        "avg_price": (total_cost / filled) if filled > 0 else None,
    }


# Example: the Walkthrough scenario (Part B)
venues = [
    Venue("A_lit",   price=50.02,  fee=0.0015,  liquidity=6000, fill_prob=0.98),
    Venue("B_dark",  price=50.01,  fee=-0.0005, liquidity=3000, fill_prob=0.60),
    Venue("C_stale", price=50.015, fee=0.0010,  liquidity=1200, fill_prob=0.90,
          adverse_selection_cost=0.02),
]

result = smart_order_route(10_000, venues)
print(f"Allocation: {result['allocation']}")
print(f"Filled: {result['filled']} / Unfilled: {result['unfilled']}")
print(f"Total cost: ${result['total_cost']:,.2f}")
print(f"Avg price: ${result['avg_price']:.4f}")
```

## Bridge to Quant / ML

- **Complementary, not competing, with [[Almgren-Chriss]]:** Almgren-Chriss (and [[TWAP-VWAP]]) solve *when* to release each child order over the execution horizon to balance impact against timing risk. Smart order routing solves *where* to send each child order once it's released. A real execution algorithm is a stack of both layers — a scheduler produces a stream of child orders, and a router decides venue allocation for each one, using something close to the cost model in [[#Math Concepts]].
- **Routing to a stale-quote venue is an adverse-selection exposure:** Section 2 of [[#Math Concepts]] shows the latency-arbitrage mechanism is structurally identical to the informed-trader mechanism in [[Adverse Selection]] — in both cases, a faster/better-informed counterparty trades against a resting quote before it can update, extracting a risk-free (or informationally-driven) profit from whoever was left behind. An SOR that ignores this is effectively choosing to route child orders toward the counterparties most likely to pick it off.
- **Venue selection as a learned policy:** Static cost models like the one implemented here are a reasonable starting point, but real fill probabilities, effective spreads, and latency-arb exposure per venue are non-stationary and depend on current market state (volatility regime, time of day, recent fill history at each venue). Modern SOR increasingly frames venue selection as a contextual bandit or reinforcement-learning problem — the "arms" are venues, the context is the current order-book/market state, and the reward is realized execution cost — rather than a fixed rule table recalibrated periodically by hand.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** What's the difference between within-venue execution scheduling ([[TWAP-VWAP]], [[Almgren-Chriss]]) and across-venue smart order routing? Why do you need both?
<details>
<summary>Answer</summary>
Within-venue scheduling decides *when* to release quantity into a single market's order flow over time, to manage the impact-vs-timing-risk tradeoff. Smart order routing decides *where* — which of the many competing venues — each slice should be sent once you've decided to trade it right now. In a fragmented market you need both layers: a scheduler (e.g., Almgren-Chriss) determines the size and timing of each child order, and a router splits that child order across venues based on their current price, fee, liquidity, and latency characteristics. Neither replaces the other — a large parent order is typically sliced in time first, then routed across venues within each time slice.
</details>

**Q2.** Why does market fragmentation create both a competition benefit and a latency-arbitrage cost from the same underlying structural fact?
<details>
<summary>Answer</summary>
Fragmentation means the same instrument trades on multiple competing venues simultaneously. Competition among venues for order flow drives down fees, tightens effective spreads, and creates price-improvement opportunities — no single venue has a monopoly on liquidity, so a router that shops across venues can systematically do better than one locked into a single destination. But that same multiplicity requires quotes across venues to be kept synchronized over finite-speed data links. Whenever one venue's price moves before another venue's quote catches up, a latency gap opens that a fast trader can exploit risklessly by trading against the stale quote. Both effects are direct consequences of "more than one place to trade the same thing" — you cannot get the competition benefit without also opening the latency gap that funds arbitrage.
</details>

**Q3.** What does "relational equivalence but not quantitative alignment" mean in the context of the Ratliff-Crain et al. replication, and why should a practitioner care?
<details>
<summary>Answer</summary>
Relational equivalence means the replicated model reproduces the same qualitative *direction* of an effect as the original study (e.g., "more latency arbitrage opportunity as propagation delay grows"). Quantitative alignment means the actual numbers — magnitudes, specific profit levels, specific execution-time changes — match within statistical confidence bounds. Ratliff-Crain et al. found the former holds for most metrics but explicitly reject the latter whenever latency is non-zero, even when reproducing results using the original authors' own released code. A practitioner should take from this that published agent-based market-structure results are usable for direction ("does X make latency arbitrage worse or better") but should never be used to calibrate specific numeric assumptions (like "latency arb costs us N bps") for production routing logic — that has to be measured empirically against your own venues and latency profile.
</details>

---

### Level 2 — Quantitative

**Q4.** A price shock of $\Delta = \$0.08$ occurs on venue A. The propagation latency to venue B's quote is $\tau = 3\text{ms}$; a fast trader's message latency is $0.4\text{ms}$. Venue B has 800 shares resting at the stale price, and the trader wants to arbitrage 2,000 shares. Compute the realizable profit and explain why the full desired size isn't captured.
<details>
<summary>Answer</summary>
Since $0.4\text{ms} < 3\text{ms}$, the arbitrage window is exploitable. The realized size is capped by whichever binds first: desired size or stale depth: $\min(2{,}000, 800) = 800$ shares. Profit $= \$0.08 \times 800 = \$64$. The remaining 1,200 shares of the desired arbitrage size cannot be captured because venue B's stale quote only had 800 shares resting at that price before it updates (or before other fast participants consume it) - the constraint is the depth available at the stale price, not the arbitrageur's own capacity to trade.
</details>

**Q5.** Venue X quotes \$20.00 with a \$0.001 taker fee, 4,000 shares available, fill probability 1.0. Venue Y quotes \$19.995 with a \$0.0008 rebate, 1,500 shares available, fill probability 0.5. For a 3,000-share buy order, compute the greedy SOR allocation and average all-in price, and compare it to routing the entire order to X.
<details>
<summary>Answer</summary>
Effective cost: X $= 20.00 + 0.001 = 20.001$. Y $= 19.995 - 0.0008 = 19.9942$ (Y is cheaper). Greedy allocation sends to Y first: expected fillable $= \min(3{,}000, \lfloor 1{,}500 \times 0.5 \rfloor) = 750$ shares at $19.9942$, cost $= \$14{,}995.65$. Remaining 2,250 shares route to X: expected fillable $= \min(2{,}250, 4{,}000) = 2{,}250$ shares at $20.001$, cost $= \$45{,}002.25$. Total cost $= \$59{,}997.90$ on 3,000 shares, average price $\approx \$19.9993$. Routing entirely to X: $3{,}000 \times 20.001 = \$60{,}003.00$, average price $\$20.001$. The split saves about \$5.10, or roughly 0.85 bps - small in absolute terms but directionally consistent with the walkthrough: shopping the rebate/price-improved venue first, even at limited size, systematically beats a single-venue default.
</details>

---

### Level 3 — Coding

**Q6.** The `smart_order_route` function ranks venues once by `effective_cost` and then waterfalls allocation in that fixed order. What structural assumption does this make, and when does it break down?
<details>
<summary>Answer</summary>
It assumes each venue's cost per share is flat (constant) regardless of how much of the order is allocated to it — i.e., that price, fee, and fill probability don't change as size is routed there. This ignores within-venue price impact / book-walking (see [[Order Book]]): sending more than the top-of-book depth to a lit venue should raise the average price for the marginal shares beyond that level, and probing a dark pool with large size can itself leak information and change its effective fill probability for the remainder of the order. Because the function sorts venues once upfront, it can't detect that a venue's *marginal* cost has risen past another venue's marginal cost partway through allocation. A more realistic implementation would model each venue's cost as convex (increasing) in allocated size and use a priority queue that recomputes the cheapest next incremental slice at every step, re-ranking venues dynamically rather than committing to a single sorted order in advance.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Fragmentation across venues is unambiguously bad for market quality | The Ratliff-Crain et al. replication of Wah & Wellman shows this conclusion is highly sensitive to how a single agent-behavior detail (the ZI traders' "greedy" routing rule) is implemented — under one plausible interpretation, fragmentation actually decreases execution times in all experiments and increases welfare in most. Treat any single ABM's fragmentation verdict as conditional on its modeling choices, not a settled law of markets. |
| Smart order routing eliminates latency arbitrage risk | SOR reduces exposure by preferring venues with reliable, fast-updating quotes, but it cannot eliminate the underlying mechanism — any venue whose quote updates slower than a fast trader's message latency is exploitable regardless of how sophisticated the router sending orders there is. The arbitrage lives in the market structure, not in any one participant's order-placement logic. |
| More venues to route to always means better execution | Each additional venue adds optionality, but also fragments displayed liquidity and adds fee, rebate, and latency-monitoring complexity. Past some point the operational and adverse-selection cost of routing to more venues can outweigh the marginal price improvement, especially for small orders that don't need to sweep deep liquidity. |
| Published agent-based market-microstructure results can be taken as calibrated ground truth for real routing logic | Ratliff-Crain et al. show that even with the original authors' own released code, quantitative alignment fails whenever latency is non-zero — only "relational equivalence" (same direction, different magnitude) survives replication. Implementation details matter enormously; the specific numbers from a published ABM shouldn't be used to calibrate production routing parameters without independent empirical verification. |

## Related Concepts

- [[Order Book]] — the per-venue data structure an SOR must read to evaluate price and depth at each candidate destination
- [[Price Impact]] — why routing size to one venue rather than splitting it changes the realized cost
- [[Adverse Selection]] — the same stale-quote mechanism that drives latency arbitrage between venues
- [[Almgren-Chriss]] — the complementary within-venue execution-scheduling layer (when to trade) that SOR (where to trade) sits alongside
- [[TWAP-VWAP]] — benchmark execution schedules that SOR routes each child slice of

## Sources Used

- Ratliff-Crain, E., Van Oort, C. M., Koehler, M. T. K., & Tivnan, B. F. — "Testing replication for an agent-based model of market fragmentation and latency arbitrage" (2026), arXiv:2604.20067v1
- Wah, E. & Wellman, M. P. — "Latency Arbitrage, Market Fragmentation, and Efficiency: A Two-Market Model" (2016)
- U.S. Securities and Exchange Commission — Regulation NMS (2005)

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-07-30 | Full content written | Content gap remediation — market structure/execution coverage |
