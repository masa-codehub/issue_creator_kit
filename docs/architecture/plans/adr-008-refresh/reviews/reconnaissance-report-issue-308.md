# Reconnaissance Report (Architecture Refactoring: Issue #308)

## 1. 調査対象 (Scope)

- **Target File:** `docs/architecture/arch-structure-issue-kit.md`
- **Reference Files:**
  - `docs/architecture/arch-structure-008-scanner.md`
  - `reqs/design/_approved/adr-008-automation-cleanup.md`
- **Goal:** ADR-008に基づき、`arch-structure-issue-kit.md` から廃止コンポーネントを削除し、新設されるScanner基盤を統合する。

## 2. 収集された事実 (Gathered Facts - Initial)

### 2.1 現状の構造 (`arch-structure-issue-kit.md` - Before)

- **UseCase Layer:** `WorkflowUseCase` (UC_WF), `ApprovalUseCase` (UC_APP) が存在。
- **CLI Layer:** `CLI Entrypoint` が上記UseCaseに依存。
- **Domain Layer:** `Document Entity` (DOM_DOC) が存在。
- **Infra Layer:** `GitHub Adapter`, `Git Adapter`, `File System Adapter` が存在。

### 2.2 変更要件 (Issue #308 & ADR-008)

- **削除対象:**
  - `WorkflowUseCase`, `ApprovalUseCase`, `RoadmapSyncUseCase` (図中および説明文から)。
- **追加対象:**
  - `ScannerService` (Domain Service)。
  - `Scanner Foundation` (ADR-008) で定義されたサブコンポーネント群 (`FileSystemScanner`, `TaskParser`, `GraphBuilder`, `Visualizer`) の概念的な統合。
- **CLIの更新:**
  - `run-workflow` コマンドの削除 (依存関係の解消)。
  - `visualize` コマンドの追加。

### 2.3 新コンポーネントの定義 (`arch-structure-008-scanner.md`)

- **FileSystemScanner:** `src/issue_creator_kit/domain/services/scanner.py` (Domain Service)
- **TaskParser:** `src/issue_creator_kit/domain/services/parser.py` (Domain Model/Entity logic)
- **GraphBuilder:** `src/issue_creator_kit/domain/services/builder.py` (Domain Service)
- **Visualizer:** `src/issue_creator_kit/domain/services/visualizer.py` (Domain Service)

## 3. 収集された事実 (Gathered Facts - Current Status)

### 3.1 `docs/architecture/arch-structure-issue-kit.md` の現状 (After Implementation)

- **図 (Mermaid):**
  - `WorkflowUseCase`, `ApprovalUseCase` は既に削除されている。
  - `Scanner Service` (SVC_SCAN) が既に追加されている。
  - 依存関係は `CLI --> SVC_SCAN` となっている。
- **構成要素の定義:**
  - `Scanner Service` が定義されており、`visualize` を統括する旨が記載されている。
  - `Workflow / Approval UseCase` のセクションは既に削除されている（代わりに `Scanner Service` がある）。

### 3.2 未完了/要確認事項

- **コマンド明示:** CLIの説明において `run-workflow` の削除と `visualize` の追加が明示的ではない。
- **サブコンポーネント:** `Scanner Service` の詳細として `FileSystemScanner` 等を記述に含めるべきか。

## 4. 懸念事項・矛盾点 (Concerns & Discrepancies)

- **レイヤー配置:** `arch-structure-008-scanner.md` では `FileSystemScanner` や `Visualizer` が Domain Layer に配置されているが、`arch-structure-issue-kit.md` の Clean Architecture Lite 構成にどう当てはめるべきか。
  - ADR-008では `FileSystemScanner` を `Use Cases / Domain Services` としており、Application Core 内での整理が必要。

## 5. エビデンス引用 (Evidence)

- **ADR-008 Decision 1:** "自動承認の廃止... `WorkflowUseCase`, `ApprovalUseCase` を完全に削除する。"
- **ADR-008 Decision 2:** "物理状態ベースのスキャナー基盤... `visualize` により、複雑な依存関係を Mermaid 形式で出力し..."
- **Issue #308 Steps:** "削除: `WorkflowUseCase`, `ApprovalUseCase`, `RoadmapSyncUseCase` を図と記述から削除。追加: `ScannerService` (Domain Service) を追加。"
