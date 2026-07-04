---
type: concept
domain: 30-Models
tags: [portfolio, risk, ml-finance, clustering]
status: math
stability: evolving
confidence: high
last_reviewed: 2026-04-18
review_interval_days: 90
sources:
  - "Lopez de Prado, M. (2016). Building Diversified Portfolios that Outperform Out-of-Sample. Journal of Portfolio Management, 42(4)"
  - "Lopez de Prado, M. (2018). Advances in Financial Machine Learning. Wiley. Chapter 16"
created: 2026-04-18
---

> Cluster similar assets together, give each cluster an equal risk budget, allocate within clusters the same way — no matrix inversion required.

> [!info] Problem Chain
> **Chain:** Hedging & Risk → Gap 5: Markowitz is unstable — inputs are unreliable, outputs are extreme
> **This concept:** HRP uses hierarchical clustering on the correlation matrix to build portfolios without matrix inversion or return estimation — avoiding the error amplification that makes MVO and flat risk parity unstable for large universes.
> **Alternative approaches to this gap:** [[CAPM]], [[Factor Models]], [[Risk Parity]], [[Black-Litterman]]
> **You need first:** [[Risk Parity]], [[Correlation and Covariance Estimation]]
> **This unlocks:** none (Gap 5 terminal)

## Why This Exists

**The gap:** Risk Parity allocates equal risk to each individual asset — but for correlated assets (e.g., three equity ETFs), this over-concentrates risk in the correlated cluster. Both MVO and flat Risk Parity require inverting $\boldsymbol{\Sigma}$, which amplifies estimation errors catastrophically for large, noisy covariance matrices.

**What came before:** Flat Risk Parity (ERC) solved return estimation but introduced matrix inversion sensitivity. For 200+ assets with noisy covariance estimates, ERC weights could be as unstable as MVO weights.

**What this adds:** HRP (Lopez de Prado 2016) uses hierarchical clustering to organize assets into a tree structure based on correlation patterns, then allocates via recursive bisection — no matrix inversion required. Assets in the same cluster share a risk budget; clusters compete for risk budget top-down. This exploits the full covariance structure for diversification without inverting it.

