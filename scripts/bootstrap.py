#!/usr/bin/env python3
"""
bootstrap.py — Creates the quant-atlas Obsidian vault structure.
Run: python bootstrap.py [--vault-path /path/to/vaults]
"""

import argparse
import textwrap
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

VAULT_NAME = "quant-atlas"

DIRS = [
    "00-MOC",
    "10-Foundations/Math",
    "10-Foundations/Statistics",
    "10-Foundations/Probability",
    "20-Markets/Equities",
    "20-Markets/Fixed-Income",
    "20-Markets/Derivatives",
    "20-Markets/FX",
    "20-Markets/Crypto",
    "30-Models/Pricing",
    "30-Models/Risk",
    "30-Models/Alpha",
    "40-Strategies/Statistical-Arb",
    "40-Strategies/Market-Making",
    "40-Strategies/Trend-Following",
    "40-Strategies/Options-Strategies",
    "40-Strategies/HFT",
    "50-Implementation/Backtesting",
    "50-Implementation/Execution",
    "50-Implementation/Data-Engineering",
    "50-Implementation/Infrastructure",
    "60-ML-Finance/Feature-Engineering",
    "60-ML-Finance/Regime-Detection",
    "60-ML-Finance/Deep-Learning",
    "60-ML-Finance/Reinforcement-Learning",
    "70-Papers/_pdfs",
    "80-Books",
    "90-Code-Snippets",
    "99-Templates",
    ".obsidian",
    "01-Paths",
    "95-Source-Captures",
]

# ── Concept seeds (title → tags, domain, one-line summary) ───────────────────

