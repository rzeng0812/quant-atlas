---
type: concept
domain: 20-Markets
tags: [microstructure, markets]
status: math
stability: stable
confidence: medium
last_reviewed: 2026-04-12
review_interval_days: 365
sources:
  - "Cartea et al - Algorithmic and HFT"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Execution → Gap 3: Execution interacts with market microstructure — other participants respond to your trades
> **This concept:** Defines the data structure that mediates all trading — price levels, queued limit orders, and order matching rules that produce price impact and adverse selection.
> **Alternative approaches to this gap:** none (the order book is the mechanism, not a solution competing with alternatives)
> **You need first:** [[Price Impact]], [[Adverse Selection]]
> **This unlocks:** [[Market Making]], [[Avellaneda-Stoikov]], [[Almgren-Chriss]], [[TWAP-VWAP]]

> LOB: queued limit orders at each price level; market state

## Why This Exists

**The gap:** Before electronic markets, price discovery required a human specialist or open-outcry pit to match buyers with sellers. There was no transparent, persistent record of who wanted to trade and at what price.
**What came before:** Open-outcry and dealer markets, where a designated market maker set bid and ask prices. This created wide spreads and opaque pricing — buyers and sellers had no way to see the full queue of resting orders.
**What this adds:** The Limit Order Book is a public, real-time record of all resting buy and sell interest at each price level. It makes the supply-and-demand schedule of a stock visible, enables automated matching, and reduces spreads through transparent competition. Every price move and every execution cost can be traced directly to the state of the book.
**What it still doesn't solve:** The LOB is fragmented across venues (16+ US equity exchanges) and contains hidden "iceberg" orders. The visible book is an incomplete picture of true liquidity, and HFT participants respond to observable book state faster than most participants can.

## Math Concepts

**Two sides of the book**

| Side | Price ordering | Participants | Example |
|------|---------------|--------------|---------|
| Bid (buy) | Descending (highest first) | Buyers wanting to buy | "Buy 100 shares at \$184.90" |
| Ask (sell) | Ascending (lowest first) | Sellers wanting to sell | "Sell 50 shares at \$185.10" |

**Key quantities:**

- **Best bid ($b$):** Highest price at which someone is willing to buy.
- **Best ask ($a$):** Lowest price at which someone is willing to sell.
- **Mid-price:** $m = (a + b) / 2$ — the "fair value" estimate between the two sides.
- **Bid-ask spread:** $s = a - b$ — cost of immediately buying and selling.
- **Depth:** Volume available at each price level.

**Order types:**

| Type | Meaning | Priority |
|------|---------|----------|
| **Limit order** | "Buy at most X" or "Sell at least Y." Sits in book if not immediately fillable. | Price-time priority |
| **Market order** | "Buy/Sell immediately at best available price." | Fills against resting limits |
| **Cancel** | Removes an existing limit order from the book | — |

**Price-time priority (FIFO):**

At each price level, orders are filled first-come-first-served. If two orders both want to sell at \$185.10, the one that arrived earlier gets filled first. This incentivizes speed in HFT.

**Order book imbalance (OBI)**

A key microstructure signal:

$$\text{OBI}_t = \frac{V^b_t - V^a_t}{V^b_t + V^a_t}$$

where $V^b_t$ = total bid volume at best bid, $V^a_t$ = total ask volume at best ask.

- OBI near +1: heavy buy pressure → price likely to rise
- OBI near -1: heavy sell pressure → price likely to fall
- OBI near 0: balanced → no directional signal

**Market order walking the book:**

If the best ask has only 50 shares but you want to buy 200, your market order fills the first 50 at the best ask, then moves to the next ask level and fills the next available shares there, and so on. This is called "walking the book" and results in **price impact** (you pay a higher average price than the best ask).

**Average fill price for a market buy of size $Q$:**

$$\bar{P}(Q) = \frac{\sum_{k} p_k \cdot v_k}{\sum_k v_k}$$

where the sum is over consecutive ask levels $k$ until total volume $Q$ is filled.

**Implementation Shortfall (price impact):**

$$\text{IS} = \bar{P}(Q) - m_0$$

The difference between average fill price and mid-price at the time of the order. This is what large orders "cost" in terms of market impact.

## Walkthrough

**Snapshot of AAPL's order book at 10:30 AM:**

```
BID SIDE                    ASK SIDE
Price    Volume              Price    Volume
------   ------              ------   ------
$185.00   1,200  ← Best Bid  $185.10   800  ← Best Ask
$184.90   3,500              $185.20   2,400
$184.80   2,800              $185.30   1,600
$184.70   5,000              $185.40   4,200
$184.60   1,500              $185.50   3,000
```

