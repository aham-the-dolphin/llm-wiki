from pathlib import Path

from llm_wiki.init import initialize_project


def test_init_creates_directories_and_templates(tmp_path: Path) -> None:
    initialize_project(tmp_path)

    expected_dirs = [
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

    for directory in expected_dirs:
        assert (tmp_path / directory).exists()
        assert (tmp_path / directory).is_dir()

    expected_templates = [
        "templates/concept-page.md",
        "templates/technology-page.md",
        "templates/entity-page.md",
        "templates/organization-page.md",
        "templates/architecture-page.md",
    ]

    for template in expected_templates:
        assert (tmp_path / template).exists()
        assert (tmp_path / template).is_file()

    assert (tmp_path / "examples/source-doc.md").exists()
    assert (tmp_path / "examples/source-doc.md").is_file()


def test_init_is_idempotent(tmp_path: Path) -> None:
    initialize_project(tmp_path)
    first_contents = {p.relative_to(tmp_path): p.read_text() for p in tmp_path.rglob("*") if p.is_file()}

    initialize_project(tmp_path)
    second_contents = {p.relative_to(tmp_path): p.read_text() for p in tmp_path.rglob("*") if p.is_file()}

    assert first_contents == second_contents
