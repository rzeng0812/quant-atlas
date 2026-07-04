---
type: concept
domain: 20-Markets
tags: [fixed-income, derivatives, interest-rates, swaps]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-18
review_interval_days: 365
sources:
  - "Hull - Options, Futures, and Other Derivatives ch.7"
created: 2026-04-18
---

> [!info] Problem Chain
> **Chain:** Hedging → Gap 1/2: Eliminating and managing interest rate risk (fixed-income hedging instrument)
> **This concept:** Provides the most liquid and flexible instrument for modifying a portfolio's interest rate exposure — a pay-fixed swap adds duration; a receive-fixed swap removes it — without buying or selling the underlying bonds.
> **Alternative approaches to this gap:** Treasury futures (exchange-traded, standardized maturities), Bond options (directional + vol), FRAs (short-end hedging only)
> **You need first:** [[Bond Basics]], [[Yield Curve]], [[Duration]]
> **This unlocks:** [[HJM Framework]] (models the rates swaps are priced off), [[SABR Model]] (swaption vol surface), [[Vasicek Model]] (short-rate models feed swap pricing)

> Exchange fixed cash flows for floating cash flows on a notional principal; most traded derivative in the world

## Why This Exists

**The gap:** An institution holding a large portfolio of floating-rate bonds (or liabilities) is exposed to interest rate moves, but selling and replacing the entire portfolio is costly, slow, and may trigger taxes or accounting events. A similarly matched institution on the other side of a rate view needs an equally frictionless way to express it.
**What came before:** Direct bond purchases or sales, fixed-rate loans, or Treasury futures with limited tenors. These either required large capital outflows or had maturity mismatches that made precise duration hedging difficult.
**What this adds:** A plain vanilla interest rate swap is the most capital-efficient rate instrument: no notional is exchanged, credit exposure is only a few percent of notional, and the instrument can be tailored to any maturity and notional. Valuing a swap as a portfolio of two bonds (long floating, short fixed) connects it directly to the yield curve discount factors, making it fully consistent with bond pricing theory. The fair swap rate is exactly the par yield, so the swap curve and the yield curve are unified.
**What it still doesn't solve:** The standard swap is linear — it has duration but no convexity beyond the small convexity of the floating leg. Interest rate *options* (caps, floors, swaptions) are needed to hedge convexity or manage the risk of rate volatility, not just rate direction.

## Math Concepts

### Plain Vanilla Interest Rate Swap

The canonical swap: Party A (the **fixed payer**) pays a fixed rate $K$ and receives the floating rate (e.g., SOFR) on notional $N$ at each payment date.

Net payment from fixed payer at each period $i$:

$$\text{Net payment}_i = (K - L_i) \times N \times \Delta t$$

Where:
- $K$ = fixed (swap) rate agreed at inception
- $L_i$ = floating rate set at the **previous** period (paid in arrears)
- $\Delta t$ = length of the payment period in years (e.g., 0.25 for quarterly)
- Positive = fixed payer pays; negative = fixed payer receives

### Valuing a Swap as Two Bonds

At any point in time, a swap to the **fixed payer** is equivalent to:
- **Long** a floating-rate bond (receiving SOFR) — worth $B_{float}$
- **Short** a fixed-rate bond (paying coupon $K$) — worth $B_{fixed}$

$$V_{swap} = B_{float} - B_{fixed}$$

**Floating bond value:** A floating-rate bond always resets to par on each coupon date. On a reset date:

$$B_{float} = N$$

Between reset dates, it is slightly off par by one accrual period.

**Fixed bond value:** Standard bond pricing with coupon $K$, using the current discount curve $P(0, t_i)$ (zero-coupon bond prices):

$$B_{fixed} = K \cdot N \cdot \Delta t \sum_{i=1}^{n} P(0, t_i) + N \cdot P(0, t_n)$$

### Fair Swap Rate at Inception

