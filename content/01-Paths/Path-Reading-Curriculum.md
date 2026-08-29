---
type: learning-path
title: "How to Read Quant Papers"
tags: [path]
status: active
created: 2026-08-24
---

## Purpose

This is an opinionated reading curriculum for someone who wants to become job-ready in quantitative finance as fast as possible. It is not a survey of the field. It is a sequenced program with specific papers, specific time allocations, and specific instructions on what to extract from each one. Read it like orders, not suggestions.

"Job-ready" means: you can sit across from a senior quant, discuss any of these papers at the level of methods and results (not just the abstract), explain why each one matters for actual trading or risk, and hold your own in a debate about the limitations. That is a higher bar than most online curricula target.

---

## Before You Start: How to Read a Quant Paper

Most people read papers wrong. They start at the abstract, read linearly, get stuck on the math, and quit. Here is the correct approach.

### The Three-Pass Method

**Pass 1 — Reconnaissance (15 minutes)**
Read: title, abstract, introduction (first and last paragraph only), section headers, figures, and conclusion. Goal: understand the question being asked, the answer claimed, and the method used. You are not reading the math yet. After Pass 1, you should be able to answer: "What problem does this paper solve, and does it work?"

**Pass 2 — Working Knowledge (1-3 hours)**
Read the introduction fully, the methods section at a level where you understand the setup (what the model assumes, what the data is, what the estimator is), the results section for the key tables and claims, and the conclusion. Skip long proofs on first read — read the lemma statements instead. Goal: you can explain the paper's central contribution, its key assumptions, and its main result in two minutes to someone who hasn't read it. After Pass 2, mark this paper as having "working knowledge."

**Pass 3 — Implementation (4-8 hours)**
Work through the math yourself. Reproduce one table or one result numerically. Write code. This is for papers that directly touch your specialization — you will not do Pass 3 on every paper in this curriculum, only on the 10-15 papers closest to your job function.

### Understanding vs. Working Knowledge

| Level | What You Can Do | Time Investment |
|-------|----------------|-----------------|
| Awareness | Name the paper, state the key claim | Pass 1 only — 15 min |
| Working Knowledge | Explain methods, state results, identify limitations | Passes 1+2 — 2-3 hrs |
| Implementation | Reproduce results, adapt to new data, debug | All 3 passes — 6-10 hrs |

For a generalist quant role (PM, risk, research), aim for Working Knowledge on ~30 papers and Awareness on ~50 more. For a specialist role (derivatives pricing, HFT market making), push 10-15 papers in your area to Implementation level.

### Reading Mathematics in Papers

Do not skip math — but do not treat it as primary on first pass either. The correct sequence: understand the model in words first, then verify the math matches your intuition. When you hit a derivation you don't follow, ask: "what does this equation claim in English?" If you can answer that, you can move on. If you cannot, you are missing a prerequisite — stop and fill it.

Prerequisites that unlock most quant math:
- Linear algebra (matrix multiplication, eigendecomposition, OLS derivation)
- Probability (expectation, variance, covariance, conditional expectation, CLT)
- Calculus (chain rule, integration, partial derivatives)
- Ito's lemma (unlocks all derivatives papers — spend real time here)
- Regression (OLS, t-tests, R-squared — unlocks all empirical finance papers)

### How Papers Relate to Textbooks

Papers assume background knowledge that textbooks provide. The right workflow: read the textbook chapter first (1-2 hours), then read the original paper (2-3 hours). The textbook gives you the vocabulary; the paper gives you the original argument, caveats, and context that textbooks sanitize away. Hull on options, then Black-Scholes. Shreve Chapter 4, then Merton. Lopez de Prado Chapter 5, then Gatev et al.

For foundational papers (pre-1990), reading the original is essential — they are short, clear, and contain arguments that later presentations distort. For recent papers, the textbook treatment (if one exists) is often cleaner than the original.

---

## The Four Phases

| Phase | Name | Focus | Fast Track | Steady Track |
|-------|------|--------|------------|--------------|
| 1 | Foundation | Core theory every quant must know | Weeks 1-4 | Months 1-3 |
| 2 | Strategy | How alpha is generated and measured | Weeks 5-8 | Months 4-6 |
| 3 | Specialization | Go deep in one area | Weeks 9-10 | Months 7-9 |
| 4 | Frontier | Current research, ML, emerging areas | Weeks 11-12 | Months 10-12 |

---

## Phase 1: Foundation

**Goal:** Understand the theoretical bedrock. These papers are not optional — every quant conversation assumes you know this material. Skipping Phase 1 to get to "interesting" papers is a mistake that will haunt every subsequent discussion.

**Why this order:** Markets → pricing → portfolio. You need to understand what prices represent (Fama/Samuelson) before you can model them (BSM), and you need to model individual assets before you can combine them (Markowitz). The interest rate and credit papers close the loop on fixed income, which appears everywhere in derivatives and risk.

### Papers and Time Allocations

#### Week 1: Market Efficiency and Price Formation

