---
id: 007-T2
parent: adr-007
type: task
title: "新アーキテクチャ図（Structure/State）の起草"
status: Draft
phase: architecture
roadmap: "docs/architecture/plans/20260204-adr007-refresh-plan.md"
depends_on: ["007-T1"]
issue_id: # 【自動追記】手動で設定しないでください
---

# 新アーキテクチャ図（Structure/State）の起草

## 1. 目的と背景 (Goal & Context)

- **As-is (現状)**: アーキテクチャ図が ADR-003 の物理構造（nested folders）に基づいた記述になっている。
- **To-be (あるべき姿)**: ADR-007 の「フラット構造」「メタデータ駆動」「Invisible SSOT」を反映した新設計図が整備されている。
- **Design Evidence (設計の根拠)**: ADR-007

## 2. 参照資料・入力ファイル (Input Context)

- [ ] `docs/architecture/arch-structure-003-vqueue.md` (旧版)
- [ ] `docs/architecture/arch-state-003-task-lifecycle.md` (旧版)

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)

- [ ] **既存破壊の禁止**: 既存の `*-003-*` ファイルを直接編集せず、新規ファイルを作成する。

### 3.2. 実装手順 (Changes)

- [ ] **ファイル**: `docs/architecture/arch-structure-007-metadata.md`
  - **処理内容**: フラットなディレクトリ配置と、メタデータによる論理的依存関係（DAG）を Mermaid C4 Container 図等で再定義。
- [ ] **ファイル**: `docs/architecture/arch-state-007-lifecycle.md`
  - **処理内容**: ADR-007 で定義されたステータス遷移（Draft/Approved/Archived）と自動移動ルールを Mermaid StateDiagram で定義。

## 4. ブランチ戦略 (Branching Strategy)

- **ベースブランチ (Base Branch)**: main
- **作業ブランチ (Feature Branch)**: feature/task-007-T2-draft-new-architecture

## 5. 検証手順・完了条件 (Verification & DoD)

- [ ] **静的解析**: Mermaid 記法が正しくレンダリングされること。
- [ ] **整合性**: ADR-007 の記述と完全に一致していること。

## 6. 成果物 (Deliverables)

- `docs/architecture/arch-structure-007-metadata.md`
- `docs/architecture/arch-state-007-lifecycle.md`