- **Mid-price:** $(185.00 + 185.10) / 2 = \$185.05$
- **Spread:** $185.10 - 185.00 = \$0.10$
- **OBI (best level):** $(1200 - 800) / (1200 + 800) = 400/2000 = +0.20$ (mild buy pressure)

**Scenario 1: Small market buy order (500 shares)**

The order hits the ask side:
- Fill 500 shares at \$185.10 (ask has 800, so fills completely)
- Ask level at \$185.10 drops from 800 → 300
- Average fill price: \$185.10 exactly (no book-walking needed)
- Price impact: $185.10 - $185.05 = \$0.05 (half the spread)

New book state: Best ask is still \$185.10 but with 300 shares remaining.

**Scenario 2: Large market buy order (5,000 shares)**

This walks the book:

| Level | Price | Available | Filled | Cumulative |
|-------|-------|-----------|--------|-----------|
| 1 | \$185.10 | 800 | 800 | 800 |
| 2 | \$185.20 | 2,400 | 2,400 | 3,200 |
| 3 | \$185.30 | 1,600 | 1,600 | 4,800 |
| 4 | \$185.40 | 4,200 | 200 | 5,000 |

Average fill price: $(800×185.10 + 2400×185.20 + 1600×185.30 + 200×185.40) / 5000 = \$185.21$

Price impact: $185.21 - 185.05 = \$0.16$. The large buyer paid 16 cents above mid on average.

After the trade, the new best ask is \$185.40 at 4,000 shares. The ask side of the book has been significantly depleted.

**Scenario 3: Limit order arrives**

A seller posts: "Sell 1,000 shares at \$184.95."

Since $184.95 < $185.00\$ (best bid), this limit sell order is immediately filled against the resting bid at \$185.00. It's an **aggressive limit order** that acts like a market order. The bid at \$185.00 drops from 1,200 to 200 shares.

## Analysis

**What the order book reveals:**

- **Short-term price direction:** Book imbalance (OBI) is one of the strongest short-term price predictors available. When the bid side is much heavier than the ask, prices tend to tick up in the next few seconds.
- **Support and resistance:** Large clusters of limit orders at round numbers (e.g., \$185.00) act as support/resistance. These orders absorb incoming flow and slow down directional moves.
- **Hidden liquidity:** Most exchanges support "iceberg" orders — only a small portion of the total size is shown. The visible book understates available liquidity, which is why algorithms try to detect icebergs.

**Order book dynamics:**

