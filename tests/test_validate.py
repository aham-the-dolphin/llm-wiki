from pathlib import Path

from llm_wiki.validate import validate_sources


def _build_page(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_validate_valid_page(tmp_path: Path) -> None:
    page = tmp_path / "wiki" / "Concepts" / "valid.md"
    _build_page(
        page,
        "---\n"
        "title: Valid Page\n"
        "created: 2026-06-14\n"
        "updated: 2026-06-14\n"
        "status: active\n"
        "---\n\n"
        "## References\n\n"
        "## Provenance Notes\n",
    )

    assert validate_sources(base_path=tmp_path)
    assert (tmp_path / "reports" / "validation-report.md").exists()


def test_validate_missing_frontmatter(tmp_path: Path) -> None:
    page = tmp_path / "wiki" / "Concepts" / "missing-frontmatter.md"
    _build_page(page, "# Missing frontmatter\n\n## References\n\n## Provenance Notes\n")

    assert not validate_sources(base_path=tmp_path)
    report = (tmp_path / "reports" / "validation-report.md").read_text()
    assert "missing_fields: frontmatter" in report


def test_validate_missing_references(tmp_path: Path) -> None:
    page = tmp_path / "wiki" / "Concepts" / "missing-references.md"
    _build_page(
        page,
        "---\n"
        "title: No References\n"
        "created: 2026-06-14\n"
        "updated: 2026-06-14\n"
        "status: active\n"
        "---\n\n"
        "## Provenance Notes\n",
    )

    assert not validate_sources(base_path=tmp_path)
    report = (tmp_path / "reports" / "validation-report.md").read_text()
    assert "missing_sections: ## References" in report


def test_validate_missing_provenance(tmp_path: Path) -> None:
    page = tmp_path / "wiki" / "Concepts" / "missing-provenance.md"
    _build_page(
        page,
        "---\n"
        "title: No Provenance\n"
        "created: 2026-06-14\n"
        "updated: 2026-06-14\n"
        "status: active\n"
        "---\n\n"
        "## References\n",
    )

    assert not validate_sources(base_path=tmp_path)
    report = (tmp_path / "reports" / "validation-report.md").read_text()
    assert "missing_sections: ## Provenance Notes" in report


def test_validate_report_generation(tmp_path: Path) -> None:
    page = tmp_path / "wiki" / "Concepts" / "valid-report.md"
    _build_page(
        page,
        "---\n"
        "title: Report Page\n"
        "created: 2026-06-14\n"
        "updated: 2026-06-14\n"
        "status: active\n"
        "---\n\n"
        "## References\n\n"
        "## Provenance Notes\n",
    )

    assert validate_sources(base_path=tmp_path)
    assert (tmp_path / "reports" / "validation-report.md").exists()