At initiation, the swap is structured so that $V_{swap} = 0$, meaning $B_{float} = B_{fixed}$. On a reset date $B_{float} = N$, so solve:

$$N = K \cdot N \cdot \Delta t \sum_{i=1}^{n} P(0, t_i) + N \cdot P(0, t_n)$$

$$\boxed{K = \frac{1 - P(0, t_n)}{\Delta t \sum_{i=1}^{n} P(0, t_i)}}$$

The fair swap rate $K$ is the coupon rate at which the fixed bond prices at par — equivalently, it is the **par yield** for that maturity. This is why the swap curve and the par yield curve are nearly identical in practice.

### Swap Value After Inception

After rates move, the swap has non-zero value. For a pay-fixed swap entered at rate $K$:

$$V = N \cdot \left[ P(0, t_n) + K \cdot \Delta t \sum_{i=1}^{n} P(0, t_i) - 1 \right] \cdot (-1)$$

Or simply: reprice the fixed leg at current discount factors and subtract from floating leg value.

### DV01 of a Swap

The swap's sensitivity to a 1bp rise in rates:

$$\text{DV01}_{swap} \approx \text{DV01}_{fixed\ leg} - \text{DV01}_{floating\ leg}$$

For a standard swap, the floating leg has very short duration (it resets frequently), so:

$$\text{DV01}_{swap} \approx \text{DV01}_{fixed\ leg} \approx N \cdot \Delta t \sum_{i=1}^{n} P(0, t_i) \times 0.0001$$

This is the **annuity factor** times one basis point. For a 10-year quarterly swap on \$10M notional, DV01 is roughly \$8,000 — meaning each 1bp move in rates causes an \$8,000 P&L swing.

### SOFR vs LIBOR

Prior to 2022, most USD swaps referenced **LIBOR** (London Interbank Offered Rate). Following manipulation scandals, the market transitioned to **SOFR** (Secured Overnight Financing Rate). SOFR is an overnight rate based on actual repo transactions — much harder to manipulate. Other major references: **SONIA** (UK), **ESTR** (EUR), **TONA** (JPY).

## Walkthrough

**Example:** 3-year pay-fixed swap, notional \$10M, fixed rate 3.5%, receive SOFR (annual settlements).

| Year | SOFR (set at start of year) | Fixed payment | Floating receipt | Net (to fixed payer) |
|------|----------------------------|---------------|-----------------|----------------------|
| 1 | 3.00% | $350,000 | $300,000 | **pay \$50,000** |
| 2 | 4.00% | $350,000 | $400,000 | **receive \$50,000** |
| 3 | 5.00% | $350,000 | $500,000 | **receive \$150,000** |

Net over 3 years: +\$150,000 received. The fixed payer benefited from locking in 3.5% — rates rose above the swap rate.

**Mark-to-market after Year 1:**

Suppose after Year 1, the market swap rate for a new 2-year swap has risen to 4.5%. Your swap (paying only 3.5%) now has positive value to you — you locked in a below-market rate.

The swap's mark-to-market value = present value of the remaining cash flows at current market rates. The fixed leg (3.5%) is worth less than the floating leg now discounted at 4.5% rates, so the swap has positive value to the fixed payer.

This is what banks report on their balance sheets as the **fair value** of their swap book.

## Analysis

### Uses of Swaps

| Use Case | Description |
|----------|-------------|
| **Hedging** | A floating-rate borrower pays fixed to eliminate rate uncertainty |
| **Asset-liability management** | Banks/insurers match duration of assets and liabilities |
| **Speculation** | If you think rates will rise, pay fixed now (profit if SOFR > K) |
| **Yield enhancement** | Receive fixed to earn carry if rates stay low |
| **Synthetic bonds** | Combine a floating-rate note with a receive-fixed swap to create a synthetic fixed bond |

### Credit Risk and Central Clearing

Because notional is never exchanged, counterparty credit risk is limited to the **net present value** of the swap — typically 1–3% of notional, not 100%. Still, pre-2008, large OTC swap books created significant systemic risk.

