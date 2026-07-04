---
type: concept
domain: 20-Markets
tags: [fixed-income, risk, interest-rates]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-12
review_interval_days: 365
sources:
  - "Hull - Options, Futures, and Other Derivatives ch.4"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Hedging → Gap 2: Delta hedging neutralizes direction but leaves other exposures (fixed-income analog)
> **This concept:** Provides the first-order sensitivity of bond price to yield changes — the fixed-income equivalent of delta — enabling systematic hedging of interest rate risk via DV01 matching.
> **Alternative approaches to this gap:** Key rate durations (non-parallel shift sensitivity), spread duration (credit spread sensitivity)
> **You need first:** [[Bond Basics]], [[Yield Curve]]
> **This unlocks:** [[Convexity]] (second-order correction), [[Interest Rate Swaps]] (DV01 of swap fixed leg), [[Immunization]]

> Price sensitivity to yield changes; weighted avg time to cash flows

## Why This Exists

**The gap:** Once bond pricing was standardized (see [[Bond Basics]]), practitioners needed a single number to answer: "If interest rates move, how much does my bond position lose?" Without such a measure, managing a portfolio of bonds with different maturities, coupons, and sizes was guesswork.
**What came before:** Traders would manually reprice each bond for a given yield shock, which was slow, not scalable, and gave no intuition for how portfolio composition affected interest rate risk.
**What this adds:** Duration collapses the entire cash flow structure of any bond into one number: $D_{mod}$ tells you the percentage price change for a 1% (100bp) yield move. DV01 translates this to the dollar P&L per basis point — a universal trading unit. Because duration is additive by market value weight, portfolio duration aggregates cleanly, enabling systematic delta-hedging of a bond book with a small number of hedging instruments.
**What it still doesn't solve:** Duration is a linear (first-order) approximation valid only for small yield moves. It also assumes the entire yield curve shifts in parallel — if the 2-year moves but the 10-year doesn't, duration mismeasures the actual exposure. [[Convexity]] fixes the first problem; key rate durations fix the second.

## Math Concepts

### Bond Price

A bond paying coupon $C$ annually, face value $F$, yield-to-maturity $y$, maturing in $T$ years:

$$P = \sum_{t=1}^{T} \frac{C}{(1+y)^t} + \frac{F}{(1+y)^T}$$

### Macaulay Duration

Macaulay duration is the **present-value-weighted average time** to each cash flow:

$$D_{Mac} = \frac{\sum_{t=1}^{T} t \cdot \frac{CF_t}{(1+y)^t}}{P}$$

Where:
- $CF_t$ = cash flow at time $t$ (coupon or coupon + face)
- $P$ = current bond price (the denominator normalizes the weights)
- Each weight $w_t = \frac{CF_t/(1+y)^t}{P}$ is the fraction of total value from time $t$

Macaulay duration has units of **years**.

### Modified Duration

Modified duration converts Macaulay duration into a direct price-sensitivity measure:

$$D_{mod} = \frac{D_{Mac}}{1 + y/n}$$

Where $n$ = number of coupon periods per year (1 for annual, 2 for semi-annual).

**Price change approximation** (first-order / linear):

$$\frac{\Delta P}{P} \approx -D_{mod} \cdot \Delta y$$

Or equivalently: $\Delta P \approx -D_{mod} \cdot P \cdot \Delta y$

The negative sign: when yields rise ($\Delta y > 0$), price falls.

### Dollar Duration and DV01

**Dollar Duration**: the dollar price change for a 1-unit change in yield.

$$\text{Dollar Duration} = D_{mod} \cdot P$$

**DV01** (Dollar Value of 1 basis point): price change per **1bp** (0.0001) move in yield.

$$\text{DV01} = D_{mod} \cdot P \cdot 0.0001$$

DV01 is the most common trading unit in bond markets. A bond with DV01 of \$500 means: for every 1bp rise in rates, you lose \$500.

### Portfolio Duration

For a portfolio of bonds with weights $w_i$ (by market value):

