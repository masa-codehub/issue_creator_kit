import re
from datetime import date as date_type
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    Field,
    TypeAdapter,
    model_validator,
)

# --- Regex Definitions (Compiled for performance) ---

# TaskID: ^task-\d{3}-\d{2,}$ or legacy ^\d{3}-T\d+(-[A-Z0-9-]+)?$
TASK_ID_PATTERN = re.compile(r"^task-\d{3}-\d{2,}$")
LEGACY_TASK_ID_PATTERN = re.compile(r"^\d{3}-T\d+(-[A-Z0-9-]+)?$")

# ADRID: ^adr-\d{3}(?:-[a-z0-9-]+)?$ (Allows both full and minimal forms for flexibility)
ADR_ID_PATTERN = re.compile(r"^adr-\d{3}(?:-[a-z0-9-]+)?$")


# --- Constants ---

VALID_ROLES = {"arch", "spec", "tdd", "audit"}
VALID_PHASES = {"arch", "spec", "tdd", "audit", "plan", "impl"}
LEGACY_PHASES = {
    "domain",
    "infrastructure",
    "usecase",
    "interface",
    "cleanup",
    "test",
    "refactor",
    "architecture",
    "Specification",
    "Implementation",
    "infra",
    "Architecture",
}  # Add other legacy phases if needed


# --- ID Type Validators ---


def validate_adr_id(v: str) -> str:
    """Validate ADR ID format."""
    if not ADR_ID_PATTERN.match(v):
        raise ValueError(
            f"Invalid ADR ID format: {v}. Expected adr-XXX or adr-XXX-slug."
        )
    return v


def validate_task_id(v: str) -> str:
    """Validate Task ID format."""
    if not TASK_ID_PATTERN.match(v):
        raise ValueError(
            f"Invalid Task ID format: {v}. Expected task-XXX-NN (where NN is 2 or more digits)."
        )
    return v


def validate_any_task_id(v: str) -> str:
    """Validate Task ID format (including legacy)."""
    if not (TASK_ID_PATTERN.match(v) or LEGACY_TASK_ID_PATTERN.match(v)):
        raise ValueError(
            f"Invalid Task ID format: {v}. Expected task-XXX-NN (where NN is 2 or more digits) or legacy format."
        )
    return v


def validate_role_compatibility(v: str | None) -> str | None:
    """Validate role against new standards, allowing None for legacy."""
    if v is None:
        return None
    if v not in VALID_ROLES:
        raise ValueError(f"Invalid role: {v}. Expected one of {VALID_ROLES}")
    return v


def validate_phase_compatibility(v: str | None) -> str | None:
    """Validate phase against new standards + legacy allowlist."""
    if v is None:
        return None
    if v in VALID_PHASES:
        return v
    if v in LEGACY_PHASES:
        return v
    raise ValueError(
        f"Invalid phase: {v}. Expected one of {VALID_PHASES} or legacy {LEGACY_PHASES}"
    )


def coerce_date_to_str(v: Any) -> Any:
    """Coerce datetime.date objects to ISO format strings."""
    if type(v) is date_type:
        return v.isoformat()
    return v


# --- Value Objects ---

ADRID = Annotated[str, AfterValidator(validate_adr_id)]
TaskID = Annotated[str, AfterValidator(validate_task_id)]
LegacyTaskID = Annotated[str, Field(pattern=LEGACY_TASK_ID_PATTERN.pattern)]
AnyTaskID = Annotated[str, AfterValidator(validate_any_task_id)]

DateStr = Annotated[str | None, BeforeValidator(coerce_date_to_str)]
RoleStr = Annotated[str | None, AfterValidator(validate_role_compatibility)]
PhaseStr = Annotated[str | None, AfterValidator(validate_phase_compatibility)]


# --- Models ---


class ADR(BaseModel):
    """ADR (Architecture Decision Record) metadata model."""

    id: ADRID
    type: Literal["adr"]
    title: str
    status: Literal["Draft", "Approved", "Postponed", "Superseded", "Implemented"]
    date: DateStr = None
    depends_on: list[TaskID | ADRID | LegacyTaskID] = Field(default_factory=list)
    path: Path | None = Field(default=None, exclude=True)
    content: str = ""


class Task(BaseModel):
    """Task (Issue Draft) metadata model."""

    id: AnyTaskID  # Allow legacy for reading
    type: Literal["task", "integration"]
    title: str
    status: Literal["Draft", "Ready", "Issued", "Completed", "Cancelled"]
    parent: ADRID
    # role and phase are relaxed to `str` to support legacy archives.
    # Stricter validation (New + Legacy allowlist) is handled by custom validators.
    role: RoleStr = None
    phase: PhaseStr = None
    depends_on: list[AnyTaskID] = Field(default_factory=list)
    labels: list[str] = Field(default_factory=list)
    issue_id: int | None = None
    path: Path | None = Field(default=None, exclude=True)
    content: str = ""

    @model_validator(mode="after")
    def validate_issue_id_requirements(self) -> "Task":
        """Ensure issue_id is present for Issued/Completed tasks."""
        if self.status in ("Issued", "Completed") and self.issue_id is None:
            raise ValueError(f"issue_id is required when status is {self.status}")
        return self

    @property
    def adr_number(self) -> str | None:
        """Extract the 3-digit ADR number from the parent ID (e.g., adr-010 -> 010)."""
        match = re.search(r"adr-(\d{3})", self.parent)
        return match.group(1) if match else None


# --- Union & Discrimination ---

# Universal document type for Scanner Foundation.
# Use 'type' as discriminator for robust validation.
DocumentType = Annotated[Task | ADR, Field(discriminator="type")]

# Helper adapter for DocumentType
Document: TypeAdapter[DocumentType] = TypeAdapter(DocumentType)