CONCEPTS = {
    # Math foundations
    "Ito's Lemma": ("math stochastic-calculus", "10-Foundations/Math",
        "Stochastic chain rule: df = f_x dX + ½f_xx (dX)² + f_t dt"),
    "Brownian Motion": ("math stochastic-calculus probability", "10-Foundations/Math",
        "Continuous-time random walk; foundation of most asset price models"),
    "Geometric Brownian Motion": ("math stochastic-calculus models", "10-Foundations/Math",
        "dS = μS dt + σS dW — standard lognormal price model"),
    "Stochastic Differential Equations": ("math stochastic-calculus", "10-Foundations/Math",
        "ODEs driven by Brownian motion; solved via Ito calculus"),
    "Martingales": ("math probability", "10-Foundations/Probability",
        "Fair game process: E[X_{t+1} | F_t] = X_t"),
    "Risk-Neutral Measure": ("math probability derivatives", "10-Foundations/Probability",
        "Equivalent measure under which discounted prices are martingales"),
    "Girsanov Theorem": ("math stochastic-calculus probability", "10-Foundations/Math",
        "Change of measure for Brownian motion; used to move to risk-neutral world"),

    # Pricing models
    "Black-Scholes Model": ("pricing options derivatives", "30-Models/Pricing",
        "Closed-form option pricing under GBM; C = S·N(d1) - K·e^{-rT}·N(d2)"),
    "Heston Model": ("pricing options stochastic-volatility", "30-Models/Pricing",
        "Mean-reverting stochastic variance; captures vol smile"),
    "SABR Model": ("pricing options stochastic-volatility interest-rates", "30-Models/Pricing",
        "Stochastic alpha-beta-rho; industry standard for rates options"),
    "Local Volatility": ("pricing options volatility-surface", "30-Models/Pricing",
        "Dupire's σ(S,t) that exactly fits the vol surface"),
    "HJM Framework": ("pricing interest-rates fixed-income", "30-Models/Pricing",
        "Models evolution of forward rate curve directly"),
    "Vasicek Model": ("pricing interest-rates fixed-income", "30-Models/Pricing",
        "Mean-reverting short rate: dr = a(b-r)dt + σdW"),

    # Greeks
    "Option Greeks": ("derivatives options risk", "20-Markets/Derivatives",
        "Delta, Gamma, Theta, Vega, Rho — sensitivities of option price"),
    "Delta Hedging": ("derivatives options risk-management", "20-Markets/Derivatives",
        "Dynamic replication by holding Δ shares to offset option exposure"),
    "Gamma Scalping": ("derivatives options strategies", "40-Strategies/Options-Strategies",
        "Profit from realized vol > implied vol via delta-hedge rebalancing"),

    # Volatility
    "Implied Volatility": ("volatility options markets", "20-Markets/Derivatives",
        "Vol that equates BSM price to market price; forward-looking"),
    "Volatility Surface": ("volatility options", "30-Models/Pricing",
        "IV as function of strike and expiry; captures smile and term structure"),
    "Volatility Smile": ("volatility options", "20-Markets/Derivatives",
        "U-shape of IV vs strike; fat tails / skew in real distributions"),
    "VIX": ("volatility markets risk", "20-Markets/Equities",
        "CBOE 30-day implied vol index; model-free via variance swaps"),
    "Variance Swap": ("derivatives volatility", "20-Markets/Derivatives",
        "Payoff = N·(σ²_realized − K_var); pure vol exposure"),

    # Risk
    "Value at Risk": ("risk portfolio", "30-Models/Risk",
        "Max loss at confidence level α over horizon T"),
    "Expected Shortfall": ("risk portfolio", "30-Models/Risk",
        "CVaR: expected loss beyond VaR; coherent risk measure"),
    "Factor Models": ("risk portfolio alpha", "30-Models/Risk",
        "Decompose returns into systematic factors (Fama-French, Barra)"),
    "Kelly Criterion": ("risk portfolio sizing", "30-Models/Risk",
        "Optimal bet size: f* = (bp - q) / b; maximizes log wealth"),
    "Sharpe Ratio": ("portfolio performance", "30-Models/Risk",
        "Risk-adjusted return: (R_p - R_f) / σ_p"),
    "Maximum Drawdown": ("risk portfolio performance", "30-Models/Risk",
        "Largest peak-to-trough decline; key strategy evaluation metric"),

    # Strategies
    "Statistical Arbitrage": ("strategy equity mean-reversion", "40-Strategies/Statistical-Arb",
        "Exploit mean-reversion in spreads of co-integrated instruments"),
    "Pairs Trading": ("strategy equity mean-reversion", "40-Strategies/Statistical-Arb",
        "Long-short pairs with cointegrated prices; Ornstein-Uhlenbeck spread"),
    "Momentum": ("strategy equity factor", "40-Strategies/Trend-Following",
        "Buy recent winners, sell recent losers; 12-1 month lookback"),
    "Mean Reversion": ("strategy equity", "40-Strategies/Statistical-Arb",
        "Prices revert to long-run mean; Hurst exponent H < 0.5"),
    "Market Making": ("strategy microstructure HFT", "40-Strategies/Market-Making",
        "Post bids and offers; profit from bid-ask spread minus adverse selection"),
    "Avellaneda-Stoikov": ("strategy market-making HFT", "40-Strategies/Market-Making",
        "Optimal MM model with inventory risk and order flow"),

    # Microstructure
    "Order Book": ("microstructure markets", "20-Markets/Equities",
        "LOB: queued limit orders at each price level; market state"),
    "Adverse Selection": ("microstructure market-making", "20-Markets/Equities",
        "MM risk of trading with informed counterparties"),
    "Price Impact": ("microstructure execution", "50-Implementation/Execution",
        "Market impact of order flow; temporary vs permanent components"),
    "TWAP-VWAP": ("execution algorithms", "50-Implementation/Execution",
        "Benchmark execution algorithms; minimize market impact over time"),
    "Almgren-Chriss": ("execution models", "50-Implementation/Execution",
        "Optimal execution balancing market impact vs timing risk"),

    # Fixed income
    "Duration": ("fixed-income risk interest-rates", "20-Markets/Fixed-Income",
        "Price sensitivity to yield changes; weighted avg time to cash flows"),
    "Convexity": ("fixed-income risk interest-rates", "20-Markets/Fixed-Income",
        "Second-order yield sensitivity; positive for bonds (long gamma analog)"),
    "Yield Curve": ("fixed-income markets interest-rates", "20-Markets/Fixed-Income",
        "Term structure of interest rates; normal/inverted/humped shapes"),

    # ML-Finance bridge
    "Alpha Factor": ("ml-finance alpha signals", "60-ML-Finance/Feature-Engineering",
        "Predictive signal for future returns; IC measures quality"),
    "Regime Detection": ("ml-finance regimes", "60-ML-Finance/Regime-Detection",
        "Identify market states (bull/bear/crisis) via HMM or clustering"),
    "Feature Engineering Finance": ("ml-finance features", "60-ML-Finance/Feature-Engineering",
        "Transform raw price/volume/alt-data into predictive ML features"),
    "Reinforcement Learning Trading": ("ml-finance rl execution", "60-ML-Finance/Reinforcement-Learning",
        "Model execution/allocation as MDP; reward = risk-adjusted PnL"),
}

