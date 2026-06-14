from __future__ import annotations

from pathlib import Path
from typing import Any

import frontmatter
from rich.table import Table

from .utils import console

REPORT_PATH = Path("reports") / "provenance-report.md"
EXPECTED_FIELDS = ["title", "created", "updated", "status"]


def _extract_provenance_data(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    parsed = frontmatter.loads(raw)
    metadata = parsed.metadata

    references_present = "## References" in parsed.content
    provenance_notes_present = "## Provenance Notes" in parsed.content
    version = metadata.get("version", "unknown")
    accessed_date = None
    lines = [line for line in parsed.content.splitlines() if line.strip()]
    for index, line in enumerate(lines):
        if "Accessed" in line and "|" in line:
            for subsequent in lines[index + 1 :]:
                if "|" in subsequent and "---" not in subsequent:
                    columns = [col.strip() for col in subsequent.split("|") if col.strip()]
                    if len(columns) >= 4:
                        accessed_date = columns[3]
                    break
            break

    missing_items: list[str] = []
    for field in EXPECTED_FIELDS:
        if field not in metadata or metadata[field] in (None, ""):
            missing_items.append(field)

    if not references_present:
        missing_items.append("references")
    if not provenance_notes_present:
        missing_items.append("provenance_notes")

    score = max(0, 100 - 25 * len(missing_items))

    return {
        "page": metadata.get("title", path.stem.replace("-", " ").title()),
        "version": str(version),
        "accessed": accessed_date or "unknown",
        "updated": str(metadata.get("updated", "unknown")),
        "provenance_notes": "present" if provenance_notes_present else "missing",
        "missing_items": missing_items,
        "score": score,
    }


def _write_report(rows: list[dict[str, Any]], base_path: Path | None = None) -> None:
    base_path = base_path or Path.cwd()
    report_path = base_path / REPORT_PATH
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Provenance Report\n"]
    for row in rows:
        lines.append(f"## {row['page']}\n")
        lines.append(f"- version: {row['version']}\n")
        lines.append(f"- accessed: {row['accessed']}\n")
        lines.append(f"- updated: {row['updated']}\n")
        lines.append(f"- provenance_notes: {row['provenance_notes']}\n")
        lines.append(f"- missing_items: {', '.join(row['missing_items']) or 'none'}\n")
        lines.append(f"- score: {row['score']}\n")
        lines.append("\n")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def provenance_report(base_path: Path | None = None) -> bool:
    base_path = base_path or Path.cwd()
    console.print("[cyan]Generating provenance report...[/]")
    page_paths = sorted((base_path / "wiki").glob("Concepts/*.md"))
    if not page_paths:
        console.print("[red]No wiki pages found in wiki/Concepts/[/]")
        return False

    rows: list[dict[str, Any]] = []
    all_passed = True
    table = Table(title="Provenance Report")
    table.add_column("Page", style="cyan")
    table.add_column("Version", style="green")
    table.add_column("Accessed", style="yellow")
    table.add_column("Updated", style="yellow")
    table.add_column("Score", style="magenta")
    table.add_column("Missing Items", style="red")

    for path in page_paths:
        row = _extract_provenance_data(path)
        rows.append(row)
        if row["score"] < 100:
            all_passed = False
        table.add_row(
            row["page"],
            row["version"],
            row["accessed"],
            row["updated"],
            str(row["score"]),
            ", ".join(row["missing_items"]) or "none",
        )

    console.print(table)
    _write_report(rows, base_path)
    if all_passed:
        console.print("[green]Provenance report complete: all pages scored 100.[/]")
    else:
        console.print("[yellow]Provenance report generated with missing items.[/]")

    return all_passed
