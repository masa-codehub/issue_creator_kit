# Specification Plan: Approval Flow (ADR-002)

- **Source Design**: [ADR-002: Document Approval Flow](../../../reqs/design/_archive/adr-002-document-approval-flow.md)
- **Architecture**: [Arch Behavior: Approval Flow](../../../docs/architecture/arch-behavior-approval-flow.md)
- **Target Audience**: Backend Implementers
- **Date**: 2026-01-20

## 1. Ubiquitous Language (Common Terms)

| Term | Definition | Code Mapping (Hint) |
| :--- | :--- | :--- |
| **Inbox** | 承認待ちの設計ドキュメントが配置されるディレクトリ。 | `path="reqs/design/_inbox"` |
| **Approved** | 承認済みドキュメントの保管場所。SSOTとして扱われる。 | `path="reqs/design/_approved"` |
| **Document** | マークダウンファイル全体を表す概念。メタデータと本文を持つ。 | `Domain.Document` |
| **Metadata** | ファイル先頭のYAMLフロントマター、またはそれに準ずるKey-Value記述。 | `Domain.Metadata` |
| **Tracking Issue** | ドキュメント承認に伴い自動起票されるGitHub Issue。 | `GitHubIssue` |
| **Archive (Directory)** | タスク（Issue）の完了後の保管場所。ADR-002の承認済みドキュメントとは区別される。 | `reqs/tasks/archive/` |

## 2. Specification Directory Structure

本機能の詳細仕様書は以下の構成で作成する。

- **Domain / Data Models**:
  - `docs/specs/data/document_model.md`: `Document`, `Metadata` クラスの定義と解析ロジック。
- **UseCase / Logic**:
  - `docs/specs/logic/approval_usecase.md`: 承認フローの全体制御、ロールバック、エラーハンドリング。
- **Infrastructure / Components**:
  - `docs/specs/components/infra_adapters.md`: `GitHubAdapter`, `GitAdapter`, `FileSystemAdapter` のインターフェースと挙動。
- **Interface / CLI**:
  - `docs/specs/api/cli_commands.md`: CLI引数、サブコマンド (`issue-kit run-workflow`) の定義。

## 3. Implementation Strategy (Slicing)

### Slice 1: Domain Models
- **Goal**: ドキュメントの読み込み、メタデータのパース/書き換えロジックの実装。
- **Verify**: ファイルIOを伴わない純粋なデータ操作としてテストできること。

### Slice 2: Infrastructure Adapters
- **Goal**: 外部システム（GitHub, Git, FileSystem）への副作用を伴う操作の実装。
- **Verify**: 各メソッドが期待通りに外部ライブラリを呼び出しているか（Mockを使用）。

### Slice 3: Approval UseCase
- **Goal**: ドメインとインフラを組み合わせてフロー全体（移動→起票→更新）を実現する。
- **Verify**: インフラをMock化し、ロールバックやエラー時の挙動を検証する。

### Slice 4: CLI Integration
- **Goal**: コマンドライン引数をパースし、UseCaseを実行するエントリポイント。
- **Verify**: シェルから `issue-kit run-workflow --help` を実行し、ヘルプが表示されることや、引数エラー時の挙動を確認する。

## 4. Common Technical Policies

### Error Codes
- `DOC_NOT_FOUND`: 対象ファイルが存在しない。
- `METADATA_INVALID`: 必須フィールド（`status`, `date` 等）が欠落している。
- `GITHUB_API_ERROR`: GitHub API呼び出し失敗。
- `GIT_OPERATION_ERROR`: Gitコマンド失敗。

### File Paths
- 常にプロジェクトルート (`/app`) からの相対パスとして扱う。
- パス操作には `pathlib.Path` を使用する。