# ── MOC contents ─────────────────────────────────────────────────────────────

MOCS = {
    "Home": {
        "icon": "🗺️",
        "description": "Root index of quant-atlas",
        "links": [
            "[[00-MOC/Mathematics]]",
            "[[00-MOC/Derivatives]]",
            "[[00-MOC/Portfolio-Theory]]",
            "[[00-MOC/Risk-Management]]",
            "[[00-MOC/Algo-Trading]]",
            "[[00-MOC/Market-Microstructure]]",
            "[[00-MOC/ML-Finance]]",
        ],
        "dataview": textwrap.dedent("""\
            ```dataview
            TABLE file.mtime as "Updated", tags
            FROM ""
            WHERE type = "concept" AND file.mtime >= date(today) - dur(7 days)
            SORT file.mtime DESC
            LIMIT 20
            ```"""),
    },
    "Mathematics": {
        "icon": "∑",
        "description": "Stochastic calculus, PDEs, probability theory",
        "links": [
            "[[Brownian Motion]]", "[[Geometric Brownian Motion]]",
            "[[Ito's Lemma]]", "[[Stochastic Differential Equations]]",
            "[[Martingales]]", "[[Risk-Neutral Measure]]", "[[Girsanov Theorem]]",
        ],
        "dataview": textwrap.dedent("""\
            ```dataview
            TABLE file.folder as "Location", tags
            FROM "10-Foundations"
            WHERE type = "concept"
            SORT file.name ASC
            ```"""),
    },
    "Derivatives": {
        "icon": "📐",
        "description": "Pricing models, Greeks, volatility",
        "links": [
            "[[Black-Scholes Model]]", "[[Heston Model]]", "[[SABR Model]]",
            "[[Local Volatility]]", "[[Option Greeks]]", "[[Delta Hedging]]",
            "[[Implied Volatility]]", "[[Volatility Surface]]", "[[Variance Swap]]",
        ],
        "dataview": textwrap.dedent("""\
            ```dataview
            TABLE tags
            FROM "30-Models/Pricing"
            WHERE type = "concept"
            SORT file.name ASC
            ```"""),
    },
    "Risk-Management": {
        "icon": "⚖️",
        "description": "VaR, factor models, portfolio risk",
        "links": [
            "[[Value at Risk]]", "[[Expected Shortfall]]", "[[Factor Models]]",
            "[[Kelly Criterion]]", "[[Sharpe Ratio]]", "[[Maximum Drawdown]]",
            "[[Duration]]", "[[Convexity]]",
        ],
        "dataview": textwrap.dedent("""\
            ```dataview
            TABLE tags
            FROM "30-Models/Risk"
            WHERE type = "concept"
            SORT file.name ASC
            ```"""),
    },
    "Algo-Trading": {
        "icon": "⚡",
        "description": "Strategies, execution, backtesting",
        "links": [
            "[[Statistical Arbitrage]]", "[[Pairs Trading]]", "[[Momentum]]",
            "[[Mean Reversion]]", "[[Market Making]]", "[[Avellaneda-Stoikov]]",
            "[[TWAP-VWAP]]", "[[Almgren-Chriss]]",
        ],
        "dataview": textwrap.dedent("""\
            ```dataview
            TABLE tags
            FROM "40-Strategies" OR "50-Implementation"
            WHERE type = "concept"
            SORT file.name ASC
            ```"""),
    },
    "Market-Microstructure": {
        "icon": "🔬",
        "description": "Order books, market impact, adverse selection",
        "links": [
            "[[Order Book]]", "[[Adverse Selection]]", "[[Price Impact]]",
            "[[Market Making]]", "[[TWAP-VWAP]]",
        ],
        "dataview": textwrap.dedent("""\
            ```dataview
            TABLE tags
            FROM ""
            WHERE contains(tags, "microstructure")
            SORT file.name ASC
            ```"""),
    },
    "ML-Finance": {
        "icon": "🤖",
        "description": "Bridge between ML/AI and quantitative finance",
        "links": [
            "[[Alpha Factor]]", "[[Regime Detection]]",
            "[[Feature Engineering Finance]]", "[[Reinforcement Learning Trading]]",
        ],
        "dataview": textwrap.dedent("""\
            ```dataview
            TABLE tags
            FROM "60-ML-Finance"
            WHERE type = "concept"
            SORT file.name ASC
            ```"""),
        "cross_vault": textwrap.dedent("""\
            ## Cross-Vault Links (neutral-path)
            > Connect experiments from neutral-path using Obsidian URIs:
            > `[Experiment](obsidian://open?vault=neutral-path&file=experiments/...)`
            """),
    },
    "Portfolio-Theory": {
        "icon": "📊",
        "description": "MPT, optimization, performance attribution",
        "links": [
            "[[Factor Models]]", "[[Kelly Criterion]]", "[[Sharpe Ratio]]",
            "[[Maximum Drawdown]]", "[[Value at Risk]]", "[[Expected Shortfall]]",
        ],
        "dataview": textwrap.dedent("""\
            ```dataview
            TABLE tags
            FROM ""
            WHERE contains(tags, "portfolio")
            SORT file.name ASC
            ```"""),
    },
}

