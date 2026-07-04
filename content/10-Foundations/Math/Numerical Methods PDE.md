---
type: concept
domain: 10-Foundations
tags: [math, numerical-methods, pricing]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-18
review_interval_days: 365
sources:
  - "Hull, Options, Futures, and Other Derivatives, ch. 21"
  - "Wilmott, Paul, Howison, Dewynne, The Mathematics of Financial Derivatives, ch. 5"
created: 2026-04-18
---

> Solve the Black-Scholes PDE on a discrete grid. Three schemes: Explicit (fast but unstable), Implicit (stable but a linear solve), Crank-Nicolson (best of both). Essential for American and exotic options.

> [!info] Problem Chain
> **Chain:** Pricing → Gap 6: Many contracts have no closed-form solution
> **This concept:** Solves the Black-Scholes PDE numerically on a discrete grid — handling American early exercise, barrier options, and any payoff structure where a closed form does not exist.
> **Alternative approaches to this gap:** [[Monte Carlo Methods]] (Solution B — simulation, better for high dimensions and path-dependent payoffs); [[Binomial Tree Model]] (Solution C — discrete lattice, simpler but less efficient)
> **You need first:** [[Black-Scholes Model]], [[Ito's Lemma]], [[Risk-Neutral Measure]]
> **This unlocks:** [[American Options]], [[Exotic Options]], [[Local Volatility]] calibration

## Why This Exists

**The gap:** Black-Scholes gives a closed-form price for European vanilla options, but the vast majority of traded derivatives do not have closed forms: American options (exercisable early), barrier options (knock-in/knock-out), options under stochastic volatility models like Heston, and interest rate derivatives all require numerical solutions.

**What came before:** Closed-form formulas and binomial trees. Binomial trees are intuitive and handle early exercise, but converge slowly ($O(1/\sqrt{N})$ in the number of steps) and become unwieldy for path-dependent features or continuous barriers.

**What this adds:** A deterministic, backward-in-time algorithm that discretizes the Black-Scholes PDE over a grid of stock price × time. The Crank-Nicolson scheme is unconditionally stable and second-order accurate in both time and space — converging quadratically as the grid is refined. Critically, early exercise is handled naturally at every grid node with a single pointwise maximum: no regression, no iteration, no additional cost. For one- or two-underlying problems, FDM is the most efficient and reliable method available.

**What it still doesn't solve:** FDM suffers from the curse of dimensionality — a $d$-dimensional problem requires a grid with $M^d$ nodes, making it impractical beyond two or three underlyings. For basket options, complex path-dependent payoffs, or high-dimensional interest rate models, [[Monte Carlo Methods]] is the right tool.

---

## Math Concepts

### The Black-Scholes PDE

Under the standard BSM assumptions, the option value $V(S, t)$ satisfies:

$$\frac{\partial V}{\partial t} + rS \frac{\partial V}{\partial S} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} - rV = 0$$

with terminal condition $V(S, T) = \text{payoff}(S)$ and boundary conditions for $S \to 0$ and $S \to S_{\max}$.

### The Grid

Discretize the domain $[0, S_{\max}] \times [0, T]$:

- $M$ spatial steps: $\Delta S = S_{\max}/M$, so $S_i = i \cdot \Delta S$ for $i = 0, 1, \ldots, M$
- $N$ time steps: $\Delta t = T/N$, so $t_n = n \cdot \Delta t$ for $n = 0, 1, \ldots, N$

Let $V_i^n \approx V(S_i, t_n)$. We work *backward* from $n = N$ (expiry) to $n = 0$ (today).

### Finite Difference Approximations

**First derivative** (central difference):
$$\frac{\partial V}{\partial S} \approx \frac{V_{i+1}^n - V_{i-1}^n}{2\Delta S}$$

**Second derivative** (central difference):
$$\frac{\partial^2 V}{\partial S^2} \approx \frac{V_{i+1}^n - 2V_i^n + V_{i-1}^n}{(\Delta S)^2}$$

**Time derivative** (backward difference):
$$\frac{\partial V}{\partial t} \approx \frac{V_i^{n+1} - V_i^n}{\Delta t}$$

### Three Schemes

Let $a_i = \frac{1}{2}\Delta t(\sigma^2 i^2 - ri)$, $b_i = 1 - \Delta t(\sigma^2 i^2 + r)$, $c_i = \frac{1}{2}\Delta t(\sigma^2 i^2 + ri)$.

**1. Explicit (FTCS — Forward Time, Central Space)**

$$V_i^n = a_i V_{i-1}^{n+1} + b_i V_i^{n+1} + c_i V_{i+1}^{n+1}$$

At each step, $V^n$ is a direct linear combination of the *already known* $V^{n+1}$. No system to solve — one matrix multiply per step.

**Stability condition (CFL):** requires $b_i \geq 0$ for all $i$, which means $\Delta t \leq \frac{1}{\sigma^2 i^2 + r}$. If violated, values blow up. In practice, requires very small $\Delta t$.

**2. Implicit (BTCS — Backward Time, Central Space)**

$$-a_i V_{i-1}^n + (1 - b_i) V_i^n - c_i V_{i+1}^n = V_i^{n+1}$$

Here $V^n$ appears on the left-hand side — need to solve a tridiagonal linear system $\mathbf{A} \mathbf{V}^n = \mathbf{V}^{n+1}$ at each step.

**Unconditionally stable** — any $\Delta t$ works. But first-order accurate in time ($O(\Delta t)$).

**3. Crank-Nicolson (CN)**

Average of explicit and implicit:

$$\frac{V_i^{n+1} - V_i^n}{\Delta t} = \frac{1}{2}\left[\mathcal{L}V_i^{n+1} + \mathcal{L}V_i^n\right]$$

where $\mathcal{L}$ is the spatial differential operator. This gives:

$$\mathbf{A} \mathbf{V}^n = \mathbf{B} \mathbf{V}^{n+1}$$

where $\mathbf{A}$ and $\mathbf{B}$ are tridiagonal matrices. Solve one tridiagonal system per time step.

**Properties:** Unconditionally stable, **second-order accurate** in both time ($O(\Delta t^2)$) and space ($O(\Delta S^2)$). Standard choice in practice.

### American Option: Early Exercise

At each time step, after computing the PDE solution $V^n_{\text{PDE}}$, apply the early exercise condition:

$$V_i^n = \max\!\left(V_i^{n, \text{PDE}},\ \text{intrinsic}_i\right)$$

where $\text{intrinsic}_i = \max(K - S_i, 0)$ for a put. This is the "free boundary" condition — it converts the PDE into a linear complementarity problem, solved here by a simple pointwise maximum.

### Boundary Conditions

| Boundary | European Call | European Put | American Put |
|----------|--------------|-------------|-------------|
| $S = 0$ | $V = 0$ | $V = K e^{-r(T-t)}$ | $V = K$ |
| $S = S_{\max}$ | $V \approx S_{\max} - K e^{-r(T-t)}$ | $V \approx 0$ | $V \approx 0$ |
| $t = T$ | $\max(S - K, 0)$ | $\max(K - S, 0)$ | $\max(K - S, 0)$ |

---

## Walkthrough

### Building the Crank-Nicolson Solver Step by Step

**Step 1: Initialize the grid.**
Set $S_i = i \cdot \Delta S$ for $i = 0, \ldots, M$. Set terminal payoff $V_i^N = \max(S_i - K, 0)$ for a call.

**Step 2: Build the tridiagonal matrices $\mathbf{A}$ and $\mathbf{B}$.**
For each interior node $i = 1, \ldots, M-1$:
- $\alpha_i = \frac{1}{4}\Delta t(\sigma^2 i^2 - ri)$
- $\beta_i = -\frac{1}{2}\Delta t(\sigma^2 i^2 + r)$  
- $\gamma_i = \frac{1}{4}\Delta t(\sigma^2 i^2 + ri)$

$\mathbf{A}_{i,i-1} = -\alpha_i$, $\mathbf{A}_{i,i} = 1 - \beta_i$, $\mathbf{A}_{i,i+1} = -\gamma_i$

$\mathbf{B}_{i,i-1} = \alpha_i$, $\mathbf{B}_{i,i} = 1 + \beta_i$, $\mathbf{B}_{i,i+1} = \gamma_i$

**Step 3: March backward in time.**
For $n = N-1$ down to $0$:
  1. Compute the right-hand side: $\mathbf{rhs} = \mathbf{B} \mathbf{V}^{n+1}$
  2. Apply boundary corrections at $i=1$ and $i=M-1$
  3. Solve $\mathbf{A} \mathbf{V}^n = \mathbf{rhs}$ using the tridiagonal (Thomas) algorithm
  4. For American options: $V_i^n = \max(V_i^n, \text{intrinsic}_i)$

**Step 4: Read off the price.**
Interpolate $V_i^0$ at $S_0 = 100$ to get the option price today.

### Checking Convergence

- Halve $\Delta t$ and $\Delta S$ — the CN price should converge quadratically to the BSM price for a European call.
- For the American put, compare to the binomial tree price (reliable benchmark without a closed form).

---

## Analysis

### Comparison of Schemes

| Scheme | Stability | Accuracy (time) | Accuracy (space) | Cost per step |
|--------|-----------|-----------------|------------------|---------------|
| Explicit | Conditional (CFL) | $O(\Delta t)$ | $O(\Delta S^2)$ | $O(M)$ — no solve |
| Implicit | Unconditional | $O(\Delta t)$ | $O(\Delta S^2)$ | $O(M)$ — tridiag solve |
| Crank-Nicolson | Unconditional | $O(\Delta t^2)$ | $O(\Delta S^2)$ | $O(M)$ — tridiag solve |

For the same accuracy, CN requires far fewer time steps than Explicit. The tridiagonal solve is $O(M)$ — not expensive. **Crank-Nicolson is almost always the right choice.**

### Grid Design Considerations

- **$S_{\max}$:** typically $3\times$ to $5\times$ the strike. Too small → boundary artifacts; too large → wastes grid points far from the money.
- **Grid concentration near the strike:** use a non-uniform grid with more points near $S = K$ and $S = H$ (for barriers). Dramatically improves accuracy for a given $M$.
- **Log-transformation:** substituting $x = \ln S$ transforms the BSM PDE into a constant-coefficient PDE — much easier to work with:

$$\frac{\partial V}{\partial t} + \left(r - \frac{1}{2}\sigma^2\right)\frac{\partial V}{\partial x} + \frac{1}{2}\sigma^2 \frac{\partial^2 V}{\partial x^2} - rV = 0$$

### When FDM Beats Monte Carlo (and Vice Versa)

| Scenario | FDM | Monte Carlo |
|----------|-----|-------------|
| 1 underlying, European/American | Better | Overkill |
| 1 underlying, barrier | Good | Fine |
| 2 underlyings | Possible (2D PDE) | Good |
| 3+ underlyings | Impractical (curse of dimensionality) | Preferred |
| Path-dependent (Asian, lookback) | Hard | Natural |
| Early exercise | Natural | Hard (Longstaff-Schwartz needed) |

---

## Implementation

```python
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ─── BSM Closed Form (Benchmark) ─────────────────────────────────────────────

def bsm_call(S, K, r, sigma, T):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)

def bsm_put(S, K, r, sigma, T):
    return bsm_call(S, K, r, sigma, T) - S + K * np.exp(-r*T)


# ─── Crank-Nicolson FDM ───────────────────────────────────────────────────────

def cn_option_pricer(S0, K, r, sigma, T,
                     M=200, N=200,
                     option_type="call",
                     american=False,
                     S_max_mult=4.0):
    """
    Crank-Nicolson finite difference pricer for European or American options.

    Parameters
    ----------
    S0          : current stock price
    K           : strike
    r           : risk-free rate
    sigma       : volatility
    T           : time to expiry
    M           : number of spatial steps
    N           : number of time steps
    option_type : 'call' or 'put'
    american    : True for American early exercise
    S_max_mult  : S_max = S_max_mult * K

    Returns
    -------
    price       : option price at S0
    S_grid      : array of stock prices on the grid
    V0          : option values across S at t=0
    """
    S_max = S_max_mult * K
    dS = S_max / M
    dt = T / N
    S = np.linspace(0, S_max, M + 1)   # S_0=0, ..., S_M=S_max
    i = np.arange(0, M + 1)

    # Terminal payoff
    if option_type == "call":
        V = np.maximum(S - K, 0.0)
    else:
        V = np.maximum(K - S, 0.0)

    # Interior nodes only: i = 1, ..., M-1
    i_int = i[1:M]      # shape (M-1,)
    alpha = 0.25 * dt * (sigma**2 * i_int**2 - r * i_int)
    beta  = -0.5 * dt * (sigma**2 * i_int**2 + r)
    gamma = 0.25 * dt * (sigma**2 * i_int**2 + r * i_int)

    # Build tridiagonal matrices A and B for interior nodes
    # A @ V^n = B @ V^{n+1}  =>  V^n = A^{-1} @ (B @ V^{n+1})
    size = M - 1

    def build_tridiag(lower, diag, upper):
        mat = np.zeros((size, size))
        np.fill_diagonal(mat, diag)
        np.fill_diagonal(mat[1:], lower[1:])
        np.fill_diagonal(mat[:, 1:], upper[:-1])
        return mat

    A = build_tridiag(-alpha, 1 - beta, -gamma)
    B = build_tridiag( alpha, 1 + beta,  gamma)

    # Time-stepping (backward in time)
    for n in range(N - 1, -1, -1):
        t_current = n * dt

        # Boundary values at current time step n
        if option_type == "call":
            bc_low  = 0.0                                 # V(0, t) = 0 for call
            bc_high = S_max - K * np.exp(-r * (T - t_current))  # V(S_max, t)
        else:
            bc_low  = K * np.exp(-r * (T - t_current))   # V(0, t) = K*e^{-r*tau} for put
            bc_high = 0.0                                 # V(S_max, t) = 0 for put

        # RHS = B @ V_interior^{n+1}, plus boundary contributions.
        # CN: A @ V^n = B @ V^{n+1}. Both A and B reference boundary nodes;
        # each contributes alpha[0]*bc_low to the right-hand side.
        # Total boundary correction = 2 * alpha[0] * bc_low (one from B, one from A).
        V_int = V[1:M]
        rhs = B @ V_int
        rhs[0]  += 2 * alpha[0]  * bc_low
        rhs[-1] += 2 * gamma[-1] * bc_high

        V_new_int = np.linalg.solve(A, rhs)

        # Apply boundary conditions
        V_new = np.empty(M + 1)
        V_new[0]  = bc_low
        V_new[M]  = bc_high
        V_new[1:M] = V_new_int

        # American early exercise
        if american:
            if option_type == "call":
                intrinsic = np.maximum(S - K, 0.0)
            else:
                intrinsic = np.maximum(K - S, 0.0)
            V_new = np.maximum(V_new, intrinsic)

        V = V_new

    # Interpolate to get price at S0
    price = np.interp(S0, S, V)
    return price, S, V


# ─── Example 1: European Call — FDM vs BSM ────────────────────────────────────

S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.20, 1.0

price_fdm,  S_grid, V0  = cn_option_pricer(S0, K, r, sigma, T, M=200, N=200,
                                            option_type="call", american=False)
price_bsm = bsm_call(S0, K, r, sigma, T)
print(f"European call — FDM: {price_fdm:.4f}  BSM: {price_bsm:.4f}  Error: {abs(price_fdm - price_bsm):.5f}")


# ─── Example 2: American Put ──────────────────────────────────────────────────

price_eur_put_fdm, _, V0_ep = cn_option_pricer(S0, K, r, sigma, T, M=300, N=300,
                                                option_type="put", american=False)
price_am_put_fdm,  _, V0_ap = cn_option_pricer(S0, K, r, sigma, T, M=300, N=300,
                                                option_type="put", american=True)
price_eur_put_bsm = bsm_put(S0, K, r, sigma, T)

print(f"European put  — FDM: {price_eur_put_fdm:.4f}  BSM: {price_eur_put_bsm:.4f}")
print(f"American put  — FDM: {price_am_put_fdm:.4f}  (early exercise premium: {price_am_put_fdm - price_eur_put_fdm:.4f})")

# Plot: European vs American put value as function of S
fig, ax = plt.subplots(figsize=(10, 5))
mask = (S_grid <= 200)
ax.plot(S_grid[mask], V0_ep[mask], "b-",  lw=2, label="European put (FDM)")
ax.plot(S_grid[mask], V0_ap[mask], "r-",  lw=2, label="American put (FDM)")
ax.plot(S_grid[mask], np.maximum(K - S_grid[mask], 0), "k--", lw=1, label="Intrinsic value")
ax.axvline(S0, color="gray", lw=1, linestyle=":")
ax.set_xlim(50, 200)
ax.set_xlabel("Stock Price S")
ax.set_ylabel("Option Value")
ax.set_title("American vs European Put: FDM Crank-Nicolson\n(K=100, r=5%, σ=20%, T=1yr)")
ax.legend()
plt.tight_layout()
plt.savefig("fdm_american_put.png", dpi=150)
plt.show()


# ─── Example 3: Convergence vs Grid Size ─────────────────────────────────────

grid_sizes = [20, 40, 80, 160, 320, 640]
errors = []
for M in grid_sizes:
    price, _, _ = cn_option_pricer(S0, K, r, sigma, T, M=M, N=M,
                                   option_type="call", american=False)
    errors.append(abs(price - price_bsm))

plt.figure(figsize=(8, 4))
plt.loglog(grid_sizes, errors, "o-", color="steelblue", lw=2)
plt.xlabel("Grid size M (= N)")
plt.ylabel("|FDM - BSM| error")
plt.title("Crank-Nicolson Convergence — European Call")
plt.grid(True, which="both", alpha=0.4)
plt.tight_layout()
plt.savefig("fdm_convergence.png", dpi=150)
plt.show()

# The slope of the log-log plot should be approximately -2, confirming O(Δt², ΔS²) convergence.
```

---

## Bridge to Quant / ML

- **American option pricing in production:** Every equity derivatives desk prices American options via FDM (or the equivalent binomial tree). The Crank-Nicolson scheme in log-price space is standard. This is not academic — it is the production algorithm.
- **Barrier options:** FDM prices knock-out and knock-in barrier options by setting $V = 0$ (or the rebate value) on the barrier grid nodes at every time step. The barrier must align with a grid point for accuracy — so grid design matters. Compare with [[Exotic Options]].
- **Calibration of local vol models:** The [[Local Volatility]] surface $\sigma(S, t)$ is calibrated by running FDM with time-and-strike-varying vol — the PDE coefficients become functions of $S$ and $t$, but the scheme is structurally identical.
- **Neural network surrogates:** Training a neural network to approximate the FDM solution surface $V(S_0, K, T, \sigma)$ gives a fast proxy pricer. The FDM-generated prices serve as training data. Used in real-time risk systems.
- **Adjoint methods for Greeks:** The **adjoint (reverse-mode) differentiation** of the FDM scheme efficiently computes all Greeks with respect to model parameters — essentially backpropagation through the PDE solver. Direct parallel to reverse-mode autodiff in deep learning.
- **PDEs in ML:** The connection is deep: neural networks trained with PDE constraints (Physics-Informed Neural Networks, PINNs) can solve the Black-Scholes PDE without building a grid. The FDM is still the validation benchmark.

---

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** What makes American options harder to price than European options? How does the FDM approach handle early exercise naturally?

<details>
<summary>Answer</summary>

**The difficulty:** A European option can only be exercised at expiry $T$. Its price satisfies the Black-Scholes PDE with a fixed terminal condition — solve backward from $T$ to today with no decisions along the way.

An American option can be exercised at **any time before** $T$. This introduces a **free boundary** problem: at each moment, the holder must decide "exercise now (get intrinsic value) or keep the option alive (get continuation value)?" The optimal exercise boundary separating "exercise" from "hold" is itself unknown and must be found as part of the solution.

Mathematically, the option value satisfies: $V(S, t) \geq \text{intrinsic}(S)$ at all times — the option can never be worth less than its immediate exercise value. This converts the linear PDE into a **linear complementarity problem**.

**How FDM handles it naturally:** At each time step of the backward sweep, after solving the PDE for $V^n_{\text{PDE}}$, apply the early exercise constraint pointwise:

$$V_i^n = \max(V_i^{n,\text{PDE}},\ \text{intrinsic}(S_i))$$

This is a simple elementwise maximum — no iteration needed, no special solver. The "free boundary" is automatically captured: grid nodes where $V_i^n = \text{intrinsic}$ are the exercise region; nodes where $V_i^n > \text{intrinsic}$ are the continuation region. FDM discovers this boundary at each time step for free.

By contrast, Monte Carlo struggles with early exercise because it simulates paths forward — deciding optimally when to exercise requires knowing the continuation value, which requires simulating many future paths (Longstaff-Schwartz regression approach).

</details>

---

**Q2.** Compare Explicit, Implicit, and Crank-Nicolson FDM schemes. What does "stability" mean in this context, and why is CN the standard choice?

<details>
<summary>Answer</summary>

**Stability** means the numerical solution does not blow up as iterations proceed. An unstable scheme amplifies small errors at each step until they dominate the solution.

| Scheme | Stability | Time accuracy | Per-step cost |
|--------|-----------|--------------|---------------|
| Explicit (FTCS) | Conditional — requires CFL: $\Delta t \leq C/(\sigma^2 M^2)$ | $O(\Delta t)$ | $O(M)$ — no linear solve |
| Implicit (BTCS) | Unconditional | $O(\Delta t)$ | $O(M)$ — tridiag solve |
| Crank-Nicolson | Unconditional | $O(\Delta t^2)$ | $O(M)$ — tridiag solve |

**Explicit:** Each future value is a direct linear combination of the previous time step — no system to solve. Fast per step, but the CFL condition forces $\Delta t$ to be tiny (for $M = 200$ spatial steps, you may need $N > 10,000$ time steps). In practice, the explicit scheme requires so many time steps that it's slower overall than CN despite being cheaper per step.

**Implicit:** Solve a tridiagonal system at each step. Unconditionally stable, but only first-order in time — needs twice as many time steps as CN for the same accuracy.

**Crank-Nicolson:** Averages explicit and implicit — second-order in both time and space, unconditionally stable, costs one tridiagonal solve per step ($O(M)$ via Thomas algorithm). The same cost as implicit but 4× fewer time steps needed for the same accuracy.

**Why CN is standard:** it hits the efficiency frontier — stable, high-order, and the tridiagonal solve is fast. The only case where alternatives are preferred: payoffs with discontinuities (e.g., digital options) can cause CN oscillations — then a smoothing step or modified CN is used.

</details>

---

**Q3.** Why is FDM preferred over Monte Carlo for a single-underlying American put, but Monte Carlo is preferred for a basket option with 10 underlyings?

<details>
<summary>Answer</summary>

**Curse of dimensionality:** FDM discretizes the full state space into a grid. For a 1D problem (one underlying), the grid has $M \times N$ nodes — manageable. For $d$ underlyings, the grid has $M^d \times N$ nodes — it explodes exponentially.

For 10 underlyings: if $M = 100$ per dimension, the grid has $100^{10} = 10^{20}$ nodes — computationally impossible. FDM is fundamentally limited to $d \leq 2$ or $d \leq 3$ underlyings.

**Monte Carlo has no curse of dimensionality:** Each path independently simulates all $d$ underlyings simultaneously. Adding more underlyings adds a constant factor of computation per path — not an exponential blowup. 10 underlyings is no harder in principle than 1.

**For the American put (1D):** Monte Carlo handles early exercise clumsily — you must simulate many paths forward, then use regression (Longstaff-Schwartz) to estimate continuation values. This is complex to implement and has estimation error from the regression. FDM finds the exact free boundary (up to grid error) deterministically in one backward pass.

**Practical rule:** 1 underlying + early exercise → FDM. High dimensions or complex path-dependence → Monte Carlo. The crossover is roughly at $d = 2-3$.

</details>

---

### Level 2 — Quantitative

**Q4.** For the Explicit FDM scheme, the stability condition requires the diagonal coefficient $b_i = 1 - \Delta t(\sigma^2 i^2 + r) \geq 0$.

For $\sigma = 0.30$, $r = 0.05$, $M = 100$ spatial steps (so $i$ can be up to 100), what is the maximum allowed $\Delta t$?

<details>
<summary>Answer</summary>

The binding constraint is at the largest $i$ — the rightmost interior node $i = M - 1 \approx M = 100$ (worst case):

$$b_i = 1 - \Delta t(\sigma^2 i^2 + r) \geq 0 \implies \Delta t \leq \frac{1}{\sigma^2 i^2 + r}$$

At $i = 100$:
$$\Delta t_{\max} = \frac{1}{\sigma^2 \times 100^2 + r} = \frac{1}{0.09 \times 10000 + 0.05} = \frac{1}{900.05} \approx 0.00111 \text{ years}$$

This means $N_{\min} \approx T / 0.00111 = 900$ time steps (for $T = 1$ year).

**Compare to CN:** Crank-Nicolson is unconditionally stable and achieves $O(\Delta t^2)$ accuracy. To match Explicit's accuracy in time, CN needs far fewer steps — perhaps $N = 50$ suffices for most options. CN with $N = 50$ is much faster than Explicit with $N = 900$. For $M = 200$, Explicit would need $N \sim 3600$ — the difference is even more dramatic.

</details>

---

**Q5.** Crank-Nicolson converges at $O(\Delta t^2,\ \Delta S^2)$.

a) If you double both $M$ and $N$ (halving both $\Delta S$ and $\Delta t$), by what factor does the CN error reduce?
b) How does this compare to Monte Carlo pricing (which converges at $O(1/\sqrt{n_\text{sims}})$)?