$$D_{portfolio} = \sum_i w_i \cdot D_{mod,i}$$

Duration is **additive by market-value weight** — this is what makes it so useful for hedging.

## Walkthrough

Consider a 5-year bond, face value \$1,000, annual coupon rate 6%, yield = 6% (priced at par).

Cash flows: \$60 at years 1-4, \$1,060 at year 5.

| Year | CF | PV of CF | Weight | Year × Weight |
|------|----|----------|--------|---------------|
| 1 | 60 | 56.60 | 0.0566 | 0.0566 |
| 2 | 60 | 53.40 | 0.0534 | 0.1068 |
| 3 | 60 | 50.38 | 0.0504 | 0.1511 |
| 4 | 60 | 47.52 | 0.0475 | 0.1900 |
| 5 | 1060 | 792.09 | 0.7921 | 3.9605 |
| **Total** | | **1000.00** | **1.0000** | **4.4650** |

So **Macaulay Duration = 4.465 years**.

**Modified Duration** = 4.465 / (1 + 0.06) = **4.212**

If yields rise from 6% to 7% ($\Delta y = +0.01$):
$$\Delta P \approx -4.212 \times 1000 \times 0.01 = -\$42.12$$

New price ≈ \$957.88. (Actual price using full formula: \$958.42 — duration slightly overstates the drop, which is where [[Convexity]] corrects.)

**DV01** = 4.212 × 1000 × 0.0001 = **\$0.4212 per basis point**

## Analysis

**Key properties:**
- Zero-coupon bond: Macaulay duration = maturity (all value arrives at one time)
- Higher coupon → lower duration (more weight on near-term coupons)
- Higher yield → lower duration (discounting makes far cash flows worth less relatively)
- Duration increases with maturity, but at a decreasing rate for coupon bonds

**Limitations:**
- Duration is a **linear approximation** — only accurate for small yield changes. For large moves, [[Convexity]] correction is needed.
- Assumes a **parallel shift** of the yield curve. In reality, short and long rates can move independently (see [[Yield Curve]]).
- Does not capture **credit spread** changes — only interest rate risk.
- Modified duration assumes continuous yield — for semi-annual bonds, use the correct $n$.

**Failure modes:**
- Negative convexity bonds (callable bonds, MBS): duration can decrease when rates fall, breaking the hedging intuition.
- Extreme rate environments: 100bp move is not "small" — convexity correction becomes essential.

## Implementation

```python
import numpy as np

def macaulay_duration(face, coupon_rate, ytm, n_years, freq=1):
    """
    Compute Macaulay and Modified duration for a coupon bond.
    
    Parameters
    ----------
    face        : float  - face/par value (e.g. 1000)
    coupon_rate : float  - annual coupon rate (e.g. 0.06 for 6%)
    ytm         : float  - yield to maturity per year (e.g. 0.06)
    n_years     : int    - years to maturity
    freq        : int    - coupon frequency per year (1=annual, 2=semi-annual)
    
    Returns
    -------
    mac_dur : float  - Macaulay duration in years
    mod_dur : float  - Modified duration
    dv01    : float  - Dollar value of 1 basis point
    price   : float  - Bond price
    """
    coupon = face * coupon_rate / freq      # coupon per period
    y_per_period = ytm / freq               # yield per period
    n_periods = n_years * freq              # total periods

    times = np.arange(1, n_periods + 1)     # period numbers: 1, 2, ..., n
    cash_flows = np.full(n_periods, coupon)
    cash_flows[-1] += face                  # add face value at final period

    # Discount each cash flow
    discount_factors = (1 + y_per_period) ** times
    pv_cash_flows = cash_flows / discount_factors

    price = pv_cash_flows.sum()

    # Macaulay duration: weighted avg of TIME (in years)
    weights = pv_cash_flows / price
    time_in_years = times / freq            # convert periods to years
    mac_dur = (weights * time_in_years).sum()

    # Modified duration
    mod_dur = mac_dur / (1 + y_per_period)

    # DV01: price change per 1 basis point (0.0001) yield change
    dv01 = mod_dur * price * 0.0001

    return mac_dur, mod_dur, dv01, price


# Example: 5-year bond, 6% coupon, 6% yield, $1000 face
mac, mod, dv01, price = macaulay_duration(
    face=1000, coupon_rate=0.06, ytm=0.06, n_years=5
)
print(f"Price:             ${price:.2f}")
print(f"Macaulay Duration: {mac:.4f} years")
print(f"Modified Duration: {mod:.4f}")
print(f"DV01:              ${dv01:.4f} per bp")

# Approximate price change for +50bp yield move
dy = 0.005
dp_approx = -mod * price * dy
print(f"\nApprox price change for +50bp: ${dp_approx:.2f}")


# --- Portfolio Duration ---
def portfolio_duration(market_values, durations):
    """
    Compute market-value-weighted portfolio duration.
    
    Parameters
    ----------
    market_values : list of float - market value of each bond position
    durations     : list of float - modified duration of each bond
    """
    mv = np.array(market_values)
    d  = np.array(durations)
    weights = mv / mv.sum()
    return (weights * d).sum()


# Example: two-bond portfolio
mvs = [500_000, 300_000]       # market values
mods = [4.21, 8.50]            # modified durations
port_dur = portfolio_duration(mvs, mods)
print(f"\nPortfolio Modified Duration: {port_dur:.3f}")
print(f"Portfolio DV01: ${port_dur * sum(mvs) * 0.0001:,.0f} per bp")
```

