---
type: concept
domain: 20-Markets
tags: [crypto, defi, market-microstructure]
status: emerging
stability: emerging
confidence: medium
last_reviewed: 2026-07-26
review_interval_days: 180
sources:
  - "Uniswap v2/v3 whitepapers"
  - "A Unified General Formula for Arbitrary Liquidity Operations in Weighted AMMs (2606.22118)"
  - "Optimal Dynamic Fees for Automated Market Makers: A Stochastic Control Approach to Loss-Versus-Rebalancing (2606.21769)"
  - "Mitigating Adverse Selection in Concentrated Liquidity AMMs with Dynamic Fees (2606.23070)"
  - "Option Pricing on Automated Market Maker Tokens (2603.29763)"
created: 2026-07-26
---

> [!info] Problem Chain
> **Chain:** Market Structure → Gap: On-chain markets need continuous liquidity without a limit order book or human market maker
> **This concept:** AMMs replace the order book with a deterministic pricing function over pooled reserves, so anyone can trade against a pool at any time without a counterparty or a market maker actively quoting
> **Alternative approaches to this gap:** order-book-based DEXs (replicate [[Order Book]] matching on-chain or via off-chain relayers with on-chain settlement) — viable but require active quote maintenance and are far more gas-expensive per update than a passive AMM pool
> **You need first:** none — this is a foundational DeFi primitive
> **This unlocks:** concentrated liquidity design (Uniswap v3), dynamic AMM fee mechanisms, AMM-token option pricing, and [[MEV]] (sandwich attacks, arbitrage extraction against LPs)

## Why This Exists

**The gap:** A traditional exchange needs a continuous stream of two-sided quotes to function. On a blockchain, quoting requires submitting and cancelling transactions, each costing gas and settling with latency measured in blocks, not microseconds. A human or algorithmic market maker running an [[Order Book]] strategy on-chain would need to resubmit quotes every block just to stay at the current price — economically infeasible at scale, and it reintroduces a centralized operator into a system designed to avoid one.

**What came before:** Early attempts ported the limit order book directly on-chain (e.g., EtherDelta) or used off-chain order relay with on-chain settlement (0x). Both work, but liquidity is thin: passive limit orders decay in value as the market moves and must be actively managed, which requires sophisticated, capitalized participants — exactly the kind of intermediary DeFi tried to route around. Retail liquidity providers had no simple way to earn fees on idle capital.

**What this adds:** The constant-product AMM (Uniswap v2, 2020) replaces active quoting with a deterministic formula: a pool holds two reserves, and any trade must leave the product of the reserves unchanged ($x \cdot y = k$). The pool "quotes" a price purely as a function of its current reserve ratio — no one needs to submit or update an order. Anyone can deposit reserves proportionally and become a passive liquidity provider (LP), earning a pro-rata share of trading fees. Concentrated liquidity (Uniswap v3, 2021) refines this by letting LPs restrict their capital to a specific price range, dramatically increasing capital efficiency for liquidity provided near the current price.

**What it still doesn't solve:** the pricing function is mechanical and blind to information — it does not know when a trade is informed (someone trading on news the pool hasn't priced in yet) versus uninformed (a liquidity-driven swap). This blindness is what creates impermanent loss (a structural transfer of value from LPs to arbitrageurs whenever the external price moves) and exposes LPs and traders to MEV extraction such as sandwich attacks. Both remain active areas of AMM design research — see the Analysis section below.

## Math Concepts

### Constant-product invariant

A Uniswap v2-style pool holds reserves $x$ (of token X) and $y$ (of token Y) and enforces the invariant

$$x \cdot y = k$$

where $k$ is constant across trades (it only changes when liquidity is added or removed). The **spot price** of X in terms of Y is the marginal exchange rate:

$$p = \frac{y}{x} = \frac{dy}{dx}$$

**Swap math.** A trader sends $\Delta x$ of token X into the pool and receives $\Delta y$ of token Y out, subject to the invariant holding before and after (ignoring fees for now):

$$(x + \Delta x)(y - \Delta y) = xy = k$$

Solving for the output:

$$\Delta y = y - \frac{k}{x+\Delta x} = y - \frac{xy}{x + \Delta x} = \frac{y \, \Delta x}{x + \Delta x}$$

**Price impact / slippage.** The *effective* price paid, $\Delta y / \Delta x$, is worse than the pre-trade spot price $p = y/x$ because the trade itself moves the reserve ratio. Define the average execution price:

$$p_{\text{exec}} = \frac{\Delta y}{\Delta x} = \frac{y}{x + \Delta x}$$

so slippage relative to spot is

$$\text{slippage} = \frac{p - p_{\text{exec}}}{p} = 1 - \frac{x}{x+\Delta x} = \frac{\Delta x}{x + \Delta x}$$

Slippage grows monotonically with trade size relative to pool depth $x$ — this is the AMM analogue of [[Price Impact]], except here it is a deterministic, closed-form function of the invariant rather than an empirically estimated square-root law.

**Fees.** Uniswap v2 charges a fixed fee $\gamma$ (e.g., 0.3%) taken from the input: only $(1-\gamma)\Delta x$ is swapped, while the fee accrues to the pool (and thus to LPs) as extra reserves. The swap equation becomes

$$\Delta y = \frac{y\,(1-\gamma)\Delta x}{x + (1-\gamma)\Delta x}$$

### Weighted AMMs (generalization)

Constant-product is the equal-weight ($w_x = w_y = 0.5$) special case of the weighted constant-function invariant used by Balancer-style pools:

$$x^{w_x} y^{w_y} = k, \qquad w_x + w_y = 1$$

The unified-formula literature on weighted AMMs shows that the *same* invariant expression that prices swaps also governs liquidity operations (deposits/withdrawals, proportional or single-sided) — the invariant itself is the general allocation formula, and any non-proportional liquidity operation decomposes into an internal rebalancing swap plus a proportional operation. This is a structural property worth knowing even though this note focuses on the $w=0.5$ case: it explains why "just deposit reserves matching the current ratio" and "just swap" are not really two separate primitives — they are the same invariant evaluated at different points.

### Concentrated liquidity (Uniswap v3)

Uniswap v2 spreads an LP's capital over the *entire* price range $(0, \infty)$, most of which is never used (pools rarely trade at extreme prices). Uniswap v3 lets an LP concentrate capital into a chosen price range $[p_a, p_b]$, acting as if they held a v2-style constant-product position but with **virtual reserves** shifted so the real capital only covers that band.

Define **virtual reserves** $X, Y$ related to real reserves $x, y$ by an offset determined by the range bounds $[p_a, p_b]$. Within the active range, the position satisfies a constant-product-like relation in virtual terms:

$$(x + L/\sqrt{p_b})(y + L\sqrt{p_a}) = L^2$$

where $L$ is the position's **liquidity** — a single scalar summarizing size, defined so that a marginal move in $\sqrt{p}$ trades off against the real reserves exactly as in a v2 pool of depth $L$:

$$L = \frac{\Delta y}{\Delta \sqrt{p}} = \frac{-\Delta x}{\Delta(1/\sqrt{p})}$$

Integrating these relations over the position's range gives the real reserves backing a liquidity-$L$ position over $[\sqrt{p_a}, \sqrt{p_b}]$ at current price $p$ (with $\sqrt{p_a} \le \sqrt{p} \le \sqrt{p_b}$):

$$x = L\left(\frac{1}{\sqrt{p}} - \frac{1}{\sqrt{p_b}}\right), \qquad y = L\left(\sqrt{p} - \sqrt{p_a}\right)$$

Ticks are discrete, pre-defined values of $\sqrt{p}$ (spaced by a fixed basis-point step) that let the protocol track, in $O(1)$ per crossing, which liquidity is active at the current price. As price moves and crosses a tick boundary, liquidity ranges that end there drop out and new ones that start there become active — the pool's effective $k$ changes discretely at each tick crossing even though it's locally constant-product within a tick. Capital efficiency versus v2 is the ratio of "how much deeper does concentrated $L$ make the pool near $p$" versus spreading the same capital over $(0,\infty)$ — for tight ranges this multiplier can be 100x or more, which is the entire commercial case for v3.

### Impermanent loss (divergence loss) — full derivation