# ── Templates ─────────────────────────────────────────────────────────────────

TEMPLATES = {
    "concept": textwrap.dedent("""\
        ---
        type: concept
        domain:
        tags: []
        status: stub
        created: <% tp.date.now("YYYY-MM-DD") %>
        ---

        ## Definition

        ## Intuition

        ## Mathematics
        $$
        $$

        ## Key Properties
        -

        ## Applications
        -

        ## Limitations / Assumptions
        -

        ## Related Concepts
        -

        ## References
        -
        """),

    "model": textwrap.dedent("""\
        ---
        type: model
        domain: [pricing/risk/alpha]
        asset_class: [equity/rates/fx/credit]
        complexity: [closed-form/numerical/simulation]
        tags: []
        status: stub
        created: <% tp.date.now("YYYY-MM-DD") %>
        ---

        ## Intuition

        ## Mathematics
        $$
        $$

        ## Parameters
        | Parameter | Meaning | Calibration Method |
        |-----------|---------|-------------------|
        |           |         |                   |

        ## Assumptions
        -

        ## Limitations
        -

        ## Calibration

        ## Implementation
        - [[90-Code-Snippets/]]

        ## Related Models
        -

        ## Papers
        -
        """),

    "strategy": textwrap.dedent("""\
        ---
        type: strategy
        alpha_source: [momentum/mean-reversion/carry/vol/flow/ml]
        holding_period:
        asset_class:
        tags: []
        status: stub
        created: <% tp.date.now("YYYY-MM-DD") %>
        ---

        ## Core Idea

        ## Entry Logic

        ## Exit Logic

        ## Position Sizing

        ## Risk Controls
        -

        ## Performance Characteristics
        | Metric | Typical Range |
        |--------|--------------|
        | Sharpe |              |
        | Max DD |              |
        | Capacity |           |

        ## Known Pitfalls
        -

        ## Related Strategies
        -

        ## Papers / References
        -
        """),

    "paper": textwrap.dedent("""\
        ---
        type: paper
        title:
        authors: []
        year:
        venue:
        arxiv_id:
        tags: []
        status: unread
        added: <% tp.date.now("YYYY-MM-DD") %>
        ---

        ## Abstract

        ## Key Contribution

        ## Methods

        ## Results

        ## Critique

        ## Relevance to My Work

        ## Related Papers
        -
        """),

    "book": textwrap.dedent("""\
        ---
        type: book
        title:
        author:
        year:
        tags: []
        status: unread
        started:
        finished:
        ---

        ## Overview

        ## Key Takeaways
        1.

        ## Chapter Notes

        ## Quotes

        ## Related Books
        -
        """),

    "code-snippet": textwrap.dedent("""\
        ---
        type: code-snippet
        language: python
        domain:
        tags: []
        created: <% tp.date.now("YYYY-MM-DD") %>
        ---

        ## Purpose

        ## Code
        ```python

        ```

        ## Usage Example
        ```python

        ```

        ## Notes
        -

        ## Related Concepts
        -
        """),
}

