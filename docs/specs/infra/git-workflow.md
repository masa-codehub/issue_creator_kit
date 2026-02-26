# Git Workflow (Auto-Commit) Specification

## 1. Overview

- **Responsibility**: GitHub Actions ワークフロー実行によるファイルシステム上の変更（アーカイブ移動等）を検知し、自動的にコミット・プッシュを行うことでリポジトリの整合性を保つインフラ定義。
- **Collaborators**: `.github/workflows/task-automation.yml`.

## 2. Data Structures (Models)

### 2.1. Change Detection State

- `changes_detected`: `true` | `false` (GitHub Actions Output).

## 3. Interfaces (API/Methods)

### 3.1. Change Detection Logic

`git status --porcelain reqs/` を使用して、ワークフロー内での物理移動を検知する。

### 3.2. Automated Commit

- **Actor**: `masa-codehub`
- **Message**: `chore: archive processed tasks [skip ci]`
- **Scope**: `reqs/` ディレクトリ配下。

## 4. Logic & Algorithms

### 4.1. Loop Prevention

1. `github.actor != 'github-actions[bot]'` 条件による再実行防止。
2. `[skip ci]` をコミットメッセージに含めることによるワークフロー連鎖の遮断。

### 4.2. PR Creation (Optional)

大量の変更が発生した場合や直接プッシュが制限されている場合、`gh pr create` を用いて PR を作成する。

## 5. Traceability

- **Merged Files**:
  - `adr-011-workflow-commit.md` (Legacy)
  - `adr-011-workflow-commit-audit.md` (Legacy)
- **Handover Constraints**:
  - N/A
