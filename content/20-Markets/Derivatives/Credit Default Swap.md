---
type: concept
domain: 20-Markets
tags: [derivatives, credit, fixed-income]
status: math
stability: evolving
confidence: high
last_reviewed: 2026-04-18
review_interval_days: 90
sources:
  - "Hull, Options Futures and Other Derivatives, ch. 24-25"
  - "O'Kane, Modelling Single-name and Multi-name Credit Derivatives (2008)"
  - "ISDA Credit Derivatives Definitions"
created: 2026-04-18
---

> [!info] Problem Chain
> **Chain:** Hedging & Risk → Gap 1 extension: Hedge credit risk specifically
> **This concept:** Creates a bilateral contract that isolates and transfers credit default risk — letting bond holders retain yield while eliminating the exposure to a specific issuer's default.
> **Alternative approaches to this gap:** selling the bond outright (loses the yield), buying a put on the bond (requires liquid bond options market), credit-linked notes (embed the protection in a bond structure)
> **You need first:** [[Bond Basics]], [[Delta Hedging]] (analogous risk transfer concept), [[Interest Rate Swaps]] (structural parallel: two-leg derivative)
> **This unlocks:** [[Value at Risk]] for credit portfolios, CDO pricing, [[Stress Testing]] with credit scenarios, credit-equity relative value

## Why This Exists

**The gap:** Banks and institutional investors held large portfolios of corporate bonds and loans that they couldn't easily sell — the secondary market was illiquid, selling would damage customer relationships, or the position was too large to exit cleanly. But holding bonds means holding credit risk: if the company defaults, the investor suffers severe losses. There was no way to hedge credit risk without physically exiting the position.

**What came before:** Before CDS, the only way to reduce credit exposure was to sell the bond, reduce the loan, or buy a put option on the bond. Selling was often impractical. Bond put options barely existed as a liquid instrument. Lenders were stuck: take the credit risk or lose the yield.

**What this adds:** A CDS separates the credit risk from the bond's yield. The protection buyer pays a recurring premium (the CDS spread) and receives a lump-sum payment if the reference entity defaults. This lets the bond holder retain the coupon income while transferring the default risk to a willing counterparty. It also creates a market-observable, real-time price for credit risk — the CDS spread — that updates continuously unlike credit ratings. And it enables speculation: investors who want credit exposure without buying bonds can sell protection.

**What it still doesn't solve:** CDS introduces counterparty risk — the protection seller must actually pay when a default occurs, precisely when financial stress is highest. Concentration of CDS positions at a few large dealers (as seen with AIG in 2008) creates systemic risk. Central clearing has mitigated this, but bilateral CDS still carry counterparty exposure. CDS also cannot perfectly hedge basis risk: the CDS spread may diverge from the bond's credit spread due to cheapest-to-deliver options, funding costs, and differing ISDA definitions across jurisdictions.

You buy a **Credit Default Swap** (CDS). A CDS is like insurance on that bond. You pay a regular premium — expressed as basis points per year of the notional — and in return, if the airline defaults on its debt, the CDS seller pays you a lump sum that compensates for the loss. The regular premium is called the **CDS spread** or **CDS premium**.

From the other side: suppose you think the airline is financially healthier than the market believes. You can *sell* CDS protection — collect the premium — and profit if no default occurs. This is effectively a leveraged bet that the company will not default.

