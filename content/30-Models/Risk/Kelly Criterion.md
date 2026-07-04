---
type: concept
domain: 30-Models
tags: [risk, portfolio, sizing]
status: math
stability: stable
confidence: high
last_reviewed: 2026-04-12
review_interval_days: 365
sources:
  - "Kelly (1956), Bell System Technical Journal"
  - "Thorp (2006), The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market"
  - "MacLean, Thorp & Ziemba (2011), The Kelly Capital Growth Investment Criterion"
created: 2026-04-12
---

> [!info] Problem Chain
> **Chain:** Hedging & Risk — supporting concept (optimal position sizing)
> **This concept:** The Kelly Criterion answers "what fraction of capital should I bet to maximize long-run geometric growth?" — grounding position sizing in mathematical optimality.
> **Alternative approaches to this gap:** none
> **You need first:** [[Sharpe Ratio]], [[Value at Risk]]
> **This unlocks:** [[Markowitz Mean-Variance Optimization]], [[Risk Parity]]

## Why This Exists

**The gap:** Knowing a strategy has positive expected value is not enough — sizing determines whether you grow or go bust. Betting too little wastes the edge; betting too much causes ruin even with a winning strategy.

**What came before:** Position sizing was largely heuristic. Traders used fixed dollar amounts, fixed percentages, or intuition. There was no mathematically principled answer to "how much should I bet given my edge?"

**What this adds:** Kelly (1956) showed that maximizing expected log wealth — equivalent to maximizing the geometric growth rate — gives a unique optimal fraction $f^* = \mu/\sigma^2$. This is the fastest long-run compounding rate; any other fixed fraction either grows slower or causes eventual ruin. It directly connects signal quality (Sharpe ratio) to appropriate leverage.

**What it still doesn't solve:** Kelly is extremely sensitive to input estimates. Overestimating expected return by 20% causes significant overbetting. Full Kelly also produces high variance paths — large short-term drawdowns even when the long-run is optimal. In practice, half-Kelly or quarter-Kelly is used as a buffer against estimation error and investor psychology.

Suppose you find a biased coin that lands heads 55% of the time. You can bet on it repeatedly. You start with \$1,000. How much should you bet on each flip?

- Bet **too little** (say \$1 each time): you grow too slowly, barely beating the bank.
- Bet **too much** (say \$900 each time): a few losses wipe you out entirely, and you can never recover.
- Bet **everything each time**: a single tails wipes you out permanently — game over regardless of your edge.

