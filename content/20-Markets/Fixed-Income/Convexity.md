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
> **Chain:** Hedging → Gap 2: Delta hedging neutralizes direction but leaves other exposures (fixed-income analog — second-order)
> **This concept:** Provides the second-order (curvature) correction to duration's linear approximation — the bond analog of gamma — capturing the asymmetric benefit that bonds gain more when rates fall than they lose when rates rise by the same amount.
> **Alternative approaches to this gap:** Key rate convexity (non-parallel), numerical convexity via finite-difference repricing
> **You need first:** [[Bond Basics]], [[Duration]]
> **This unlocks:** More accurate bond hedging for large rate moves, negative convexity modeling for callable bonds and MBS

> Second-order yield sensitivity; positive for bonds (long gamma analog)

## Why This Exists

**The gap:** Duration's linear approximation becomes increasingly wrong for large yield moves. A trader hedging a bond portfolio with duration alone will find the hedge bleeds P&L as rates move significantly — the portfolio is "gamma unhedged."
**What came before:** Duration was the standard risk measure. Practitioners using duration-matched hedges observed residual P&L that grew with the square of the yield move — unexplained by their duration models.
**What this adds:** Convexity is the second derivative of price with respect to yield, divided by price. It captures the curvature of the price-yield relationship — the fact that the bond price function is not a straight line but a bow. Adding the convexity term $\frac{1}{2} C (\Delta y)^2$ to the duration estimate restores accuracy for moves of 50–200bp, which is the typical range of interest rate shocks in practice.
**What it still doesn't solve:** Even duration + convexity is a second-order Taylor approximation. For extreme moves (>300bp) or for bonds with embedded options (callables, MBS), which exhibit negative convexity, higher-order terms and option-adjusted frameworks are required.

## Math Concepts

### Price-Yield Relationship

Bond price $P$ is a nonlinear, decreasing, convex function of yield $y$. The Taylor expansion of $P(y)$ around a current yield $y_0$:

$$\Delta P \approx \frac{dP}{dy}\Delta y + \frac{1}{2}\frac{d^2P}{dy^2}(\Delta y)^2$$

Dividing by $P$:

$$\frac{\Delta P}{P} \approx -D_{mod} \cdot \Delta y + \frac{1}{2} \cdot C \cdot (\Delta y)^2$$

Where:
- $D_{mod}$ = modified duration (captures the first-order / slope effect)
- $C$ = convexity (captures the second-order / curvature effect)
- The negative sign on duration: prices fall when yields rise
- The positive sign on convexity: always adds to price return regardless of direction of move

### Convexity Formula

$$C = \frac{1}{P} \cdot \frac{d^2P}{dy^2} = \frac{\sum_{t=1}^{T} \frac{CF_t \cdot t(t+1)}{(1+y)^{t+2}}}{P}$$

For annual coupons with $n$ periods per year, the full formula adjusts the time weighting:

$$C = \frac{1}{P \cdot (1+y/n)^2} \sum_{t=1}^{T} \frac{CF_t \cdot t \cdot (t+1)/n^2}{(1+y/n)^t}$$

Convexity has units of **years squared**.

### Dollar Convexity

Similar to Dollar Duration, Dollar Convexity = $C \times P$. The full second-order P&L approximation in dollar terms:

$$\Delta P \approx -D_{mod} \cdot P \cdot \Delta y + \frac{1}{2} \cdot C \cdot P \cdot (\Delta y)^2$$

### Positive vs. Negative Convexity

- **Standard bonds**: positive convexity. The price-yield curve bows outward.
- **Callable bonds**: the issuer can call (redeem early) when rates fall, capping price appreciation. This creates **negative convexity** in the region where yields are low — the curve flattens or even bends inward.
- **Mortgage-backed securities (MBS)**: homeowners prepay when rates fall (refinancing), creating negative convexity similar to callable bonds.

## Walkthrough

Use our 5-year, 6% coupon, \$1,000 face bond priced at par (yield = 6%).

From the [[Duration]] note: $D_{mod} = 4.212$.

Computing convexity (annual periods):

| t | CF_t | $\frac{CF_t \cdot t(t+1)}{(1.06)^{t+2}}$ |
|---|------|------------------------------------------|
| 1 | 60 | 60 × 2 / 1.06³ = 100.75 |
| 2 | 60 | 60 × 6 / 1.06⁴ = 285.17 |
| 3 | 60 | 60 × 12 / 1.06⁵ = 538.01 |
| 4 | 60 | 60 × 20 / 1.06⁶ = 846.04 |
| 5 | 1060 | 1060 × 30 / 1.06⁷ = 21,150.02 |
| **Sum** | | **22,920.00** |

