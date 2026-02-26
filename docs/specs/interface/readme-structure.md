# [Spec] Documentation (README.md) Structure

## 概要

本仕様書は、外部プロジェクトの管理者が本ツールキット（Issue Creator Kit）を円滑に導入・運用できるように、公式ドキュメントである `README.md` の網羅的な章構成と、記述すべき具体的な内容を定義する。

Markdown 駆動の Issue 自動化（Markdown-driven Issue Automation）というコンセプトを明確に伝え、最小限の手順で CI/CD 連携を完了させるための「実行可能なガイド」としての役割を果たす。

## 関連ドキュメント

- Common Definitions: `reqs/context/specs/adr-014-modular-reusability/definitions.md`
- Distribution Spec: `docs/specs/distribution.md`
- Reusable Workflow Spec: `docs/specs/interface/reusable-workflows.md`
- Dynamic Dispatcher Spec: `docs/specs/logic/dynamic-dispatch.md`

## 章構成の定義 (Table of Contents)

### 1. About

- **コンセプト**: Markdown-driven Issue Automation.
- **解決する課題**:
  - Issue とコード（設計ドキュメント）の乖離。
  - 手動での Issue 作成・更新に伴うヒューマンエラー。
  - 依存関係のある複雑なタスク管理の自動化。
- **特徴**:
  - Pydantic による厳密なメタデータバリデーション。
  - `pre-commit` によるローカル検証。
  - GitHub Actions によるリモート同期。
  - PR ラベルに基づいた動的なエージェントロール割り当て。

### 2. Getting Started

#### 2.1. Prerequisites

- Python 3.13+
- Git

#### 2.2. Installation

```bash
pip install issue-creator-kit
```

#### 2.3. Project Initialization (`ick init`)

リポジトリを本ツールキット対応に初期化するコマンド。

- **Behavior**:
  - プロジェクトテンプレート（`src/issue_creator_kit/assets/project_template/` 配下）のファイル・ディレクトリを、現在のディレクトリ直下に再帰的にコピーする。
  - テンプレートに含まれる `.github/issue-kit-config.json` のひな形や `reqs/` ディレクトリ、`.pre-commit-config.yaml` などが一括で配置される。
- **Usage**:
  ```bash
  ick init [-f|--force]
  ```

### 3. Usage (Main Commands)

#### 3.1. `ick process`

ドキュメントをスキャンし、Issue の作成・更新を行う。

```bash
ick process --root reqs/ --execute
```

#### 3.2. `ick check`

ドキュメントの構文やメタデータの整合性を検証する（Dry-run 相当）。

```bash
ick check --root reqs/
```

#### 3.3. `ick relay`

指定した Issue の後続タスクのステータス更新やエージェントの活性化を行う。

```bash
ick relay --issue-no 123 --execute
```

#### 3.4. `ick dispatch`

PR ラベルと設定ファイルを照合し、実行すべきエージェントロール名を標準出力に返す。

```bash
ick dispatch --labels "arch,gemini"
```

### 4. CI/CD Integration (Core Value)

#### 4.1. Pre-commit Hook

ローカルでのコミット前に自動検証を行うための設定。
`.pre-commit-config.yaml` に以下を追記：

```yaml
repos:
  - repo: https://github.com/masa-codehub/issue_creator_kit
    rev: v1.0.0 # 適切なバージョンを指定
    hooks:
      - id: ick-check
      - id: ick-visualize
      - id: ick-sync-relay
```

#### 4.2. GitHub Actions (Reusable Workflows)

PR 同期や自動化をリモートで実行するための設定。
`.github/workflows/task-automation.yml`（注：呼び出し先は `workflow_call` に対応している必要がある）：

```yaml
jobs:
  automation:
    uses: masa-codehub/issue_creator_kit/.github/workflows/task-automation.yml@v1.0.0
    with:
      root: "reqs"
      execute: ${{ github.event_name == 'push' && github.ref == 'refs/heads/main' }}
    secrets:
      gh_token: ${{ secrets.GITHUB_TOKEN }}
```

### 5. Configuration (`.github/issue-kit-config.json`)

設定ファイルのスキーマと記述例。

```json
{
  "roles": [
    { "name": "TECHNICAL_DESIGNER", "labels": ["spec", "gemini:spec"] },
    { "name": "SYSTEM_ARCHITECT", "labels": ["arch", "gemini:arch"] }
  ],
  "default_role": "BACKENDCODER"
}
```

## 補足・制約事項

- **GitHub Token**: GitHub Actions で使用する `GITHUB_TOKEN` には、`contents: write`, `issues: write`, `pull-requests: write` の権限が必要である。
- **Path Validation**: ワークフローの `root` パスには親ディレクトリ参照（`..`）を含めることはできない。
- **Fail-fast**: 設定ファイルに不備がある場合、ツールは即座にエラーを返して停止する。
