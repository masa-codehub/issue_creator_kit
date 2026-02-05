---
id: 007-T3-03
parent: adr-007
parent_issue: #279
type: task
phase: spec
status: Draft
date: 2026-02-05
depends_on: ["007-T3-01"]
title: "Update Infrastructure Adapter Specifications"
labels:
  - "gemini:spec"
  - "P1" # Priority: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
  - "BACKENDCODER" # Role: BACKENDCODER, SYSTEM_ARCHITECT, etc.
---

# Task: Update Infrastructure Adapter Specifications

## 1. Goal & Context
### Goal
FileSystem (Atomic Move) および GitHub API (Issue/Status Sync) との連携インターフェース仕様を更新する。

### As-is
`infra_adapters.md` は古いディレクトリ構造（`archive/` フォルダ固定）に基づいたファイル操作仕様となっている。

### To-be
ADR-007 の「フラットなアーカイブ構造」と「`issue_id` の自動追記」に対応したアダプタのインターフェースが定義されている。

### Design Evidence
- `reqs/design/_approved/adr-007-metadata-driven-lifecycle.md`

## 2. Input Context
- `docs/specs/components/infra_adapters.md` (編集対象)

## 3. Implementation Steps & Constraints
### Changes
1. **FileSystem Adapter Spec:**
   - 物理移動（`reqs/tasks/<ADR-ID>/` -> `reqs/tasks/_archive/`）の原子性（Atomicity）確保のための手順。
   - `id` をキーとしたファイル検索ロジックの定義。
2. **GitHub Adapter Spec:**
   - メタデータを元にした Issue 起票パラメータのマッピング定義。
   - `issue_id` の抽出とメタデータへの書き戻し仕様。

## 4. Branching Strategy
- **Base Branch:** `feature/spec-update-adr007`
- **Feature Branch:** `spec/task-007-T3-03-infra`

## 5. Verification & DoD
- [ ] **Interface Check:** ファイル移動とIssue起票のインターフェースが定義されていること。
- [ ] **TDD Criteria:** `test_github_adapter.py` 等で検証すべき「APIエラー時のファイル移動抑止」ケースが記述されていること。
