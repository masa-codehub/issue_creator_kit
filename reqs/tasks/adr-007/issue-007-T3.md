---
id: 007-T3
parent: adr-007
type: task
title: "旧アーキテクチャドキュメントの非推奨化"
status: Draft
phase: architecture
roadmap: "docs/architecture/plans/20260204-adr007-refresh-plan.md"
depends_on: ["007-T2"]
issue_id: # 【自動追記】手動で設定しないでください
---
# 旧アーキテクチャドキュメントの非推奨化

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: ADR-003 ベースの設計図が有効なドキュメントとして残っており、誤解を招く可能性がある。
- **To-be (あるべき姿)**: 旧ドキュメントに「非推奨」の警告が明記され、最新の ADR-007 および新設計図への誘導が行われている。
- **Design Evidence (設計の根拠)**: ADR-007

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/architecture/arch-behavior-003-autopr.md`
- [ ] `docs/architecture/arch-behavior-003-creation.md`
- [ ] `docs/architecture/arch-state-003-task-lifecycle.md`
- [ ] `docs/architecture/arch-structure-003-vqueue.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **削除禁止**: このタスクでは削除せず、警告の追記のみとする（実装完了後に削除）。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `docs/architecture/*-003-*.md`
    - **処理内容**: ファイル冒頭に以下の警告メッセージを挿入。
      > **DEPRECATED: This document is based on ADR-003 and has been superseded by the new architecture defined in ADR-007.**
      > Please refer to the new architecture documents, such as `arch-structure-007-metadata.md` and `arch-state-007-lifecycle.md`.

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: main
- **作業ブランチ (Feature Branch)**: feature/task-007-T3-deprecate-old-docs

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **ファイル状態**: 全対象ファイルの冒頭に警告が正しく記載されていること。

## 6. 成果物 (Deliverables)
- 修正された4つの旧設計ドキュメント