Post-2008 (Dodd-Frank, EMIR): most standardized swaps are **centrally cleared** through CCPs (e.g., LCH, CME). Parties post initial margin and variation margin daily — dramatically reducing counterparty risk.

### The Swap Curve as a Benchmark

For maturities beyond 2 years, the **swap curve** (par swap rates vs. maturity) is often more liquid than Treasury bonds and is used as the primary benchmark for:
- Pricing corporate bonds (spread over swap rate)
- Discounting derivatives cash flows
- ALM benchmarking for pension funds

### LIBOR Transition Impact

The LIBOR transition required repricing trillions in legacy contracts. SOFR is a risk-free overnight rate with no credit component, so SOFR-based swap rates trade slightly below old LIBOR rates. A **credit spread adjustment** (CSA) was added to legacy LIBOR contracts to approximate equivalence.

## Implementation

```python
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt


# ── Step 1: Build a discount curve from par swap rates ────────────────────────

def bootstrap_discount_curve(maturities: list, par_rates: list) -> dict:
    """
    Bootstrap discount factors P(0, T) from annual par swap rates.

    At each maturity T_n, the par swap rate K_n satisfies:
        1 = K_n * sum_{i=1}^{n} P(0,T_i) + P(0,T_n)

    Solve sequentially: given P(0,T_1),...,P(0,T_{n-1}), solve for P(0,T_n).

    Parameters
    ----------
    maturities : list of int   - e.g. [1, 2, 3, 5, 7, 10]
    par_rates  : list of float - annual par swap rates, e.g. [0.03, 0.032, ...]

    Returns
    -------
    dict mapping maturity -> discount factor
    """
    discount_factors = {}
    annuity_sum = 0.0

    for T, K in zip(maturities, par_rates):
        # For maturities > 1: P(0,T) = (1 - K * annuity_sum) / (1 + K)
        # For maturity = 1:   P(0,1) = 1 / (1 + K)
        P = (1 - K * annuity_sum) / (1 + K)
        discount_factors[T] = P
        annuity_sum += P

    return discount_factors


# Example: flat(ish) rate environment
maturities  = [1, 2, 3, 5, 7, 10]
par_rates   = [0.030, 0.032, 0.035, 0.038, 0.040, 0.042]

df = bootstrap_discount_curve(maturities, par_rates)
print("Discount factors:")
for T, P in df.items():
    zero_rate = -np.log(P) / T
    print(f"  T={T:2d}y  P(0,T)={P:.5f}  zero rate={zero_rate:.4%}")


# ── Step 2: Value a swap ───────────────────────────────────────────────────────

def swap_value(notional: float, fixed_rate: float,
               payment_times: list, discount_factors: dict,
               payer: str = 'fixed') -> float:
    """
    Value a plain vanilla interest rate swap.

    Parameters
    ----------
    notional        : float - notional principal
    fixed_rate      : float - fixed leg rate (e.g. 0.035 for 3.5%)
    payment_times   : list  - annual payment dates, e.g. [1, 2, 3]
    discount_factors: dict  - {maturity: P(0,T)} from bootstrap
    payer           : str   - 'fixed' (pay fixed, receive float) or 'float'

    Returns
    -------
    float : mark-to-market value to the specified payer
    """
    # Interpolate missing discount factors via log-linear interpolation
    def get_df(t):
        if t in discount_factors:
            return discount_factors[t]
        # log-linear interpolation
        ts = sorted(discount_factors.keys())
        ps = [discount_factors[k] for k in ts]
        log_ps = np.log(ps)
        return np.exp(np.interp(t, ts, log_ps))

    # Fixed leg: PV of coupon payments + principal
    fixed_leg = sum(fixed_rate * notional * get_df(t) for t in payment_times)
    fixed_leg += notional * get_df(payment_times[-1])  # principal repayment

    # Floating leg: at a reset date, floating bond always prices to par
    float_leg = notional  # assumes we are on a reset date

    value = float_leg - fixed_leg
    if payer == 'float':
        value = -value
    return value


# Value a 3-year pay-fixed swap at 3.5% on $10M (at inception, should be ~0)
pmt_times = [1, 2, 3]
v = swap_value(10_000_000, 0.035, pmt_times, df, payer='fixed')
print(f"\nSwap value at inception (3.5% fixed, 3yr): ${v:,.2f}")
# Close to 0 because 3.5% is near the 3-year par rate


# ── Step 3: Fair swap rate ────────────────────────────────────────────────────

def fair_swap_rate(payment_times: list, discount_factors: dict) -> float:
    """
    Compute the fair (par) swap rate K such that swap value = 0 at inception.

    K = (1 - P(0, T_n)) / (dt * sum P(0, T_i))
    Assumes annual payments (dt=1).
    """
    def get_df(t):
        if t in discount_factors:
            return discount_factors[t]
        ts = sorted(discount_factors.keys())
        ps = [discount_factors[k] for k in ts]
        return np.exp(np.interp(t, ts, np.log(ps)))

    annuity = sum(get_df(t) for t in payment_times)
    P_Tn = get_df(payment_times[-1])
    return (1 - P_Tn) / annuity


k3 = fair_swap_rate([1, 2, 3], df)
k10 = fair_swap_rate(list(range(1, 11)), df)
print(f"\nFair swap rate (3yr): {k3:.4%}")
print(f"Fair swap rate (10yr): {k10:.4%}")


# ── Step 4: DV01 of a swap ────────────────────────────────────────────────────

def swap_dv01(notional: float, fixed_rate: float,
              payment_times: list, discount_factors: dict,
              bump: float = 0.0001) -> float:
    """
    DV01: change in swap value for a 1bp parallel shift in rates.
    Approximate by bumping all discount factors.
    """
    def bump_dfs(dfs, dy):
        """Bump discount factors: P_new(0,T) = P(0,T) * exp(-dy*T)"""
        return {T: P * np.exp(-dy * T) for T, P in dfs.items()}

    df_up   = bump_dfs(discount_factors, bump)
    df_down = bump_dfs(discount_factors, -bump)

    v_up   = swap_value(notional, fixed_rate, payment_times, df_up,   payer='fixed')
    v_down = swap_value(notional, fixed_rate, payment_times, df_down, payer='fixed')

    return (v_up - v_down) / 2  # central difference; DV01 per 1bp bump


dv01 = swap_dv01(10_000_000, 0.035, [1, 2, 3], df)
print(f"\nDV01 (3yr swap, $10M notional): ${dv01:,.0f} per bp")


# ── Step 5: Visualize mark-to-market as rates shift ──────────────────────────

rate_shifts = np.linspace(-0.02, 0.02, 100)  # -200bp to +200bp

def bump_dfs(dfs, dy):
    return {T: P * np.exp(-dy * T) for T, P in dfs.items()}

values = []
for shift in rate_shifts:
    df_shifted = bump_dfs(df, shift)
    v = swap_value(10_000_000, 0.035, [1, 2, 3], df_shifted, payer='fixed')
    values.append(v)

plt.figure(figsize=(8, 4))
plt.plot(rate_shifts * 100, [v / 1000 for v in values], color='steelblue', linewidth=2)
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle=':')
plt.xlabel('Parallel rate shift (bps)')
plt.ylabel('Swap MtM value ($000s)')
plt.title('3yr Pay-Fixed Swap: MtM vs Rate Move ($10M notional, K=3.5%)')
plt.tight_layout()
plt.show()
# If rates rise, the floating receipts increase → pay-fixed swap gains value
```