| Paper | Level | Time | What to Focus On |
|-------|-------|------|------------------|
| [[Fama-1970-Efficient-Capital-Markets\|Fama (1970)]] | Working Knowledge | 2 hrs | The three forms of efficiency. Understand the joint hypothesis problem — this is the most important single idea in empirical finance and most people get it wrong. |
| [[Samuelson-1965-Proof-That-Properly-Anticipated-Prices\|Samuelson (1965)]] | Awareness | 45 min | The mathematical proof that efficient prices fluctuate randomly. Short paper. Read to understand why randomness in prices is a sign of health, not chaos. |
| [[Lo-MacKinlay-1988-Stock-Prices-Do-Not-Follow-Random-Walks\|Lo & MacKinlay (1988)]] | Working Knowledge | 2 hrs | The variance ratio test. This paper directly attacks Fama's EMH with data. Read it immediately after Fama to see how the empirical debate works. |
| [[Cont-2001-Empirical-Properties-Asset-Returns-Stylized-Facts\|Cont (2001)]] | Working Knowledge | 2 hrs | Memorize the stylized facts: fat tails, volatility clustering, autocorrelation of absolute returns, leverage effect. These are the empirical targets that every model is judged against. |

**Key question to answer after Week 1:** If markets are efficient, why do quants have jobs? (The joint hypothesis problem is the answer.)

#### Week 2: Derivatives Pricing

**Prerequisite:** Read Hull Chapters 13-15 before tackling Black-Scholes. Do not skip this. The textbook gives you binomial trees and risk-neutral pricing, which are essential mental models for the original paper.

| Paper | Level | Time | What to Focus On |
|-------|-------|------|------------------|
| [[Black-Scholes-1973-Pricing-of-Options-and-Corporate-Liabilities\|Black & Scholes (1973)]] | Implementation | 6 hrs | The derivation from delta-hedging to PDE to formula. Work through the Greeks. Derive implied volatility conceptually. Understand that constant volatility is wrong and why the market still uses the formula. |
| [[Merton-1973-Theory-of-Rational-Option-Pricing\|Merton (1973)]] | Working Knowledge | 2.5 hrs | Continuous-time option theory; American exercise premium; the rigorous foundations BSM assumed. Read after BSM; it fills in what Black and Scholes left implicit. |
| [[Harrison-Kreps-1979-Martingales-and-Arbitrage\|Harrison & Kreps (1979)]] | Awareness | 1 hr | The First FTAP: no-arbitrage is equivalent to the existence of a risk-neutral measure. You do not need to follow the proof — understand the statement and why it matters for everything that follows. |

**Key question to answer after Week 2:** What exactly does "risk-neutral pricing" mean, and how does it avoid needing to know the expected return of a stock?

#### Week 3: Portfolio Theory and Factor Pricing

| Paper | Level | Time | What to Focus On |
|-------|-------|------|------------------|
| [[Markowitz-1952-Portfolio-Selection\|Markowitz (1952)]] | Implementation | 4 hrs | Mean-variance optimization, the efficient frontier, and the role of correlation. Build a small efficient frontier in code using a 5-stock example. The paper is only 14 pages — read it fully. |
| [[Sharpe-1964-Capital-Asset-Prices\|Sharpe (1964)]] | Working Knowledge | 2 hrs | CAPM derivation from Markowitz equilibrium. Understand beta as the only priced risk. Know the Security Market Line cold. |
| [[Ross-1976-Arbitrage-Theory-of-Capital-Asset-Pricing\|Ross (1976)]] | Working Knowledge | 2.5 hrs | APT: multi-factor pricing from no-arbitrage alone, without the CAPM equilibrium assumptions. This is the theoretical foundation for everything in factor investing. |
| [[Kelly-1956-New-Interpretation-of-Information-Rate\|Kelly (1956)]] | Working Knowledge | 1.5 hrs | Log-optimal betting. Understand why maximizing log-wealth is the right objective for long-run growth, and the relationship to Shannon entropy. The paper is 7 pages. |

**Key question to answer after Week 3:** What is the difference between CAPM (one factor, equilibrium) and APT (multi-factor, no-arbitrage)? Which one is more useful in practice and why?

#### Week 4: Risk and Volatility Modeling

| Paper | Level | Time | What to Focus On |
|-------|-------|------|------------------|
| [[Engle-1982-ARCH\|Engle (1982)]] | Working Knowledge | 2 hrs | ARCH: volatility clustering modeled as time-varying conditional variance. Understand the setup, the likelihood estimation approach, and why OLS fails when errors are heteroskedastic. |
| [[Bollerslev-1986-GARCH\|Bollerslev (1986)]] | Working Knowledge | 1.5 hrs | GARCH(1,1): the parsimonious extension of ARCH that actually fits data. Read right after Engle — this is one paper split across two publications. |
| [[Artzner-1999-Coherent-Measures-of-Risk\|Artzner et al. (1999)]] | Working Knowledge | 2.5 hrs | Coherent risk measures: the four axioms, why VaR violates subadditivity, and why Expected Shortfall is the coherent replacement. Every risk management conversation references this paper. |
| [[Rockafellar-Uryasev-2000-Optimization-of-CVaR\|Rockafellar & Uryasev (2000)]] | Working Knowledge | 2 hrs | CVaR as a linear program. The key insight is that minimizing CVaR is computationally tractable. Read the LP formulation carefully — it is used in practice. |
| [[Mandelbrot-1963-Variation-of-Certain-Speculative-Prices\|Mandelbrot (1963)]] | Awareness | 1 hr | Fat tails and Lévy stable distributions. You do not need to fully follow the stable distribution theory — understand that returns have heavier tails than normal, and that this has been known since 1963. |

