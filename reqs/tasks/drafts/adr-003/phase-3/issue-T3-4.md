---
title: "プロジェクト完了監査とアーカイブ"
labels:
  - "task"
  - "P1"
  - "SYSTEM_ARCHITECT"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T3-4"
depends_on: ["issue-T3-3.md"]
next_phase_path: ""
status: "Draft"
---
# プロジェクト完了監査とアーカイブ

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T3-4

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: Phase 3 (Cleanup/Docs) の成果が `feature/phase-3-foundation` に集約されている。
- **To-be (あるべき姿)**: プロジェクト全体の成果物が監査され、ADR-003 の目的（仮想キュー・自己推進）が完全に達成されていることが確認された上で、ロードマップがアーカイブされる。
- **Design Evidence (設計の根拠)**: ADR-003, SYSTEM_ARCHITECT Audit Protocol

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/roadmap/active/roadmap-adr003-task-lifecycle.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **監査基準**: 旧システム（物理キュー等）の遺物が完全に除去されていない場合、完了としてはいけない。

### 3.2. 実装手順 (Changes)
- [ ] **プロジェクト完了監査 (Final Audit)**:
    - **クリーンアップ確認**: `reqs/tasks/_queue` などの廃止フォルダが完全に消滅しているか。
    - **ドキュメント整合性**: システムコンテキスト、開発ガイド、ADR の記述に矛盾がないか。
    - **機能検証**: 新しい起票フロー（仮想キュー）が正常に機能することを最終確認する。
- [ ] **レポート作成**:
    - 最終監査レポートを Pull Request の Body に記載する。
- [ ] **アーカイブ操作**:
    - `reqs/roadmap/active/roadmap-adr003-task-lifecycle.md` を `reqs/roadmap/archive/` へ移動。
    - ファイル内の Status を `Completed` に更新。
- [ ] **承認要請 (PR作成)**:
    - `feature/phase-3-foundation` から `main` へのプルリクエストを作成し、レビューを依頼する。
    - **注意**: マージは行わない。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- [ ] **移動**: `reqs/roadmap/active/roadmap-adr003-task-lifecycle.md` -> `reqs/roadmap/archive/`

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `main` (PRのターゲット)
- **作業ブランチ (Feature Branch)**: `feature/phase-3-foundation`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: `main` への Pull Request が作成され、詳細な監査レポートが記載されていること。
- [ ] **観測される挙動**: 自動テスト（CI）がパスしていること。

## 6. 成果物 (Deliverables)
- 最終監査レポート付きの Pull Request
- アーカイブされたロードマップ
- クリーンアップされた `main` ブランチ