---
type: concept
domain: 20-Markets
tags: [crypto, defi, market-microstructure, adverse-selection]
status: emerging
stability: emerging
confidence: medium
last_reviewed: 2026-07-26
review_interval_days: 180
sources:
  - "Imperfect Commitment in Maximal Extractable Value Auctions"
  - "Concave Continuation: Linking Routing to Arbitrage"
  - "The Viability of Blockchain Markets under Discrete Clearing and Paid Priority"
  - "Joint Exclusivity"
created: 2026-07-26
---

> [!info] Problem Chain
> **Chain:** Market Structure → Gap: Public, ordered blockchain mempools let anyone see a pending trade before it executes
> **This concept:** Maximal Extractable Value (MEV) is the profit an adversarial actor can extract by choosing what transactions go into a block and in what order — sandwich attacks are the canonical case, where an attacker frontruns and backruns a victim's visible AMM trade to capture the price impact the victim was about to pay for.
> **Alternative approaches to this gap:** private/encrypted mempools (hide the trade until inclusion), batch auctions with uniform clearing prices (remove ordering advantage entirely) — mentioned in Analysis, not developed here
> **You need first:** [[Adverse Selection]] and [[AMM Mechanics]] (constant-product market makers)
> **This unlocks:** smart order routing (choosing venues and slicing orders to minimize MEV exposure)

## Why This Exists

**The gap:** In a traditional exchange, an order sits in a matching engine that nobody outside the exchange can see before it executes. On a public blockchain, the opposite is true: a submitted transaction sits in a public mempool, visible to every node on the network, for the seconds or minutes it takes to be included in a block. Anyone watching the mempool can see exactly what trade is about to happen, at what size, and against which pool — before it happens. Worse, the entity that decides the final ordering of transactions within a block (historically the miner, now the block builder under Proposer-Builder Separation, PBS) has unilateral power to insert, reorder, or exclude transactions.

**What came before:** Early blockchain design treated transaction ordering as an afterthought — miners were assumed to order transactions arbitrarily (e.g., by gas price, to maximize their own fee revenue) with no adversarial intent beyond that. The mempool was treated as a queue, not a signal.

**What this adds:** MEV formalizes that visible, orderable transaction flow is an exploitable resource. A trader who can see a pending trade and control its position relative to their own transactions can extract value from it — by frontrunning it (trading ahead to move the price adversely), backrunning it (trading after to capture an arbitrage the pending trade creates), or sandwiching it (both at once). This turned block construction into a competitive market: **searchers** find MEV opportunities and bid for inclusion, **builders** assemble blocks that maximize the fees and MEV they can capture, and **proposers** (validators) sell the right to propose a block to the highest-bidding builder — the architecture now known as Proposer-Builder Separation (PBS). Priority Gas Auctions (PGAs) are the earlier, cruder mechanism: searchers bid up gas prices in public, in real time, to win ordering priority for the same opportunity, which is itself a race that burns value in gas.

**What it still doesn't solve:** MEV extraction is a direct, measurable tax on ordinary users — sandwich attacks alone have extracted hundreds of millions of dollars in cumulative victim losses. PBS professionalizes and centralizes extraction rather than eliminating it, and — as the "Imperfect Commitment" paper shows — the auction that allocates a block to a builder is not fully credible: a builder who observes a searcher's bundle has no protocol-level obligation to honor the auction outcome, and can defect by replicating the winning opportunity itself. Private mempools and encrypted mempools hide the trade from bots but concentrate trust in whoever operates them; batch auctions with uniform clearing prices remove the ordering advantage within a batch but don't eliminate MEV across batches or protect against auctioneer misbehavior. None of these fully closes the gap — they trade one form of extraction or one trust assumption for another.

## Math Concepts

**Setup: a constant-product AMM.** A pool holds reserves of token $X$ and token $Y$ with invariant

$$x \cdot y = k$$

Swapping $\Delta x$ of $X$ into the pool (fee-free, for tractability) returns

$$\Delta y = y - \frac{k}{x + \Delta x} = \frac{y\,\Delta x}{x+\Delta x}$$

This is the AMM price-impact function: the marginal exchange rate worsens as $\Delta x$ grows, because each unit traded moves the pool along the $xy=k$ curve.

