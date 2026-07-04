#!/usr/bin/env python3
"""
ingest_papers.py — Fetch quant papers from arXiv and create Obsidian notes.

Usage:
    pip install arxiv
    python ingest_papers.py --vault ~/Documents/quant-atlas
    python ingest_papers.py --vault ~/Documents/quant-atlas --query "stochastic volatility" --max 10
"""

import argparse
import re
import time
from datetime import datetime
from pathlib import Path

try:
    import arxiv
except ImportError:
    raise SystemExit("Run: pip install arxiv")

# arXiv categories for quantitative finance
QUANT_CATEGORIES = {
    "q-fin.PR": "Pricing of Securities",
    "q-fin.PM": "Portfolio Management",
    "q-fin.TR": "Trading and Market Microstructure",
    "q-fin.ST": "Statistical Finance",
    "q-fin.RM": "Risk Management",
    "q-fin.MF": "Mathematical Finance",
    "q-fin.CP": "Computational Finance",
    "q-fin.EC": "Economics",
    "q-fin.GN": "General Finance",
    # ML + finance crossover
    "cs.LG": "Machine Learning (finance-relevant)",
}

# Default queries covering major quant topics
DEFAULT_QUERIES = [
    "cat:q-fin.PR",   # pricing
    "cat:q-fin.TR",   # trading / microstructure
    "cat:q-fin.PM",   # portfolio management
    "cat:q-fin.RM",   # risk management
]


def sanitize_filename(s: str, max_len: int = 80) -> str:
    s = re.sub(r'[<>:"/\\|?*]', "-", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:max_len]


def tag_from_categories(categories: list[str]) -> list[str]:
    tag_map = {
        "q-fin.PR": "pricing",
        "q-fin.PM": "portfolio",
        "q-fin.TR": "microstructure",
        "q-fin.ST": "statistical-finance",
        "q-fin.RM": "risk",
        "q-fin.MF": "math-finance",
        "q-fin.CP": "computational-finance",
        "cs.LG": "machine-learning",
        "cs.AI": "ai",
        "stat.ML": "machine-learning",
    }
    return [tag_map[c] for c in categories if c in tag_map]


def build_note(paper) -> str:
    authors = [a.name for a in paper.authors]
    author_str = ", ".join(authors[:5])
    if len(authors) > 5:
        author_str += f" et al."

    tags = tag_from_categories(paper.categories)
    tag_yaml = "[" + ", ".join(["paper", "unread"] + tags) + "]"

    arxiv_id = paper.entry_id.split("/")[-1]
    date_str = paper.published.strftime("%Y-%m-%d")

    return f"""---
type: paper
title: "{paper.title.replace('"', "'")}"
authors: [{', '.join(f'"{a}"' for a in authors[:8])}]
year: {paper.published.year}
arxiv_id: {arxiv_id}
categories: {paper.categories}
tags: {tag_yaml}
status: unread
added: {datetime.now().strftime("%Y-%m-%d")}
url: https://arxiv.org/abs/{arxiv_id}
---

## Abstract
{paper.summary.strip()}

## Key Contribution
*Fill after reading.*

## Methods
*Fill after reading.*

## Results
*Fill after reading.*

## Critique
*Fill after reading.*

## Relevance
*Fill after reading.*

## Related
-
"""


def ingest(vault_path: Path, query: str, max_results: int, days_back: int):
    papers_dir = vault_path / "70-Papers"
    papers_dir.mkdir(parents=True, exist_ok=True)

    client = arxiv.Client(page_size=50, delay_seconds=1.0)
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    created = 0
    skipped = 0

    for paper in client.results(search):
        # Skip if too old
        age_days = (datetime.now(paper.published.tzinfo) - paper.published).days
        if age_days > days_back:
            continue

        filename = sanitize_filename(paper.title) + ".md"
        path = papers_dir / filename

        if path.exists():
            skipped += 1
            continue

        path.write_text(build_note(paper))
        created += 1
        print(f"  + {paper.title[:70]}")
        time.sleep(0.1)

    print(f"\n  Created: {created}, Skipped (already exist): {skipped}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest arXiv quant papers into quant-atlas")
    parser.add_argument(
        "--vault",
        type=Path,
        default=Path.home() / "Documents" / "quant-atlas",
        help="Path to quant-atlas vault (default: ~/Documents/quant-atlas)",
    )
    parser.add_argument(
        "--query",
        type=str,
        default=None,
        help="arXiv query string (default: runs all quant categories)",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=20,
        help="Max papers per query (default: 20)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Only fetch papers from last N days (default: 90)",
    )
    args = parser.parse_args()

    if not args.vault.exists():
        raise SystemExit(f"Vault not found: {args.vault}\nRun bootstrap.py first.")

    queries = [args.query] if args.query else DEFAULT_QUERIES

    print(f"Ingesting into: {args.vault}")
    for q in queries:
        print(f"\nQuery: {q}")
        ingest(args.vault, q, args.max, args.days)
