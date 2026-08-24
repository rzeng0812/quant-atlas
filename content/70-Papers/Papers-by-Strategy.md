---
type: index
title: "Papers by Strategy"
description: "All papers in the atlas organized by trading strategy and research domain"
tags: [index, papers, strategy-map]
created: 2026-08-23
---

# Papers by Strategy

A navigable map of all papers, organized by the strategy or research domain they belong to. Papers can appear in multiple sections where relevant.

> **Legend:** ⭐ = Foundational classic paper · 🤖 = ML/AI-focused · 🔬 = Primarily theoretical

---

## 1. Mathematical Foundations & Market Theory

*The bedrock: why markets price things the way they do, and what mathematical objects govern prices.*

| Paper | Key Idea |
|-------|----------|
| ⭐ [[Bachelier-1900-Theorie-de-la-Speculation\|Bachelier (1900)]] | First mathematical model of markets; Brownian motion for prices |
| ⭐ [[Samuelson-1965-Proof-That-Properly-Anticipated-Prices\|Samuelson (1965)]] | Proof that efficient prices fluctuate randomly; GBM justified |
| ⭐ [[Fama-1970-Efficient-Capital-Markets\|Fama (1970)]] | EMH formalized: weak / semi-strong / strong forms |
| ⭐ [[Harrison-Kreps-1979-Martingales-and-Arbitrage\|Harrison & Kreps (1979)]] | First FTAP: no-arbitrage ↔ risk-neutral measure |
| ⭐ [[Harrison-Pliska-1981-Martingales-and-Stochastic-Integrals\|Harrison & Pliska (1981)]] | Second FTAP: complete markets ↔ unique EMM |
| ⭐ [[Mandelbrot-1963-Variation-of-Certain-Speculative-Prices\|Mandelbrot (1963)]] | Fat tails in financial returns; Lévy stable distributions |
| ⭐ [[Cont-2001-Empirical-Properties-Asset-Returns-Stylized-Facts\|Cont (2001)]] | Stylized facts: fat tails, volatility clustering, leverage effect |
| ⭐ [[Lo-MacKinlay-1988-Stock-Prices-Do-Not-Follow-Random-Walks\|Lo & MacKinlay (1988)]] | Variance ratio test; rejects random walk for weekly returns |
| 🔬 [[Against a Universal Trading Strategy- No-Arbitrage, No-Free-Lunch, and Adversari\|Against a Universal Trading Strategy]] | No-arbitrage limits on universal strategies |
| 🔬 [[The Fundamental Theorem of Asset Pricing, Formalized in Lean 4\|FTAP Formalized in Lean 4]] | Machine-verified proof of FTAP |
| 🔬 [[Geometric Brownian motion with intermittent entries and exits\|GBM with Intermittent Entries/Exits]] | GBM extensions for interrupted trading |
| 🔬 [[Trends, Volatility, Correlations, and Critical Phenomena in Financial Markets\|Trends, Volatility & Critical Phenomena]] | Statistical physics perspective on market dynamics |

---

## 2. Portfolio Construction & Asset Allocation

*How to combine assets optimally: from mean-variance to RL-based allocation.*

### 2a. Classical Theory
| Paper | Key Idea |
|-------|----------|
| ⭐ [[Markowitz-1952-Portfolio-Selection\|Markowitz (1952)]] | Mean-variance optimization; the efficient frontier |
| ⭐ [[Sharpe-1964-Capital-Asset-Prices\|Sharpe (1964)]] | CAPM; beta as systematic risk; Security Market Line |
| ⭐ [[Lintner-1965-Security-Prices-Risk\|Lintner (1965)]] | Independent CAPM derivation; capital budgeting under risk |
| ⭐ [[Ross-1976-Arbitrage-Theory-of-Capital-Asset-Pricing\|Ross (1976)]] | APT; multi-factor pricing from no-arbitrage alone |
| ⭐ [[Kelly-1956-New-Interpretation-of-Information-Rate\|Kelly (1956)]] | Log-optimal position sizing; IR = IC × √BR precursor |
| ⭐ [[Grinold-1989-Fundamental-Law-Active-Management\|Grinold (1989)]] | Fundamental Law: IR = IC × √BR |
| ⭐ [[Lo-2002-Statistics-of-Sharpe-Ratios\|Lo (2002)]] | Sharpe ratio inference; autocorrelation adjustment |
| ⭐ [[Rockafellar-Uryasev-2000-Optimization-of-CVaR\|Rockafellar & Uryasev (2000)]] | CVaR as a linear program; tail-risk portfolio optimization |

### 2b. Modern / Quantitative
| Paper | Key Idea |
|-------|----------|
| [[Post-Screening Portfolio Selection\|Post-Screening Portfolio Selection]] | Portfolio selection after factor screening |
| [[Which Portfolios- The Construction Dependence of Factor Model Performance\|Which Portfolios?]] | How construction choices affect factor model results |
| [[Forecasting Tangency Portfolios and Investing in the Minimum Euclidean Distance \|Forecasting Tangency Portfolios]] | ML-forecasted tangency portfolios vs. min-distance benchmark |
| [[Asset allocation using a Markov process of clustered efficient frontier coeffici\|Markov-Clustered Efficient Frontier]] | Regime-switching efficient frontier allocation |
| [[Topological Risk Parity\|Topological Risk Parity]] | Risk parity via persistent homology |
| [[Hedging market risk and uncertainty via a robust portfolio approach\|Robust Portfolio Hedging]] | Robust optimization under model uncertainty |
| [[Portfolio Optimization under Fast and Slow Latent Mean-Reverting and Momentum Drift\|Portfolio Optimization: Mean-Reversion + Momentum]] | Optimal allocation with mixed signal types |
| [[Tail Risk Management with Puts and Trend Following- A CVaR Framework for Crashes and\|Tail Risk Management: Puts + Trend Following]] | CVaR-optimal combination of puts and trend strategies |
| [[Temperature Anomalies and Climate Physical Risk in Portfolio Construction\|Climate Physical Risk in Portfolios]] | Climate risk in asset allocation |
| 🤖 [[Multi periods mean-DCVaR optimization- a Recursive Neural Network resolution\|Multi-Period mean-DCVaR via RNN]] | Neural network solution to multi-period CVaR optimization |
| 🤖 [[Portfolio Optimization Proxies under Label Scarcity and Regime Shifts via Bayesi\|Portfolio Optimization under Regime Shifts]] | Bayesian approach to regime-robust portfolio construction |
| 🤖 [[Portfolio Optimization for Commodity ETFs under Heavy-Tailed Returns\|Commodity ETF Portfolio Optimization]] | Heavy-tail-aware commodity portfolio construction |
| 🤖 [[Deep Reinforcement Learning Framework for Diversified Portfolio Management Acros\|RL Portfolio Management]] | DRL for multi-asset portfolio management |
| 🤖 [[A Two-Stage Decision Support System for Sustainability-Aware Long Short Portfoli\|ESG Long-Short Portfolio System]] | Two-stage system for sustainable long-short portfolios |
| 🤖 [[End-to-End Parametric Portfolio Policies for Cross-Asset Futures Timing- When Do AI\|End-to-End Parametric Portfolio Policies]] | Parametric policies for AI-driven cross-asset futures timing |
| 🤖 [[The Self Driving Portfolio- Agentic Architecture for Institutional Asset Managem\|The Self-Driving Portfolio]] | Agentic LLM system for institutional asset management |
| 🤖 [[Designing Agentic AI-Based Screening for Portfolio Investment\|Agentic AI Screening for Portfolios]] | AI agent for investment screening and selection |
| 🤖 [[A Penalty-Free Pipeline for Direct Quantum-Annealer Portfolio Optimization\|Quantum Annealer Portfolio Optimization]] | D-Wave quantum approach to portfolio optimization |
| 🤖 [[Where the Quantum Lives in D-Wave Hybrid Portfolio Optimization\|Where Quantum Lives in D-Wave]] | Analysis of quantum vs. classical contributions in D-Wave hybrid |
| 🤖 [[Asymmetry PRISM- A CPU-GPU Portfolio Optimization Engine for Deadline-Bounded In\|Asymmetry PRISM]] | High-performance GPU portfolio optimization engine |
| 🤖 [[Investing Is Compression\|Investing Is Compression]] | Information-theoretic view of investment alpha |

