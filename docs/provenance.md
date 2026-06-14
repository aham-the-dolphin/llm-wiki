# Provenance

Provenance is the ability to trace the origin, evolution, and audit trail of wiki content.

## Lineage

Each wiki page includes metadata that records when it was created and last updated. Source references are captured in the `## References` section to document the origin of content.

## Auditability

The project generates a provenance report that summarizes completeness and missing fields for each page. This report makes it easy to identify pages that lack required traceability information.

## Traceability

The provenance pipeline verifies that wiki pages include:

- a title
- creation date
- update date
- status
- references section
- provenance notes section

By enforcing these elements, `llm-wiki` maintains a consistent audit trail for each page.

## Reporting

The provenance report produces a score for each page based on missing items. Scores are assigned as:

- `100` = complete
- `75` = missing one item
- `50` = missing two items
- `25` = missing three items
- `0` = missing four or more items

This helps teams prioritize content remediation and ensures that provenance quality is visible.
