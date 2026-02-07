---
id: task-008-07
parent: adr-008
type: task
title: "[Arch Fix] Update arch-structure-issue-kit.md & Metadata Invariants"
status: Issued
phase: architecture
labels:
  - "gemini:arch"
  - "P1"
  - "SYSTEM_ARCHITECT"
roadmap: "docs/architecture/plans/adr-008-automation-cleanup/design-brief.md"
depends_on: []
issue_id: 315
---

# [Arch Fix] Update arch-structure-issue-kit.md & Metadata Invariants

## 1. 目的と背景 (Goal & Context)

- **As-is (現状)**:
  - `docs/architecture/arch-structure-issue-kit.md` が削除済みの `WorkflowUseCase` 等を記述しており、新設された Scanner 基盤を反映していない。
  - `docs/architecture/arch-structure-007-metadata.md` に ID形式や依存関係（循環参照禁止）に関するバリデーションルール（Invariant）が記述されておらず、ライフサイクルドキュメントに分散している。
- **To-be (あるべき姿)**:
  - `issue-kit` の構造図が Scanner Architecture を正しく反映している。
  - `metadata` 定義書にデータ構造の制約（Invariant）が集約されている。
- **Design Evidence (設計の根拠)**:
  - `docs/architecture/plans/adr-008-automation-cleanup/reviews/integration-audit.md` (Audit Report)
  - `docs/architecture/arch-structure-008-scanner.md` (Scanner SSOT)

## 2. 参照資料・入力ファイル (Input Context)

- [ ] `docs/architecture/arch-structure-issue-kit.md`
- [ ] `docs/architecture/arch-structure-008-scanner.md`
- [ ] `docs/architecture/arch-structure-007-metadata.md`
- [ ] `docs/architecture/arch-state-007-lifecycle.md` (現状のInvariant記述元)

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)

- [ ] **変更禁止**: `docs/architecture/arch-structure-008-scanner.md` (これは正しい定義なので変更しない)
- [ ] **スコープ外**: 実装コードの修正（ドキュメント修正のみ）

### 3.2. 実装手順 (Changes)

#### 3.2.1. Update Issue Kit Structure

- [ ] **ファイル**: `docs/architecture/arch-structure-issue-kit.md`
  - **削除**: `WorkflowUseCase`, `ApprovalUseCase` のセクションと図中のノード。
  - **追加**: `Scanner Foundation` (FileSystemScanner, TaskParser, GraphBuilder) の概要と `arch-structure-008-scanner.md` への参照。
  - **修正**: コンポーネント図を更新し、`CLI -> Scanner -> Parser/Builder` のフローを反映。

#### 3.2.2. Add Metadata Invariants

- [ ] **ファイル**: `docs/architecture/arch-structure-007-metadata.md`
  - **追加**: `## Invariants (Validation Rules)` セクションを追加。
  - **記述**:
    - **ID Format**: `adr-\d{3}-.*` / `task-\d{3}-\d{2,}`
    - **Dependency**: 存在するIDのみ指定可能、自己参照禁止、循環参照禁止。
  - **参照**: `arch-state-007-lifecycle.md` からの転記・集約を行う（元のドキュメントからは削除せず、参照関係を整理してもよい）。

## 4. ブランチ戦略 (Branching Strategy)

- **ベースブランチ (Base Branch)**: main (または feature/arch-update-adr008)
- **作業ブランチ (Feature Branch)**: feature/task-008-07-arch-fix

## 5. 検証手順・完了条件 (Verification & DoD)

- [ ] **整合性**: `arch-structure-issue-kit.md` の記述が `arch-structure-008-scanner.md` と矛盾していないこと。
- [ ] **網羅性**: `arch-structure-007-metadata.md` を見れば、実装すべきバリデーションルールが全て把握できること。
- [ ] **監査パス**: `auditing-architecture` (または `ssot`) の観点で、SSOT間の循環や矛盾がないこと。

## 6. 成果物 (Deliverables)

- `docs/architecture/arch-structure-issue-kit.md`
- `docs/architecture/arch-structure-007-metadata.md`
