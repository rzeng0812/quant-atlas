---
type: concept
domain: 20-Markets
tags: [derivatives, options, no-arbitrage]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-11
review_interval_days: 365
sources:
  - "Hull ch.11"
created: 2026-04-18
---

> [!info] Problem Chain
> **Chain:** Pricing → Gap 1: No agreed method to value an uncertain future payoff
> **This concept:** Demonstrates the no-arbitrage principle in its cleanest form — two portfolios with identical payoffs must have the same price, regardless of any model.
> **Alternative approaches to this gap:** none — unique solution (the first no-arbitrage relationship; [[Black-Scholes Model]] later generalizes the principle)
> **You need first:** basic option payoff definitions (call, put, strike, expiry)
> **This unlocks:** [[Black-Scholes Model]], [[Implied Volatility]], [[Delta Hedging]], [[American Options]]

## Why This Exists

**The gap:** Option traders needed to know whether a call and a put on the same stock — same strike, same expiry — were priced consistently with each other. Without any relationship between them, each option was priced independently, and the market could have a call and put at prices that together created free money for anyone who noticed.

**What came before:** There was no agreed framework for connecting call and put prices. Each option was treated as a standalone object with its own supply and demand. Practitioners had intuitions that the two were related, but no rigorous statement.

**What this adds:** A model-free identity: holding a call plus cash equal to the present value of the strike produces exactly the same payoff at expiry as holding a put plus the stock. Because the payoffs are identical in every possible scenario, the prices must be equal today — or someone can extract risk-free profit. This is the first clean instance of no-arbitrage pricing. No volatility model needed, no assumptions about how stock prices move.

**What it still doesn't solve:** Parity tells you the *relationship* between call and put prices, but not the *level* of either price. You still need a model — like Black-Scholes — to say what an option is actually worth in dollars.

## Math Concepts

**The core identity** (European options on a non-dividend paying stock):

$$C + K e^{-rT} = P + S_0$$

