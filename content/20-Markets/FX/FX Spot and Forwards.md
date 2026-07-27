---
type: concept
domain: 20-Markets
tags: [fx, rates, no-arbitrage]
status: math
stability: stable
confidence: high
last_reviewed: 2026-07-26
review_interval_days: 365
sources:
  - "Hull ch.5 (FX forwards and CIP)"
  - "Du, Tepper, Verdelhan (2018)"
created: 2026-07-26
---

> [!info] Problem Chain
> **Chain:** Pricing → Gap: How do you price a contract to exchange one currency for another at a future date?
> **This concept:** No-arbitrage forward pricing via covered interest rate parity — the forward FX rate is pinned down entirely by the spot rate and the two currencies' interest rates, with no need to forecast where the exchange rate is going
> **Alternative approaches to this gap:** none — CIP is the unique no-arbitrage relationship (this parallels [[Put-Call Parity]] as a model-free, replication-based no-arbitrage relationship rather than a model requiring calibration)
> **You need first:** none — foundational
> **This unlocks:** currency-hedged portfolio construction, cross-currency basis trading

## Why This Exists

**The gap:** A US pension fund needs to pay a Japanese supplier ¥1bn in six months. It could wait and buy yen spot when the payment is due, but that leaves it exposed to exchange-rate risk for six months. It wants to lock in a rate *today* for an exchange that happens *later*. What should that locked-in rate be?

**What came before:** Before forward markets standardized around a formula, the naive approach was to guess: survey traders on where they expect USD/JPY to be in six months and quote that. This fails for the same reason expected-value option pricing fails — it depends on a subjective forecast nobody agrees on, and it ignores a much stronger constraint that's available for free: the interest rates in each currency.

**What this adds:** Covered interest rate parity (CIP) shows that the forward rate is not a forecast at all — it is a pure arbitrage identity. If you need $1 in six months, you can either (a) buy the forward today, or (b) borrow yen now, convert to dollars at spot, invest the dollars at the dollar rate, and separately let the yen loan accrue interest. Both strategies deliver the same $1 payoff with certainty, so by no-arbitrage they must cost the same today. This pins the forward rate to a unique value determined only by the spot rate and the two risk-free rates — no forecast of the future spot rate required. This is the FX analogue of [[Put-Call Parity]]: a relationship enforced by replication, not by a model of price dynamics.