**The sandwich attack.** A victim broadcasts a transaction to swap $\Delta x$ of $X$ for $Y$ against a pool with reserves $(x_0, y_0)$. An attacker watching the mempool inserts two transactions around it in the same block:

1. **Frontrun:** swap $a$ of $X$ into the pool *before* the victim's trade.
2. *(Victim's trade executes against the shifted pool.)*
3. **Backrun:** sell the $Y$ acquired in step 1 back into the pool *after* the victim's trade.

**Step 1 — frontrun.** Reserves move to $x_1 = x_0+a$, $y_1 = k/x_1$. The attacker receives

$$\Delta y_a = y_0 - y_1 = \frac{y_0\,a}{x_0+a}$$

**Step 2 — victim's trade.** Against the shifted pool $(x_1,y_1)$, the victim receives

$$\Delta y_{\text{victim}}(a) = \frac{y_1\,\Delta x}{x_1+\Delta x} < \Delta y_{\text{victim}}(0) = \frac{y_0\,\Delta x}{x_0+\Delta x}$$

The victim's **slippage from the attack** (as opposed to ordinary price impact) is $\Delta y_{\text{victim}}(0) - \Delta y_{\text{victim}}(a)$. Reserves are now $x_2 = x_1+\Delta x$, $y_2 = k/x_2$.

**Step 3 — backrun.** The attacker sells $\Delta y_a$ back into the pool $(x_2,y_2)$, receiving $\Delta x_{\text{back}} = x_2 - \dfrac{k}{y_2+\Delta y_a}$.

Substituting through (with $A \equiv x_0+a$, $B \equiv x_0+a+\Delta x = A+\Delta x$), the algebra collapses to a clean closed form for gross attacker profit:

$$\boxed{\Pi(a) = \Delta x_{\text{back}} - a = \Delta x - \frac{\Delta x\,x_0^2}{(x_0+a)^2 + a\,\Delta x}}$$

**Key structural result.** $\Pi(a)$ is **strictly increasing and concave in $a$**, and satisfies $\lim_{a\to\infty}\Pi(a) = \Delta x$. In a fee-free CPMM with unlimited capital, a sandwich attacker can extract an arbitrarily large *fraction* of the victim's trade value, but never more than the trade's own size — and each additional dollar of frontrun capital buys diminishing marginal profit. This means there is **no interior optimum from the AMM math alone**: absent other constraints, more capital is always weakly better. Two real constraints create the actual binding optimum searchers use in practice:

- **Slippage tolerance (the operative constraint).** Every swap carries a `minOut` — the smallest output the trader will accept before the transaction reverts. The attacker rationally pushes $a$ up to (but not past) the point where the victim's trade still clears at exactly `minOut`. Setting $\Delta y_{\text{victim}}(a^*) = (1-s)\,\Delta y_{\text{victim}}(0)$ for tolerance $s$ and solving (using $y_1=k/x_1$) reduces to the elegant relation

$$x_1(x_1+\Delta x) = \frac{x_0(x_0+\Delta x)}{1-s}, \qquad a^* = x_1 - x_0$$

  a quadratic in $x_1$ solvable in closed form. This *is* the optimal frontrun size subject to not reverting the victim's trade — the binding constraint in practice, since a reverted victim transaction typically breaks the atomic bundle and kills the attack.
- **Fixed extraction cost.** Winning block-inclusion priority (the PGA bribe, or the builder tip under PBS) costs a roughly fixed amount $G$ per bundle, largely independent of $a$. The attack is worth firing only if $\Pi(a^*) > G$ — a threshold condition, not a size-optimization one. This is why sandwich bots ignore trades below a minimum size: the fixed cost dominates for small $\Delta x$.

## Walkthrough

Pool: 3,000,000 USDC and 1,000 ETH (spot price $3{,}000 / \text{ETH}$, $k = 3\times10^9$).

**Victim's trade:** swap 30,000 USDC for ETH, with a 1% slippage tolerance.

**Without attack:** victim receives $\dfrac{1{,}000\times30{,}000}{3{,}030{,}000} = 9.900990$ ETH, at an effective price of \$3,030/ETH (already worse than spot 3,000, due to ordinary AMM price impact — [[Price Impact]]).

**Victim's minOut:** $0.99 \times 9.900990 = 9.801980$ ETH.

**Optimal frontrun size.** Solving $x_1(x_1+30{,}000) = 3{,}000{,}000\times3{,}030{,}000 / 0.99$ gives $x_1 = 3{,}015{,}188.64$, so $a^* = 15{,}188.64$ USDC.

**Attacker's frontrun:** buys $\frac{1{,}000\times15{,}188.64}{3{,}015{,}188.64} = 5.037376$ ETH for 15,188.64 USDC. Pool is now $(3{,}015{,}188.64\text{ USDC}, 994.962624\text{ ETH})$.

**Victim's trade executes:** against the shifted pool, the victim's 30,000 USDC now buys exactly $9.801980$ ETH — precisely the minOut, so the transaction just clears (any larger frontrun would revert it).

**Victim's shortfall:** $9.900990 - 9.801980 = 0.099010$ ETH, worth about \$297 at spot — value the victim would have received in a fair, unordered market.

**Attacker's backrun:** sells the 5.037376 ETH back into the pool (now $3{,}045{,}188.64$ USDC / $985.199$ ETH after the victim's trade), receiving **15,491.61 USDC**.

