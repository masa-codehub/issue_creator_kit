# Issue Creator Kit

Issue Creator Kit (ICK) is a Markdown-driven automation tool for managing GitHub Issues and tasks directly from your design documents and ADRs. By synchronizing your documentation with GitHub, ICK ensures that your project's implementation stays perfectly aligned with its architectural decisions.

## 1. About

ICK bridges the gap between design and execution. It scans your documentation for metadata, builds a task dependency graph, and automates the lifecycle of GitHub Issues.

### Key Features

- **Markdown-Driven**: Your documentation is the Single Source of Truth (SSOT).
- **Dependency Management**: Automatically handles task ordering and prerequisites.
- **Pre-commit Validation**: Catch syntax errors and circular dependencies before they hit your repo.
- **GitHub Actions Integration**: Seamlessly syncs issues on every push.
- **Dynamic Role Dispatching**: Assigns the right agent to the right task based on PR labels.

---

## 2. Getting Started

### 2.1. Prerequisites

- Python 3.13+
- Git

### 2.2. Installation

Install the package via pip:

```bash
pip install issue-creator-kit
```

### 2.3. Project Initialization (`ick init`)

To set up a new project with the recommended directory structure and configuration templates:

```bash
ick init
```

This command creates the following structure:

- `reqs/`: Root directory for ADRs and task definitions.
- `docs/`: System context and detailed specifications.
- `.github/issue-kit-config.json`: Default configuration for roles and labels.

---

## 3. Usage

### `ick process`

Scans documents and creates/updates GitHub Issues.

```bash
# Dry-run: Preview changes
ick process --root reqs/ --dry-run

# Execute: Create issues on GitHub
ick process --root reqs/ --execute
```

### `ick check`

Statically validates task files for ID consistency and circular dependencies.

```bash
ick check --root reqs/
```

### `ick relay`

Manually triggers descendant tasks for a specific closed issue.

```bash
ick relay --issue-no <ISSUE_NUMBER> --execute
```

### `ick dispatch`

Determines the appropriate agent role based on PR labels.

```bash
ick dispatch --labels "arch,gemini"
```

---

## 4. CI/CD Integration

### 4.1. Pre-commit Hook

Add ICK to your `.pre-commit-config.yaml` to ensure documentation quality:

```yaml
repos:
  - repo: https://github.com/masa-codehub/issue_creator_kit
    rev: v0.1.0 # Use the latest version
    hooks:
      - id: ick-check
      - id: ick-visualize
      - id: ick-sync-relay
```

#### Note for Private Repositories

If the `issue_creator_kit` repository is **Private**, your local Git environment must be authenticated to allow `pre-commit` to clone it.

- **Local Development**: Ensure you have SSH keys registered with GitHub or are logged in via the [GitHub CLI (`gh auth login`)](https://cli.github.com/).
- **CI/CD**: When running `pre-commit` in a CI environment (like GitHub Actions), you may need to use a Personal Access Token (PAT) with `repo` scope or ensure the environment has the necessary SSH keys to access the ICK repository.

### 4.2. GitHub Actions (Reusable Workflow)

Integrate ICK into your CI pipeline using our reusable workflow.
Create `.github/workflows/task-automation.yml`:

```yaml
name: Task Automation

on:
  push:
    branches: [main]

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  automation:
    uses: masa-codehub/issue_creator_kit/.github/workflows/task-automation.yml@main
    with:
      root: "reqs"
      execute: ${{ github.event_name == 'push' && github.ref == 'refs/heads/main' }}
    secrets:
      gh_token: ${{ secrets.GITHUB_TOKEN }}
```

---

## 5. Configuration

Configure roles and labels in `.github/issue-kit-config.json`:

```json
{
  "roles": [
    { "name": "SYSTEM_ARCHITECT", "labels": ["arch", "gemini:arch"] },
    { "name": "TECHNICAL_DESIGNER", "labels": ["spec", "gemini:spec"] },
    { "name": "BACKENDCODER", "labels": ["tdd", "gemini:tdd"] }
  ],
  "default_role": "BACKENDCODER"
}
```
