---
type: concept
domain: 60-ML-Finance
tags: [machine-learning, deep-learning, forecasting]
status: emerging
stability: emerging
confidence: medium
last_reviewed: 2026-07-26
review_interval_days: 180
sources:
  - "He & Zhang (2026) — Heads, Not Backbones: Output Heads Dominate Architectures on Fat-Tailed Returns"
  - "Vaswani et al. (2017) — Attention Is All You Need"
created: 2026-07-26
---

> [!info] Problem Chain
> **Chain:** ML-Finance → Gap: Classical time-series models (ARIMA, GARCH) impose rigid linear/parametric structure that misses complex nonlinear dependencies in return sequences
> **This concept:** Self-attention lets a forecasting model weigh every past observation against every other directly, capturing long-range and nonlinear dependencies without a recurrent model's vanishing-memory problems — but for fat-tailed financial returns, how the predictive distribution is modeled (the output head) often matters more than which backbone computes the features feeding into it.
> **Alternative approaches to this gap:** LSTM/RNN sequence models (recurrent, sequential processing, real competing baseline), simpler linear models like DLinear (a single linear layer per horizon — a real, competitive baseline in benchmark studies, not a strawman)
> **You need first:** general deep learning / attention mechanism background
> **This unlocks:** [[Regime Detection]], [[Deep Hedging]]

## Why This Exists

**The gap:** ARIMA models returns as a linear function of their own past values plus a moving-average error term; GARCH models volatility as a linear function of past squared shocks and past variances. Both impose a fixed, hand-specified functional form. Real return series exhibit nonlinear volatility clustering, asymmetric responses to shocks (leverage effects), and dependencies that span irregular, data-dependent lags — structure that a linear parametric model cannot represent no matter how it is fit.

**What came before:** LSTMs and other recurrent networks were the first widely adopted nonlinear alternative. They process a sequence one step at a time, carrying a hidden state forward, so a signal from 60 days ago must survive 60 sequential updates to influence today's forecast — it degrades (vanishing gradients) or must be explicitly gated. Recurrence is also inherently sequential, which makes training slow because time steps cannot be parallelized.

**What this adds:** Self-attention computes a direct, weighted connection between every pair of time steps in the input window in a single layer, with no decay from sequential composition. A large move 40 days ago and a large move 2 days ago are equally reachable in one hop; the model learns how much each past step should matter for the current forecast rather than having that captured implicitly through many chained state updates. Attention layers are also parallelizable across the whole sequence, unlike recurrence.

**What it still doesn't solve:** Long-range, parallel connectivity does not by itself produce a good forecast of a fat-tailed, non-stationary process. [[70-Papers/Heads, Not Backbones- Output Heads Dominate Architectures on Fat-Tailed Returns|Heads, Not Backbones]] tested an attention-based backbone (iTransformer) against three non-attention backbones (TimesNet, DLinear, N-BEATS) on S&P 500 monthly returns and found that swapping backbones changed CRPS by less than 1.5% at short horizons — smaller than the effect of just changing how the output distribution is parameterized. Architecture alone, attention included, is not the binding constraint on fat-tailed return forecasting at short horizons; the shape assumed for the predictive distribution is. Standard transformers also assume tokens arrive at fixed, evenly-spaced positions (via sinusoidal positional encoding) and implicitly assume roughly stationary input statistics — both false for calendar-gapped, regime-shifting financial series — so naive transplants from NLP require adaptation before any of the attention advantages materialize.

## Math Concepts

### Self-attention

$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

For a financial return sequence $r_{t-L+1}, \ldots, r_t$ embedded into vectors, each time step produces three learned projections of its embedding:

- **Query ($Q$):** what the current time step is "asking about" — e.g., a representation of "what past conditions predict tomorrow's return."
- **Key ($K$):** what each past time step "advertises" about itself — e.g., a representation of the market conditions on that day.
- **Value ($V$):** the actual content each past time step contributes if it turns out to be relevant — e.g., a representation of the return/volatility information carried by that day.

$QK^T$ computes a similarity score between the query at each position and the key at every other position; dividing by $\sqrt{d_k}$ (the key dimension) keeps the scores from growing too large as dimensionality increases, which would otherwise push softmax into near-one-hot, hard-to-train regions. Softmax turns the scaled scores into a set of weights that sum to 1 across the past positions. The output is a weighted average of the Values — so the model produces, for each time step, a context vector that pools information from the entire lookback window, weighted by learned relevance rather than a fixed decay (as in an EWMA) or a fixed window (as in a moving average).

