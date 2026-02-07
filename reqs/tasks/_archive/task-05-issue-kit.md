---
id: task-008-05
parent: adr-008
type: task
title: "Refactor Issue Kit Architecture Diagram"
status: Draft
phase: architecture
labels:
  - "gemini:arch"
  - "P2"
  - "SYSTEM_ARCHITECT"
roadmap: "docs/architecture/plans/adr-008-automation-cleanup/design-brief.md"
depends_on: ["task-008-04"]
issue_id:
---

# Refactor Issue Kit Architecture Diagram

## 1. 目的と背景 (Goal & Context)

- **As-is (現状)**: `arch-structure-issue-kit.md` に削除予定の `WorkflowUseCase` 等が含まれている。
- **To-be (あるべき姿)**: 不要なコンポーネントが削除され、新設される `ScannerService` が組み込まれた最新の構造図になっている。
- **Design Evidence (設計の根拠)**: ADR-008 "Cleanup Scope".

## 2. 参照資料・入力ファイル (Input Context)

- [ ] `docs/architecture/arch-structure-issue-kit.md` (編集対象)
- [ ] `docs/architecture/arch-structure-008-scanner.md` (参照: 新コンポーネント)

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 実装手順 (Changes)

- [ ] **ファイル**: `docs/architecture/arch-structure-issue-kit.md`
  - **削除**: `WorkflowUseCase`, `ApprovalUseCase`, `RoadmapSyncUseCase` を図と記述から削除。
  - **追加**: `ScannerService` (Domain Service) を追加。
  - **更新**: CLI コマンドの依存関係を更新（`run-workflow` 削除, `visualize` 追加）。

## 4. ブランチ戦略 (Branching Strategy)

- **ベースブランチ (Base Branch)**: feature/arch-update-adr008
- **作業ブランチ (Feature Branch)**: feature/task-008-05-issue-kit

## 5. 検証手順・完了条件 (Verification & DoD)

- [ ] **整合性**: `design-brief.md` の削除対象リストと一致していること。
