---
depends_on:
- issue-T4-1.md
issue: '#174'
labels:
- task
- P1
- TECHNICAL_DESIGNER
next_phase_path: ''
roadmap: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
status: Draft
task_id: T4-2
title: システムコンテキストと運用ガイドの最新化
---
# システムコンテキストと運用ガイドの最新化

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T4-2

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: ドキュメント（システムコンテキストやADR-001）が古い物理キュー方式を説明していたり、ステータスが不正確である。
- **To-be (あるべき姿)**: 新しい「仮想キュー」「Auto-PR」方式を反映し、ADR-001 も実装済みのロジック仕様として正しく定義されている。
- **Design Evidence (設計の根拠)**: ADR-003

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/system-context.md`
- [ ] `docs/guides/development-setup.md`
- [ ] `reqs/design/_approved/adr-001-issue-creation-logic.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] なし

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `docs/system-context.md`
    - **処理内容**: システムの仕組み説明を更新（Virtual Queue の詳細化、Physical Queue 廃止の明記）。
- [ ] **ファイル**: `docs/guides/development-setup.md`
    - **処理内容**: 開発者が Issue を起票する手順（Draft作成 → `archive/` への移動 PR 作成 → マージによる自動起票）を具体的に解説。
- [ ] **ファイル**: `reqs/design/_approved/adr-001-issue-creation-logic.md`
    - **処理内容**: ステータスを「承認済み/実装済み」に更新。「物理キュー」の記述を「仮想キュー（ADR-003参照）」に修正し、依存解決ロジックの SSOT として整備する。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-4-foundation`
- **作業ブランチ (Feature Branch)**: `feature/T4-2-docs-update`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: ドキュメントレビュー通過。

## 6. 成果物 (Deliverables)
- 更新されたドキュメント群