**Attacker's gross profit:** $15{,}491.61 - 15{,}188.64 = \mathbf{302.97\ USDC}$ — captured entirely within one block, using capital the attacker gets back at the end of the same transaction bundle (flash-loanable).

**Profitability after gas:** the bundle costs a fixed priority fee/builder tip. At \$50 gas the attack nets \$252.97; at \$200 gas it nets \$102.97; above roughly \$303 gas it is not worth firing. This threshold — not an interior size optimum — is what determines whether small trades get sandwiched at all.

## Analysis

**Private and encrypted mempools.** If the victim's transaction is never visible in a public mempool (e.g., sent directly to a builder via Flashbots Protect, or encrypted until after ordering is committed via threshold encryption / SUAVE-style designs), the attacker cannot condition a frontrun on it. This closes the sandwich vector specifically but shifts trust to whoever operates the private channel — that operator can still see and act on the order, so it converts a *public* commitment problem into a *private* one.

**MEV-Boost / Proposer-Builder Separation (PBS).** Post-Merge Ethereum separates the roles of proposer (validator, chosen by stake) and builder (who assembles the block and competes for it). Builders run sealed-bid auctions among searchers for bundle inclusion and pay the proposer the winning bid via `MEV-Boost`. PBS professionalizes MEV extraction — it doesn't eliminate sandwiching, it consolidates who does it and adds competitive pressure that returns some of the surplus to proposers (and, via that, diffusely to the protocol) rather than letting it be fully captured by whichever searcher wins a chaotic public gas auction.

**PBS's own commitment problem.** This is where the grounding matters most: the "Imperfect Commitment in MEV Auctions" paper studies exactly the trust assumption PBS quietly relies on — that a builder honors the sealed-bid auction it ran. Nothing in the protocol forces this. A builder who observes a searcher's winning bundle can defect with some probability $\varepsilon$ and replicate a type-specific fraction $\gamma(\tau)$ of the MEV itself rather than including the searcher's bundle as submitted. Searchers, anticipating this, must choose between a risky first-price bid (which reveals the opportunity to a builder who might steal it) and a safer "deterrence" bid sized just large enough that frontrunning it is unprofitable for the builder. The paper's empirical result (estimating $\gamma(\tau)$ from bid-plateau data) is a sharp heterogeneity across MEV types: **sandwich opportunities are already so competitive among searchers that little surplus is left for a builder to steal**, whereas **naked arbitrage and liquidations leave substantially more surplus exposed** to builder defection, because fewer searchers are bidding it down. The upshot: a credible MEV auction needs more than a good auction *format* — it needs constraints on what a builder can do with information it observes but doesn't win, which current PBS does not fully provide.

