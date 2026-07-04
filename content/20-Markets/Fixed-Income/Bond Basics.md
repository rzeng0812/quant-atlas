---
type: concept
domain: 20-Markets
tags: [fixed-income, bonds, markets]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-18
review_interval_days: 365
sources:
  - "Hull - Options, Futures, and Other Derivatives ch.4"
created: 2026-04-18
---

> [!info] Problem Chain
> **Chain:** Pricing → Gap 1: No agreed method to value an uncertain future payoff (fixed-income analog)
> **This concept:** Establishes that a bond's fair price is the present value of all promised cash flows discounted at the market yield — the no-arbitrage pricing foundation of all fixed income.
> **Alternative approaches to this gap:** none (PV discounting is the universal framework; dispute is only about *which* discount rate to use)
> **You need first:** [[Yield Curve]] (the source of discount rates)
> **This unlocks:** [[Duration]], [[Convexity]], [[Interest Rate Swaps]], [[Vasicek Model]], [[HJM Framework]]

> The simplest loan repackaged as a tradeable instrument; price = PV of future cash flows

## Why This Exists

**The gap:** Before standardized bond pricing, different participants used inconsistent conventions — some discounted coupon-by-coupon, others used approximate rules — producing disagreements over fair value and making bonds difficult to trade across institutions.
**What came before:** Informal loan pricing based on face value and coupon rate alone, with no formal present-value calculation. The discount rate (yield) was not explicitly separated from the coupon rate, making it impossible to systematically compare bonds of different maturities and coupons.
**What this adds:** The bond pricing formula $P = \sum C/(1+y)^t + F/(1+y)^T$ provides a universal, agreed-upon method to convert any promise of future cash flows into a present value. It makes the inverse relationship between price and yield explicit, enables comparison across bonds via YTM, and provides the foundation for all subsequent fixed-income risk measurement (duration, convexity) and derivative pricing (swaps, caps, floors).
**What it still doesn't solve:** A single YTM treats all cash flows as discounted at one flat rate, ignoring the fact that market rates differ across maturities. The [[Yield Curve]] captures this richness; bond basics is the single-rate approximation that [[Duration]] and [[Convexity]] refine.

## Math Concepts

### Bond Price Formula

A bond with face value $F$, annual coupon payment $C$, yield-to-maturity $y$, and $T$ years to maturity:

$$P = \sum_{t=1}^{T} \frac{C}{(1+y)^t} + \frac{F}{(1+y)^T}$$

The first term sums the discounted coupon payments; the second discounts the face value repayment.

### Yield to Maturity (YTM)

YTM is the single discount rate $y$ that makes the present value of all future cash flows equal to the market price $P$. It is the bond's internal rate of return if held to maturity.