## Bridge to Quant / ML

**The risk-free curve:** Swap rates (especially SOFR swaps) are the primary input to the risk-free discount curve used to price all derivatives. Every option, cap, floor, and swaption is priced against this curve.

**Swaptions and vol surface:** A swaption is an option to enter a swap — it brings optionality into the fixed income world. The [[SABR Model]] is the standard model for swaption implied volatility surfaces. Swap DV01 is the key sensitivity used when delta-hedging a swaption book.

**Interest rate models:** The [[Vasicek Model]] and [[HJM Framework]] describe the evolution of rates over time. Their outputs feed directly into swap pricing: given a model for the short rate, you can compute $P(0,T)$ for all maturities and then price any swap.

**Curve bootstrapping in practice:** The bootstrap algorithm (Step 1 above) is the core routine in every fixed income pricing library. In a real desk system, it handles overnight rates, futures, and swap rates simultaneously, with interpolation methods that ensure smooth forward curves.

**ALM and XVA:** Banks compute swap portfolios' Potential Future Exposure (PFE) using Monte Carlo simulations of the yield curve. This feeds into CVA (credit valuation adjustment) and MVA (margin valuation adjustment) — collectively called XVA. Machine learning models increasingly predict CVA changes given portfolio and macro features.

**Macro factor models:** Swap rates at different maturities are highly correlated. PCA of the swap curve typically yields three factors: level (~95% of variance), slope, and curvature — the same factors as in the [[Yield Curve]] note. Long-short positions on swaps are often expressed as level bets (duration) or slope bets (receiving 2s vs paying 10s).

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why is a plain vanilla swap equivalent to a long floating-rate bond and a short fixed-rate bond (for the fixed payer)? What does this imply about the swap's duration?
<details><summary>Answer</summary>The fixed payer receives the floating leg (equivalent to owning a floating-rate bond — receives SOFR each period, plus notional at maturity) and pays the fixed leg (equivalent to having issued a fixed-rate bond — pays coupon $K$ each period, plus notional at maturity). The notional payments cancel at maturity, which is why notional is never actually exchanged. Duration: a floating-rate bond resets to par at each coupon date, so its duration is approximately the time to the next reset (very short, e.g., 0.25 years for a quarterly swap). The fixed-rate bond has duration proportional to its maturity. Therefore, the swap's net duration ≈ duration of the fixed leg ≈ DV01 of the fixed leg.</details>

