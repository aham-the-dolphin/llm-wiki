# Architecture

The `llm-wiki` architecture separates source content, generated wiki pages, validation rules, and reporting into distinct layers.

## Sources

Raw input documents are stored under `sources/` and `examples/`. These markdown files are the deterministic inputs that the system ingests to produce structured wiki pages.

## Wiki

Generated wiki content is stored in `wiki/`, with dedicated subdirectories for:

- `Concepts`
- `Technologies`
- `Organizations`
- `Architectures`
- `Relationships`

This directory structure supports modular content growth and future graph-based linking.

## Schema

Each wiki page follows a consistent schema with YAML frontmatter and required content sections. The frontmatter includes:

- `title`
- `created`
- `updated`
- `status`

Required structural sections include:

- `## References`
- `## Provenance Notes`

This schema ensures pages remain machine-readable and verifiable.

## Provenance

Provenance is derived from both metadata and page content. The system captures lineage through page headers, references, and provenance notes, then generates structured provenance reports.

## Future LLM Integration

The current architecture is intentionally deterministic to establish a stable foundation. Future phases will enable:

- LLM synthesis of richer wiki narratives
- knowledge graph generation from wiki link structure
- multi-agent maintenance and content validation