**What it still doesn't solve:** HRP's results depend on the linkage method used in clustering (Ward's vs. single vs. complete) and on the quality of the correlation estimates. The allocation logic (bisection) is heuristic — it has no formal optimality guarantee relative to a stated objective.

Both [[Markowitz Mean-Variance Optimization]] and Risk Parity share a hidden vulnerability: they require **inverting the covariance matrix** $\boldsymbol{\Sigma}^{-1}$. Matrix inversion amplifies estimation errors. When $\boldsymbol{\Sigma}$ is estimated from finite historical data — as it always is — it contains noise, and that noise gets blown up by the inverse. The resulting portfolio weights can be dominated by estimation error rather than signal. This problem worsens with more assets: a 200-asset covariance matrix estimated from 2 years of daily data is nearly singular.

Lopez de Prado (2016) proposed a fundamentally different approach: **Hierarchical Risk Parity (HRP)**. Rather than inverting anything, HRP uses hierarchical clustering to organize assets into a tree structure based on their correlation patterns. It then allocates risk top-down through the tree using a recursive bisection procedure.

The key insight is geometric: assets that are similar to each other (high correlation) compete for the same risk budget. By grouping them hierarchically first, HRP ensures that similar assets collectively get one "share" of risk — preventing the optimizer from over-concentrating in a cluster of correlated assets just because their individual variances appear low.

Three steps:
1. **Cluster** assets by similarity using correlation-based distances.
2. **Reorder** the covariance matrix so correlated assets sit adjacent (quasi-diagonalization).
3. **Allocate** risk top-down through the cluster tree via recursive bisection.

No matrix inversion. No return estimation. No solver. Just matrix operations and sorting.

## Math Concepts

**Step 1: Correlation-based distance matrix.**

Convert correlations into distances that satisfy metric properties:

$$\boxed{d(i, j) = \sqrt{\frac{1 - \rho_{ij}}{2}}}$$

This maps $\rho = 1$ (identical assets) to $d = 0$ and $\rho = -1$ (perfectly anti-correlated) to $d = 1$. The formula satisfies the triangle inequality, which makes it suitable for hierarchical clustering.

**Step 2: Hierarchical clustering.**

Apply agglomerative clustering on the distance matrix. Common linkage methods:

| Linkage | Merges clusters by | Behavior |
|---------|-------------------|---------|
| Single | Minimum pairwise distance | Sensitive to outliers, "chaining" |
| Complete | Maximum pairwise distance | More compact, balanced clusters |
| Ward's | Minimize within-cluster variance | Often preferred for financial data |

The result is a **dendrogram** — a binary tree where leaves are individual assets and internal nodes represent merged clusters.

**Step 3: Quasi-diagonalization.**

Reorder the covariance matrix columns/rows to match the dendrogram's leaf order. This places highly correlated assets adjacent to each other. The reordered $\boldsymbol{\Sigma}$ is approximately block-diagonal — clusters of similar assets form blocks along the diagonal.

**Step 4: Recursive bisection — the allocation rule.**

Split the dendrogram recursively into left and right subtrees. At each split, allocate between the two subtrees inversely proportional to their **cluster variances**:

$$\alpha_L = \frac{\tilde{V}_R}{\tilde{V}_L + \tilde{V}_R}, \quad \alpha_R = 1 - \alpha_L$$

where $\tilde{V}_C$ is the variance of the cluster portfolio (computed using inverse-variance weights within the cluster):

$$\tilde{V}_C = \mathbf{w}_C^\top \boldsymbol{\Sigma}_C \mathbf{w}_C, \quad w_i^C = \frac{1/\sigma_i^2}{\sum_{j \in C} 1/\sigma_j^2}$$

Within each leaf cluster, assets receive **inverse-variance weights**. Combining the top-down bisection allocations with the within-cluster weights gives the final portfolio weights.

**The full allocation is the product of all bisection factors along the path from root to each leaf.**

## Walkthrough

**Setup.** Six assets with known correlation structure:

| Asset | Volatility | Cluster (approximate) |
|-------|-----------|----------------------|
| US Equity | 16% | Growth |
| EM Equity | 22% | Growth |
| Tech Equity | 24% | Growth |
| US Bonds | 5% | Defensive |
| EM Bonds | 8% | Defensive |
| Commodities | 18% | Real Assets |

**Correlation structure:** Equities are highly correlated with each other ($\rho \approx 0.7$–$0.8$). Bonds are correlated with each other ($\rho \approx 0.5$) and negatively correlated with equities. Commodities are weakly correlated with all.

**Distance matrix:** Applying $d(i,j) = \sqrt{(1-\rho_{ij})/2}$, pairs within the equity cluster have distances around 0.22–0.32. Equity-bond pairs have distances around 0.71–0.77.

**Dendrogram (described):**
```
Root
├── Equities cluster (d ≈ 0.55)
│   ├── US Equity
│   ├── EM Equity
│   └── Tech Equity
└── Right cluster (d ≈ 0.60)
    ├── Bonds cluster
    │   ├── US Bonds
    │   └── EM Bonds
    └── Commodities
```

**Quasi-diagonal reordering:** Reorder columns/rows to match this leaf order: [US Eq, EM Eq, Tech Eq, US Bd, EM Bd, Commodities]. The reordered covariance matrix shows large values in the upper-left (equity) and middle (bond) blocks.

**Recursive bisection:**
- Root split: Equities cluster vs. Bonds+Commodities cluster. Equities have high variance → receive less weight. Suppose cluster variances imply a 35/65 split (35% to equities, 65% to bonds+commodities).
- Within equities: three assets get inverse-variance weights (lower volatility assets get more). US Equity (16%) gets the most, Tech Equity (24%) the least.
- Within bonds+commodities: split between bonds cluster and commodities, then within bonds between US and EM.

**Final weights (approximate):**

| Asset | HRP | Equal Weight | MVO | Risk Parity |
|-------|-----|-------------|-----|-------------|
| US Equity | 15% | 17% | 5% | 20% |
| EM Equity | 10% | 17% | 2% | 14% |
| Tech Equity | 8% | 17% | 1% | 13% |
| US Bonds | 30% | 17% | 60% | 22% |
| EM Bonds | 18% | 17% | 20% | 18% |
| Commodities | 19% | 17% | 12% | 13% |

HRP produces a balanced allocation — more defensive than equal weight, more diversified than MVO, and influenced by cluster structure in a way flat risk parity is not.

## Analysis

**HRP vs. MVO:**

| Dimension | MVO | HRP |
|-----------|-----|-----|
| Matrix inversion | Required ($\boldsymbol{\Sigma}^{-1}$) | Not required |
| Return estimation | Required ($\boldsymbol{\mu}$) | Not required |
| Out-of-sample stability | Poor — sensitive to estimation error | Better — covariance structure is more stable |
| Handles correlated assets | Poorly (extreme weights) | Well (tree structure groups them) |
| Computational complexity | Quadratic programming | $O(n^2)$ clustering |

**HRP vs. Risk Parity:** Risk parity allocates so that each *individual asset* contributes equal risk. HRP allocates so that each *cluster* contributes equal risk, and within clusters each asset contributes equally. The tree structure is the key difference — it prevents risk parity from concentrating within a highly correlated cluster.

**Sensitivity to linkage method:** Ward's linkage tends to produce more compact, balanced clusters and is generally preferred. Single linkage can create elongated "chain" clusters that behave poorly. The choice of linkage is a hyperparameter that affects final weights.

**Empirical results (Lopez de Prado 2016):** In out-of-sample backtests across 10 years of data, HRP achieved higher Sharpe ratios than both MVO (including with shrinkage) and equal risk contribution (risk parity). The improvement was attributed to HRP's robustness to estimation error — its weights are less sensitive to small changes in the covariance matrix because it does not invert it.

## Implementation

```python
import numpy as np
from scipy.cluster.hierarchy import linkage, to_tree
from scipy.spatial.distance import squareform

# ── Setup: 6-asset example ────────────────────────────────────────────────────
assets = ['US_Eq', 'EM_Eq', 'Tech_Eq', 'US_Bd', 'EM_Bd', 'Cmdty']
vol = np.array([0.16, 0.22, 0.24, 0.05, 0.08, 0.18])

corr = np.array([
    [1.00, 0.78, 0.75, -0.25, -0.18,  0.12],
    [0.78, 1.00, 0.72, -0.20, -0.15,  0.15],
    [0.75, 0.72, 1.00, -0.18, -0.12,  0.10],
    [-0.25,-0.20,-0.18, 1.00,  0.52, -0.08],
    [-0.18,-0.15,-0.12, 0.52,  1.00, -0.05],
    [0.12, 0.15, 0.10,-0.08, -0.05,  1.00],
])
Sigma = np.outer(vol, vol) * corr

# ── Step 1: Correlation-based distance matrix ─────────────────────────────────
dist_matrix = np.sqrt((1 - corr) / 2)
np.fill_diagonal(dist_matrix, 0)
condensed_dist = squareform(dist_matrix)

# ── Step 2: Hierarchical clustering (Ward's linkage) ─────────────────────────
link = linkage(condensed_dist, method='ward')

# ── Step 3: Quasi-diagonalization — get leaf order from dendrogram ────────────
def get_leaf_order(node, n_assets):
    """Recursively extract leaf order from scipy linkage tree."""
    root, rd = to_tree(link, rd=True)

    def _get_leaves(node):
        if node.is_leaf():
            return [node.id]
        return _get_leaves(node.left) + _get_leaves(node.right)

    return _get_leaves(root)

leaf_order = get_leaf_order(link, len(assets))
print("Quasi-diagonal order:", [assets[i] for i in leaf_order])

# Reorder covariance matrix
Sigma_reordered = Sigma[np.ix_(leaf_order, leaf_order)]

# ── Step 4: Recursive bisection ───────────────────────────────────────────────
def cluster_variance(indices, Sigma):
    """Variance of an inverse-variance-weighted cluster portfolio."""
    sub_Sigma = Sigma[np.ix_(indices, indices)]
    inv_var = 1.0 / np.diag(sub_Sigma)
    w = inv_var / inv_var.sum()
    return w @ sub_Sigma @ w

def recursive_bisection(sorted_indices, Sigma):
    """
    Recursively bisect the sorted asset list and allocate weights
    via inverse-variance at each split.
    Returns a dict {asset_index: weight}.
    """
    weights = {i: 1.0 for i in sorted_indices}

    def bisect(items):
        if len(items) <= 1:
            return
        mid = len(items) // 2
        left, right = items[:mid], items[mid:]

        var_L = cluster_variance(left, Sigma)
        var_R = cluster_variance(right, Sigma)

        # Allocate inversely proportional to cluster variance
        alpha = var_R / (var_L + var_R)   # weight going to left
        for i in left:
            weights[i] *= alpha
        for i in right:
            weights[i] *= (1 - alpha)

        bisect(left)
        bisect(right)

    bisect(sorted_indices)
    return weights

weight_dict = recursive_bisection(leaf_order, Sigma)

# Convert to array in original asset order
w_hrp = np.array([weight_dict[i] for i in range(len(assets))])
w_hrp /= w_hrp.sum()   # normalize (should already sum to ~1)

# ── Results ───────────────────────────────────────────────────────────────────
w_equal = np.ones(len(assets)) / len(assets)
w_ivp   = (1.0 / vol**2) / (1.0 / vol**2).sum()  # inverse-variance (flat)

print("\nWeights comparison:")
print(f"{'Asset':>10} {'HRP':>8} {'Equal':>8} {'Inv-Var':>8}")
for i, a in enumerate(assets):
    print(f"{a:>10} {w_hrp[i]:>8.1%} {w_equal[i]:>8.1%} {w_ivp[i]:>8.1%}")

# Portfolio statistics
def port_vol(w): return np.sqrt(w @ Sigma @ w)

print(f"\nHRP vol:     {port_vol(w_hrp):.2%}")
print(f"Equal vol:   {port_vol(w_equal):.2%}")
print(f"Inv-Var vol: {port_vol(w_ivp):.2%}")
```

## Bridge to Quant / ML

**HRP is unsupervised ML applied to portfolio construction.** The hierarchical clustering at its core is a classic unsupervised learning algorithm. Replacing the clustering step with other algorithms (k-means, DBSCAN, graph-based methods) produces variations of HRP — some of which have appeared in the literature under names like "community detection portfolios."

**Minimum spanning tree connection.** An alternative to hierarchical clustering is to build a minimum spanning tree (MST) of assets based on the distance matrix, then allocate proportional to each asset's "centrality" in the tree. Lopez de Prado discusses MST as a related approach. The MST is a sparser representation of the correlation structure.

**Factor allocation.** HRP is not limited to individual assets. You can run it on a set of factor portfolios (value, momentum, quality, low-vol, etc.) to build a diversified multi-factor portfolio. The clustering will group correlated factors (e.g., value and profitability often cluster together), and the bisection naturally limits overexposure to any one factor theme.

**Crypto and alternative assets.** HRP has become popular for crypto portfolios, where correlations are unstable and expected returns are especially hard to estimate. The no-inversion property makes it robust to the frequent regime changes in crypto markets.

**As a baseline for ML portfolio models.** HRP serves as a strong non-parametric benchmark for ML-based portfolio models. If a neural network or reinforcement learning agent cannot beat HRP out-of-sample, it's likely overfitting. Many papers in the ML-for-finance space now use HRP as the baseline to beat rather than equal-weight or MVO.

**Connection to [[Regime Detection]]:** HRP's correlation-based clustering implicitly captures regime information. In crisis regimes, all correlations spike toward 1, compressing the dendrogram — the tree flattens and HRP approaches equal-weight. This is an automatic, adaptive response to changing market structure.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why does matrix inversion amplify estimation error in covariance matrices, and how does HRP avoid this problem?
<details><summary>Answer</summary>When a covariance matrix is estimated from finite data, the eigenvalues are noisy — some are spuriously large, some spuriously small. Matrix inversion flips eigenvalues: $\lambda_{\min}$ in $\Sigma$ becomes $1/\lambda_{\min}$ (large) in $\Sigma^{-1}$. Noisy small eigenvalues get amplified into large entries in the inverse, and the portfolio optimizer exploits these spurious large entries to create extreme (and noisy) positions. HRP avoids this entirely by never inverting the covariance matrix — it uses only the correlation structure for clustering (pairwise distances) and only the diagonal variance for within-cluster allocation (inverse variance weighting). These operations are robust to eigenvalue noise.</details>

**Q2.** In HRP's recursive bisection step, why is the weight allocated to a sub-tree inversely proportional to its cluster variance, rather than proportional?
<details><summary>Answer</summary>Risk parity logic: allocate less capital to higher-risk clusters and more to lower-risk clusters, so each cluster contributes equal *risk* to the total portfolio. If cluster A has variance $\tilde{V}_A$ and cluster B has variance $\tilde{V}_B$, setting $\alpha_A = \tilde{V}_B / (\tilde{V}_A + \tilde{V}_B)$ means cluster A receives capital inversely proportional to its risk. The portfolio's risk contribution from each cluster then balances: high-variance cluster A gets less capital, contributing similar risk to low-variance cluster B with more capital. This is the same logic as naive risk parity (inverse volatility weighting) applied at the cluster level.</details>

**Q3.** What is quasi-diagonalization in HRP, and why does it matter for the allocation step?
<details><summary>Answer</summary>Quasi-diagonalization reorders the rows and columns of the covariance matrix to match the dendrogram's leaf order — placing correlated assets adjacent to each other. After reordering, the matrix is approximately block-diagonal: highly correlated assets cluster in the same block, and off-diagonal blocks (between clusters) are small.

This matters because HRP's bisection step splits the ordered list at the midpoint. If correlated assets are adjacent (quasi-diagonal order), the bisection splits clusters naturally — the left half contains one cluster, the right half another. Without quasi-diagonalization, the bisection would split within a cluster, mixing correlated assets across both halves and destroying the diversification logic.</details>

---

### Level 2 — Quantitative

**Q4.** Three assets: A (vol 20%), B (vol 25%), C (vol 10%). Correlations: A-B = 0.80 (highly correlated), A-C = 0.10, B-C = 0.15. Using single-linkage clustering (merges at minimum pairwise distance), describe which two assets would merge first and what the cluster variance of the merged cluster would be (using inverse-variance weights within the cluster).
<details><summary>Answer</summary>

Distances: $d(i,j) = \sqrt{(1-\rho_{ij})/2}$

$d(A,B) = \sqrt{(1-0.80)/2} = \sqrt{0.10} = 0.316$

$d(A,C) = \sqrt{(1-0.10)/2} = \sqrt{0.45} = 0.671$

$d(B,C) = \sqrt{(1-0.15)/2} = \sqrt{0.425} = 0.652$

A and B merge first (minimum distance = 0.316).

Cluster {A,B} variance with inverse-variance weights:

Inverse variances: $1/\sigma_A^2 = 1/0.04 = 25$, $1/\sigma_B^2 = 1/0.0625 = 16$. Sum = 41.

Weights within cluster: $w_A = 25/41 = 0.610$, $w_B = 16/41 = 0.390$.

Covariance matrix for {A,B}: $\Sigma_{AB} = \begin{pmatrix}0.04 & 0.80(0.20)(0.25)\\0.80(0.20)(0.25)&0.0625\end{pmatrix} = \begin{pmatrix}0.04&0.04\\0.04&0.0625\end{pmatrix}$

$\tilde{V}_{AB} = w^\top \Sigma_{AB} w = (0.610)^2(0.04) + (0.390)^2(0.0625) + 2(0.610)(0.390)(0.04)$
$= 0.0149 + 0.0095 + 0.0190 = \mathbf{0.0434}$</details>

**Q5.** Continuing from Q4: the {A,B} cluster has cluster variance $\tilde{V}_{AB} = 0.0434$ and asset C has variance $\sigma_C^2 = 0.01$. In the root bisection, what weight goes to the {A,B} cluster and what weight goes to C?
<details><summary>Answer</summary>

Bisection: allocate inversely proportional to cluster variance.

$\alpha_{AB} = \tilde{V}_C / (\tilde{V}_{AB} + \tilde{V}_C) = 0.01 / (0.0434 + 0.01) = 0.01 / 0.0534 = \mathbf{0.187}$

$\alpha_C = 1 - 0.187 = \mathbf{0.813}$

So {A,B} cluster gets 18.7% of total capital; C gets 81.3%. Within the {A,B} cluster, the inverse-variance weights split as $w_A = 0.610 \times 0.187 = 11.4\%$ and $w_B = 0.390 \times 0.187 = 7.3\%$.

Final HRP weights: **A = 11.4%, B = 7.3%, C = 81.3%**. The low-volatility asset C dominates because the high-vol, high-correlation {A,B} cluster is penalized as a whole.</details>

---

### Level 3 — Coding

**Q6.** The implementation uses `scipy.cluster.hierarchy.linkage` with Ward's method. Describe how you would change the code to use average linkage instead, and explain one scenario where average linkage would produce a qualitatively different portfolio from Ward's linkage.
<details><summary>Answer</summary>

Change is one line: replace `method='ward'` with `method='average'`:
```python
link = linkage(condensed_dist, method='average')
```

Ward's linkage merges clusters to minimize the increase in total within-cluster variance — it produces compact, balanced clusters. Average linkage merges based on the average pairwise distance between all members of two clusters.

Scenario where they differ: suppose assets A and B are tightly correlated (d=0.1) and asset C is moderately correlated with both (d=0.45 with A, d=0.50 with B). Ward's will merge {A,B} first, then add C — creating a clean {A,B} vs {C} structure. Average linkage may also merge {A,B} first, but the subsequent merge with C would use the average distance $\bar{d} = (0.45+0.50)/2 = 0.475$. If there were a fourth asset D with d=0.40 from C but 0.60 from A and B, average linkage might cluster {C,D} before adding to {A,B}, while Ward's might merge differently based on variance minimization. This can produce meaningfully different cluster trees and therefore different HRP weights when the correlation structure has mixed patterns.</details>

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| HRP is a generalization of Risk Parity | HRP shares the risk-parity philosophy but is structurally different — tree-based bisection vs. ERC optimization. They produce different weights even for the same covariance matrix. |
| HRP requires no covariance estimates | HRP still requires the full covariance matrix for cluster distances and within-cluster variance. It avoids *inverting* the covariance matrix, but estimation quality still matters. |
| HRP always beats MVO out-of-sample | Lopez de Prado's results depend on the specific dataset. HRP consistently beats naive MVO, but well-implemented MVO with shrinkage can match or beat HRP depending on regime. |
| Cluster structure is stable over time | Correlations change across regimes. In a crisis, everything becomes highly correlated and the dendrogram flattens — HRP approaches equal-weight automatically, which is actually a feature, not a bug. |

## Related Concepts

- [[Risk Parity]] — flat risk parity ignores cluster structure; HRP extends it with a tree
- [[Markowitz Mean-Variance Optimization]] — HRP avoids MVO's matrix inversion and return estimation
- [[Correlation and Covariance Estimation]] — the input to HRP's distance matrix; quality matters
- [[Factor Models]] — HRP can be applied to factors, not just individual assets
- [[Regime Detection]] — correlation structure changes across regimes, affecting HRP's clustering
- [[Black-Litterman]] — alternative approach to MVO's instability; improves returns rather than eliminating them

## Sources Used

- Lopez de Prado, M. (2016). Building Diversified Portfolios that Outperform Out-of-Sample. *Journal of Portfolio Management*, 42(4)
- Lopez de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley. Chapter 16

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-04-18 | Full content written | initial build |