**Priority Gas Auctions and paid-priority ordering more broadly.** Before PBS, competing searchers resolved conflicts over the same opportunity by bidding up gas price in public, in real time — a PGA. This burns value directly into miner/validator revenue (and gas waste from losing bids) rather than routing it through a cleaner sealed-bid mechanism. The "Viability of Blockchain Markets under Discrete Clearing and Paid Priority" paper generalizes this: because blockchains clear in discrete blocks and order by paid priority, only traders whose valuation clears a rising participation cutoff bother to compete at all — the cutoff rises with competition (more searchers, cheaper information) — which concentrates trading among the most aggressive, best-informed participants and *increases*, not decreases, the adverse selection that liquidity providers absorb in each clearing round. This is a structural, mechanism-level reason MEV and adverse selection are linked, not just an artifact of any one attack type: discrete, paid-priority clearing selects for exactly the informed, aggressive flow that hurts liquidity providers most, and longer block times make it worse.

**Batch auctions.** Clearing all orders in a batch at a single uniform price (as CowSwap and some L2 designs do) removes the within-batch ordering advantage that sandwich attacks rely on — there is no "before" and "after" the victim's trade within one clearing round. It does not eliminate MEV that arises across batches (e.g., which batch a transaction lands in, or arbitrage against external venues after the batch clears) and introduces its own design questions about who resolves ties and computes the clearing price.

**A tangential but real connection.** The "Joint Exclusivity" paper's framework for extremal negative dependence — structures where realizing one outcome excludes the interior of the joint support of others — offers language for modeling a fact searchers already treat as gospel: within a single block, at most one bundle can actually capture a given MEV opportunity (the first one included consumes the arbitrage or sandwich window; everyone else's identical bundle reverts or captures nothing). Competing searcher payoffs for the same opportunity are jointly exclusive in exactly this sense, which is part of why PGA/first-price competition dissipates so much of the extractable surplus into gas rather than into any one searcher's pocket.

## Implementation

```python
import math
from dataclasses import dataclass


@dataclass
class SandwichResult:
    frontrun_size: float          # X tokens attacker sells in (frontrun)
    frontrun_out: float           # Y tokens attacker receives (frontrun)
    victim_out_with_attack: float # Y tokens victim receives, post-attack
    victim_out_baseline: float    # Y tokens victim would have received, no attack
    backrun_out: float            # X tokens attacker receives (backrun)
    attacker_profit: float        # X tokens, gross of gas
    victim_shortfall: float       # Y tokens lost by victim vs baseline


def cpmm_swap_out(reserve_in: float, reserve_out: float, amount_in: float) -> float:
    """Constant-product swap: amount of `out` token received for `amount_in`
    of `in` token. No fee, matches x*y=k exactly."""
    k = reserve_in * reserve_out
    new_reserve_in = reserve_in + amount_in
    new_reserve_out = k / new_reserve_in
    return reserve_out - new_reserve_out


def max_frontrun_size(x0: float, y0: float, dx: float, slippage_tol: float) -> float:
    """Largest frontrun size `a` (in X) such that the victim's trade of size dx
    still clears at or above their minOut, i.e. does not revert.
    Solves x1*(x1+dx) = x0*(x0+dx) / (1 - slippage_tol) for x1 = x0 + a."""
    target = x0 * (x0 + dx) / (1 - slippage_tol)
    # x1^2 + dx*x1 - target = 0
    x1 = (-dx + math.sqrt(dx**2 + 4 * target)) / 2
    return x1 - x0


def simulate_sandwich(x0: float, y0: float, dx: float, frontrun_size: float) -> SandwichResult:
    """Simulate a sandwich attack on a constant-product pool (reserves x0, y0),
    where the victim swaps `dx` of token X for token Y, and the attacker
    frontruns with `frontrun_size` of X, then backruns by selling the Y back."""
    baseline_out = cpmm_swap_out(x0, y0, dx)

    # 1. Attacker frontrun: X -> Y
    frontrun_out = cpmm_swap_out(x0, y0, frontrun_size)
    x1, y1 = x0 + frontrun_size, y0 - frontrun_out

    # 2. Victim's trade executes against shifted reserves
    victim_out = cpmm_swap_out(x1, y1, dx)
    x2, y2 = x1 + dx, y1 - victim_out

    # 3. Attacker backrun: Y -> X (sell what was bought in step 1)
    backrun_out = cpmm_swap_out(y2, x2, frontrun_out)

    return SandwichResult(
        frontrun_size=frontrun_size,
        frontrun_out=frontrun_out,
        victim_out_with_attack=victim_out,
        victim_out_baseline=baseline_out,
        backrun_out=backrun_out,
        attacker_profit=backrun_out - frontrun_size,
        victim_shortfall=baseline_out - victim_out,
    )


# Example: 3,000,000 USDC / 1,000 ETH pool, victim swaps 30,000 USDC, 1% slippage tolerance
x0, y0 = 3_000_000.0, 1_000.0
dx = 30_000.0

a_star = max_frontrun_size(x0, y0, dx, slippage_tol=0.01)
result = simulate_sandwich(x0, y0, dx, a_star)

print(f"optimal frontrun size a*: {a_star:,.2f} USDC")          # 15,188.64
print(f"attacker gross profit:    {result.attacker_profit:,.4f} USDC")  # 302.9697
print(f"victim shortfall:         {result.victim_shortfall:.6f} ETH")   # 0.099010

for gas in [5, 50, 200, 500]:
    net = result.attacker_profit - gas
    print(f"  gas={gas:>4} USDC -> net={net:,.2f} USDC "
          f"({'profitable' if net > 0 else 'unprofitable'})")
```