---

## 3. Factor Investing (Equity)

*The cross-section of expected returns: which characteristics predict returns and why.*

| Paper | Key Idea |
|-------|----------|
| ⭐ [[Banz-1981-Relationship-Return-Market-Value\|Banz (1981)]] | Size effect: small-cap premium; first CAPM anomaly |
| ⭐ [[Fama-French-1992-Cross-Section-Expected-Stock-Returns\|Fama & French (1992)]] | CAPM failure; size + book-to-market predict returns |
| ⭐ [[Fama-French-1993-Common-Risk-Factors\|Fama & French (1993)]] | Three-factor model: MKT + SMB + HML |
| ⭐ [[Carhart-1997-Persistence-in-Mutual-Fund-Performance\|Carhart (1997)]] | Four-factor model: adds MOM; mutual fund alpha explained |
| ⭐ [[Fama-French-2015-Five-Factor-Asset-Pricing-Model\|Fama & French (2015)]] | Five-factor model: adds RMW (profitability) + CMA (investment) |
| [[The Co-Pricing Factor Zoo\|The Co-Pricing Factor Zoo]] | Revisiting which factors survive multiple testing |
| [[Interpretable Systematic Risk around the Clock\|Interpretable Systematic Risk around the Clock]] | Intraday factor exposures and risk decomposition |
| [[A Cap-Axis Integral Diagnostic of Factor Models\|Cap-Axis Integral Diagnostic of Factor Models]] | Diagnostic for factor model misspecification |
| [[Mislearning of Factor Risk Premia under Structural Breaks- A Misspecified Bayesi\|Mislearning of Factor Risk Premia]] | Bayesian factor learning under structural breaks |
| [[Continuous Timing Signals for Growth-Defensive Style Allocation- Factor Attribut\|Continuous Timing Signals for Style Allocation]] | Continuous factor timing for growth/defensive allocation |
| [[Shifting Correlations- How Trade Policy Uncertainty Alters stock-T bill Relation\|Shifting Correlations under Trade Policy Uncertainty]] | Policy uncertainty and factor correlation dynamics |
| [[Which Voices Move Markets- Speaker Identity and the Cross-Section of Post-Earnin\|Which Voices Move Markets?]] | Speaker identity as a cross-sectional signal post-earnings |
| 🤖 [[Supply Chain Propagation of Textual Signals- LLM Embeddings and Cross-Sectional Return\|Supply Chain LLM Signals]] | LLM embeddings on supply chain text for cross-sectional returns |

---

## 4. Momentum & Trend Following

*Exploiting price persistence across time horizons — from cross-sectional to CTA.*

| Paper | Key Idea |
|-------|----------|
| ⭐ [[Jegadeesh-Titman-1993-Returns-Buying-Winners-Selling-Losers\|Jegadeesh & Titman (1993)]] | Price momentum: past 3-12m winners outperform losers |
| [[Is Trend Still Your Friend-- A Microstructural Account of the Demise of Short-Term\|Is Trend Still Your Friend?]] | Microstructural explanation for momentum decay |
| [[Heads, Not Backbones- Output Heads Dominate Architectures on Fat-Tailed Returns\|Heads, Not Backbones]] | Architecture study: output heads matter most for fat-tailed signals |
| [[Global Persistence, Local Residual Structure- Forecasting Heterogeneous Investme\|Global Persistence, Local Residual Structure]] | Heterogeneous persistence in factor momentum forecasting |
| [[Tail Risk Management with Puts and Trend Following- A CVaR Framework for Crashes and\|Tail Risk Management: Puts + Trend Following]] | CVaR-optimal defensive tail hedging with trend overlay |
| [[End-to-End Parametric Portfolio Policies for Cross-Asset Futures Timing- When Do AI\|Parametric Policies for Futures Timing]] | When does AI beat classical trend for futures timing? |

---

## 5. Statistical Arbitrage & Mean Reversion

*Exploiting transient mispricings relative to a statistical equilibrium.*