The book constantly changes via:
1. **New limit orders** (additions at any price level)
2. **Cancellations** (removals; 90%+ of all limit orders are cancelled before being filled in modern markets)
3. **Market orders** (consume book liquidity)
4. **Trade executions** (reduction of a level's volume)

In HFT, orders live for microseconds. At US equities exchanges, roughly 95% of all limit orders are cancelled within a second.

**Fragmentation:**

Modern US equity markets are fragmented across 16+ trading venues (NYSE, NASDAQ, BATS, IEX, dark pools, etc.). The "consolidated order book" is not a single entity — order routing algorithms must synthesize it. This creates complexity and opportunity for arbitrage across venues.

## Implementation

```python
import heapq
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Optional, List, Tuple
import time

# ------------------------------------------------------------------
# Limit Order Book implementation
# ------------------------------------------------------------------

@dataclass
class Order:
    order_id: int
    side: str           # 'bid' or 'ask'
    price: float
    size: int
    timestamp: float = field(default_factory=time.time)

@dataclass
class Trade:
    aggressor_id: int   # market order or aggressive limit
    passive_id: int     # resting limit order
    price: float
    size: int


class PriceLevel:
    """Orders queued at a single price (FIFO)."""
    def __init__(self):
        self.orders: deque = deque()
        self.total_size: int = 0

    def add(self, order: Order):
        self.orders.append(order)
        self.total_size += order.size

    def remove_front(self, size: int) -> List[Tuple[Order, int]]:
        """Fill up to `size` shares from the front. Returns (order, filled) pairs."""
        fills = []
        remaining = size
        while self.orders and remaining > 0:
            order = self.orders[0]
            fill = min(order.size, remaining)
            fills.append((order, fill))
            order.size -= fill
            self.total_size -= fill
            remaining -= fill
            if order.size == 0:
                self.orders.popleft()
        return fills


class LimitOrderBook:
    """
    Simple Limit Order Book with price-time priority (FIFO per price level).
    
    Bids stored as max-heap (negate prices for Python's min-heap).
    Asks stored as min-heap.
    """

    def __init__(self):
        self._bids: dict = defaultdict(PriceLevel)  # price -> PriceLevel
        self._asks: dict = defaultdict(PriceLevel)
        self._bid_prices = []  # max-heap (negated)
        self._ask_prices = []  # min-heap
        self._orders: dict = {}  # order_id -> Order
        self._next_id = 1
        self.trades: List[Trade] = []

    # ---------- Public API ----------

    def add_limit_order(self, side: str, price: float, size: int) -> int:
        """
        Submit a limit order. Returns the order_id.
        Immediately matches against the opposite side if possible.
        """
        order_id = self._next_id
        self._next_id += 1
        order = Order(order_id, side, price, size)
        self._orders[order_id] = order

        if side == 'bid':
            # Can we fill immediately against resting asks?
            size = self._match_bid(order)
            if size > 0:  # remaining unmatched size
                order.size = size
                self._bids[price].add(order)
                heapq.heappush(self._bid_prices, -price)
        else:  # ask
            size = self._match_ask(order)
            if size > 0:
                order.size = size
                self._asks[price].add(order)
                heapq.heappush(self._ask_prices, price)

        return order_id

    def cancel_order(self, order_id: int) -> bool:
        """Cancel a resting limit order. Returns True if found and cancelled."""
        if order_id not in self._orders:
            return False
        order = self._orders.pop(order_id)
        level = self._bids[order.price] if order.side == 'bid' else self._asks[order.price]
        # Remove from deque (O(n) but acceptable for demo)
        try:
            level.orders.remove(order)
            level.total_size -= order.size
        except ValueError:
            pass  # already filled
        return True

    def market_order(self, side: str, size: int) -> Tuple[float, List[Trade]]:
        """
        Submit a market order. Returns (avg_fill_price, trades).
        """
        filled = 0
        total_cost = 0.0
        trades_this_order = []

        if side == 'buy':
            while size > 0 and self._ask_prices:
                best_ask = self._ask_prices[0]
                level = self._asks[best_ask]
                if level.total_size == 0:
                    heapq.heappop(self._ask_prices)
                    del self._asks[best_ask]
                    continue
                fills = level.remove_front(size)
                for order, qty in fills:
                    trade = Trade(-1, order.order_id, best_ask, qty)
                    self.trades.append(trade)
                    trades_this_order.append(trade)
                    filled += qty
                    total_cost += qty * best_ask
                    size -= qty
                if level.total_size == 0:
                    heapq.heappop(self._ask_prices)
                    del self._asks[best_ask]

        else:  # sell
            while size > 0 and self._bid_prices:
                best_bid = -self._bid_prices[0]
                level = self._bids[best_bid]
                if level.total_size == 0:
                    heapq.heappop(self._bid_prices)
                    del self._bids[best_bid]
                    continue
                fills = level.remove_front(size)
                for order, qty in fills:
                    trade = Trade(-1, order.order_id, best_bid, qty)
                    self.trades.append(trade)
                    trades_this_order.append(trade)
                    filled += qty
                    total_cost += qty * best_bid
                    size -= qty
                if level.total_size == 0:
                    heapq.heappop(self._bid_prices)
                    del self._bids[best_bid]

        avg_price = total_cost / filled if filled > 0 else 0.0
        return avg_price, trades_this_order

    # ---------- Book state ----------

    def best_bid(self) -> Optional[float]:
        while self._bid_prices and self._bids[-self._bid_prices[0]].total_size == 0:
            heapq.heappop(self._bid_prices)
        return -self._bid_prices[0] if self._bid_prices else None

    def best_ask(self) -> Optional[float]:
        while self._ask_prices and self._asks[self._ask_prices[0]].total_size == 0:
            heapq.heappop(self._ask_prices)
        return self._ask_prices[0] if self._ask_prices else None

    def mid_price(self) -> Optional[float]:
        b, a = self.best_bid(), self.best_ask()
        return (b + a) / 2 if b and a else None

    def spread(self) -> Optional[float]:
        b, a = self.best_bid(), self.best_ask()
        return a - b if b and a else None

    def order_book_imbalance(self) -> Optional[float]:
        b, a = self.best_bid(), self.best_ask()
        if not b or not a:
            return None
        vb = self._bids[b].total_size
        va = self._asks[a].total_size
        return (vb - va) / (vb + va) if (vb + va) > 0 else 0.0

    def snapshot(self, levels: int = 5) -> dict:
        bids = sorted(self._bids.keys(), reverse=True)
        asks = sorted(self._asks.keys())
        return {
            'bids': [(p, self._bids[p].total_size) for p in bids[:levels]
                     if self._bids[p].total_size > 0],
            'asks': [(p, self._asks[p].total_size) for p in asks[:levels]
                     if self._asks[p].total_size > 0],
        }

    # ---------- Internal matching ----------

    def _match_bid(self, order: Order) -> int:
        """Match incoming bid against resting asks. Returns remaining size."""
        size = order.size
        while size > 0 and self._ask_prices:
            best_ask = self._ask_prices[0]
            if order.price < best_ask:
                break
            level = self._asks[best_ask]
            fills = level.remove_front(size)
            for passive, qty in fills:
                trade = Trade(order.order_id, passive.order_id, best_ask, qty)
                self.trades.append(trade)
                size -= qty
            if level.total_size == 0:
                heapq.heappop(self._ask_prices)
                del self._asks[best_ask]
        return size

    def _match_ask(self, order: Order) -> int:
        """Match incoming ask against resting bids. Returns remaining size."""
        size = order.size
        while size > 0 and self._bid_prices:
            best_bid = -self._bid_prices[0]
            if order.price > best_bid:
                break
            level = self._bids[best_bid]
            fills = level.remove_front(size)
            for passive, qty in fills:
                trade = Trade(order.order_id, passive.order_id, best_bid, qty)
                self.trades.append(trade)
                size -= qty
            if level.total_size == 0:
                heapq.heappop(self._bid_prices)
                del self._bids[best_bid]
        return size


# ------------------------------------------------------------------
# Demo usage
# ------------------------------------------------------------------

lob = LimitOrderBook()

# Build initial book (mirroring the walkthrough)
for price, size in [(185.00, 1200), (184.90, 3500), (184.80, 2800)]:
    lob.add_limit_order('bid', price, size)

for price, size in [(185.10, 800), (185.20, 2400), (185.30, 1600), (185.40, 4200)]:
    lob.add_limit_order('ask', price, size)

print("Initial state:")
snap = lob.snapshot()
print(f"  Bids: {snap['bids']}")
print(f"  Asks: {snap['asks']}")
print(f"  Mid:  {lob.mid_price()}")
print(f"  Spread: {lob.spread():.2f}")
print(f"  OBI: {lob.order_book_imbalance():.4f}")

# Small market buy (500 shares)
avg_price, trades = lob.market_order('buy', 500)
print(f"\nMarket buy 500 shares: avg fill = ${avg_price:.4f}")
print(f"  Price impact: ${avg_price - 185.05:.4f}")

# Large market buy (5000 shares) — walks the book
avg_price2, trades2 = lob.market_order('buy', 5000)
print(f"\nMarket buy 5000 shares: avg fill = ${avg_price2:.4f}")
print(f"  Price impact: ${avg_price2 - 185.05:.4f}")
print(f"  Trades executed: {len(trades2)}")

print(f"\nAfter large buy, best ask: ${lob.best_ask()}")
```

## Bridge to Quant / ML

- **Order book features for ML:** The snapshot of the LOB (top N levels of bid/ask prices and volumes, OBI, spread, depth ratio) forms a rich feature vector for predicting short-term price moves. Academic papers show significant predictive power at sub-second horizons.
- **Deep LOB models:** Convolutional and recurrent neural networks trained on the full LOB (typically top 10 levels on each side, updated tick-by-tick) can outperform simpler OBI-based models for mid-price prediction. These are state-of-the-art microstructure ML models.
- **Event-based data:** The raw LOB data is not time-series but an event stream (order arrivals, cancellations, fills). Bar construction (tick bars, volume bars, dollar bars — per Lopez de Prado) from this stream is a key preprocessing step before applying any ML model.
- **Execution optimization:** Given a large order to execute, an RL agent can learn to slice the order optimally — trading aggressively when the book is deep and slowing down when the book is thin — to minimize implementation shortfall.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why does a large market order result in a higher average fill price than the best ask?
<details><summary>Answer</summary>A large market order exhausts the volume available at the best ask price level. Once that level is depleted, the order continues filling at the next ask level (which is higher), then the next, and so on. This process of "walking the book" means each successive tranche is filled at a worse price. The average fill price is a volume-weighted average across all the levels consumed, which is always above the best ask when the order size exceeds the best-ask quantity.</details>

**Q2.** What does a high positive Order Book Imbalance (OBI) signal about short-term price direction, and why?
<details><summary>Answer</summary>A high positive OBI means there is substantially more buy-side volume queued at the best bid than sell-side volume at the best ask. This imbalance means that incoming market sell orders will be absorbed more easily (deep bid), while incoming market buy orders will quickly exhaust the thin ask and push the price up. Empirically, a positive OBI predicts that the next mid-price tick is likely upward — it is one of the strongest microstructure signals at sub-second horizons.</details>

**Q3.** Why does price-time priority (FIFO) at each price level incentivize speed in HFT?
<details><summary>Answer</summary>At a given price level, the first order to arrive gets filled first. If the market maker who is first in the queue gets the fill (earning the spread), being slightly faster than competitors at the same price level is the difference between filling and not filling. This creates an arms race: each microsecond of latency advantage translates directly into queue position priority, which drives massive investment in co-location and low-latency infrastructure.</details>

---

### Level 2 — Quantitative

**Q4.** Using the AAPL book snapshot from the walkthrough (best bid \$185.00/1200 shares, best ask \$185.10/800 shares), compute the OBI and interpret the signal.
<details><summary>Answer</summary>$\text{OBI} = (1200 - 800)/(1200 + 800) = 400/2000 = +0.20$. This is a mild positive imbalance — the bid side is 50% heavier than the ask side at the best level. The signal suggests mild upward price pressure: incoming buy orders will exhaust the thin ask faster than sell orders will absorb the deeper bid. At a +0.20 OBI the signal is present but not strong; practitioners typically look for OBI > 0.5 or < −0.5 for confident directional signals.</details>

**Q5.** A market buy order for 3,000 shares arrives in the AAPL book from the walkthrough (ask side: 800@$185.10, 2400@$185.20, 1600@\$185.30). Compute the average fill price and implementation shortfall relative to the mid-price of \$185.05.
<details><summary>Answer</summary>The order fills: 800 shares at \$185.10, then 2,200 shares at \$185.20 (to reach 3,000 total). Average fill price = $(800 \times 185.10 + 2200 \times 185.20) / 3000 = (148,080 + 407,440) / 3000 = 555,520 / 3000 = \$185.173$. Implementation shortfall $= 185.173 - 185.05 = \$0.123$ per share, or about 6.6 basis points above mid. Note: the ask at \$185.20 still has 200 shares remaining after this fill.</details>

---

### Level 3 — Coding

**Q6.** The `LimitOrderBook` implementation uses a heap for price priority and a deque for time priority. What is the time complexity of adding a limit order, cancelling an order, and processing a market order of size $Q$ that walks through $k$ price levels?
<details><summary>Answer</summary>Adding a limit order: O(log P) for the heap push, where P is the number of distinct price levels. Cancellation: O(log P) to find the level, plus O(n) within the deque to find and remove the specific order (the implementation notes this is O(n) for demo purposes; production systems use an order_id → node pointer for O(1) removal). Market order walking k levels: O(k log P) for the heap pops per level, plus O(F) where F is the total number of individual fill events across all levels. In practice, the dominant cost for large orders is the matching loop, which is O(F).</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| A market order always fills at the best bid/ask | Only if the requested size is at most the volume available at that level. Larger orders walk to worse prices. |
| The order book shows all available liquidity | Dark pools, iceberg orders, and off-exchange volume are not visible. The displayed book is a lower bound on liquidity. |
| Cancelling an order before it fills has no cost | Cancellations dominate modern markets (95%+ of limit orders). However, sophisticated counterparties may infer information from your cancellation patterns. |
| High OBI always predicts the next price move | OBI is predictive on average but noisy. Order book manipulation (spoofing — placing large orders to move OBI then cancelling) can create false signals. |

## Related Concepts

- [[Adverse Selection]] — the risk market makers face from informed traders in the LOB
- [[Market Making]] — strategy built around posting quotes in the LOB
- [[Statistical Arbitrage]] — execution of two legs requires understanding LOB depth
- [[Price Impact]] — large orders walking the book directly create price impact

## Sources Used

- Cartea, A., Jaimungal, S., & Penalva, J. — *Algorithmic and High-Frequency Trading* (2015)
- Gould, M. D. et al. — "Limit Order Books" (2013), *Quantitative Finance*
- Cont, R., Stoikov, S., & Talreja, R. — "A Stochastic Model for Order Book Dynamics" (2010)

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review: replaced unknown wikilink [[Mean Reversion]] with [[Price Impact]] | quality-review |