**Q2.** Why is the swap market so much larger in notional than the bond market, given that swaps have no upfront notional payment?
<details><summary>Answer</summary>Because no notional is exchanged, entering a swap requires minimal upfront capital — only initial margin (typically 1–3% of notional) for centrally cleared swaps, versus 100% of notional for a bond purchase. This makes swaps extremely capital-efficient for expressing or hedging rate views. A bank wanting to hedge \$1B in rate exposure can enter a swap for that notional while using only \$10–30M of capital, versus \$1B to buy Treasury bonds. The leverage embedded in swaps multiplies their notional far beyond the comparable bond market, producing the \$400+ trillion outstanding figure.</details>

**Q3.** A corporation has a 5-year floating-rate loan at SOFR + 1.5%. To "fix" its interest cost using a swap, should it pay fixed or receive fixed in the swap? What is the net rate it will pay?
<details><summary>Answer</summary>It should **pay fixed** and receive floating (receive SOFR). Combining: (1) loan: pays SOFR + 1.5%; (2) swap: pays fixed rate $K$, receives SOFR. Net cash flow: SOFR + 1.5% + $K$ - SOFR = $K$ + 1.5%. The SOFR exposure cancels, leaving a fixed total rate of $K$ + 1.5% regardless of where SOFR moves. If $K$ = 3.5%, the corporation pays 5.0% fixed — their borrowing cost is now fully predictable for the life of the loan.</details>

---

### Level 2 — Quantitative

