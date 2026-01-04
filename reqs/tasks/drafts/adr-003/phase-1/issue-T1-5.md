---
title: "制御用メタデータスキーマ確定とテンプレート更新"
labels:
  - "task"
  - "P1"
  - "TECHNICAL_DESIGNER"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T1-5"
depends_on: ["issue-T1-3.md"]
next_phase_path: ""
status: "Draft"
---
# 制御用メタデータスキーマ確定とテンプレート更新

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T1-5

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: Issue テンプレート (`issue-draft.md`) に、フェーズ連鎖に必要な `next_phase_path` などのフィールドが正式に定義されていない（現状は仮定義）。
- **To-be (あるべき姿)**: Frontmatter スキーマが確定し、テンプレートファイルが更新され、バリデーションルールが明確になっている。
- **Design Evidence (設計の根拠)**: ADR-003 第 3 項「自己推進型ワークフロー」

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/tasks/template/issue-draft.md`
- [ ] `reqs/design/_inbox/design-003-logic.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **変更禁止**: 既存の必須フィールド（`title`, `labels` 等）を削除しない。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `reqs/tasks/template/issue-draft.md`
    - **処理内容**:
        - `next_phase_path`: 任意項目として追加。ディレクトリパス形式のバリデーションルールをコメント追記。
        - `roadmap`: 必須項目として強調。
        - `task_id`: 必須項目として強調。
- [ ] **ファイル**: `docs/specs/metadata-logic-spec.md` (もしあれば更新、なければ新規作成)
    - メタデータの仕様を記述。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-1-foundation`
- **作業ブランチ (Feature Branch)**: `feature/T1-5-schema-update`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: テンプレートファイルが更新されていること。
- [ ] **ファイル状態**: `reqs/tasks/template/issue-draft.md` に `next_phase_path` が含まれていること。

## 6. 成果物 (Deliverables)
- テンプレート: `reqs/tasks/template/issue-draft.md`
- 仕様書: `docs/specs/metadata-logic-spec.md`