| Paper | Key Idea |
|-------|----------|
| ⭐ [[Gatev-Goetzmann-Rouwenhorst-2006-Pairs-Trading\|Gatev, Goetzmann & Rouwenhorst (2006)]] | Pairs trading: distance-based stat arb; 11%/yr before costs |
| [[Measuring Strategy-Decay Risk- Minimum Regime Performance and the Durability of \|Measuring Strategy-Decay Risk]] | How strategies deteriorate across market regimes |
| [[Evaluating Structured Strategy Backtests- Peer Benchmarks, Regime Timing, and Li\|Evaluating Structured Strategy Backtests]] | Backtesting methodology with peer benchmarks |
| [[Signature-Based Optimal Execution for Statistical Arbitrage with Path-Dependent Trading\|Signature-Based Stat Arb Execution]] | Path signatures for optimal execution in stat arb strategies |
| [[Regime-Conditional Distributional Comparison of Trading Strategies- A GAMLSS-ZAGA\|Regime-Conditional Strategy Comparison]] | GAMLSS framework for comparing strategies across regimes |
| [[Portfolio Optimization under Fast and Slow Latent Mean-Reverting and Momentum Drift\|Portfolio Optimization: Mean-Reversion + Momentum]] | Optimal allocation with mean-reverting signals |
| [[The Virtue of Sparsity in Complexity\|The Virtue of Sparsity in Complexity]] | Sparse models for robust signal extraction |

---

## 6. Options & Derivatives Pricing

*From the BSM formula to deep hedging — models for valuing and hedging contingent claims.*

### 6a. Classical Models
| Paper | Key Idea |
|-------|----------|
| ⭐ [[Black-Scholes-1973-Pricing-of-Options-and-Corporate-Liabilities\|Black & Scholes (1973)]] | BSM formula; delta hedging; founded quantitative finance |
| ⭐ [[Merton-1973-Theory-of-Rational-Option-Pricing\|Merton (1973)]] | General option theory; American exercise; continuous-time |
| ⭐ [[Black-1976-Pricing-of-Commodity-Contracts\|Black (1976)]] | Black's model for futures options; standard for caps/floors |
| ⭐ [[Cox-Ross-Rubinstein-1979-Option-Pricing-Simplified-Approach\|Cox, Ross & Rubinstein (1979)]] | Binomial tree; risk-neutral pricing; American options |
| ⭐ [[Heston-1993-Closed-Form-Solution-Options-Stochastic-Volatility\|Heston (1993)]] | Stochastic volatility; characteristic function; vol smile |
| ⭐ [[Longstaff-Schwartz-2001-Valuing-American-Options-LSM\|Longstaff & Schwartz (2001)]] | LSM algorithm: American options via least-squares Monte Carlo |

