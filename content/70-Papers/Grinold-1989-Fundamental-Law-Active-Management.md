---
type: paper
title: "The Fundamental Law of Active Management"
authors: ["Richard C. Grinold"]
year: 1989
categories: ["q-fin.PM"]
tags: [paper, classic, unread, portfolio-management, active-management, information-ratio, information-coefficient, breadth, alpha]
status: unread
added: 2026-08-23
journal: "Journal of Portfolio Management, 15(3), 30-37"
---

## Abstract
Grinold establishes the Fundamental Law of Active Management: IR = IC × √BR, where IR is the information ratio (risk-adjusted excess return), IC is the information coefficient (correlation between forecasted and actual returns), and BR is the breadth (number of independent investment bets per year). This elegant result shows that active managers can improve their information ratio by either improving their forecasting skill (IC) or increasing the number of independent bets (BR). The law quantifies why diversified systematic strategies with many small edges can compete with concentrated strategies with large edges.

## Key Contribution
Derived the fundamental law: IR = IC × √BR. Quantified the roles of skill and breadth in generating alpha. Showed that systematic strategies (high BR) can dominate concentrated strategies (high IC but low BR) even with lower per-bet IC. Foundation for portfolio construction in quantitative asset management. Key tool for comparing systematic vs. discretionary approaches.

## Methods
Portfolio construction as a signal-to-noise optimization. Information coefficient: IC = Corr(forecast, realization). Breadth: number of independent bets N per period. Information ratio: IR = E[active return] / σ(active return). Derivation under simplifying assumptions of independent, identically forecasted securities.

## Results
Fundamental law: IR = IC × √N. Implication: doubling number of bets (breadth) → IR improves by √2. Example: IC=0.05, N=100 → IR=0.5 (good); IC=0.10, N=25 → IR=0.5 (equivalent). Maximum IR: combine maximum IC with maximum breadth. Portfolio optimization (transfer coefficient TC) can reduce effective BR.

## Critique
Independence assumption rarely holds (correlated signals, positions). Transfer coefficient (Clarke et al.) extension needed for constrained portfolios. IC is constant across bets—unrealistic. "Breadth" is difficult to measure in practice when bets are correlated. Decay of IC over time not addressed.

## Relevance
The theoretical foundation of quantitative portfolio management. Every systematic equity manager uses this framework to evaluate their strategy's potential. The law explains why diversified factor strategies (hundreds of names) beat concentrated stock-picking (few names) at the same skill level. Essential for understanding information ratios, portfolio sizing, and the economics of systematic vs. discretionary management.

## Related
- [[Markowitz-1952-Portfolio-Selection]]
- [[Kelly-1956-New-Interpretation-of-Information-Rate]]
- [[Lo-2002-Statistics-of-Sharpe-Ratios]]
- [[Fama-French-1993-Common-Risk-Factors]]