$C = 22,920.00 / 1000 = **22.92** \text{ years}^2$

Now compare approximations for a **+200bp** yield shock ($\Delta y = 0.02$):

**Duration only:**
$$\frac{\Delta P}{P} \approx -4.212 \times 0.02 = -8.42\%$$

**Duration + Convexity:**
$$\frac{\Delta P}{P} \approx -4.212 \times 0.02 + 0.5 \times 22.92 \times (0.02)^2 = -8.42\% + 0.46\% = -7.96\%$$

**Actual price** at 8% yield: $P = \$920.15$, which is $-7.99\%$. The duration + convexity estimate is much closer than duration alone.

For a symmetric **-200bp** shock ($\Delta y = -0.02$):

**Duration only:** $+8.42\%$

**Duration + Convexity:** $+8.42\% + 0.46\% = +8.88\%$

**Actual:** $+8.91\%$. The convexity term correctly shows that price gains more than it loses — the asymmetric benefit of positive convexity.

## Analysis

**Key properties:**
- Convexity is always positive for plain (option-free) bonds
- Zero-coupon bonds have the highest convexity relative to their duration (all cash flow at one point in time creates a highly curved price-yield relationship)
- Lower coupon bonds have higher convexity than higher coupon bonds (for same maturity/duration)
- Convexity increases as yield decreases (the curve gets steeper at low yields)

**The convexity premium:** Investors pay for convexity. Two bonds with the same duration but different convexity are not equivalent — the higher-convexity bond will outperform in large rate moves. The price for this protection is a lower yield.

**Negative convexity pathology:**
- Callable bonds: issuer's call option is a short call on the bond → buyer is effectively short that option → negative convexity
- MBS prepayment option has the same effect
- For these instruments, the simple formula breaks down: must model the embedded option explicitly

**Relationship to options:**
| Bond world | Options world |
|---|---|
| Duration | Delta |
| Convexity | Gamma |
| DV01 | Delta dollar |
| Positive convexity | Long gamma |
| Negative convexity | Short gamma |

**Failure modes:**
- Convexity correction is still approximate — for extreme moves (>300bp), even second-order Taylor fails
- Cross-convexity (how convexity changes with yield) requires third-order terms
- Negative convexity models need option-adjusted spread (OAS) framework

## Implementation

```python
import numpy as np

def bond_convexity(face, coupon_rate, ytm, n_years, freq=1):
    """
    Compute convexity and full price-change approximation.
    
    Parameters
    ----------
    face        : float - face/par value
    coupon_rate : float - annual coupon rate
    ytm         : float - yield to maturity (annual)
    n_years     : int   - years to maturity
    freq        : int   - coupon payments per year
    
    Returns
    -------
    convexity : float - convexity (years^2)
    price     : float - bond price
    """
    coupon = face * coupon_rate / freq
    y = ytm / freq                          # yield per period
    n = n_years * freq                      # total periods

    t = np.arange(1, n + 1)
    cash_flows = np.full(n, coupon)
    cash_flows[-1] += face

    # Present value of each cash flow
    pv_cf = cash_flows / (1 + y) ** t
    price = pv_cf.sum()

    # Convexity: second derivative of price w.r.t. yield, scaled by 1/P
    # Formula: sum[ CF_t * t*(t+1) / (1+y)^(t+2) ] / P
    convexity = (cash_flows * t * (t + 1) / (1 + y) ** (t + 2)).sum() / price

    # Adjust for frequency (convexity in years^2)
    convexity = convexity / freq**2

    return convexity, price


def price_change_approx(price, mod_dur, convexity, dy):
    """
    Approximate price change using duration + convexity.
    
    Returns both the duration-only and full approximations.
    """
    pct_dur_only = -mod_dur * dy
    pct_full = -mod_dur * dy + 0.5 * convexity * dy**2
    
    dp_dur_only = price * pct_dur_only
    dp_full     = price * pct_full
    
    return dp_dur_only, dp_full, pct_dur_only * 100, pct_full * 100


# Example: 5-year 6% coupon bond at 6% yield
conv, price = bond_convexity(1000, 0.06, 0.06, 5)
mac_dur = 4.4650   # from Duration note
mod_dur = mac_dur / 1.06

print(f"Bond price:  ${price:.2f}")
print(f"Convexity:   {conv:.4f} years^2")
print(f"Mod Duration:{mod_dur:.4f}")

print("\n--- Price change approximations ---")
for dy_bps in [50, 100, 200]:
    dy = dy_bps / 10000
    dp_d, dp_dc, pct_d, pct_dc = price_change_approx(price, mod_dur, conv, dy)
    print(f"\n+{dy_bps}bp shock:")
    print(f"  Duration only:           ${dp_d:.2f}  ({pct_d:.3f}%)")
    print(f"  Duration + Convexity:    ${dp_dc:.2f}  ({pct_dc:.3f}%)")


# --- Visualize the price-yield curve and approximations ---
import matplotlib.pyplot as plt

def exact_bond_price(face, coupon_rate, ytm, n_years, freq=1):
    coupon = face * coupon_rate / freq
    y = ytm / freq
    n = n_years * freq
    t = np.arange(1, n + 1)
    cf = np.full(n, coupon)
    cf[-1] += face
    return (cf / (1 + y) ** t).sum()

ytm_range = np.linspace(0.01, 0.15, 200)
prices_exact = [exact_bond_price(1000, 0.06, y, 5) for y in ytm_range]

y0 = 0.06
p0 = exact_bond_price(1000, 0.06, y0, 5)
dy_range = ytm_range - y0
prices_dur_only = p0 * (1 - mod_dur * dy_range)
prices_dur_conv = p0 * (1 - mod_dur * dy_range + 0.5 * conv * dy_range**2)

plt.figure(figsize=(9, 5))
plt.plot(ytm_range * 100, prices_exact, 'b-', lw=2, label='Exact price')
plt.plot(ytm_range * 100, prices_dur_only, 'r--', lw=1.5, label='Duration approx (tangent line)')
plt.plot(ytm_range * 100, prices_dur_conv, 'g-.', lw=1.5, label='Duration + Convexity (parabola)')
plt.axvline(6, color='gray', linestyle=':', alpha=0.7)
plt.xlabel('Yield (%)')
plt.ylabel('Bond Price ($)')
plt.title('Price-Yield Curve: Convexity Makes Bonds Benefit from Large Moves')
plt.legend()
plt.tight_layout()
plt.savefig('convexity_curve.png', dpi=150)
plt.show()
```

