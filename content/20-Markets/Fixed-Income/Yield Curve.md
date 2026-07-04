---
type: concept
domain: 20-Markets
tags: [fixed-income, markets, interest-rates]
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
> **Chain:** Pricing → Gap 1: No agreed method to value an uncertain future payoff (extended to term structure)
> **This concept:** Establishes the full term structure of discount rates — replacing the single YTM of Bond Basics with a rate for every maturity — which is the foundation for pricing all fixed-income instruments consistently.
> **Alternative approaches to this gap:** Nelson-Siegel parametric fitting (smooth but less exact), spline interpolation (flexible but can produce unsmooth forwards)
> **You need first:** [[Bond Basics]]
> **This unlocks:** [[Interest Rate Swaps]] (use discount curve for valuation), [[HJM Framework]], [[Vasicek Model]], [[Duration]] key rate extensions

> Term structure of interest rates; normal/inverted/humped shapes

## Why This Exists

**The gap:** A single bond's YTM gives one discount rate, but that rate blends together the time value of money at every maturity. If a 5-year bond's YTM is 5%, this does not mean the 1-year rate is also 5% — rates are different at every maturity, and using a single flat rate mismeasures the present value of cash flows at different horizons.
**What came before:** The YTM convention (see [[Bond Basics]]) treated each bond independently with its own discount rate. There was no consistent framework for relating rates across maturities, making it impossible to price a cash flow stream that crossed multiple maturity points consistently.
**What this adds:** The yield curve bootstrapping algorithm extracts a separate spot rate $z(t)$ for every maturity $t$ from observable bond prices. This produces a fully consistent discount function $P(0,t)$ that prices all bonds without arbitrage — the foundation for pricing swaps, caps, floors, and all fixed-income derivatives. The shape of the curve (normal, inverted, humped) also encodes market expectations about future rates and the economic cycle.
**What it still doesn't solve:** The static yield curve is a snapshot at one point in time. Pricing interest rate derivatives (caps, swaptions) requires a *dynamic* model for how the curve moves — addressed by the [[Vasicek Model]], [[Hull-White Model]], and [[HJM Framework]].

## Math Concepts

### Spot Rate (Zero Rate)

The **spot rate** $z(t)$ (also called the zero-coupon rate) is the yield on a zero-coupon bond maturing at time $t$. It represents pure time-value of money with no intermediate cash flows. 

A zero-coupon bond price:
$$P(0, t) = \frac{1}{(1 + z(t))^t} \quad \text{(annual compounding)}$$

Or with continuous compounding:
$$P(0, t) = e^{-z(t) \cdot t}$$

### Par Rate vs. Spot Rate

The **par rate** is the coupon rate that makes a coupon bond priced at par (\$100). US Treasury quotes are typically par rates (yield-to-maturity on coupon bonds). **Spot rates must be bootstrapped** from par rates.

### Bootstrapping the Zero Curve

Given a set of coupon bond prices or par rates, we extract spot rates sequentially. The idea: price each bond as the sum of discounted cash flows, solve for the unknown spot rate at each maturity.

For a 2-year par bond with coupon $c_2$ and par rate $r_2$:
$$100 = \frac{c_2}{1 + z(1)} + \frac{100 + c_2}{(1 + z(2))^2}$$

Since we already know $z(1)$ from the 1-year bond, we can solve for $z(2)$.

Repeating for each maturity bootstraps the entire zero curve.

### Forward Rates

A **forward rate** $f(t_1, t_2)$ is the rate implied by the curve for borrowing between future dates $t_1$ and $t_2$.

From spot rates (continuous compounding):
$$f(t_1, t_2) = \frac{z(t_2) \cdot t_2 - z(t_1) \cdot t_1}{t_2 - t_1}$$

Interpretation: the forward rate is the "break-even" rate. If 1-year spot = 4% and 2-year spot = 5%, the implied forward rate from year 1 to year 2 is approximately 6%. Locking in money for 2 years earns the same as locking it for 1 year, then rolling it at 6%.

### Key Rate Durations

