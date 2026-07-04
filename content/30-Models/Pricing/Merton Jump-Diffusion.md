---
type: concept
domain: 30-Models
tags: [pricing, options, volatility, jumps]
status: math
stability: evolving
confidence: high
last_reviewed: 2026-04-18
review_interval_days: 90
sources:
  - "Merton (1976), Option pricing when underlying stock returns are discontinuous"
  - "Cont & Tankov — Financial Modelling with Jump Processes, ch.1"
created: 2026-04-18
---

> GBM plus Poisson jumps; explains the left-tail vol smile that flat diffusion cannot

> [!info] Problem Chain
> **Chain:** Pricing → Gap 5: BSM assumes constant σ — real markets show a volatility smile
> **This concept:** Solution C to Gap 5 — overlays discrete jumps onto GBM; fat tails and left skew arise naturally from the possibility of sudden crashes, not from vol dynamics
> **Alternative approaches to this gap:** [[Local Volatility]] (Solution A — deterministic σ(S,t)), [[Heston Model]] (Solution B — stochastic vol)
> **You need first:** [[Black-Scholes Model]], [[Geometric Brownian Motion]], [[Volatility Smile]]
> **This unlocks:** [[Exotic Options]] (jump risk in path-dependent products), [[Volatility Surface]] (understanding the skew premium)

## Why This Exists

**The gap:** Black-Scholes prices all options with a single constant σ, but in reality OTM put options are systematically more expensive than BSM predicts — especially for short maturities. On Black Monday (1987), the S&P 500 dropped 22% in a single day, an event GBM assigns essentially zero probability to. The market charges a premium for crash insurance that BSM cannot justify.

**What came before:** BSM with its continuous GBM paths simply cannot produce gap moves. Even with high σ, the probability of a 20% one-day move under a continuous diffusion is negligibly small. The BSM price of a deep OTM put with 1-month expiry is essentially zero, yet the market charges meaningful premium — the "crash risk premium."

**What this adds:** Merton (1976) overlays a Poisson jump process on top of GBM. Most of the time the stock follows its usual continuous drift and diffusion, but occasionally a Poisson "alarm" fires and the stock makes a sudden discrete jump drawn from a lognormal distribution. This directly models the possibility of overnight gaps and crash events. The pricing formula is a Poisson-weighted sum of BSM prices — tractable and semi-closed-form. OTM puts become materially more expensive because the tail probability of a crash within the option's life is now explicit.

**What it still doesn't solve:** Jump risk cannot be hedged away with a delta hedge — the stock teleports, and no continuous adjustment strategy can replicate this. Merton's derivation assumes jump risk is diversifiable (idiosyncratic), which does not hold for index options where jumps are systematic. In practice, jump models produce better pricing but poorer hedging than diffusion models, and the model generates a roughly symmetric smile rather than the pronounced left skew seen in equity markets.

---

## Math Concepts

### The SDE

$$\frac{dS}{S} = (\mu - \lambda\bar{k})\,dt + \sigma\,dW_t + (J-1)\,dN_t$$

The $-\lambda\bar{k}$ drift correction keeps the process risk-neutral: since jumps on average push the stock up by $\bar{k}$, the continuous part of the drift must be reduced to compensate.

### Components

| Symbol | Meaning |
|--------|---------|
| $\sigma$ | diffusion volatility (GBM component) |
| $\lambda$ | Poisson intensity — expected number of jumps per year |
| $N_t$ | Poisson process with intensity $\lambda$ |
| $J$ | jump size multiplier; $\log J \sim \mathcal{N}(\mu_J, \sigma_J^2)$ |
| $\bar{k}$ | mean excess jump: $\bar{k} = \mathbb{E}[J-1] = e^{\mu_J + \sigma_J^2/2} - 1$ |

### Jump Size Distribution

Because $\log J$ is normally distributed, $J$ is lognormal. A jump with $\mu_J = -0.1$ and $\sigma_J = 0.15$ means the average jump drops the stock by roughly 10%, with substantial dispersion around that. Negative $\mu_J$ encodes left-skewed shocks — crash risk.

### Pricing Formula (Series Expansion)

The key insight: condition on how many jumps $n$ occurred over $[0,T]$. Given $n$ jumps, the log-price is Gaussian, so the price is just a BSM call. The unconditional price is the Poisson-weighted average over all $n$:

$$C_{\text{Merton}} = \sum_{n=0}^{\infty} \frac{e^{-\lambda' T}(\lambda' T)^n}{n!} \cdot C_{\text{BSM}}(S, K, r_n, \sigma_n, T)$$

where:

$$\lambda' = \lambda(1+\bar{k}), \qquad r_n = r - \lambda\bar{k} + \frac{n\mu_J}{T} + \frac{n\sigma_J^2}{2T}, \qquad \sigma_n^2 = \sigma^2 + \frac{n\sigma_J^2}{T}$$

Each BSM call in the sum uses a risk-adjusted rate $r_n$ and a blended volatility $\sigma_n$ that absorbs the jump variance from $n$ shocks. The sum converges rapidly — in practice 20–50 terms suffice.

---

## Walkthrough

### Setup

Price a 1-month OTM put: $S=100$, $K=90$, $T=1/12$, $r=0.03$, $\sigma=0.20$.

Jump parameters: $\lambda=1$ (one jump per year on average), $\mu_J=-0.10$ (average -10% jump), $\sigma_J=0.15$.

### BSM vs. Merton

Under BSM, the 1-month put with $K=90$ is deep OTM — only 10 points below spot on a 20-vol, 1-month horizon. The BSM price is very small; the implied vol is the same flat 20% regardless of strike.

Under Merton, the same put is notably more expensive. Even though the expected number of jumps in one month is $\lambda T = 1/12 \approx 0.08$ — so most of the time no jump occurs — the tail scenario where one crash lands within the month, driving the stock to ~90 or below, gets non-trivial weight. The Poisson probability of at least one jump in a month is $1 - e^{-1/12} \approx 8\%$; conditional on a jump of $\mu_J = -0.10$, the put is now in the money.

### Implied Vol Smile

If you price a strip of calls at different strikes with the Merton formula and invert each price through BSM, you recover a non-flat implied vol curve — a smile. Specifically:

- OTM puts (low strikes) have higher implied vol — left tail is fatter.
- ATM vol is close to $\sigma = 20\%$.
- OTM calls get slightly elevated vol too — the smile is roughly symmetric around ATM (not a pure skew).

This contrasts with BSM's flat line at 20% across all strikes. The smile curvature is driven primarily by $\lambda$ and $\sigma_J$; the skew tilt (left vs. right asymmetry) is driven by the sign of $\mu_J$.

---

## Analysis

### Strengths

- Analytically tractable semi-closed-form pricing (series sum, not a full PDE or simulation).
- Directly models the tail events that BSM misses — crash risk is built in.
- Explains why OTM puts trade rich: it's not mispricing, it's jump premium.
- Parameters have economic intuition: $\lambda$ is crash frequency, $\mu_J$ is average crash severity.

### Weaknesses

- **Jump risk is unhedgeable.** You cannot replicate a jump with a delta hedge. Merton's derivation assumes jump risk is diversifiable (idiosyncratic), which does not hold for index options where jumps are systematic.
- **Hard to calibrate.** $\lambda$, $\mu_J$, $\sigma_J$ are entangled — many combinations produce similar smiles. Time-series estimation of $\lambda$ from historical data conflicts with the risk-neutral $\lambda^*$ implied by option prices.
- **Symmetric smile, not skew.** The lognormal jump size produces a roughly symmetric smile. Real equity markets show strong left skew (puts much richer than calls). Kou's double-exponential jump model (2002) improves this by allowing asymmetric up/down jump distributions.
- **Constant intensity.** $\lambda$ is fixed. Stochastic intensity models (Hawkes processes) allow volatility clustering — periods of frequent jumps followed by calm.
- **Jumps at short dates.** At very short maturities, Merton's smile collapses toward flat because the Poisson probability of a jump in a tiny interval is tiny. This also means it underprices very short-dated OTM options.

### Industry Usage

Merton is the conceptual foundation for all jump models, but is rarely used directly in production. It gives way to Lévy process models (Variance Gamma, NIG, CGMY) that generalize the jump component, and to stochastic-vol-plus-jumps hybrids like Bates (1996).

---

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, poisson
from scipy.optimize import brentq