**Key question to answer after Week 4:** Why is VaR the regulatory standard if Artzner showed it is not coherent? (Political/computational history, not a math failure.)

---

## Phase 2: Strategy

**Goal:** Understand how actual alpha strategies are constructed, tested, and evaluated. These papers are the empirical workhorses that launched real businesses. After Phase 2, you can read a hedge fund marketing deck and identify exactly which academic papers underlie their strategy.

**Why this order:** Factor theory → empirical evidence → specific strategies → execution. You need the theoretical framework (APT from Phase 1) before you can evaluate factor evidence. Once you understand factors, momentum and stat arb are natural extensions. Execution comes last because it presupposes you have a strategy worth executing.

### Papers and Time Allocations

#### Week 5: The Factor Model Evidence

| Paper | Level | Time | What to Focus On |
|-------|-------|------|------------------|
| [[Fama-French-1992-Cross-Section-Expected-Stock-Returns\|Fama & French (1992)]] | Working Knowledge | 2.5 hrs | The demolition of CAPM. Understand the Fama-MacBeth regression procedure — it is used everywhere. Focus on Tables 2-4. The conclusion: beta is dead. |
| [[Fama-French-1993-Common-Risk-Factors\|Fama & French (1993)]] | Implementation | 5 hrs | The three-factor model. Build SMB and HML yourself from CRSP or Ken French's data website. Run time-series regressions on 25 size-B/M portfolios. Understand the GRS test. This is the most cited paper in finance — you need to know it at implementation level. |
| [[Carhart-1997-Persistence-in-Mutual-Fund-Performance\|Carhart (1997)]] | Working Knowledge | 2 hrs | Four-factor model adding momentum. Read to understand how factors are used as benchmarks, not just as strategies. The mutual fund alpha question is the right frame for understanding what a factor model is for. |
| [[Fama-French-2015-Five-Factor-Asset-Pricing-Model\|Fama & French (2015)]] | Awareness | 1 hr | Five factors: MKT + SMB + HML + RMW + CMA. Understand that adding profitability and investment factors largely kills the HML premium. Know the debate about whether this is better or just more parameters. |

**Side read (not a paper):** Download FF factor data from mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html and compute factor correlations. Seeing the actual time series grounds everything from the papers.

#### Week 6: Anomalies, Momentum, and Stat Arb

| Paper | Level | Time | What to Focus On |
|-------|-------|------|------------------|
| [[Banz-1981-Relationship-Return-Market-Value\|Banz (1981)]] | Awareness | 45 min | The first CAPM anomaly paper: small caps earn more than CAPM predicts. Short read, historically important — it broke the ice. |
| [[Jegadeesh-Titman-1993-Returns-Buying-Winners-Selling-Losers\|Jegadeesh & Titman (1993)]] | Implementation | 4 hrs | Price momentum: buy 3-12 month winners, sell losers. The formation period/holding period structure is the template for how all cross-sectional strategies are tested. Replicate Table 1. |
| [[Gatev-Goetzmann-Rouwenhorst-2006-Pairs-Trading\|Gatev, Goetzmann & Rouwenhorst (2006)]] | Working Knowledge | 3 hrs | Pairs trading via distance matching. Read the methodology section carefully — the distance-based pair selection and the trigger/trade logic. Understand why 11%/year gross drops significantly after transaction costs. |
| [[Grinold-1989-Fundamental-Law-Active-Management\|Grinold (1989)]] | Implementation | 3 hrs | IR = IC x sqrt(BR). This formula governs every systematic strategy business. Understand all three terms deeply: what IC actually measures, what counts as a breadth (BR) unit, and the independence assumption. Practitioners abuse this formula constantly — knowing the assumptions is what separates you. |

#### Week 7: Market Microstructure

| Paper | Level | Time | What to Focus On |
|-------|-------|------|------------------|
| [[Kyle-1985-Continuous-Auctions-and-Insider-Trading\|Kyle (1985)]] | Implementation | 5 hrs | Kyle's lambda: price impact = lambda * order flow. Work through the linear equilibrium derivation. Understand why the informed trader spreads their trade over time. Lambda is cited in nearly every execution and market making paper ever written. |
| [[Glosten-Milgrom-1985-Bid-Ask-Transaction-Prices\|Glosten & Milgrom (1985)]] | Working Knowledge | 2.5 hrs | Bid-ask spread from adverse selection in a sequential trade model. Read alongside Kyle — they are complementary views of the same problem (strategic vs. sequential). Focus on the spread decomposition: adverse selection component + inventory component. |
| [[Almgren-Chriss-2001-Optimal-Execution-Portfolio-Transactions\|Almgren & Chriss (2001)]] | Implementation | 5 hrs | Optimal execution: the mean-variance frontier over trading trajectories. Understand the linear impact model, the TWAP/VWAP benchmarks, and the efficient frontier of execution schedules. This paper is directly implemented in every execution management system. |

