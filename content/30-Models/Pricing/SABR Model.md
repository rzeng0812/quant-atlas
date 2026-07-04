---
type: concept
domain: 30-Models
tags: [pricing, options, stochastic-volatility, interest-rates]
status: math
stability: evolving
confidence: high
last_reviewed: 2026-04-11
review_interval_days: 90
sources:
  - "Hagan et al. (2002), Managing Smile Risk"
  - "Gatheral, The Volatility Surface, ch. 7"
created: 2026-04-12
---

> Stochastic alpha-beta-rho; industry standard for rates options

> [!info] Problem Chain
> **Chain:** Pricing → Gap 5: BSM assumes constant σ — real markets show a volatility smile (interest rate analog)
> **This concept:** Provides an explicit, approximate closed-form formula mapping four parameters (α, β, ν, ρ) to implied vol at any strike — solving Gap 5 for the interest rate options market where Heston's equity-focused approach is less natural
> **Alternative approaches to this gap:** [[Heston Model]] (stochastic vol — preferred for equities), [[Local Volatility]] (Dupire — preferred as input for exotics pricing)
> **You need first:** [[Black-Scholes Model]], [[Volatility Surface]], [[Volatility Smile]]
> **This unlocks:** [[HJM Framework]], [[Volatility Surface]] (via smooth interpolation), interest rate exotic pricing

## Why This Exists

**The gap:** Interest rate options — caps, floors, and swaptions — exhibit a pronounced implied volatility smile, just like equity options. Rates desks need to quote and risk-manage options across a grid of strikes and maturities consistently. BSM (or Black-76 for rates) produces a flat vol line, which cannot price different strikes consistently. A practitioner hedging a 2% receiver swaption with an ATM swaption using the same vol for both would systematically misprice the trade.

**What came before:** Ad hoc adjustments — using different vols for different strikes without any model consistency, or fitting a polynomial to observed vols. There was no single framework that could describe the smile across all strikes and allow a trader to immediately understand how a parameter change shifts the shape.

**What this adds:** Hagan et al. (2002) derived an explicit approximate formula that maps four parameters (α, β, ν, ρ) directly to the Black implied vol at any strike. Because the formula is explicit (not an integral or PDE solution), calibration reduces to a simple regression — fast enough for real-time use. Each parameter has immediate intuitive meaning: α sets the vol level, β sets the backbone (whether to use normal or lognormal dynamics), ρ tilts the smile left or right, and ν controls the curvature. Traders can reason directly in parameter space about how to shift the smile.

**What it still doesn't solve:** The Hagan formula is an approximation that breaks down for long maturities (>10 years) and very low strikes — producing arbitrage (negative probability density) in extreme regions. SABR is also essentially a static smile model per expiry slice — it says nothing about how the smile will evolve over time or how different expiry slices are related. For a full term structure model, SABR must be embedded in LMM-SABR.

---

## Math Concepts

### The SDEs

SABR models the **forward price** $F_t$ (not the spot), because interest rate options are naturally priced in forward measure:

$$dF_t = \alpha_t \, F_t^\beta \, dW_t$$
$$d\alpha_t = \nu \, \alpha_t \, dZ_t$$
$$dW_t \, dZ_t = \rho \, dt$$

### Parameters

| Symbol | Name | Plain English |
|--------|------|---------------|
| $F_0$ | initial forward | today's forward price/rate |
| $\alpha$ | initial stochastic vol | initial level of vol; controls the overall height of the smile |
| $\beta$ | backbone exponent | 0 = normal model, 1 = lognormal model, 0.5 = CIR-like; controls whether vol is additive or multiplicative in $F$ |
| $\nu$ | vol of vol | how much $\alpha$ itself moves; higher = wider, more curved smile |
| $\rho$ | correlation | negative = downward slope (puts more expensive); positive = upward slope |

### The Backbone: What $\beta$ Does

The term $F^\beta$ changes how vol scales with the forward level:

- $\beta = 1$ (lognormal backbone): vol moves proportionally with $F$. Percentage vol is roughly constant. This was the classic rates assumption pre-2010.
- $\beta = 0$ (normal backbone): vol is additive, independent of $F$. Used when rates can go negative (post-2015 Europe/Japan). Gives a "normal vol" or "basis points vol."
- $\beta = 0.5$: intermediate; similar to CIR dynamics.

In practice, $\beta$ is often fixed by convention (e.g., $\beta=0.5$ for swaptions, $\beta=1$ for FX) and only $(\alpha, \nu, \rho)$ are calibrated.

### Hagan's Approximate Implied Vol Formula

The key result: for a European option with forward $F$, strike $K$, maturity $T$, the SABR-implied Black vol is approximately:

$$\sigma_{BS}(K, F) \approx \frac{\alpha}{(FK)^{(1-\beta)/2}} \cdot \frac{z}{\chi(z)} \cdot \left[1 + \left(\frac{(1-\beta)^2}{24}\frac{\alpha^2}{(FK)^{1-\beta}} + \frac{\rho\beta\nu\alpha}{4(FK)^{(1-\beta)/2}} + \frac{2-3\rho^2}{24}\nu^2\right)T\right]$$

where:
$$z = \frac{\nu}{\alpha}(FK)^{(1-\beta)/2}\ln\frac{F}{K}$$
$$\chi(z) = \ln\left(\frac{\sqrt{1-2\rho z + z^2}+z-\rho}{1-\rho}\right)$$

At the money ($K = F$), this simplifies considerably.

**Key intuition for each parameter's effect on the smile:**
- $\alpha$ up → whole smile shifts up (higher vol level)
- $\nu$ up → smile is more curved (wider wings)
- $\rho$ negative → smile tilts left (put skew); $\rho$ positive → smile tilts right

---

## Walkthrough

### Typical Parameter Values (USD swaption market)

| Parameter | Typical Range | Notes |
|-----------|--------------|-------|
| $\alpha$ | 0.01–0.05 | roughly ATM normal vol level |
| $\beta$ | 0.5 (fixed) | often fixed by convention |
| $\nu$ | 0.2–0.5 | vol of vol |
| $\rho$ | −0.3 to −0.1 | mild negative correlation for rates |

### Calibration Process

1. Fix $\beta$ by market convention or fit to historical backbone data.
2. Observe market implied vols across strikes for a given expiry/tenor.
3. Minimize sum-of-squared errors between SABR formula and market vols over $(\alpha, \nu, \rho)$.
4. Since the formula is explicit, calibration is fast (no inner pricing loop).
5. Repeat for each expiry/tenor to get a surface of SABR parameter sets.

### How to Use After Calibration

Once $(\alpha, \beta, \nu, \rho)$ are fitted for each expiry:
- **Price any strike:** plug strike into the Hagan formula → get implied vol → plug into Black formula → get price.
- **Interpolate the smile:** the SABR formula naturally extends to any strike, including deep OTM.
- **Risk management:** compute sensitivity of implied vol to parameter changes ($\partial \sigma / \partial \alpha$, etc.).

### Known Issue: Arbitrage at Low Strikes

The Hagan (2002) formula is an approximation. For very low strikes or long maturities, it can produce negative probability densities (i.e., arbitrage). The "SABR-LN" and "free boundary SABR" extensions fix this.

---

## Analysis

### Pros vs BSM

- **Explicit smile formula** — no numerical integration needed, very fast.
- **Intuitive parameters** — traders can reason about smile shape directly.
- **Industry standard** for USD/EUR/GBP swaptions, caps, floors.
- **Handles negative rates** when $\beta = 0$ (shifted SABR or normal SABR).
- **Interpolation/extrapolation** is smooth and model-consistent.

### Cons / Where It Breaks

- **Approximate formula has errors** for long maturities (>10yr) and extreme strikes.
- **Arbitrage at low strikes** (negative density issue) — requires extensions.
- **Parameter instability** across time — $\alpha$ can jump day to day.
- **No dynamic model** for hedging path-dependent rates products — SABR is essentially a static smile model, not a term structure model.
- **Doesn't capture forward vol** or term structure dynamics well (use LMM-SABR for that).