<details>
<summary>Answer</summary>

**a)** CN error $\sim C_1(\Delta t)^2 + C_2(\Delta S)^2$. Doubling $M$ and $N$: $\Delta t \to \Delta t/2$ and $\Delta S \to \Delta S/2$.

New error $\sim C_1(\Delta t/2)^2 + C_2(\Delta S/2)^2 = \frac{1}{4}[C_1(\Delta t)^2 + C_2(\Delta S)^2]$.

The error reduces by **factor of 4** (two orders of magnitude per doubling). This is extremely fast convergence — the grid cost increases by $4\times$ (double both dimensions) and the error drops $4\times$. CN is extremely efficient.

**b)** Monte Carlo error $\sim C/\sqrt{n}$. To reduce MC error by factor 4, you need $n \to 16n$ — 16× more paths. To reduce by factor 4 is just doubling the grid for CN. MC is far less efficient for problems where FDM applies.

| Method | Error $\to$ Error/4 | Grid cost multiplier |
|--------|--------------------|--------------------|
| Crank-Nicolson | Double $M$ and $N$ | $4\times$ |
| Monte Carlo | $16\times$ simulations | $16\times$ |

For smooth 1D payoffs, CN converges quadratically while MC converges at the square root — CN is the clear winner in 1D.

</details>

