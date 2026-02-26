from pydantic import BaseModel, Field


class RenderedIssue(BaseModel):
    """Value object representing a task rendered for GitHub Issue."""

    title: str
    body: str
    labels: list[str] = Field(default_factory=list)
