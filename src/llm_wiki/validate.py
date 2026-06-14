from __future__ import annotations

from pathlib import Path
from typing import Any

import frontmatter
from rich.table import Table

from .utils import console

VALIDATION_FIELDS = ["title", "created", "updated", "status"]
REQUIRED_SECTIONS = ["## References", "## Provenance Notes"]
REPORT_PATH = Path("reports") / "validation-report.md"


def _validate_frontmatter(data: dict[str, Any]) -> list[str]:
    return [
        field for field in VALIDATION_FIELDS if field not in data or data[field] in (None, "")
    ]


def _validate_sections(content: str) -> list[str]:
    return [section for section in REQUIRED_SECTIONS if section not in content]


def _validate_page(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    missing_fields: list[str] = []
    missing_sections: list[str] = []

    if not raw.lstrip().startswith("---"):
        parsed = frontmatter.loads(raw)
        missing_fields = ["frontmatter"]
        missing_sections = _validate_sections(parsed.content)
        status = "invalid"
        return {
            "page": str(path),
            "status": status,
            "missing_fields": missing_fields,
            "missing_sections": missing_sections,
        }

    try:
        parsed = frontmatter.loads(raw)
    except Exception:
        return {
            "page": str(path),
            "status": "invalid",
            "missing_fields": ["frontmatter"],
            "missing_sections": ["References", "Provenance Notes"],
        }

    missing_fields = _validate_frontmatter(parsed.metadata)
    missing_sections = _validate_sections(parsed.content)
    status = "valid" if not missing_fields and not missing_sections else "invalid"

    return {
        "page": str(path),
        "status": status,
        "missing_fields": missing_fields,
        "missing_sections": missing_sections,
    }


def _write_report(results: list[dict[str, Any]], base_path: Path | None = None) -> None:
    base_path = base_path or Path.cwd()
    report_path = base_path / REPORT_PATH
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Validation Report\n"]
    for result in results:
        lines.append(f"## {result['page']}\n")
        lines.append(f"- status: {result['status']}\n")
        lines.append(
            f"- missing_fields: {', '.join(result['missing_fields']) or 'none'}\n"
        )
        lines.append(
            f"- missing_sections: {', '.join(result['missing_sections']) or 'none'}\n"
        )
        lines.append("\n")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def validate_sources(base_path: Path | None = None) -> bool:
    base_path = base_path or Path.cwd()
    console.print("[yellow]Validating wiki sources...[/]")
    page_paths = sorted((base_path / "wiki").glob("Concepts/*.md"))
    if not page_paths:
        console.print("[red]No wiki pages found in wiki/Concepts/[/]")
        return False

    table = Table(title="Validation Results")
    table.add_column("Page", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Missing Fields", style="yellow")
    table.add_column("Missing Sections", style="yellow")

    results: list[dict[str, Any]] = []
    all_passed = True

    for path in page_paths:
        result = _validate_page(path)
        results.append(result)
        if result["status"] != "valid":
            all_passed = False
        table.add_row(
            result["page"],
            result["status"],
            ", ".join(result["missing_fields"]) or "none",
            ", ".join(result["missing_sections"]) or "none",
        )

    console.print(table)
    _write_report(results, base_path)

    if all_passed:
        console.print("[green]All wiki pages passed validation.[/]")
    else:
        console.print("[red]Validation failed for one or more pages.[/]")

    return all_passed