### Positional encoding for financial series

Standard transformers add a fixed sinusoidal function of the token *index* to each embedding, since raw attention has no notion of order. This assumes evenly spaced, infinitely repeating, stationary positions — true for word order in a sentence, false for trading days. Financial series have calendar gaps (weekends, holidays, exchange closures) that a naive integer index ignores, and their statistics are non-stationary (a 20-day window in 2017 and a 20-day window in 2008 have very different volatility even at the "same" relative position). Common adaptations: encode by trading-day count rather than calendar day, add explicit calendar-gap features, or replace fixed sinusoidal encodings with learned or relative positional embeddings that can absorb irregular spacing.

### Output-head distinction

The **backbone** (LSTM, TimesNet, DLinear, N-BEATS, an attention-based encoder like iTransformer, ...) produces a feature representation. The **output head** decides how that representation is turned into a forecast, and what loss trains it:

**Point head** — a single scalar forecast $\hat y$, trained with mean squared error:
$$\mathcal{L}_{\text{MSE}} = \frac{1}{N}\sum_{i=1}^N (y_i - \hat y_i)^2$$
This is the MLE loss under an implicit assumption of Gaussian, constant-variance, symmetric errors. It targets the conditional mean and says nothing about the width or shape of the forecast distribution — useless input for anything requiring tail behavior.

**Single-Gaussian density head** — outputs $(\mu_i, \sigma_i)$ per time step, trained by minimizing the Gaussian negative log-likelihood:
$$\mathcal{L}_{\text{NLL}} = \frac{1}{N}\sum_{i=1}^N \left[\frac{(y_i - \mu_i)^2}{2\sigma_i^2} + \log \sigma_i\right] + \text{const}$$
This captures time-varying volatility (heteroskedasticity) — $\sigma_i$ can widen in turbulent periods — but still forces a single symmetric, unimodal bell curve onto returns that are actually skewed and fat-tailed.

**Gaussian-mixture density head** ($K$ components) — outputs $(\pi_{i,k}, \mu_{i,k}, \sigma_{i,k})$ for $k = 1, \ldots, K$, trained with the mixture negative log-likelihood:
$$\mathcal{L}_{\text{NLL}} = -\frac{1}{N}\sum_{i=1}^N \log\left(\sum_{k=1}^K \pi_{i,k}\, \mathcal{N}(y_i \mid \mu_{i,k}, \sigma_{i,k}^2)\right)$$
A weighted sum of Gaussians can represent multimodality (a calm-regime component alongside a crisis-regime component), skew, and heavier tails than any single Gaussian — at the cost of more parameters and a less interpretable, non-closed-form marginal distribution.

**CRPS (Continuous Ranked Probability Score)** — the metric used to *compare* heads on a common scale regardless of parametric form:
$$\text{CRPS}(F, y) = \int_{-\infty}^{\infty} \big(F(x) - \mathbb{1}\{x \ge y\}\big)^2\, dx$$
where $F$ is the model's predictive CDF and $y$ is the realized outcome. CRPS reduces exactly to absolute error when $F$ is a point mass (a point forecast), so it generalizes MAE to full distributions: it rewards a forecast for putting probability mass close to where the outcome actually landed, not just for getting the mean right. Lower CRPS is better, and it is reported in the same units as the target variable.

## Walkthrough

Take a 4-day window of daily log returns ending at time $t$: $r_{t-3} = +0.3\%$, $r_{t-2} = -1.8\%$ (a sharp drawdown day), $r_{t-1} = +0.1\%$, $r_t = -0.2\%$. The model wants to forecast $r_{t+1}$, so it forms a query from the current step and keys/values from all four past steps (attention is causal: only past and present are keys).

Suppose (illustratively) the learned query/key projections encode something like "how similar is this day's regime to today's," and the dot-product similarity scores between the query and each key come out as:

| Day | Raw score $q \cdot k_i$ | Scaled score $/\sqrt{d_k}$ |
|---|---|---|
| $t-3$ (+0.3%) | 0.4 | 0.28 |
| $t-2$ (−1.8%, crash) | 2.1 | 1.48 |
| $t-1$ (+0.1%) | 0.1 | 0.07 |
| $t$ (−0.2%) | 1.2 | 0.85 |