#### Week 8: Volatility Strategies and the Interest Rate World

| Paper | Level | Time | What to Focus On |
|-------|-------|------|------------------|
| [[Heston-1993-Closed-Form-Solution-Options-Stochastic-Volatility\|Heston (1993)]] | Working Knowledge | 3 hrs | Stochastic volatility model with a closed-form characteristic function. Understand the two-factor SDE structure (price + vol), and why the characteristic function approach gives a semi-closed-form solution. This is the industry standard vol model. |
| [[Vasicek-1977-Equilibrium-Characterization-Term-Structure\|Vasicek (1977)]] | Working Knowledge | 2 hrs | Mean-reverting short rate; affine term structure; closed-form bond prices. This is the entry point to all term structure models. Understand why negative rates are possible and why that is a model deficiency. |
| [[Heath-Jarrow-Morton-1992-Bond-Pricing-Term-Structure\|Heath, Jarrow & Morton (1992)]] | Working Knowledge | 2.5 hrs | Forward rate dynamics — the general framework that nests Vasicek, CIR, and Hull-White. Read to understand how HJM unifies the short-rate model zoo. The drift restriction (the HJM condition) is the key result. |
| [[Lo-2002-Statistics-of-Sharpe-Ratios\|Lo (2002)]] | Working Knowledge | 2 hrs | Sharpe ratio inference: autocorrelation in returns biases the SR upward and its standard error is large. Every time someone shows you a backtest Sharpe, apply the Lo correction mentally. |

---

## Phase 3: Specialization

**Goal:** Go deep in one area. You cannot be expert at everything. Pick one track below based on your target role and spend the equivalent of 3 weeks (fast track) or 3 months (steady track) on it. Read the Phase 3 papers at Working Knowledge minimum, push the most relevant 3-4 to Implementation.

Do not skip Phase 3 — depth in one area is what makes you hireable. Generalists with shallow knowledge across all areas are easy to hire but hard to promote.

### Track A: Derivatives and Volatility (for sell-side quant, vol desk, derivatives structuring)

**Additional prerequisite:** Hull Chapters 19-20 (Greeks and volatility surface), then Gatheral "The Volatility Surface" Chapter 1.

| Paper | Level | Time | What to Focus On |
|-------|-------|------|------------------|
| [[Cox-Ross-Rubinstein-1979-Option-Pricing-Simplified-Approach\|Cox, Ross & Rubinstein (1979)]] | Implementation | 4 hrs | Binomial tree: build one. Understand risk-neutral pricing from the up/down factors. The bridge from discrete to continuous BSM. |
| [[Black-1976-Pricing-of-Commodity-Contracts\|Black (1976)]] | Working Knowledge | 1.5 hrs | Black's model for futures and bond options. The standard quoting model for caps/floors/swaptions. Short, consequential. |
| [[Longstaff-Schwartz-2001-Valuing-American-Options-LSM\|Longstaff & Schwartz (2001)]] | Implementation | 5 hrs | Least-squares Monte Carlo for American options. Implement the LSM algorithm from scratch. This is the standard industry method for path-dependent early exercise. |
| [[Harrison-Pliska-1981-Martingales-and-Stochastic-Integrals\|Harrison & Pliska (1981)]] | Working Knowledge | 2.5 hrs | Second FTAP: complete markets and unique EMM. Read after Harrison-Kreps. Together these two papers are the mathematical foundation for the entire derivatives industry. |
| [[Merton-1974-Pricing-Corporate-Debt\|Merton (1974)]] | Working Knowledge | 2 hrs | Equity as a call option on firm assets; structural credit model. The conceptual link between options theory and credit risk. |

**Textbook supplement:** Gatheral "The Volatility Surface" (entire book, ~150 pages). Read in parallel with this track.

### Track B: Systematic Equity and Factor Investing (for equity long/short, quant PM, factor shop)

| Paper | Level | Time | What to Focus On |
|-------|-------|------|------------------|
| [[Fama-French-1993-Common-Risk-Factors\|Fama & French (1993)]] | Implementation (if not done) | — | Required from Phase 2. Make sure you have replicated the factor construction. |
| [[Lo-MacKinlay-1988-Stock-Prices-Do-Not-Follow-Random-Walks\|Lo & MacKinlay (1988)]] | Implementation | 3 hrs | Implement the variance ratio test on equity index data. Understand how to detect autocorrelation structure that can be exploited. |
| [[Gatev-Goetzmann-Rouwenhorst-2006-Pairs-Trading\|Gatev, Goetzmann & Rouwenhorst (2006)]] | Implementation (if not done) | — | Required from Phase 2. Implement the pairs selection and trading rule. |
| [[Rockafellar-Uryasev-2000-Optimization-of-CVaR\|Rockafellar & Uryasev (2000)]] | Implementation | 3 hrs | Build a CVaR portfolio optimization using the LP formulation. Compare to mean-variance on the same dataset. |
| [[Brunnermeier-Pedersen-2009-Market-Liquidity-Funding-Liquidity\|Brunnermeier & Pedersen (2009)]] | Working Knowledge | 2.5 hrs | Liquidity spirals: why strategies collapse in crises. Essential for understanding the 2008 quant meltdown and designing robust strategies. |

