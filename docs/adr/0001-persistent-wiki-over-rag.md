# ADR 0001: Persistent Wiki over RAG

## Context

A persistent, deterministic wiki provides a stable knowledge base, while retrieval-augmented generation (RAG) is better suited for transient query-time synthesis.

## Decision

We will build a persistent wiki as the primary knowledge store and reserve RAG for future content synthesis and query serving.

## Consequences

- wiki pages are first-class artifacts that can be validated and audited
- deterministic ingestion ensures reproducibility
- future LLM layers can consume the wiki without relying on live RAG generation