Softmax over the scaled scores concentrates most of the weight on $t-2$ and $t$ — the crash day and the most recent day — because a large-magnitude recent move is informative about near-term volatility (volatility clustering), while the small, unremarkable moves at $t-3$ and $t-1$ get discounted. Illustrative resulting weights: $[0.10, 0.42, 0.07, 0.41]$. The context vector fed forward is the weighted sum of the four days' Value vectors using these weights — a pooled representation dominated by the crash day and today, not a fixed-window average of all four days equally.

This is the qualitative advantage attention offers over a fixed-decay model: the weighting is content-dependent and learned, so a quiet day 3 steps back can be almost ignored while a volatile day gets amplified — without hand-specifying a decay rate. Whether that advantage translates into a better *forecast distribution*, however, depends heavily on the output head, as the next section shows.

## Analysis

[[70-Papers/Heads, Not Backbones- Output Heads Dominate Architectures on Fat-Tailed Returns|Heads, Not Backbones]] is the direct empirical test of the backbone-vs-head question for this domain. Setup: S&P 500 monthly log-returns, 1871–2023, anchored walk-forward validation, 4 backbones (TimesNet, DLinear, N-BEATS, iTransformer — the last being the attention-based one) crossed with 3 output heads (point, single-Gaussian, $K$=4 Gaussian mixture) — 12 variants total.

**The head dominates at short horizons.** Averaged across backbones, moving from a point head to a single-Gaussian head improves CRPS by about 1.3%; moving from Gaussian to the mixture head adds a further ~2.4% (roughly 3.7% cumulative from point to mixture). By contrast, holding the head fixed at "point" and swapping the backbone — including swapping in the attention-based iTransformer — changes CRPS by less than 1.5%. The output head is the larger lever.

**Point-accuracy metrics can't see any of this.** The Model Confidence Set applied to squared errors does not exclude any of the 12 variants at the 5% level: by MSE/RMSE alone, none of the backbone-head combinations is statistically distinguishable from any other. The separation only appears once you score the *full predictive distribution* with CRPS. This is a genuinely important nuance, not a footnote: a study that only reported RMSE would have concluded "architecture doesn't matter" and missed the real, economically meaningful gradient in distributional quality across output heads.

**The mixture head's edge is regime-dependent.** Its incremental CRPS improvement over the Gaussian head is largest exactly when it matters most for risk management — in the highest-volatility regimes, e.g. +13.9% at $h=12$ during the 1970s stagflation period. In calmer regimes the benefit shrinks toward the unconditional average, consistent with the mixture capturing tail/multimodal structure that a single Gaussian simply cannot express during stress.

**Horizon reverses the ranking.** At short horizons the head dominates; at longer horizons ($h \geq 6$) the backbone re-takes the lead. Correctly shaping the one-step-ahead conditional distribution is the first-order concern close in; how the backbone aggregates and rolls forward information over a longer window becomes the binding constraint further out.

**What this does *not* say:** it does not say transformers are the best backbone for financial forecasting, and it does not say architecture never matters. iTransformer was not shown to systematically dominate DLinear — a single linear layer — or N-BEATS on this benchmark; the paper's central claim is that, for fat-tailed monthly equity returns at short horizons, output-head choice is the larger lever, and backbone choice becomes the larger lever only once the horizon lengthens. This directly undercuts a naive "bigger, fancier (attention-based) architecture wins" narrative — a simple linear model with a well-specified mixture head can be competitive with, or beat, an attention-based backbone paired with a point head.

**Caveats to hold onto:** single index (S&P 500), monthly frequency, univariate return sequence, one paper (2026) not yet widely replicated. Intraday, multi-asset, or cross-sectional settings — where attention's capacity to model relationships *across* series (assets, or price vs. order-flow channels) rather than just *within* one series comes into play — are not covered by this result and could show a different backbone/head balance. Confidence in generalizing this finding beyond the tested setup should stay medium.

## Implementation

