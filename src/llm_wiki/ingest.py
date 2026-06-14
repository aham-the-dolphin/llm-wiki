import re
from datetime import date
from pathlib import Path

from .models import WikiPage
from .utils import console

WIKI_DIRECTORY = Path("wiki") / "Concepts"
FRONTMATTER = """---
title: {title}
created: {created}
updated: {updated}
status: active
tags:
  - ingested
---

"""
CONTENT_TEMPLATE = """# {title}

## Overview

Generated from source.

## Key Concepts

{key_concepts}

## Details

Generated via deterministic ingestion.

## Relationships

### Related Concepts

### Related Technologies

## Best Practices

## Risks and Limitations

## Contradictions

## References

| Source | Version | Date | Accessed | Type |
|---|---|---|---|---|

## Provenance Notes

Generated from {source}
"""

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)


def _slugify(value: str) -> str:
    cleaned = re.sub(r"[^\w\- ]+", "", value.lower())
    cleaned = re.sub(r"[\s_]+", "-", cleaned)
    cleaned = re.sub(r"-+", "-", cleaned)
    return cleaned.strip("-") or "page"


def _extract_headings(content: str) -> tuple[str | None, list[str]]:
    title: str | None = None
    extracted_headings: list[str] = []

    for match in HEADING_PATTERN.finditer(content):
        level = len(match.group(1))
        heading = match.group(2).strip()
        if level == 1 and title is None:
            title = heading
        if level in {2, 3}:
            extracted_headings.append(heading)

    return title, extracted_headings


def _build_page_content(title: str, source: str, headings: list[str]) -> str:
    date_stamp = date.today().isoformat()
    if headings:
        key_concepts = "\n".join(f"- {heading}" for heading in headings)
    else:
        key_concepts = "- none"

    return FRONTMATTER.format(title=title, created=date_stamp, updated=date_stamp) + CONTENT_TEMPLATE.format(
        title=title,
        key_concepts=key_concepts,
        source=source,
    )


def ingest_file(
    file_path: str,
    force: bool = False,
    dest_dir: Path | None = None,
) -> WikiPage:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(file_path)

    content = path.read_text(encoding="utf-8")
    title, headings = _extract_headings(content)
    title_text = title or path.stem.replace("-", " ").replace("_", " ").title()
    slug = _slugify(path.stem)
    destination_dir = dest_dir or WIKI_DIRECTORY
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / f"{slug}.md"

    if destination.exists() and not force:
        raise FileExistsError(f"Destination already exists: {destination}")

    page_content = _build_page_content(title_text, str(path), headings)
    destination.write_text(page_content, encoding="utf-8")
    console.print(f"[green]Ingested {file_path} into {destination}[/]")

    return WikiPage(
        title=title_text,
        source=str(path),
        destination=str(destination),
        metadata={
            "headings": headings,
            "provenance": "deterministic markdown ingestion",
        },
    )
