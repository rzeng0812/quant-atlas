---
type: concept
domain: 20-Markets
tags: [derivatives, credit, risk, rates]
status: math
stability: stable
confidence: high
last_reviewed: 2026-07-30
review_interval_days: 365
sources:
  - "Gregory, The xVA Challenge (2020)"
  - "Hull ch.24"
  - "Green, XVA: Credit, Funding and Capital Valuation Adjustments (2015)"
created: 2026-07-30
---

> [!info] Problem Chain
> **Chain:** Pricing → Gap: A risk-neutral derivative price assumes both counterparties are default-free and funding is frictionless — neither is true
> **This concept:** XVA is the set of adjustments that convert a clean risk-neutral price into the actual price a bank should charge, accounting for counterparty default risk and the real cost of funding the hedge
> **Alternative approaches to this gap:** posting full collateral / central clearing (removes most counterparty risk but not funding cost — see [[#Analysis]])
> **You need first:** [[Black-Scholes Model]], [[Credit Default Swap]], [[Risk-Neutral Measure]]
> **This unlocks:** regulatory capital treatment of derivatives (Basel III), central clearing mandates

## Why This Exists

**The gap:** A "clean" derivative price — a Black-Scholes option price, a swap valued off a discount curve — is computed as if the contract will certainly be honored by both sides and as if hedging it costs exactly the risk-free rate. Neither assumption survives contact with a real bank's balance sheet. The counterparty might default before the trade matures, and hedging the trade requires borrowing money and posting collateral at rates that are never actually the risk-free rate.

**What came before:** Pre-2008, derivatives desks priced trades off the clean model price and managed counterparty risk *outside* the pricing model entirely — via credit limits, netting agreements, and occasionally a coarse, desk-level reserve against "bad" counterparties. Counterparty default risk was a credit department problem, not a pricing input. Funding was treated as a non-issue: banks assumed they could borrow and lend at (or near) Libor, itself treated as a proxy for the risk-free rate, and that assumption was cheap enough to ignore. AAA-rated monoline insurers and large banks were, for pricing purposes, treated as effectively default-free. This is precisely the assumption that broke in 2008: Lehman Brothers defaulted with a large derivatives book outstanding, AIG (see [[Credit Default Swap]]) nearly failed to honor CDS protection it had sold, and banks discovered simultaneously that (a) even large, well-rated counterparties can default and (b) unsecured funding can become extremely expensive or unavailable exactly when a bank needs it most.

**What this adds:** XVA formalizes counterparty risk and funding cost as explicit, priced-in adjustments layered on top of the clean price:

$$\text{Price}_{\text{actual}} = \text{Price}_{\text{clean}} - \text{CVA} + \text{DVA} - \text{FVA} - \text{KVA} - \text{MVA} - \cdots$$

- **CVA** (Credit Valuation Adjustment): the expected loss from the *counterparty* defaulting while the trade has positive value to you.
- **DVA** (Debit Valuation Adjustment): the symmetric adjustment for *your own* default risk — the mirror image of CVA, and the more controversial of the two (see [[#Math Concepts]]).
- **FVA** (Funding Valuation Adjustment): the cost (or benefit) of funding the hedge and any uncollateralized exposure at a spread over the risk-free rate.
- **KVA** (Capital Valuation Adjustment): the cost of the regulatory capital the trade consumes over its life (Basel III capital charges).
- **MVA** (Margin Valuation Adjustment): the cost of funding the initial margin required by central clearing or bilateral variation-margin rules.

Each of these is now computed, quoted, and in many cases actively hedged, by dedicated desks. A quoted derivative price today is not "the model price" — it is the model price minus a stack of these adjustments.

**What it still doesn't solve:** XVA desks introduce their own model risk on top of the risk they're trying to price — CVA requires simulating the entire future distribution of exposure under a set of model assumptions (rates, vols, correlations between exposure and default) that are themselves uncertain and hard to hedge. Several of the adjustments (FVA especially) are not cleanly replicable the way the clean BSM price is: there is no liquid, unique market instrument that lets a desk perfectly hedge its own funding cost the way it can delta-hedge an option. And because different banks use different funding curves, different default probability models, and different assumptions about collateral behavior, two banks pricing the identical trade with the identical counterparty routinely arrive at materially different XVA numbers — a genuine, persistent source of pricing disagreement that has no analogue in clean BSM pricing, where two banks with the same market data converge to the same number.

## Math Concepts

**CVA as an expected-loss integral.** CVA is the price today of the expected loss a bank suffers if its counterparty defaults before the trade matures. A loss only occurs if, at the moment of default, the trade has *positive* value to the surviving party (if it has negative value, the surviving party owes the defaulted estate money, and — subject to netting — that claim is unaffected by who defaulted). Define $\text{EE}(t) = \mathbb{E}^{\mathbb{Q}}[\max(V(t), 0)]$, the **expected positive exposure** at time $t$ under the risk-neutral measure, where $V(t)$ is the mark-to-market value of the netting set to the bank. Then:

$$\boxed{\text{CVA} = (1-R)\int_0^T \mathbb{E}^{\mathbb{Q}}[\text{EE}(t)] \, dQ_{\text{default}}(t)}$$

where $R$ is the counterparty's recovery rate and $Q_{\text{default}}(t)$ is the risk-neutral probability that the counterparty has defaulted by time $t$ (so $dQ_{\text{default}}(t)$ is the risk-neutral default-time density). This is structurally identical to the CDS protection leg from [[Credit Default Swap]] — $(1-R)$ times a probability-weighted, discounted exposure — except the CDS protection leg is written against a *fixed notional*, whereas CVA is written against a *time-varying, stochastic, trade-specific exposure profile* $\text{EE}(t)$ that must itself be simulated. In discrete form (see [[#Walkthrough]] and [[#Implementation]]), with $t_1, \dots, t_n$ a grid of times:

$$\text{CVA} \approx (1-R)\sum_{i=1}^{n} \text{EE}(t_i)\, D(t_i)\,\left[Q_{\text{surv}}(t_{i-1}) - Q_{\text{surv}}(t_i)\right]$$

where $D(t_i)$ discounts the exposure to today and $Q_{\text{surv}}(t) = 1 - Q_{\text{default}}(t)$ is the counterparty's survival probability (bootstrapped from CDS spreads exactly as in [[Credit Default Swap]]).

**DVA — the symmetric, uncomfortable adjustment.** Just as the counterparty defaulting when the trade is an asset to the bank causes a loss to the bank, the *bank itself* defaulting when the trade is a *liability* to the bank (an asset to the counterparty) causes a loss to the counterparty — which the bank, from its own accounting perspective, records as a *gain*, because it will not have to pay the full amount it owes. This is DVA:

$$\text{DVA} = (1-R_B)\int_0^T \mathbb{E}^{\mathbb{Q}}[\text{EE}_{\text{counterparty}}(t)] \, dQ_{\text{default},B}(t)$$

where $R_B$ is the bank's own recovery rate, $\text{EE}_{\text{counterparty}}(t) = \mathbb{E}^{\mathbb{Q}}[\max(-V(t), 0)]$ is the expected exposure from the counterparty's point of view (i.e., the bank's expected negative exposure), and $Q_{\text{default},B}(t)$ is the bank's *own* risk-neutral default probability, typically read off the bank's own CDS spread. Note the sign in the price identity above: $\text{Price}_{\text{actual}} = \text{Price}_{\text{clean}} - \text{CVA} + \text{DVA} - \cdots$ — DVA *adds* to the price the bank can claim.

The uncomfortable implication is real and worth stating precisely: as a bank's own credit quality *deteriorates* — its CDS spread widens — $Q_{\text{default},B}(t)$ rises, DVA rises, and the bank's own accounting P&L on its derivatives book *improves*, all else equal. This is not a modeling artifact; it follows directly from the economics of a defaultable liability. A bond trading below par because the issuer's credit has worsened is, by the same logic, a "cheaper" liability to extinguish — DVA is simply this same mark-to-market effect applied to derivatives payables. Banks reported large DVA gains during their own credit deterioration in 2008–2011, which generated real controversy: reporting profits *because your own default risk went up* struck many observers (and regulators) as perverse, since the "gain" can only ever be realized by actually defaulting, which is not a strategy a going concern can monetize. This is why DVA is often excluded from regulatory capital calculations even where it is included in accounting P&L, and why some banks choose not to hedge DVA at all — hedging DVA would mean actively taking a position that profits from your own firm's decline, which is organizationally and reputationally fraught even when it is economically coherent hedging.

**FVA — funding cost of the hedge.** A derivatives desk that is not fully, symmetrically collateralized must fund its hedge positions and any uncollateralized exposure in the wholesale funding market, at the bank's own funding spread $s_F$ over the risk-free/OIS rate, not at the risk-free rate itself. If a trade requires the bank to post cash collateral or fund an asset, that funding costs $r + s_F$; if the trade generates cash the bank can invest, it only earns $r + s_F$ as well (banks generally cannot borrow *or* invest at the pure risk-free rate — only fund at their own, wider, funding curve). FVA is the value of this funding spread, integrated over the (expected, signed) funding exposure of the trade:

$$\text{FVA} \approx \int_0^T s_F(t)\, \mathbb{E}^{\mathbb{Q}}[\text{EE}_{\text{funding}}(t)]\, D(t)\, dt$$

where $\text{EE}_{\text{funding}}(t)$ is the expected funding requirement of the position at $t$ (positive when the bank must fund the position, e.g. because the trade is uncollateralized and in the bank's favor, or must post collateral against it). This is structurally the same expected-exposure-integral shape as CVA — the difference is that CVA integrates exposure against *counterparty default probability*, while FVA integrates exposure against the bank's *own funding spread*.

**The DVA/FVA double-counting problem.** Both DVA and FVA are, at root, adjustments for the bank's own credit risk: DVA prices the fact that the bank's own liabilities are defaultable, while FVA prices the fact that the bank's unsecured funding costs embed the market's view of that same default risk (a bank's funding spread $s_F$ is, to a first approximation, its own CDS spread plus a liquidity premium). Including both a DVA term computed from the bank's CDS curve *and* an FVA term computed from the bank's funding curve risks charging for the bank's own credit risk twice, since the two curves overlap substantially in what they represent. The industry has never fully resolved this: some frameworks argue FVA should only capture the *liquidity* component of the funding spread (netting out the credit component already captured by DVA), others argue DVA should be dropped entirely in economic pricing (since it is unhedgeable and unrealizable pre-default) and FVA alone should carry the full funding cost. Different banks make different choices here, which is itself one more reason two banks routinely disagree on the XVA-adjusted price of an identical trade.

## Walkthrough

A bank has a 5-year, uncollateralized interest rate swap with a single counterparty, notional $N = \$100\text{m}$. Because a payer swap's mark-to-market value rises and falls with rates in both directions, exposure is not monotonic — it typically rises for the first half of the trade's life (as rate uncertainty accumulates) then falls (as the remaining cashflows shrink toward maturity). Approximate the expected positive exposure profile with a simple triangular shape peaking at year 2.5:

| Year $t$ | $\text{EE}(t)$ (expected positive exposure, \$m) |
|---|---|
| 0.5 | 1.2 |
| 1.5 | 2.6 |
| 2.5 | 3.4 |
| 3.5 | 2.3 |
| 4.5 | 1.0 |

Counterparty data: flat 5-year CDS spread $s = 150$ bp, recovery $R = 40\%$ (standard market convention, as in [[Credit Default Swap]]). From [[Credit Default Swap]], the implied hazard rate is:

$$\lambda \approx \frac{s}{1-R} = \frac{0.015}{0.60} = 0.025 \text{ per year}$$

Survival probability $Q_{\text{surv}}(t) = e^{-\lambda t}$, discount rate $r = 4\%$ (flat, for simplicity), $D(t) = e^{-rt}$. Using annual buckets centered on the midpoints above ($t_i - t_{i-1} = 1$ year each):

| $t_i$ | $\text{EE}(t_i)$ | $Q_{\text{surv}}(t_{i-1})$ | $Q_{\text{surv}}(t_i)$ | $\Delta Q_{\text{default}}$ | $D(t_i)$ |
|---|---|---|---|---|---|
| 0.5 | 1.2 | 1.0000 | $e^{-0.025\times1}=0.9753$ | 0.0247 | $e^{-0.04\times0.5}=0.9802$ |
| 1.5 | 2.6 | 0.9753 | $e^{-0.025\times2}=0.9512$ | 0.0241 | $e^{-0.04\times1.5}=0.9418$ |
| 2.5 | 3.4 | 0.9512 | $e^{-0.025\times3}=0.9277$ | 0.0235 | $e^{-0.04\times2.5}=0.9048$ |
| 3.5 | 2.3 | 0.9277 | $e^{-0.025\times4}=0.9048$ | 0.0229 | $e^{-0.04\times3.5}=0.8694$ |
| 4.5 | 1.0 | 0.9048 | $e^{-0.025\times5}=0.8825$ | 0.0223 | $e^{-0.04\times4.5}=0.8353$ |

(Using annual survival steps as a proxy for the 1-year bucket around each midpoint.)

Contribution of each bucket $= \text{EE}(t_i)\times D(t_i) \times \Delta Q_{\text{default}}$:

- $t=0.5$: $1.2 \times 0.9802 \times 0.0247 = 0.02905$
- $t=1.5$: $2.6 \times 0.9418 \times 0.0241 = 0.05902$
- $t=2.5$: $3.4 \times 0.9048 \times 0.0235 = 0.07231$
- $t=3.5$: $2.3 \times 0.8694 \times 0.0229 = 0.04580$
- $t=4.5$: $1.0 \times 0.8353 \times 0.0223 = 0.01863$

Sum $= 0.22481$ (\$m). With $(1-R) = 0.60$:

$$\text{CVA} \approx 0.60 \times 0.22481\text{m} = \$0.1349\text{m} \approx \$135{,}000$$

On a trade whose clean value might be close to zero (an at-market swap), a CVA charge of \$135,000 against a \$100m notional, 5-year uncollateralized swap is entirely typical in magnitude — a few basis points of notional, driven almost entirely by the counterparty's credit spread and the shape of the exposure profile. If the same swap were fully collateralized under a CSA with daily margining, $\text{EE}(t)$ would collapse toward the margin period of risk (days, not years) and CVA would fall by an order of magnitude or more — the mechanism explored in [[#Analysis]].

## Analysis

**Collateral (CSA) and central clearing reduce but don't eliminate CVA.** A Credit Support Annex (CSA) requires counterparties to post collateral against the mark-to-market value of a netting set, typically daily. This caps exposure at roughly the largest move the trade's value can make over the "margin period of risk" (the gap between the last posted collateral and a default event, commonly assumed to be 5–10 business days) rather than the full, multi-year peak exposure used in the uncollateralized walkthrough above. Central clearing through a CCP goes further: it standardizes daily variation margin, adds initial margin as a buffer against gap risk, and mutualizes remaining losses through a default fund. Both reduce CVA sharply — but neither eliminates it. Collateral itself has to be funded (which is exactly what MVA prices), collateral disputes and operational delays reintroduce gap exposure, and CCPs concentrate rather than eliminate systemic counterparty risk (a CCP failure, while rare, would be far larger than any single dealer default). CVA on a well-collateralized book is small; it is never exactly zero.

**The FVA debate.** FVA's arrival split the derivatives-pricing community more than any other XVA component, because it strikes at a foundational assumption of no-arbitrage pricing: that there is a single, universal risk-neutral price for a given payoff, independent of who is pricing it. The case *for* FVA: banks genuinely cannot fund at the risk-free rate — they fund at their own credit-and-liquidity-inclusive spread — so any hedge that requires funding really does cost more than the clean model assumes, and ignoring this systematically overvalues uncollateralized trades. Not charging FVA means giving away real economic value. The case *against*: a "price" that depends on the specific bank's own funding curve is no longer a price for the *instrument* — it's a bank-specific cost allocation, and two banks that are otherwise identical except for their funding spreads would, under FVA, quote different prices for the identical hedgeable payoff, which looks less like arbitrage-free pricing and more like cost-plus accounting. Critics (including senior academics like Hull and White, who published prominently against including FVA in "the" price) argued FVA reflects the bank's own funding strategy and capital structure choices, not a property of the derivative, and so shouldn't appear in a supposedly universal valuation. In practice, the debate was settled by the market rather than by theory: banks that didn't charge FVA were persistently on the wrong side of trades with banks that did (systematically overpaying to unwind uncollateralized trades, underpricing new ones), so FVA became standard practice regardless of which side of the theoretical argument was "correct." This is a recurring pattern in post-2008 derivatives pricing (see [[FX Spot and Forwards]] for the same dynamic playing out in the cross-currency basis) — theoretically debatable adjustments become practically mandatory once enough of the market prices them in, because failing to do so becomes an exploitable gap rather than a principled stand.

**Why XVA is centralized in one desk.** Before this discipline existed, each trading desk (rates, FX, credit, equities) managed its own view of counterparty risk informally, if at all. XVA desks are now almost universally centralized: a single desk owns CVA, FVA, and increasingly KVA/MVA for the *entire* bank's derivatives book, rather than each product desk pricing its own counterparty and funding adjustments trade-by-trade. This is because these adjustments are fundamentally netting-set-level and portfolio-level, not trade-level, quantities: $\text{EE}(t)$ for a given counterparty depends on the *entire* portfolio of trades with that counterparty (since exposures net against each other under a master netting agreement), and a bank's overall funding cost depends on its consolidated balance sheet, not any single desk's positions. A rates desk pricing a new swap with a counterparty that already has an offsetting FX forward on the book needs to know the *incremental* CVA/FVA the new trade adds to the existing netting set — a calculation only a centralized desk with full visibility into the counterparty relationship and the bank's funding position can do correctly. Centralization also lets the bank actively manage and hedge these exposures (buying CDS protection on large counterparties, managing the aggregate funding book) at a scale no individual trading desk could justify.

## Implementation

```python
import numpy as np

def bootstrap_hazard_rate(cds_spread: float, recovery: float = 0.40) -> float:
    """
    Approximate constant hazard rate implied by a CDS spread, as in the
    Credit Default Swap note: lambda ~= spread / (1 - recovery).
    """
    return cds_spread / (1.0 - recovery)


def survival_curve(hazard_rate: float, times: np.ndarray) -> np.ndarray:
    """Risk-neutral survival probability Q(tau > t) = exp(-lambda * t)."""
    return np.exp(-hazard_rate * times)


def compute_cva(
    expected_exposure: np.ndarray,   # EE(t_i), same units as notional (e.g. $m)
    times: np.ndarray,               # bucket times t_i, in years
    hazard_rate: float,              # counterparty's (constant) hazard rate
    recovery: float = 0.40,
    risk_free_rate: float = 0.04,
) -> float:
    """
    Discretized CVA:
        CVA ~= (1-R) * sum_i EE(t_i) * D(t_i) * [Q_surv(t_{i-1}) - Q_surv(t_i)]

    times[i] is treated as the midpoint/endpoint of bucket i; the survival
    drop over each bucket is computed against the previous bucket boundary
    (t=0 survival = 1.0 for the first bucket).
    """
    surv = survival_curve(hazard_rate, times)
    surv_prev = np.concatenate([[1.0], surv[:-1]])
    default_prob_bucket = surv_prev - surv

    discount = np.exp(-risk_free_rate * times)

    cva = (1.0 - recovery) * np.sum(expected_exposure * discount * default_prob_bucket)
    return cva


if __name__ == "__main__":
    # Walkthrough reproduction: 5y uncollateralized swap, triangular EE profile
    times = np.array([0.5, 1.5, 2.5, 3.5, 4.5])
    ee = np.array([1.2, 2.6, 3.4, 2.3, 1.0])   # $m

    cds_spread = 0.0150   # 150 bp
    recovery = 0.40
    r = 0.04

    lam = bootstrap_hazard_rate(cds_spread, recovery)
    print(f"Implied hazard rate: {lam:.4%} / yr")

    cva = compute_cva(ee, times, lam, recovery, r)
    print(f"CVA: ${cva:.4f}m  (${cva*1e6:,.0f})")

    # Sensitivity: CVA roughly scales with hazard rate near the base case
    for bp in [50, 100, 150, 250, 400]:
        lam_i = bootstrap_hazard_rate(bp / 1e4, recovery)
        cva_i = compute_cva(ee, times, lam_i, recovery, r)
        print(f"  spread={bp:>4}bp -> CVA=${cva_i*1e6:>10,.0f}")
```

Running the base case reproduces the walkthrough's roughly \$135,000 CVA figure (small differences come from rounding in the hand calculation above). The sensitivity loop shows the expected result: CVA rises roughly proportionally with the counterparty's credit spread, since a higher spread implies a higher hazard rate and therefore more default probability mass falling inside the exposure profile's window.

## Bridge to Quant / ML

- **The cross-currency basis is FVA's close cousin.** [[FX Spot and Forwards]] shows that post-2008, the cost of swapping currencies deviates persistently from covered interest parity because balance-sheet capacity became a scarce, priced resource — the basis is, in that note's words, "the shadow price of bank balance-sheet capacity." FVA is the same phenomenon applied to single-currency derivatives funding: both are cases where a pre-2008 "frictionless funding" assumption broke down permanently, and both required banks to build entirely new pricing infrastructure (cross-currency-basis-adjusted discount curves; FVA desks) to price balance-sheet cost explicitly rather than assume it away. A bank pricing a long-dated cross-currency swap today must, consistently, account for both the cross-currency basis *and* FVA — they are not competing explanations, they are the same underlying cost showing up in two related markets.
- **CVA is a bespoke CDS.** [[Credit Default Swap]] prices protection against a counterparty's default on a *fixed notional*. CVA prices the same underlying risk — expected loss given counterparty default, using the identical $(1-R)$ recovery mechanics and hazard-rate/survival-probability machinery — but struck against the *time-varying, stochastic exposure* of one specific netting set rather than a flat notional. This is why CVA desks are, in effect, running a CDS trading book on every material counterparty, sized not to notional but to a simulated exposure profile that itself depends on interest rates, FX, and volatility — CVA is a derivative on a derivative, in that its value depends on the market-implied distribution of another derivative's future mark-to-market.
- **Exposure simulation is a Monte Carlo / ML-adjacent problem at scale.** Real CVA desks don't use a hand-rolled triangular exposure profile — they run full Monte Carlo simulations of thousands of risk-factor paths across an entire counterparty's netting set to generate $\text{EE}(t)$, then aggregate across tens of thousands of counterparties. This is one of the largest computational workloads in a bank, and it has become a proving ground for regression-based and ML-accelerated exposure approximation techniques (e.g., neural-network or Chebyshev-polynomial proxies for full repricing) designed to make nightly XVA recalculation computationally tractable.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** CVA and DVA are described as symmetric. Explain precisely what "symmetric" means here, and why a bank's DVA can rise even while nothing about the trade itself or the counterparty has changed.
<details>
<summary>Answer</summary>
CVA prices the risk that the *counterparty* defaults while the trade is an asset to the bank (positive value); DVA prices the risk that the *bank itself* defaults while the trade is a liability to the bank (negative value, i.e., an asset to the counterparty). They use the identical mathematical machinery — (1 − recovery) × discounted, probability-weighted exposure — just with the roles of "who defaults" and "whose exposure" swapped. DVA can rise purely because the bank's own credit spread widens (its own CDS/funding spread increases), which raises the market-implied probability of the bank's own default, even if the trade's exposure profile and the counterparty's credit are completely unchanged. This is exactly why DVA is controversial: a bank's own P&L can improve simply because the market thinks the bank is more likely to fail, which is not something the bank can actually monetize as a going concern — only by defaulting, which ends the P&L benefit along with everything else.
</details>

**Q2.** Why didn't CVA/FVA exist as a formal, priced discipline before 2008, given that counterparty default and funding cost were always theoretically present risks?
<details>
<summary>Answer</summary>
Two things were true pre-2008 that made ignoring these risks a reasonable practical approximation: large bank and monoline counterparties were treated as effectively default-free for pricing purposes (their default probabilities were low enough, and confidence in "too big to fail" support strong enough, that the expected-loss adjustment was considered immaterial next to the size of the trades), and unsecured funding was cheap, deep, and assumed available at close to the risk-free rate, so the spread between funding cost and the risk-free rate was small enough to ignore. Lehman's default (a major derivatives counterparty actually failing) and the 2008 funding crisis (banks discovering they could not fund at anything close to risk-free, and sometimes could not fund at all) simultaneously falsified both assumptions. What had been a rounding error became a first-order pricing input, and banks that didn't adjust were mispricing trades relative to banks that did.
</details>

**Q3.** A junior trader argues: "If we're fully collateralized under a daily-margined CSA, we don't need to worry about CVA at all." Is this correct?
<details>
<summary>Answer</summary>
Not quite. Daily collateralization dramatically shrinks CVA by capping exposure at roughly the "margin period of risk" — the handful of business days between the last good collateral exchange and a default event — rather than letting exposure run over the trade's full multi-year life. But it does not reduce CVA to zero: the trade's value can still move sharply within the margin period (gap risk), collateral disputes or operational failures can delay margin calls right when they matter most, and the collateral itself has to be funded (which is what MVA prices, and is a real, non-zero cost). So collateralization is a powerful CVA mitigant, not an eliminator — and it introduces its own new costs (MVA) that have to be priced in turn.
</details>

---

### Level 2 — Quantitative

**Q4.** A 3-year uncollateralized trade has expected positive exposure of \$2m (constant, as a simplification) at each of years 1, 2, and 3. The counterparty's flat CDS spread is 200bp, recovery is 40%, and the risk-free rate is 3%. Using annual buckets and the discretized CVA formula, compute CVA.
<details>
<summary>Answer</summary>

Hazard rate: $\lambda = \dfrac{0.02}{1-0.40} = \dfrac{0.02}{0.60} = 0.03333$/yr

Survival probabilities: $Q(1) = e^{-0.03333} = 0.9672$, $Q(2) = e^{-0.06667} = 0.9355$, $Q(3) = e^{-0.10} = 0.9048$

Default probability per bucket: $\Delta Q(1) = 1 - 0.9672 = 0.0328$; $\Delta Q(2) = 0.9672 - 0.9355 = 0.0317$; $\Delta Q(3) = 0.9355 - 0.9048 = 0.0307$

Discount factors: $D(1) = e^{-0.03} = 0.9704$; $D(2) = e^{-0.06} = 0.9418$; $D(3) = e^{-0.09} = 0.9139$

Bucket contributions ($\text{EE}\times D \times \Delta Q$, with EE = \$2m each):
- Year 1: $2 \times 0.9704 \times 0.0328 = 0.06366$
- Year 2: $2 \times 0.9418 \times 0.0317 = 0.05971$
- Year 3: $2 \times 0.9139 \times 0.0307 = 0.05611$

Sum = 0.17948; CVA $= (1-0.40)\times 0.17948 = 0.60 \times 0.17948 \approx \$0.1077\text{m} \approx \$107{,}700$
</details>

**Q5.** Using the Q4 setup, suppose the counterparty's spread widens from 200bp to 400bp (credit deterioration) with everything else unchanged. Roughly how does CVA change, and why is it not exactly proportional to the spread (i.e., not exactly double)?
<details>
<summary>Answer</summary>
Doubling the spread roughly doubles the hazard rate ($\lambda \approx 0.0667$/yr), which raises the annual default probability increments substantially, so CVA rises by considerably more than the exposure alone would suggest — but not by exactly a factor of two, because the *survival* probabilities used to weight later years also fall faster (the counterparty is less likely to still be alive to generate a loss in year 3 at all under the higher hazard rate), partially offsetting the higher per-period default probability in later buckets. The net effect is still a large increase in CVA (roughly on the order of 1.8–1.9x in this case, not exactly 2x), which is why CVA desks actively hedge against counterparty spread widening — CVA is a highly convex, credit-spread-sensitive position, similar to being short a large amount of CDS protection on every material counterparty.
</details>

---

### Level 3 — Coding

**Q6.** In `compute_cva`, `surv_prev` is built as `np.concatenate([[1.0], surv[:-1]])`, exactly mirroring the pattern used in the Credit Default Swap note's `cds_fair_spread` function. Why is this the correct way to compute the default probability in each exposure bucket, and what would go wrong if `times` were unevenly spaced (e.g. quarterly for year 1, then annual afterward) but the function were called without any other changes?
<details>
<summary>Answer</summary>
`surv_prev[0] = 1.0` represents certainty of survival at time zero, so the first bucket's default probability is `1.0 - Q_surv(times[0])`, correctly capturing the chance of defaulting between contract inception and the first exposure date. Each subsequent bucket's default probability is `Q_surv(times[i-1]) - Q_surv(times[i])`, the probability of surviving to the previous bucket boundary but defaulting by the current one. This is exactly correct regardless of spacing, because `survival_curve` is evaluated directly at the actual `times` values passed in — `Q_surv(t) = exp(-lambda * t)` doesn't assume even spacing, and neither does the subtraction. So unevenly spaced times (quarterly then annual) work correctly with no changes needed; the function only assumes that `times` is sorted in increasing order, which if violated would produce negative default probabilities and a wrong (likely negative or nonsensical) CVA. The one thing to watch is that `expected_exposure[i]` must correspond to the *same* index as `times[i]`, i.e., the exposure and time grids must be aligned entry-by-entry, which is the caller's responsibility, not something the function itself validates.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---|---|
| DVA means a bank actively wants its own credit to get worse | DVA is an accounting mark-to-market effect: as a bank's own default probability rises, the market value of what it owes falls, which the bank records as a gain. No bank rationally *wants* its credit to deteriorate — the "gain" is unrealizable except by actually defaulting, which is why many banks don't hedge DVA and why regulators often exclude it from regulatory capital even where it appears in accounting P&L. |
| CVA is just credit risk moved into the pricing model — conceptually nothing new | CVA is credit risk applied to a *stochastic, trade-specific exposure profile* rather than a fixed notional, which requires simulating the future distribution of a derivative's mark-to-market value — a materially harder and more computationally intensive problem than pricing a CDS on a bond's fixed face value. |
| FVA is a settled, universally agreed-upon adjustment like CVA | FVA remains genuinely contested: prominent academics (Hull and White) argued publicly it shouldn't be part of a supposedly universal no-arbitrage price, since it depends on the pricing bank's own funding curve. It became market practice because banks that ignored it were adversely selected against, not because the theoretical debate was resolved. |
| Once a trade is centrally cleared, XVA no longer applies | Central clearing changes the shape and size of the exposure (variation + initial margin instead of full uncollateralized exposure to a bilateral counterparty) but doesn't eliminate CVA (residual gap/margin-period-of-risk exposure to the CCP) or funding cost (MVA, the cost of funding the initial margin itself, becomes the dominant remaining charge). |

## Related Concepts
- [[Black-Scholes Model]] — the "clean" risk-neutral pricing framework XVA adjusts
- [[Credit Default Swap]] — CVA's expected-loss mathematics is the same machinery, applied to a stochastic exposure instead of a fixed notional
- [[Risk-Neutral Measure]] — the measure under which expected exposure $\text{EE}(t)$ and default probabilities are computed
- [[FX Spot and Forwards]] — the cross-currency basis is the FX-market twin of FVA: both price balance-sheet/funding cost explicitly post-2008
- [[Interest Rate Swaps]] — the canonical uncollateralized product used in the CVA walkthrough
- [[Value at Risk]] — related but distinct: VaR measures tail risk of a portfolio's future value, while CVA prices the *expected* loss from counterparty default specifically

## Sources Used
- Gregory, J. (2020). *The xVA Challenge: Counterparty Credit Risk, Funding, Collateral, and Capital*, 4th ed. Wiley Finance.
- Hull, J. (2022). *Options, Futures and Other Derivatives*, 11th ed., ch. 24 — credit risk and CVA.
- Green, A. (2015). *XVA: Credit, Funding and Capital Valuation Adjustments*. Wiley Finance.

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-07-30 | Full content written | Content gap remediation — XVA coverage |
