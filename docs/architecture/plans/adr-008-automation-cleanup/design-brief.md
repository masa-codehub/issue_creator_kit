# 設計指針 (Design Brief) - ADR-008: Cleanup & Scanner Foundation

## 1. 作成する成果物 (Target Artifacts)

- **種類:** Architecture Plan (Task Slicing)
- **出力ファイル名:** `docs/architecture/plans/adr-008-automation-cleanup/arch-to-spec.md`
- **SSOT参照:** `reqs/design/_approved/adr-008-automation-cleanup.md`

## 2. 解決すべき課題と方針 (Strategic Intent)

- **課題 (Problem):** ADR-007 移行期の自動化負債（停止中のワークフロー、複雑な同期ロジック、不安定な `diff-tree` 検知）が、開発サイクルの停滞と不確実性を招いている。
- **採用された方針 (Decision):** 「引き算」による徹底的なクリーンアップと、物理状態（ファイル配置）を正とする堅牢なスキャナー基盤の構築。
- **主な理由 (Rationale):** 複雑な自動リカバリよりも「単純さ」と「Fail-fast」を優先し、将来のイベント駆動リレー（ADR-009〜012）のための安全な土台を作るため。

## 3. ドキュメントに含めるべき内容 (Content Requirements)

### 3.1. 削除・アーカイブ対象 (Cleanup Scope)

- **Code:**
  - `.github/workflows/auto-approve-docs.yml` の物理削除。
  - `issue-kit` 内の `WorkflowUseCase`, `ApprovalUseCase` および関連 CLI コマンド (`run-workflow`, `approve`, `process-merge`) の削除。
  - Markdown ファイルへの Issue 番号書き戻しロジック (`RoadmapSyncUseCase` 等) の削除。
- **Documentation (Architecture):**
  - `arch-behavior-003-autopr.md` (Archive)
  - `arch-behavior-003-creation.md` (Archive)
  - `arch-state-003-task-lifecycle.md` (Archive)
  - `arch-structure-003-vqueue.md` (Archive)
  - _Note: Move all obsolete files to `docs/architecture/archive/` for historical preservation._

### 3.2. スキャナー基盤の設計 (Scanner Foundation)

- **Documentation Update:**
  - `arch-state-007-lifecycle.md`: "Physical State" ライフサイクル（ファイル配置に基づく状態遷移）への更新。
  - `arch-structure-008-scanner.md` (New): Scanner Component の構造と DAG 可視化の設計を記述。
  - `arch-structure-issue-kit.md`: UseCase 削除と Scanner 導入の反映。
- **System Logic:**
  - **物理走査ロジック**: `reqs/tasks/` および `reqs/design/_approved/` を走査し、`_archive/` に存在しないファイルを「未処理」として検出するアルゴリズム。
  - **検証モード**: `process-diff` コマンドに `--dry-run` オプションを追加し、起票予定リストと検出された依存関係を表示する仕様。
  - **可視化**: `visualize` コマンドを追加し、現在のディレクトリ状態から DAG (Mermaid) を生成する仕様。

### 3.3. ドメイン層の強化 (Domain Guardrails)

- **Documentation Update:**
  - `arch-structure-007-metadata.md`: Pydantic Validator による不変条件（ID形式、循環参照禁止）の記述追加。
- **System Logic:**
  - **Pydantic モデル**: `id` 形式 (ADRは `adr-\d{3}-.*`、タスクは `task-\d{3}-\d{2,}`), `depends_on` の整合性（自己参照、循環参照禁止）を検証するバリデーターの実装方針。
  - **共通化**: CLI と将来の Actions で同じバリデーションロジックを利用するための設計。

## 4. 制約と評価基準 (Constraints & Evaluation)

- **技術的制約:** `git mv` の原子性を前提とするが、失敗時は二重起票を許容する（Fail-fast）。
- **受容するリスク:** 自動承認機能の廃止による手動運用のコスト増（ただしこれは ADR-008 の意図的な決定である）。
- **完了条件 (Definition of Done):**
  - `issue-kit` から不要なコードが一掃されていること。
  - `process-diff --dry-run` が正確に未処理ファイルをリストアップできること。
  - Pydantic モデルによるバリデーションが単体テストで保証されていること。
  - アーキテクチャ図が現状（ADR-008）と完全に整合していること。

## 5. 推奨される次のアクション (Next Actions)

- **推奨スキル:** `planning-architecture` (Task Slicing の作成)