An LP deposits reserves worth $V_0 = 2\sqrt{xy}$ (value of a 50/50 constant-product position, in units of token Y, using $x_0, y_0$ with $x_0 y_0 = k$). Suppose the external market price of X (in Y) moves from $p_0 = y_0/x_0$ to $p_1 = p_0 \cdot k_r$, where $k_r$ is the **price ratio** $k_r = p_1/p_0$.

**Step 1 — where the pool ends up.** Arbitrageurs trade against the pool until its internal price matches the external price $p_1$ (ignoring fees). Because $x\cdot y = k$ is preserved and $p = y/x$, solving the two equations:

$$x_1 y_1 = k, \qquad \frac{y_1}{x_1} = p_1 \;\Rightarrow\; x_1 = \sqrt{\frac{k}{p_1}}, \quad y_1 = \sqrt{k\,p_1}$$

Since $k = x_0 y_0 = x_0^2 p_0$ (using $y_0 = x_0 p_0$):

$$x_1 = x_0\sqrt{\frac{p_0}{p_1}} = \frac{x_0}{\sqrt{k_r}}, \qquad y_1 = y_0\sqrt{\frac{p_1}{p_0}} = y_0\sqrt{k_r}$$

**Step 2 — value of the LP position vs. holding.** The LP's pool position, valued in token Y at the new price $p_1$:

$$V_{\text{pool}} = x_1 p_1 + y_1 = x_0\sqrt{k_r}\,p_0 \cdot\frac{1}{\sqrt{k_r}}\cdot\sqrt{k_r} + y_0\sqrt{k_r}$$

Simplify directly using $x_1 y_1 = k$ and $x_1 p_1 = y_1$ (pool is always balanced at its own spot price), so $V_{\text{pool}} = 2 y_1 = 2\sqrt{k p_1} = 2\sqrt{x_0 y_0 p_1} = 2 x_0 p_0 \sqrt{k_r} \cdot \frac{1}{\sqrt{p_0}}\cdot\sqrt{p_0}$. Cleaner: since $y_0 = x_0 p_0$,

$$V_{\text{pool}} = 2\sqrt{x_0 y_0 \, p_1} = 2\sqrt{x_0^2 p_0 \, p_1} = 2 x_0 p_0 \sqrt{p_1/p_0} = 2x_0 p_0 \sqrt{k_r} = V_0 \sqrt{k_r}$$

where $V_0 = 2x_0 p_0 = 2y_0$ is the initial position value in Y.

If instead the LP had simply **held** the original $x_0$ and $y_0$ (no pooling), the value at the new price is:

$$V_{\text{hold}} = x_0 p_1 + y_0 = x_0 p_0 k_r + x_0 p_0 = \frac{V_0}{2}(k_r + 1)$$

**Step 3 — Impermanent Loss.** Define $IL(k_r)$ as the proportional shortfall of the pool position relative to holding:

$$\boxed{IL(k_r) = \frac{V_{\text{pool}}}{V_{\text{hold}}} - 1 = \frac{2\sqrt{k_r}}{1+k_r} - 1}$$

This is always $\le 0$ for $k_r \neq 1$ (by AM-GM, $1 + k_r \ge 2\sqrt{k_r}$), and $IL(1) = 0$ (no price change, no loss). It is symmetric in $k_r \leftrightarrow 1/k_r$ — a price doubling and a price halving produce the same *proportional* loss, which is why "impermanent" loss is really a divergence loss: it depends only on how far price has moved from the deposit price, not on direction.

**Small-move approximation.** Let $k_r = 1 + \epsilon$ for small $\epsilon = \Delta p / p_0$. A second-order Taylor expansion of $2\sqrt{k_r}/(1+k_r)$ around $\epsilon = 0$ (verified symbolically) gives:

$$IL(\epsilon) \approx -\frac{1}{8}\epsilon^2 = -\frac{1}{8}\left(\frac{\Delta p}{p_0}\right)^2$$