**Q4.** Using the discount factors from the implementation: $P(0,1)=0.9709$, $P(0,2)=0.9387$, $P(0,3)=0.9000$ (approximate). Verify the fair 3-year swap rate.
<details><summary>Answer</summary>Fair swap rate formula (annual payments, $\Delta t = 1$): $K = (1 - P(0,3)) / \sum_{i=1}^{3} P(0,t_i) = (1 - 0.9000) / (0.9709 + 0.9387 + 0.9000) = 0.1000 / 2.8096 \approx 3.559\%$. This is close to the 3.5% par rate used in the example (small difference due to the approximate discount factors used here). The fair swap rate equals the par yield — the coupon rate at which the fixed bond prices at par — confirming the bond/swap equivalence.</details>

**Q5.** A pay-fixed swap has DV01 of \$8,000 per bp (10-year, \$10M notional). Rates rise by 25bp. What is the P&L to the fixed payer?
<details><summary>Answer</summary>The fixed payer receives floating (SOFR) and pays fixed. When rates rise, SOFR receipts increase while the fixed payment is unchanged → the swap gains value for the fixed payer. P&L = $+25 \times \$8,000 = +\$200,000$. Intuition: each 1bp rise in rates increases the floating leg receipts by \$8,000/bp relative to the fixed payment, so a 25bp rise generates \$200,000 in mark-to-market gain. This also explains why a bond portfolio manager who is long bonds (long duration, vulnerable to rate rises) would pay fixed in a swap to hedge — the swap gains offset the bond losses.</details>

---

### Level 3 — Coding

**Q6.** The `swap_dv01` function uses a central-difference bump: it applies $\pm 1$bp to all discount factors and takes $(V_{up} - V_{down})/2$. Why is a central difference more accurate than a forward difference $(V_{up} - V_0)/1$?
<details><summary>Answer</summary>The central difference approximates $\partial V / \partial y \approx (V(y+h) - V(y-h))/(2h)$, which is second-order accurate in $h$ (error $\sim h^2$). The forward difference $(V(y+h) - V(y))/h$ is only first-order accurate (error $\sim h$). For a bump size of $h = 1$bp (0.0001), the second-order term in the Taylor expansion of $V$ contributes $O(h^2) \approx 10^{-8}$ error for the central difference, versus $O(h) \approx 10^{-4}$ for the forward difference. Since DV01 is reported to dollar precision for a \$10M notional swap, the higher accuracy of the central difference is meaningful. Practically: the central difference also cancels out any odd-order Taylor terms (the \$h^3$, $h^5$ terms vanish by symmetry), leaving only even-order error.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| The notional principal changes hands in a swap | Notional is never exchanged. Only net interest payments are settled, making swaps extremely capital-efficient relative to equivalent bond positions. |
| A swap value is always zero | A swap is zero at inception (designed so). After rates move, its mark-to-market value changes — it can be substantially positive or negative to either party. |
| Pay-fixed swaps always lose money when rates rise | The opposite: a pay-fixed swap gains value when rates rise (you locked in paying a below-market rate). Receive-fixed swaps lose when rates rise. |
| Swaps carry the full notional as credit risk | Credit exposure is only the replacement cost (mark-to-market value), typically 1–3% of notional, and is further reduced by central clearing and collateral posting. |

## Related Concepts

- [[Bond Basics]] — a swap's fixed leg is priced exactly like a coupon bond
- [[Yield Curve]] — swap rates form the primary benchmark yield curve
- [[Duration]] — the DV01 of a swap is computed from the fixed leg's duration
- [[HJM Framework]] — no-arbitrage model for the forward rate curve underlying swap pricing
- [[Vasicek Model]] — one-factor short-rate model; outputs used to price swaps
- [[SABR Model]] — standard volatility model for swaptions

## Sources Used

- Hull, J. - *Options, Futures, and Other Derivatives*, ch. 7 (Swaps)
- Hull, J. - *Options, Futures, and Other Derivatives*, ch. 4 (Discount curve, par rates)
- Andersen, L. & Piterbarg, V. - *Interest Rate Modeling Vol. 1*, ch. 1-2

---
## Revision Log
| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | Hull |
| 2026-04-18 | Renamed "Implementation (Python)" → "Implementation" for section consistency | review |