## Bridge to Quant / ML

**Rates trading:** Duration is the primary tool for expressing interest rate views. A rates trader who thinks yields will fall buys duration (long bonds). A trader who thinks yields will rise sells duration (short bonds) or receives-fixed in a swap.

**Immunization:** Pension funds and insurance companies match asset duration to liability duration so that rising rates hurt asset values and liability PVs equally — the portfolio is "immune" to rate moves. This is the classic ALM (Asset-Liability Management) problem.

**DV01 hedging:** To hedge a \$1M bond position with DV01 of \$500/bp, you would short Treasury futures with the same DV01. The futures position exactly offsets the rate sensitivity.

**Factor model connection:** In fixed-income factor models (e.g., PCA on yield curves), duration loads heavily on the first factor (the level factor). The second factor (slope) maps to duration differences between short and long positions — a barbell vs. bullet trade.

**ML angle:** Duration and DV01 are used as **risk constraints** in fixed-income ML models. A factor model predicting yield curve moves would combine its output with DV01 to compute expected P&L per position.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why does a zero-coupon bond have Macaulay duration equal to its maturity, while a coupon bond has duration less than its maturity?
<details><summary>Answer</summary>Macaulay duration is the present-value-weighted average time to receive cash flows. For a zero-coupon bond, 100% of the value is received at maturity — there is only one cash flow, so the weighted average time is trivially equal to the maturity. For a coupon bond, some cash flows arrive earlier (the coupon payments), pulling the weighted average time earlier than the final maturity date. The higher the coupon relative to the face value, the more weight the early cash flows carry, and the shorter the duration relative to maturity.</details>

**Q2.** Two bonds have the same modified duration. Does this mean they have the same price sensitivity to all yield changes? What situation would reveal a difference between them?
<details><summary>Answer</summary>Same modified duration means same *first-order* price sensitivity to small, parallel yield shifts. A difference emerges for large yield moves (where convexity matters) or for non-parallel yield curve shifts (where key rate durations matter). If one bond has higher convexity, it will outperform for large moves in either direction. If the two bonds have different concentrations of cash flows at different maturities, a twist in the yield curve (e.g., short rates rising while long rates fall) will affect them differently despite equal total duration.</details>