There is a mathematically optimal fraction that maximizes your long-run wealth: the **Kelly fraction**. It balances aggressiveness (grow faster) with survival (don't blow up).

The key insight is counterintuitive: **maximizing expected dollar profit is not the same as maximizing long-run wealth**. If you flip 100 coins and bet 100% each time, expected value is positive ($1000 × 1.1^{100}$ if you never lose), but in reality you have a near-certain probability of ruin before that. The Kelly Criterion maximizes the *geometric* growth rate — the rate at which your account compounds — not the arithmetic expected value.

Think of it like compounding interest: 20% per year does not mean you double in 5 years if there are losing years mixed in. A -50% loss requires a +100% gain to recover. Volatility "drag" erodes geometric returns below arithmetic ones. Kelly minimizes this drag by sizing bets proportionally to the edge and inversely to the variance.

In quant finance, the Kelly Criterion is the foundation for position sizing. It answers: **given my strategy's expected return and volatility, what fraction of my capital should I allocate?**

## Math Concepts

**Discrete Kelly formula (binary bets).**

You bet fraction $f$ of your wealth on a binary outcome: win \$b per \$1 bet (net odds) with probability $p$, lose your stake with probability $q = 1 - p$.

Wealth after $N$ bets: $W_N = W_0 \cdot (1 + fb)^{N_w} \cdot (1 - f)^{N_l}$

where $N_w \approx pN$ are wins and $N_l \approx qN$ are losses.

The geometric growth rate per bet:

$$g(f) = p \ln(1 + fb) + q \ln(1 - f)$$

Maximize by taking $\frac{dg}{df} = 0$:

$$\frac{pb}{1 + fb^*} - \frac{q}{1-f^*} = 0 \implies \boxed{f^* = \frac{pb - q}{b} = \frac{bp - q}{b}}$$

This simplifies for even-odds ($b = 1$) to: $f^* = p - q = 2p - 1$.

**Continuous Kelly formula (portfolio context).**

For a continuously-rebalanced portfolio where the risky asset has expected excess return $\mu$ and standard deviation $\sigma$:

$$\boxed{f^* = \frac{\mu}{\sigma^2}}$$

This is equivalent to the Sharpe Ratio divided by $\sigma$:

$$f^* = \frac{\mu/\sigma}{\sigma} = \frac{S}{\sigma}$$

where $S = \mu/\sigma$ is the [[Sharpe Ratio]]. High Sharpe AND low vol = large Kelly fraction.

**Log-wealth maximization.** Kelly is equivalent to maximizing expected log utility:

$$f^* = \arg\max_f \, E[\ln(W_{t+1}/W_t)]$$

This objective has a specific economic meaning: it corresponds to an investor with log utility — constant relative risk aversion (CRRA) of 1. Any investor with less risk aversion (CRRA < 1) would bet *more* than Kelly; any with more risk aversion (CRRA > 1) would bet *less*.

**Growth rate vs. fraction curve.** The growth function $g(f)$ has key properties:
- $g(0) = 0$ (no bet = no growth)
- $g(f^*) = $ maximum geometric growth
- $g(f) = 0$ when $f = f_{ruin}$ (above this you expect to lose wealth long-run)
- $g(f) < 0$ when $f > f_{ruin}$ — overbetting destroys wealth in expectation

$f_{ruin} = 2f^*$ — betting double Kelly is expected to have zero growth. Betting more than double Kelly leads to long-run ruin.

**Half-Kelly.** In practice, $f = 0.5 f^*$ is common:
- Reduces variance to 25% of full Kelly (variance scales as $f^2$)
- Reduces expected long-run growth by only ~25%
- Much better Sharpe ratio for the growth process itself

This is a sensible concession to parameter uncertainty: if your estimated $\mu$ and $\sigma$ are noisy, using half of your Kelly estimate is a buffer against overconfident sizing.

**Kelly for multiple simultaneous bets.** With $K$ uncorrelated bets each with Kelly fraction $f_k^*$, you can run them simultaneously. The joint Kelly solution with correlated assets requires the full covariance matrix:

$$\mathbf{f}^* = \Sigma^{-1} \boldsymbol{\mu}$$

This is the same as the mean-variance tangency portfolio — Kelly and Markowitz optimization converge when return forecasts are reliable.

## Walkthrough

**Example 1: Coin flip.**

- Coin: $p = 0.55$ heads, $q = 0.45$ tails
- Even odds: $b = 1$ (win \$1 per \$1 bet)
- $f^* = (0.55 \times 1 - 0.45) / 1 = 0.10$

Bet **10% of wealth** each flip.

Verify: if $f = 0.50$ (bet half your wealth), the growth rate:
$$g(0.5) = 0.55 \ln(1.5) + 0.45 \ln(0.5) = 0.55(0.405) - 0.45(0.693) = 0.223 - 0.312 = -0.089$$

Negative! Betting 50% on a game you have a 55% edge on still *destroys* your wealth over time.

At $f^* = 0.10$:
$$g(0.10) = 0.55 \ln(1.10) + 0.45 \ln(0.90) = 0.55(0.0953) - 0.45(0.1054) = 0.0524 - 0.0474 = 0.0050$$

Positive: you grow at 0.50% per flip — compounding over thousands of flips.

**Example 2: Equity strategy.**

A systematic strategy has:
- Annualized expected excess return: $\mu = 12\%$
- Annualized volatility: $\sigma = 15\%$
- Sharpe Ratio: $S = 0.12 / 0.15 = 0.80$

Full Kelly fraction:
$$f^* = \frac{\mu}{\sigma^2} = \frac{0.12}{0.15^2} = \frac{0.12}{0.0225} = 5.33$$

This says to lever up 533%! This is extreme and signals that the Kelly framework is highly sensitive to the accuracy of $\mu$ and $\sigma$ estimates. A small error in $\mu$ leads to dramatic over/under-betting.

Half-Kelly: $f = 0.5 \times 5.33 = 2.67$ — still 267% leverage. In practice this is the starting point for negotiation with risk limits, not a literal instruction.

For a strategy with $\mu = 2\%$, $\sigma = 15\%$: $f^* = 0.02/0.0225 = 0.89$ — bet 89% of capital, which is more manageable.

## Analysis

**Strengths:**
- Theoretically optimal for long-run wealth maximization — no other fixed-fraction strategy outperforms it asymptotically.
- Automatically sizes down during drawdowns (fraction of a smaller bankroll is a smaller absolute bet).
- Provides a principled link between strategy quality ($\mu/\sigma$) and appropriate leverage.
- Never results in ruin if followed exactly (you can only bet a fraction of what you have, never borrow beyond $f^*$ without knowing it).

**Weaknesses:**
- Extremely sensitive to input estimates. Overestimating $\mu$ by 20% leads to significant overbetting.
- For continuous returns: requires accurate estimates of the *full* distribution, not just $\mu$ and $\sigma$.
- Kelly portfolios are highly concentrated in volatile short-term periods — path variance is large even though long-run growth is maximized.
- Assumes a fixed opportunity set — in practice, the distribution of returns changes over time.
- Log utility may not represent actual investor preferences.

**Known failure modes:**
- **Estimation error:** The single biggest practical problem. With finite data, $\hat{\mu}$ and $\hat{\sigma}$ are noisy. The Kelly formula amplifies estimation error.
- **Non-stationarity:** If the strategy's alpha decays, historical $\mu$ overestimates forward-looking $\mu$, leading to overbetting.
- **Tail risk / ruin:** The discrete formula assumes a maximum loss of the bet. If a position can gap down more than $f^*$ × portfolio (e.g., overnight gap risk), actual ruin probability is non-zero.
- **Capital constraints:** Most institutional investors cannot freely lever and delever — they face leverage limits, margin requirements, and transaction costs that prevent continuous Kelly rebalancing.

**Practical rule of thumb:**
- Full Kelly is a theoretical upper bound.
- Half-Kelly or quarter-Kelly is typical in practice.
- When uncertain about the signal, use even less.

## Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

# ── 1. Discrete Kelly for binary bets ─────────────────────────────────────
def kelly_discrete(p: float, b: float) -> float:
    """
    Kelly fraction for a binary bet.
    p = probability of winning
    b = net odds (win $b per $1 bet)
    Returns fraction of wealth to bet.
    """
    q = 1 - p
    return (b * p - q) / b

# Example: biased coin
p, b = 0.55, 1.0
f_star = kelly_discrete(p, b)
print(f"Coin flip Kelly fraction: {f_star:.2%}")

# ── 2. Growth rate as a function of bet fraction ───────────────────────────
def growth_rate(f: float, p: float, b: float) -> float:
    """Expected log growth per bet at fraction f."""
    q = 1 - p
    if f <= 0 or f >= 1:
        return -np.inf
    return p * np.log(1 + f * b) + q * np.log(1 - f)

f_grid = np.linspace(0.001, 0.999, 500)
g_values = [growth_rate(f, p, b) for f in f_grid]

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(f_grid, g_values, color='steelblue', linewidth=2)
ax.axvline(f_star,        color='red',    linestyle='--', label=f'Full Kelly: f*={f_star:.2%}')
ax.axvline(f_star * 0.5,  color='green',  linestyle='--', label=f'Half Kelly: {f_star*0.5:.2%}')
ax.axvline(f_star * 2.0,  color='orange', linestyle='--', label=f'2x Kelly (ruin zone): {f_star*2:.2%}')
ax.axhline(0, color='black', linewidth=0.8)
ax.set_xlabel('Bet Fraction f')
ax.set_ylabel('Growth Rate g(f) per bet')
ax.set_title(f'Kelly Growth Curve (p={p}, b={b})')
ax.set_ylim(-0.10, growth_rate(f_star, p, b) * 1.3)
ax.legend()
plt.tight_layout()
plt.savefig('kelly_growth_curve.png', dpi=150)
plt.show()

# ── 3. Simulation: compare full Kelly vs. half-Kelly vs. overbetting ───────
def simulate_wealth(f: float, p: float, b: float, n_bets: int = 1000,
                    n_paths: int = 200, W0: float = 1_000.0) -> np.ndarray:
    """Simulate wealth paths under fraction f."""
    outcomes = np.random.binomial(1, p, size=(n_bets, n_paths))  # 1=win, 0=lose
    multipliers = np.where(outcomes == 1, 1 + f * b, 1 - f)
    log_returns  = np.log(multipliers)
    log_wealth   = np.cumsum(log_returns, axis=0)
    return W0 * np.exp(log_wealth)

np.random.seed(42)
n_bets, n_paths = 500, 100
W_kelly     = simulate_wealth(f_star,       p, b, n_bets, n_paths)
W_half      = simulate_wealth(f_star * 0.5, p, b, n_bets, n_paths)
W_double    = simulate_wealth(f_star * 2.0, p, b, n_bets, n_paths)

fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=False)
for ax, W, label, color in zip(
    axes,
    [W_kelly, W_half, W_double],
    ['Full Kelly', 'Half Kelly', 'Double Kelly (overbetting)'],
    ['steelblue', 'green', 'red']
):
    ax.semilogy(W[:, :30], alpha=0.3, color=color, linewidth=0.8)
    ax.semilogy(np.median(W, axis=1), color='black', linewidth=2, label='Median path')
    ax.set_title(label)
    ax.set_xlabel('Bet number')
    ax.set_ylabel('Wealth ($, log scale)')
    ax.legend()
