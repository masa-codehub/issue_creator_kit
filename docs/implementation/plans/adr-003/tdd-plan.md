# TDD Implementation Plan: ADR-003 Virtual Queue & Workflow

- **Spec Source**: `docs/specs/**/*.md`
- **Handover**: `docs/handovers/spec-to-tdd.md`
- **Target Feature**: Virtual Queue, Auto-PR, Roadmap Sync

## 1. Overview & Strategy
ADR-003 で定義された「自己推進型ワークフロー」を実現するため、厳密なレイヤー分離と依存性注入（DI）を用いた実装を行う。
テストファースト（Red-Green）を徹底し、特に「Fail-fast」な原子性を保証する。

### 1.1. Architecture Mapping
| Layer | Description | Path |
| :--- | :--- | :--- |
| **Domain** | `Document`, `Metadata` などのコアモデル。外部依存なし。 | `src/issue_creator_kit/domain/` |
| **UseCase** | `IssueCreation`, `WorkflowAutomation` などのビジネスロジック。 | `src/issue_creator_kit/usecase/` |
| **Infrastructure** | `GitAdapter`, `GitHubAdapter` などの外部連携。 | `src/issue_creator_kit/infrastructure/` |
| **Interface** | CLI エントリポイント。 | `src/issue_creator_kit/cli.py` |

### 1.2. Test Strategy
- **Unit Test (Domain/UseCase)**:
    - `unittest.mock` を使用し、Infrastructure を完全にモック化する。
    - ファイルシステムへのアクセスについては、`pathlib.Path` のモックを使用するか、`pyfakefs` の代わりに `MockAdapter` を使用することを推奨する。
- **Integration Test (Infrastructure)**:
    - 実際に一時ディレクトリ (`tempfile`) を作成し、Git コマンドやファイル操作が正しく動作するか検証する。
    - GitHub API は `responses` や `unittest.mock` でシミュレートする（実際の API は叩かない）。

## 2. Common Fixtures & Stubs
以下の共通テストリソースを `tests/conftest.py` または `tests/shared/` に定義する。

- **`mock_git_adapter`**: コミット、Diff取得、Branch作成をシミュレートするスタブ。
- **`mock_github_adapter`**: Issue検索、作成、PR作成をシミュレートするスタブ。
- **`sample_document`**: 正常なメタデータを持つ Markdown ドキュメントのファクトリ。

## 3. Implementation Tasks (Slicing)

### Phase 1: Core Domain (Value Objects & Logic)
- **T-1: Document & Metadata Model**
    - `docs/specs/data/document_model.md`
    - 正規化ロジック、日本語キー対応、ステータスバリデーションの実装。

### Phase 2: Infrastructure (Adapters)
- **T-2: Git & FileSystem Adapters**
    - `docs/specs/components/infra_adapters.md`
    - `get_added_files` (with `--no-renames`), `commit_changes` 等の実装。
- **T-3: GitHub Adapter**
    - `docs/specs/components/infra_adapters.md`
    - `find_or_create_issue`, `create_pull_request` 等の実装。

### Phase 3: UseCase (Business Logic)
- **T-4: Issue Creation Logic**
    - `docs/specs/logic/creation_logic.md`
    - 仮想キュー検知、Topological Sort、Fail-fast ループの実装。
- **T-5: Roadmap Sync Logic**
    - `docs/specs/logic/roadmap_sync_logic.md`
    - リンク置換と Issue 番号追記ロジックの実装。
- **T-6: Phase Promotion Logic**
    - `docs/specs/logic/promotion_logic.md`
    - PR Body 解析、次フェーズ特定、Auto-PR 作成ロジックの実装。

### Phase 4: Interface & Integration
- **T-7: CLI Commands**
    - `docs/specs/api/cli_commands.md`
    - `process-diff`, `process-merge` コマンドの実装と例外ハンドリング。

## 4. Coding Standards (Strict)
- **Type Hints**: 全ての関数引数・戻り値に型ヒントを必須とする (`mypy --strict` 準拠)。
- **Docstrings**: Google Style で記述する。
- **Error Handling**: 独自例外 (`DomainError`, `InfrastructureError`) を定義し、生のエラーをラップして送出する。