There is no closed-form solution — $y$ must be solved numerically (e.g., via bisection or Newton's method).

$$P = \sum_{t=1}^{T} \frac{C}{(1+y)^t} + \frac{F}{(1+y)^T} \quad \Rightarrow \quad \text{solve for } y$$

### Zero Coupon Bond

A zero-coupon bond pays no intermediate coupons — only the face value at maturity. Using continuous compounding:

$$P = F \cdot e^{-rT}$$

Where $r$ is the continuously compounded rate. Zero-coupon bonds are the building blocks of all yield curve construction.

### Par, Premium, and Discount

The relationship between coupon rate and YTM determines whether a bond trades above or below face value:

| Condition | Bond trades at |
|-----------|---------------|
| Coupon rate = YTM | **Par** ($P = F$) |
| Coupon rate > YTM | **Premium** ($P > F$) |
| Coupon rate < YTM | **Discount** ($P < F$) |

Intuition: if you're promised 5% coupons but the market only requires 4%, you'd pay extra up front for that extra 1% per year.

### Clean Price vs Dirty Price

Between coupon dates, interest **accrues** to the seller. Market convention quotes the **clean price** (no accrued interest), but you actually pay the **dirty price**:

$$\text{Dirty Price} = \text{Clean Price} + \text{Accrued Interest}$$

$$\text{Accrued Interest} = C \times \frac{\text{days since last coupon}}{\text{days in coupon period}}$$

### Semi-Annual Conventions

Most government bonds pay coupons semi-annually. Adjust by: halving the coupon ($C/2$), halving the yield ($y/2$), and doubling the number of periods ($2T$):

$$P = \sum_{t=1}^{2T} \frac{C/2}{(1+y/2)^t} + \frac{F}{(1+y/2)^{2T}}$$

### Price-Yield Relationship

The price-yield curve is **inverse and convex**: price falls as yield rises, but the fall slows down at higher yields. This convexity means:
- Duration (first derivative) gives the linear approximation of price change.
- Convexity (second derivative) corrects for the curvature. See [[Duration]] and [[Convexity]].

## Walkthrough

**Example:** 5-year bond, face value \$1,000, coupon rate 5% (annual payments), YTM = 4%.

Annual coupon: $C = 1000 \times 5\% = \$50$

$$P = \frac{50}{1.04^1} + \frac{50}{1.04^2} + \frac{50}{1.04^3} + \frac{50}{1.04^4} + \frac{1050}{1.04^5}$$

| Year | Cash Flow | Discount Factor | PV |
|------|-----------|----------------|----|
| 1 | 50 | 1.0400 | 48.08 |
| 2 | 50 | 1.0816 | 46.23 |
| 3 | 50 | 1.1249 | 44.45 |
| 4 | 50 | 1.1699 | 42.74 |
| 5 | 1050 | 1.2167 | 863.02 |
| **Total** | | | **\$1,044.52** |

Since the coupon rate (5%) exceeds the YTM (4%), the bond trades at a **premium**: $1,044.52 > $1,000.

**Check:** if YTM were 5% (equal to coupon), the price would be exactly \$1,000 (par). If YTM were 6%, the price would drop below par — a discount.

## Analysis

### Bond Risks

| Risk | Description |
|------|-------------|
| **Interest rate risk** | Price falls when rates rise. Measured by [[Duration]] and [[Convexity]]. |
| **Credit risk** | Issuer may default and fail to pay coupons or principal. |
| **Inflation risk** | Fixed nominal payments buy less in real terms as inflation rises. |
| **Liquidity risk** | Hard to sell quickly at fair value, especially for corporate bonds. |
| **Reinvestment risk** | Coupon payments may need to be reinvested at lower future rates. |

### Credit Quality

Rating agencies (Moody's, S&P, Fitch) assess the probability of issuer default:

- **Investment grade:** AAA → BBB (Moody's: Aaa → Baa). Lower yield; institutional investors required to hold these.
- **High yield ("junk"):** BB and below. Higher yield to compensate for default risk.
- **Spread:** the extra yield above a comparable Treasury is the **credit spread**, which prices in default risk and liquidity.

### Yield Curve Context

Bonds of different maturities trade at different yields — the [[Yield Curve]] captures this. Longer maturity bonds typically offer higher yields (term premium), but not always. An inverted yield curve (short rates > long rates) is historically a recession signal.

### The Price-Yield Trade-off Summarized

- **Short maturity, high coupon** → low duration → low price sensitivity to rates.
- **Long maturity, low coupon (or zero coupon)** → high duration → high price sensitivity to rates.
- A 30-year zero-coupon bond is the most volatile; a 3-month T-bill barely moves.

## Implementation

```python
import numpy as np
from scipy.optimize import brentq
import matplotlib.pyplot as plt


def bond_price(face: float, coupon_rate: float, ytm: float,
               maturity: int, frequency: int = 2) -> float:
    """
    Compute the price of a coupon bond.

    Parameters
    ----------
    face        : float - par/face value (e.g. 1000)
    coupon_rate : float - annual coupon rate (e.g. 0.05 for 5%)
    ytm         : float - annual yield to maturity (e.g. 0.04)
    maturity    : int   - years to maturity
    frequency   : int   - coupon payments per year (2 = semi-annual, default)

    Returns
    -------
    float : dirty price of the bond
    """
    coupon = face * coupon_rate / frequency          # coupon per period
    y_per = ytm / frequency                          # yield per period
    n = maturity * frequency                         # total periods

    periods = np.arange(1, n + 1)
    cash_flows = np.full(n, coupon)
    cash_flows[-1] += face                           # principal at maturity

    pv = cash_flows / (1 + y_per) ** periods
    return pv.sum()


def ytm_solver(face: float, coupon_rate: float, price: float,
               maturity: int, frequency: int = 2) -> float:
    """
    Solve for yield to maturity given market price.

    Uses Brent's method to find the root of: bond_price(y) - price = 0
    """
    func = lambda y: bond_price(face, coupon_rate, y, maturity, frequency) - price
    # Search in [0.0001, 0.5] — covers any realistic bond yield
    return brentq(func, 0.0001, 0.5)


# ── Example: 5-year, 5% coupon, 4% YTM, semi-annual ──────────────────────────
face = 1000
coupon_rate = 0.05
ytm = 0.04
maturity = 5
freq = 2

price = bond_price(face, coupon_rate, ytm, maturity, freq)
print(f"Bond price (semi-annual, YTM=4%): ${price:.2f}")
# Expected: ~$1,044.91 (semi-annual convention gives slightly different result)

# Recover YTM from price
recovered_ytm = ytm_solver(face, coupon_rate, price, maturity, freq)
print(f"Recovered YTM: {recovered_ytm:.4%}")

# ── Plot: price vs yield (the convex curve) ───────────────────────────────────
yields = np.linspace(0.001, 0.15, 300)
prices = [bond_price(face, coupon_rate, y, maturity, freq) for y in yields]

plt.figure(figsize=(8, 4))
plt.plot(yields * 100, prices, color='steelblue', linewidth=2)
plt.axvline(x=coupon_rate * 100, color='gray', linestyle='--', label='Coupon rate (5%)')
plt.axhline(y=face, color='gray', linestyle=':', label='Par ($1,000)')
plt.xlabel('Yield to Maturity (%)')
plt.ylabel('Bond Price ($)')
plt.title('Bond Price vs Yield — 5yr, 5% Coupon (semi-annual)')
plt.legend()
plt.tight_layout()
plt.show()
# Observe: convex downward curve; price = par exactly where yield = coupon rate


# ── Zero-coupon bond comparison ───────────────────────────────────────────────
def zero_coupon_price(face: float, r: float, T: float) -> float:
    """Continuous compounding."""
    return face * np.exp(-r * T)


zcb_price = zero_coupon_price(1000, 0.04, 5)
print(f"\nZero-coupon bond price (4%, 5yr, cont.): ${zcb_price:.2f}")
# Compare: much lower price — all value at maturity, discounted heavily


# ── Accrued interest example ──────────────────────────────────────────────────
def accrued_interest(face: float, coupon_rate: float,
                     days_since_coupon: int, days_in_period: int = 182) -> float:
    """Semi-annual accrued interest (Actual/Actual convention)."""
    semi_annual_coupon = face * coupon_rate / 2
    return semi_annual_coupon * (days_since_coupon / days_in_period)


ai = accrued_interest(1000, 0.05, days_since_coupon=45)
clean_price = 1020.00
dirty_price = clean_price + ai
print(f"\nClean price: ${clean_price:.2f}")
print(f"Accrued interest (45 days): ${ai:.2f}")
print(f"Dirty price (what you pay): ${dirty_price:.2f}")
```

## Bridge to Quant / ML

**Yield curve fitting:** Bond prices are the raw inputs used to bootstrap the [[Yield Curve]]. Each bond gives one equation; collectively they pin down the term structure of interest rates. All interest rate derivatives are priced off this curve.

**Fixed-income factor models:** The first three principal components of yield curve moves — level, slope, and curvature — explain ~99% of bond price variance. Duration loads almost purely on the level factor. This is why PCA is so natural in fixed income.

**Credit spread modeling:** Investment-grade bond yields = risk-free rate + credit spread. Credit spreads can be modeled as mean-reverting processes (similar to Vasicek, see [[Vasicek Model]]) or implied from CDS prices. ML models use bond characteristics (rating, sector, duration, covenant quality) to predict spread changes.

**Arbitrage-free pricing:** No-arbitrage pricing — the foundation of [[HJM Framework]] and derivatives pricing — generalizes the bond PV formula into a continuous-time setting with stochastic rates.

**Risk management:** Bond portfolios are stress-tested by shocking the yield curve (parallel shift, steepening, flattening). DV01 from [[Duration]] and convexity from [[Convexity]] are the primary risk metrics. Regulatory capital (Basel III) for bond books is computed from these sensitivities.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why do bond prices and interest rates move in opposite directions? Give the intuition without using a formula.
<details><summary>Answer</summary>When you buy a bond, you lock in a series of fixed cash flows (coupons and principal). If market interest rates rise after you buy, new bonds are issued with higher coupons for the same price. Your old bond now looks worse by comparison — nobody will pay you full price for a below-market coupon stream. You must sell at a discount. Conversely, if rates fall, your above-market coupons become attractive, and buyers will pay a premium to own them. The bond price is simply the present value of fixed future cash flows: higher discount rates mean lower present values, so higher rates mean lower prices.</details>

**Q2.** What is the difference between a bond's coupon rate and its yield to maturity? Can they ever differ, and if so, why?
<details><summary>Answer</summary>The coupon rate is fixed at issuance — it determines the dollar amount of each coupon payment ($C = \text{face} \times \text{coupon rate}$). The YTM is the current market discount rate that makes the present value of all future cash flows equal to the market price. They differ whenever the market price differs from par: if the bond trades at a discount (price < face), the YTM > coupon rate (you earn extra return from the price appreciation to par). If it trades at a premium (price > face), YTM < coupon rate. Only when price = par does YTM = coupon rate exactly.</details>

**Q3.** Why does accrued interest matter when buying a bond between coupon dates? Who pays it and to whom?
<details><summary>Answer</summary>When you buy a bond between coupon dates, the seller has been "earning" the next coupon for the portion of the period they held the bond — they deserve compensation for those days. The bond price quoted in the market (clean price) does not include this, but the actual settlement price (dirty price) does. The buyer pays the seller accrued interest at settlement, then receives the full next coupon on the payment date. Net result: the buyer effectively receives only their proportionate share of the next coupon, and the seller receives theirs via the upfront accrued interest payment.</details>

---

### Level 2 — Quantitative

**Q4.** A 3-year bond has face value \$1,000, coupon rate 6% (annual), and the current YTM is 8%. Compute the bond price and identify whether it trades at par, premium, or discount.
<details><summary>Answer</summary>$P = 60/1.08 + 60/1.08^2 + 1060/1.08^3 = 55.56 + 51.44 + 841.62 = \$948.62$. Since $948.62 < 1000$, the bond trades at a **discount** — the coupon rate (6%) is below the YTM (8%), so the market demands a price reduction to make the total return competitive with 8% bonds.</details>

**Q5.** A 10-year zero-coupon bond with face value \$1,000 is priced at \$613.91. What is the continuously compounded YTM?
<details><summary>Answer</summary>$P = F \cdot e^{-rT}$ → $613.91 = 1000 \cdot e^{-r \times 10}$ → $e^{-10r} = 0.61391$ → $-10r = \ln(0.61391) = -0.48790$ → $r = 4.879\%$. The continuously compounded zero rate for 10 years is 4.879%. Compare: $(1000/613.91)^{1/10} - 1 = 4.997\%$ as an annually compounded rate — the continuous rate is slightly lower.</details>

---

### Level 3 — Coding

**Q6.** The `ytm_solver` function uses Brent's method to solve for YTM. Why can't you solve for YTM analytically, and what property of the `bond_price(y)` function guarantees that Brent's method will find the solution?
<details><summary>Answer</summary>YTM requires solving $P = \sum_{t=1}^{n} \frac{C/(1+y/f)^t}{} + F/(1+y/f)^n$, which is a polynomial equation in $(1+y/f)$ of degree $n$. For $n > 4$, the Abel-Ruffini theorem states there is no general closed-form algebraic solution. Brent's method is guaranteed to converge because `bond_price(y)` is (a) continuous, (b) strictly decreasing in $y$ (bond prices fall as yields rise), and (c) the search bracket $[0.0001, 0.50]$ covers all realistic yields and satisfies `bond_price(0.0001) > price > bond_price(0.50)` for any positive-coupon bond trading within normal ranges. These conditions guarantee a unique root exists within the bracket and Brent's method will find it.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| A bond with a high coupon is always a good investment | A high coupon bond may trade at a premium, with YTM lower than the coupon rate. What matters is the YTM relative to alternative investments, not the coupon rate. |
| The quoted price is what you pay for a bond | The quoted (clean) price excludes accrued interest. The dirty price (what you actually pay) = clean price + accrued interest. |
| A zero-coupon bond has zero return | A ZCB pays no coupons but is bought at a deep discount and redeemed at par — all return comes from price appreciation. The YTM can be identical to a coupon bond of the same maturity and credit quality. |
| YTM tells you your actual return | YTM equals your actual return only if you hold to maturity AND can reinvest each coupon at exactly the YTM rate. Reinvestment risk means actual return will differ from YTM in most cases. |

## Related Concepts

- [[Duration]] — measures price sensitivity to yield changes (first derivative of price w.r.t. yield)
- [[Convexity]] — second-order correction; why duration over-estimates price drops
- [[Yield Curve]] — bonds of different maturities form the term structure
- [[Interest Rate Swaps]] — derivatives that swap fixed vs floating rate obligations
- [[Vasicek Model]] — one-factor model for the short rate underlying bond prices
- [[HJM Framework]] — no-arbitrage model for the entire forward rate curve

## Sources Used

- Hull, J. - *Options, Futures, and Other Derivatives*, ch. 4 (Interest Rates, Bond Pricing)
- Fabozzi, F. - *Fixed Income Mathematics*, ch. 1-3

---
## Revision Log
| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | Hull |
| 2026-04-18 | Renamed "Implementation (Python)" → "Implementation" for section consistency | review |
