# Infrastructure Container Components
extend infra {
    gh_adapter = component "GitHubAdapter" "Wrapper for GitHub REST API." "github_adapter.py" {
        tags "Layer:Infrastructure" "Type:Component"
    }
    fs_adapter = component "FileSystemAdapter" "Wrapper for physical file operations." "filesystem.py" {
        tags "Layer:Infrastructure" "Type:Component"
    }
}

# Implementation Relationships
gh_adapter -> interfaces "Implements"
fs_adapter -> interfaces "Implements"
