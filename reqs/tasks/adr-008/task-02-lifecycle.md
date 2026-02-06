---
id: 008-02
parent: adr-008
type: task
title: "Update Architecture Lifecycle to Physical State"
status: Draft
phase: architecture
labels:
  - "gemini:arch"
  - "P1"
  - "SYSTEM_ARCHITECT"
roadmap: "docs/architecture/plans/adr-008-automation-cleanup/design-brief.md"
depends_on: ["008-01"]
issue_id:
---
# Update Architecture Lifecycle to Physical State

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: `arch-state-007-lifecycle.md` がまだ古い自動化ロジックや未定義の状態を含んでいる可能性がある。
- **To-be (あるべき姿)**: ライフサイクル定義が「物理ディレクトリ（Inbox, Approved, Archive）」と「手動承認」のみに基づく単純なものに更新されている。
- **Design Evidence (設計の根拠)**: ADR-008 "Scanner Foundation".

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/architecture/plans/adr-008-automation-cleanup/definitions.md` (Physical State Scanner)
- [ ] `docs/architecture/arch-state-007-lifecycle.md` (編集対象)

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 実装手順 (Changes)
- [ ] **ファイル**: `docs/architecture/arch-state-007-lifecycle.md`
    - **状態定義の更新**: State を `Draft (Inbox)`, `Approved`, `Done (Archive)` の3つに整理。
    - **遷移の更新**: Transition Trigger を「Manual PR Merge」や「Task Completion」に限定。Auto-script による遷移を削除。
    - **図の更新**: Mermaid State Diagram を更新。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: feature/arch-update-adr008
- **作業ブランチ (Feature Branch)**: feature/task-008-02-lifecycle

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **整合性**: 定義された状態遷移が `definitions.md` の "Manual Approval Flow" と一致していること。
