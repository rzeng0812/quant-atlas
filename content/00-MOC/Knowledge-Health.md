---
type: moc
tags: [moc, health]
---

# Knowledge Health Dashboard

> Surface stale, disputed, or low-confidence knowledge that needs attention.

This page is a maintainer tool, not published content. Each concept/model/strategy note
carries `stability`, `confidence`, `last_reviewed`, and `review_interval_days` frontmatter;
locally, with the [Dataview](https://blacksmithgu.github.io/obsidian-dataview/) Obsidian
plugin installed, the queries below surface notes overdue for review, disputed or
low-confidence notes, alpha-status drift in strategies, superseded papers, and stale
empirical notes. This site does not render Dataview, so the live queries aren't reproduced
here — open this vault in Obsidian with Dataview enabled to use the dashboard.

**Checks this dashboard runs locally:**
- Overdue for review — `last_reviewed` older than `review_interval_days`
- Disputed or low confidence — `confidence` is `low`/`disputed`, or tagged `disputed`
- Strategy alpha-status drift — all `type: strategy` notes by `alpha_status`
- Superseded or disputed papers — `70-Papers/` notes where `validity != active`
- Stale empirical notes — `stability: empirical` notes untouched for 30+ days
- Full stability map — every concept/model/strategy note by `stability` and `confidence`
