---
type: concept
domain: 10-Foundations
tags: [foundations, overview, pedagogy]
status: evergreen
stability: stable
confidence: high
last_reviewed: 2026-04-25
review_interval_days: 365
created: 2026-04-25
---

> Read this first. Every concept in this vault is an answer to a specific problem. This note traces the four chains of problems and solutions that define quantitative finance — so you always know *why* you are learning something.

---

## The Four Root Problems

Quantitative finance exists because of four fundamental human needs that practitioners kept running into:

| Problem            | In plain English                                                                                        |
| ------------------ | ------------------------------------------------------------------------------------------------------- |
| **Pricing**        | I want to trade a contract whose value depends on uncertain future events. What is a fair price today?  |
| **Hedging & Risk** | I've taken on risk by holding a position. How do I measure it, neutralize it, and survive bad outcomes? |
| **Alpha**          | Are there patterns in markets I can exploit systematically before others arbitrage them away?           |
| **Execution**      | I have a large order to fill. How do I do it without moving the market against myself?                  |

Each chain below traces how practitioners first attacked the problem, what they discovered was wrong, and what new concepts they developed to fix it — and in several cases, how different teams gave different answers to the same gap.

---

## Chain 1 — Pricing

**The root problem:** Someone wants to buy a contract that pays based on where a stock ends up (an option). What should the seller charge today?

---

### Gap 1: No agreed method to value an uncertain future payoff

The most natural idea: estimate where the stock will go, compute the expected payoff, and discount it back at some rate. This is how you would price any investment.

**The wall:** Buyer and seller have different views on where the stock is going. Different expected returns produce different prices. There is no agreed price — the market cannot function.

**The insight that broke through:** Forget expectations. If you can *replicate* the contract's payoff by trading the stock and a bond in a specific way, then the price of the contract must equal the cost of building that replicating portfolio — or someone can arbitrage it. Both parties agree on replication cost even if they disagree on the future.

This is **no-arbitrage pricing** — the organizing principle of all of derivatives theory.

> *Related concepts: [[Put-Call Parity]] — the first clean example of a no-arbitrage price relationship.*

---

### Gap 2: To build the replicating portfolio, you need a model for how prices move

Replication works in theory. In practice, you need to continuously adjust the hedge as the stock moves. To know how to adjust it, you need to model the stock's path mathematically.

**The wall:** Real stock prices move continuously and randomly. You need a rigorous model that captures this — positive prices, proportional moves, no predictable trend.

**Solution: Geometric Brownian Motion (GBM)**

Model the stock as drifting and jittering at every instant, where the jitter is proportional to the price level. This gives:
- Prices that stay positive (an exponential cannot go below zero)
- Log-returns that are normally distributed — roughly matching real data
- A clean parameter: μ (drift) and σ (volatility)

> *Related concept: [[Brownian Motion]] — the raw noise process. [[Geometric Brownian Motion]] — applied to prices.*

---

### Gap 3: Ordinary calculus cannot operate on GBM paths

To derive the value of the replicating portfolio as the stock moves, you need to differentiate functions of the stock price. But GBM paths are nowhere differentiable — they are infinitely jagged. The ordinary chain rule gives the wrong answer.

**The wall:** d(f(S)) ≠ f'(S)dS when S follows a stochastic process.

**Solution: Ito's Lemma (the stochastic chain rule)**

Because Brownian paths have nonzero quadratic variation — (dW)² = dt — the second-order term in the Taylor expansion survives. Ito's Lemma adds this correction:

df = (∂f/∂t + μ·∂f/∂S + ½σ²·∂²f/∂S²)dt + σ·∂f/∂S·dW

This is the single most-used mathematical tool in quantitative finance. Every derivative pricing model uses it.