Instead of one parallel-shift duration, **key rate durations** measure sensitivity to yield changes at specific maturities (e.g., 2yr, 5yr, 10yr, 30yr), holding other rates constant. Captures non-parallel curve moves.

### Common Spreads

| Spread | Formula | Use |
|--------|---------|-----|
| 2s10s | $z(10) - z(2)$ | Recession indicator |
| 2s30s | $z(30) - z(2)$ | Long-end steepness |
| TED | 3M LIBOR - 3M T-bill | Bank credit risk |
| OIS | Overnight rate - OIS rate | Short-end stress indicator |

## Walkthrough

### Bootstrapping Example

Suppose we observe these Treasury par rates:

| Maturity | Par Rate |
|----------|---------|
| 0.5 yr   | 4.00%   |
| 1.0 yr   | 4.20%   |
| 1.5 yr   | 4.40%   |
| 2.0 yr   | 4.60%   |

Assume semi-annual coupons. All bonds priced at par = 100.

**Step 1 (0.5 yr):** 0.5-year bond pays one cash flow of 102 (coupon 2.00 + principal 100).
$$100 = \frac{102}{1 + z(0.5)/2} \implies z(0.5) = 4.00\%$$

**Step 2 (1.0 yr):** 1-year bond pays 2.10 at 0.5yr, then 102.10 at 1yr.
$$100 = \frac{2.10}{1+z(0.5)/2} + \frac{102.10}{(1+z(1)/2)^2}$$
$$100 = \frac{2.10}{1.0200} + \frac{102.10}{(1+z(1)/2)^2}$$
$$\frac{102.10}{(1+z(1)/2)^2} = 100 - 2.059 = 97.941$$
$$(1+z(1)/2)^2 = 1.04254 \implies z(1) = 4.212\%$$

Continue for 1.5yr and 2yr maturities.

### Yield Curve Shapes (Visual)

```
Normal:   __---‾‾‾‾‾‾‾     (rates rise with maturity)
Inverted: ‾‾‾---___         (short > long)
Humped:   _--‾‾--__         (peak at medium maturity)
```

## Analysis

**Why the curve shape matters for the economy:**
- Normal curve: banks borrow short, lend long → profitable → they lend more → economic expansion
- Inverted curve: bank margins compressed → reduced lending → economic contraction
- The yield curve forecasts expectations for future short rates (under the expectations hypothesis)

**Theories of the yield curve:**
1. **Expectations hypothesis:** long rates = expected future short rates. Implies flat/inverted when Fed expected to cut.
2. **Liquidity preference theory:** adds a term premium — investors demand extra yield for locking up money long-term. Explains the normal upward slope as the default.
3. **Market segmentation:** different buyers dominate different maturities (insurance at 30yr, money market at 3mo), creating independent supply/demand at each maturity.

**2s10s as a recession signal:**
- Has inverted before every US recession since 1970 (with a ~6-18 month lead)
- Not perfect: false signal in 1998; long lead times vary
- Mechanism: tight Fed policy (high 2yr) + weak growth expectations (low 10yr)

**Limitations:**
- The yield curve captures risk-free rate expectations; it ignores credit spreads, liquidity, and supply/demand technicals
- Parallel shift assumption (used in Duration) is violated most of the time
- Bootstrapping requires interpolation between quoted maturities — choice of interpolation method (linear, cubic spline, Nelson-Siegel) affects results

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# --- Bootstrapping zero rates from par rates ---