### 6b. Computation & Extensions
| Paper | Key Idea |
|-------|----------|
| [[STN-GPR- A Singularity Tensor Network Framework for Efficient Option Pricing\|STN-GPR Option Pricing]] | Tensor network for efficient option pricing |
| [[Analytic Pricing of Bermudan Swaptions with Few Exercise Dates\|Analytic Bermudan Swaption Pricing]] | Closed-form approximation for Bermudan swaptions |
| [[Valuing American options and Flexible Forwards contracts in time-dependent model\|Valuing American Options in Time-Dependent Models]] | American options in models with time-varying parameters |
| [[Matrix Approximation of Bachelier Option Prices and Greeks under Stochastic Vola\|Matrix Approximation of Bachelier Prices]] | Efficient matrix methods for normal vol option pricing |
| [[Faster Monotone Implied Volatility Solver\|Faster Monotone Implied Vol Solver]] | Fast root-finding for implied volatility inversion |
| [[Explicit Rational Formulae for Bachelier (Normal) Implied Volatility\|Explicit Bachelier Implied Vol Formulae]] | Closed-form rational approximation for normal implied vol |
| [[Higher-order ATM asymptotics for the CGMY model via the characteristic function\|Higher-Order ATM Asymptotics (CGMY)]] | ATM vol asymptotics for infinite-activity Lévy models |
| [[From Arbitrage Removal to Density Extraction- A Model-Free Framework for Short-D\|Model-Free Density Extraction from Options]] | Extract risk-neutral densities without assuming a model |
| [[Hedging Maturity-Specific Risk in Forward Curve Derivatives under Stochastic Volatility\|Hedging Forward Curve Derivatives]] | Stochastic vol hedging for term structure derivatives |
| [[Semi-Static Variance-Optimal Hedging of Covariance Risk in Multi-Asset Derivativ\|Semi-Static Variance-Optimal Hedging]] | Hedging covariance risk in multi-asset derivatives |
| [[On options-driven realized volatility forecasting- Information gains via rough v\|Options-Driven Realized Vol Forecasting]] | Using option prices to improve realized vol forecasts |
| [[Pricing and Hedging Financial Derivatives in Merger-&Acquisition Deals with Pric\|M&A Derivatives Pricing]] | Pricing derivatives with price uncertainty in M&A contexts |
| [[Target Weight Mechanism doesn't make delta hedge easier\|Target Weight Mechanism and Delta Hedging]] | Analysis of target-weight rebalancing vs. delta hedging |
| [[Adaptive VaR Control for Standardized Option Books under Marking Frictions\|Adaptive VaR Control for Option Books]] | Dynamic VaR management for standardized option portfolios |

### 6c. Deep Hedging & ML Pricing
| Paper | Key Idea |
|-------|----------|
| 🤖 [[What Does Deep Hedging Actually Learn- Delta Corrections, Regime Fragility, and \|What Does Deep Hedging Actually Learn?]] | RL hedging vs. BSM delta: corrections, fragility, distillation |
| 🤖 [[Bridging Stochastic Control and Deep Hedging- Structural Priors for No-Transacti\|Bridging Stochastic Control and Deep Hedging]] | Structural priors to improve deep hedging generalization |

---

## 7. Volatility Strategies & Modeling

*Understanding and trading volatility: from GARCH to rough vol to vol arb.*

| Paper | Key Idea |
|-------|----------|
| ⭐ [[Engle-1982-ARCH\|Engle (1982)]] | ARCH: time-varying conditional variance; volatility clustering |
| ⭐ [[Bollerslev-1986-GARCH\|Bollerslev (1986)]] | GARCH(1,1): parsimonious volatility persistence |
| [[Rough volatility dynamics in commodity markets\|Rough Volatility in Commodity Markets]] | Rough volatility estimation for commodity derivatives |
| [[Do Better Volatility Forecasts Lead to Better Portfolios- Evidence from Graph Ne\|Better Vol Forecasts → Better Portfolios?]] | Graph neural network vol forecasting for portfolio optimization |
| [[A Hybrid Gaussian Process Regression Framework for Stable Volatility-Covariance \|Hybrid GPR for Volatility-Covariance]] | Gaussian process for joint vol + covariance estimation |
| [[Continuous Hidden Markov Models for Equity Returns- Heavy-Tail Emission Families\|HMM for Equity Returns]] | HMM regime detection with heavy-tailed emission distributions |
| [[Real-time identification of the onset of financial rogue waves\|Real-Time Financial Rogue Wave Detection]] | Early warning system for extreme vol events |
| [[Trends, Volatility, Correlations, and Critical Phenomena in Financial Markets\|Trends, Volatility & Critical Phenomena]] | Vol and correlation dynamics near market tipping points |
| 🤖 [[Risk-Sensitive Specialist Routing for Volatility Forecasting\|Risk-Sensitive Specialist Routing]] | Mixture-of-experts routing for vol forecasting |
| 🤖 [[Do Prediction Markets Forecast Cryptocurrency Volatility- Evidence from Kalshi M\|Prediction Markets for Crypto Vol]] | Kalshi prediction markets as crypto vol forecasters |
| 🤖 [[On options-driven realized volatility forecasting- Information gains via rough v\|Options-Driven Realized Vol Forecasting]] | Rough vol + options data for realized vol prediction |

---

## 8. Fixed Income & Interest Rate Strategies

*Term structure models, bond pricing, duration management, and rate derivatives.*

| Paper | Key Idea |
|-------|----------|
| ⭐ [[Vasicek-1977-Equilibrium-Characterization-Term-Structure\|Vasicek (1977)]] | Mean-reverting short rate; first affine term structure model |
| ⭐ [[Cox-Ingersoll-Ross-1985-Theory-Term-Structure-Interest-Rates\|Cox, Ingersoll & Ross (1985)]] | CIR model: non-negative rates; square-root process |
| ⭐ [[Hull-White-1990-Pricing-Interest-Rate-Derivative-Securities\|Hull & White (1990)]] | Extended Vasicek; calibrates to market curve; industry standard |
| ⭐ [[Heath-Jarrow-Morton-1992-Bond-Pricing-Term-Structure\|Heath, Jarrow & Morton (1992)]] | HJM: forward rate dynamics; unifies all short-rate models |
| ⭐ [[Black-1976-Pricing-of-Commodity-Contracts\|Black (1976)]] | Black's model: caps, floors, swaptions (standard for rates) |
| [[Data-Driven Duration Management -- Term Structure Forecasting Using Machine Lear\|Data-Driven Duration Management]] | ML for yield curve forecasting and duration positioning |
| [[Orthogonal reparametrization of the Nelson-Siegel-Svensson interest rate curve m\|Nelson-Siegel-Svensson Reparametrization]] | Better parameterization of the NS-S yield curve model |
| [[Priced risk in corporate bonds\|Priced Risk in Corporate Bonds]] | Factor analysis of risk premia in corporate bond returns |
| [[The Corporate Bond Factor Replication Crisis\|Corporate Bond Factor Replication Crisis]] | Replication failure for published corporate bond factors |
| [[Analytic Pricing of Bermudan Swaptions with Few Exercise Dates\|Analytic Bermudan Swaption Pricing]] | Closed-form approximation for few-exercise Bermudan swaptions |

---

## 9. Credit Risk & Structured Products

*Modeling default, pricing credit derivatives, and structured credit.*

| Paper | Key Idea |
|-------|----------|
| ⭐ [[Merton-1974-Pricing-Corporate-Debt\|Merton (1974)]] | Structural credit model: equity as call option on firm assets |
| ⭐ [[Jarrow-Turnbull-1995-Pricing-Derivatives-Credit-Risk\|Jarrow & Turnbull (1995)]] | Reduced-form credit: Poisson default intensity |
| ⭐ [[Duffie-Singleton-1999-Modeling-Term-Structures-Defaultable-Bonds\|Duffie & Singleton (1999)]] | Affine defaultable bond pricing; credit spread = Lλ |
| [[When AAA Satisfies Nothing- Impossibility Theorems for Structured Credit Ratings\|When AAA Satisfies Nothing]] | Impossibility theorems for structured credit ratings |
| [[Temporal Coarse-Graining of Multi-Sector Default Count Data Generates Posterior-\|Temporal Coarse-Graining of Default Data]] | Bayesian posterior for default count data across sectors |
| [[Contagion or Macroeconomic Fluctuations- Identifiability in Aggregated Default D\|Contagion vs. Macro Fluctuations]] | Identifying contagion vs. macro effects in default clustering |
| [[A Counterfactual Diagnostic Framework for Explaining KS Deterioration in Credit \|Counterfactual Diagnostics for Credit Models]] | Explaining KS stat deterioration in credit scorecards |
| [[Transfer Learning for Loan Recovery Prediction under Distribution Shifts with He\|Transfer Learning for Loan Recovery]] | Transfer learning for credit recovery prediction |
| [[Semi-structured multi-state delinquency model for mortgage default\|Multi-State Mortgage Delinquency Model]] | Semi-structured model for mortgage default transitions |
| [[Modeling dependency between operational risk losses and macroeconomic variables \|Operational Risk and Macro Dependencies]] | Linking operational risk losses to macroeconomic factors |
| [[Vault as a credit instrument\|Vault as a Credit Instrument]] | Crypto vault mechanics as a credit product |
| [[Climate-Aware Copula Models for Sovereign Rating Migration Risk\|Climate-Aware Sovereign Rating Migration]] | Climate scenarios in sovereign credit rating models |
| [[The Corporate Bond Factor Replication Crisis\|Corporate Bond Factor Replication Crisis]] | Replication failures in corporate bond factor research |

---

## 10. Market Making & High-Frequency Trading

*The microstructure of price formation: order books, spreads, and information.*

### 10a. Foundational Models
| Paper | Key Idea |
|-------|----------|
| ⭐ [[Kyle-1985-Continuous-Auctions-and-Insider-Trading\|Kyle (1985)]] | Kyle's λ: insider trading model; constant market depth |
| ⭐ [[Glosten-Milgrom-1985-Bid-Ask-Transaction-Prices\|Glosten & Milgrom (1985)]] | Bid-ask spread from adverse selection; sequential trade model |
| ⭐ [[Avellaneda-Stoikov-2008-High-Frequency-Trading-Limit-Order-Book\|Avellaneda & Stoikov (2008)]] | Stochastic control for market making; reservation price |

### 10b. Extensions & Empirical
| Paper | Key Idea |
|-------|----------|
| [[Bond Market Making with a Hit-Ratio Target\|Bond Market Making with Hit-Ratio Target]] | Optimal bond market making with execution rate constraint |
| [[Early Detection of Latent Microstructure Regimes in Limit Order Books\|Early Detection of LOB Regimes]] | Detecting hidden regime changes in the limit order book |
| [[Bridging the Reality Gap in Limit Order Book Simulation\|Bridging the Reality Gap in LOB Simulation]] | Calibrated LOB simulation for market making research |
| [[The Privacy Subsidy- Kyle's $λ$ under Noise-Perturbed Order-Flow Observation\|Privacy Subsidy: Kyle's λ]] | Effect of noisy order flow observation on Kyle's λ |
| [[The Privacy Subsidy in Glosten-Milgrom- Bid-Ask Spread and Welfare under Flip-No\|Privacy Subsidy: Glosten-Milgrom]] | Welfare effects of flip-noise on Glosten-Milgrom spreads |
| [[Flexible Information Acquisition in the Kyle Model\|Flexible Information Acquisition (Kyle)]] | Endogenous information acquisition in Kyle's model |
| [[Mandatory Disclosure in Oligopolistic Market Making\|Mandatory Disclosure in Market Making]] | Disclosure rules in oligopolistic dealer markets |
| [[When large trades are not news- Liquidity tail risk and price discovery\|When Large Trades Are Not News]] | Liquidity tail risk and the information content of block trades |
| [[The Bounce Has No Direction- Sign, Magnitude, and the Microstructure of Equity Return\|The Bounce Has No Direction]] | Bid-ask bounce decomposition in equity microstructure |
| [[Forecasting duration in high-frequency financial data using a self-exciting flex\|Forecasting Duration in HF Data]] | ACD model extensions for intraday trade timing |
| [[Is Trend Still Your Friend-- A Microstructural Account of the Demise of Short-Term\|Is Trend Still Your Friend?]] | Microstructural explanation for short-term momentum decay |
| [[Empirical Confirmation of the Square-Root Law of Market Impact in a U.S. Large-C\|Square-Root Law of Market Impact]] | Empirical confirmation of concave price impact |
| 🤖 [[The Inference-Compute Frontier and a Latency-Efficient Architecture for Limit Or\|Inference-Compute Frontier for LOB]] | ML architecture for latency-efficient LOB prediction |
| 🤖 [[KineticSim- A Lightweight, High-Performance Execution Engine for Real-Time Marke\|KineticSim]] | High-performance simulation engine for real-time market making |
| 🤖 [[Testing replication for an agent-based model of market fragmentation and latency\|Agent-Based Market Fragmentation Model]] | Agent-based model of fragmentation and latency effects |
| 🤖 [[Sequential Structure in Intraday Futures Data- LSTM vs Gradient Boosting on MNQ\|Sequential Structure in Intraday Futures]] | LSTM vs. gradient boosting for intraday futures prediction |

---

## 11. Optimal Execution & Transaction Costs

*How to trade large orders without moving the market against yourself.*

| Paper | Key Idea |
|-------|----------|
| ⭐ [[Almgren-Chriss-2001-Optimal-Execution-Portfolio-Transactions\|Almgren & Chriss (2001)]] | Optimal execution: mean-variance tradeoff over trajectories |
| ⭐ [[Brunnermeier-Pedersen-2009-Market-Liquidity-Funding-Liquidity\|Brunnermeier & Pedersen (2009)]] | Liquidity spirals: market and funding liquidity feedback |
| [[Model Predictive Control For Trade Execution\|Model Predictive Control for Execution]] | MPC framework for adaptive execution in dynamic markets |
| [[Empirical Confirmation of the Square-Root Law of Market Impact in a U.S. Large-C\|Square-Root Law of Market Impact]] | Empirical square-root impact law; Almgren-Chriss calibration |
| [[Signature-Based Optimal Execution for Statistical Arbitrage with Path-Dependent Trading\|Signature-Based Optimal Execution]] | Path signatures for stat arb execution optimization |
| [[Liquidity Premium and Investment Horizons\|Liquidity Premium and Investment Horizons]] | How investment horizon affects the liquidity risk premium |

---

## 12. Risk Management

*Measuring, quantifying, and managing tail risk, systemic risk, and portfolio risk.*

### 12a. Risk Measure Theory
| Paper | Key Idea |
|-------|----------|
| ⭐ [[Artzner-1999-Coherent-Measures-of-Risk\|Artzner et al. (1999)]] | Coherent risk measures; VaR not coherent; ES is |
| ⭐ [[Rockafellar-Uryasev-2000-Optimization-of-CVaR\|Rockafellar & Uryasev (2000)]] | CVaR as a linear program |
| [[The Risk Quadrangle in Optimization- An Overview with Recent Results and Extensi\|The Risk Quadrangle]] | Unified framework: risk, deviation, regret, error quadrangle |
| [[Biased Mean Quadrangle and Applications\|Biased Mean Quadrangle]] | Extensions to the risk quadrangle with biased mean |
| [[On Prudence of Risk Measures\|On Prudence of Risk Measures]] | Prudence properties of risk measures under uncertainty |
| [[Geometrically convex return risk measures on AM-algebras\|Geometrically Convex Risk Measures]] | Abstract algebraic framework for return-based risk measures |
| [[Absolute Continuity of Monotone Aggregations under Positive Regression Dependenc\|Absolute Continuity of Monotone Aggregations]] | Mathematical properties of risk measure aggregation |
| [[Universal Value-at-Risk superadditivity\|Universal VaR Superadditivity]] | Conditions under which VaR fails subadditivity universally |
| [[Lambda Rényi entropic value-at-risk\|Lambda Rényi Entropic VaR]] | Rényi entropy-based risk measure generalizing CVaR |
| [[Ranking Metrics- Extending Acceptability and Performance Indexes\|Ranking Metrics: Acceptability Indexes]] | Extending performance indexes to rank risky prospects |
| [[Joint Exclusivity\|Joint Exclusivity]] | Probability bounds for joint tail events |

### 12b. Tail Risk & Systemic Risk
| Paper | Key Idea |
|-------|----------|
| [[Modeling and Forecasting Tail Risk Spillovers- A Component-Based CAViaR Approach\|Tail Risk Spillovers via CAViaR]] | Component CAViaR for tail risk contagion |
| [[Tail copula representation of path-based maximal tail dependence\|Tail Copula and Path-Based Tail Dependence]] | Path-based characterization of maximal tail dependence |
| [[Hidden Dependence and Aggregate Tail Risk\|Hidden Dependence and Aggregate Tail Risk]] | Latent dependence structures in portfolio tail risk |
| [[Identifying dynamical network markers of financial market instability\|Dynamical Network Markers of Instability]] | Network-based early warning indicators of financial crises |
| [[Budgeted Robust Intervention Design for Financial Networks with Common Asset Exp\|Robust Intervention in Financial Networks]] | Optimal interventions in contagion networks |
| [[Asymptotic Behaviour of Unexpected Losses and Risk Ratios for Co-Monotonic Alter\|Asymptotics of Unexpected Losses]] | Limiting behavior of portfolio losses under co-monotonicity |
| [[Generating Plausible Stress Scenarios via Large Deviations\|Stress Scenarios via Large Deviations]] | Large deviation theory for generating financial stress scenarios |
| [[The Geometry of Risk- Path-Dependent Regulation and Anticipatory Hedging via the\|The Geometry of Risk]] | Path-dependent regulation and optimal anticipatory hedging |

### 12c. Portfolio Risk
| Paper | Key Idea |
|-------|----------|
| [[On the Structure of Risk Contribution- A Leave-One-Out Decomposition into Inhere\|Structure of Risk Contribution]] | LOO decomposition of portfolio risk into inherent + interaction |
| [[Capital-Allocation-Induced Risk Sharing\|Capital-Allocation-Induced Risk Sharing]] | How capital allocation rules induce risk sharing |
| [[Pareto Optimal Centralized Risk Sharing with Multiple Agents- Inclusivity and Fa\|Pareto Optimal Risk Sharing]] | Centralized risk sharing with multiple agents |
| [[Financial Resilience Evaluation- From Conditional Expectations to Dynamic Convex Risk\|Financial Resilience Evaluation]] | Dynamic convex risk measures for financial resilience |
| [[Robust Hedging Valuation Adjustment under Liquidity--Demand Stress\|Robust Hedging Valuation Adjustment]] | XVA under liquidity and demand stress |
| [[Reliability-Aware ETF Tail-Risk Monitoring\|Reliability-Aware ETF Tail-Risk Monitoring]] | Tail risk monitoring framework for ETF portfolios |
| [[Climate Risk Stress Testing in California- A Geospatial Framework for Banking an\|Climate Risk Stress Testing]] | Geospatial framework for climate stress testing in banking |
| [[Mislearning of Factor Risk Premia under Structural Breaks- A Misspecified Bayesi\|Mislearning of Factor Risk Premia]] | Bayesian misspecification under structural breaks in factor risk |

---

## 13. Systematic / ML-Driven Strategies

*Machine learning and AI applied to alpha generation, signal processing, and trading.*

### 13a. NLP & Alternative Data
| Paper | Key Idea |
|-------|----------|
| 🤖 [[Cross-Stock Predictability via LLM-Augmented Semantic Networks\|Cross-Stock Predictability via LLM Networks]] | LLM semantic graphs for cross-asset return predictability |
| 🤖 [[Learning to Aggregate Zero-Shot LLM Agents for Corporate Disclosure Classificati\|LLM Agents for Corporate Disclosure]] | Zero-shot LLM ensemble for NLP-based signal extraction |
| 🤖 [[Supply Chain Propagation of Textual Signals- LLM Embeddings and Cross-Sectional Return\|Supply Chain LLM Signals]] | Text embeddings for supply chain signal propagation |
| 🤖 [[Which Voices Move Markets- Speaker Identity and the Cross-Section of Post-Earnin\|Which Voices Move Markets?]] | Speaker identity as earnings call signal |
| 🤖 [[Signal or Noise in Multi-Agent LLM-based Stock Recommendations-\|Signal or Noise in LLM Recommendations?]] | Evaluating information content of LLM stock recommendations |
| 🤖 [[Shapley in Context- Explaining Financial Language with Domain Expertise\|Shapley in Context: Financial NLP]] | SHAP explanations for financial language models |
| 🤖 [[Debiasing LLMs by Fine-tuning\|Debiasing LLMs by Fine-Tuning]] | Reducing bias in LLMs for financial applications |

### 13b. Reinforcement Learning
| Paper | Key Idea |
|-------|----------|
| 🤖 [[Reinforcement Learning for Speculative Trading under Exploratory Framework\|RL for Speculative Trading]] | Entropy-regularized RL for speculative trading |
| 🤖 [[Anticipatory Reinforcement Learning- From Generative Path-Laws to Distributional\|Anticipatory RL]] | RL with anticipatory reward shaping via path-law generation |
| 🤖 [[Reinforcement Learning for Risk-Sensitive Investment Management- a Free Energy--\|RL for Risk-Sensitive Investment Management]] | Free energy RL framework for risk-sensitive portfolio management |
| 🤖 [[OOM-RL- Out-of-Money Reinforcement Learning Market-Driven Alignment for LLM-Base\|OOM-RL: LLM-Based Options Trading]] | RL alignment for LLM-based options trading |
| 🤖 [[Deep Reinforcement Learning Framework for Diversified Portfolio Management Acros\|DRL Portfolio Management]] | Multi-asset DRL for diversified portfolio management |
| 🤖 [[FinRL-X- An AI-Native Modular Infrastructure for Quantitative Trading\|FinRL-X]] | Modular AI-native infrastructure for quant trading |

### 13c. ML Models & Forecasting
| Paper | Key Idea |
|-------|----------|
| 🤖 [[Machine Spirits- Speculation and Adaptation of LLM Agents in Asset Markets\|Machine Spirits: LLM Agents in Markets]] | LLM agents in simulated asset markets; speculation dynamics |
| 🤖 [[Heads, Not Backbones- Output Heads Dominate Architectures on Fat-Tailed Returns\|Heads, Not Backbones]] | Output head design dominates backbone choice for return prediction |
| 🤖 [[Adaptive AI Delegation under Uncertainty- A Bayesian Governance Policy for Sequential\|Adaptive AI Delegation]] | Bayesian policy for delegating to AI agents under uncertainty |
| 🤖 [[Endogenous Randomness from Adversarial Market Learning\|Endogenous Randomness from Adversarial Learning]] | How adversarial learning generates market randomness |
| 🤖 [[How to spot outliers- an Ensemble Anomaly Detection Framework\|Ensemble Anomaly Detection]] | Ensemble approach for outlier detection in financial data |
| 🤖 [[Attributing Forecast Gaps to Component Models in Complex Model Suites\|Attributing Forecast Gaps]] | Model attribution for ensemble forecast decomposition |
| 🤖 [[When Forecast Accuracy Fails- Rank Correlation and Decision Quality in Multi-Mar\|When Forecast Accuracy Fails]] | Rank correlation vs. accuracy as decision quality metric |
| 🤖 [[Sequential Structure in Intraday Futures Data- LSTM vs Gradient Boosting on MNQ\|Sequential Structure in Intraday Futures]] | LSTM vs. XGBoost for micro-futures intraday prediction |
| 🤖 [[Risk-Sensitive Specialist Routing for Volatility Forecasting\|Risk-Sensitive Specialist Routing]] | MoE routing for vol forecasting |
| 🤖 [[The Self Driving Portfolio- Agentic Architecture for Institutional Asset Managem\|Self-Driving Portfolio]] | Agentic AI for institutional asset management |
| 🤖 [[PolySwarm- A Multi-Agent Large Language Model Framework for Prediction Market Tr\|PolySwarm: LLM Prediction Market Trading]] | Multi-agent LLM framework for prediction market trading |

---

## 14. Crypto & DeFi

*Automated market makers, on-chain risk, MEV, and crypto-native strategies.*

### 14a. Automated Market Makers (AMMs)
| Paper | Key Idea |
|-------|----------|
| [[Option Pricing on Automated Market Maker Tokens\|Option Pricing on AMM Tokens]] | Applying option theory to AMM LP positions |
| [[A Unified General Formula for Arbitrary Liquidity Operations in Weighted AMMs- P\|Unified Formula for Weighted AMMs]] | General liquidity operation formula for weighted AMMs |
| [[Concave Continuation- Linking Routing to Arbitrage\|Concave Continuation: Routing to Arbitrage]] | Routing arbitrage in AMM networks as a concave program |
| [[Mitigating Adverse Selection in Concentrated Liquidity AMMs with Dynamic Fees- A\|Mitigating Adverse Selection in CLMM]] | Dynamic fee mechanisms to reduce LP adverse selection |
| [[Optimal Dynamic Fees for Automated Market Makers- A Stochastic Control Approach \|Optimal Dynamic AMM Fees]] | Stochastic control for optimal AMM fee setting |

### 14b. On-Chain Risk & Regulation
| Paper | Key Idea |
|-------|----------|
| [[The Viability of Blockchain Markets under Discrete Clearing and Paid Priority\|Viability of Blockchain Markets]] | Market viability with discrete clearing and paid ordering |
| [[Transaction Costs and Speed in the Ethereum Ecosystem- Scalability of the Mainne\|Transaction Costs in Ethereum]] | Empirical analysis of Ethereum gas costs and scalability |
| [[Time-dependent weighted directed networks of cryptocurrency interaction from hig\|Crypto Interaction Networks (HFT)]] | High-frequency network analysis of crypto asset interactions |
| [[On-chain Peak Shaving\|On-Chain Peak Shaving]] | Demand management for blockchain network congestion |
| [[Common Risk Factors in Decentralized AI Subnets\|Risk Factors in Decentralized AI Subnets]] | Factor model for DeFi AI subnet token returns |
| [[Imperfect Commitment in Maximal Extractable Value Auctions\|MEV Auction Design]] | Game theory of MEV auctions with imperfect commitment |
| 🤖 [[DeXposure-Claw- An Agentic System for DeFi Risk Supervision\|DeXposure-Claw: DeFi Risk Supervision]] | Agentic system for DeFi risk monitoring |
| [[PEB Separation and State Migration- Unmasking the New Frontiers of DeFi AML Evas\|DeFi AML Evasion]] | Privacy mechanisms and AML evasion in DeFi |

### 14c. Prediction Markets
| Paper | Key Idea |
|-------|----------|
| [[Do Prediction Markets Match Option Prices- Bitcoin Threshold Evidence from Binan\|Prediction Markets vs. Option Prices]] | Comparing Binance prediction markets to option-implied prices |
| [[Settlement Manipulation in Prediction Markets\|Settlement Manipulation in Prediction Markets]] | Strategic manipulation of prediction market settlement |
| [[What Happens When Institutional Liquidity Enters Prediction Markets- Identificat\|Institutional Liquidity in Prediction Markets]] | Price impact of institutional participation in prediction markets |
| 🤖 [[Do Prediction Markets Forecast Cryptocurrency Volatility- Evidence from Kalshi M\|Prediction Markets for Crypto Vol]] | Kalshi markets as crypto volatility forecasters |
| 🤖 [[PolySwarm- A Multi-Agent Large Language Model Framework for Prediction Market Tr\|PolySwarm]] | Multi-agent LLM framework for prediction market trading |

---

## 15. Commodities & Energy

*Futures, seasonality, spread strategies, and energy trading.*

| Paper | Key Idea |
|-------|----------|
| [[Hierarchical Graph Learning for Calendar Spread Strategies in Commodity Futures \|Graph Learning for Commodity Calendar Spreads]] | GNN for calendar spread strategy in commodity futures |
| [[Rough volatility dynamics in commodity markets\|Rough Volatility in Commodity Markets]] | Rough Heston calibration for commodity options |
| [[Approximate Dynamic Programming for Degradation-aware Market Participation of Ba\|ADP for Battery Market Participation]] | Battery storage dispatch optimization in energy markets |
| [[Probabilistic Forecasting for Day-ahead Electricity Prices, Battery Trading Stra\|Probabilistic Electricity Price Forecasting]] | Probabilistic forecasting for day-ahead power + battery trading |

---

## 16. Insurance, Actuarial & Risk-Sharing

*Actuarial risk, reinsurance structures, and insurance-linked products.*

| Paper | Key Idea |
|-------|----------|
| [[Endogenous Reinsurance Pricing in Large Competitive Insurance Markets- Finite-Pl\|Endogenous Reinsurance Pricing]] | Mean-field game model for reinsurance market equilibrium |
| [[Optimal Dividend, Reinsurance, and Capital Injection for Collaborating Business \|Optimal Dividend, Reinsurance & Capital Injection]] | Cramér-Lundberg framework for collaborative business units |
| [[Optimal Insurance Menu Design under the Expected-Value Premium Principle\|Optimal Insurance Menu Design]] | Mechanism design for insurance contracts under EV principle |
| [[Dividend ratcheting and capital injection under the Cramér-Lundberg model- Stron\|Dividend Ratcheting under Cramér-Lundberg]] | Ratchet dividend constraints in insurance surplus models |
| [[Strategic Risk Reduction- Self-Protection and Self-Insurance\|Strategic Risk Reduction]] | Self-protection vs. self-insurance tradeoffs |
| [[On the Expected Maximum Deficit and the Optimal Allocation of Reserves\|Expected Maximum Deficit & Reserve Allocation]] | Optimal reserve allocation for maximum deficit minimization |
| [[Balancing Shareholder Value and Financial Stability under a Reduced-Form Liquidation Model\|Shareholder Value vs. Financial Stability]] | Reduced-form model for bank liquidation and capital policy |
| [[Capital-Allocation-Induced Risk Sharing\|Capital-Allocation-Induced Risk Sharing]] | Risk sharing properties of internal capital allocation |
| [[Mortality Heterogeneity and Actuarial Fairness in China's Notional Defined Contr\|Mortality Heterogeneity & Actuarial Fairness]] | Longevity risk heterogeneity in pension system design |
| [[A Censored Transformed Model for Proportional Outcomes with Boundary Mass and an\|Censored Transformed Model for Proportional Outcomes]] | Statistical model for bounded actuarial outcomes |
| [[Revealing Geography-Driven Signals in Zone-Level Claim Frequency Models- An Empi\|Geography-Driven Signals in Claim Frequency]] | Spatial signal extraction for P&C insurance claim modeling |
| [[Your SaaS Is an Insurance Product- A Modeling Framework\|SaaS as an Insurance Product]] | Applying actuarial methods to SaaS subscription churn risk |
| [[Sequential Audit Sampling with Statistical Guarantees\|Sequential Audit Sampling]] | Sequential sampling design with statistical coverage guarantees |

---

## 17. Mathematical & Computational Finance

*Numerical methods, measure theory, and mathematical tools for derivatives.*

| Paper | Key Idea |
|-------|----------|
| [[Diagonal Frog- High-order positivity-preserving FD schemes for anisotropic Fokke\|Diagonal Frog: High-Order FD Schemes]] | Positivity-preserving finite-difference PDE schemes |
| [[Mean Field Equilibrium Asset Pricing Models With Exponential Utility\|Mean Field Asset Pricing]] | Mean field game approach to equilibrium asset pricing |
| [[A sharp order-three obstruction to the aggregation of conditional price-of-risk \|Order-Three Obstruction to Price-of-Risk Aggregation]] | Mathematical obstruction in risk premium aggregation |
| [[Optimal Order of Multi-Agent and General Many-Body Systems\|Optimal Order of Multi-Agent Systems]] | Mean-field optimal control for multi-agent financial systems |
| [[Risk-Sensitive Investment Management via Free Energy-Entropy Duality\|Risk-Sensitive Investment via Free Energy]] | Free energy-entropy duality for risk-sensitive portfolio control |
| [[Asymmetry PRISM- A CPU-GPU Portfolio Optimization Engine for Deadline-Bounded In\|Asymmetry PRISM]] | GPU-accelerated optimization for real-time portfolio problems |
| 🔬 [[The Fundamental Theorem of Asset Pricing, Formalized in Lean 4\|FTAP Formalized in Lean 4]] | Computer-verified proof of the First FTAP |
| [[Valuation Reveals Uncertainty\|Valuation Reveals Uncertainty]] | Information-theoretic link between valuation and uncertainty |
| [[Optimal Parlay Wagering and Whitrow Asymptotics- A State-Price and Implicit-Cash\|Optimal Parlay Wagering]] | Kelly-optimal parlay betting with state-price interpretation |
| [[Risk-Constrained Kelly for Mutually Exclusive Outcomes- CRRA Support Invariance \|Risk-Constrained Kelly]] | Kelly criterion under CRRA utility with risk constraints |
| [[$α$-robust utility maximization with intractable claims- A quantile optimization\|α-Robust Utility Maximization]] | Robust utility max for hard-to-hedge claims via quantile methods |

---

## Cross-Reference: Foundational Paper Reading Order

If you're new to quant finance, read the classics in this order:

1. **Probability & Markets:** [[Bachelier-1900-Theorie-de-la-Speculation|Bachelier]] → [[Samuelson-1965-Proof-That-Properly-Anticipated-Prices|Samuelson]] → [[Fama-1970-Efficient-Capital-Markets|Fama (1970)]]
2. **Portfolio:** [[Markowitz-1952-Portfolio-Selection|Markowitz]] → [[Sharpe-1964-Capital-Asset-Prices|Sharpe]] → [[Ross-1976-Arbitrage-Theory-of-Capital-Asset-Pricing|Ross APT]] → [[Fama-French-1993-Common-Risk-Factors|FF3]]
3. **Options:** [[Black-Scholes-1973-Pricing-of-Options-and-Corporate-Liabilities|Black-Scholes]] → [[Merton-1973-Theory-of-Rational-Option-Pricing|Merton (1973)]] → [[Harrison-Kreps-1979-Martingales-and-Arbitrage|Harrison-Kreps]] → [[Heston-1993-Closed-Form-Solution-Options-Stochastic-Volatility|Heston]]
4. **Rates:** [[Vasicek-1977-Equilibrium-Characterization-Term-Structure|Vasicek]] → [[Cox-Ingersoll-Ross-1985-Theory-Term-Structure-Interest-Rates|CIR]] → [[Hull-White-1990-Pricing-Interest-Rate-Derivative-Securities|Hull-White]] → [[Heath-Jarrow-Morton-1992-Bond-Pricing-Term-Structure|HJM]]
5. **Microstructure:** [[Kyle-1985-Continuous-Auctions-and-Insider-Trading|Kyle]] → [[Glosten-Milgrom-1985-Bid-Ask-Transaction-Prices|Glosten-Milgrom]] → [[Almgren-Chriss-2001-Optimal-Execution-Portfolio-Transactions|Almgren-Chriss]] → [[Avellaneda-Stoikov-2008-High-Frequency-Trading-Limit-Order-Book|Avellaneda-Stoikov]]
6. **Risk:** [[Mandelbrot-1963-Variation-of-Certain-Speculative-Prices|Mandelbrot]] → [[Engle-1982-ARCH|Engle ARCH]] → [[Bollerslev-1986-GARCH|GARCH]] → [[Artzner-1999-Coherent-Measures-of-Risk|Artzner]]
7. **Factor Alpha:** [[Banz-1981-Relationship-Return-Market-Value|Banz]] → [[Jegadeesh-Titman-1993-Returns-Buying-Winners-Selling-Losers|Jegadeesh-Titman]] → [[Gatev-Goetzmann-Rouwenhorst-2006-Pairs-Trading|Gatev et al.]] → [[Kelly-1956-New-Interpretation-of-Information-Rate|Kelly]] → [[Grinold-1989-Fundamental-Law-Active-Management|Grinold]]
