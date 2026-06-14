from typer.testing import CliRunner

from llm_wiki.cli import app


runner = CliRunner()


def test_help_shows_commands() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "init" in result.stdout
    assert "ingest" in result.stdout
    assert "validate" in result.stdout
    assert "check-links" in result.stdout
    assert "provenance-report" in result.stdout