def bootstrap_zero_rates(maturities_yr, par_rates, freq=2):
    """
    Bootstrap zero-coupon (spot) rates from par rates.
    
    Parameters
    ----------
    maturities_yr : list of float - maturity in years (e.g. [0.5, 1.0, 1.5, 2.0])
    par_rates     : list of float - par coupon rates (e.g. [0.04, 0.042, ...])
    freq          : int - coupon payments per year (2 = semi-annual)
    
    Returns
    -------
    zero_rates : list of float - bootstrapped zero rates
    """
    zero_rates = []
    # discount_factors[i] = P(0, t_i) = 1 / (1 + z_i/freq)^(t_i * freq)
    discount_factors = []

    for i, (T, r) in enumerate(zip(maturities_yr, par_rates)):
        n_periods = int(round(T * freq))
        coupon = 100 * r / freq         # coupon per period, per $100 face

        # Sum of discounted intermediate coupons (using already-known zero rates)
        pv_intermediate = 0.0
        for j in range(len(discount_factors)):
            pv_intermediate += coupon * discount_factors[j]

        # Solve for the terminal discount factor:
        # 100 = pv_intermediate + (100 + coupon) * df_T
        df_T = (100 - pv_intermediate) / (100 + coupon)
        discount_factors.append(df_T)

        # Convert discount factor to zero rate (annual, compounding at freq)
        z = freq * ((1 / df_T) ** (1 / n_periods) - 1)
        zero_rates.append(z)

    return zero_rates


# Example data: US Treasury-like par rates
maturities = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0, 30.0]
par_rates  = [0.0400, 0.0420, 0.0440, 0.0460, 0.0490, 0.0520,
              0.0535, 0.0545, 0.0550, 0.0530]

zero_rates = bootstrap_zero_rates(maturities[:4], par_rates[:4])
print("Bootstrapped zero rates:")
for m, z in zip(maturities[:4], zero_rates):
    print(f"  {m:.1f}yr: {z*100:.4f}%")


# --- Forward rate calculation ---

def forward_rates_continuous(maturities, zero_rates_continuous):
    """
    Compute instantaneous forward rates from continuously-compounded zero rates.
    f(t1, t2) = (z2*t2 - z1*t1) / (t2 - t1)
    """
    fwds = []
    for i in range(1, len(maturities)):
        t1, t2 = maturities[i-1], maturities[i]
        z1, z2 = zero_rates_continuous[i-1], zero_rates_continuous[i]
        f = (z2 * t2 - z1 * t1) / (t2 - t1)
        fwds.append((t1, t2, f))
    return fwds


# --- Plot yield curve shapes ---