## Bridge to Quant / ML

- **This is on-chain adverse selection, structurally.** The Kyle/Glosten-Milgrom lens (see [[Adverse Selection]]) treats a market maker's loss to informed order flow as the cost of not being able to distinguish informed from uninformed trades before pricing them. An AMM liquidity provider faces an even starker version: it *cannot* distinguish trades at all — its pricing function is fixed and mechanical ($x\cdot y=k$), so it cannot widen spreads pre-emptively the way a Glosten-Milgrom dealer does. A sandwich attacker is the purest possible "informed trader" in this framework: informed not about fundamental value, but about the victim's own order — a certainty rather than a signal. LP losses to sandwiching and to ordinary toxic flow (loss-versus-rebalancing) are both instances of the same adverse-selection mechanism Kyle's $\lambda$ was built to price, just with the information source being order-flow visibility rather than private fundamental knowledge.
- **The block-builder auction is a mechanism-design problem, not just a market-microstructure one.** Builders run sealed-bid, first-price-like auctions among searchers for bundle inclusion, then compete with each other (also roughly first-price) for the right to propose via MEV-Boost. Each layer has its own incentive-compatibility question: is the searcher-to-builder auction credible (the "Imperfect Commitment" finding — no, not fully, and the shortfall is quantifiable and type-dependent), and is the builder-to-proposer auction actually competitive or does it concentrate (empirically, block building is highly concentrated among a handful of sophisticated builders, a centralization pressure structurally similar to how HFT market-making concentrated among firms with the fastest adverse-selection detection).
- **Estimating extraction probability as a supervised-learning problem.** $\gamma(\tau)$ — the fraction of an MEV opportunity a defecting builder could replicate — is estimated empirically from bid-plateau structure in bundle auction data (the `libmev` dataset in the source paper). This is directly analogous to estimating Kyle's $\lambda$ from order-flow data: both are latent parameters of an adverse-selection/extraction process recovered from the shape of observed prices or bids, not observed directly.
- **Mempool/mempool-adjacent data as an ML feature source.** Pending-transaction size, gas price, and pool state are public, real-time features; sandwich-detection and MEV-protection products (e.g., simulating whether a pending swap is sandwichable before submission) are essentially adverse-selection classifiers running on mempool data instead of order-book data.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why is a sandwich attack possible on an AMM but not (easily) on a traditional exchange with a hidden order book?
<details>
<summary>Answer</summary>
A sandwich attack requires the attacker to know, before it executes, that a specific trade of a specific size is about to hit a specific pool — and to be able to insert transactions immediately before and after it. On a blockchain, pending transactions sit in a public mempool for seconds to minutes before inclusion, and the AMM's pricing function is deterministic and public ($x\cdot y=k$), so anyone can compute exactly how much the victim's trade will move the price and exactly how to position around it. On a traditional exchange, pending orders are not visible to other participants before they execute (no public "mempool" of resting orders), and even visible limit orders don't reveal market orders about to arrive. The attack requires both visibility of the pending trade and control over transaction ordering relative to it — blockchains uniquely provide both.
</details>

