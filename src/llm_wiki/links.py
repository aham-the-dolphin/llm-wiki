from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from rich.table import Table

from .utils import console

LINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")
REPORT_PATH = Path("reports") / "link-report.md"


def _find_pages(base_path: Path) -> dict[str, Path]:
    pages: dict[str, Path] = {}
    for path in sorted((base_path / "wiki").glob("Concepts/*.md")):
        title = path.stem.replace("-", " ").replace("_", " ").title()
        pages[title] = path
    return pages


def _extract_links(content: str) -> list[str]:
    return [match.group(1).strip() for match in LINK_PATTERN.finditer(content)]


def _write_report(results: dict[str, Any], base_path: Path | None = None) -> None:
    base_path = base_path or Path.cwd()
    report_path = base_path / REPORT_PATH
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines = ["# Link Report\n"]
    for page, data in results.items():
        lines.append(f"## {page}\n")
        lines.append(f"- broken_links: {', '.join(data['broken_links']) or 'none'}\n")
        lines.append(f"- orphan_pages: {', '.join(data['orphan_pages']) or 'none'}\n")
        lines.append(f"- circular_references: {', '.join(data['circular_references']) or 'none'}\n")
        lines.append("\n")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def _detect_circular_references(graph: dict[str, list[str]]) -> list[str]:
    visited: set[str] = set()
    stack: set[str] = set()
    circular: set[str] = set()

    def visit(node: str) -> None:
        if node in stack:
            circular.update(stack)
            return
        if node in visited:
            return
        visited.add(node)
        stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor in graph:
                visit(neighbor)
        stack.remove(node)

    for node in graph:
        visit(node)
    return sorted(circular)


def _find_orphans(graph: dict[str, list[str]], pages: set[str]) -> list[str]:
    incoming: defaultdict[str, int] = defaultdict(int)
    for source, targets in graph.items():
        for target in targets:
            if target in pages:
                incoming[target] += 1
    orphans = sorted(page for page in pages if incoming[page] == 0 and graph.get(page, []) != [])
    return orphans


def check_links(base_path: Path | None = None) -> bool:
    base_path = base_path or Path.cwd()
    console.print("[yellow]Checking links...[/]")
    pages = _find_pages(base_path)
    if not pages:
        console.print("[red]No wiki pages found in wiki/Concepts/[/]")
        return False

    graph: dict[str, list[str]] = {}
    broken_links: dict[str, list[str]] = {}

    for title, path in pages.items():
        content = path.read_text(encoding="utf-8")
        links = _extract_links(content)
        graph[title] = links
        broken_links[title] = [link for link in links if link not in pages]

    circular_references = _detect_circular_references(graph)
    orphans = _find_orphans(graph, set(pages))
    all_passed = not any(broken_links.values()) and not orphans

    table = Table(title="Link Validation")
    table.add_column("Page", style="cyan")
    table.add_column("Broken Links", style="red")
    table.add_column("Orphan Pages", style="yellow")
    table.add_column("Circular References", style="magenta")

    results: dict[str, Any] = {}
    for page in sorted(pages):
        page_broken = broken_links.get(page, [])
        page_orphans = [p for p in orphans if p == page]
        page_circular = [p for p in circular_references if p == page]
        table.add_row(
            page,
            ", ".join(page_broken) or "none",
            ", ".join(page_orphans) or "none",
            ", ".join(page_circular) or "none",
        )
        results[page] = {
            "broken_links": page_broken,
            "orphan_pages": page_orphans,
            "circular_references": page_circular,
        }

    console.print(table)
    _write_report(results, base_path)

    if all_passed:
        console.print("[green]Link validation passed.[/]")
    else:
        console.print("[red]Link validation failed.[/]")

    return all_passed