# ─── Black-Scholes helpers ────────────────────────────────────────────────────

def bsm_call(S, K, T, r, sigma):
    if sigma <= 0 or T <= 0:
        return max(S - K * np.exp(-r * T), 0.0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def bsm_put(S, K, T, r, sigma):
    call = bsm_call(S, K, T, r, sigma)
    return call - S + K * np.exp(-r * T)  # put-call parity

def implied_vol(price, S, K, T, r, option="call", tol=1e-8):
    fn = bsm_call if option == "call" else bsm_put
    intrinsic = max(S - K * np.exp(-r * T), 0) if option == "call" else max(K * np.exp(-r * T) - S, 0)
    if price <= intrinsic + tol:
        return np.nan
    try:
        return brentq(lambda s: fn(S, K, T, r, s) - price, 1e-6, 5.0, xtol=tol)
    except Exception:
        return np.nan


# ─── Merton Jump-Diffusion Call Price ────────────────────────────────────────

def merton_call(S, K, T, r, sigma, lam, mu_J, sigma_J, N_terms=50):
    """
    European call price under Merton (1976) jump-diffusion.

    Parameters
    ----------
    S       : spot price
    K       : strike
    T       : time to expiry (years)
    r       : risk-free rate
    sigma   : diffusion volatility
    lam     : Poisson jump intensity (jumps/year)
    mu_J    : mean of log-jump size
    sigma_J : std of log-jump size
    N_terms : number of series terms (20-50 is usually enough)
    """
    k_bar = np.exp(mu_J + 0.5 * sigma_J**2) - 1.0   # E[J-1]
    lam_prime = lam * (1.0 + k_bar)                  # risk-neutral intensity

    price = 0.0
    for n in range(N_terms):
        # Poisson weight for exactly n jumps
        w = np.exp(-lam_prime * T) * (lam_prime * T)**n / np.math.factorial(n)

        # Adjusted rate and vol for n jumps
        r_n = r - lam * k_bar + (n * mu_J) / T + (n * sigma_J**2) / (2.0 * T)
        sigma_n = np.sqrt(sigma**2 + n * sigma_J**2 / T)

        price += w * bsm_call(S, K, T, r_n, sigma_n)

    return price


# ─── Monte Carlo validation ───────────────────────────────────────────────────

def merton_mc(S0, K, T, r, sigma, lam, mu_J, sigma_J, N_paths=200_000, seed=42):
    """
    Monte Carlo price of a European call under Merton jump-diffusion.
    Uses exact simulation: GBM + compound Poisson jumps.
    """
    rng = np.random.default_rng(seed)
    k_bar = np.exp(mu_J + 0.5 * sigma_J**2) - 1.0

    # Number of jumps over [0,T] for each path
    N_jumps = rng.poisson(lam * T, N_paths)

    # Continuous part: GBM with drift correction
    Z = rng.standard_normal(N_paths)
    log_S = (np.log(S0)
             + (r - lam * k_bar - 0.5 * sigma**2) * T
             + sigma * np.sqrt(T) * Z)

    # Jump part: sum of n log-normal jumps for each path
    max_jumps = N_jumps.max() if N_jumps.max() > 0 else 1
    log_jumps_all = rng.normal(mu_J, sigma_J, (N_paths, max_jumps))
    # Mask out jumps beyond each path's count
    mask = np.arange(max_jumps)[None, :] < N_jumps[:, None]
    log_S += (log_jumps_all * mask).sum(axis=1)

    S_T = np.exp(log_S)
    payoffs = np.maximum(S_T - K, 0.0)
    return np.exp(-r * T) * payoffs.mean(), payoffs.std() / np.sqrt(N_paths)


# ─── Example: compare BSM and Merton, plot implied vol smile ─────────────────

S0, r, sigma = 100.0, 0.03, 0.20
lam, mu_J, sigma_J = 1.0, -0.10, 0.15
T = 1.0  # 1-year options

# Price at ATM
merton_atm = merton_call(S0, 100, T, r, sigma, lam, mu_J, sigma_J)
bsm_atm    = bsm_call(S0, 100, T, r, sigma)
mc_price, mc_se = merton_mc(S0, 100, T, r, sigma, lam, mu_J, sigma_J)

print(f"ATM Call  — BSM: {bsm_atm:.4f}  |  Merton series: {merton_atm:.4f}  |  MC: {mc_price:.4f} ± {2*mc_se:.4f}")

# 1-month OTM put comparison (K=90, T=1/12)
T_short = 1 / 12
bsm_put_p    = bsm_put(S0, 90, T_short, r, sigma)
merton_put_p = merton_call(S0, 90, T_short, r, sigma, lam, mu_J, sigma_J)
# Convert call to put via put-call parity
merton_put_p = merton_put_p - S0 + 90 * np.exp(-r * T_short)

print(f"\n1-month OTM Put (K=90) — BSM: {bsm_put_p:.4f}  |  Merton: {merton_put_p:.4f}")

# Implied vol smile across strikes
strikes = np.linspace(70, 140, 35)
iv_bsm    = np.full(len(strikes), sigma * 100)   # flat at 20%
iv_merton = []

for K in strikes:
    price = merton_call(S0, K, T, r, sigma, lam, mu_J, sigma_J)
    iv = implied_vol(price, S0, K, T, r, option="call")
    iv_merton.append(iv * 100 if iv is not None else np.nan)

plt.figure(figsize=(9, 4))
plt.plot(strikes, iv_bsm,    "k--",  lw=1.5, label="BSM (flat 20%)")
plt.plot(strikes, iv_merton, "b-o",  lw=2,   markersize=4, label="Merton implied vol")
plt.axvline(S0, color="gray", lw=0.8, linestyle=":")
plt.title(f"Merton Jump-Diffusion: Implied Vol Smile (T=1yr, λ={lam}, μ_J={mu_J}, σ_J={sigma_J})")
plt.xlabel("Strike")
plt.ylabel("Implied Volatility (%)")
plt.legend()
plt.tight_layout()
plt.savefig("merton_smile.png", dpi=150)
plt.show()
```

---

## Bridge to Quant / ML

- **Lévy process foundation.** Merton is the prototype for the broader class of Lévy process models. Variance Gamma (VG), Normal Inverse Gaussian (NIG), and CGMY all generalize the jump component to infinite-activity processes — infinitely many tiny jumps — and are used in credit derivatives and exotic pricing.
- **Deep hedging.** Modern deep hedging papers (Buehler et al. 2019) explicitly use jump-diffusion dynamics in their simulation environment because realistic hedging strategies must account for gap risk. Jump models make the point that delta hedging is fundamentally incomplete.
- **Tail risk and vol surface.** The left-tail skew in equity vol surfaces is a direct empirical signature of crash risk. Merton's formula quantifies how much of the observed skew can be explained by jumps vs. by stochastic vol (Heston). In practice, both are needed — hybrid Bates model.
- **Credit modelling.** The firm-value approach to credit (Merton 1974) uses a jump-diffusion for the asset value to model sudden default — connecting equity option pricing to CDS spreads.
- **Parameter estimation.** Calibrating $(\lambda, \mu_J, \sigma_J)$ from options vs. from realized jumps in time-series data illustrates the risk-neutral vs. physical measure gap — a central concept in any quantitative framework.

---

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why can't BSM's constant-vol diffusion produce the deep OTM put skew that real markets show, even if you choose a very high σ?
<details>
<summary>Answer</summary>
Under BSM (lognormal distribution with fixed σ), the log-return over any period is normally distributed. Normal distributions have light tails — the probability of a 3σ or 4σ event is small but not dramatically larger than a Gaussian would imply relative to a 2σ event. Increasing σ raises the probability of all tail events proportionally. But real markets show a specific pattern: the left tail (large downside moves) is disproportionately fat compared to the right tail (large upside moves), and particularly fat for short time periods. A large σ in BSM makes the entire distribution wider symmetrically — it inflates OTM call prices alongside OTM put prices. It cannot create asymmetric tail risk. Jumps, in contrast, model the actual mechanism: discrete crash events that can gap the price 10–20% overnight, something no diffusion process can do.
</details>

**Q2.** Merton's pricing formula prices options as a Poisson-weighted sum of BSM prices. What is the intuition behind conditioning on the number of jumps n?
<details>
<summary>Answer</summary>
Given that exactly n jumps occurred in [0,T], the log-price is the sum of the continuous GBM component plus n independent lognormal jump contributions. The sum of a Gaussian and n Gaussians is still Gaussian — so given n jumps, the terminal price is lognormally distributed. This means the BSM formula applies exactly, just with adjusted parameters: r_n (the effective rate, corrected for jump drift) and σ_n (the blended vol, inflated by the variance of n jump sizes). The unconditional Merton price is the Poisson-weighted average over all possible values of n. This is elegant because it reduces the complex jump-diffusion problem to a countable mixture of analytically tractable BSM problems.
</details>

**Q3.** Why is jump risk "unhedgeable" in the same way that diffusion risk is hedgeable by delta-hedging?
<details>
<summary>Answer</summary>
Delta hedging works for diffusion because stock price changes are continuous — you can rebalance your hedge infinitesimally often to match the option's changing delta. The hedge portfolio perfectly tracks the option because both move at the same speed. A jump, by definition, is instantaneous and discontinuous. When the stock teleports from 100 to 80, your hedge portfolio (holding −Δ shares) also changes in value, but the option's value may change by a different amount (depending on its payoff profile). No amount of continuous rebalancing prevents this P&L difference, because it happens in zero time. To fully hedge jump risk, you would need to hold other options as hedging instruments (so you have a claim that also pays if the jump happens), but then you face additional basis risk and the cost of buying those options eats into the hedge.
</details>

---

### Level 2 — Quantitative

**Q4.** Set up the Merton series for n = 0 and n = 1 terms. Parameters: S = 100, K = 100, r = 3%, σ = 0.20, T = 1 year, λ = 0.5 (half a jump per year on average), μ_J = −0.10, σ_J = 0.15. Compute k̄ and λ', then compute the n=0 and n=1 BSM call components. What fraction of the total price do these two terms contribute?
<details>
<summary>Answer</summary>

**Step 1: Compute k̄ and λ'**

k̄ = exp(μ_J + σ_J²/2) − 1 = exp(−0.10 + 0.15²/2) − 1 = exp(−0.10 + 0.01125) − 1 = exp(−0.08875) − 1 = 0.9151 − 1 = **−0.0849**

λ' = λ(1 + k̄) = 0.5 × (1 − 0.0849) = 0.5 × 0.9151 = **0.4576**

**Step 2: n = 0 term (no jumps)**

Poisson weight: w₀ = e^{−λ'T}(λ'T)⁰/0! = e^{−0.4576} = **0.6329**

Adjusted parameters: r₀ = r − λk̄ = 0.03 − 0.5×(−0.0849) = 0.03 + 0.04245 = **0.07245**; σ₀ = σ = **0.20**

BSM call₀ = BSM(S=100, K=100, r=0.07245, σ=0.20, T=1)
d₁ = [0 + (0.07245 + 0.02)×1] / 0.20 = 0.09245/0.20 = 0.4623
d₂ = 0.4623 − 0.20 = 0.2623
N(0.4623) ≈ 0.678, N(0.2623) ≈ 0.604
BSM call₀ = 100×0.678 − 100×e^{−0.07245}×0.604 = 67.8 − 100×0.9301×0.604 = 67.8 − 56.18 = **\$11.62**

n=0 contribution: 0.6329 × 11.62 = **\$7.35**

**Step 3: n = 1 term (one jump)**

w₁ = e^{−0.4576} × 0.4576 / 1 = 0.6329 × 0.4576 = **0.2895**

r₁ = r − λk̄ + μ_J/T + σ_J²/(2T) = 0.07245 + (−0.10) + 0.01125 = **−0.0163**
σ₁ = √(0.04 + 0.15²/1) = √(0.04 + 0.0225) = √0.0625 = **0.25**

BSM call₁ = BSM(100, 100, r=−0.0163, σ=0.25, T=1) ≈ ~\$10.3 (ATM, lower effective rate, higher vol)

n=1 contribution ≈ 0.2895 × 10.3 ≈ **\$2.98**

Together, n=0 and n=1 contribute ≈ $7.35 + $2.98 = \$10.33 out of the full Merton price (which is ≈ \$10.80 with all terms). These two terms capture about 95% of the total price — the series converges rapidly.
</details>

**Q5.** A 1-month OTM put (K=90, T=1/12) is priced under BSM at $0.08 and under Merton (λ=1, μ_J=−0.15, σ_J=0.10, σ=0.20) at approximately $0.85. Explain in words why the Merton price is so much higher for this specific option (short-dated, deep OTM put) compared to the vanilla ATM option where the two models agree more closely.
<details>
<summary>Answer</summary>
The deep OTM 1-month put is extremely sensitive to tail events. Under BSM (continuous diffusion), the stock must move continuously from 100 to below 90 within 1 month via a series of small incremental moves — an event with extremely low probability under lognormal dynamics.

Under Merton, a single jump with mean −15% can transport the stock from 100 to below 85 in an instant. The probability of at least one jump in a month is 1 − e^{−λ/12} = 1 − e^{−1/12} ≈ 8%. Given a jump occurs with mean −15%, the stock lands around 85, well inside the money for the 90-strike put. The Merton price is ≈ 8% × (intrinsic value conditional on jump) ≈ 8% × $5 ≈ $0.40, plus additional probability from the diffusion component. The full Merton price of \$0.85 reflects both the direct jump channel and the interaction with the diffusion.

For an ATM 1-year option, both models have similar prices because the diffusion vol (20%) over 1 year generates substantial probability mass near the ATM strike regardless of jump risk. The relative importance of jumps is highest for short-dated, deep OTM options — exactly where BSM is most wrong in practice.
</details>

---

### Level 3 — Coding

**Q6.** In `merton_call`, the factorial is computed as `np.math.factorial(n)` inside the loop. For large N_terms (e.g., 50), this computes factorials of large numbers and involves big-integer arithmetic. What would be a more numerically stable approach, and why does it matter?
<details>
<summary>Answer</summary>
Computing the Poisson weight as e^{−λ'T}(λ'T)^n / n! directly with large-integer factorials risks numerical overflow for large n, and separately using a float approximation of the factorial loses precision. The numerically stable approach is to compute Poisson probabilities recursively: w₀ = e^{−λ'T}, and w_{n+1} = w_n × (λ'T)/(n+1). This recurrence is exact, avoids computing large factorials, and stays in floating-point range throughout. The code as written works for N_terms ≤ 50 because the Poisson weights for n > ~30 are typically machine-epsilon small (the mean number of jumps λ'T is usually ≤ 2–3, so weights beyond n=10 are negligible), but the recursive approach is the production-quality solution. Alternatively, `scipy.stats.poisson.pmf(n, lambda_prime * T)` computes log-pmf internally for numerical stability.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Jump-diffusion models are mainly academic — real desks use Heston | Jump-diffusion concepts underlie all serious crash risk pricing. Index vol desks explicitly think about jump risk, and hybrid models (Bates 1996 = Heston + jumps) are used in production for equity derivatives. The Merton model specifically is the foundational framework. |
| Adding jumps to the model makes it harder to calibrate | Jumps actually make calibration more targeted: λ and μ_J directly explain the short-dated OTM put skew, while σ and diffusion parameters handle the rest. The harder problem is that risk-neutral jump parameters (from option prices) often differ substantially from physical jump parameters (from historical data). |
| A large negative μ_J explains the left-skew in equity vol surfaces | Merton with lognormal jumps produces a roughly symmetric smile, not a pure skew, because the lognormal has finite variance. The left-skew arises from negative μ_J but is symmetric enough that Merton alone undersells the actual equity skew. You need asymmetric jump distributions (Kou's double-exponential) or Heston combined with jumps (Bates) for the full skew. |
| Jump risk can be hedged by dynamic delta hedging | Delta hedging cannot hedge jump risk. When a jump occurs instantaneously, the delta hedge cannot respond. Jump risk requires holding other options (or variance swaps) as hedging instruments — and those have their own costs and basis risks. |

## Related Concepts

- [[Black-Scholes Model]]
- [[Volatility Smile]]
- [[Volatility Surface]]
- [[Geometric Brownian Motion]]
- [[Exotic Options]]
- [[Implied Volatility]]

---

## Sources Used

- Merton, R.C. (1976). "Option pricing when underlying stock returns are discontinuous." *Journal of Financial Economics* 3(1–2), 125–144.
- Cont, R. & Tankov, P. (2004). *Financial Modelling with Jump Processes*. Chapman & Hall / CRC. Ch. 1.

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | initial build |
