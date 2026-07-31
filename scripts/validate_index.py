#!/usr/bin/env python3
from pathlib import Path
import sys
import yaml

ALLOWED_STATUSES = {"Queued", "Reading", "Completed", "Skimmed", "Revisit", "Reference"}
ALLOWED_PRIORITIES = {"Core", "Important", "Optional"}
REQUIRED_FIELDS = {
    "id", "title", "authors", "year", "field", "status", "priority",
    "inclusion_reason", "why_it_matters", "primary_source",
    "date_recommended", "date_completed", "related_papers"
}

def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)

data = yaml.safe_load(Path("papers.yaml").read_text(encoding="utf-8"))
papers = data.get("papers", [])
seen_ids = set()
seen_titles = set()
seen_links = set()

for paper in papers:
    missing = REQUIRED_FIELDS - set(paper)
    if missing:
        fail(f"{paper.get('id', '<unknown>')} missing fields: {sorted(missing)}")

    paper_id = paper["id"]
    title_key = " ".join(paper["title"].lower().split())
    link_key = paper["primary_source"].strip().lower()

    if paper_id in seen_ids:
        fail(f"duplicate ID: {paper_id}")
    if title_key in seen_titles:
        fail(f"duplicate title: {paper['title']}")
    if link_key in seen_links:
        fail(f"duplicate primary source: {paper['primary_source']}")
    if paper["status"] not in ALLOWED_STATUSES:
        fail(f"{paper_id} has invalid status: {paper['status']}")
    if paper["priority"] not in ALLOWED_PRIORITIES:
        fail(f"{paper_id} has invalid priority: {paper['priority']}")

    seen_ids.add(paper_id)
    seen_titles.add(title_key)
    seen_links.add(link_key)

print(f"Validated {len(papers)} papers.")
