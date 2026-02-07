---
id: 007-T1
parent: adr-007
type: task
title: "旧自動化ワークフローの安全停止"
status: Draft
phase: infrastructure
roadmap: "docs/architecture/plans/20260204-adr007-refresh-plan.md"
depends_on: []
issue_id: # 【自動追記】手動で設定しないでください
---

# 旧自動化ワークフローの安全停止

## 1. 目的と背景 (Goal & Context)

- **As-is (現状)**: 旧仕様（ADR-003）に基づくディレクトリ構造を前提とした自動化ワークフローが稼働しており、ADR-007 への移行中に誤作動するリスクがある。
- **To-be (あるべき姿)**: 該当するワークフローのトリガーが無効化され、意図しないファイル移動や Issue 起票が完全に防止されている。
- **Design Evidence (設計の根拠)**: ADR-007 および刷新計画書。

## 2. 参照資料・入力ファイル (Input Context)

- [ ] `.github/workflows/auto-approve-docs.yml`
- [ ] `.github/workflows/auto-create-issues.yml`
- [ ] `.github/workflows/auto-phase-promotion.yml`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)

- [ ] **変更禁止**: `gemini-handler.yml`, `gemini-reviewer.yml`, `ci.yml` などの開発支援ワークフロー。
- [ ] **削除禁止**: ファイル自体は削除せず、コメントアウトに留める。

### 3.2. 実装手順 (Changes)

- [ ] **ファイル**: `.github/workflows/auto-*.yml` (3ファイル)
  - **処理内容**:
    - ファイル先頭に `# DISABLED for ADR-007 migration` を追記。
    - `on:` セクション全体をコメントアウト。

## 4. ブランチ戦略 (Branching Strategy)

- **ベースブランチ (Base Branch)**: main
- **作業ブランチ (Feature Branch)**: feature/task-007-T1-disable-old-workflows

## 5. 検証手順・完了条件 (Verification & DoD)

- [ ] **静的解析**: GitHub Actions の Syntax としてエラーになっていないこと。
- [ ] **挙動**: 該当ディレクトリへのファイル追加時にワークフローが起動しないこと。

## 6. 成果物 (Deliverables)

- `.github/workflows/auto-approve-docs.yml`
- `.github/workflows/auto-create-issues.yml`
- `.github/workflows/auto-phase-promotion.yml`
