# llm-wiki

`llm-wiki` is a deterministic markdown ingestion and validation toolkit for building a structured knowledge base from source documents. It converts markdown sources into wiki pages, validates schema and link integrity, and generates provenance and link reports.

## Purpose

The project is designed to:

- ingest markdown source files into a consistent wiki structure
- enforce metadata and section requirements
- verify internal wiki link integrity
- capture provenance and traceability of content
- provide a foundation for future LLM-powered synthesis and graph generation

## Installation

Install dependencies and sync the environment using `uv`:

```bash
uv sync
```

Run the CLI help:

```bash
uv run llm-wiki --help
```

## Quick Start

Initialize a project scaffold:

```bash
uv run llm-wiki init
```

Ingest a source document:

```bash
uv run llm-wiki ingest examples/source-doc.md
```

Validate the generated wiki pages:

```bash
uv run llm-wiki validate
```

Check internal wiki links:

```bash
uv run llm-wiki check-links
```

Generate provenance summaries:

```bash
uv run llm-wiki provenance-report
```

## Architecture

The repository is organized into:

- `sources/` – raw source markdown documents
- `wiki/` – generated structured wiki pages
- `templates/` – page templates for consistent content creation
- `reports/` – validation, link, and provenance reports
- `src/llm_wiki/` – application logic and CLI implementation

For a detailed architecture overview, see `docs/architecture.md`.

## CLI Commands

- `llm-wiki init` – create required project directories and templates
- `llm-wiki ingest <file>` – deterministically ingest markdown into `wiki/Concepts/`
- `llm-wiki validate` – validate metadata, sections, and page schema
- `llm-wiki check-links` – detect broken links, orphans, and circular references
- `llm-wiki provenance-report` – generate provenance completeness reporting

## Development

Run tests and static analysis:

```bash
uv run pytest
uv run ruff check .
uv run mypy src
```

### Contributing

Contributions should follow the governance practices in `docs/governance.md`.
