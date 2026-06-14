from pathlib import Path

from llm_wiki.links import check_links


def _build_page(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_check_links_valid_links(tmp_path: Path) -> None:
    page_a = tmp_path / "wiki" / "Concepts" / "page-a.md"
    page_b = tmp_path / "wiki" / "Concepts" / "page-b.md"
    _build_page(page_a, "# Page A\n\n[[Page B]]\n")
    _build_page(page_b, "# Page B\n\n[[Page A]]\n")

    assert check_links(base_path=tmp_path)
    assert (tmp_path / "reports" / "link-report.md").exists()


def test_check_links_broken_link(tmp_path: Path) -> None:
    page_a = tmp_path / "wiki" / "Concepts" / "page-a.md"
    _build_page(page_a, "# Page A\n\n[[Missing Page]]\n")

    assert not check_links(base_path=tmp_path)
    report = (tmp_path / "reports" / "link-report.md").read_text()
    assert "broken_links" in report


def test_check_links_orphan_page(tmp_path: Path) -> None:
    page_a = tmp_path / "wiki" / "Concepts" / "page-a.md"
    page_b = tmp_path / "wiki" / "Concepts" / "page-b.md"
    _build_page(page_a, "# Page A\n\n[[Page B]]\n")
    _build_page(page_b, "# Page B\n\n")

    assert not check_links(base_path=tmp_path)
    report = (tmp_path / "reports" / "link-report.md").read_text()
    assert "orphan_pages" in report


def test_check_links_report_generation(tmp_path: Path) -> None:
    page_a = tmp_path / "wiki" / "Concepts" / "page-a.md"
    page_b = tmp_path / "wiki" / "Concepts" / "page-b.md"
    _build_page(page_a, "# Page A\n\n[[Page B]]\n")
    _build_page(page_b, "# Page B\n\n[[Page A]]\n")

    assert check_links(base_path=tmp_path)
    assert (tmp_path / "reports" / "link-report.md").exists()