**Textbook supplement:** Lopez de Prado "Advances in Financial Machine Learning" Chapters 1-5 (purging, fractional differentiation, meta-labeling). These are practical chapters, read them as methods, not theory.

### Track C: Market Making and Execution (for HFT, market making desk, execution algo)

| Paper | Level | Time | What to Focus On |
|-------|-------|------|------------------|
| [[Kyle-1985-Continuous-Auctions-and-Insider-Trading\|Kyle (1985)]] | Implementation (if not done) | — | Required from Phase 2. |
| [[Avellaneda-Stoikov-2008-High-Frequency-Trading-Limit-Order-Book\|Avellaneda & Stoikov (2008)]] | Implementation | 6 hrs | Stochastic control for market making: the reservation price and optimal spread. Implement the model in simulation. This is the theoretical foundation for every modern market making system. |
| [[Glosten-Milgrom-1985-Bid-Ask-Transaction-Prices\|Glosten & Milgrom (1985)]] | Implementation | 3 hrs | Sequential trade model. Implement a simple adverse selection spread calculator. |
| [[Almgren-Chriss-2001-Optimal-Execution-Portfolio-Transactions\|Almgren & Chriss (2001)]] | Implementation (if not done) | — | Required from Phase 2. |
| [[Brunnermeier-Pedersen-2009-Market-Liquidity-Funding-Liquidity\|Brunnermeier & Pedersen (2009)]] | Working Knowledge | 2.5 hrs | Market and funding liquidity feedback loops. Essential context for why market making fails precisely when it is most needed. |

**Textbook supplement:** Cartea, Jaimungal & Penalva "Algorithmic and High-Frequency Trading" Chapters 4-6. Read in parallel with this track.

### Track D: Fixed Income and Credit (for rates desk, credit fund, bank risk)

| Paper | Level | Time | What to Focus On |
|-------|-------|------|------------------|
| [[Vasicek-1977-Equilibrium-Characterization-Term-Structure\|Vasicek (1977)]] | Implementation | 3 hrs | Implement bond pricing under Vasicek. Calibrate to a yield curve. |
| [[Cox-Ingersoll-Ross-1985-Theory-Term-Structure-Interest-Rates\|Cox, Ingersoll & Ross (1985)]] | Working Knowledge | 2 hrs | Non-negative rates; square-root process. Understand why this restriction matters and when it still breaks (near-zero rate environment). |
| [[Hull-White-1990-Pricing-Interest-Rate-Derivative-Securities\|Hull & White (1990)]] | Working Knowledge | 2 hrs | Extended Vasicek calibrated exactly to the current yield curve. This is the industry standard for vanilla rate derivatives. |
| [[Heath-Jarrow-Morton-1992-Bond-Pricing-Term-Structure\|Heath, Jarrow & Morton (1992)]] | Implementation | 4 hrs | HJM forward rate model. Understand the no-drift condition and implement a two-factor HJM simulation. |
| [[Merton-1974-Pricing-Corporate-Debt\|Merton (1974)]] | Working Knowledge | 2 hrs | Structural credit model. |
| [[Jarrow-Turnbull-1995-Pricing-Derivatives-Credit-Risk\|Jarrow & Turnbull (1995)]] | Working Knowledge | 2 hrs | Reduced-form credit model: Poisson default intensity. Understand the calibration to CDS spreads. |
| [[Duffie-Singleton-1999-Modeling-Term-Structures-Defaultable-Bonds\|Duffie & Singleton (1999)]] | Working Knowledge | 2.5 hrs | Affine defaultable bond pricing; credit spread = L * lambda. The industry foundation for credit term structure. |

---

## Phase 4: Frontier

**Goal:** Understand what the field is actively working on. Phase 4 is not about mastering everything — it is about being able to engage intelligently with current research and knowing which frontier directions are likely to matter for your role.

Spend 2 weeks (fast track) or 3 months (steady track) here. Aim for Awareness on most papers, Working Knowledge on 2-3 that are directly relevant.

### Current Research Worth Tracking

**Microstructure and Execution**
- [[Empirical Confirmation of the Square-Root Law of Market Impact in a U.S. Large-C\|Square-Root Law of Market Impact]] — The concave (not linear) price impact law is now empirically confirmed at scale. Almgren-Chriss uses linear impact; the square-root law is better empirically.
- [[Bridging the Reality Gap in Limit Order Book Simulation\|Bridging the Reality Gap in LOB Simulation]] — Simulated LOBs for training execution algorithms; the calibration gap between simulation and real markets.