The coefficient is exactly $1/8$, not $1/4$ — this holds whether $\epsilon$ is defined as the linear fractional change $(p_1-p_0)/p_0$ or the log price change $\ln(p_1/p_0)$; both expansions agree to second order. (Some informal write-ups round or misstate this as $-\tfrac14(\Delta p/p)^2$; treat the $1/8$ coefficient derived here as authoritative — it is also the coefficient that appears in the continuous-time Loss-Versus-Rebalancing rate $\text{LVR}_t \propto \tfrac18\sigma^2$, discussed below.) **Always compute the exact boxed $IL(k_r)$ formula for real position sizing** — the quadratic approximation is only for quick intuition on small moves (a few percent).

**Numeric anchors from the exact formula:**
- $k_r = 1.25$ (price up 25%): $IL = 2\sqrt{1.25}/2.25 - 1 \approx -0.62\%$
- $k_r = 2$ (price doubles): $IL = 2\sqrt2/3 - 1 \approx -5.72\%$
- $k_r = 4$ (price 4x): $IL = 2\cdot2/5 - 1 = -20\%$
- $k_r = 0.5$ (price halves): identical to $k_r=2$ by symmetry, $-5.72\%$

**Connection to LVR.** The dynamic-fees literature (Milionis et al.'s Loss-Versus-Rebalancing framework, extended in the stochastic-control fee paper referenced in Sources) reframes impermanent loss in continuous time: an LP is structurally short a claim that resembles a continuously-rebalanced portfolio, and the *rate* at which arbitrageurs extract value from the pool as price diffuses is proportional to $\sigma^2$ (instantaneous variance) times the pool's local depth. LVR is the continuous-time limit of the discrete IL derived above, and it is the quantity dynamic-fee mechanisms are explicitly designed to offset with fee revenue.

## Walkthrough

**Setup.** An ETH/USDC constant-product pool starts with $x_0 = 1{,}000$ ETH and $y_0 = 2{,}000{,}000$ USDC, so $k = 2 \times 10^9$ and spot price $p_0 = y_0/x_0 = \$2{,}000$/ETH. Pool fee $\gamma = 0.3\%$.

**Part 1 — price impact of a trade.** A trader wants to buy ETH with 50,000 USDC ($\Delta x_{\text{in}} = 50{,}000$ USDC in, receiving ETH out). Using the fee-adjusted swap formula with USDC as the input token (relabel $x=y_0=2{,}000{,}000$ pool-side reserve of USDC, $y=x_0=1000$ reserve of ETH, to keep the derivation above consistent — output is ETH):

$$\Delta(\text{ETH out}) = \frac{1000 \times (1-0.003)\times 50{,}000}{2{,}000{,}000 + (1-0.003)\times 50{,}000} = \frac{49{,}850{,}000}{2{,}049{,}850} \approx 24.32\text{ ETH}$$

Effective price paid: $50{,}000 / 24.32 \approx \$2{,}056.1$/ETH, versus spot $\$2{,}000$ - **slippage + fee $\approx 2.8\%$**. Using the no-fee slippage formula alone: $\Delta x/(x+\Delta x) = 50{,}000/2{,}050{,}000 \approx 2.44\%$, and the remaining ~0.3–0.4% is the trading fee plus the interaction between fee and curvature.

**Part 2 — impermanent loss on a price move.** Suppose ETH rallies from \$2,000 to \$2,800 (a $k_r = 1.4$ move). Using the boxed formula:

$$IL(1.4) = \frac{2\sqrt{1.4}}{2.4} - 1 = \frac{2 \times 1.1832}{2.4} - 1 = \frac{2.3664}{2.4} - 1 \approx -1.40\%$$

Concretely: the LP's initial \$4,000,000 position (1,000 ETH + 2,000,000 USDC) would be worth $V_{\text{hold}} = 1000\times2800 + 2{,}000{,}000 = \$4{,}800{,}000$ if simply held. The pool position is worth $V_{\text{pool}} = V_{\text{hold}} \times (1 + IL) = 4{,}800{,}000\times0.9860 \approx \$4{,}732{,}800$ - about **\$67,200 of divergence loss**, which trading fees earned over the holding period must exceed for the LP to come out ahead of simply holding the two assets.

## Analysis

**Impermanent loss is structural, not incidental.** As derived above, any external price move away from the LP's deposit price produces a mechanical shortfall versus holding — the pool is always trading away the appreciating asset and accumulating the depreciating one, because arbitrageurs only trade against it when it's profitable for *them*. This isn't a bug that better engineering removes; it is the LP's compensation-for-liquidity problem in a different form, directly parallel to the market maker's [[Adverse Selection]] cost in an [[Order Book]] — except here the "informed trader" is the price arbitrageur, and the AMM has no way to charge them a wider spread than an uninformed retail swapper.

**MEV and sandwich attacks compound the problem.** Because AMM trades and their prices are fully deterministic and visible in the mempool before settlement, a searcher can front-run a large swap (pushing the price against the victim), let the victim's trade execute at the worsened price, then back-run to capture the difference — a sandwich attack. This is a second, distinct channel of value extraction from AMM users (traders, not LPs directly) that has no analogue in a matched, sequential order book with price-time priority. The concentrated-liquidity adverse-selection literature models this together with LVR: the "Mitigating Adverse Selection in Concentrated Liquidity AMMs" agent-based model explicitly includes MEV searchers and latency-sensitive arbitrageurs alongside a Heston-driven reference price, and finds that *dynamic fees mainly compensate LPs for adverse selection (raising fee income when order flow looks toxic) rather than reducing realized LVR itself* — i.e., dynamic fees are a revenue lever, not primarily a mechanism that changes how much arbitrageurs can extract.

**Why dynamic, volatility-linked fees are an active research direction.** A static fee (e.g., Uniswap v2's flat 0.3%) is a blunt instrument: too low during high volatility and LPs get picked off by arbitrageurs faster than fee income compensates; too high during calm periods and volume (and fee revenue) is needlessly discouraged. The stochastic-control fee literature formalizes this as an ergodic control problem where the fee only affects the *drift* of LP wealth relative to a continuously-rebalanced benchmark, never its diffusion — yielding a clean result that the growth-optimal fee rises with instantaneous variance (pro-cyclical) and is invariant to the LP's risk aversion under log utility. This is a direct, quantitative answer to "how should fees respond to volatility," derived rather than heuristic.

**Why AMMs are still used despite these costs:**
- **Permissionless, passive liquidity provision.** Anyone can become an LP without active quote management — this is the entire value proposition versus an order book, and it remains true even with IL and MEV costs.
- **Composability.** AMM pools are simple on-chain primitives other DeFi protocols (lending, derivatives, aggregators) can call atomically, unlike an off-chain-matched order book.
- **Deep liquidity is achievable via concentration.** Uniswap v3-style ranges let sophisticated LPs (or automated vaults) approximate active market making with far less operational overhead than running order-book infrastructure, closing much of the capital-efficiency gap with CEXs.
- **Fee income, on net and in aggregate, has historically compensated many LPs** for realized IL in high-volume pairs — the economics are pair- and volatility-dependent, not universally negative, which is exactly why the optimal-fee research above matters.

## Implementation

```python
import numpy as np

def constant_product_swap(x_reserve, y_reserve, dx_in, fee=0.003):
    """
    Swap dx_in of token X into a constant-product pool, return (dy_out, new_x, new_y).
    x_reserve, y_reserve: pool reserves before the trade.
    fee: proportional fee taken from the input (e.g. 0.003 = 0.3%).
    """
    dx_after_fee = dx_in * (1 - fee)
    k = x_reserve * y_reserve
    new_x = x_reserve + dx_after_fee
    new_y = k / new_x
    dy_out = y_reserve - new_y
    # reserves actually held by the pool include the un-swapped fee remainder
    final_x = x_reserve + dx_in
    final_y = new_y
    return dy_out, final_x, final_y


def price_impact(x_reserve, y_reserve, dx_in, fee=0.003):
    """Slippage of the average execution price vs. pre-trade spot price."""
    spot = y_reserve / x_reserve
    dy_out, _, _ = constant_product_swap(x_reserve, y_reserve, dx_in, fee)
    exec_price = dy_out / dx_in
    return (spot - exec_price) / spot


def impermanent_loss(price_ratio):
    """
    Exact impermanent (divergence) loss as a function of price ratio k_r = p1/p0.
    Returns a negative fraction (e.g. -0.0572 for a 5.72% loss).
    """
    k_r = np.asarray(price_ratio, dtype=float)
    return 2 * np.sqrt(k_r) / (1 + k_r) - 1


def impermanent_loss_quadratic_approx(price_ratio):
    """Small-move approximation: IL(eps) ~= -1/8 * eps^2, eps = k_r - 1."""
    eps = np.asarray(price_ratio, dtype=float) - 1.0
    return -0.125 * eps**2


if __name__ == "__main__":
    x0, y0 = 1_000.0, 2_000_000.0  # 1,000 ETH / 2,000,000 USDC, spot = $2,000
    dy, fx, fy = constant_product_swap(y0, x0, 50_000, fee=0.003)  # buying ETH with USDC
    print(f"ETH received for 50,000 USDC: {dy:.4f} ETH")
    print(f"Price impact: {price_impact(y0, x0, 50_000, fee=0.003):.4%}")

    for k_r in [0.5, 0.8, 1.0, 1.25, 1.4, 2.0, 4.0]:
        exact = impermanent_loss(k_r)
        approx = impermanent_loss_quadratic_approx(k_r)
        print(f"k_r={k_r:.2f}  IL_exact={exact:.4%}  IL_quadratic_approx={approx:.4%}")
```

## Bridge to Quant / ML

- **AMM tokens as CEV processes.** "Option Pricing on Automated Market Maker Tokens" shows that when a token's *only* price discovery mechanism is a constant-product pool and net flow into the pool follows a diffusion, the resulting token price process is a constant elasticity of variance (CEV) process — nesting Black-Scholes as the infinite-liquidity limit. This gives closed-form option prices and liquidity-adjusted Greeks directly from AMM reserve dynamics, and predicts a leverage effect (volatility rises as price falls) whose implied-vol skew depends only on the pool's weighting parameter, not on pool depth — a testable, AMM-specific analogue of the equity volatility smile that [[Black-Scholes Model]] alone cannot generate.
- **LPing as a short-volatility, short-gamma position.** The exact $IL(k_r)$ derivation above is mathematically the payoff of writing a covered position that is short convexity in price — economically similar to a short straddle or short variance swap. This is why LVR analyses (and the dynamic-fee papers referenced here) treat fee income as compensation an LP must earn to offset a structurally short-vol exposure, directly analogous to how an option writer must be compensated by premium for gamma risk.
- **AMM fee-setting as Avellaneda-Stoikov-style inventory/quoting control.** The stochastic-control optimal-fee paper frames the AMM's fee as the on-chain analogue of the spread a market maker sets around a reservation price in [[Avellaneda-Stoikov]]: both are risk-compensation levers that must widen with volatility, and both trade off revenue-per-trade against adverse-selection cost from being picked off by better-informed counterparties. The mathematical machinery differs (ergodic HJB control on relative wealth here vs. inventory-driven quote skewing there), but the economic logic — quote wider (or charge more) exactly when informed flow is more likely — is the same.
- **Agent-based simulation as a research tool.** The adverse-selection/MEV paper's use of an agent-based model (heterogeneous arbitrageurs, searchers, LPs against a Heston reference price) is a template for how quant researchers evaluate microstructure mechanisms that don't have clean closed forms once realistic frictions (block latency, mempool visibility) are included — a complement to the closed-form LVR/CEV results above.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why does a constant-product AMM never need to "update its quote" the way a limit order book market maker does, and what is the cost of that convenience?
<details>
<summary>Answer</summary>
The AMM's price is fully determined by its current reserve ratio $y/x$ via the invariant $xy=k$ — there is no separate quote to maintain because the pricing function updates itself automatically the moment any trade changes the reserves. This removes the need for an active operator resubmitting orders every block. The cost is that the pool cannot distinguish informed from uninformed flow the way a discretionary market maker can widen spreads or pull quotes: it will always sell the arbitrageur exactly what the invariant dictates at the pre-trade price, even when that price is stale relative to the broader market. That structural blindness is the root cause of impermanent loss.
</details>

**Q2.** Why is "impermanent loss" arguably a misleading name, and what does the concentrated-liquidity / LVR literature prefer to call it?
<details>
<summary>Answer</summary>
"Impermanent" suggests the loss reverses if the price returns to its original level — which is true only if no further trading occurred and fees are ignored. In practice, once fees have been earned and paid out, or once the price has moved again, the loss from any given divergence period is realized and does not automatically undo itself. The LVR (Loss-Versus-Rebalancing) framing used in the dynamic-fee literature is preferred because it precisely defines the loss as the gap between the LP's realized position and what a continuously rebalanced portfolio holding the same target weights would have earned — a well-defined, path-dependent quantity rather than a vague "it might come back" framing.
</details>

**Q3.** Why does concentrated liquidity (Uniswap v3) increase capital efficiency, and what is the tradeoff for an LP who chooses a narrow price range?
<details>
<summary>Answer</summary>
In v2, capital is spread uniformly across all prices from 0 to infinity, most of which the pool will never actually trade at — that capital sits idle. In v3, an LP can commit capital only to a chosen band $[p_a, p_b]$ around the current price, so the same dollar amount produces much deeper liquidity (lower slippage) exactly where trading actually happens. The tradeoff is that if price exits the chosen range, the position becomes 100% one asset and stops earning fees until price re-enters the range (or the LP manually adjusts it) — narrower ranges earn more fee density per dollar when active, but require more active management and carry higher risk of falling "out of range," which increases both realized impermanent loss and the LP's opportunity cost of idle capital.
</details>

---

### Level 2 — Quantitative

**Q4.** A constant-product pool has 500 ETH and 1,500,000 USDC (spot price $3,000/ETH). A trader swaps in 20,000 USDC for ETH with a 0.3% fee. Compute the ETH received and the price impact including fees.
<details>
<summary>Answer</summary>

Using $x=1{,}500{,}000$ (USDC reserve), $y=500$ (ETH reserve), $\Delta x_{\text{in}} = 20{,}000$:

$$\Delta y = \frac{y \cdot (1-\gamma)\Delta x}{x + (1-\gamma)\Delta x} = \frac{500 \times 0.997 \times 20{,}000}{1{,}500{,}000 + 0.997\times20{,}000} = \frac{9{,}970{,}000}{1{,}519{,}940} \approx 6.559\text{ ETH}$$

Effective price: $20{,}000 / 6.559 \approx \$3{,}049.0$/ETH vs. spot \$3,000 — **price impact + fee $\approx 1.63\%$**.

Fee-free slippage alone: $\Delta x/(x+\Delta x) = 20{,}000/1{,}520{,}000 \approx 1.32\%$; the remaining ~0.3% is the trading fee.
</details>

**Q5.** Using the exact impermanent loss formula, compute the divergence loss if ETH falls from \$3,000 to \$2,100 (price ratio $k_r = 0.70$). Then compute IL for the *reciprocal* move, ETH rising from \$3,000 to \$4,285.71 (price ratio $k_r = 1/0.70 \approx 1.4286$). What does the comparison illustrate?
<details>
<summary>Answer</summary>

Fall to \$2,100: $k_r = 2100/3000 = 0.70$.
$$IL(0.70) = \frac{2\sqrt{0.70}}{1.70} - 1 = \frac{2\times0.8367}{1.70} - 1 \approx -1.57\%$$

Rise to \$4,285.71: $k_r = 4285.71/3000 \approx 1.4286$.
$$IL(1.4286) = \frac{2\sqrt{1.4286}}{2.4286} - 1 = \frac{2\times1.1952}{2.4286} - 1 \approx -1.57\%$$

The two losses are identical in proportional terms, even though a 30% drawdown and a ~42.9% rally look like very different price moves in percentage terms. This illustrates the $k_r \leftrightarrow 1/k_r$ symmetry proven algebraically above: IL depends only on the *ratio* of price divergence from the deposit price, not on direction. A naive comparison of "-30% vs. +30%" (i.e. $k_r=0.70$ vs. $k_r=1.30$) would *not* match, because $1.30 \neq 1/0.70$ — the symmetric counterpart of a 30% drawdown is not a 30% rally but a ~42.9% rally, since it's the reciprocal price ratio, not the reciprocal percentage change, that IL is symmetric under.
</details>

---

### Level 3 — Coding

**Q6.** In `constant_product_swap`, the function computes `new_x = x_reserve + dx_after_fee` (using the fee-adjusted input) but returns `final_x = x_reserve + dx_in` (using the full, pre-fee input) as the pool's actual new reserve. Why are these two different quantities, and why would using `new_x` instead of `final_x` as the pool's actual post-trade reserve be a bug?
<details>
<summary>Answer</summary>
The invariant $k = x \cdot y$ must only see the fee-adjusted amount, because the protocol fee is not "swapped" — it is retained by the pool as extra reserves that accrue to LPs rather than being used to compute the output amount. `new_x` (using `dx_after_fee`) is the correct quantity for computing how much Y to release, since only the post-fee amount participates in the constant-product exchange. But the pool's actual token X balance increases by the *full* `dx_in` the trader sent — the fee portion doesn't leave the pool, it just doesn't count toward the swap calculation. If you used `new_x` as the pool's real reserve going forward, you would silently discard the fee revenue: the next trade's invariant would be computed against a pool that never actually received the fee, understating $k$ and effectively giving away the accumulated fee income instead of letting it compound into LPs' claims.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Impermanent loss only happens if you withdraw at a loss | IL is a well-defined, continuously accruing shortfall versus holding the same assets outside the pool — it exists at every instant the price has diverged from the deposit price, whether or not you withdraw. "Impermanent" only means it can shrink if price reverts, not that it isn't real in the meantime, and any fees earned or further price moves can make it permanent in practice. |
| A 0.3% pool fee means LPs always net-earn 0.3% of volume regardless of volatility | Fee income and impermanent loss are separate, competing effects. In high-volatility regimes, LVR (the rate at which arbitrageurs extract value) can exceed fee revenue even at high trading volume — which is precisely why dynamic, volatility-linked fee schedules are an active research area rather than a solved problem. |
| Concentrated liquidity (v3) eliminates impermanent loss | It does not — it changes the LP's exposure profile (more fee density, more sensitivity to falling out of range) but the underlying divergence-loss mechanic versus holding is still present, and can be worse per dollar of capital if price exits the chosen range and the position becomes fully one-sided. |
| AMM slippage and traditional market impact are fundamentally different phenomena | They are the same economic idea — the cost of demanding immediacy from a finite pool of liquidity — expressed through different mechanisms. AMM slippage is a deterministic function of the invariant curve; [[Price Impact]] in order books is typically estimated empirically (e.g., the square-root law), but both describe execution price moving against the trader as size increases relative to available depth. |

## Related Concepts
- [[Market Making]] — the general economics of liquidity provision that AMMs replace with a deterministic algorithm
- [[Adverse Selection]] — the information-asymmetry cost that impermanent loss/LVR is the AMM-specific instance of
- [[Price Impact]] — the order-book analogue of AMM slippage
- [[Order Book]] — the alternative liquidity mechanism AMMs were designed to avoid needing
- [[Avellaneda-Stoikov]] — the market-making quoting framework whose volatility-widens-spread logic parallels AMM dynamic-fee design
- [[Black-Scholes Model]] — the infinite-liquidity limiting case of the CEV process that AMM-token prices follow

## Sources Used
- Uniswap v2 whitepaper (constant-product invariant, fee mechanics) and Uniswap v3 whitepaper (concentrated liquidity, ticks)
- Astarita, Guido, Shaffiee Haghshenas & Shaffiee Haghshenas — "A Unified General Formula for Arbitrary Liquidity Operations in Weighted AMMs" (arXiv:2606.22118)
- Ghasemlu — "Optimal Dynamic Fees for Automated Market Makers: A Stochastic Control Approach to Loss-Versus-Rebalancing" (arXiv:2606.21769)
- Di Nosse & Lillo — "Mitigating Adverse Selection in Concentrated Liquidity AMMs with Dynamic Fees: An Agent-Based Model Approach" (arXiv:2606.23070)
- Maymin — "Option Pricing on Automated Market Maker Tokens" (arXiv:2603.29763)

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-07-26 | Full content written | Content gap remediation — crypto/DeFi coverage |