# ── Obsidian config ────────────────────────────────────────────────────────────

OBSIDIAN_APP_JSON = """{
  "defaultViewMode": "source",
  "livePreview": true,
  "foldHeading": false,
  "useTab": false,
  "tabSize": 2,
  "spellcheck": false,
  "strictLineBreaks": false,
  "showFrontmatter": true,
  "allowIframesByDefault": false,
  "newFileLocation": "folder",
  "newFileFolderPath": "10-Foundations",
  "attachmentFolderPath": "./_assets",
  "readableLineLength": true
}
"""

OBSIDIAN_PLUGINS_JSON = """{
  "enabledCorePlugins": [
    "file-explorer",
    "global-search",
    "switcher",
    "graph",
    "backlink",
    "outgoing-link",
    "tag-pane",
    "page-preview",
    "daily-notes",
    "templates",
    "command-palette",
    "word-count",
    "outline",
    "starred",
    "markdown-importer",
    "theme-picker",
    "canvas"
  ]
}
"""

HOTKEYS_JSON = """{
  "editor:toggle-source": [{"modifiers":["Mod","Shift"],"key":"E"}],
  "graph:open": [{"modifiers":["Mod","Shift"],"key":"G"}],
  "switcher:open": [{"modifiers":["Mod"],"key":"O"}]
}
"""

# ── Builders ──────────────────────────────────────────────────────────────────

def _infer_stability(folder: str) -> str:
    """Infer stability from folder location."""
    if folder.startswith("10-Foundations") or folder.startswith("20-Markets"):
        return "stable"
    if folder.startswith("30-Models") or folder.startswith("60-ML-Finance"):
        return "evolving"
    if folder.startswith("40-Strategies") or folder.startswith("50-Implementation"):
        return "empirical"
    return "evolving"


def _review_interval(stability: str) -> int:
    return {"stable": 365, "evolving": 90, "empirical": 30}[stability]


def build_concept_note(name: str, tags: str, folder: str, summary: str) -> str:
    tag_list = "[" + ", ".join(tags.split()) + "]"
    stability = _infer_stability(folder)
    interval = _review_interval(stability)
    today = "2026-04-12"
    return textwrap.dedent(f"""\
        ---
        type: concept
        domain: {folder.split("/")[0]}
        tags: {tag_list}
        status: stub
        stability: {stability}
        confidence: medium
        last_reviewed: {today}
        review_interval_days: {interval}
        sources: []
        created: {today}
        ---

        > {summary}

        ## Motivation

        ## Math Concepts

        ## Walkthrough

        ## Analysis
        -

        ## Implementation
        -

        ## Bridge to Quant / ML
        -

        ## Related Concepts
        -

        ## Sources Used
        -

        ---

        ## Revision Log

        | Date | Change | Trigger |
        |------|--------|---------|
        | {today} | Note created | bootstrap |
        """)


def build_moc_note(name: str, data: dict) -> str:
    links_block = "\n".join(f"- {l}" for l in data["links"])
    cross = data.get("cross_vault", "")
    return textwrap.dedent(f"""\
        ---
        type: moc
        tags: [moc]
        ---

        # {data['icon']} {name}
        {data['description']}

        ## Concepts
        {links_block}

        {cross}
        ## All Notes
        {data['dataview']}
        """)