**Factor and Portfolio Construction**
- [[Which Portfolios- The Construction Dependence of Factor Model Performance\|Which Portfolios?]] — Factor model results depend heavily on portfolio construction choices that are often glossed over. Important skeptic reading after Phase 2.
- [[The Co-Pricing Factor Zoo\|The Co-Pricing Factor Zoo]] — The multiple-testing problem: how many of the 400+ published factors survive rigorous correction?
- [[Measuring Strategy-Decay Risk- Minimum Regime Performance and the Durability of \|Measuring Strategy-Decay Risk]] — Strategies deteriorate. How to diagnose and quantify decay.

**Volatility and Risk**
- [[Rough volatility dynamics in commodity markets\|Rough Volatility in Commodity Markets]] — Rough volatility (Hurst exponent < 0.5) is an empirical regularity. This is the current direction of vol modeling beyond Heston.
- [[Generating Plausible Stress Scenarios via Large Deviations\|Stress Scenarios via Large Deviations]] — Large deviation theory for generating stress scenarios; more principled than historical or ad hoc scenarios.

**ML in Finance — What is Worth Your Time**

Be selective here. Most ML-in-finance papers overfit on historical data and underperform out-of-sample. The following are worth reading because they address methodology, not just application:
- [[Heads, Not Backbones- Output Heads Dominate Architectures on Fat-Tailed Returns\|Heads, Not Backbones]] — Architecture choices matter less than objective function and output head design for return prediction. Useful methodological finding.
- [[When Forecast Accuracy Fails- Rank Correlation and Decision Quality in Multi-Mar\|When Forecast Accuracy Fails]] — Forecast accuracy and decision quality diverge. The right metric for evaluating ML forecasts in finance is decision-relevant, not statistical.
- [[What Does Deep Hedging Actually Learn- Delta Corrections, Regime Fragility, and \|What Does Deep Hedging Actually Learn?]] — Deep hedging vs. BSM delta: when does it help and when does it overfit? Grounded critique of the deep hedging literature.

---

## Complete Sequenced Reading List

This is the canonical order. Follow it strictly through Phase 2, then branch into your Phase 3 track.

### Core Sequence (Phases 1-2, 30 papers, ~90 hours total)

1. [[Fama-1970-Efficient-Capital-Markets\|Fama (1970)]] — 2 hrs
2. [[Samuelson-1965-Proof-That-Properly-Anticipated-Prices\|Samuelson (1965)]] — 45 min
3. [[Lo-MacKinlay-1988-Stock-Prices-Do-Not-Follow-Random-Walks\|Lo & MacKinlay (1988)]] — 2 hrs
4. [[Cont-2001-Empirical-Properties-Asset-Returns-Stylized-Facts\|Cont (2001)]] — 2 hrs
5. [[Black-Scholes-1973-Pricing-of-Options-and-Corporate-Liabilities\|Black & Scholes (1973)]] — 6 hrs
6. [[Merton-1973-Theory-of-Rational-Option-Pricing\|Merton (1973)]] — 2.5 hrs
7. [[Harrison-Kreps-1979-Martingales-and-Arbitrage\|Harrison & Kreps (1979)]] — 1 hr
8. [[Markowitz-1952-Portfolio-Selection\|Markowitz (1952)]] — 4 hrs
9. [[Sharpe-1964-Capital-Asset-Prices\|Sharpe (1964)]] — 2 hrs
10. [[Ross-1976-Arbitrage-Theory-of-Capital-Asset-Pricing\|Ross (1976)]] — 2.5 hrs
11. [[Kelly-1956-New-Interpretation-of-Information-Rate\|Kelly (1956)]] — 1.5 hrs
12. [[Engle-1982-ARCH\|Engle (1982)]] — 2 hrs
13. [[Bollerslev-1986-GARCH\|Bollerslev (1986)]] — 1.5 hrs
14. [[Artzner-1999-Coherent-Measures-of-Risk\|Artzner et al. (1999)]] — 2.5 hrs
15. [[Rockafellar-Uryasev-2000-Optimization-of-CVaR\|Rockafellar & Uryasev (2000)]] — 2 hrs
16. [[Mandelbrot-1963-Variation-of-Certain-Speculative-Prices\|Mandelbrot (1963)]] — 1 hr
17. [[Fama-French-1992-Cross-Section-Expected-Stock-Returns\|Fama & French (1992)]] — 2.5 hrs
18. [[Fama-French-1993-Common-Risk-Factors\|Fama & French (1993)]] — 5 hrs
19. [[Carhart-1997-Persistence-in-Mutual-Fund-Performance\|Carhart (1997)]] — 2 hrs
20. [[Fama-French-2015-Five-Factor-Asset-Pricing-Model\|Fama & French (2015)]] — 1 hr
21. [[Banz-1981-Relationship-Return-Market-Value\|Banz (1981)]] — 45 min
22. [[Jegadeesh-Titman-1993-Returns-Buying-Winners-Selling-Losers\|Jegadeesh & Titman (1993)]] — 4 hrs
23. [[Gatev-Goetzmann-Rouwenhorst-2006-Pairs-Trading\|Gatev, Goetzmann & Rouwenhorst (2006)]] — 3 hrs
24. [[Grinold-1989-Fundamental-Law-Active-Management\|Grinold (1989)]] — 3 hrs
25. [[Kyle-1985-Continuous-Auctions-and-Insider-Trading\|Kyle (1985)]] — 5 hrs
26. [[Glosten-Milgrom-1985-Bid-Ask-Transaction-Prices\|Glosten & Milgrom (1985)]] — 2.5 hrs
27. [[Almgren-Chriss-2001-Optimal-Execution-Portfolio-Transactions\|Almgren & Chriss (2001)]] — 5 hrs
28. [[Heston-1993-Closed-Form-Solution-Options-Stochastic-Volatility\|Heston (1993)]] — 3 hrs
29. [[Vasicek-1977-Equilibrium-Characterization-Term-Structure\|Vasicek (1977)]] — 2 hrs
30. [[Lo-2002-Statistics-of-Sharpe-Ratios\|Lo (2002)]] — 2 hrs

