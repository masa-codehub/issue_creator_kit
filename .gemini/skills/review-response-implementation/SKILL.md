---
name: review-response-implementation
description: Orchestrates the Code Review Response process (Analysis -> Fix -> Reply/Close). Manages the workflow by invoking specialized sub-skills like review-analysis, tdd-refactoring, and tdd-audit.
---

# Review Response Implementation (Orchestrator)

このスキルは、コードレビュー指摘への対応を、感情論ではなく技術的プロセスとして確実に完遂するためのワークフローを提供します。

## 役割定義 (Role Definition)
あなたは **Review Responder** です。`task-management` のステートマシンを駆動させ、適切なタイミングで `review-analysis`, `tdd-refactoring`, `tdd-audit` を指揮します。

## 前提 (Prerequisites)
- `task-management` スキルが有効であること。
- `review-analysis`, `tdd-refactoring`, `tdd-audit`, `pull_request_review_write` が利用可能であること。

## 手順 (Procedure)

### 1. State: Planning (分析・計画)
- **Action:**
  - `task-management` スキルをアクティベートする。
    `activate_skill{name: "task-management"}`
  - `task-management` の `State 1` に入り、`review-analysis` スキルをアクティベートする。
    `activate_skill{name: "review-analysis"}`
  - 指摘を分析し、`.gemini/todo.md` に対応計画を作成する。

### 2. State: Execution (修正・回答準備)
- **Action:**
  - `task-management` の `State 2` に入り、`.gemini/todo.md` のタスクを順次実行する。
  - **Code Fixes (Accept):** `tdd-refactoring` スキルをアクティベートし、安全に修正を行う。
    - ※ 修正は「指摘されたスコープ」に限定する（Boy Scout Ruleは適用可だが、無関係な拡張は禁止）。
    `activate_skill{name: "tdd-refactoring"}`
  - **Replies (Explain/Discuss):** `pull_request_review_write` や `add_comment_to_pending_review` を用いて回答を下書きする。

### 3. State: Closing (完了・提出)
- **Action:**
  - `task-management` の `State 3` に入り、`tdd-audit` スキルをアクティベートする。
    `activate_skill{name: "tdd-audit"}`
  - **品質監査:** テストパス、Linterパスを確認。
  - **対応漏れ監査:** 全ての指摘に対して修正または回答が行われたか確認する。
  - **提出:** 修正をPushし、レビュー回答をSubmitする。
  - 振り返りを行い、タスクをクローズする。

## 完了条件 (Definition of Done)
- 全ての指摘に対して「修正」または「回答」が完了していること。
- 修正後のコードがCI（テスト・Lint）を通過していること。
- PRが更新され、レビュアーに再通知（Re-request review等）が行われていること。