def build_home_note(data: dict) -> str:
    links_block = "\n".join(f"- {l}" for l in data["links"])
    return textwrap.dedent(f"""\
        ---
        type: home
        tags: [moc, home]
        ---

        # quant-atlas

        > A comprehensive knowledge base for quantitative finance.

        ## Maps of Content
        {links_block}

        ## Recently Updated
        {data['dataview']}

        ## Quick Links
        - [[99-Templates/concept|New Concept]]
        - [[99-Templates/paper|New Paper]]
        - [[99-Templates/strategy|New Strategy]]
        - [[70-Papers|Papers]]
        - [[90-Code-Snippets|Code]]
        """)


# ── Main ──────────────────────────────────────────────────────────────────────

def bootstrap(vault_root: Path):
    vault = vault_root / VAULT_NAME
    print(f"Creating vault at: {vault}")

    # Directories
    for d in DIRS:
        (vault / d).mkdir(parents=True, exist_ok=True)

    # Concept notes — overwrite stubs, preserve notes with real content
    for name, (tags, folder, summary) in CONCEPTS.items():
        path = vault / folder / f"{name}.md"
        if path.exists():
            content = path.read_text()
            # Only overwrite if still a stub (no user-written content in body sections)
            if "status: stub" not in content:
                continue
        path.write_text(build_concept_note(name, tags, folder, summary))

    # MOC notes
    for moc_name, data in MOCS.items():
        if moc_name == "Home":
            path = vault / "Home.md"
            path.write_text(build_home_note(data))
        else:
            path = vault / "00-MOC" / f"{moc_name}.md"
            path.write_text(build_moc_note(moc_name, data))

    # Templates — never overwrite; vault files are source of truth
    for tname, content in TEMPLATES.items():
        path = vault / "99-Templates" / f"{tname}.md"
        if not path.exists():
            path.write_text(content)

    # Obsidian config
    (vault / ".obsidian" / "app.json").write_text(OBSIDIAN_APP_JSON)
    (vault / ".obsidian" / "core-plugins.json").write_text(OBSIDIAN_PLUGINS_JSON)
    (vault / ".obsidian" / "hotkeys.json").write_text(HOTKEYS_JSON)

    # Gitignore
    (vault / ".gitignore").write_text(".obsidian/workspace*\n.obsidian/cache\n_assets/\n")

    # README
    (vault / "README.md").write_text(textwrap.dedent(f"""\
        # quant-atlas

        Quantitative finance knowledge base. Open in Obsidian.

        ## Structure
        - `00-MOC/` — Maps of Content (start here)
        - `10-Foundations/` — Math, statistics, probability
        - `20-Markets/` — Asset classes
        - `30-Models/` — Pricing, risk, alpha models
        - `40-Strategies/` — Trading strategies
        - `50-Implementation/` — Backtesting, execution, infra
        - `60-ML-Finance/` — ML/AI applications in finance
        - `70-Papers/` — Literature notes
        - `80-Books/` — Book summaries
        - `90-Code-Snippets/` — Annotated implementations
        - `99-Templates/` — Note templates

        ## Recommended Obsidian Plugins
        - Dataview
        - Templater
        - Excalidraw
        - QuickAdd
        - Obsidian Git
        """))

    # Count
    notes = list(vault.rglob("*.md"))
    print(f"\n✓ Vault created: {vault}")
    print(f"  {len(notes)} notes across {len(DIRS)} directories")
    print(f"\nOpen in Obsidian: File → Open Vault → {vault}")
    print(f"Then install plugins: Dataview, Templater, Excalidraw, QuickAdd, Obsidian Git")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap quant-atlas Obsidian vault")
    parser.add_argument(
        "--vault-path",
        type=Path,
        default=Path.home() / "Documents",
        help="Parent directory where quant-atlas/ will be created (default: ~/Documents)",
    )
    args = parser.parse_args()
    bootstrap(args.vault_path)
