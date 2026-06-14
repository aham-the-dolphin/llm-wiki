import typer
from rich.console import Console

from . import __version__
from .ingest import ingest_file
from .init import initialize_project
from .links import check_links
from .provenance import provenance_report
from .validate import validate_sources

console = Console()
app = typer.Typer(help="llm-wiki CLI")


@app.command()
def init() -> None:
    """Initialize llm-wiki project structure."""
    initialize_project()


@app.command()
def ingest(file: str, force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing wiki page if present.")) -> None:
    """Ingest a markdown file into the wiki source set."""
    try:
        ingest_file(file, force=force)
    except FileExistsError as exc:
        console.print(f"[red]{exc}[/]")
        raise typer.Exit(code=1)


@app.command(name="validate")
def validate_command() -> None:
    """Validate the wiki sources."""
    validate_sources()


@app.command(name="check-links")
def check_links_command() -> None:
    """Check for broken wiki links."""
    check_links()


@app.command(name="provenance-report")
def provenance_report_command() -> None:
    """Generate provenance report."""
    provenance_report()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        console.print(f"[blue]llm-wiki v{__version__}[/]")
        console.print("Use --help to see available commands.")