**Q2.** In the profit formula $\Pi(a) = \Delta x - \dfrac{\Delta x\,x_0^2}{(x_0+a)^2+a\Delta x}$, what happens as $a\to\infty$, and why doesn't this mean an attacker with infinite capital should use an infinite frontrun size?
<details>
<summary>Answer</summary>
As $a\to\infty$, $\Pi(a)\to\Delta x$: the attacker's profit asymptotically approaches (but never exceeds) the full size of the victim's trade. This might suggest "more capital is always better," and mathematically, on the AMM alone, that's true — $\Pi(a)$ is strictly increasing. But two real-world constraints cap it: (1) the victim's transaction has a slippage tolerance (`minOut`); push the price too far and the victim's trade reverts, which typically breaks the attacker's atomic bundle and captures nothing. (2) Capital has an opportunity cost and the attacker still has to win block-inclusion priority, whose cost is roughly fixed regardless of $a$ — so the decision to attack at all is a threshold condition ($\Pi(a^*) > \text{gas}$), not a size-optimization one, once $a^*$ is pinned down by the slippage constraint.
</details>

**Q3.** How does the "Imperfect Commitment" paper's finding that sandwich opportunities are highly competitive (while liquidations and naked arbitrage are not) change how you'd think about which MEV types are most at risk from a defecting builder?
<details>
<summary>Answer</summary>
Competition among searchers for the same opportunity bids the winning price up toward the opportunity's full value — leaving little surplus for anyone downstream (including a builder who might want to steal it) to capture. Sandwich attacks are targeted at essentially every large AMM swap and many bots race for each one, so the winning bid already captures most of the available value; there's little left on the table for a builder to profitably defect on. Liquidations and naked arbitrage opportunities are rarer, more idiosyncratic, and require more specialized capital or protocol knowledge, so fewer searchers compete for any given one — the winning bid is further from the opportunity's full value, leaving more surplus exposed if the builder observes the bundle and decides to replicate it rather than include it. This means "credible auction" guarantees matter least for the MEV type most people worry about (sandwiching) and most for the types that are harder to observe in aggregate MEV statistics.
</details>

---

### Level 2 — Quantitative

**Q4.** A pool has reserves $x_0 = 500{,}000$ USDC and $y_0 = 250$ ETH. A victim swaps $\Delta x = 10{,}000$ USDC for ETH with a 2% slippage tolerance. Find the victim's baseline output, their minOut, and the optimal frontrun size $a^*$.
<details>
<summary>Answer</summary>

Baseline: $\Delta y_{\text{victim}}(0) = \dfrac{250 \times 10{,}000}{510{,}000} = 4.901961$ ETH.

minOut: $0.98 \times 4.901961 = 4.803922$ ETH.

Optimal frontrun: solve $x_1(x_1+10{,}000) = \dfrac{500{,}000 \times 510{,}000}{0.98} = 260{,}204{,}081{,}632.65$.

$x_1^2 + 10{,}000\,x_1 - 260{,}204{,}081{,}632.65 = 0 \Rightarrow x_1 = \dfrac{-10{,}000+\sqrt{10{,}000^2+4\times260{,}204{,}081{,}632.65}}{2} \approx 505{,}126.53$

$a^* = x_1 - x_0 \approx 5{,}126.53$ USDC.

Note that here $a^*$ is *smaller* than $\Delta x$, unlike the walkthrough — because this pool is shallower relative to the trade size (10,000 / 500,000 = 2% of reserves, vs. 30,000 / 3,000,000 = 1% in the walkthrough) and the tolerance is looser (2% vs. 1%), so less frontrun capital is needed to push the price to the victim's minOut.
</details>

**Q5.** Using the pool and result from Q4, verify the profit formula gives a sensible profit, and determine whether the attack is worth executing if the total gas/priority-fee cost is 120 USDC.
<details>
<summary>Answer</summary>

$$\Pi(a^*) = \Delta x - \frac{\Delta x\,x_0^2}{(x_0+a^*)^2 + a^*\Delta x} = 10{,}000 - \frac{10{,}000\times500{,}000^2}{505{,}126.53^2 + 5{,}126.53\times10{,}000} \approx 203.92 \text{ USDC}$$

