---
title: "統合検証（フェーズ 1→2 の自動リレー確認）"
labels:
  - "task"
  - "P1"
  - "SYSTEM_ARCHITECT"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T2-6"
depends_on: ["issue-T2-5.md"]
next_phase_path: ""
status: "Draft"
---
# 統合検証（フェーズ 1→2 の自動リレー確認）

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T2-6

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 実装と設定が完了したが、実際の Git 操作を通じたエンドツーエンドの動作確認が未実施。
- **To-be (あるべき姿)**: ダミーのタスク移動や PR マージを行い、ログを確認して正常動作（起票、ロードマップ更新、Auto-PR）を検証する。
- **Design Evidence (設計の根拠)**: `test-criteria.md`

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/test-criteria.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **注意**: 本番のリポジトリを汚さないよう、ダミーファイルを使用し、検証後はクリーンアップする。

### 3.2. 実装手順 (Changes)
- [ ] **検証**:
    - `drafts/` にダミータスクを作成。
    - PR を作成し、マージ。
    - GitHub Actions のログを確認。
    - Issue が起票され、ロードマップが更新されたか確認。
    - 次のフェーズへの Auto-PR が作成されたか確認（もし該当トリガーがあれば）。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- [ ] **Cleanup**: 検証用ダミーファイルの削除。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-2-foundation`
- **作業ブランチ (Feature Branch)**: `feature/T2-6-e2e-verify`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: 全てのテストシナリオが Pass すること。

## 6. 成果物 (Deliverables)
- 検証ログ（Issueコメント等に残す）