## Bridge to Quant / ML

**Rates trading — gamma trading:** A bond portfolio manager running a long-duration book is inherently long convexity. In volatile rate environments, this convexity "earns" additional return beyond what duration alone captures. Traders actively buy or sell convexity depending on their volatility view.

**Options analogy for quants:** The duration/convexity framework maps exactly onto delta/gamma hedging in options. A delta-hedged options position profits from realized volatility (gamma P&L). Similarly, a duration-hedged bond position with positive convexity profits from large rate moves.

**MBS and negative convexity:** Mortgage-backed securities are the most important example of negative convexity. When rates fall, homeowners refinance, returning principal to investors at the worst time. Modeling this requires Monte Carlo simulation of prepayment behavior — a core fixed-income quant problem.

**Convexity in yield curve risk models:** The second principal component of the yield curve (the "slope" factor) generates convexity exposure for barbell vs. bullet portfolios. A barbell (long 2yr + long 30yr) has higher convexity than a bullet (long 10yr) with the same duration.

**ML note:** ML models predicting yield moves that produce large $\Delta y$ will have large prediction-error if their P&L calculation uses only duration. Incorporating convexity into the reward function of [[Reinforcement Learning Trading]] or into [[Feature Engineering Finance]] pipelines is essential for accurate P&L attribution.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why is positive convexity described as an "asymmetric benefit" for bond investors? How does it manifest in price changes for equal up and down yield moves?
<details><summary>Answer</summary>Positive convexity means the price-yield curve bows away from the tangent line (duration approximation). For a downward yield move of $\Delta y$, the bond gains more than the duration estimate predicts (price rises faster than linearly). For an upward move of the same magnitude, the bond loses less than duration predicts (price falls slower than linearly). Both effects are positive — the convexity term $\frac{1}{2} C (\Delta y)^2$ is always positive regardless of the sign of $\Delta y$. An investor long a convex bond benefits from large rate moves in either direction, not just in one direction.</details>

**Q2.** What is negative convexity, and why does it arise in callable bonds and mortgage-backed securities?
<details><summary>Answer</summary>Negative convexity means the price-yield curve bends inward — prices rise less when rates fall, and fall more when rates rise, relative to a bond with positive convexity. In callable bonds, the issuer holds an option to redeem the bond when rates fall (refinancing at a lower rate). This caps the price appreciation — when rates drop, the bond is called back at par, preventing the investor from capturing the full price gain. The investor is effectively short a call option on the bond, creating negative convexity in the low-yield region. MBS exhibit the same effect because homeowners prepay their mortgages when rates fall, returning principal to investors at the worst time.</details>

