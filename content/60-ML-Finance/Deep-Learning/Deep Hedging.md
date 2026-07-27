---
type: concept
domain: 60-ML-Finance
tags: [machine-learning, deep-learning, derivatives, risk]
status: emerging
stability: emerging
confidence: medium
last_reviewed: 2026-07-26
review_interval_days: 180
sources:
  - "Buehler, Gonon, Teichmann, Wood (2019) — Deep Hedging"
  - "What Does Deep Hedging Actually Learn? Delta Corrections, Regime Fragility, and Symbolic Distillation"
  - "Bridging Stochastic Control and Deep Hedging: Structural Priors for No-Transaction Band Networks"
created: 2026-07-26
---

> [!info] Problem Chain
> **Chain:** Pricing → Gap: BSM's continuous-trading, zero-transaction-cost delta hedge is not implementable in real markets
> **This concept:** Trains a neural network end-to-end to output a hedging policy that directly minimizes a convex risk measure (e.g. CVaR) of terminal hedged P&L under realistic frictions, rather than deriving a hedge ratio from a closed-form pricing PDE
> **Alternative approaches to this gap:** Leland's transaction-cost-adjusted volatility (a classical closed-form fix — inflate σ in the BSM delta to pre-pay for expected trading costs, but only handles proportional costs and stays within the BSM model class), [[Heston Model]] and other stochastic-vol models (address model misspecification but not transaction costs or discrete rebalancing)
> **You need first:** [[Black-Scholes Model]], [[Delta Hedging]], [[Option Greeks]]
> **This unlocks:** risk-aware execution policies, model-free hedging

## Why This Exists

**The gap:** [[Delta Hedging]] gives an exact, provably optimal hedge ratio — but only under BSM's assumptions of continuous trading, zero transaction costs, and known constant volatility. None of these hold in a real market. Every real hedger rebalances at discrete times, pays the bid-ask spread and market impact on every trade, and does not know the "true" volatility or even the true price process. The BSM delta is the right answer to the wrong question.

**What came before:** The classical response was to patch the BSM machinery rather than replace it: Leland's volatility adjustment inflates σ to account for expected transaction costs in a proportional-cost model; Whalley-Wilmott and Davis-Panas-Zariphopoulou solve a stochastic-control problem (a Hamilton-Jacobi-Bellman quasi-variational inequality) under CARA utility, producing a "no-transaction band" around the BSM delta — trade only when delta drifts outside the band. These are principled, but each is derived for one specific friction model and one specific utility function, solved by hand for that case. Add jump risk, stochastic vol, and nonlinear price impact simultaneously, and the HJBQVI becomes intractable.

**What this adds:** Buehler, Gonon, Teichmann, and Wood (2019) reframed hedging as a direct optimization problem: parameterize the entire hedging strategy as a neural network $\delta_\theta$ that maps observable market state to a position, simulate many paths of the market (under any model, or even historical data), compute the resulting hedged P&L path-by-path including realistic frictions, and train $\theta$ by gradient descent to minimize a convex risk measure of the terminal P&L. No PDE is derived and no closed-form hedge ratio is assumed. The network discovers whatever hedging rule minimizes risk given the frictions and dynamics it is shown — frictionless GBM, proportional costs, stochastic volatility, jumps, or a mix, without a new derivation for each case.

**What it still doesn't solve:** grounded in "What Does Deep Hedging Actually Learn?", trained deep hedging policies exhibit **regime fragility** — a network trained by walk-forward simulation on S&P 500 options from 2015 onward learns a systematic *delta haircut* (underhedging relative to BSM) that improves reward and downside variance in calm and moderately volatile years, but this same haircut produces losses in adverse daily states during 2022 and can raise ordinary variance in 2023 when option P&L is spot-dominated and the spot–implied-vol co-movement the policy relies on is unusually weak. Deep hedges are also comparatively opaque relative to a one-line BSM delta formula — a genuine cost in an industry that requires auditable risk models. Structural-prior architectures (below) partially address interpretability but do not eliminate the regime-dependence of what the network has learned.