---

### Level 3 — Coding

**Q6.** The implementation uses `np.linalg.solve(A, rhs)` to solve the tridiagonal system at each time step. In production, why would you replace this with a specialized banded solver, and what is the computational complexity of each?

<details>
<summary>Answer</summary>

**`np.linalg.solve` complexity:** General LU decomposition is $O(M^3)$ for an $M \times M$ matrix. For each of $N$ time steps: total cost $O(N \cdot M^3)$. For $M = N = 300$: $\sim 300 \times 27{,}000{,}000 = 8.1 \times 10^9$ flops — very slow.

**Specialized tridiagonal solver (Thomas algorithm / `scipy.linalg.solve_banded`) complexity:** A tridiagonal system can be solved in $O(M)$ flops using forward and backward substitution. For $N$ time steps: total cost $O(N \cdot M)$.

For $M = N = 300$: $\sim 300 \times 300 = 90{,}000$ flops — $10^5\times$ faster than the general solver.

**In code:**
```python
from scipy.linalg import solve_banded

# Build banded form: ab[0] = upper diag, ab[1] = main diag, ab[2] = lower diag
ab = np.zeros((3, M-1))
ab[0, 1:] = -gamma[:-1]   # upper diagonal
ab[1, :]  = np.diag(A)    # main diagonal
ab[2, :-1] = -alpha[1:]   # lower diagonal

V_new_int = solve_banded((1, 1), ab, rhs)  # O(M) per step
```

