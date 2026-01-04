---
title: "git diff によるマージ差分特定ロジックの実機検証"
labels:
  - "task"
  - "P1"
  - "BACKENDCODER"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T1-2"
depends_on: ["issue-T1-1.md"]
next_phase_path: ""
status: "Draft"
---
# git diff によるマージ差分特定ロジックの実機検証

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T1-2

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 仮想キュー方式において、`archive/` フォルダへ移動されたファイルのみを正確に検知する方法が未検証である。
- **To-be (あるべき姿)**: `git diff` コマンドを用いて、マージコミットにおいて「追加または移動されたファイル」のみを特定する具体的なコマンドオプションが確定している。
- **Design Evidence (設計の根拠)**: ADR-003 第 1.B 項「仮想キュー」および「実行トリガー」

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/design/_approved/adr-003-task-and-roadmap-lifecycle.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **変更禁止**: プロダクションコードへの組み込みは行わない（Spikeであるため）。

### 3.2. 実装手順 (Changes)
- [ ] **調査・検証**:
    - ローカルでダミーのマージコミットを作成し、`git diff` の挙動を確認する。
    - 特に `rename` (移動) と `add` (新規) の扱いの違い、および `--name-only`, `--diff-filter` オプションの有効性を検証する。
- [ ] **成果物作成**:
    - 検証結果をまとめたマークダウンファイルを作成する。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-1-foundation`
- **作業ブランチ (Feature Branch)**: `feature/T1-2-diff-spike`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: 作成された調査メモに、期待通り動作する `git` コマンドラインが記載されていること。
- [ ] **ファイル状態**: `docs/spikes/git-diff-logic.md` (仮) が作成されていること。

## 6. 成果物 (Deliverables)
- 調査メモ: `docs/spikes/git-diff-logic.md` (パスは任意)