**What it still doesn't solve:** Before 2008, CIP held to within a few basis points — deviations were arbitraged away almost instantly by bank trading desks. Since the 2008 financial crisis, CIP has persistently and systematically *failed*, with realized forward rates deviating from the CIP-implied rate by tens of basis points, sustained for years, across nearly every major currency pair. This shouldn't be possible if arbitrage capital is unconstrained — someone should borrow in the cheap currency, lend in the rich one, and erase the gap. The reason it persists is that the arbitrage is no longer free: post-crisis balance-sheet regulation (Basel III leverage ratios, the liquidity coverage ratio, the supplementary leverage ratio) makes it costly for banks to hold the matched but balance-sheet-intensive positions the arbitrage requires. The "law" of CIP has been replaced by a "law plus a balance-sheet cost term" — this is the subject of [[#Analysis]] below and is the reason this note treats CIP as a *bounded* relationship rather than an exact one post-2008.

## Math Concepts

**Quoting conventions.** An FX rate is always quoted as *base/quote* (or *base-quote*): the number of units of the **quote currency** needed to buy one unit of the **base currency**. EUR/USD = 1.0850 means 1 EUR costs 1.0850 USD — EUR is the base, USD is the quote.

- **Bid-ask:** dealers quote a two-sided price, e.g. EUR/USD 1.0850 / 1.0852. The bid (1.0850) is what the dealer pays for EUR (client sells EUR); the ask (1.0852) is what the dealer charges for EUR (client buys EUR). The dealer earns the spread.
- **Pips:** the smallest conventional price increment, usually the 4th decimal place for most pairs (2nd for JPY crosses, since JPY has no minor unit at that scale). In the quote above, the spread is 2 pips.
- **Forward quoting:** forwards are rarely quoted as outright rates in interbank markets. Instead, dealers quote **forward points** — the difference between the forward and spot rate, scaled to pips: $\text{Forward points} = (F - S) \times 10^4$ (for most pairs). The outright forward is reconstructed as $F = S + \text{points}/10^4$.

**Setting up the no-arbitrage argument.** Let:
- $S$ = spot exchange rate, domestic currency per unit of foreign currency (e.g. USD per EUR)
- $F$ = forward rate for delivery at time $T$, same units
- $r_d$ = domestic (quote currency) risk-free rate
- $r_f$ = foreign (base currency) risk-free rate
- $T$ = time to delivery, in years

**Two ways to guarantee delivery of 1 unit of foreign currency at time $T$**, valued in domestic currency:

*Strategy A — buy forward:* Enter a forward contract today to buy 1 unit of foreign currency at $T$, paying $F$ domestic currency units at $T$. Cost today: $0$ (forward contracts have zero initial value); domestic cash needed at $T$: $F$.

*Strategy B — replicate via borrowing/lending (covered):* the goal is to guarantee delivery of exactly 1 unit of foreign currency at $T$, funded entirely by a domestic-currency loan repaid at $T$ — i.e., no cash changes hands until $T$, just like the forward.
1. **Today:** buy $\dfrac{1}{1+r_f T}$ units of foreign currency at the spot rate, costing $\dfrac{S}{1+r_f T}$ domestic currency.
2. **Today:** invest that foreign-currency amount at the foreign rate $r_f$; by construction it grows to exactly $1$ unit of foreign currency at $T$.
3. **Today:** fund the domestic outlay in step 1 by borrowing $\dfrac{S}{1+r_f T}$ domestic currency at the domestic rate $r_d$.
4. **At $T$:** the foreign investment matures to the 1 unit of foreign currency you need, and you owe $\dfrac{S}{1+r_f T}(1+r_d T)$ domestic currency to repay the loan.

Strategy A delivers 1 unit of foreign currency at $T$ for a domestic cost of $F$ at $T$. Strategy B delivers the same 1 unit of foreign currency at $T$ for a domestic cost of $\dfrac{S(1+r_d T)}{1+r_f T}$ at $T$. Since both strategies produce an *identical* payoff (1 unit of foreign currency, delivered at $T$, nothing before), their costs must be identical, or a riskless arbitrage exists (buy the cheap one, sell the expensive one, pocket the difference at $T$ with zero net risk). This forces:

$$\boxed{F = S\cdot\frac{1+r_d T}{1+r_f T}}$$

This is **covered interest rate parity (CIP)**. "Covered" means the FX risk is fully hedged (covered) by the forward — this is distinct from *uncovered* interest parity (UIP), which is a behavioral/expectations hypothesis about spot rate drift, not a no-arbitrage identity, and does not hold empirically.

**Continuous-compounding form** (more common in derivatives pricing):

$$F = S \, e^{(r_d - r_f)T}$$

**Arbitrage check — what happens if $F$ deviates:**
- If the market forward $F_{\text{mkt}} > F_{\text{CIP}}$ (forward too rich in domestic currency): borrow domestic currency, convert to foreign at spot, invest foreign, and *sell* the foreign currency forward at the rich rate $F_{\text{mkt}}$ — locks in a riskless profit at $T$.
- If $F_{\text{mkt}} < F_{\text{CIP}}$: do the reverse — borrow foreign, convert to domestic at spot, invest domestic, buy foreign forward at the cheap rate.

Before 2008, this two-sided arbitrage kept deviations to a few bps (transaction costs). Since 2008, it has not.

**The cross-currency basis.** Define the basis $b$ as the rate adjustment needed to make the *observed* market forward consistent with actual funding costs, typically quoted against USD Libor/SOFR-equivalent legs in a cross-currency swap:

$$F_{\text{mkt}} = S\cdot\frac{1+(r_d + b)T}{1+r_f T}$$

Equivalently, in continuous-compounding log form, the basis is the annualized deviation:

$$b = \frac{1}{T}\ln\!\left(\frac{F_{\text{mkt}}}{S}\right) - (r_d - r_f)$$

A **negative** cross-currency basis for, say, EUR/USD means it costs *more* than the interest-rate differential implies to swap euros into dollars — i.e., dollar funding via the FX swap market is more expensive than dollar funding via unsecured cash markets would suggest. This basis is quoted in basis points per annum and is directly tradeable via cross-currency basis swaps.

## Walkthrough

**Step 1 — theoretical forward under CIP.** Spot EUR/USD $S = 1.0850$. USD rate $r_d = 5.25\%$ (3-month SOFR-equivalent), EUR rate $r_f = 3.75\%$ (3-month €STR-equivalent), $T = 0.25$.

$$F_{\text{CIP}} = 1.0850 \times \frac{1 + 0.0525\times 0.25}{1+0.0375\times 0.25} = 1.0850\times\frac{1.013125}{1.009375} = 1.0850\times 1.003715$$

$$F_{\text{CIP}} = 1.08903$$

Forward points: $(1.08903 - 1.0850)\times 10^4 = 40.3$ pips. Since $r_d > r_f$ (dollar rates exceed euro rates), the euro trades at a **forward premium** — you get more dollars per euro forward than spot, exactly compensating for euro's lower deposit rate. This is a completely general rule: the higher-rate currency always trades at a forward discount against itself (weakens forward), and the lower-rate currency trades at a forward premium (strengthens forward) — otherwise you could earn the rate differential *and* keep the spot exposure for free.

**Step 2 — observed market forward and implied basis.** Suppose the actual quoted 3-month EUR/USD forward in the market is $F_{\text{mkt}} = 1.0887$ (2.3 pips *below* the CIP-implied forward of 1.08903).

Using the log-basis formula with continuous-compounding rates approximated from the simple rates ($r_d \approx 5.19\%$, $r_f \approx 3.72\%$ continuously compounded, close enough for illustration):

$$b = \frac{1}{0.25}\ln\!\left(\frac{1.0887}{1.0850}\right) - (0.0519 - 0.0372)$$

$$b = 4\times\ln(1.003410) - 0.0147 = 4\times 0.003404 - 0.0147 = 0.013616 - 0.0147 = -0.00108$$

$$b \approx -10.8 \text{ bps}$$

So the market is pricing a euro cross-currency basis of roughly **−11 bps**: dollars are structurally more expensive to obtain via the FX swap market than the pure interest-rate differential implies. This is a small but entirely typical, persistent, and empirically well-documented deviation from CIP for EUR/USD in the post-2008 period — in stress periods (e.g., quarter-end regulatory reporting dates, March 2020) the EUR/USD basis has blown out to −50 to −140 bps.

## Analysis

**CIP as a "law" that broke down.** Pre-2008, CIP held almost to the penny — it was treated in textbooks (including Hull) as one of the closest things to a true law in finance, on par with put-call parity. The arbitrage required almost no capital: banks with AAA-rated balance sheets and deep repo access could put on the trade in near-unlimited size, so deviations were competed away in seconds. Du, Tepper, and Verdelhan (2018) document that this stopped holding systematically after the crisis, across essentially every G10 currency pair, and the deviations are not noise — they are persistent, priced, and correlated with measures of bank balance-sheet cost.

**Why balance-sheet-constrained arbitrage explains it.** The CIP arbitrage (borrow currency A, swap into currency B, invest, unwind via forward) requires a bank to gross up its balance sheet: it adds matched assets and liabilities that net to near-zero risk but are *not* netted for regulatory capital and leverage-ratio purposes under Basel III. The supplementary leverage ratio (SLR) in particular penalizes gross balance-sheet size regardless of the risk being economically hedged. Since balance sheet is now a scarce, costed resource (banks must hold capital against it and it counts against leverage constraints), banks demand a spread to intermediate the trade — this spread shows up as the cross-currency basis. The basis is, in effect, the shadow price of bank balance-sheet capacity.

**Why the basis differs by currency pair and tenor.**
- **By pair:** the basis is typically most negative for currencies where structural dollar demand is high relative to dollar supply — e.g., Japanese and European institutions with large USD-denominated asset books (hedging USD bonds back to home currency) create persistent one-directional demand to swap into dollars, widening JPY and EUR bases versus, say, commodity-bloc currencies with more balanced flows.
- **By tenor:** short tenors (overnight, 1-week) are less capital-intensive to intermediate (less balance-sheet time held) and see smaller deviations; the basis also spikes sharply around quarter-end and year-end reporting dates when banks temporarily shrink balance sheet to improve reported leverage ratios, then reverts — a clean signature of a regulatory-capital-driven, not fundamentals-driven, effect.
- **Cyclicality:** the basis widens in stress (dollar funding squeezes, e.g., 2008, March 2020) when the value of balance sheet / dollar funding spikes, and has structurally not returned to zero even in calm periods, reflecting the permanent post-Basel-III cost of intermediation.

**What this means practically:** anyone pricing a cross-currency hedge, cross-currency swap, or FX forward for size can no longer use textbook CIP directly — they must price in the observed basis, which is itself a traded, quoted market object (cross-currency basis swap spreads), not a theoretical residual.

## Implementation

```python
import numpy as np

def cip_forward(spot: float, r_domestic: float, r_foreign: float, T: float,
                 compounding: str = "simple") -> float:
    """
    Theoretical forward FX rate under covered interest rate parity.
    spot: S, in domestic currency per unit of foreign currency (e.g. USD per EUR)
    r_domestic, r_foreign: annualized risk-free rates (decimal, e.g. 0.0525)
    T: time to delivery in years
    """
    if compounding == "simple":
        return spot * (1 + r_domestic * T) / (1 + r_foreign * T)
    elif compounding == "continuous":
        return spot * np.exp((r_domestic - r_foreign) * T)
    else:
        raise ValueError("compounding must be 'simple' or 'continuous'")


def forward_points(spot: float, forward: float, pip_factor: float = 1e4) -> float:
    """Forward points quoted in pips (pip_factor=1e2 for JPY crosses)."""
    return (forward - spot) * pip_factor


def implied_cross_currency_basis(spot: float, forward_mkt: float,
                                  r_domestic: float, r_foreign: float,
                                  T: float) -> float:
    """
    Implied cross-currency basis (annualized, decimal) from an observed
    market forward that deviates from CIP. Uses continuous-compounding
    log form: b = (1/T) * ln(F_mkt / S) - (r_d - r_f)
    Negative b => domestic currency (e.g. USD) structurally expensive to
    obtain via the FX swap market relative to cash rates.
    """
    return (1.0 / T) * np.log(forward_mkt / spot) - (r_domestic - r_foreign)


if __name__ == "__main__":
    S = 1.0850          # EUR/USD spot
    r_usd = 0.0525       # 3M USD rate
    r_eur = 0.0375       # 3M EUR rate
    T = 0.25

    F_cip = cip_forward(S, r_usd, r_eur, T)
    pts = forward_points(S, F_cip)
    print(f"CIP forward: {F_cip:.5f}  ({pts:.1f} pips)")   # ~1.08903, ~40.3 pips

    F_mkt = 1.0887        # observed market forward
    basis = implied_cross_currency_basis(S, F_mkt, r_usd, r_eur, T)
    print(f"Implied cross-currency basis: {basis*1e4:.1f} bps")  # ~ -10.8 bps
```

## Bridge to Quant / ML

- **Funding and collateral cost modeling (XVA):** the cross-currency basis is a direct input to Funding Valuation Adjustment (FVA) and cross-currency CSA discounting — desks now discount USD cashflows collateralized in EUR (and vice versa) using basis-adjusted curves rather than flat OIS, because ignoring the basis materially misprices long-dated cross-currency swaps and hedges.
- **Basis as a tradeable factor:** the cross-currency basis behaves like a risk premium — it is persistently negative for structurally USD-short currencies (JPY, EUR) and can be harvested (short the basis, i.e., receive it) as a carry-like strategy, subject to blow-up risk at funding-stress events (a classic "picking up nickels in front of a steamroller" payoff profile, structurally similar to other funding/liquidity premia).
- **Feature engineering:** the level and term structure of cross-currency bases are used as macro-liquidity-stress features in factor models — a rapidly widening basis is one of the more reliable early-warning signals of dollar funding stress, and is watched alongside repo spreads and CDS-bond basis as a systemic risk indicator.
- **Balance-sheet-aware pricing:** more broadly, CIP's breakdown is the canonical teaching example that regulatory capital costs must be modeled as a first-class pricing input in the post-2008 world, not treated as a friction layered on top of frictionless no-arbitrage prices — an insight that generalizes to repo markets, bond-CDS basis trades, and other balance-sheet-intensive relative value trades.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** CIP is derived by replicating a forward contract using spot FX plus borrowing/lending in two currencies. Walk through why this replication argument forces $F$ to a unique value, without appealing to any forecast of the future spot rate.
<details>
<summary>Answer</summary>
The replication strategy (buy discounted foreign currency at spot, invest it at the foreign rate so it grows to exactly 1 unit at T, fund the purchase by borrowing domestic currency at the domestic rate) delivers exactly 1 unit of foreign currency at time T, with a domestic-currency cost fixed today by only the spot rate and the two interest rates — nothing about this cost depends on where the spot rate ends up at T. A forward contract delivers the identical payoff: 1 unit of foreign currency at T for F domestic currency. Two strategies with identical payoffs must have identical costs, or you could buy the cheap one and sell (replicate the opposite side of) the expensive one and lock in riskless profit today with zero net exposure at T. Because the replication cost never referenced a forecast of S_T, neither does F — this is what makes CIP a no-arbitrage identity rather than a prediction.
</details>

**Q2.** Explain the difference between covered interest rate parity (CIP) and uncovered interest rate parity (UIP). Why does only one of them hold reliably in practice?
<details>
<summary>Answer</summary>
CIP relates the *forward* rate to the spot rate and interest rate differential, and the FX risk is fully hedged ("covered") by the forward contract itself — it's a pure replication/no-arbitrage identity that must hold (up to the basis) because it involves no uncertain future spot rate. UIP instead claims that the *expected future spot rate* equals the forward rate (or equivalently, that expected currency depreciation offsets the interest rate differential) — this is an unhedged ("uncovered") bet on where spot will actually be, and it is a behavioral/expectations hypothesis, not an arbitrage relationship. Empirically, UIP fails badly and persistently (the "forward premium puzzle" / "uncovered interest parity puzzle") — high-interest-rate currencies tend to appreciate rather than depreciate on average, the opposite of what UIP predicts — because it requires risk-neutral, unconstrained speculators to enforce it, and currency risk premia and constrained speculative capital prevent that. CIP requires only riskless arbitrage capital (pre-2008, essentially unlimited) to enforce it, which is why it held far more reliably, though even CIP now has a persistent balance-sheet-cost-driven basis.
</details>

**Q3.** Why did cross-currency basis deviations from CIP appear specifically after 2008, rather than being a constant, pre-existing feature of FX markets?
<details>
<summary>Answer</summary>
Before 2008, banks treated balance sheet as essentially free and unlimited for low-risk, matched-book trades like the CIP arbitrage — any dislocation was competed away almost instantly by dealers with deep, cheap access to funding and no binding constraint on gross balance-sheet size. Post-crisis, Basel III introduced leverage ratios (including the supplementary leverage ratio) and liquidity requirements that constrain *gross* balance-sheet size and cost of funding, regardless of how well-hedged a position is netted economically. The CIP arbitrage requires grossing up the balance sheet (matched borrow/lend/swap legs that don't net for regulatory purposes), so it now consumes a scarce, costly resource. Banks demand compensation (the basis) to intermediate it, and because the regulatory constraint is structural and permanent rather than a temporary liquidity shortage, the basis has not reverted to zero even a decade-plus after the crisis — it's a new steady state, not a transient dislocation.
</details>

---

### Level 2 — Quantitative

**Q4.** Spot USD/JPY = 150.00. 6-month USD rate = 5.00%, 6-month JPY rate = 0.10% (both simple, annualized). Compute the CIP forward rate and the forward points (in pips, where 1 pip = 0.01 for USD/JPY).
<details>
<summary>Answer</summary>

Here domestic currency is JPY (quote currency) and foreign currency is USD (base currency), so $r_d$ = JPY rate = 0.10%, $r_f$ = USD rate = 5.00%, $T = 0.5$:

$$F = 150.00 \times \frac{1 + 0.0010\times 0.5}{1+0.0500\times 0.5} = 150.00\times\frac{1.0005}{1.0250}$$

$$F = 150.00\times 0.97610 = 146.41$$

Forward points: $(146.41 - 150.00)/0.01 = -359$ pips.

The dollar (the higher-rate currency, foreign/base here) trades at a large forward *discount* against yen — you get fewer yen per dollar forward than spot, consistent with the rule that the higher-rate currency always weakens forward. This large point spread reflects the wide US-Japan rate differential (4.9 percentage points).
</details>

**Q5.** Using the setup in Q4, suppose the actual market 6-month USD/JPY forward trades at 147.00 (yen stronger / dollar weaker than the CIP-implied 146.41). Using the simple-rate basis approximation $b \approx \dfrac{1}{T}\left(\dfrac{F_{\text{mkt}}}{S} - \dfrac{F_{\text{CIP}}}{S}\right)$, roughly how large is the implied basis in bps, and what does its sign tell you about the cost of dollar funding via the FX swap market?
<details>
<summary>Answer</summary>

$$b \approx \frac{1}{0.5}\left(\frac{147.00}{150.00} - \frac{146.41}{150.00}\right) = 2\times\left(0.98000 - 0.97607\right) = 2\times 0.00393 = 0.00786$$

$$b \approx 78.6 \text{ bps (positive, in this domestic=JPY convention)}$$

Because JPY is the domestic/quote currency here, a positive $b$ in this convention means dollars are *cheaper* to obtain synthetically (via spot + swap) than the JPY/USD rate differential implies — equivalently, this is the mirror image of the conventional "USD-basis" quoting (where deviations are usually expressed as an add-on to the *foreign*, i.e. non-USD, leg). In the standard market convention (basis quoted on the non-dollar currency against USD), this situation corresponds to a positive JPY cross-currency basis of similar magnitude — historically JPY basis has usually been *negative* (dollars expensive), so a large positive reading like this would be unusual and worth double-checking against the live market rather than taken as typical; the exercise is illustrative of the mechanics of extracting the basis, not a claim about JPY's typical sign.
</details>

---

### Level 3 — Coding

**Q6.** In `implied_cross_currency_basis`, the function takes `r_domestic` and `r_foreign` as simple annualized rates but combines them with `np.log(forward_mkt / spot)` using a continuous-compounding formula. Is this internally consistent? What error does mixing simple and continuously-compounded rates introduce, and how would you fix the function to be fully consistent?
<details>
<summary>Answer</summary>
It is not perfectly consistent — `np.log(forward_mkt/spot)/T` is the continuously-compounded equivalent rate differential implied by the forward, but subtracting `(r_domestic - r_foreign)` computed from simple rates mixes two different compounding conventions. For short tenors (3M, 6M) and typical rate levels, the numerical difference is small (a fraction of a basis point) because $\ln(1+x) \approx x$ for small $x$, which is why the walkthrough treats it as "close enough for illustration." To be fully consistent, either (a) convert the simple rates to continuously-compounded equivalents first — $r_d^{cc} = \ln(1+r_d T)/T$, $r_f^{cc} = \ln(1+r_f T)/T$ — before subtracting, or (b) keep everything in simple-rate form and compute the basis as an add-on to $r_d$ that solves $F_{\text{mkt}} = S(1+(r_d+b)T)/(1+r_f T)$ for $b$ directly, avoiding logs entirely. For tenors beyond a year or in high-rate environments, this inconsistency stops being negligible and must be fixed.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| The forward FX rate is the market's prediction of where the spot rate will be | The forward rate is a no-arbitrage replication cost, derived purely from the spot rate and the interest rate differential. It says nothing about expected future spot levels — that's the (empirically failing) uncovered interest parity claim, a completely different relationship. |
| A currency trading at a forward premium is expected to strengthen | A forward premium simply reflects that currency's lower interest rate relative to the other leg (it must strengthen forward to offset the lower carry, by CIP). It carries no information about expected future spot direction. |
| CIP still holds exactly today, just like it did pre-2008 | CIP has shown persistent, economically meaningful (tens of bps, sometimes 100+ in stress) deviations since 2008 across essentially all major currency pairs, driven by post-crisis bank balance-sheet regulation, not by measurement error or illiquidity alone. |
| The cross-currency basis is the same across all currency pairs and tenors | The basis varies substantially by pair (driven by structural USD funding demand, e.g., from JPY and EUR institutions hedging USD assets) and by tenor (spiking at quarter/year-end reporting dates), reflecting the specific balance-sheet and hedging-flow dynamics of each currency, not a single universal number. |

## Related Concepts
- [[Put-Call Parity]] — the equities/options analogue: another model-free, replication-enforced no-arbitrage identity
- [[Yield Curve]] — the domestic and foreign interest rate curves that feed directly into the CIP forward calculation

## Sources Used
- Hull — *Options, Futures & Other Derivatives*, ch.5 (FX forwards and CIP)
- Du, W., Tepper, A., & Verdelhan, A. (2018). *Deviations from Covered Interest Rate Parity.* Journal of Finance, 73(3), 915–957.

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-07-26 | Full content written | Content gap remediation — FX coverage |