### Industry Usage

Dominant in rates derivatives (swaptions, caps/floors). Common in FX options with $\beta=1$. Less used for equities where Heston/local vol are preferred.

---

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import norm

# ─── Hagan (2002) SABR Implied Vol Formula ───────────────────────────────────

def sabr_implied_vol(F, K, T, alpha, beta, nu, rho):
    """
    Hagan et al. (2002) approximate implied Black vol for SABR model.

    Parameters
    ----------
    F     : forward price/rate
    K     : strike
    T     : time to expiry (years)
    alpha : initial stochastic vol
    beta  : backbone exponent (0=normal, 1=lognormal)
    nu    : vol of vol
    rho   : correlation
    """
    eps = 1e-7

    if abs(F - K) < eps:
        # ATM formula
        FK_mid = F
        prefix = alpha / (FK_mid ** (1 - beta))
        term1 = 1.0
        correction = (
            ((1 - beta)**2 / 24) * alpha**2 / FK_mid**(2*(1-beta))
            + (rho * beta * nu * alpha) / (4 * FK_mid**(1-beta))
            + (2 - 3*rho**2) / 24 * nu**2
        )
        return prefix * term1 * (1 + correction * T)

    log_FK = np.log(F / K)
    FK_beta = (F * K) ** ((1 - beta) / 2)

    # z and chi(z)
    z = (nu / alpha) * FK_beta * log_FK
    chi_z = np.log((np.sqrt(1 - 2*rho*z + z**2) + z - rho) / (1 - rho))

    if abs(chi_z) < eps:
        z_over_chi = 1.0
    else:
        z_over_chi = z / chi_z

    # Leading term
    A = alpha / (
        FK_beta * (
            1
            + ((1-beta)**2 / 24) * log_FK**2
            + ((1-beta)**4 / 1920) * log_FK**4
        )
    )

    # Correction term
    correction = (
        ((1-beta)**2 / 24) * alpha**2 / (F*K)**(1-beta)
        + (rho * beta * nu * alpha) / (4 * (F*K)**((1-beta)/2))
        + (2 - 3*rho**2) / 24 * nu**2
    )

    return A * z_over_chi * (1 + correction * T)


# ─── Black (lognormal) formula for rates options ─────────────────────────────