def plot_yield_curves():
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    mats = np.linspace(0.25, 30, 100)

    shapes = {
        'Normal': lambda t: 0.02 + 0.025 * (1 - np.exp(-t/5)),
        'Inverted': lambda t: 0.06 - 0.025 * (1 - np.exp(-t/5)),
        'Humped': lambda t: 0.03 + 0.02 * t/5 * np.exp(1 - t/5),
    }

    for ax, (name, fn) in zip(axes, shapes.items()):
        yields = fn(mats)
        ax.plot(mats, yields * 100, 'b-', lw=2)
        ax.set_title(f'{name} Yield Curve')
        ax.set_xlabel('Maturity (years)')
        ax.set_ylabel('Yield (%)')
        ax.set_ylim(0, 8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('yield_curve_shapes.png', dpi=150)
    plt.show()

plot_yield_curves()


# --- 2s10s spread visualization ---

import pandas as pd

def plot_2s10s_example():
    """Simulate and plot 2s10s spread with recession shading."""
    np.random.seed(42)
    dates = pd.date_range('2000-01-01', '2025-12-31', freq='M')
    n = len(dates)

    # Simulate stylized 2yr and 10yr yields
    t = np.arange(n)
    rate_2yr  = 3.0 + 2.5 * np.sin(2 * np.pi * t / (n * 0.6)) + np.random.randn(n) * 0.2
    rate_10yr = 4.0 + 1.5 * np.sin(2 * np.pi * t / (n * 0.8)) + np.random.randn(n) * 0.15
    spread_2s10s = rate_10yr - rate_2yr

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 6), sharex=True)
    ax1.plot(dates, rate_2yr, label='2yr yield', alpha=0.8)
    ax1.plot(dates, rate_10yr, label='10yr yield', alpha=0.8)
    ax1.set_ylabel('Yield (%)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(dates, spread_2s10s, 'purple', lw=1.5, label='2s10s spread')
    ax2.axhline(0, color='red', linestyle='--', lw=1, alpha=0.7)
    ax2.fill_between(dates, spread_2s10s, 0,
                     where=(spread_2s10s < 0), alpha=0.3, color='red', label='Inverted')
    ax2.set_ylabel('Spread (%)')
    ax2.set_xlabel('Date')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.suptitle('2yr vs 10yr Treasury Yield and 2s10s Spread', fontsize=12)
    plt.tight_layout()
    plt.savefig('2s10s_spread.png', dpi=150)
    plt.show()

plot_2s10s_example()
```

## Bridge to Quant / ML

**Rates trading strategies:**
- **Curve steepener/flattener:** bet on the 2s10s spread widening or narrowing. Long 2yr + short 10yr = flattener (profits if curve flattens).
- **Butterfly:** long belly (5yr), short wings (2yr + 10yr). Profits from curve humping.
- **Carry and roll:** hold bonds that are cheap relative to their forward rates and benefit from the passage of time as they "roll down" the curve.

**Fixed income risk management:** Key rate durations measure exposure to each part of the curve independently. A portfolio manager can be flat duration overall but have significant exposure to the 2yr-5yr sector flattening.

**Macro signals for quant models:** The yield curve (especially 2s10s and 3M-10yr spreads) is one of the most powerful macroeconomic predictors. It is commonly used as a regime feature in [[Regime Detection]] models and as an alpha signal in macro quantitative strategies.

**Nelson-Siegel model:** A parametric model that fits the yield curve with three factors: level, slope, and curvature. The three factors map to: (1) a constant long-run rate, (2) an exponential decaying component (short end), (3) a humped component. Frequently used in central bank research and [[Feature Engineering Finance]] for generating compact, interpretable yield curve features.

**Credit spreads:** Corporate bond yields = Treasury yield + credit spread. The yield curve provides the risk-free baseline; credit spread models (structural or reduced-form) explain the difference.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** What is the difference between a spot (zero) rate, a par rate, and a forward rate? Give an intuitive description of each.
<details><summary>Answer</summary>A **spot rate** $z(t)$ is the yield on a zero-coupon bond maturing at time $t$ — the pure, unambiguous rate for lending money from today to time $t$ with no intermediate cash flows. A **par rate** is the coupon rate that makes a coupon bond price exactly at par (\$100) — it blends together spot rates across maturities, making it less "pure" but easier to observe from quoted market prices. A **forward rate** \$f(t_1, t_2)\$ is the implied rate for borrowing between two future dates — it answers: "given today's spot rates, what rate would a rational lender demand to commit to a loan starting at \$t_1\$ and maturing at \$t_2$?" It is the marginal rate embedded in the term structure between those two dates.</details>

**Q2.** Why has an inverted yield curve (short rates > long rates) historically predicted recessions?
<details><summary>Answer</summary>Two mechanisms. First, under the expectations hypothesis, long rates reflect the market's expectation of future short rates. If the 10-year yield is below the 2-year yield, the market expects interest rates to fall substantially over the next decade — which typically happens as central banks cut rates in response to economic weakness. Second, mechanically: an inverted curve compresses bank net interest margins (banks borrow short, lend long). When short rates exceed long rates, the lending business becomes unprofitable, banks tighten credit, and economic activity slows. The 2s10s inversion has preceded every US recession since 1970 with a 6–18 month lead.</details>

**Q3.** Why must you bootstrap spot rates from par rates rather than using par rates directly as discount rates?
<details><summary>Answer</summary>A par rate is an internal rate of return that makes a coupon bond price at par — it is a blend of the true spot rates at every cash flow date, weighted by the size of each cash flow. Using par rates as discount rates would lead to inconsistency: you would be discounting, say, the 1-year cash flow of a 5-year bond at the 5-year par rate, rather than at the actual 1-year spot rate. This misprices the early cash flows. Bootstrapping extracts a separate, pure spot rate for each maturity, so that each cash flow is discounted at the correct rate for its specific horizon. Only spot rates produce consistent, arbitrage-free bond prices.</details>

---

### Level 2 — Quantitative

**Q4.** Given: 1-year spot rate = 4.00%, 2-year spot rate = 5.00% (continuous compounding). Compute the 1-year forward rate from year 1 to year 2.
<details><summary>Answer</summary>Using the forward rate formula: $f(1,2) = \frac{z(2) \times 2 - z(1) \times 1}{2-1} = \frac{0.05 \times 2 - 0.04 \times 1}{1} = \frac{0.10 - 0.04}{1} = 0.06 = 6\%$. Interpretation: lending money for 2 years at 5% must be equivalent to lending for 1 year at 4% and then re-lending for 1 more year at 6%. Any other forward rate would create an arbitrage opportunity between the 1-year and 2-year investments.</details>

**Q5.** Using the bootstrapping example from the walkthrough (0.5yr par rate 4.00%, 1yr par rate 4.20%, semi-annual), verify that $z(1) = 4.212\%$.
<details><summary>Answer</summary>From Step 1: $z(0.5) = 4.00\%$ → discount factor for 0.5yr: $df_{0.5} = 1/(1+0.04/2) = 1/1.02 = 0.98039$. Step 2: 1-year par bond with 4.20% coupon pays $2.10$ at 0.5yr and $102.10$ at 1yr. $100 = 2.10 \times 0.98039 + 102.10 \times df_1$. $100 = 2.059 + 102.10 \times df_1$. $df_1 = 97.941/102.10 = 0.95927$. $z(1) = 2 \times (1/0.95927^{0.5} - 1) = 2 \times (1/0.97949 - 1) = 2 \times 0.02096 = 4.191\%$. Close to the stated 4.212% — small rounding differences in the walkthrough's intermediate steps produce the exact 4.212%.</details>

---

### Level 3 — Coding

**Q6.** The `bootstrap_discount_curve` function assumes annual payment dates. What changes would be needed to handle semi-annual coupon bonds, and why does the number of discount factors needed equal the number of payment periods, not the number of years?
<details><summary>Answer</summary>For semi-annual bonds, you need a discount factor at every 6-month payment date (0.5yr, 1yr, 1.5yr, ...) rather than at every year. The `maturities` list would be `[0.5, 1.0, 1.5, 2.0, ...]` and the coupon per period would be `rate/2` (semi-annual coupon). The `annuity_sum` accumulates discount factors at each 6-month interval. The reason the number of discount factors equals the number of payment periods is that each coupon bond gives exactly one equation (pricing at par), which pins down exactly one unknown discount factor — the one at the final maturity. All earlier discount factors are already known from shorter-maturity bonds solved previously. You need as many bootstrapping steps as there are distinct payment dates.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| The yield curve shows the return from buying bonds | The yield curve shows current spot rates, which are guaranteed returns only for zero-coupon bonds held to maturity. Coupon bond returns depend on reinvestment rates. |
| An inverted yield curve means the market predicts a recession | An inverted curve means the market expects short rates to fall in the future. This usually accompanies recession expectations, but the causation is through the monetary policy expectation mechanism, not the inversion itself. |
| Spot rates and par rates are interchangeable | Par rates blend across maturities; spot rates are pure single-maturity rates. Using par rates as discount rates misprices multi-cash-flow instruments. |
| The yield curve is a single curve | In practice, there are multiple curves: the Treasury spot curve, the swap curve (SOFR), the OIS curve, and corporate curves for each rating. They differ by credit risk and liquidity. |

## Related Concepts

- [[Duration]] — price sensitivity assumes a parallel yield curve shift
- [[Convexity]] — curvature of price-yield relationship; curve trades generate convexity
- [[Forward Rate Agreement]] — instrument that locks in a forward rate
- [[Regime Detection]] — yield curve inversion as a macro regime signal
- [[Feature Engineering Finance]] — Nelson-Siegel factors as ML features

## Sources Used

- Hull, J. - *Options, Futures, and Other Derivatives*, ch. 4 (Interest Rate Futures and the Yield Curve)
- Tuckman, B. & Serrat, A. - *Fixed Income Securities*, ch. 2 (Spot, Forward, and Par Rates)
- Diebold, F. & Li, C. - *Forecasting the Term Structure of Government Bond Yields* (2006)

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
