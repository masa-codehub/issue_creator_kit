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