Since gross profit (\$203.92) exceeds the \$120 gas cost, the attack nets **\$83.92** and a rational searcher would fire it. Note that $\Pi(a^*)/\Delta x \approx 0.0204$, very close to the 2% slippage tolerance itself — this holds as a close approximation ($\Pi(a^*)/\Delta x \approx s$) whenever the victim's trade is small relative to pool depth, and is a convenient rule of thumb: **a victim's chosen slippage tolerance is approximately what they're offering an attacker, in percentage terms, whenever their trade doesn't already move the pool by much on its own.**
</details>

---

### Level 3 — Coding

**Q6.** In `simulate_sandwich`, the backrun step calls `cpmm_swap_out(y2, x2, frontrun_out)` — note the reserve arguments are passed as `(y2, x2)`, reversed from how `(x1, y1)` were passed for the frontrun and victim swaps. Why is this necessary, and what would go wrong if you called it as `cpmm_swap_out(x2, y2, frontrun_out)` instead?
<details>
<summary>Answer</summary>
`cpmm_swap_out(reserve_in, reserve_out, amount_in)` always expects the reserve of the token being *sold in* first and the reserve of the token being *bought out* second. In the frontrun and victim steps, the trader sells X and buys Y, so the call is `cpmm_swap_out(x, y, amount_of_X)`. In the backrun, the attacker sells Y (the ETH acquired in the frontrun) and buys back X (USDC), so the roles are reversed — Y is now the "in" token and X is the "out" token, and the call must be `cpmm_swap_out(y2, x2, frontrun_out)` to compute how much X comes out for that amount of Y in. If you called `cpmm_swap_out(x2, y2, frontrun_out)` instead, the function would incorrectly treat `frontrun_out` (an amount of ETH) as if it were being added to the USDC reserve, since it would use `x2` as `reserve_in`. That mismatches units — the constant-product formula would still return *a* number, but it would represent "how much Y comes out for `frontrun_out` units of X in," which is not the trade the attacker is actually making, silently corrupting the profit calculation.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Sandwich attacks require the attacker to know the victim's identity or intent | The attacker only needs to see the pending transaction's calldata (which pool, which direction, size, minOut) in the mempool. No identity or motive is needed — it's mechanical, automated, and runs on every sufficiently large swap that meets a profitability threshold. |
| More frontrun capital always means more attacker profit, without limit | True only in the idealized fee-free AMM math. In practice the victim's slippage tolerance caps how far the attacker can push the price before the victim's transaction reverts and the attack fails outright — this, not diminishing marginal returns alone, is the binding constraint on $a^*$. |
| PBS (MEV-Boost) eliminates MEV | PBS reorganizes who captures MEV — it moves competition from a chaotic public gas auction into a sealed-bid builder auction, returning some surplus to proposers — but sandwiching, arbitrage, and liquidations still occur, and the auction itself is not fully credible against a defecting builder (see the "Imperfect Commitment" grounding above). |
| MEV is a niche technical issue that only sophisticated traders should care about | Any AMM swap above a small size threshold is a candidate for sandwiching; the victim shortfall computed in the Walkthrough is a direct, measurable transfer from an ordinary user's wallet to a searcher's, no different in kind from the adverse-selection losses market makers price into spreads in traditional markets. |

## Related Concepts

- [[Adverse Selection]] — the classical microstructure framework MEV is a special, fully-informed case of
- [[Price Impact]] — the AMM mechanism (the $xy=k$ curve's slope) that sandwich attacks exploit
- [[Order Book]] — contrasts with AMM/mempool market structure; explains why sandwich attacks have no clean analogue in traditional limit order markets

## Sources Used

- "Imperfect Commitment in Maximal Extractable Value Auctions" — Adadurov, Barseghyan, Chtepine, Eloranta, Sebyakin, Valitov (2026)
- "Concave Continuation: Linking Routing to Arbitrage" — Jiang, Wen (2026)
- "The Viability of Blockchain Markets under Discrete Clearing and Paid Priority" — Capponi, Cartea, Drissi (2026)
- "Joint Exclusivity" — Mohammed (2026)

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-07-26 | Full content written | Content gap remediation — crypto/DeFi coverage |