CDS are extraordinarily flexible:
- They let investors take credit exposure without buying bonds (lenders can't always participate in bond markets).
- They allow precise hedging of credit risk without selling the underlying bond.
- They enable speculation on corporate credit quality.
- They create a market-observable credit risk price — the CDS spread — updated in real time.

The 2008 financial crisis threw CDS into public consciousness. AIG had sold hundreds of billions of dollars of CDS protection on mortgage-backed securities. When housing defaults spiked, AIG faced catastrophic losses on its CDS book and had to be bailed out by the U.S. government — because the firms on the other side of those contracts (Goldman, Deutsche Bank, Societe Generale) would have suffered massive unhedged credit losses otherwise.

## Math Concepts

A CDS contract has two legs:

**The premium leg (protection buyer pays)**

The protection buyer pays the CDS spread $s$ (in basis points per year) on the notional $N$ at regular intervals (typically quarterly) until the earlier of: (a) maturity $T$, or (b) a credit event.

**The protection leg (protection seller pays)**

If a credit event occurs at time $\tau \leq T$, the protection seller pays the loss given default:

$$\text{Protection payment} = N \times (1 - R)$$

where $R$ is the recovery rate — the fraction of face value recovered by bondholders in bankruptcy. Market convention typically assumes $R = 0.40$ (40%) for senior unsecured debt, though recovery varies widely.

**Fair value spread (single-name CDS)**

Under the assumption of a constant risk-free rate $r$ and constant hazard rate $\lambda$ (instantaneous default intensity), the fair CDS spread is:

$$s = \frac{(1 - R) \cdot \lambda}{r + \lambda}$$

This can be derived by setting the present value of the premium leg equal to the present value of the protection leg.

*Intuition:* $(1-R)$ is the loss given default. $\lambda$ is the probability of defaulting per unit time. $r + \lambda$ is the total "discount rate" — you discount both for time value ($r$) and for the chance the contract terminates early due to default ($\lambda$). Higher default probability (higher $\lambda$) → higher spread.

**Survival probability.** The probability of surviving (no default) until time $t$ under constant hazard rate:

$$P(\tau > t) = e^{-\lambda t}$$

The hazard rate $\lambda$ is related to the CDS spread approximately as:

$$\lambda \approx \frac{s}{1 - R}$$

**Mark-to-market.** After initiation, the value of a CDS to the protection buyer changes as the credit quality of the reference entity changes. If the CDS spread widens (credit quality deteriorates), the value of protection bought at the original (lower) spread increases — you can close out for a profit.

**CDS term structure.** Just as bond yields vary by maturity, CDS spreads vary by tenor (1yr, 2yr, 3yr, 5yr, 7yr, 10yr). The term structure reveals market expectations:
- **Upward sloping:** Default is more likely far in the future (healthy company with long-term uncertainty).
- **Downward sloping (inverted):** Market fears near-term default — the "distressed" shape. Seen in pre-default situations.
- **Humped:** Near-term stability, medium-term concern, long-term normalization.

**Hazard rate bootstrapping.** The market quotes CDS at discrete tenors. To get a continuous hazard rate curve, you bootstrap: start with the 1-year CDS spread, solve for the hazard rate implied by that spread, then move to the 2-year spread (holding the 1-year hazard rate fixed), and so on. This is analogous to bootstrapping the yield curve from bond prices.

**CDS indices.** Single-name CDS reference one company. CDS indices reference a basket of companies:
- **CDX.NA.IG:** 125 North American investment-grade credits (5yr standard)
- **CDX.NA.HY:** 100 high-yield credits
- **iTraxx Europe:** 125 European investment-grade credits

Index spreads provide a benchmark for overall credit market conditions — rising CDX spreads signal broad credit stress, just as rising VIX signals equity market stress.

## Walkthrough

**Contract terms:**
- Reference entity: Fictional airline, "Atlas Air"
- Notional: \$10,000,000
- Maturity: 5 years
- CDS spread: 200 bp (2.00% per year)
- Recovery rate assumption: 40%
- Payment frequency: Quarterly

**Premium leg payments (no default):**

Each quarter, the protection buyer pays:
$$\text{Premium}_{\text{quarterly}} = s \times N \times \Delta t = 0.02 \times \$10{,}000{,}000 \times 0.25 = \$50{,}000$$

Over the full 5 years (20 quarterly payments, if no default):
$$\text{Total premium paid} = 20 \times \$50{,}000 = \$1{,}000{,}000$$

**Credit event scenario (default at year 2.0):**

Atlas Air defaults 2 years into the contract. Market price of the bonds in default is 40 cents on the dollar (recovery = 40%).

Protection seller pays:
$$(1 - 0.40) \times \$10{,}000{,}000 = \$6{,}000{,}000$$

Protection buyer stops paying premiums. The buyer paid \$400,000 in premiums over 2 years and received \$6,000,000 — a net gain of \$5,600,000 on the CDS contract (which offsets the ~\$6M loss on the bond itself).

**Hazard rate from spread:**
$$\lambda \approx \frac{s}{1 - R} = \frac{0.02}{1 - 0.40} = \frac{0.02}{0.60} = 0.0333 \text{ per year}$$

**5-year survival probability:**
$$P(\tau > 5) = e^{-0.0333 \times 5} = e^{-0.167} \approx 84.6\%$$

The market prices in about a 15.4% chance of default within 5 years for this 200 bp spread.

## Analysis

**Credit events.** ISDA (International Swaps and Derivatives Association) defines the legal trigger events:
- **Bankruptcy:** Filing for court protection.
- **Failure to pay:** Missing a coupon or principal payment (after a grace period).
- **Restructuring:** Debt terms modified unfavorably — haircut on principal, extended maturity, lower coupon. (Whether restructuring triggers CDS is jurisdiction-dependent and contentious.)
- **Obligation acceleration / default:** Bond becomes immediately due due to a covenant breach.

Sovereign CDS also includes **repudiation/moratorium** (government refuses to honor debt).

**Basis risk: CDS spread vs. bond spread.**

In theory, the CDS spread should equal the bond's credit spread over the risk-free rate (the "CDS-bond basis"). In practice, they diverge due to:
- **Cheapest-to-deliver (CTD) option:** After a credit event, the protection seller accepts delivery of the defaulted bond. If multiple bonds exist, the buyer delivers the cheapest one — which is worth more to the buyer than the "average" bond.
- **Funding costs:** Buying a bond requires capital; a CDS does not. This creates a basis.
- **Restructuring definitions:** Different ISDA definitions across jurisdictions affect whether a CDS pays out.

**Counterparty risk.** The protection seller must be able to pay when defaults spike — precisely when financial firms are under the most stress. Post-2008, most standardized CDS are now centrally cleared through CCPs (central counterparties like ICE Clear Credit), which collect daily margin and mutualize counterparty risk. Bilateral (uncleared) CDS still exist for customized trades.

**Leverage.** A CDS provides credit exposure equal to the full notional for a fraction of the upfront cost. A 200 bp spread on \$10M notional costs \$200,000/year — but provides \$6M of protection. This makes CDS a highly leveraged instrument.

## Implementation

```python
import numpy as np
import pandas as pd
from scipy.optimize import brentq
import matplotlib.pyplot as plt

# ── 1. CDS fair spread calculator ─────────────────────────────────────────
def cds_fair_spread(
    hazard_rate: float,
    recovery: float = 0.40,
    risk_free_rate: float = 0.04,
    maturity_years: float = 5.0,
    payment_freq: int = 4,        # quarterly
) -> float:
    """
    Compute the fair CDS spread using discrete premium and protection legs.
    
    Premium leg PV   = sum over payment dates of: s * dt * N * survival_prob * discount
    Protection leg PV = sum over periods of: (1-R) * default_prob_in_period * discount
    
    Returns fair spread in decimal (e.g., 0.02 = 200 bp).
    """
    dt = 1.0 / payment_freq
    times = np.arange(dt, maturity_years + dt/2, dt)  # payment dates
    
    # Survival probability and discount factor at each time
    surv = np.exp(-hazard_rate * times)
    disc = np.exp(-risk_free_rate * times)
    
    # Premium leg (unit notional, unit spread): sum of dt * S(t) * D(t)
    pv_premium_per_bp = np.sum(dt * surv * disc)
    
    # Protection leg: probability of defaulting in each period × (1-R) × discount
    # P(default in [t-dt, t]) ≈ S(t-dt) - S(t)
    times_mid = times - dt/2
    surv_prev = np.concatenate([[1.0], surv[:-1]])
    default_prob_period = surv_prev - surv     # prob of default in this period
    disc_mid = np.exp(-risk_free_rate * times_mid)
    
    pv_protection = (1 - recovery) * np.sum(default_prob_period * disc_mid)
    
    return pv_protection / pv_premium_per_bp

# Example: compute fair spread for a range of hazard rates
hazard_rates = np.linspace(0.001, 0.20, 200)
spreads_bps  = [cds_fair_spread(h) * 10_000 for h in hazard_rates]

print("CDS Fair Spread Examples (R=40%, r=4%, 5yr):")
for h in [0.01, 0.02, 0.05, 0.10, 0.15]:
    s_bps = cds_fair_spread(h) * 10_000
    survival = np.exp(-h * 5) * 100
    print(f"  Hazard rate {h:.0%}/yr -> Spread {s_bps:.0f} bp,  5yr survival {survival:.1f}%")

# ── 2. Implied hazard rate from observed CDS spread ───────────────────────
def implied_hazard_rate(
    spread: float,               # in decimal, e.g. 0.02 for 200bp
    recovery: float = 0.40,
    risk_free_rate: float = 0.04,
    maturity_years: float = 5.0,
) -> float:
    """Back out the hazard rate implied by a quoted CDS spread."""
    def objective(h):
        return cds_fair_spread(h, recovery, risk_free_rate, maturity_years) - spread
    return brentq(objective, 1e-6, 0.99)

spread_200bp = 0.020   # 200 basis points
h_implied = implied_hazard_rate(spread_200bp)
print(f"\nImplied hazard rate for 200 bp spread: {h_implied:.4f} ({h_implied*100:.2f}%/yr)")
print(f"Implied 5yr survival probability: {np.exp(-h_implied*5):.1%}")

# ── 3. Hazard rate bootstrapping from CDS term structure ──────────────────
# Suppose the market quotes these CDS spreads at standard tenors:
cds_term_structure = {
    1: 0.0080,   # 80 bp
    2: 0.0120,   # 120 bp
    3: 0.0160,   # 160 bp
    5: 0.0200,   # 200 bp
    7: 0.0220,   # 220 bp
   10: 0.0230,   # 230 bp
}

def bootstrap_hazard_curve(
    cds_quotes: dict[int, float],
    recovery: float = 0.40,
    risk_free_rate: float = 0.04,
) -> dict[int, float]:
    """
    Bootstrap piecewise-constant hazard rates from CDS term structure.
    At each tenor, solve for the hazard rate that prices the CDS correctly,
    holding prior-period hazard rates fixed.
    """
    hazard_curve = {}
    sorted_tenors = sorted(cds_quotes.keys())
    
    for tenor in sorted_tenors:
        spread = cds_quotes[tenor]
        h = implied_hazard_rate(spread, recovery, risk_free_rate, tenor)
        hazard_curve[tenor] = h
    
    return hazard_curve

hazard_curve = bootstrap_hazard_curve(cds_term_structure)
print("\nBootstrapped hazard curve:")
print(f"{'Tenor':>6} | {'CDS Spread':>12} | {'Hazard Rate':>12} | {'Survival Prob':>14}")
print("-" * 52)
for tenor, h in hazard_curve.items():
    spread_bps = cds_term_structure[tenor] * 10_000
    surv = np.exp(-h * tenor) * 100
    print(f"{tenor:>5}yr | {spread_bps:>10.0f} bp | {h*100:>10.2f}%/yr | {surv:>13.1f}%")

# ── 4. P&L simulation: protection buyer over a credit event ───────────────
notional = 10_000_000
spread = 0.020            # 200 bp
recovery = 0.40
default_year = 2.0        # default at year 2
payment_freq = 4          # quarterly

# Premiums paid before default
quarters_paid = int(default_year * payment_freq)
premium_per_quarter = spread * notional / payment_freq
total_premiums_paid = quarters_paid * premium_per_quarter

# Protection payment received
protection_received = (1 - recovery) * notional

net_pnl = protection_received - total_premiums_paid

print(f"\nCDS P&L: Protection Buyer (default at year {default_year})")
print(f"  Premiums paid   : ${total_premiums_paid:>12,.0f}  ({quarters_paid} quarters)")
print(f"  Protection rcvd : ${protection_received:>12,.0f}")
print(f"  Net CDS P&L     : ${net_pnl:>12,.0f}")

# ── 5. Spread sensitivity to default probability ──────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Spread vs hazard rate
axes[0].plot(np.array(hazard_rates) * 100, spreads_bps, 'b-', linewidth=2)
axes[0].set_xlabel('Hazard Rate (%/yr)')
axes[0].set_ylabel('CDS Spread (bp)')
axes[0].set_title('CDS Spread vs Default Intensity')
axes[0].grid(True, alpha=0.3)

# CDS term structure and implied survival probability
tenors = list(cds_term_structure.keys())
surv_probs = [np.exp(-hazard_curve[t] * t) * 100 for t in tenors]
axes[1].bar(tenors, surv_probs, color='steelblue', alpha=0.7)
axes[1].set_xlabel('Tenor (years)')
axes[1].set_ylabel('Survival Probability (%)')
axes[1].set_title('Implied Survival Probabilities from CDS Curve')
axes[1].set_ylim(0, 100)
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('cds_analysis.png', dpi=150)
plt.show()
```

## Bridge to Quant / ML

**Credit spread as a signal.** CDS spreads are real-time, liquid indicators of corporate credit quality — they update continuously, unlike credit ratings (which lag). Quant strategies use CDS spread levels and changes as signals: widening spreads predict negative equity returns (companies under financial stress), steepening CDS curves signal near-term default concern, and cross-sectional CDS ranks identify relative credit quality across a sector.

**Credit-equity relationship.** By Merton's model (1974), equity is a call option on the firm's assets with strike equal to the face value of debt. This creates a structural link between equity prices, equity volatility, and CDS spreads. When equity vol rises, CDS spreads should widen. Basis trades (long CDS + long equity) exploit deviations from this relationship.

**Risk management.** Any portfolio with significant corporate bond exposure uses CDS to hedge credit risk without liquidating the bond positions. VaR and ES calculations for credit portfolios require modeling correlated default probabilities — a problem closely related to covariance estimation and factor models.

**ML connections:**
- Predicting CDS spread changes is a classification/regression problem: features include equity returns, equity volatility, interest coverage ratios, sector indicators, and macro factors. Random forests and gradient boosted trees have been applied to this.
- CDS term structure inversion (predicting near-term default risk) is an early-warning classification problem: the inverted curve is a leading indicator of distress.
- Credit portfolio modeling uses copulas to capture joint default correlations — Gaussian copula (the "Li formula" behind CDO pricing) was the dominant model pre-2008 and its failure in capturing tail dependence was a major cause of crisis mispricing.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** A CDS buyer is described as buying "insurance" on a bond. What are two key ways a CDS differs from regular insurance — one in terms of who can buy it, and one in terms of the seller's obligations?
<details>
<summary>Answer</summary>
(1) Insurable interest: insurance typically requires you to own the thing being insured. CDS has no such requirement — you can buy protection on a company's debt without owning any of that company's bonds. This makes CDS a pure speculation vehicle: investors buy protection simply because they believe the company will default, with no underlying credit exposure to hedge. (2) Bilateral credit risk: in insurance, the insurer is regulated and required to maintain capital reserves. In CDS (especially pre-2008 uncleared CDS), the protection seller faced no such requirement. AIG sold protection on hundreds of billions of notional with minimal capital backing. When correlations moved against them, they couldn't pay — demonstrating that "insurance" from a counterparty with insufficient capital is worth nothing precisely when you need it most.
</details>

**Q2.** The hazard rate λ is described as the "instantaneous default intensity." Explain what it means practically and why the survival probability P(τ > t) = e^{-λt} follows from this definition.
<details>
<summary>Answer</summary>
The hazard rate λ means: in any very short interval [t, t+dt], the probability of defaulting (given no default so far) is approximately λ × dt. It is the continuous-time analog of a "default rate per unit time." This is identical to the structure of radioactive decay or a Poisson arrival process. The survival probability follows from integrating the hazard: P(survive past t) = P(no Poisson event in [0,t]) = e^{-λt}. Intuitively, each small interval contributes a multiplicative survival factor of (1 − λ dt) ≈ e^{-λ dt}, and multiplying these over [0, t] gives e^{-λt}. For a 200bp CDS spread with 40% recovery, λ ≈ 0.02/0.6 ≈ 3.3%/year, giving a 5-year survival probability of e^{-0.033 × 5} ≈ 84.6%.
</details>

**Q3.** In the 2008 financial crisis, AIG's CDS book nearly brought down the global financial system. Explain the mechanism: why was AIG's position so dangerous, and what about CDS structure specifically created this systemic risk?
<details>
<summary>Answer</summary>
AIG had sold enormous amounts of CDS protection on mortgage-backed securities and CDOs — effectively writing insurance that these assets would not default. The premiums they collected were modest; the potential payouts were hundreds of billions. When US housing prices collapsed, the underlying CDOs suffered massive losses, triggering CDS credit events. AIG had to pay out protection — but had not reserved capital for these scenarios (assuming diversification would prevent correlated defaults). Simultaneously, the collateral agreements in their bilateral CDS contracts required AIG to post additional collateral as spreads widened, even before actual defaults — creating immediate cash calls they couldn't meet. Because AIG was the counterparty for protection bought by Goldman Sachs, Deutsche Bank, Societe Generale, and others, AIG's failure would have left these firms with massive, unhedged credit losses. The US government bailout of AIG was effectively a bailout of AIG's counterparties. The specific CDS structure that enabled this: bilateral trading with no central clearing, no mandatory capital requirements, and collateral terms that created liquidity spirals (mark-to-market losses → collateral calls → forced selling → further losses).
</details>

---

### Level 2 — Quantitative

**Q4.** A 5-year CDS on a company trades at a spread of 150bp. The recovery rate assumption is 40% and the risk-free rate is 3%. Compute: (a) the implied hazard rate using the approximation λ ≈ s/(1−R), (b) the 5-year survival probability, (c) the implied probability of default within 5 years.
<details>
<summary>Answer</summary>
(a) λ ≈ s/(1−R) = 0.015 / (1 − 0.40) = 0.015 / 0.60 = 0.025 per year = 2.5%/year.

(b) 5-year survival probability: P(τ > 5) = e^{−λ × 5} = e^{−0.025 × 5} = e^{−0.125} = 0.8825 = 88.25%.

(c) Probability of default within 5 years = 1 − 0.8825 = 11.75%. The market is pricing in roughly a 12% chance of default over 5 years for this 150bp spread.
</details>

**Q5.** Protection buyer enters a 5-year CDS on \$5,000,000 notional at 300bp (3%/year), paying quarterly. After 1.5 years, the company's credit deteriorates and the 5-year CDS spread has widened to 600bp. Compute: (a) quarterly premium payments, (b) total premiums paid after 1.5 years, (c) the approximate mark-to-market gain on the CDS position (use the annuity approximation: MTM ≈ (s_new − s_old) × remaining_years × notional).
<details>
<summary>Answer</summary>
(a) Quarterly premium = s × N × Δt = 0.03 × 5,000,000 × 0.25 = \$37,500 per quarter.

(b) After 1.5 years = 6 quarters: total premiums paid = 6 × $37,500 = $225,000.

(c) Spread widened from 300bp to 600bp. Remaining life = 5 − 1.5 = 3.5 years.
MTM ≈ (0.06 − 0.03) × 3.5 × 5,000,000 = 0.03 × 3.5 × 5,000,000 = \$525,000 gain.

The protection buyer paid \$225,000 in premiums and now has a mark-to-market gain of ~\$525,000 — a net profit of ~\$300,000 without a credit event having occurred. They can close the position by selling protection at 600bp to lock in this gain.
</details>

---

### Level 3 — Coding

**Q6.** The `cds_fair_spread` function computes default probability in each period as `surv_prev - surv`, where `surv_prev = np.concatenate([[1.0], surv[:-1]])`. Why does `surv_prev` start with 1.0, and what would happen to the protection leg PV if you forgot this and used `surv_prev = surv` (starting from the first payment date's survival probability instead)?
<details>
<summary>Answer</summary>
`surv_prev[0] = 1.0` represents the survival probability at time zero — the start of the contract. The probability of defaulting in the first period [0, dt] is P(survive to 0) − P(survive to dt) = 1.0 − e^{-λ·dt}. This is the first default probability bucket, and it must be computed using the starting survival probability of 1.0 (certainty of survival at inception).

If you used `surv_prev = surv` (shifted by one period), you'd be computing default probability in the first period as e^{-λ·dt} − e^{-λ·2dt} — which is the probability of defaulting in the *second* period, not the first. You would miss the default probability in [0, dt] entirely and instead double-count the second period. For a high-hazard-rate credit (say λ = 20%/year), the first-period default probability is substantial — omitting it would understate the protection leg PV significantly, producing a fair spread that is too low.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| CDS buyers must own the underlying bond | CDS have no insurable interest requirement — any counterparty can buy or sell protection regardless of bond ownership. "Naked CDS" are pure credit speculation positions |
| The CDS spread equals the bond's yield spread | In theory they are equal (the CDS-bond basis should be zero). In practice they diverge due to cheapest-to-deliver optionality, funding costs, ISDA definitional differences, and technical supply/demand imbalances |
| Central clearing eliminated CDS counterparty risk | Central clearing reduces bilateral counterparty risk but concentrates it in the CCP. A CCP failure would be more systemic than a single dealer failure. Clearing also doesn't cover customized bilateral CDS |
| A high CDS spread means default is imminent | A high spread means the market prices elevated default probability — it doesn't predict timing. Companies can trade at 500bp+ spreads for years (distressed but surviving) or default suddenly from 50bp (surprise event). The spread reflects risk-neutral probability including a risk premium |

## Related Concepts

- [[Bond Basics]] — the underlying instrument that CDS reference; bond credit spread vs. CDS spread
- [[Yield Curve]] — risk-free rate term structure underpins CDS valuation; sovereign CDS reference government default risk
- [[Value at Risk]] — credit VaR measures the tail risk of default losses in bond/loan portfolios
- [[Stress Testing]] — scenario testing for credit portfolios includes CDS spread shocks and default rate shocks
- [[Interest Rate Swaps]] — structurally similar two-leg derivative; CDS replaces interest rate risk with credit default risk

## Sources Used

- Hull, J. (2022). *Options, Futures and Other Derivatives*, 11th ed., chs. 24–25 — CDS mechanics, valuation, hazard rates
- O'Kane, D. (2008). *Modelling Single-name and Multi-name Credit Derivatives*. Wiley Finance — comprehensive CDS reference
- ISDA (2014). *Credit Derivatives Definitions* — legal definitions of credit events
- Li, D.X. (2000). On default correlation: A copula function approach. *Journal of Fixed Income* — the Gaussian copula model

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | initial build |