**Why `np.linalg.solve` works for the tutorial but not production:**
- Tutorial: $M = N = 200$, single option → acceptable speed.
- Production: thousands of options repriced per second, $M = N = 500+$ for Greeks accuracy. The $O(M^3)$ vs $O(M)$ difference matters enormously.

The Thomas algorithm is also numerically superior for tridiagonal systems (no pivoting needed if the matrix is diagonally dominant, which it is for the FDM system).

</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "The Explicit scheme is better because it needs no linear solve at each step" | The CFL stability condition forces such a small $\Delta t$ that Explicit typically requires far more total work than Crank-Nicolson, which uses larger time steps with unconditional stability. |
| "FDM and Monte Carlo always give the same price for the same option" | Both approximate the same mathematical answer, but with different error structures. FDM has deterministic grid error $O(\Delta t^2, \Delta S^2)$; MC has stochastic sampling error $O(1/\sqrt{n})$ plus bias from discretization. For the same compute budget, they may give different answers, and both are approximations. |
| "American options are worth the same as European options except for a simple premium formula" | There is no closed-form formula for American option prices (except the trivial case of American calls on non-dividend-paying stocks, where early exercise is never optimal). The American premium requires numerical methods (FDM, binomial tree, or Longstaff-Schwartz) for every strike and maturity. |
| "More grid points always means better accuracy" | True for spatial accuracy ($\Delta S$), but the stability condition and boundary effects also matter. A fine spatial grid near the strike paired with a coarse boundary region can introduce boundary artifacts. Grid design — not just size — determines accuracy. |

