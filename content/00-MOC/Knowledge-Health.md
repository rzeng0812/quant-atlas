---
type: moc
tags: [moc, health]
---

# Knowledge Health Dashboard

> Surface stale, disputed, or low-confidence knowledge that needs attention.

---

## Overdue for Review

```dataview
TABLE last_reviewed, review_interval_days, stability, confidence
FROM ""
WHERE type = "concept" OR type = "model" OR type = "strategy"
WHERE last_reviewed < date(today) - dur(review_interval_days + "days")
SORT last_reviewed ASC
```

---

## Disputed or Low Confidence

```dataview
TABLE confidence, stability, last_reviewed
FROM ""
WHERE (type = "concept" OR type = "model" OR type = "strategy")
  AND (confidence = "low" OR confidence = "disputed" OR contains(tags, "disputed"))
SORT confidence ASC, last_reviewed ASC
```

---

## Strategies: Alpha Status Check

```dataview
TABLE alpha_status, confidence, last_reviewed, asset_class
FROM ""
WHERE type = "strategy"
SORT alpha_status ASC, last_reviewed ASC
```

---

## Papers: Superseded or Disputed

```dataview
TABLE validity, year, superseded_by
FROM "70-Papers"
WHERE validity != "active"
SORT validity ASC
```

---

## Stale Empirical Notes (>30 days)

```dataview
TABLE last_reviewed, stability
FROM ""
WHERE (type = "concept" OR type = "model" OR type = "strategy")
  AND stability = "empirical"
  AND last_reviewed < date(today) - dur(30 days)
SORT last_reviewed ASC
```

---

## All Notes — Stability Map

```dataview
TABLE stability, confidence, status, last_reviewed
FROM ""
WHERE type = "concept" OR type = "model" OR type = "strategy"
SORT stability ASC, confidence ASC
```