plt.tight_layout()
plt.savefig('kelly_simulation.png', dpi=150)
plt.show()

# Summary stats after n_bets
for W, label in [(W_kelly, 'Full Kelly'), (W_half, 'Half Kelly'), (W_double, 'Double Kelly')]:
    final = W[-1, :]
    print(f"{label:30s}: median=${np.median(final):>12,.0f}, mean=${np.mean(final):>12,.0f}, "
          f"P(ruin<100)={np.mean(final < 100):.2%}")

# ── 4. Continuous Kelly for portfolio returns ──────────────────────────────
def kelly_continuous(mu: float, sigma: float) -> float:
    """
    Kelly fraction for continuous returns.
    f* = mu / sigma^2
    mu, sigma in same units (e.g., both annualized).
    """
    return mu / (sigma ** 2)

strategies = [
    ("Conservative: mu=5%, sigma=10%",  0.05, 0.10),
    ("Moderate:     mu=10%, sigma=15%", 0.10, 0.15),
    ("Aggressive:   mu=15%, sigma=20%", 0.15, 0.20),
    ("High-Sharpe:  mu=20%, sigma=15%", 0.20, 0.15),
]

print("\nContinuous Kelly fractions:")
print(f"{'Strategy':<45} {'f*':>8} {'Half-Kelly':>12} {'Sharpe':>8}")
print("-" * 80)
for name, mu, sigma in strategies:
    f = kelly_continuous(mu, sigma)
    sharpe = mu / sigma
    print(f"{name:<45} {f:>8.2f} {f/2:>12.2f} {sharpe:>8.2f}")