---

## Fast Track: 3-Month Intensive Schedule

For a highly motivated person with 20+ hours per week available. Realistic for: full-time students, people between jobs, intensive self-study programs. This schedule is demanding — it will slip. Build in one free week at the end as buffer.

### Month 1: Foundation

| Week | Papers | Hours | Notes |
|------|--------|-------|-------|
| Week 1 | Fama (1970), Samuelson (1965), Lo-MacKinlay (1988), Cont (2001) | 8 hrs papers + 4 hrs textbook | Hull Ch.13 as weekend supplement |
| Week 2 | Black-Scholes (1973), Merton (1973), Harrison-Kreps (1979) | 10 hrs papers + 5 hrs textbook | Hull Ch.14-15 prerequisite; do BSM Implementation pass |
| Week 3 | Markowitz (1952), Sharpe (1964), Ross (1976), Kelly (1956) | 10 hrs papers + 4 hrs coding | Build efficient frontier; replicate Sharpe's CAPM regression |
| Week 4 | Engle (1982), Bollerslev (1986), Artzner (1999), Rockafellar-Uryasev (2000), Mandelbrot (1963) | 9 hrs papers + 3 hrs coding | Fit GARCH to equity returns; code up CVaR LP |

**Month 1 milestone:** You can derive Black-Scholes from the replication argument and explain the efficient frontier without notes.

### Month 2: Strategy

| Week | Papers | Hours | Notes |
|------|--------|-------|-------|
| Week 5 | FF (1992), FF (1993), Carhart (1997), FF (2015) | 11 hrs papers + 5 hrs coding | Download FF data; replicate factor construction |
| Week 6 | Banz (1981), Jegadeesh-Titman (1993), Gatev et al. (2006), Grinold (1989) | 11 hrs papers + 4 hrs coding | Replicate JT Table 1; code a simple pairs backtest |
| Week 7 | Kyle (1985), Glosten-Milgrom (1985), Almgren-Chriss (2001) | 12 hrs papers + 4 hrs coding | Implement Almgren-Chriss optimal trajectory |
| Week 8 | Heston (1993), Vasicek (1977), Heath-Jarrow-Morton (1992), Lo (2002) | 10 hrs papers + 3 hrs coding | Price bonds under Vasicek; apply Lo SR correction to a backtest |

**Month 2 milestone:** You can construct the Fama-French three factors from scratch and explain Kyle's lambda to a non-quant.

### Month 3: Specialization + Frontier

| Week | Papers | Hours | Notes |
|------|--------|-------|-------|
| Week 9 | Phase 3 track — papers 1-3 | 15 hrs papers + 5 hrs coding | All Implementation passes |
| Week 10 | Phase 3 track — papers 4-5 | 15 hrs papers + 5 hrs coding | Finish track |
| Week 11 | Phase 4 frontier (6-8 papers, Awareness level) | 10 hrs | Read broadly; take notes on research directions |
| Week 12 | Review + interview prep | Variable | Re-read abstracts and key results of all 30 core papers |

**Month 3 milestone:** You can speak credibly about current research in your specialization and explain two or three open problems in the area.

---

## Steady Track: 12-Month Schedule

For someone learning alongside work or other commitments. Assumes 8-10 hours per week consistently. This is more realistic for most people.

| Month | Phase | Papers | Focus |
|-------|-------|--------|-------|
| 1 | Phase 1 | Fama, Samuelson, Lo-MacKinlay, Cont | Market efficiency; stylized facts |
| 2 | Phase 1 | Black-Scholes, Merton, Harrison-Kreps | Derivatives pricing and risk-neutral measure |
| 3 | Phase 1 | Markowitz, Sharpe, Ross, Kelly | Portfolio theory and factor pricing |
| 4 | Phase 1 | Engle, Bollerslev, Artzner, Rockafellar-Uryasev, Mandelbrot | Risk and volatility |
| 5 | Phase 2 | FF (1992), FF (1993), Carhart, FF (2015) | Factor model evidence |
| 6 | Phase 2 | Banz, Jegadeesh-Titman, Gatev et al., Grinold | Anomalies and strategy |
| 7 | Phase 2 | Kyle, Glosten-Milgrom, Almgren-Chriss | Microstructure and execution |
| 8 | Phase 2 | Heston, Vasicek, HJM, Lo (2002) | Stochastic vol and rates |
| 9-11 | Phase 3 | Track-specific (5-7 papers) | Deep specialization |
| 12 | Phase 4 | Frontier papers (Awareness) | Current research |