## Related Concepts

- [[Black-Scholes Model]] — the PDE being solved
- [[Monte Carlo Methods]] — the competing numerical approach; better for high dimension
- [[American Options]] — the canonical application of FDM with early exercise
- [[Exotic Options]] — barrier options use FDM with modified boundary conditions
- [[Heston Model]] — 2D PDE (S and v); FDM extends to 2D at high cost
- [[Ito's Lemma]] — derives the BSM PDE from the SDE
- [[Local Volatility]] — FDM with time- and level-varying vol coefficients

---

## Sources Used

- Hull, J.C. (2022). *Options, Futures, and Other Derivatives*, 11th ed. Ch. 21. Pearson.
- Wilmott, P., Howison, S. and Dewynne, J. (1995). *The Mathematics of Financial Derivatives*. Ch. 5. Cambridge University Press.
- Tavella, D. and Randall, C. (2000). *Pricing Financial Instruments: The Finite Difference Method*. Wiley.
- Duffy, D.J. (2006). *Finite Difference Methods in Financial Engineering*. Wiley Finance.

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | initial build |
| 2026-04-18 | Fixed Crank-Nicolson boundary correction bug: was adding boundary terms 4× due to duplicate code blocks; corrected to 2× (once from B, once from A); fixed Implicit scheme formula typo `(1 - b_i + 1)` → `(1 - b_i)` | review |
