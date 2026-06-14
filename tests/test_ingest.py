from pathlib import Path

from llm_wiki.ingest import ingest_file


def test_ingest_file_extracts_h1_title(tmp_path: Path) -> None:
    target_dir = tmp_path / "wiki" / "Concepts"
    file_path = tmp_path / "example.md"
    file_path.write_text("# Example Title\n\n## Concepts\n\n### Details")

    result = ingest_file(str(file_path), dest_dir=target_dir)

    assert result.title == "Example Title"
    assert result.source == str(file_path)
    assert result.destination.endswith("example.md")
    assert result.metadata["headings"] == ["Concepts", "Details"]


def test_ingest_file_uses_filename_when_no_h1(tmp_path: Path) -> None:
    target_dir = tmp_path / "wiki" / "Concepts"
    file_path = tmp_path / "my-file.md"
    file_path.write_text("## First Heading\n\n### Subheading")

    result = ingest_file(str(file_path), dest_dir=target_dir)

    assert result.title == "My File"
    assert Path(result.destination).exists()
    assert "First Heading" in result.metadata["headings"]


def test_ingest_creates_wiki_page(tmp_path: Path) -> None:
    target_dir = tmp_path / "wiki" / "Concepts"
    file_path = tmp_path / "source-doc.md"
    file_path.write_text("# Sample\n\n## Key Concept")

    result = ingest_file(str(file_path), dest_dir=target_dir)

    page_path = Path(result.destination)
    assert page_path.exists()
    contents = page_path.read_text()
    assert "# Sample" in contents
    assert "## Key Concepts" in contents
    assert "- Key Concept" in contents
    assert "## Provenance Notes" in contents


def test_ingest_prevents_overwrite_by_default(tmp_path: Path) -> None:
    target_dir = tmp_path / "wiki" / "Concepts"
    file_path = tmp_path / "source-doc.md"
    file_path.write_text("# Sample\n")
    ingest_file(str(file_path), dest_dir=target_dir)

    try:
        ingest_file(str(file_path), dest_dir=target_dir)
    except FileExistsError as exc:
        assert "Destination already exists" in str(exc)
    else:
        assert False, "Expected FileExistsError"


def test_ingest_allows_force_overwrite(tmp_path: Path) -> None:
    target_dir = tmp_path / "wiki" / "Concepts"
    file_path = tmp_path / "source-doc.md"
    file_path.write_text("# Sample\n")
    ingest_file(str(file_path), dest_dir=target_dir)

    file_path.write_text("# Updated Sample\n")
    second = ingest_file(str(file_path), force=True, dest_dir=target_dir)

    assert second.title == "Updated Sample"
    assert Path(second.destination).read_text().startswith("---")
