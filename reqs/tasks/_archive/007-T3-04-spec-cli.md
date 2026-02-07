---
id: 007-T3-04
parent: adr-007
parent_issue: #279
type: task
phase: spec
status: Issued
issue_id: 286
date: 2026-02-05
depends_on: ["007-T3-01"]
title: "Update CLI Interface Specification"
labels:
  - "gemini:spec"
  - "P1" # Priority: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
  - "BACKENDCODER" # Role: BACKENDCODER, SYSTEM_ARCHITECT, etc.
---

# Task: Update CLI Interface Specification

## 1. Goal & Context

### Goal

`issue-kit` CLI のコマンド引数と挙動定義を更新し、新しいディレクトリ構造（`reqs/tasks/<ADR-ID>/`）に対応させる。

### As-is

`cli_commands.md` はデフォルト値として `reqs/tasks/archive/` 等の古いパス構造を使用している。また、コマンド体系が物理移動前提になっている可能性がある。

### To-be

`cli_commands.md` が更新され、メタデータ駆動に対応したコマンド引数（例: `--adr-id` フィルタ等）やデフォルトパスが定義されている。

### Design Evidence

- `docs/specs/plans/adr-007-metadata-driven-lifecycle/definitions.md`

## 2. Input Context

- `docs/specs/api/cli_commands.md` (編集対象)

## 3. Implementation Steps & Constraints

### Negative Constraints

- 既存のサブコマンド（`run-workflow` 等）を削除せず、後方互換性（または移行期間）を考慮すること。

### Changes

1. **Command Arguments Update:**
   - `run-workflow` (または `process-diff` 相当) において、対象ディレクトリを走査する際のデフォルトパスを `reqs/tasks/` ルートに変更（再帰探索）。
   - 必要に応じて `--adr-id` フィルタオプションを追加。
2. **Path Configuration:**
   - デフォルトのアーカイブ先を `reqs/tasks/_archive/` に変更。
3. **Help Message Definition:**
   - 各コマンドのヘルプメッセージ定義を更新。

## 4. Branching Strategy

- **Base Branch:** `feature/spec-update-adr007`
- **Feature Branch:** `spec/task-007-T3-04-cli`

## 5. Verification & DoD

### 5.1. Verification Criteria

- [ ] **Path Defaults:** デフォルトパスが ADR-007 準拠になっていること。
- [ ] **TDD Criteria:** `test_cli.py` で検証すべき「引数解析」「デフォルト値適用」のケースが記述されていること。

### 5.2. Automated Tests

- `grep "reqs/tasks/_archive" docs/specs/api/cli_commands.md`