```python
import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class ReturnEmbedding(nn.Module):
    """Embeds scalar returns + a positional signal. Financial series are
    irregularly spaced (weekends/holidays) and non-stationary, so a fixed
    sinusoidal index encoding (as in NLP transformers) is a poor fit --
    here we use a learned embedding indexed by trading-day count instead."""
    def __init__(self, d_model=32, max_len=512):
        super().__init__()
        self.value_proj = nn.Linear(1, d_model)
        self.pos_embed = nn.Embedding(max_len, d_model)

    def forward(self, returns, trading_day_idx):
        # returns: (batch, seq_len, 1); trading_day_idx: (batch, seq_len) int64
        x = self.value_proj(returns)
        x = x + self.pos_embed(trading_day_idx)
        return x


class ReturnTransformerBlock(nn.Module):
    """Minimal single-layer transformer encoder block for a univariate
    return sequence."""
    def __init__(self, d_model=32, n_heads=4, d_ff=64, dropout=0.1):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(
            d_model, n_heads, dropout=dropout, batch_first=True
        )
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_ff), nn.GELU(), nn.Linear(d_ff, d_model)
        )
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, attn_mask=None):
        # x: (batch, seq_len, d_model); attn_mask enforces causality
        attn_out, attn_weights = self.self_attn(
            x, x, x, attn_mask=attn_mask, need_weights=True
        )
        x = self.norm1(x + self.dropout(attn_out))
        ff_out = self.ff(x)
        x = self.norm2(x + self.dropout(ff_out))
        return x, attn_weights


class GaussianMixtureHead(nn.Module):
    """K-component Gaussian mixture density head: outputs mixture weights
    (softmax), means, and positive std devs (softplus, numerically floored)."""
    def __init__(self, d_model=32, n_components=4):
        super().__init__()
        self.n_components = n_components
        self.pi_layer = nn.Linear(d_model, n_components)
        self.mu_layer = nn.Linear(d_model, n_components)
        self.log_sigma_layer = nn.Linear(d_model, n_components)

    def forward(self, h):
        # h: (batch, d_model) -- pooled representation (e.g. last time step)
        pi = torch.softmax(self.pi_layer(h), dim=-1)
        mu = self.mu_layer(h)
        sigma = F.softplus(self.log_sigma_layer(h)) + 1e-6
        return pi, mu, sigma


def gaussian_mixture_nll(y, pi, mu, sigma):
    """Negative log-likelihood loss for the mixture head.
    y: (batch, 1); pi, mu, sigma: (batch, K)."""
    y = y.expand_as(mu)
    component_ll = -0.5 * ((y - mu) / sigma) ** 2 - torch.log(sigma) - 0.5 * math.log(2 * math.pi)
    weighted_ll = torch.log(pi + 1e-12) + component_ll
    nll = -torch.logsumexp(weighted_ll, dim=-1)  # numerically stable log-sum-exp
    return nll.mean()


# --- Minimal forward pass sketch ---
batch, seq_len, d_model = 8, 60, 32
embed = ReturnEmbedding(d_model=d_model)
block = ReturnTransformerBlock(d_model=d_model)
head = GaussianMixtureHead(d_model=d_model, n_components=4)

returns = torch.randn(batch, seq_len, 1) * 0.01          # daily log returns
day_idx = torch.arange(seq_len).unsqueeze(0).expand(batch, -1)
causal_mask = torch.triu(torch.full((seq_len, seq_len), float("-inf")), diagonal=1)

x = embed(returns, day_idx)
h, attn_weights = block(x, attn_mask=causal_mask)         # (batch, seq_len, d_model)
h_last = h[:, -1, :]                                      # pooled: last step's representation
pi, mu, sigma = head(h_last)

y_next = torch.randn(batch, 1) * 0.01
loss = gaussian_mixture_nll(y_next, pi, mu, sigma)
```

## Bridge to Quant / ML

**[[Regime Detection]]:** a Gaussian-mixture output head is, in effect, an implicit and fully differentiable regime model — one component can come to represent calm markets, another crisis conditions — learned jointly with the forecast rather than fit separately as an HMM. The paper's finding that the mixture head's edge is largest in identifiable high-volatility regimes (1970s stagflation) is consistent with it picking up exactly the kind of structure an explicit regime detector targets, without requiring hard state labels.

**Risk management ([[Value at Risk]], [[Expected Shortfall]]):** VaR and CVaR are quantiles and tail expectations of the forecast distribution, not point predictions. A point head trained with MSE optimizes the conditional mean and conveys nothing about tail width — it cannot produce a 99% VaR without an extra, bolted-on assumption about the error distribution. A density head (Gaussian or mixture) produces the quantiles and tail mass directly, and the paper's regime-dependent result — the mixture head helps most exactly when volatility is highest — is precisely the situation where VaR/CVaR estimates matter most for capital and risk limits.

**[[Deep Hedging]]:** hedging policies trained against a point forecast under-hedge tail risk by construction, since the point forecast carries no information about how wide or skewed the outcome distribution really is. A distributional output head feeding a hedging pipeline supplies the shape of the P&L distribution, not just its center — closer to what a hedging objective (e.g., a CVaR-based hedging loss) actually needs.