**One rule for the steady track:** Do not skip weeks. A consistent 8 hours every week beats sporadic 20-hour sessions. Schedule specific blocks on your calendar and treat them as fixed.

---

## What Good Notes Look Like

After reading each paper, write down the following (takes 15-20 minutes):

1. **Question:** What problem was the paper trying to solve, stated in one sentence?
2. **Answer:** What did they find, stated in one or two sentences?
3. **Method:** How did they find it (model, data, estimator)?
4. **Assumptions:** What must be true for the result to hold? List the top 3.
5. **Limitations:** Where does this break in practice?
6. **My questions:** What would I need to check to believe this? What would extend it?

This note structure forces active reading. If you cannot fill in all six fields, you need to re-read. Papers where you can fill these in confidently are at Working Knowledge level.

---

## Common Mistakes

**Reading too broadly and too fast.** Skimming 50 papers gives you the ability to name-drop, not to do quant work. Depth on 20 papers is worth more than awareness of 200.

**Skipping the math because it is hard.** The math is the content. If you do not understand GARCH's log-likelihood or the Almgren-Chriss objective function, you do not understand the paper — you only know that a paper exists.

**Not coding.** Reading about Markowitz is not the same as building an efficient frontier and watching weights blow up when the covariance matrix is ill-conditioned. Implementation passes reveal failure modes that reading conceals.

**Reading out of order.** APT (Ross 1976) before CAPM (Sharpe 1964) is confusing. Heston before Black-Scholes is confusing. The sequence in this curriculum is not arbitrary — it follows the intellectual dependencies of the field.

**Stopping at Phase 2 and calling it done.** Phase 2 gives you the vocabulary of the field. Phase 3 gives you something to contribute. The difference is what separates candidates who pass phone screens from those who get offers.

---

## Recommended Textbook Stack

Read these in parallel with the paper curriculum, not sequentially.

| Textbook | Role in Curriculum | Which Chapters |
|----------|--------------------|----------------|
| Hull — *Options, Futures & Other Derivatives* | BSM and derivatives mechanics | Ch. 13-15, 19-22 |
| Shreve — *Stochastic Calculus for Finance II* | Rigorous Ito/BSM foundations | Ch. 4-5 |
| Gatheral — *The Volatility Surface* | After Black-Scholes; vol surface mechanics | Ch. 1-4 |
| Lopez de Prado — *Advances in Financial Machine Learning* | Practical ML methods and backtesting | Ch. 1-5, 11 |
| Cartea, Jaimungal & Penalva — *Algorithmic and High-Frequency Trading* | Market making and execution theory | Ch. 4-8 |
| Campbell, Lo & MacKinlay — *The Econometrics of Financial Markets* | Empirical methods; the reference for Phase 2 | Ch. 2-5 |

Do not try to read any of these cover-to-cover. Read the chapters listed above alongside the relevant papers.

---

## Sequencing Rationale: The Intellectual Dependencies

The ordering in this curriculum is not alphabetical or chronological — it follows logical dependency:

- **Fama before Black-Scholes:** BSM assumes markets are frictionless and you can delta-hedge continuously. Fama tells you what that assumption implies about information in prices. Knowing EMH makes the BSM assumptions interpretable rather than arbitrary.
- **Markowitz before Fama-French:** The FF model is an equilibrium model. Equilibrium models extend Markowitz. You need the optimization problem before you can appreciate the equilibrium pricing result.
- **Engle before Artzner:** GARCH models the dynamic process. Artzner gives you the right objective function to use when measuring risk from that process. Method before evaluation.
- **Kyle before Almgren-Chriss:** Almgren-Chriss needs a price impact model. Kyle's lambda is that model. The AC framework is the optimization layer on top of Kyle's equilibrium.
- **Vasicek before HJM:** Vasicek is the simplest affine short-rate model. HJM is the framework that shows why Vasicek is a special case. Special case before general framework, always.

---

## Final Advice

The field has a long memory. Papers from 1952 (Markowitz), 1965 (Samuelson), and 1973 (Black-Scholes) are still live references in current research. The classics are classics because the problems they solve have not gone away — markets still have risk, options still need pricing, informed traders still move prices. Read them with the respect they deserve.

The frontier is exciting but unreliable. A paper published last month has not been replicated, critiqued, or stress-tested by the community. A paper from 1985 that is still cited has survived that process. Weight your reading accordingly: heavy on the classics, selective on the frontier.

Speed matters less than you think. A week spent implementing Almgren-Chriss in code is worth more than a month of reading abstracts. Go slow on the papers that are closest to your job.
