# quant-atlas

A quantitative finance knowledge base — browse it as an [Obsidian](https://obsidian.md) vault or read it as a static site at [rzeng0812.github.io/quant-atlas](https://rzeng0812.github.io/quant-atlas).

## What's in here

```
quant-atlas/
├── content/              ← Obsidian vault (open this folder in Obsidian)
│   ├── 00-MOC/           ← Maps of Content — start here
│   ├── 10-Foundations/   ← Math, statistics, probability
│   ├── 20-Markets/       ← Asset classes (equities, rates, FX, crypto)
│   ├── 30-Models/        ← Pricing, risk, and alpha models
│   ├── 40-Strategies/    ← Trading strategies
│   ├── 50-Implementation/← Backtesting, execution, infrastructure
│   ├── 60-ML-Finance/    ← ML/AI applications in finance
│   ├── 70-Papers/        ← Literature notes (arXiv + manual)
│   ├── 80-Books/         ← Book summaries
│   ├── 90-Code-Snippets/ ← Annotated implementations
│   └── 99-Templates/     ← Note templates
└── scripts/
    ├── bootstrap.py      ← Scaffold/re-seed the vault structure
    └── ingest_papers.py  ← Fetch arXiv papers as notes
```

## Using as an Obsidian vault

1. Open Obsidian → **File → Open folder as vault** → select `content/`
2. Install recommended plugins via **Settings → Community plugins**:
   - **Dataview** — powers the dynamic index tables in MOC notes
   - **Templater** — enables the note templates in `99-Templates/`
   - **Excalidraw** — for diagrams
   - **QuickAdd** — fast note creation from templates
   - **Obsidian Git** — auto-commit and sync

Start in `content/Home.md` or any `00-MOC/` file.

## Scripts

### Bootstrap the vault

Re-seeds concept stubs, folder structure, MOC files, and templates. Safe to re-run — it skips any note that has already been edited (no longer `status: stub`).

```bash
python scripts/bootstrap.py --vault-path ~/Documents
# Creates ~/Documents/quant-atlas/
```

### Ingest arXiv papers

Fetches recent papers from quantitative finance arXiv categories and creates Obsidian notes in `70-Papers/`.

```bash
pip install arxiv
python scripts/ingest_papers.py --vault ~/Documents/quant-atlas
# Optional: filter by query
python scripts/ingest_papers.py --vault ~/Documents/quant-atlas --query "stochastic volatility" --max 10
```

## Publishing the site

The site is built with [Quartz v4](https://quartz.jzhao.xyz) and deployed automatically to GitHub Pages on every push to `v4`.

To preview locally:

```bash
npm install
npx quartz build --serve
# Opens at http://localhost:8080
```

To deploy manually:

```bash
npx quartz sync
```

## Keeping Quartz up to date

This repo tracks the upstream Quartz framework as a separate remote:

```bash
git fetch upstream
git merge upstream/v4
```

## Structure conventions

Each note has frontmatter with `type`, `tags`, `status`, and `stability`:

| `status`   | Meaning                          |
|------------|----------------------------------|
| `stub`     | Auto-generated, not yet written  |
| `draft`    | In progress                      |
| `complete` | Reviewed and finished            |

| `stability` | Review interval |
|-------------|-----------------|
| `stable`    | 365 days        |
| `evolving`  | 90 days         |
| `empirical` | 30 days         |