## Self-Assessment

---

### Level 1 — Conceptual

**Q1.** Why do standard transformer positional encodings (fixed sinusoidal functions of token index) need adaptation for financial time series?
<details>
<summary>Answer</summary>
Sinusoidal positional encoding assumes tokens arrive at evenly spaced, indefinitely repeating positions with roughly stationary statistics — true for word order in a sentence. Financial series violate both assumptions: they have calendar gaps (weekends, holidays, exchange closures) that a raw integer index ignores, and their statistics are non-stationary — volatility in a 2008 window is very different from volatility in a 2017 window even at the "same" relative position in the lookback. Adaptations include indexing by trading-day count rather than calendar day, adding explicit calendar-gap features, or replacing the fixed encoding with a learned or relative positional embedding that can absorb irregular spacing and shifting regimes.
</details>

**Q2.** What is the central finding of "Heads, Not Backbones," and why does it complicate a simple story of "use a transformer for time-series forecasting"?
<details>
<summary>Answer</summary>
Comparing four backbones (including the attention-based iTransformer) against three output heads (point, Gaussian, Gaussian mixture) on S&P 500 monthly returns, the paper finds that output-head choice moves CRPS far more than backbone choice does at short horizons — point-to-Gaussian gains ~1.3%, Gaussian-to-mixture a further ~2.4%, while swapping backbones changes CRPS by under 1.5%. This complicates the naive story because it shows attention's architectural advantages are a second-order effect here: a linear model (DLinear) with a well-chosen output head can be competitive with an attention-based backbone. The ranking does flip at longer horizons (h ≥ 6), where backbone choice regains the lead — so the honest takeaway is "it depends on horizon," not "transformers win" or "transformers don't matter."
</details>

**Q3.** Why is mean squared error a poor loss/metric for fat-tailed return forecasting, even though it is the default for most regression tasks?
<details>
<summary>Answer</summary>
MSE is the maximum-likelihood loss for a Gaussian, constant-variance, symmetric error assumption. Its minimizer is the conditional mean, and by construction it carries no information about the spread or shape of the forecast distribution — two forecasts with identical MSE can imply wildly different tail risk. It also treats every observation's error the same way, regardless of the current volatility regime. The paper's finding that the Model Confidence Set could not statistically distinguish any of the 12 backbone-head variants on squared error, while CRPS revealed a clear and economically meaningful gradient, is direct evidence that squared error is not sensitive to the distributional differences that actually matter for fat-tailed returns.
</details>

---

### Level 2 — Quantitative

**Q4.** A query vector $q = [1, 0]$ attends over three past days with key vectors $k_1 = [1, 0]$, $k_2 = [0, 1]$, $k_3 = [-1, 0]$, and associated (scalar) value contributions $v_1 = 0.5\%$, $v_2 = -0.2\%$, $v_3 = 1.0\%$. Using $d_k = 2$, compute the attention output.
<details>
<summary>Answer</summary>

Raw dot products: $q \cdot k_1 = 1$, $q \cdot k_2 = 0$, $q \cdot k_3 = -1$.

Scale by $\sqrt{d_k} = \sqrt{2} \approx 1.414$: scores $\approx [0.707, 0, -0.707]$.

Exponentiate: $e^{0.707} \approx 2.028$, $e^{0} = 1$, $e^{-0.707} \approx 0.493$. Sum $\approx 3.521$.

Softmax weights: $w_1 \approx 0.576$, $w_2 \approx 0.284$, $w_3 \approx 0.140$.

Attention output (weighted sum of values):
$$0.576(0.5\%) + 0.284(-0.2\%) + 0.140(1.0\%) \approx 0.288\% - 0.057\% + 0.140\% \approx 0.37\%$$

The context vector for this query is dominated by day 1 (highest similarity), with a small negative pull from day 2 and a small positive contribution from day 3.
</details>

**Q5.** A Gaussian density head predicts $\mu = 0.5\%$, $\sigma = 1.2\%$ for tomorrow's return, and the realized return is $y = -2.1\%$ (a crash). Compute the NLL loss contribution (drop the constant term). Then recompute assuming the model had instead predicted $\sigma = 3.0\%$ for the same error, and explain why the second loss is lower despite an identical squared error.
<details>
<summary>Answer</summary>

Error: $y - \mu = -2.1\% - 0.5\% = -2.6\%$, so $(y-\mu)^2 = 6.76\ (\%^2)$.