## Math Concepts

**Setup.** Let $S_t$ be the underlying price process observed at discrete times $t_0 < t_1 < \dots < t_n = T$, and let $Z$ be the (possibly path-dependent) payoff of the derivative being hedged, e.g. $Z = \max(S_T - K, 0)$ for a European call. A hedging strategy is a sequence of positions $\delta_{t_i}$ in the underlying, chosen using only information available at $t_i$.

**Terminal wealth.** Starting from an initial hedge price $p_0$ (or given, since deep hedging can also be used to derive an indifference price), the accumulated trading P&L under strategy $\delta$ is

$$\text{PL}_T(\delta) = \sum_{i=0}^{n-1} \delta_{t_i}\,(S_{t_{i+1}} - S_{t_i}) - \underbrace{\sum_{i=0}^{n-1} c\big(\delta_{t_{i+1}} - \delta_{t_i}\big)}_{\text{transaction costs}}$$

where $c(\cdot)$ is a cost function — commonly proportional, $c(\Delta\delta) = \kappa\, S_{t_i}\,|\Delta\delta|$, for spread $\kappa$. The hedged terminal wealth (what the hedger actually ends up with) is

$$Z_T(\delta) = -Z + \text{PL}_T(\delta)$$

i.e. the option liability offset by the hedge's trading gains net of costs. (Sign conventions vary in the literature; some papers define $Z_T = p_0 + \text{PL}_T(\delta) - Z$ to fold in the option premium received.)

**The training objective.** Deep hedging chooses the strategy to minimize a **convex, monotone risk measure** $\rho$ of the hedged loss $-Z_T(\delta)$:

$$\min_{\theta} \; \rho\big(-Z_T(\delta_\theta)\big)$$

$\rho$ must be convex so the optimization is well-posed and so diversification (more hedging instruments) can never increase risk; monotone so that a uniformly worse outcome is never preferred. Buehler et al. use **coherent risk measures** in the sense of Artzner et al., of which the workhorse choice is **CVaR** (Conditional Value-at-Risk, also called Expected Shortfall).

**CVaR at level $\alpha$** of a loss $L = -Z_T(\delta)$ is the expected loss conditional on being in the worst $\alpha$-tail:

$$\text{CVaR}_\alpha(L) = \inf_{w \in \mathbb{R}} \left\{ w + \frac{1}{\alpha}\,\mathbb{E}\big[(L - w)^+\big] \right\}$$

This Rockafellar-Uryasev form is what makes CVaR trainable by gradient descent: $w$ becomes an extra learnable scalar (effectively an estimate of the $(1-\alpha)$-quantile / VaR), and the whole expression is convex and subdifferentiable in both $w$ and the strategy parameters, so it drops directly into a stochastic-gradient training loop alongside $\theta$.

**Policy parameterization.** $\delta_\theta$ is a neural network — typically a small MLP or an LSTM/recurrent architecture for path dependence — whose inputs at each time step are the observable market state: current spot $S_{t_i}$, time-to-expiry $T - t_i$, the network's own previous position $\delta_{t_{i-1}}$ (so it can account for its own transaction costs), and optionally realized/implied volatility or other state variables. The same network (shared weights) is applied at every time step, so training over many simulated paths effectively learns *one* function of state that plays the role BSM delta plays, but is not constrained to look like $N(d_1)$.

## Walkthrough

Concretely, one epoch of deep-hedging training for a short 30-day ATM call on a stock with $S_0 = 100$, $\sigma = 20\%$, proportional cost $\kappa = 5\text{bp}$, rebalanced daily, looks like:

1. **Simulate a batch of paths.** Draw, say, 100,000 independent 30-step GBM paths $S_{t_0}, \dots, S_{t_{30}}$ (or paths from a richer model — Heston, a jump-diffusion, or bootstrapped historical returns, per Buehler et al.'s point that the method is model-agnostic).
2. **Forward pass.** For each path, at each step feed $(S_{t_i}/S_0,\ (T-t_i)/T,\ \delta_{t_{i-1}})$ into the network to get $\delta_{t_i}$. Accumulate the trading P&L $\delta_{t_i}(S_{t_{i+1}} - S_{t_i})$ and subtract the cost $\kappa\,S_{t_i}|\delta_{t_i} - \delta_{t_{i-1}}|$ at each rebalance.
3. **Compute terminal wealth.** At $t_{30}$, subtract the option payoff $\max(S_{30}-K,0)$ to get $Z_T$ for each of the 100,000 paths — a distribution of hedged P&L outcomes, e.g. mean near 0, with a left tail representing paths where large moves and costs outpaced the hedge.
4. **Compute the risk measure.** Plug the empirical distribution of $-Z_T$ into the CVaR$_{0.95}$ formula above (average of the worst 5% of the 100,000 losses, via the Rockafellar-Uryasev auxiliary variable $w$).
5. **Backpropagate.** Because every step — the network forward passes, the P&L accumulation, and the CVaR estimator — is differentiable, gradients of CVaR with respect to $\theta$ (and $w$) flow back through all 30 time steps. An optimizer (Adam) takes a gradient step.
6. **Repeat** for thousands of epochs with fresh simulated batches, annealing toward a $\delta_\theta$ that minimizes tail risk of the hedged position under the assumed frictions and price dynamics.

At convergence, evaluating $\delta_\theta(S_t, T-t, \delta_{t^-})$ at a given state plays the same role as evaluating the BSM $\Delta = N(d_1)$ formula — except it was learned from simulated P&L outcomes rather than derived from a PDE, and it has implicitly absorbed the transaction-cost structure the BSM delta ignores.

## Analysis

**Does it recover BSM delta in the frictionless limit?** Yes, and this is the correct sanity check for any deep hedging implementation: if trained with zero transaction costs against GBM paths and a quadratic (or CVaR-at-high-confidence) risk measure, $\delta_\theta$ converges to the classical BSM delta almost everywhere, since delta hedging is the variance-minimizing (and, under GBM, replicating) strategy in that limit. Deep hedging is a strict generalization, not a replacement — BSM delta hedging is the special case of the deep hedging objective when frictions vanish and the model is GBM.

**What delta correction does it learn under frictions?** "What Does Deep Hedging Actually Learn?" trains TD3 (a reinforcement-learning actor-critic algorithm) agents against a local downside-shortfall reward on real S&P 500 index options, walk-forward from 2015–2023, and compares them against a daily-rebalanced BSM delta hedge on the same episodes. The consistent finding is that the learned policy applies a **systematic delta haircut** — it holds a smaller position than BSM delta prescribes. The paper explains this haircut via **spot–implied-volatility co-movement**: because spot and implied vol are empirically negatively correlated (spot down → IV up, and vice versa), an option's total P&L sensitivity to a spot move is not just its BSM delta but also picks up a vega contribution through this co-movement — closely related to the classical "minimum-variance delta" adjustment used by practitioners. The learned haircut partially internalizes this cross-effect that the BSM delta, computed under constant vol, cannot see. This correction usually improves accumulated reward and terminal downside variance relative to plain BSM hedging.

**Regime fragility.** The same paper is explicit that this advantage is not stable across regimes: 2022 (a year of sharp, adverse, high-vol daily moves) exposes losses from the underhedged policy in exactly the states where the spot–vol co-movement broke down or reversed; 2023 shows that underhedging can *increase* ordinary variance, not just downside variance, when option P&L becomes spot-dominated and the volatility channel the policy leans on is weak. In other words, the network learned a correction that is correlated with a specific historical relationship between spot and vol, not a universally optimal hedge — and it degrades when that relationship shifts. The paper further distills the learned neural policies into compact symbolic formulas via symbolic regression; these formulas retain much of the reward/CVaR advantage over BSM out-of-sample (and are auditable, unlike the raw network), but they inherit the same regime fragility, confirming the fragility is a property of *what was learned*, not an artifact of the network's black-box representation.

**Structural priors for robustness and interpretability.** "Bridging Stochastic Control and Deep Hedging" tackles a complementary weakness — that an unconstrained network trained under proportional transaction costs must rediscover, from scratch, the qualitative shape that stochastic control theory already proves is optimal: a **no-transaction band** around a central hedge, inside which the hedger should not trade at all (Davis et al. 1993's CARA-utility HJBQVI, with the Whalley-Wilmott asymptotic formula giving a closed-form approximation to the band width under small costs). The paper builds on Imaki et al.'s (2023) No-Transaction Band Network and proposes two variants: **NTBN-Delta**, which makes the delta-centering of the band explicit in the architecture, and **WW-NTBN**, which bakes the Whalley-Wilmott formula in as a *structural prior* on the band's width and replaces the network's hard clamp (no trading inside the band) with a differentiable soft clamp. Their experiments find WW-NTBN converges faster during training, matches the stochastic-control-derived no-transaction bands more closely than an unconstrained network, and generalizes better across transaction-cost regimes it wasn't explicitly trained on. They also show, using both frameworks, that a bull call spread's price loses linearity in the transaction-cost regime — the price of the two-leg spread is no longer simply the difference of the two single-leg option prices, an effect neither BSM nor a naive additive hedging argument captures. Together with the regime-fragility findings above, this frames the honest tradeoff: **unconstrained deep hedging is maximally flexible but can overfit to sample-period relationships (spot–vol co-movement in one historical regime) and is hard to audit; injecting classical stochastic-control structure (no-transaction bands, Whalley-Wilmott priors) sacrifices some flexibility for faster convergence, closer agreement with provably optimal control-theoretic solutions, and better cross-regime generalization.**

## Implementation

```python
import torch
import torch.nn as nn

class HedgePolicy(nn.Module):
    """Maps (spot, time-to-expiry, prev position) -> new hedge ratio."""
    def __init__(self, hidden=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, 1),
        )

    def forward(self, spot, tau, prev_delta):
        x = torch.stack([spot, tau, prev_delta], dim=-1)
        return self.net(x).squeeze(-1)


def simulate_gbm_paths(n_paths, n_steps, S0=100.0, mu=0.0, sigma=0.20, T=30/252):
    dt = T / n_steps
    Z = torch.randn(n_paths, n_steps)
    log_ret = (mu - 0.5 * sigma**2) * dt + sigma * dt**0.5 * Z
    log_S = torch.log(torch.tensor(S0)) + torch.cumsum(log_ret, dim=1)
    S = torch.cat([torch.full((n_paths, 1), float(S0)), torch.exp(log_S)], dim=1)
    return S  # (n_paths, n_steps + 1)


def hedged_terminal_pl(policy, S, K, cost_bp, T=30/252):
    n_paths, n_pts = S.shape
    n_steps = n_pts - 1
    dt = T / n_steps
    prev_delta = torch.zeros(n_paths)
    pl = torch.zeros(n_paths)
    for i in range(n_steps):
        tau = torch.full((n_paths,), (n_steps - i) * dt)
        delta = policy(S[:, i] / K, tau / T, prev_delta)
        trade_cost = cost_bp * S[:, i] * (delta - prev_delta).abs()
        pl = pl + delta * (S[:, i + 1] - S[:, i]) - trade_cost
        prev_delta = delta
    payoff = torch.clamp(S[:, -1] - K, min=0.0)
    return pl - payoff  # terminal hedged wealth Z_T (short one call)


def cvar_loss(losses, alpha=0.95):
    """Rockafellar-Uryasev CVaR of `losses`, with w as a free learnable scalar."""
    w = torch.quantile(losses.detach(), alpha)  # VaR estimate, used as w
    return w + torch.clamp(losses - w, min=0.0).mean() / (1 - alpha)


policy = HedgePolicy()
optimizer = torch.optim.Adam(policy.parameters(), lr=1e-3)

for epoch in range(2000):
    S = simulate_gbm_paths(n_paths=4096, n_steps=30)
    Z_T = hedged_terminal_pl(policy, S, K=100.0, cost_bp=0.0005)
    loss = cvar_loss(-Z_T, alpha=0.95)  # minimize CVaR of the *loss* -Z_T
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

This sketch omits the free scalar $w$ as a true learnable parameter (using the empirical quantile instead, a common simplification) and any GPU batching/scheduling detail, but captures the structure: simulate → roll the policy forward through time accumulating cost-adjusted P&L → score the terminal distribution with a convex risk measure → backprop through the whole path.

## Bridge to Quant / ML

- Deep hedging is naturally read as a special case of **reinforcement learning**: the market state is the RL state, the hedge position is the action, and the negative risk measure of terminal P&L is the (delayed, episodic) reward — see [[Reinforcement Learning Trading]]. The RL framing is literal in "What Does Deep Hedging Actually Learn?", which trains hedging policies with TD3, an off-policy actor-critic algorithm from continuous-control RL, rather than the direct supervised-style backprop-through-simulation of the original Buehler et al. paper — both are legitimate ways to solve the same risk-minimization objective, differing in whether the environment is differentiable (backprop through simulation) or treated as a black box (RL/policy-gradient).
- The **risk-sensitive objective** (CVaR of terminal wealth rather than expected return) distinguishes deep hedging from most RL-for-trading work, which typically maximizes expected cumulative reward; deep hedging's convex-risk-measure objective is closer to risk-sensitive/robust RL and to distributional RL, which model the full return distribution rather than its mean.
- Symbolic distillation of the trained network (per the regime-fragility paper) is an instance of the broader ML-finance pattern of extracting an auditable, low-dimensional surrogate from an opaque model for deployment in regulated environments.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** In what precise sense is BSM delta hedging a "special case" of deep hedging rather than a competing approach?
<details>
<summary>Answer</summary>
Deep hedging is defined as minimizing a convex risk measure of terminal hedged P&L over a class of strategies parameterized by a neural network. If you set transaction costs to zero, assume the underlying follows GBM, and use a risk measure whose minimizer coincides with variance minimization (or you take the risk measure's confidence level to a limit where it behaves like variance), the risk-minimizing strategy in that constrained problem is exactly the BSM delta — because delta hedging is the (continuous-time) variance-minimizing, and in fact replicating, strategy under GBM with no frictions. So BSM delta isn't a different technique; it's the specific point in deep hedging's strategy space that the training procedure converges to once you strip out the frictions and model richness that motivated deep hedging in the first place. Any deep hedging implementation that doesn't approximately recover BSM delta in this limit likely has a bug.
</details>

**Q2.** Why does CVaR (rather than plain variance) show up as the standard risk measure in the deep hedging objective, and what makes it compatible with gradient-based training?
<details>
<summary>Answer</summary>
Variance penalizes upside and downside deviations symmetrically, which is the wrong objective for a hedger who cares about tail losses, not about occasionally making more money than expected. CVaR (Expected Shortfall) is a coherent, convex risk measure that focuses specifically on the average loss in the worst α-fraction of outcomes, which matches what risk managers actually care about (and is used in regulatory capital calculations). It's compatible with gradient training because of the Rockafellar-Uryasev representation, which rewrites CVaR as a minimization over an auxiliary scalar w of a simple expression involving a hinge-like function (L − w)⁺. That expression is convex and subdifferentiable everywhere, so it can be optimized jointly with the network weights by ordinary stochastic gradient descent — no need for order statistics or sorting inside the computational graph beyond estimating the quantile w.
</details>

**Q3.** "What Does Deep Hedging Actually Learn?" finds that RL-trained hedging agents apply a systematic delta haircut versus BSM. Why does this improve performance in most years but hurt in 2022?
<details>
<summary>Answer</summary>
The haircut is explained by empirical spot–implied-volatility co-movement: because IV tends to rise when spot falls (and vice versa), the *total* sensitivity of an option's value to a spot move is not just its BSM delta but also includes an indirect vega effect transmitted through that co-movement — a real, tradeable relationship that BSM's constant-vol assumption cannot represent. Underhedging relative to pure BSM delta partially captures this second-order effect, and it pays off in years where the historical spot-vol relationship holds. But the relationship is empirical, not structural — it can weaken or invert in stressed regimes. In 2022, adverse daily states broke the relationship the policy had learned to lean on, so the same haircut that helped in calmer years produced losses. The network learned a regularity in its training data, not a law of markets, and it degraded exactly when that regularity failed.
</details>

---

### Level 2 — Quantitative

**Q4.** A deep hedging network trained on 100,000 simulated terminal P&L outcomes for a short position produces losses $L_i = -Z_{T,i}$ with the worst 5,000 (the 5% tail) averaging a loss of \$12.40, and the 95th-percentile loss (VaR at 95%) is \$8.10. Using the Rockafellar-Uryasev form, confirm this is consistent, and state what CVaR$_{0.95}$ equals.
<details>
<summary>Answer</summary>
By definition, CVaR at level α is the average loss conditional on being in the worst α-tail — here the worst 5% (5,000 of 100,000 paths). That average is given directly as \$12.40, so CVaR$_{0.95}(L) = \$12.40$. The VaR (the α-quantile itself, \$8.10) plays the role of $w$ in the Rockafellar-Uryasev formula: $w + \frac{1}{\alpha}\mathbb{E}[(L-w)^+]$. Since only losses in the worst 5% exceed $w = 8.10$ by construction (VaR is the boundary of the tail), $\mathbb{E}[(L-w)^+]$ averaged over *all* 100,000 paths equals $0.05 \times (12.40 - 8.10) = 0.05 \times 4.30 = 0.215$. Plugging in: $w + \frac{1}{0.05}\times 0.215 = 8.10 + 4.30 = 12.40$ — consistent with the direct tail-average definition. CVaR$_{0.95} = \$12.40$, and it is (as required) always $\geq$ VaR$_{0.95} = \$8.10$.
</details>

**Q5.** A deep hedging policy for a short call is found to hold, at a given state, a position of $\delta_\theta = 0.42$ where the contemporaneous BSM delta is $\Delta_{BSM} = 0.50$. If the spot then moves by $+\$3$ and realized volatility exactly matches the BSM-assumed volatility with no jump, which position accrues less hedging P&L variance to first order, and why might the network still have chosen the smaller position?
<details>
<summary>Answer</summary>
Under the stated conditions — realized vol matches the volatility the BSM delta was computed with, and there's no other source of model misspecification — BSM delta ($\Delta = 0.50$) is the locally variance-minimizing hedge, so in this idealized scenario the network's smaller position (0.42) would accrue more hedging P&L variance to first order; a $3 move against a 0.08 delta shortfall leaves roughly $0.08 \times \$3 = \$0.24$ of unhedged directional exposure relative to the BSM hedge. The network nonetheless may have learned 0.42 because its training objective was not "minimize variance under the exact assumed vol with no other frictions" — it was trained under transaction costs (a smaller position costs less to maintain and rebalance) and/or under the empirical spot-IV co-movement discussed in Q3/Q3-Level-1, which is a real effect in realistic data even though it's switched off in this idealized single-scenario question. The haircut is optimal on average over the training distribution, even though it looks suboptimal in any single scenario, like this one, where the effect it was compensating for doesn't materialize.
</details>

---

### Level 3 — Coding

**Q6.** In the `hedged_terminal_pl` function above, `tau` (time-to-expiry) is recomputed at every step as `(n_steps - i) * dt` and passed into the policy network alongside the current spot and previous delta. What would go wrong, both in training and in the meaning of the learned policy, if `tau` were dropped from the network's inputs entirely?
<details>
<summary>Answer</summary>
Without `tau`, the network would be forced to apply the *same* function of (normalized spot, previous position) at every time step, regardless of whether there are 30 days or 1 day left to expiry. This is a real problem because the optimal hedge ratio's sensitivity to spot changes dramatically with time-to-expiry — an ATM option's delta is far more sensitive to small spot moves (higher gamma) close to expiry than far from it, and the appropriate transaction-cost trade-off (how tightly to track the "ideal" delta versus how much to save on trading) also shifts as time runs out and there are fewer future rebalancing opportunities to amortize costs over. Stripping `tau` would force the single shared-weight network to average over very different optimal behaviors across the life of the option, degrading the fit at every horizon simultaneously — analogous to trying to fit one BSM delta formula with no T dependence. In training terms, the gradient signal from early-life and late-life states would be conflated for a parameter that needs to behave differently at each, slowing convergence and producing a worse (higher-CVaR) policy than one with `tau` included, even though the model has the same capacity otherwise.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Deep hedging replaces BSM entirely and proves it's "wrong" | Deep hedging is a strict generalization: with zero frictions and GBM dynamics, the trained policy converges to the BSM delta. It extends BSM to handle frictions and richer dynamics BSM cannot represent in closed form — it doesn't invalidate BSM's frictionless-limit result. |
| A trained deep hedging network is a universal hedge, portable across markets and regimes | "What Does Deep Hedging Actually Learn?" shows the opposite: networks trained on one historical period (e.g. 2015–2021) can learn regularities (like spot-IV co-movement) that fail in later adverse regimes (2022), producing losses precisely when robustness matters most. Deep hedges need the same walk-forward, out-of-sample validation discipline as any other trained model. |
| Deep hedging networks are inherently black boxes with no interpretable structure | Two mitigations exist in the literature covered here: symbolic regression can distill a trained network into a compact, auditable formula that retains much of its performance; and architectures like WW-NTBN bake in known structural priors (Whalley-Wilmott no-transaction bands) so the learned policy is interpretable by construction, not just post hoc. |
| The risk measure choice (e.g. CVaR vs. variance) is a minor implementation detail | It determines what "optimal" means for the trained policy. A network trained to minimize variance will hedge symmetrically; one trained to minimize CVaR at a specific confidence level will specifically prioritize avoiding tail losses, potentially at the cost of more frequent small losses elsewhere — the choice of $\rho$ and $\alpha$ materially changes the learned strategy. |

## Related Concepts
- [[Black-Scholes Model]] — the frictionless closed-form limit deep hedging must recover
- [[Delta Hedging]] — the classical hedging strategy deep hedging generalizes
- [[Option Greeks]] — delta is the quantity deep hedging policies implicitly re-learn under frictions
- [[Heston Model]] — an alternative fix for model misspecification (stochastic vol) that deep hedging can also be trained against as a simulator
- [[Value at Risk]] — VaR is the quantile that CVaR averages beyond; both are risk measures deep hedging can target
- [[Reinforcement Learning Trading]] — the RL framing under which deep hedging is trained in the regime-fragility paper (TD3 agents)

## Sources Used
- Buehler, Gonon, Teichmann, Wood (2019) — "Deep Hedging"
- "What Does Deep Hedging Actually Learn? Delta Corrections, Regime Fragility, and Symbolic Distillation" — Kirill Zernikov (2026), arXiv:2605.21696v1
- "Bridging Stochastic Control and Deep Hedging: Structural Priors for No-Transaction Band Networks" — Jules Arzel, Noureddine Lehdili (2026), arXiv:2603.29994v1

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-07-26 | Full content written | Content gap remediation — deep learning coverage |
