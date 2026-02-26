class DomainError(Exception):
    """Base class for domain errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ValidationError(DomainError):
    """Raised when metadata validation fails."""

    def __init__(self, message: str, field: str | None = None):
        super().__init__(message)
        self.field = field


class SecurityValidationError(DomainError):
    """Raised when path validation fails against security constraints."""

    pass


class InfrastructureError(RuntimeError):
    """Base class for infrastructure errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class GitHubAPIError(InfrastructureError):
    """Raised when GitHub API call fails."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class GitHubRateLimitError(GitHubAPIError):
    """Raised when GitHub API rate limit is exceeded."""

    pass


class GitOperationError(InfrastructureError):
    """Raised when Git command fails."""

    pass


class FileSystemError(InfrastructureError):
    """Raised when file system operation fails."""

    pass


class GraphError(DomainError):
    """Raised when dependency graph operations or validation fail."""

    def __init__(self, message: str, code: str | None = None):
        super().__init__(message)
        self.code = code


class CircularDependencyError(GraphError):
    """Raised when a circular dependency is detected in the graph."""

    pass


class DependencyResolutionError(DomainError):
    """Raised when a task ID in depends_on cannot be resolved."""

    pass


class MetadataSerializationError(DomainError):
    """Raised when metadata JSON serialization fails."""

    pass


class MetadataNotFoundError(DomainError):
    """Raised when metadata tag is not found in the issue body."""

    pass


class MetadataParseError(DomainError):
    """Raised when metadata JSON parsing fails."""

    pass


class MetadataValidationError(ValidationError):
    """Raised when metadata validation fails against Task model."""

    pass
