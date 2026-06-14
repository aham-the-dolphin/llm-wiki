from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class WikiPage(BaseModel):
    title: str = Field(..., description="Page title")
    source: str = Field(..., description="Source file path")
    destination: str = Field(..., description="Generated wiki page path")
    metadata: dict[str, Any] = Field(default_factory=dict)


class LinkCheckResult(BaseModel):
    source: str
    passed: bool
    message: str