**With $\sigma = 1.2\%$:** $\sigma^2 = 1.44$.
$$\mathcal{L} = \frac{6.76}{2(1.44)} + \ln(1.2) \approx 2.347 + 0.182 = 2.529$$

**With $\sigma = 3.0\%$:** $\sigma^2 = 9.0$.
$$\mathcal{L} = \frac{6.76}{2(9.0)} + \ln(3.0) \approx 0.376 + 1.099 = 1.475$$

Same squared error (6.76 in both cases — indistinguishable to an MSE loss), but the NLL under $\sigma = 3.0\%$ is much lower because the model "expected" more uncertainty and a large deviation is less surprising under a wider predictive distribution. This is exactly why a squared-error metric can fail to separate models (as the Model Confidence Set found on this paper's 12 variants) while a likelihood-based metric like NLL or CRPS rewards well-calibrated uncertainty, not just point accuracy.
</details>

---

### Level 3 — Coding

**Q6.** In `gaussian_mixture_nll` above, the mixture log-likelihood is computed with `torch.logsumexp(weighted_ll, dim=-1)` rather than `torch.log((pi * component_likelihoods).sum(dim=-1))`. Why is this preferred?
<details>
<summary>Answer</summary>
`logsumexp` computes $\log\sum_k e^{x_k}$ in a numerically stable way by internally subtracting the maximum $x_k$ before exponentiating, so no term ever overflows and the result doesn't underflow to exactly zero. The naive alternative first exponentiates each component's log-density (`component_ll`) back into raw likelihoods, multiplies by $\pi_k$, sums, and takes a log — but component log-densities can be very negative in the tails (far from $\mu_k$), so `exp()` of them can silently underflow to 0.0 in floating point, especially early in training when $\sigma$ estimates are poorly calibrated. Once even one term underflows and the sum is dominated by rounding, the subsequent `log()` can produce `-inf` or `NaN` and break gradients. Working entirely in log-space with `logsumexp` avoids ever materializing the raw (potentially tiny) likelihoods, which is the standard numerically stable pattern for mixture-density training.
</details>

---

### Common Misconceptions

| Misconception | Reality |
|---|---|
| A more sophisticated, attention-based backbone always improves forecasts | On S&P 500 monthly returns, swapping backbones (including to the attention-based iTransformer) changed CRPS by under 1.5% at short horizons — smaller than the effect of just changing the output head. A simple linear model (DLinear) with a well-specified distributional head can match or beat an attention backbone with a point head. |
| If point-accuracy metrics (MSE/RMSE) can't distinguish models, the models don't really differ | The Model Confidence Set found no statistically significant differences among 12 backbone-head variants on squared error, yet CRPS revealed a clear, economically meaningful gradient across output heads. Point-accuracy metrics are blind to distributional quality; a model can be indistinguishable on MSE and still be meaningfully better or worse for risk management. |
| NLP positional encodings transfer directly to financial time series | Sinusoidal encodings assume evenly spaced, stationary tokens. Financial series have calendar gaps and non-stationary volatility, so trading-day-based or learned/relative positional encodings are typically needed instead. |
| A point forecast, if accurate enough, is sufficient for risk management | VaR and CVaR require quantiles and tail expectations of the full predictive distribution, not a conditional mean. The value of a distributional (density or mixture) head over a point forecast is largest precisely in high-volatility regimes — exactly when risk decisions matter most. |

## Related Concepts

- [[Regime Detection]] — a mixture output head implicitly learns regime-like structure without explicit state labels
- [[Deep Hedging]] — hedging policies need the shape of the P&L distribution, not just its mean
- [[Value at Risk]] — a quantile of the predictive distribution that a point head cannot supply
- [[Expected Shortfall]] — a tail expectation requiring the same distributional information
- [[Alpha Factor]] — attention-derived representations can serve as learned features/factors
- [[Overfitting and Multiple Testing]] — deep sequence models with many parameters are especially exposed to this risk on short financial histories

## Sources Used

- He, S. & Zhang, Y. (2026) — "Heads, Not Backbones: Output Heads Dominate Architectures on Fat-Tailed Returns" (arXiv:2606.30037)
- Vaswani, A. et al. (2017) — "Attention Is All You Need"

---

## Revision Log

| Date | Change | Trigger |
|------|--------|---------|
| 2026-07-26 | Full content written | Content gap remediation — deep learning coverage |
