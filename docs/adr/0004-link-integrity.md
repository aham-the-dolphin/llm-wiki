# ADR 0004: Link Integrity

## Context

Internal wiki links are essential for navigating the knowledge base and identifying relationships.

## Decision

The system will validate internal `[[Page Name]]` links, detect broken references, orphan pages, and simple circular references.

## Consequences

- link quality becomes part of the validation pipeline
- broken and orphaned content can be remediated quickly
- link graphs can support future knowledge discovery and graph generation
