# Reconnaissance Report - Issue #308 (Architecture Refactoring)

## 1. 調査対象 (Scope)
- **対象ファイル:** `docs/architecture/arch-structure-issue-kit.md`
- **参照ファイル:** `docs/architecture/arch-structure-008-scanner.md`
- **目的:** ADR-008に基づき、`arch-structure-issue-kit.md` を最新化する。

## 2. 収集された事実 (Gathered Facts)

### 2.1 Gitの状態
- **現在のブランチ:** `feature/task-008-05-issue-kit`
- **ステータス:** `docs/architecture/arch-structure-issue-kit.md` が「修正済み (modified)」としてワークツリーに存在する。

### 2.2 `docs/architecture/arch-structure-issue-kit.md` の現状 (ワークツリー)
- **図 (Mermaid):**
    - `WorkflowUseCase`, `ApprovalUseCase` は既に削除されている。
    - `Scanner Service` (SVC_SCAN) が既に追加されている。
    - 依存関係は `CLI --> SVC_SCAN` となっている。
- **構成要素の定義:**
    - `Scanner Service` が定義されており、`visualize` を統括する旨が記載されている。
    - `Workflow / Approval UseCase` のセクションは既に削除されている（代わりに `Scanner Service` がある）。

### 2.3 `docs/architecture/arch-structure-008-scanner.md` との比較
- `arch-structure-008-scanner.md` では以下の詳細コンポーネントが定義されている：
    - `FileSystemScanner`, `TaskParser`, `GraphBuilder`, `Visualizer`
- 現在の `arch-structure-issue-kit.md` では、これらは `Scanner Service` という単一コンポーネントとして抽象化されている。

### 2.4 未完了/要確認事項
- **コマンド明示:** CLIの説明において `run-workflow` の削除と `visualize` の追加が明示的ではない。
- **サブコンポーネント:** `Scanner Service` の詳細として `FileSystemScanner` 等を記述に含めるべきか。

## 3. 証拠 (Evidence)
- `cat docs/architecture/arch-structure-issue-kit.md` の実行結果（ワークツリー上の最新）。
- `git status` の結果。
