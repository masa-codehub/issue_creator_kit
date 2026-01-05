---
title: "統合検証（自動起票とフェーズ連鎖の動作実証）"
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
# 統合検証（自動起票とフェーズ連鎖の動作実証）

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T2-6

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 個別のコンポーネントは TDD で実装されたが、Git コマンドと GitHub Actions、GitHub API が連鎖した際の実機挙動が未検証。
- **To-be (あるべき姿)**: 模擬的なタスク移動 PR のマージを通じ、Issue 起票から Auto-PR までのサイクルが正常に完遂されることが証明されている。
- **Design Evidence (設計の根拠)**: `test-criteria.md` 第 5 項

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/test-criteria.md`
- [ ] `docs/spikes/git-diff-logic.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **注意**: 開発用メインリポジトリに大量のテスト Issue を作らないよう、必要最小限のダミーファイル（2〜3個）で検証すること。

### 3.2. 実装手順 (Changes)
- [ ] **実機検証**:
    - `drafts/` に検証用タスクを作成し、`next_phase_path` を設定。
    - PR を作成し、`main` へマージ。
    - **Actions ログ監視**: `git diff-tree` で正しくファイルが抽出されているか。
    - **GitHub 確認**: Issue が起票され、本文内のリンクが置換されているか。
    - **ロードマップ確認**: リンクが `archive` パスに自動更新されているか。
    - **Auto-PR 確認**: 次フェーズの PR が自動で Open されているか。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- [ ] **クリーンアップ**: 検証で作成されたダミータスクファイルの削除。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-2-foundation`
- **作業ブランチ (Feature Branch)**: `feature/task-T2-6-integration-verify`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: `test-criteria.md` に定義された全ての主要成功シナリオが実機で再現されること。

## 6. 成果物 (Deliverables)
- 検証ログ（PR コメントまたは活動報告に記載）