Where:
- $C$ = price of a European call
- $P$ = price of a European put
- $S_0$ = current stock price
- $K$ = strike price (same for both options)
- $r$ = risk-free rate (continuously compounded)
- $T$ = time to expiry (in years)
- $K e^{-rT}$ = present value of the strike (cash you'd need today to have $K$ at expiry)

**Rearrangements** — all equivalent, all useful:

$$C - P = S_0 - K e^{-rT}$$

$$P = C + K e^{-rT} - S_0 \quad \text{(put from call)}$$

$$C = P + S_0 - K e^{-rT} \quad \text{(call from put)}$$

**Why it holds — arbitrage proof:**

Build two portfolios today:

| | Portfolio A | Portfolio B |
|--|-------------|-------------|
| Hold | Long call + $K e^{-rT}$ cash | Long put + Long stock |
| Cash grows to | $K$ at expiry | — |

At expiry, examine both cases:

| Scenario | Portfolio A payoff | Portfolio B payoff |
|----------|--------------------|--------------------|
| $S_T > K$ | $(S_T - K) + K = S_T$ (call ITM, cash pays K) | $0 + S_T = S_T$ (put worthless, hold stock) |
| $S_T < K$ | $0 + K = K$ (call worthless, cash pays K) | $(K - S_T) + S_T = K$ (put ITM, stock worth $S_T$) |
| $S_T = K$ | $K$ | $K$ |

Identical payoffs in every scenario → must have identical prices today. Otherwise: buy the cheaper one, sell the expensive one, pocket the difference at zero risk.

**Synthetic relationships** derived from put-call parity:

$$\underbrace{C - P}_{\text{synthetic forward}} = S_0 - K e^{-rT}$$

- **Synthetic long stock** = long call + short put + invest $K e^{-rT}$
- **Synthetic call** = long stock + long put (a "protective put")
- **Synthetic put** = short stock + long call (a "covered call")
- **Synthetic forward** = long call + short put at the same strike

**Dividends:** if the stock pays dividends with present value $\text{PV}(\text{div})$, the stock's forward price is reduced:

$$C + K e^{-rT} = P + S_0 - \text{PV}(\text{div})$$

**American options:** put-call parity becomes an *inequality* for American options because early exercise is possible. The relationship is:

$$S_0 - K \leq C_{\text{Am}} - P_{\text{Am}} \leq S_0 - K e^{-rT}$$

## Walkthrough

**Setup:** $S_0 = 100$, $K = 100$, $r = 5\%$, $T = 1$ year.

**Given:** a European call trades at $C = 10$. What must the European put cost?

Step 1: compute $K e^{-rT}$:

$$K e^{-rT} = 100 \times e^{-0.05 \times 1} = 100 \times 0.9512 = 95.12$$

Step 2: apply put-call parity:

$$P = C + K e^{-rT} - S_0 = 10 + 95.12 - 100 = 5.12$$

So if $C = 10$, the put *must* be \$5.12. Any other price is an arbitrage.

**Verification with BSM:**

Using Black-Scholes with $\sigma = 20\%$:
- $d_1 = \frac{\ln(100/100) + (0.05 + 0.02) \times 1}{0.20 \times 1} = \frac{0.07}{0.20} = 0.35$
- $d_2 = 0.35 - 0.20 = 0.15$
- $C_{\text{BSM}} \approx 10.45$, $P_{\text{BSM}} \approx 5.57$

Check: $C - P = 10.45 - 5.57 = 4.88$. And $S_0 - K e^{-rT} = 100 - 95.12 = 4.88$. Parity holds exactly.

**Arbitrage example:** Suppose $C = 10$ but $P = 4$ (put is too cheap):

- The correct put price is $5.12$, so $P = 4$ violates parity.
- Buy the cheap side: buy put (\$4) + buy stock (\$100) = \$104 outlay
- Sell the expensive side: sell call (\$10) + invest PV of strike (\$95.12) = \$105.12 received
- Net today: +\$1.12 received upfront, zero risk at expiry (payoffs cancel). Free money.

## Analysis

**Model-free:** put-call parity requires no assumptions about how stock prices move. It holds under any model that rules out arbitrage.

**European only (strictly):** the proof requires holding to expiry. American options can be exercised early, breaking the exact equality (see [[American Options]]).

**Practical violations:** in real markets, tiny violations exist because:
- Bid-ask spreads make the arbitrage unprofitable once transaction costs are included
- Different option series may have slightly different settlement conventions
- Hard-to-borrow stocks (where short-selling is costly) can distort put prices
- Taxes and margin requirements differ between the two sides

**Dividend extensions:** for dividend-paying stocks the adjusted formula must be used. Using the wrong formula (no-dividend version on a dividend stock) gives apparent arbitrage that isn't real.

**Put-call parity as a sanity check:** quants use parity to verify option pricing code. If your model's call and put prices don't satisfy the identity (up to floating-point precision), there's a bug.

**Implied forward price:** rearranging gives $S_0 e^{rT} - (C - P) e^{rT} = K$, which means the market's implied forward stock price can be read directly from the call-put spread — no model needed.

## Implementation

```python
import numpy as np
from scipy.stats import norm


def bsm_price(S, K, r, sigma, T, option_type="call"):
    """Black-Scholes-Merton option price for European options."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def verify_put_call_parity(S, K, r, T, sigma, tol=1e-8):
    """
    Verify put-call parity: C + K*e^{-rT} = P + S
    Returns True if parity holds within tolerance.
    """
    C = bsm_price(S, K, r, sigma, T, "call")
    P = bsm_price(S, K, r, sigma, T, "put")
    pv_strike = K * np.exp(-r * T)

    lhs = C + pv_strike   # call + PV(strike)
    rhs = P + S           # put + stock

    print(f"Call price:       {C:.6f}")
    print(f"Put price:        {P:.6f}")
    print(f"PV of strike:     {pv_strike:.6f}")
    print(f"LHS (C + Ke^-rT): {lhs:.6f}")
    print(f"RHS (P + S):      {rhs:.6f}")
    print(f"Difference:       {abs(lhs - rhs):.2e}")
    print(f"Parity holds:     {abs(lhs - rhs) < tol}")
    return abs(lhs - rhs) < tol


# Base case: ATM, 1 year
print("=== ATM, T=1yr ===")
verify_put_call_parity(S=100, K=100, r=0.05, T=1.0, sigma=0.20)

print()

# Given call price, infer put price
def put_from_call(C, S, K, r, T):
    """Compute put price from call via put-call parity."""
    return C + K * np.exp(-r * T) - S

C_given = 10.0
P_implied = put_from_call(C_given, S=100, K=100, r=0.05, T=1.0)
print(f"=== Given C={C_given}, implied P={P_implied:.4f} ===")

print()

# Demonstrate parity holds across different strikes
print("=== Parity check across strikes ===")
strikes = [80, 90, 100, 110, 120]
for K in strikes:
    holds = verify_put_call_parity(S=100, K=K, r=0.05, T=1.0, sigma=0.20, tol=1e-8)
    C = bsm_price(100, K, 0.05, 0.20, 1.0, "call")
    P = bsm_price(100, K, 0.05, 0.20, 1.0, "put")
    print(f"  K={K:3d}: C={C:.4f}, P={P:.4f}, C-P={C-P:.4f}, "
          f"S-Ke^-rT={100 - K*np.exp(-0.05):.4f}, parity={holds}")
```

## Bridge to Quant / ML

- **Volatility arbitrage:** traders use put-call parity to check for mispricings in implied volatility — if a call and put at the same strike have different implied vols, something is off
- **Synthetic positions:** market makers use synthetic relationships to hedge positions without trading the underlying — crucial for managing inventory
- **Options market microstructure:** the bid-ask spread in options is partly set so that put-call parity violations after transaction costs are always zero — parity is a constraint on how tight spreads can be
- **Model validation:** any option pricing model (neural net, stochastic vol, etc.) can be sanity-checked by verifying it satisfies put-call parity. Violations signal implementation errors.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Put-call parity is described as "model-free." What does that mean, and why does it matter compared to Black-Scholes?
<details>
<summary>Answer</summary>
Model-free means the identity C + Ke^{-rT} = P + S holds under any pricing model that rules out arbitrage — you do not need to assume GBM, constant volatility, or any specific distribution of returns. It follows purely from the fact that two portfolios with identical payoffs in every future scenario must cost the same today. This matters because it is a much stronger statement than BSM: even if BSM is wrong about how prices move, parity must still hold. Violations signal either a data error, transaction cost issue, or a genuine arbitrage opportunity.
</details>

**Q2.** Why does put-call parity become an inequality for American options instead of an equality?
<details>
<summary>Answer</summary>
The proof of put-call parity requires both portfolios to be held to expiry so their payoffs can be compared at that single date. American options can be exercised early. If early exercise is optimal for the put, the holder will exercise before expiry, breaking the "hold to expiry" assumption. The inequality S_0 − K ≤ C_Am − P_Am ≤ S_0 − Ke^{-rT} replaces the equality because early exercise of the put can extract value that the European version cannot, making P_Am > P_Eu and thus the difference C_Am − P_Am smaller than the European version.
</details>

**Q3.** A trader observes that a put is trading cheaper than put-call parity implies. Describe the exact trades to exploit this.
<details>
<summary>Answer</summary>
If the put P is too cheap: the right side (P + S) is cheaper than the left side (C + Ke^{-rT}). Buy the cheap side and sell the expensive side. Specifically: buy the put, buy the stock, sell the call, and borrow Ke^{-rT} (i.e., receive the present value of the strike today and repay K at expiry). At expiry, both sides pay off identically in all scenarios — the borrowed K is repaid by the payoffs — and you pocket the difference in prices upfront with zero net cash flow at expiry.
</details>

---

### Level 2 — Quantitative

**Q4.** S = 50, K = 55, r = 3% (continuously compounded), T = 0.5 years. A call trades at C = 2.00. What must the put cost? If the put instead trades at P = 5.50, describe the arbitrage.
<details>
<summary>Answer</summary>
Step 1: PV of strike = 55 × e^{−0.03 × 0.5} = 55 × 0.9851 = 54.18.
Step 2: P = C + Ke^{-rT} − S = 2.00 + 54.18 − 50 = 6.18. The put must cost \$6.18.

If P = 5.50 (too cheap): buy put (\$5.50), buy stock (\$50), sell call ($2.00), borrow $54.18 (receive now, repay \$55 at T). Net cash today = −5.50 − 50 + 2.00 + 54.18 = +\$0.68 received upfront. At expiry, payoffs cancel in all scenarios — zero risk, \$0.68 profit locked in.
</details>

**Q5.** Using BSM with S = 100, K = 95, r = 5%, σ = 25%, T = 1 year: compute d1, d2, the call price, and verify parity holds by computing the put price two ways — (a) from the BSM put formula and (b) from put-call parity.
<details>
<summary>Answer</summary>
d1 = [ln(100/95) + (0.05 + 0.5 × 0.0625) × 1] / (0.25 × 1) = [0.0513 + 0.08125] / 0.25 = 0.13255 / 0.25 = 0.530.
d2 = 0.530 − 0.25 = 0.280.
N(0.530) ≈ 0.7019, N(0.280) ≈ 0.6103.
Ke^{-rT} = 95 × e^{-0.05} = 95 × 0.9512 = 90.36.
C = 100 × 0.7019 − 90.36 × 0.6103 = 70.19 − 55.14 = 15.05.

(a) BSM put: N(−d2) = N(−0.280) ≈ 0.3897, N(−d1) = N(−0.530) ≈ 0.2981.
P_BSM = 90.36 × 0.3897 − 100 × 0.2981 = 35.21 − 29.81 = 5.40.

(b) Parity: P = C + Ke^{-rT} − S = 15.05 + 90.36 − 100 = 5.41. Matches (rounding).
</details>

---

### Level 3 — Coding

**Q6.** In the `verify_put_call_parity` function, the tolerance is set to `tol=1e-8`. Why is the check `abs(lhs - rhs) < tol` rather than `lhs == rhs`, and what would happen if you set `tol=0`?
<details>
<summary>Answer</summary>
Floating-point arithmetic on computers cannot represent most real numbers exactly — operations like `norm.cdf`, `np.exp`, and multiplication accumulate tiny rounding errors (on the order of machine epsilon, ~1e-16 per operation). So even though BSM call and put formulas are mathematically guaranteed to satisfy parity, their computed values will differ by a small floating-point error (typically ~1e-14 to 1e-12). Setting `tol=1e-8` accepts differences up to 10 nanodollars as "zero," which is correct behavior. Setting `tol=0` would cause the function to return False even for a correct implementation, making it useless as a validation tool. The right tolerance should be orders of magnitude larger than machine epsilon but small enough to catch actual pricing bugs (which would cause errors of cents, not nanodollars).
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Put-call parity requires Black-Scholes | It is completely model-free — it holds under any no-arbitrage framework regardless of how stock prices move |
| Parity holds for American options | It holds only as an inequality for American options; the exact equality requires holding to expiry, which early exercise prevents |
| A put and call at the same strike should have the same price | They have the same price only when the stock equals the present value of the strike (forward ATM). Otherwise C ≠ P; their relationship is C − P = S − Ke^{-rT} |
| Parity violations are real arbitrage opportunities | In practice, bid-ask spreads, transaction costs, and hard-to-borrow fees consume the apparent profit; true riskless arbitrage from parity violations is extremely rare in liquid markets |

## Related Concepts
- [[Black-Scholes Model]] — BSM call and put prices satisfy parity exactly by construction
- [[Option Greeks]] — Delta of a call minus delta of a put equals 1 (a direct consequence of parity)
- [[Implied Volatility]] — call and put at same strike must have the same implied vol (from parity)
- [[American Options]] — parity becomes an inequality; early exercise breaks the exact relationship
- [[Delta Hedging]] — synthetic relationships from parity are the building blocks of hedging strategies

## Sources Used
- Hull — *Options, Futures & Other Derivatives*, ch.11

---

## Revision Log
| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | Hull ch.11 |
| 2026-04-11 | QA review passed — all math, code, sections verified correct | QA review |
| 2026-04-18 | Renamed "Implementation (Python)" → "Implementation" for section consistency | review |