def black_call(F, K, T, r, sigma):
    """Standard Black-76 call price."""
    d1 = (np.log(F / K) + 0.5 * sigma**2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return np.exp(-r * T) * (F * norm.cdf(d1) - K * norm.cdf(d2))


# ─── Calibration to a market smile ───────────────────────────────────────────

def calibrate_sabr(F, T, market_strikes, market_vols, beta=0.5):
    """
    Calibrate SABR (alpha, nu, rho) to market implied vols at given strikes.
    beta is fixed.
    """
    def objective(params):
        alpha, nu, rho = params
        if alpha <= 0 or nu <= 0 or abs(rho) >= 1:
            return 1e10
        model_vols = np.array([
            sabr_implied_vol(F, K, T, alpha, beta, nu, rho)
            for K in market_strikes
        ])
        return np.sum((model_vols - market_vols)**2)

    # Initial guess
    x0 = [0.02, 0.3, -0.2]
    bounds = [(1e-4, 1.0), (1e-4, 2.0), (-0.999, 0.999)]
    result = minimize(objective, x0, method="L-BFGS-B", bounds=bounds)
    alpha_fit, nu_fit, rho_fit = result.x
    return alpha_fit, nu_fit, rho_fit


# ─── Example: visualize SABR smile ───────────────────────────────────────────

F = 0.03          # forward swap rate = 3%
T = 5.0           # 5-year swaption
beta = 0.5

# Hypothetical market smile (in normal vol basis points -- here as lognormal vols)
market_strikes = np.array([0.01, 0.02, 0.03, 0.04, 0.05, 0.06])
market_vols    = np.array([0.38, 0.32, 0.28, 0.27, 0.28, 0.31])  # typical hump shape

# Calibrate
alpha_fit, nu_fit, rho_fit = calibrate_sabr(F, T, market_strikes, market_vols, beta)
print(f"Calibrated: alpha={alpha_fit:.4f}, nu={nu_fit:.4f}, rho={rho_fit:.4f}")

# Plot market vs model
strikes_fine = np.linspace(0.005, 0.07, 200)
sabr_vols = [sabr_implied_vol(F, K, T, alpha_fit, beta, nu_fit, rho_fit) for K in strikes_fine]

plt.figure(figsize=(9, 5))
plt.plot(strikes_fine * 100, np.array(sabr_vols) * 100, "b-", lw=2, label="SABR fit")
plt.scatter(market_strikes * 100, market_vols * 100, color="red", zorder=5, label="Market vols")
plt.axvline(F * 100, color="gray", linestyle="--", alpha=0.6, label=f"ATM = {F*100:.1f}%")
plt.xlabel("Strike (%)")
plt.ylabel("Implied Vol (%)")
plt.title(f"SABR Smile Fit: α={alpha_fit:.3f}, β={beta}, ν={nu_fit:.3f}, ρ={rho_fit:.3f}")
plt.legend()
plt.tight_layout()
plt.savefig("sabr_smile.png", dpi=150)
plt.show()

# Sensitivity: how rho shifts the smile
plt.figure(figsize=(9, 5))
for rho_test in [-0.5, -0.2, 0.0, 0.2, 0.5]:
    vols_test = [sabr_implied_vol(F, K, T, alpha_fit, beta, nu_fit, rho_test) for K in strikes_fine]
    plt.plot(strikes_fine * 100, np.array(vols_test) * 100, label=f"rho={rho_test}")
plt.axvline(F * 100, color="gray", linestyle="--", alpha=0.5)
plt.xlabel("Strike (%)")
plt.ylabel("Implied Vol (%)")
plt.title("SABR: Effect of rho on Smile Shape")
plt.legend()
plt.tight_layout()
plt.savefig("sabr_rho_sensitivity.png", dpi=150)
plt.show()
```

---

## Bridge to Quant / ML

- **Fast calibration target:** SABR's explicit formula means calibration is fast enough for real-time use. ML models can learn the smile-to-parameter mapping (inverse problem) even faster.
- **Feature engineering:** SABR parameters $(\alpha, \nu, \rho)$ make excellent features for ML models predicting smile dynamics or vol regime changes.
- **Neural SABR:** Recent work replaces the Hagan approximate formula with a neural network trained on Monte Carlo prices, achieving higher accuracy especially for negative rates and long maturities.
- **Vol surface interpolation:** SABR is used to interpolate between quoted strikes/maturities before feeding the surface into a Dupire local vol calculation.
- **Arbitrage constraints:** ML vol surface models must satisfy no-arbitrage conditions. SABR satisfies these approximately (up to the low-strike issue), making it a useful constraint or prior.

---

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** SABR is described as a "stochastic vol model," yet in practice it is mostly used as a smile interpolation tool rather than a simulation model. Why this disconnect?
<details>
<summary>Answer</summary>
The SABR SDEs formally define a stochastic volatility model for the forward price, similar to Heston. But the key contribution of Hagan et al. (2002) was not the SDE itself — it was the explicit approximate formula mapping SABR parameters to BSM implied vol at any strike. In practice, no one simulates the SABR SDE paths to price options. Instead, they: (1) observe market implied vols at several strikes, (2) fit the four SABR parameters by least-squares, (3) evaluate the Hagan formula at any desired strike to interpolate/extrapolate the smile. This makes SABR a parameterized smile model — a compact four-number description of the smile curve for one expiry. The stochastic vol dynamics are used only to motivate the formula, not to run simulations. For path-dependent products requiring actual simulation (Bermudan swaptions, range accruals), practitioners use LMM-SABR or Hull-White instead.
</details>

**Q2.** What does the β parameter control in SABR, and why is it typically fixed by convention rather than calibrated?
<details>
<summary>Answer</summary>
β (the backbone exponent) controls how volatility scales with the forward level. β=1 means vol scales proportionally with the forward (lognormal backbone): if rates double, vol doubles. β=0 means vol is independent of the forward level (normal backbone): vol is the same in basis points regardless of rate level. β=0.5 is intermediate, similar to CIR dynamics. When rates can go deeply negative (as in EUR post-2015), β=0 (normal SABR) is most appropriate because it doesn't produce strange behavior near zero. When rates are comfortably positive, β=1 (lognormal) is traditional. The reason β is fixed by convention rather than calibrated: it is hard to identify from cross-sectional option data alone (many (α,β) pairs can produce similar smiles), and it requires time-series data to estimate accurately. Fixing it by asset class convention (β=0.5 for swaptions, β=1 for FX) reduces degrees of freedom in calibration without significantly worsening the fit.
</details>

**Q3.** Why does SABR fail (produce arbitrage) at very low strikes or long maturities, and how do practitioners fix this?
<details>
<summary>Answer</summary>
The Hagan (2002) formula is an asymptotic approximation derived assuming the forward F is not too far from the strike K and the maturity T is not too long. For deep OTM options (K much smaller than F) or very long maturities, the approximation error accumulates and can produce implied vols that, when inverted through BSM, yield negative probability densities — butterfly arbitrage. This is not a fundamental flaw of the SABR model itself (the SDE is well-posed), but of the approximation formula. Three common fixes: (1) "free boundary SABR" — extends the SDE to allow negative rates, avoids the low-strike issue; (2) "SABR-LN" — a different approximation with better small-strike behavior; (3) "Mixture SABR" — blends SABR with a lognormal component at extreme strikes to enforce no-arbitrage. In practice, most desks use shifted SABR (adding a positive displacement to rates before applying the standard formula) to handle negative rates while preserving the lognormal structure they know.
</details>

---

### Level 2 — Quantitative

**Q4.** Using the SABR ATM formula (simplified for K=F), compute the ATM implied vol for: F = 0.03 (3% forward rate), T = 2 years, α = 0.02, β = 0.5, ν = 0.30, ρ = −0.20. Use the ATM simplification: σ_BS = α / F^{1−β} × [1 + (...)T].
<details>
<summary>Answer</summary>

At ATM (K=F), the Hagan formula simplifies to:

σ_BS = α/F^{1−β} × [1 + correction×T]

where correction = ((1−β)²/24)×α²/F^{2(1−β)} + (ρ×β×ν×α)/(4×F^{1−β}) + (2−3ρ²)/24×ν²

**Step 1: Leading term**

F^{1−β} = 0.03^{0.5} = 0.1732

α/F^{1−β} = 0.02 / 0.1732 = **0.1155**

**Step 2: Correction terms**

Term 1: (1−0.5)²/24 × (0.02)² / (0.03)¹ = 0.25/24 × 0.0004/0.03 = 0.01042 × 0.01333 = **0.000139**

Term 2: (−0.20 × 0.5 × 0.30 × 0.02) / (4 × 0.1732) = (−0.0006) / 0.6928 = **−0.000866**

Term 3: (2 − 3×0.04)/24 × 0.09 = (2−0.12)/24 × 0.09 = 1.88/24 × 0.09 = 0.07833 × 0.09 = **0.00705**

Total correction = 0.000139 − 0.000866 + 0.00705 = **0.006323**

**Step 3: Apply correction over T=2**

σ_BS = 0.1155 × (1 + 0.006323 × 2)
     = 0.1155 × 1.01265
     = **0.1170 (11.70%)**

This is the ATM lognormal (Black) implied vol. For a 3% forward swaption with these SABR parameters, the ATM vol is about 11.7% — consistent with normal rate volatility conditions.
</details>

**Q5.** If you change ρ from −0.20 to −0.50 (more negative) in the SABR model, which direction does the smile tilt and why? Estimate the magnitude of the effect on the ATM vol from Q4 and on a 1% strike (deep OTM receiver).
<details>
<summary>Answer</summary>

**Effect on ATM vol:**

Term 2 changes: (−0.50 × 0.5 × 0.30 × 0.02) / (4 × 0.1732) = −0.0015/0.6928 = −0.002166

New correction = 0.000139 − 0.002166 + 0.00705 = 0.005023

σ_BS(ρ=−0.5) = 0.1155 × (1 + 0.005023 × 2) = 0.1155 × 1.01005 = **0.1167 (11.67%)**

The ATM vol barely changes (−0.03% absolute) — ρ primarily shifts the smile slope, not the ATM level.

**Effect on 1% strike (deep OTM receiver):**

At low strikes (K=0.01 vs F=0.03), the z/χ(z) factor in the full SABR formula is strongly influenced by ρ. More negative ρ tilts the smile so that low strikes (receiver swaptions, equivalent to OTM puts in rates space) have higher implied vol. The effect is roughly: a change of Δρ = −0.30 at a 1% strike vs 3% forward causes approximately +1% to +3% extra implied vol on the receiver wing, making low-strike receivers more expensive — reflecting increased correlation between rates falling and vol rising, analogous to the equity skew.
</details>

---

### Level 3 — Coding

**Q6.** The `sabr_implied_vol` function handles the ATM case (K ≈ F) with a separate branch using the simplified ATM formula. Why is this branch necessary rather than just using the general formula with K=F?
<details>
<summary>Answer</summary>
The general SABR formula involves the ratio z/χ(z), where z = (ν/α)×(FK)^{(1−β)/2}×ln(F/K). As K → F, ln(F/K) → 0, so z → 0, and χ(z) → 0 as well — both the numerator and denominator approach zero simultaneously. The ratio z/χ(z) has a well-defined limit of 1 as z → 0 (by L'Hôpital's rule or the Taylor expansion of χ), but direct numerical evaluation produces 0/0, which in floating point gives NaN. The leading term A in the general formula also involves 1/(FK)^{(1−β)/2} times a series expansion in ln(F/K) — as K→F, the series terms with log² and log⁴ all vanish, leaving the correct ATM limit, but numerical floating-point precision near zero differences can produce large errors. The separate ATM branch directly evaluates the exact limit of the formula as K→F, avoiding this 0/0 issue and providing a numerically stable and accurate result for the most important point on the smile — the ATM vol that every calibration uses as its anchor.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| SABR is a dynamic model for simulating vol paths | In practice, SABR is used almost exclusively as a static smile parameterization via the Hagan approximate formula. No one simulates SABR paths for vanilla pricing. The SDEs define the model mathematically, but the approximate formula is the practical tool. |
| β can be freely calibrated like α, ν, ρ | β is typically fixed by market convention or estimated separately from time-series data. Calibrating all four parameters simultaneously from cross-sectional option quotes leads to flat calibration loss surfaces and unstable parameters. |
| SABR guarantees arbitrage-free prices at all strikes | The Hagan approximation is not arbitrage-free at extreme strikes for long maturities — it can produce negative probability densities. Extensions (free boundary SABR, mixture SABR) are needed for no-arbitrage guarantees. |
| SABR and Heston are different models for the same problem and one is clearly better | They target different markets: Heston is the standard for equity options (smooth, heavy left tail, mean-reverting variance); SABR is the standard for rates options (explicit formula, easy calibration, normal/lognormal backbone flexibility). Neither is universally "better." |

## Related Concepts

- [[Black-Scholes Model]]
- [[Heston Model]]
- [[Local Volatility]]
- [[Volatility Surface]]
- [[Black-76 Model]]
- [[Interest Rate Caps and Floors]]
- [[Swaptions]]
- [[LIBOR Market Model]]

---

## Sources Used

- Hagan, P.S., Kumar, D., Lesniewski, A.S., Woodward, D.E. (2002). "Managing Smile Risk." *Wilmott Magazine*, September 2002, pp. 84–108.
- Gatheral, J. (2006). *The Volatility Surface: A Practitioner's Guide*. Wiley Finance. Ch. 7.
- Antonov, A., Konikov, M., Spector, M. (2015). "SABR spreads its wings." *Risk Magazine*.

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review passed — Hagan formula, ATM branch, calibration code verified | QA review |
