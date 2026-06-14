from pathlib import Path

from llm_wiki.provenance import provenance_report


def _build_page(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_provenance_extraction_and_scoring(tmp_path: Path) -> None:
    page = tmp_path / "wiki" / "Concepts" / "provenance.md"
    _build_page(
        page,
        "---\n"
        "title: Provenance Page\n"
        "created: 2026-06-14\n"
        "updated: 2026-06-15\n"
        "status: active\n"
        "---\n\n"
        "## References\n\n"
        "| Source | Version | Date | Accessed | Type |\n"
        "|---|---|---|---|---|\n"
        "Example | 1.0 | 2026-06-14 | 2026-06-15 | doc |\n\n"
        "## Provenance Notes\n"
        "Detailed provenance here.\n",
    )

    assert provenance_report(base_path=tmp_path)
    report = (tmp_path / "reports" / "provenance-report.md").read_text()
    assert "score: 100" in report
    assert "Provenance Page" in report


def test_provenance_missing_provenance(tmp_path: Path) -> None:
    page = tmp_path / "wiki" / "Concepts" / "missing-provenance.md"
    _build_page(
        page,
        "---\n"
        "title: Missing Provenance\n"
        "created: 2026-06-14\n"
        "updated: 2026-06-15\n"
        "status: active\n"
        "---\n\n"
        "## References\n\n"
        "| Source | Version | Date | Accessed | Type |\n"
        "|---|---|---|---|---|\n"
        "Example | 1.0 | 2026-06-14 | 2026-06-15 | doc |\n",
    )

    assert not provenance_report(base_path=tmp_path)
    report = (tmp_path / "reports" / "provenance-report.md").read_text()
    assert "score: " in report
    assert "provenance_notes: missing" in report


def test_provenance_report_generation(tmp_path: Path) -> None:
    page = tmp_path / "wiki" / "Concepts" / "report.md"
    _build_page(
        page,
        "---\n"
        "title: Report Page\n"
        "created: 2026-06-14\n"
        "updated: 2026-06-15\n"
        "status: active\n"
        "---\n\n"
        "## References\n\n"
        "| Source | Version | Date | Accessed | Type |\n"
        "|---|---|---|---|---|\n"
        "Example | 1.0 | 2026-06-14 | 2026-06-15 | doc |\n\n"
        "## Provenance Notes\n"
        "Notes.\n",
    )

    assert provenance_report(base_path=tmp_path)
    assert (tmp_path / "reports" / "provenance-report.md").exists()