**Q3.** Two bonds have equal duration. Bond A has convexity 15; Bond B has convexity 35. An investor believes rates will be volatile but has no directional view. Which bond should the investor prefer, and why?
<details><summary>Answer</summary>The investor should prefer Bond B (higher convexity) if rates are expected to be volatile. With equal duration, both bonds have the same expected P&L from small moves. But for large moves, Bond B outperforms in both directions due to its higher curvature. Volatility creates asymmetric gains for the higher-convexity bond. The catch: investors pay for convexity — Bond B will likely have a slightly lower yield (yield giveup). This is the convexity premium: you accept lower carry to own the better payoff profile in volatile rate environments.</details>

---

### Level 2 — Quantitative

**Q4.** A bond has modified duration 6.0 and convexity 48. Rates rise by 150bp. Compute (a) the duration-only price change and (b) the duration + convexity price change as a percentage.
<details><summary>Answer</summary>(a) Duration only: $\Delta P/P \approx -6.0 \times 0.015 = -9.00\%$. (b) Duration + convexity: $\Delta P/P \approx -9.00\% + 0.5 \times 48 \times (0.015)^2 = -9.00\% + 0.5 \times 48 \times 0.000225 = -9.00\% + 0.54\% = -8.46\%$. The convexity correction adds 54bp, reducing the estimated price decline. For a \$1,000 bond: duration-only estimates a \$90 loss; convexity-adjusted estimates \$84.60 — a \$5.40 difference that comes from the curvature of the price-yield relationship.</details>

**Q5.** From the walkthrough: for the 5-year 6% bond (duration 4.212, convexity 22.92), compare the duration-only and duration+convexity estimates versus the exact price for a −200bp rate shock (yield falls from 6% to 4%).
<details><summary>Answer</summary>$\Delta y = -0.02$ (200bp decline). Duration only: $\Delta P/P \approx -4.212 \times (-0.02) = +8.424\%$. Duration + convexity: $+8.424\% + 0.5 \times 22.92 \times (0.02)^2 = +8.424\% + 0.459\% = +8.883\%$. Exact: at 4% yield, price $= \$1,089.04$ from $\$1,000$, so $+8.904\%$. The convexity-adjusted estimate ($+8.883\%$) is much closer to the exact value ($+8.904\%$) than the duration-only estimate ($+8.424\%$), with a residual error of only 0.021% vs 0.48%.</details>

---

### Level 3 — Coding

**Q6.** In the `bond_convexity` function, the raw convexity sum is divided by `freq**2` to convert to years-squared. Explain why this frequency adjustment is necessary.
<details><summary>Answer</summary>The convexity formula sums $CF_t \cdot t \cdot (t+1) / (1+y)^{t+2}$ where $t$ is in *periods*. The resulting convexity is in units of *periods-squared*. To convert to years-squared (the standard unit for convexity), you divide by $freq^2$: each period is $1/freq$ years, so $t_{periods}^2 = (t_{years} \times freq)^2$, meaning $C_{periods} = C_{years} \times freq^2$, so $C_{years} = C_{periods} / freq^2$. For a semi-annual bond ($freq=2$), the raw sum overstates the convexity by a factor of 4 — so dividing by 4 converts to the correct annualized convexity in years-squared.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Convexity is always positive | Callable bonds and MBS have negative convexity in certain yield regions. The standard formula applies only to option-free bonds. |
| If I match duration and convexity, my hedge is perfect | Duration + convexity is still a second-order approximation. Extremely large moves require higher-order terms. Also, neither duration nor convexity captures non-parallel yield curve shifts. |
| Higher convexity always means a better bond | Higher convexity is better for a given duration, all else equal. But investors pay for convexity via lower yield. Whether it's "better" depends on your realized rate volatility vs. the implied convexity premium. |
| The convexity correction is always small | For 50bp moves it is typically small. For 200bp moves (common in crisis periods), the convexity correction can exceed 40–50bp of return, which is economically significant. |

## Related Concepts

- [[Duration]] — the first-order approximation that convexity corrects
- [[Yield Curve]] — curve moves are non-parallel; convexity is relevant to curvature trades
- [[Options]] — gamma is the options analog of convexity
- [[MBS]] — negative convexity is the defining risk of mortgage securities

## Sources Used

- Hull, J. - *Options, Futures, and Other Derivatives*, ch. 4
- Fabozzi, F. - *Fixed Income Mathematics*, ch. 4 (Convexity and Price-Yield Relationship)
- Tuckman, B. - *Fixed Income Securities* ch. 5

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | Fixed walkthrough table: corrected t=5 row and sum (22,920, C=22.92); updated ±200bp approximations | QA review |