```

## Bridge to Quant / ML

**Position sizing in systematic trading.** The Kelly fraction is the theoretical basis for position sizing in quant strategies. In practice:
- Estimate $\mu$ (expected return) and $\sigma$ (volatility) for each trade or strategy.
- Apply Kelly or fraction-of-Kelly to determine notional size.
- Scale down when signal uncertainty is high, up when conviction is high.

**Kelly in portfolio context.** The multi-asset Kelly solution $\mathbf{f}^* = \Sigma^{-1}\boldsymbol{\mu}$ is the tangency portfolio — the portfolio that maximizes the Sharpe ratio. This connects Kelly to modern portfolio theory: Kelly = Markowitz + log utility.

**ML connections:**
- **Expected value estimation:** The numerator of the Kelly formula ($\mu$) is exactly what ML forecasting models predict. A regression model that outputs expected returns feeds directly into Kelly sizing.
- **Uncertainty quantification:** Kelly sizing is highly sensitive to $\mu$ estimates. Bayesian or conformal interval estimates of $\mu$ can be used to compute a "Kelly fraction under uncertainty" — shrinking toward zero when the confidence interval on $\mu$ includes zero.
- **Reinforcement Learning:** Kelly is the theoretical RL policy for a log-utility investor. Policy gradient methods can recover Kelly-optimal sizing when trained with a log-wealth reward signal.
- **Ensemble sizing:** When running multiple ML models in ensemble, Kelly provides a principled way to size each model's contribution proportional to its estimated edge and inversely proportional to its variance.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why is maximizing expected dollar profit the wrong objective for sizing bets, and what does the Kelly Criterion maximize instead?
<details><summary>Answer</summary>Maximizing expected dollar profit ignores path dependency and ruin. A bet that has positive expected value in a single trial can have near-certain ruin over many trials if sized too large (because compounding means a -50% loss requires a +100% gain to recover). The Kelly Criterion maximizes the expected log of wealth, which is equivalent to maximizing the *geometric* growth rate — the rate at which wealth compounds over many periods. This correctly weights the multiplicative nature of compounding and implicitly penalizes variance through the concavity of the log function.</details>

**Q2.** Why does Kelly say to bet double the Kelly fraction has *zero* expected growth, and betting more than double leads to ruin in expectation?
<details><summary>Answer</summary>The growth function $g(f) = p\ln(1+fb) + q\ln(1-f)$ is a concave function of $f$ with a maximum at $f^*$. At $f = 2f^*$, symmetry around the maximum of the concave curve means the growth rate has come back down to the same value as $g(0) = 0$. Beyond $2f^*$, $g(f) < 0$, meaning the geometric growth rate is negative — wealth is expected to shrink with each bet even though the game has a positive edge. The losing bets' damage outweighs the winning bets' gains due to the asymmetry of multiplicative returns.</details>

**Q3.** The continuous Kelly formula gives $f^* = \mu/\sigma^2$. A strategy has $\mu = 10\%$ and $\sigma = 15\%$ annually. The computed Kelly fraction is 4.44 (444% leverage). Why would a practitioner never actually use this number directly?
<details><summary>Answer</summary>Four reasons: (1) **Estimation error** — $\mu$ and $\sigma$ are estimated from noisy data; a 20% upward bias in $\hat{\mu}$ produces catastrophic overbetting. (2) **Non-stationarity** — the strategy's alpha may be decaying; historical $\mu$ overestimates forward $\mu$. (3) **Tail risk** — the formula assumes the maximum loss is bounded by the bet; in reality, overnight gaps or illiquidity can cause losses exceeding the entire position. (4) **Capital constraints** — most institutions have leverage limits, margin requirements, and risk committees that prevent 4× leverage. In practice, half-Kelly or quarter-Kelly is used as a starting point.</details>

---

### Level 2 — Quantitative

**Q4.** You have a strategy with annualized $\mu = 8\%$ and annualized $\sigma = 12\%$. (a) Compute the full Kelly fraction. (b) Compute the half-Kelly fraction. (c) If you use half-Kelly and start with \$1,000,000, what is the notional position size? (d) How does the Sharpe Ratio connect to the Kelly fraction?
<details><summary>Answer</summary>

(a) Full Kelly: $f^* = \mu/\sigma^2 = 0.08 / 0.12^2 = 0.08 / 0.0144 = \mathbf{5.56}$ (556% leverage)

(b) Half-Kelly: $f = 0.5 \times 5.56 = \mathbf{2.78}$ (278% leverage)

(c) Notional position: $2.78 \times \$1{,}000{,}000 = \mathbf{\$2{,}780{,}000}$

(d) Connection: $f^* = \mu/\sigma^2 = (\mu/\sigma)/\sigma = S/\sigma$ where $S = \mu/\sigma$ is the Sharpe Ratio. High Sharpe and low vol both increase the Kelly fraction — they are not independent. A strategy with Sharpe = 1.0 and $\sigma = 10\%$ has $f^* = 10$; same Sharpe with $\sigma = 20\%$ has $f^* = 5$. Lower vol warrants more leverage even at the same Sharpe.</details>

**Q5.** A coin pays \$1.50 per \$1 bet (net odds $b = 1.5$) with probability $p = 0.60$. (a) Compute the Kelly fraction. (b) Compute the growth rate at the Kelly fraction. (c) Compute the growth rate at $f = 0.5$ (betting half your wealth). Which is positive?
<details><summary>Answer</summary>

(a) Kelly fraction: $f^* = (bp - q)/b = (1.5 \times 0.60 - 0.40)/1.5 = (0.90 - 0.40)/1.5 = 0.50/1.5 = \mathbf{0.333}$ (bet 33.3%)

(b) Growth rate at $f^* = 0.333$:
$$g(0.333) = 0.60 \ln(1 + 1.5 \times 0.333) + 0.40 \ln(1 - 0.333)$$
$$= 0.60 \ln(1.50) + 0.40 \ln(0.667) = 0.60(0.405) + 0.40(-0.405) = 0.243 - 0.162 = \mathbf{0.081}$$
Positive: 8.1% growth per bet.

(c) Growth rate at $f = 0.5$ (overbetting):
$$g(0.5) = 0.60 \ln(1.75) + 0.40 \ln(0.50) = 0.60(0.560) + 0.40(-0.693) = 0.336 - 0.277 = \mathbf{0.059}$$
Also positive (0.5 < 2f* = 0.667), but lower than Kelly: 5.9% vs 8.1%. Once $f > 2f^* = 0.667$, the growth rate turns negative.</details>

---

### Level 3 — Coding

**Q6.** The simulation code compares Full Kelly, Half Kelly, and Double Kelly by running 500 bets on 100 paths each. The Double Kelly paths frequently approach \$0. Explain why `np.median(final)` is a more meaningful statistic than `np.mean(final)` for evaluating overbetting strategies, and describe a modification to the simulation that would make the Double Kelly ruin probability even more visible.
<details><summary>Answer</summary>

The median is more meaningful because Kelly wealth is log-normally distributed — the distribution is right-skewed with a few extremely large wins and many paths that collapsed toward zero. The mean is dominated by the rare jackpot paths, giving an optimistic picture. The median represents the experience of the typical investor following the strategy (50th percentile path). For Double Kelly: the median declines while the mean might still be positive due to a few explosive outliers.

To make ruin more visible, add:
```python
# Track how many paths fell below 10% of starting wealth at any point
ruin_pct = np.mean(np.min(W_double, axis=0) < 100)  # starting wealth 1000, ruin at 100
print(f"Double Kelly ruin rate: {ruin_pct:.1%}")
```
Or plot the fraction of paths still above the starting wealth as a function of bet number — this shows the "survival curve" and makes the decay of Double Kelly dramatically visible vs. Full and Half Kelly.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Kelly maximizes expected return | Kelly maximizes geometric growth rate (log utility), not arithmetic expected return. Strategies that maximize expected value often have lower geometric growth due to variance drag. |
| Full Kelly is the "correct" bet size | Full Kelly is theoretically optimal only with perfectly known parameters. With estimation error, it causes overbetting. Half-Kelly is often better in practice. |
| Kelly never causes ruin | Kelly can only guarantee no ruin if losses are bounded by $f^*$ of the portfolio. Gap risk (overnight crashes > $f^*$) can cause ruin even with Kelly sizing. |
| Higher Sharpe always means bet more Kelly | True in formula, but higher Sharpe from noisy estimates (overfitting) leads to overbetting. The Kelly formula is only as good as the inputs. |

## Related Concepts

- [[Sharpe Ratio]] — appears directly in the Kelly formula: $f^* = S/\sigma$
- [[Maximum Drawdown]] — Kelly sizing does not directly control drawdowns; in practice MaxDD constraints modify Kelly allocations
- [[Factor Models]] — provides covariance estimates needed for multi-asset Kelly
- [[Value at Risk]] — can be used as a constraint that caps Kelly fraction to limit tail risk

## Sources Used

- Kelly, J. L. (1956). A new interpretation of information rate. *Bell System Technical Journal*, 35(4), 917-926
- Thorp, E. O. (2006). The Kelly criterion in blackjack, sports betting, and the stock market. In *Handbook of Asset and Liability Management*, North-Holland
- MacLean, L. C., Thorp, E. O., & Ziemba, W. T. (2011). *The Kelly Capital Growth Investment Criterion*. World Scientific

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-12 | Note created | bootstrap |
| 2026-04-12 | Full content written | initial build |
| 2026-04-11 | QA review: no issues found | quality review |
