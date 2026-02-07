# Reconnaissance Report (Scouting Facts) - Issue #315

## 1. 調査の目的 (Objective)

- ADR-008 (Cleanup & Scanner Foundation) に基づき、`arch-structure-issue-kit.md` の更新内容と `arch-structure-007-metadata.md` に追加すべき Invariants を特定する。

## 2. 収集された事実 (Facts & Evidence)

### 2.1. 現状のドキュメント状態 (Current State)

- **`docs/architecture/arch-structure-issue-kit.md`**:
  - `WorkflowUseCase`, `ApprovalUseCase` が存在し、Clean Architecture Lite の図解に含まれている。
  - `Scanner` 関連の記述が全くない。
- **`docs/architecture/arch-structure-007-metadata.md`**:
  - メタデータ駆動型ライフサイクルのコンテナ図や DAG の概念図はあるが、バリデーションルール（Invariants）のセクションが不足している。
- **`docs/architecture/arch-state-007-lifecycle.md`**:
  - `Invariants (不変条件)` セクションがあり、Unique ID, Strict Dependency, Atomic Issue Creation, Hierarchy Priority が記述されている。
- **`docs/architecture/arch-structure-008-scanner.md` (Reference)**:
  - `FileSystemScanner`, `TaskParser`, `GraphBuilder`, `Visualizer` のコンポーネント定義とシーケンス図が存在する。
  - `Quality Policy` に `Domain Guardrails` (ID形式, 依存性整合性) が記述されている。

### 2.2. ADR-008 による変更点 (ADR-008 Decisions)

- **削除**: `WorkflowUseCase`, `ApprovalUseCase`, `auto-approve-docs.yml` (自動承認・書き戻しロジックの廃止)。
- **追加**: `Scanner Foundation` (物理状態ベースのスキャナー)。
- **Invariant**: ID形式 (`adr-\d{3}-.*`, `task-\d{3}-\d{2,}`), 循環参照禁止, 自己参照禁止。

### 2.3. 設計の根拠 (Design Evidence)

- **`reqs/design/_approved/adr-008-automation-cleanup.md`**: 負債削除とスキャナー基盤構築を決定。
- **`docs/architecture/plans/adr-008-automation-cleanup/definitions.md`**: スキャナーの概念とディレクトリマッピングを定義。

## 3. 特定された乖離と課題 (Gaps & Issues)

- `arch-structure-issue-kit.md` が古いアーキテクチャ（ADR-003）のままであり、実装予定の `Scanner` 基盤が反映されていない。
- `arch-structure-007-metadata.md` に、実装時に守るべき具体的なバリデーションルール（Invariants）が集約されていない。

## 4. 依存関係の確認 (Dependencies)

- `arch-structure-issue-kit.md` の更新は `arch-structure-008-scanner.md` の定義に依存する。
- メタデータのバリデーションルールは `adr-008-automation-cleanup.md` および `definitions.md` に基づく。
