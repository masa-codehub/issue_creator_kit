# Reconnaissance Report: CLI Integration with Scanner Foundation (ADR-008)

## 1. 調査の目的 (Purpose)
ADR-008 に基づく Scanner Foundation の CLI への統合（Task-008-05）に向け、現状の `cli.py` および関連する仕様・設計ドキュメントの状態を把握し、詳細仕様策定のインプットとする。

## 2. 調査結果 (Findings)

### 2.1. 既存の CLI 実装 (`src/issue_creator_kit/cli.py`)
- **現状のコマンド**: `init`, `process-diff`, `process-merge`, `run-workflow`, `approve`, `approve-all` が実装されている。
- **依存 UseCase**: `IssueCreationUseCase`, `ApprovalUseCase`, `RoadmapSyncUseCase`, `WorkflowUseCase` に依存している。
- **問題点**: これらは ADR-003/007 に基づく Git 差分ベースのロジックであり、ADR-008 で非推奨（Deprecate）とされている。

### 2.2. 新しいドメインサービスの状態
- **FileSystemScanner**: `src/issue_creator_kit/domain/services/scanner.py` (Planned/Implemented in Task-03)
- **GraphBuilder**: `src/issue_creator_kit/domain/services/builder.py` (Planned/Implemented in Task-04)
- **Visualizer**: `src/issue_creator_kit/domain/services/visualizer.py` (Planned/Implemented in Task-04)
- **仕様**: `docs/specs/logic/scanner_logic.md` および `docs/specs/logic/graph_and_validators.md` に定義済み。

### 2.3. アーキテクチャ設計 (`docs/architecture/arch-structure-008-scanner.md`)
- **CLI の役割**: `cli.py` は `FileSystemScanner` および `Visualizer` を直接呼び出す構造。
- **プロセルフロー**: 
    1. `CLI` -> `FileSystemScanner.scan()` -> `GraphBuilder.build_graph()`
    2. `visualize` コマンドの場合はさらに `Visualizer.to_mermaid()` を呼び出す。

### 2.4. 仕様策定計画 (`docs/specs/plans/adr-008-automation-cleanup/definitions.md`)
- **用語定義**: `Physical State Scanner`, `Domain Guardrails`, `DAG Visualization` が定義されている。
- **依存関係**: `Graph --> CLI` となっており、CLI 統合はグラフ構築ロジックの完成後に実施される。

## 3. 証拠 (Evidence)
- `src/issue_creator_kit/cli.py`: 旧 UseCase への依存を確認。
- `docs/specs/logic/scanner_logic.md`: 新しい走査ロジックの仕様を確認。
- `docs/specs/logic/graph_and_validators.md`: グラフ構築と可視化の仕様を確認。
- `docs/architecture/arch-structure-008-scanner.md`: CLI と各コンポーネントの依存関係図を確認。

## 4. 懸念点・未解決事項 (Concerns/Issues)
- **既存コマンドの扱い**: `process-diff` 等の旧コマンドを完全に削除するのか、共存させるのか。ADR-008 は "Deprecates" としているが、移行期間が必要か。
- **依存性注入**: `ScannerService` (あるいは `FileSystemScanner`) のインスタンス化に必要な引数（`root_path` 等）を CLI がどのように管理・提供するか。
