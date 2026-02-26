from pydantic import BaseModel, Field


class RoleMapping(BaseModel):
    """Mapping between an agent role name and triggering labels.

    Attributes:
        name: The name of the agent role (e.g., "SYSTEM_ARCHITECT").
        labels: A list of GitHub labels that trigger this role (AND condition).
        context: Optional path to the prompt context file for this role/label combination.
    """

    name: str = Field(..., min_length=1)
    labels: list[str] = Field(..., min_length=1)
    context: str | None = None


class IssueKitConfig(BaseModel):
    """Root configuration model for Issue Creator Kit.

    Attributes:
        version: The configuration schema version.
        roles: A list of role-to-label mappings.
        triggers: Future extension for custom trigger definitions.
        default_role: Future reservation for a default role.
        trigger_label: The base label required to trigger Gemini workflows.
    """

    version: str = Field(default="1.0", pattern=r"^\d+\.\d+(\.\d+)?$")
    roles: list[RoleMapping] = Field(..., min_length=1)
    triggers: dict[str, list[str]] = Field(default_factory=dict)
    default_role: str | None = None
    trigger_label: str = Field(default="gemini")

    def find_role(self, labels: list[str]) -> RoleMapping | None:
        """Find the first matching role mapping for the given labels.

        Matches only if ALL labels specified in the config are present in the provided labels.

        Args:
            labels: A list of labels from a PR or issue.

        Returns:
            The matched RoleMapping object, or None if no match.
        """
        labels_set = set(labels)
        for role in self.roles:
            if all(label in labels_set for label in role.labels):
                return role
        return None