**Q3.** What does it mean to "immunize" a bond portfolio against interest rate risk, and why is matching duration to liabilities sufficient (approximately)?
<details><summary>Answer</summary>Immunization means structuring a portfolio so that a change in interest rates causes the portfolio's asset value and liability present value to change by the same amount — leaving the net funded status unchanged. If the asset portfolio duration equals the liability duration, then a parallel yield shift causes equal percentage changes in both assets and liabilities. Since both are scaled by the same DV01, the P&L of the hedge exactly offsets the P&L of the liability. "Approximately" because duration is a linear approximation — large moves require convexity matching as well to maintain the hedge through non-linear price moves.</details>

---

### Level 2 — Quantitative

**Q4.** A bond has modified duration 7.2 and price \$950. You hold 100 bonds. What is the portfolio DV01, and what is the approximate price change if yields rise by 50bp?
<details><summary>Answer</summary>Single bond DV01 $= 7.2 \times 950 \times 0.0001 = \$0.684$ per bp. Portfolio DV01 $= 100 \times 0.684 = \$68.40$ per bp. For a 50bp rise: $\Delta P \approx -50 \times 68.40 = -\$3,420$ total portfolio loss. Equivalently: $\Delta P / P \approx -7.2 \times 0.005 = -3.60\%$, so each bond loses $\approx -\$34.20$ and the portfolio loses $\approx \$3,420$.</details>

**Q5.** From the walkthrough: a 5-year, 6% coupon, \$1,000 face bond at 6% yield has \$D_{Mac} = 4.465$ years. Verify the Modified Duration and DV01, then compute the approximate price if yields rise to 6.5%.
<details><summary>Answer</summary>$D_{mod} = 4.465 / (1 + 0.06/1) = 4.465 / 1.06 = 4.212$. DV01 $= 4.212 \times 1000 \times 0.0001 = \$0.4212$ per bp. For $\Delta y = +50$bp: $\Delta P \approx -4.212 \times 1000 \times 0.005 = -\$21.06$. New approximate price $\approx \$978.94$. (The exact price at 6.5% is $\approx \$979.01$; the duration approximation overstates the loss by about \$0.07 due to positive convexity.)</details>

---

### Level 3 — Coding

**Q6.** The `macaulay_duration` function computes both Macaulay and Modified duration. Why is the `time_in_years = times / freq` conversion necessary, and what would go wrong if you used period numbers instead?
<details><summary>Answer</summary>Macaulay duration has units of *years* — it answers "how many years, on average, do you wait for your cash flows?" The `times` array contains period numbers (1, 2, ..., n_periods), not years. If you compute the weighted average of period numbers, you get Macaulay duration in *periods*, not years. For a semi-annual bond ($freq=2$), this would give a number twice as large as the correct duration. Dividing by `freq` converts periods to years: period $k$ corresponds to year $k/freq$. The Modified Duration then correctly measures percent price change per unit change in the annual yield.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Duration equals the maturity of the bond | Only for zero-coupon bonds. Coupon bonds have duration strictly less than maturity because early coupon cash flows reduce the weighted average time. |
| Duration gives an exact price change | Duration is a linear (first-order) approximation. For small moves (<25bp) it is quite accurate; for large moves (>100bp) convexity correction is essential. |
| A bond portfolio with zero duration has no interest rate risk | Zero total duration means no net parallel-shift risk. But the portfolio can still be exposed to curve twists, slope changes, or credit spread moves — all invisible to total duration. |
| DV01 is the same as duration | DV01 = $D_{mod} \times P \times 0.0001$ — it scales duration by price and converts to a dollar-per-basis-point measure. Different bonds can have the same DV01 with very different durations if their prices differ. |

## Related Concepts

- [[Convexity]] — second-order correction to the duration approximation
- [[Yield Curve]] — duration assumes a parallel shift; real moves are rarely parallel
- [[DV01]] — the trading unit; dollar price change per basis point
- [[Immunization]] — matching asset/liability durations for ALM

## Sources Used

- Hull, J. - *Options, Futures, and Other Derivatives*, ch. 4 (Bond Pricing and Duration)
- Fabozzi, F. - *Fixed Income Mathematics* ch. 2-3

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