> *Related concept: [[Ito's Lemma]], [[Stochastic Differential Equations]]*

---

### Gap 4: The derived option price still contains μ — but no one agrees on μ

Using Ito's Lemma to derive the option price produces a formula that depends on the stock's expected return μ. But μ is a subjective quantity — every investor estimates it differently. We are back to the original problem: no agreed price.

**The wall:** The math works but the answer is wrong — it depends on something unobservable.

**The insight:** When you hold the option and continuously hedge with the stock, the portfolio becomes riskless. A riskless portfolio must earn exactly the risk-free rate r — not μ. The drift μ cancels out of the hedge. So the price cannot depend on μ.

**Solution A: Risk-Neutral Measure**

Instead of working in the real world (where stock grows at μ), price in a fictional world where every asset grows at r. In this world, option price = discounted expected payoff. No μ needed. This is the risk-neutral measure Q.

**Solution B: Girsanov Theorem (the mathematical tool that makes Solution A rigorous)**

Changing the probability measure shifts the drift of Brownian motion from μ to r without changing the volatility σ. The market price of risk λ = (μ−r)/σ is the exact adjustment. Girsanov proves this change is valid and that Q is equivalent to P (same impossible events, different probabilities).

> *Related concepts: [[Risk-Neutral Measure]], [[Girsanov Theorem]], [[Martingales]] — discounted prices are Q-martingales, which is why the pricing formula works.*
>
> *Together these produce: [[Black-Scholes Model]] — the complete solution to Gap 4.*

---

### Gap 5: BSM assumes constant σ — real markets show a volatility smile

BSM produces a single option price for a given σ. But when you observe market prices across different strikes and maturities and ask "what σ makes BSM match each price?", you get different σ values for each strike. Options far out-of-the-money trade at higher implied volatility than at-the-money options. BSM cannot reproduce this.

**The wall:** One model, one σ — but markets have a whole surface of σ values. The model is systematically wrong off-the-money.

Three teams gave different answers to this gap:

**Solution A: Local Volatility (Dupire, 1994)**
Make σ a deterministic function of stock price and time: σ(S,t). Given any market-observed option surface, Dupire showed you can uniquely extract the local vol surface that reproduces it. Perfect fit to today's prices.
- *Remaining gap:* The model predicts that when the stock moves, the vol surface moves in the wrong direction. Forward smiles are too flat. Used for exotics pricing, not for trading vol dynamics.

**Solution B: Heston Stochastic Volatility Model (Heston, 1993)**
Make σ itself a random process — it has its own mean-reversion (OU-style) and its own noise. The correlation ρ between stock and vol shocks produces the skew. Better at capturing the dynamics of how the vol surface moves.
- *Remaining gap:* No closed-form for most exotic payoffs; calibration is complex; still doesn't fully capture extreme short-term skew.

**Solution C: Jump-Diffusion (Merton, 1976)**
Add discrete jumps to GBM — the stock can gap instantaneously. Jumps naturally produce fat tails and explain the steep skew for short-dated options.
- *Remaining gap:* Jumps are very hard to hedge. Model works well for pricing but not for constructing hedge portfolios.

> *Related concepts: [[Volatility Smile]], [[Implied Volatility]], [[Local Volatility]], [[Heston Model]], [[Merton Jump-Diffusion]], [[Volatility Surface]]*

---

### Gap 6: Many contracts have no closed-form solution

American options (exercisable at any time), barrier options, and options under stochastic vol models generally have no closed-form price formula. You can write down the PDE or the expectation but cannot solve it analytically.

**The wall:** The math exists but cannot be evaluated by hand or in a formula.

Two main numerical approaches:

**Solution A: Finite Difference Methods — solve the PDE on a grid**
Discretize the Black-Scholes PDE over a grid of stock price × time. March backward from the known terminal payoff to today's price. Naturally handles American early exercise by checking intrinsic value at each grid node. Three variants: Explicit (fast but unstable), Implicit (stable but first-order), Crank-Nicolson (stable, second-order — the standard).
- *Best for:* 1–2 underlying assets, American options, barrier options.

**Solution B: Monte Carlo Methods — simulate many paths**
Simulate thousands of price paths under Q, compute the average discounted payoff. Simple to implement, easily parallelized, handles path-dependent payoffs (Asian, lookback).
- *Best for:* Many underlyings, complex path-dependent payoffs.
- *Gap:* American options require Longstaff-Schwartz regression; convergence is slow (O(1/√n)).

**Solution C: Binomial Tree**
Discrete-time lattice where stock moves up or down at each step. Simple, intuitive, and converges to BSM in the limit. Standard for American option education and simple barriers.

> *Related concepts: [[Numerical Methods PDE]], [[Monte Carlo Methods]], [[Binomial Tree Model]], [[American Options]], [[Exotic Options]]*

---

## Chain 2 — Hedging and Risk

**The root problem:** You've entered a position and taken on risk. How do you measure it precisely enough to neutralize what you want to neutralize, and survive the risks you choose to keep?

---

### Gap 1: Holding an unhedged derivatives position is pure directional speculation

When a bank sells an option, it has sold a contract that could lose an arbitrary amount if the market moves. Holding it naked is gambling with the firm's capital.

**The wall:** Need a systematic way to eliminate (or control) the primary source of risk.

**Solution: Delta Hedging**

The option's sensitivity to the stock price is Δ = ∂V/∂S. Hold −Δ units of stock for every option. Now small moves in the stock cancel out in P&L. Continuously rebalance as Δ changes.

- *Gap:* Δ changes as the stock moves. Discrete rebalancing and transaction costs eat into the hedge. Γ = ∂²V/∂S² remains as unhedged risk.

> *Related concepts: [[Delta Hedging]], [[Option Greeks]]*

---

### Gap 2: Delta hedging neutralizes direction but leaves other exposures

A delta-hedged position still loses money if: time passes (Θ), volatility changes (ν), interest rates move (ρ), or the stock makes a large move (Γ).

**The wall:** One hedge ratio is not enough. Need to decompose risk into all dimensions.

**Solution: The Option Greeks**

A complete set of partial derivatives: Δ (price direction), Γ (rate of change of Δ), Θ (time decay), ν (vega — sensitivity to vol), ρ (interest rate sensitivity). Each can be hedged individually using different instruments.

> *Related concept: [[Option Greeks]]*

---

### Gap 3: Need a single number summarizing how bad things can get

Greeks measure sensitivity at a point. Risk managers and regulators need to answer: "If markets move adversely over the next day/month, what is the worst loss likely to be?"

**The wall:** Greeks are local sensitivities, not tail risk measures.

**Solution A: Value at Risk (VaR)**
"The loss we will not exceed with X% probability over horizon T." A single number for regulatory reporting and internal limits. Adopted by Basel accords.
- *Gap:* Not sub-additive — VaR of a portfolio can exceed the sum of VaRs of its parts (penalizes diversification). Tells you nothing about how bad losses are beyond the threshold.

**Solution B: Expected Shortfall (ES / CVaR)**
"The average loss given that we are in the worst X% of outcomes." Coherent risk measure — sub-additive, better tail characterization. Now the Basel III standard.

> *Related concepts: [[Value at Risk]], [[Expected Shortfall]]*

---

### Gap 4: Measuring risk is not the same as managing it across a portfolio

Greeks and VaR handle individual positions or small books. A portfolio of hundreds of positions needs a framework for constructing the portfolio so the total risk is acceptable and the return is maximized.

**The wall:** How do you combine N risky assets optimally?

**Solution: Markowitz Mean-Variance Optimization (1952)**

Hold a portfolio that maximizes expected return for a given level of variance (or minimizes variance for a given return). Diversification reduces variance without reducing expected return. The efficient frontier is the set of optimal portfolios.

- *Gap:* The optimization is highly sensitive to small changes in expected return inputs — garbage in, garbage out. Correlations are estimated from historical data and are unstable. Assumes returns are normally distributed. Produces concentrated portfolios that look nothing like what practitioners use.

> *Related concepts: [[Markowitz Mean-Variance Optimization]], [[Efficient Frontier]]*

---

### Gap 5: Markowitz is unstable — inputs are unreliable, outputs are extreme

Practitioners observed that plugging in slightly different return estimates produced wildly different optimal portfolios. The model was mathematically correct but practically useless as written.

Three teams gave different answers:

**Solution A: Factor Models (CAPM, Fama-French, Barra)**
Decompose each asset's return into exposure to systematic factors (market, size, value, momentum) plus idiosyncratic noise. Risk is measured in factor space, not stock space — far fewer, more stable parameters. The CAPM is the simplest factor model: one factor (the market).
- *Gap:* Factor exposures also change over time; choosing the right factors is an ongoing research problem.

**Solution B: Risk Parity**
Instead of optimizing on return (which is noisy), target equal risk contribution from each asset. No return estimates needed — only risk (variance/covariance). More robust to input uncertainty.
- *Gap:* Ignores expected returns entirely, which may leave return on the table.

**Solution C: Black-Litterman (1990)**
Blend the market equilibrium (implied returns from current market-cap weights, which encode millions of investors' views) with the investor's own views. Produces more stable, less extreme portfolios than raw Markowitz.

> *Related concepts: [[CAPM]], [[Factor Models]], [[Risk Parity]], [[Hierarchical Risk Parity]], [[Black-Litterman]]*

---

## Chain 3 — Alpha

**The root problem:** Markets are not perfectly efficient. Are there systematic patterns in prices that can be exploited repeatedly and profitably?

---

### Gap 1: Is there any evidence of persistent, tradeable patterns?

The Efficient Market Hypothesis (EMH) says prices already reflect all available information — you cannot beat the market systematically. But empirically, this is not perfectly true.

**The wall:** Need to find patterns that are statistically robust, not just data-mining artifacts.

**Solution A: Momentum (Jegadeesh and Titman, 1993)**
Stocks that outperformed over the past 12 months (skipping the last month) tend to continue outperforming over the next 3–12 months. A systematic, long/short portfolio captures this premium.
- *Gap:* Momentum strategies crash violently during sharp market reversals (2009, 2020). Underlying mechanism is still debated.

**Solution B: Mean Reversion / Statistical Arbitrage**
Over short horizons, prices exhibit mean-reversion rather than momentum. If two historically co-moving assets diverge, the spread tends to revert.
- *Gap:* Finding genuine co-movement vs. spurious correlation is hard. Co-integration relationships break down.

> *Related concepts: [[Momentum]], [[Mean Reversion]]*

---

### Gap 2: Individual signals work but are fragile — they decay and crash

A single signal (momentum or mean reversion alone) has high drawdown periods and decays as more capital chases it.

**The wall:** Need a systematic framework that combines multiple signals, controls risk, and adapts to changing market conditions.

**Solution: Statistical Arbitrage and Factor Models for Alpha**

Build a market-neutral portfolio using multiple alpha signals (momentum, value, quality, volatility) combined with a risk model that controls factor exposures. Diversification across signals and positions reduces drawdown.

- *Gap:* The more signals you test, the higher the risk of data-mining / overfitting. Multiple testing inflates false discovery rates.

> *Related concepts: [[Statistical Arbitrage]], [[Pairs Trading]], [[Factor Models]], [[Overfitting and Multiple Testing]], [[Alpha Factor]]*

---

### Gap 3: Traditional factors are linear combinations — may miss nonlinear patterns

Linear factor models can only capture additive relationships between signals and returns. Real market dynamics may be nonlinear.

**The wall:** Need to model complex, nonlinear relationships while avoiding overfitting.

**Solution: Machine Learning for Alpha**

Tree models (gradient boosting), neural networks, and NLP on alternative data can capture nonlinear patterns. Feature engineering in finance maps market data to signals.

- *Gap:* Financial data has very low signal-to-noise ratio. Overfitting is endemic. Models trained on one regime fail in another. Interpretability is limited — hard to know if the model learned a real economic relationship or a statistical artifact.

> *Related concepts: [[Feature Engineering Finance]], [[Alternative Data]], [[Regime Detection]], [[Reinforcement Learning Trading]]*

---

## Chain 4 — Execution

**The root problem:** You have decided to buy or sell a large quantity of an asset. How do you execute without moving the price against yourself?

---

### Gap 1: Naive execution destroys value

A large market order fills at increasingly bad prices as it exhausts liquidity in the order book. A 100,000-share order in a market with 10,000 shares at the best price moves the price before you finish filling.

**The wall:** Market impact cost can exceed the entire alpha of the trade.

**Solution: Spread execution over time (TWAP / VWAP)**

Trade a fixed quantity per time period (TWAP) or proportional to market volume (VWAP). Reduces impact by spreading the order. Simple, widely used as benchmarks.

- *Gap:* TWAP and VWAP are arbitrary schedules — they don't optimize the trade-off between going too fast (high impact) and going too slowly (timing risk while the price drifts).

> *Related concepts: [[TWAP-VWAP]], [[Order Book]], [[Price Impact]]*

---

### Gap 2: Need a principled framework for the impact-vs-timing-risk tradeoff

Going slowly reduces market impact but increases the risk that the stock moves against you while you're executing. Going quickly reduces timing risk but increases impact. Where is the optimal balance?

**The wall:** No rigorous model for the right execution schedule.

**Solution: Almgren-Chriss Model (2001)**

Model market impact as a function of execution rate, and timing risk as a function of residual position and stock volatility. Solve for the optimal trajectory that minimizes the sum of expected cost plus a penalty for variance. Produces a closed-form optimal execution schedule.

- *Gap:* Assumes deterministic, static impact functions. Real markets have intraday patterns, regime changes, and order book dynamics that the model ignores.

> *Related concepts: [[Almgren-Chriss]], [[Transaction Cost Analysis]]*

---

### Gap 3: Execution interacts with market microstructure — other participants respond to your trades

Execution is not happening in isolation. Market makers, HFT firms, and other institutional traders observe order flow and respond to it. Large orders get detected and front-run.

**The wall:** Need to understand how market structure creates costs and how to minimize information leakage.

**Solution: Market Microstructure concepts**

Market Making — dealers provide liquidity by quoting bid/ask; they profit from the spread but bear inventory risk. Adverse Selection — informed traders trade against market makers who don't know which trades are informed. The Avellaneda-Stoikov model formalizes the optimal market maker quoting strategy given inventory risk and adverse selection.

> *Related concepts: [[Market Making]], [[Adverse Selection]], [[Avellaneda-Stoikov]], [[Order Book]]*

---

## The Full Concept Map

| Concept | Chain | Gap it closes |
|---------|-------|---------------|
| [[Brownian Motion]] | Pricing | Gap 2 — foundation for price movement model |
| [[Geometric Brownian Motion]] | Pricing | Gap 2 — stock price model |
| [[Stochastic Differential Equations]] | Pricing | Gap 2 — general framework for all continuous-time models |
| [[Ito's Lemma]] | Pricing | Gap 3 — stochastic chain rule |
| [[Martingales]] | Pricing | Gap 4 — mathematical language of no-arbitrage |
| [[Risk-Neutral Measure]] | Pricing | Gap 4 — removes μ from option prices |
| [[Girsanov Theorem]] | Pricing | Gap 4 — makes the measure change rigorous |
| [[Black-Scholes Model]] | Pricing | Gap 4 — complete solution for European options |
| [[Put-Call Parity]] | Pricing | Gap 1 — first no-arbitrage price relationship |
| [[Implied Volatility]] | Pricing | Gap 5 — measures market's Q-vol at each strike |
| [[Volatility Smile]] | Pricing | Gap 5 — documents the constant-σ failure |
| [[Volatility Surface]] | Pricing | Gap 5 — full map of implied vols across strikes and maturities |
| [[Local Volatility]] | Pricing | Gap 5 — Solution A (deterministic σ(S,t)) |
| [[Heston Model]] | Pricing | Gap 5 — Solution B (stochastic vol) |
| [[Merton Jump-Diffusion]] | Pricing | Gap 5 — Solution C (jumps) |
| [[SABR Model]] | Pricing | Gap 5 — solution for interest rate vol surfaces |
| [[Ornstein-Uhlenbeck Process]] | Pricing / Alpha | Gap 2 model for mean-reverting quantities; used in Vasicek and pairs trading |
| [[Vasicek Model]] | Pricing | Gap 5 extension — interest rate analog of GBM + mean reversion |
| [[Hull-White Model]] | Pricing | Gap 5 extension — time-varying Vasicek, fits today's yield curve exactly |
| [[HJM Framework]] | Pricing | Gap for forward rate modeling — models entire yield curve evolution |
| [[Numerical Methods PDE]] | Pricing | Gap 6 — Solution A (finite difference) |
| [[Monte Carlo Methods]] | Pricing | Gap 6 — Solution B (simulation) |
| [[Binomial Tree Model]] | Pricing | Gap 6 — Solution C (discrete lattice) |
| [[American Options]] | Pricing | Gap 6 application — early exercise |
| [[Exotic Options]] | Pricing | Gap 6 application — path-dependent payoffs |
| [[Delta Hedging]] | Hedging | Gap 1 — eliminate directional risk |
| [[Option Greeks]] | Hedging | Gap 2 — full risk decomposition |
| [[Value at Risk]] | Risk | Gap 3 — Solution A (threshold loss metric) |
| [[Expected Shortfall]] | Risk | Gap 3 — Solution B (tail-coherent metric) |
| [[Markowitz Mean-Variance Optimization]] | Risk | Gap 4 — optimal portfolio construction |
| [[Efficient Frontier]] | Risk | Gap 4 — visual/mathematical result of Markowitz |
| [[CAPM]] | Risk | Gap 5 — Solution A single-factor model |
| [[Factor Models]] | Risk | Gap 5 — Solution A multi-factor model |
| [[Risk Parity]] | Risk | Gap 5 — Solution B (risk-contribution weighting) |
| [[Hierarchical Risk Parity]] | Risk | Gap 5 — Solution B extension (cluster-based) |
| [[Black-Litterman]] | Risk | Gap 5 — Solution C (equilibrium + views) |
| [[Sharpe Ratio]] | Risk | Measuring return per unit risk — the universal performance metric |
| [[Kelly Criterion]] | Risk | Optimal bet sizing to maximize long-run growth rate |
| [[Maximum Drawdown]] | Risk | Tail risk of a strategy's equity curve |
| [[Stress Testing]] | Risk | Scenario-based risk beyond VaR |
| [[Correlation and Covariance Estimation]] | Risk | Input quality problem for all portfolio optimization |
| [[Momentum]] | Alpha | Gap 1 — Solution A (trend persistence) |
| [[Mean Reversion]] | Alpha | Gap 1 — Solution B (spread reversion) |
| [[Pairs Trading]] | Alpha | Gap 1 — Solution B applied (cointegration-based) |
| [[Statistical Arbitrage]] | Alpha | Gap 2 — systematic, multi-signal approach |
| [[Carry Strategies]] | Alpha | Gap 1 extension — exploit yield differentials across assets |
| [[CTA and Trend Following]] | Alpha | Gap 1 — systematic momentum across asset classes |
| [[Alpha Factor]] | Alpha | Gap 2 — building blocks of signal construction |
| [[Feature Engineering Finance]] | Alpha | Gap 3 — structured signal creation from raw data |
| [[Alternative Data]] | Alpha | Gap 3 — non-price information for signal generation |
| [[Overfitting and Multiple Testing]] | Alpha | Gap 3 — controls false discovery in signal research |
| [[Regime Detection]] | Alpha | Gap 2 — knowing when a signal applies |
| [[Reinforcement Learning Trading]] | Alpha | Gap 3 — nonlinear adaptive signal generation |
| [[TWAP-VWAP]] | Execution | Gap 1 — basic execution scheduling |
| [[Almgren-Chriss]] | Execution | Gap 2 — optimal impact/risk tradeoff |
| [[Transaction Cost Analysis]] | Execution | Gap 2 — measuring actual vs expected execution cost |
| [[Market Making]] | Execution | Gap 3 — providing liquidity, managing inventory |
| [[Avellaneda-Stoikov]] | Execution | Gap 3 — optimal quoting strategy for market makers |
| [[Order Book]] | Execution | Gap 3 — understanding market microstructure |
| [[Price Impact]] | Execution | Gap 1/2 — measuring cost of order flow |
| [[Adverse Selection]] | Execution | Gap 3 — informed vs uninformed order flow |
| [[Variance Swap]] | Pricing | Gap 5 extension — trade volatility directly as an asset |
| [[Credit Default Swap]] | Hedging | Gap 1 extension — hedge credit risk specifically |
| [[Gamma Scalping]] | Hedging | Gap 2 — actively monetize Γ exposure |
| [[Options Strategies]] | Hedging / Alpha | Structured payoff combinations using Greeks |
| [[Volatility Arbitrage]] | Alpha | Gap 5 — trade implied vol vs realized vol |
| [[VIX]] | Risk / Alpha | Market's aggregate implied vol — fear gauge |
| [[Backtesting Methodology]] | Alpha | Gap 2 — validating strategies before live trading |
| [[Bond Basics]] | Pricing | Fixed income analog of equity pricing |
| [[Duration]] | Hedging | Fixed income Gap 2 — sensitivity of bond price to rates |
| [[Convexity]] | Hedging | Fixed income Gap 2 — second-order rate sensitivity (bond Γ) |
| [[Yield Curve]] | Pricing | Foundation for all fixed income pricing |
| [[Interest Rate Swaps]] | Hedging | Fixed income hedging instrument |

---

## How to Use This Note

When you open any concept note in this vault, look for the **Problem Chain** block at the top. It tells you:
- Which chain this concept belongs to
- Which specific gap it was created to close
- What other solutions exist for the same gap
- What you need to understand first
- What this concept enables

If you are new to quantitative finance, follow the chains in order. The Pricing chain is the logical starting point — it builds from basic probability all the way to numerical methods, and most concepts in other chains reference it.

If you already know some concepts, use the Concept Map table above to locate yourself and navigate to adjacent nodes.

---

## Sources Used
- Hull — *Options, Futures & Other Derivatives*, ch. 1 (overview of derivatives markets)
- Shreve — *Stochastic Calculus for Finance I & II* (mathematical development)
- Lopez de Prado — *Advances in Financial Machine Learning* (alpha and ML chains)
- Almgren & Chriss — "Optimal Execution of Portfolio Transactions" (execution chain)
- Jegadeesh & Titman — "Returns to Buying Winners and Selling Losers" (momentum)
