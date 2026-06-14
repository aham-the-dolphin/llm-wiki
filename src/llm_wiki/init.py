from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .utils import console

TEMPLATE_CONTENT = """---
title:
created:
updated:
status: active
tags: []
---

# Title

## Overview

## Key Concepts

## Details

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
"""

DIRECTORIES = [
    "prompts",
    "docs",
    "docs/adr",
    "templates",
    "examples",
    "reports",
    "sources",
    "wiki/Concepts",
    "wiki/Technologies",
    "wiki/Organizations",
    "wiki/Architectures",
    "wiki/Relationships",
    "tests",
]

TEMPLATES = [
    "templates/concept-page.md",
    "templates/technology-page.md",
    "templates/entity-page.md",
    "templates/organization-page.md",
    "templates/architecture-page.md",
]

EXAMPLE_FILE = "examples/source-doc.md"


def _ensure_directories(base_path: Path, directories: Iterable[str]) -> None:
    for directory in directories:
        path = base_path / directory
        path.mkdir(parents=True, exist_ok=True)


def _ensure_templates(base_path: Path, templates: Iterable[str]) -> None:
    for template in templates:
        path = base_path / template
        if not path.exists():
            path.write_text(TEMPLATE_CONTENT, encoding="utf-8")


def _ensure_example(base_path: Path, example_file: str) -> None:
    path = base_path / example_file
    if not path.exists():
        path.write_text("# Example source document\n\nThis is a placeholder source document for llm-wiki.\n", encoding="utf-8")


def initialize_project(base_path: Path | None = None) -> None:
    base_path = base_path or Path.cwd()
    _ensure_directories(base_path, DIRECTORIES)
    _ensure_templates(base_path, TEMPLATES)
    _ensure_example(base_path, EXAMPLE_FILE)
    console.print("[green]llm-wiki project initialized successfully.[/]")
