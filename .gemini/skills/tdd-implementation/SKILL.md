---
name: tdd-implementation
description: Orchestrates the entire TDD process (Planning -> Execution -> Closing). Manages the workflow by invoking specialized sub-skills like tdd-planning, tdd-cycle, and tdd-audit. Used for (1) implementing complex features requiring high reliability, (2) fixing critical bugs with regression testing, and (3) refactoring legacy code safely using test harnesses.
---

# TDD Implementation (Orchestrator)

このスキルは、複雑な実装タスクを TDD の原則に基づき、構造化されたプロセスで確実に完遂することを目的とします。

## 役割定義 (Role Definition)
あなたは **TDD Lead** です。`task-management` のステートマシンを駆動させ、適切なタイミングで `tdd-planning`, `tdd-cycle`, `tdd-audit` を指揮します。

## 前提 (Prerequisites)
- `task-management` スキルが有効であること。
- `tdd-planning`, `tdd-cycle`, `tdd-audit` スキルが定義されていること。

## 手順 (Procedure)

### 1. State: Planning (計画)
- **Action:**
  - `task-management` の `State 1` に入り、`tdd-planning` スキルをアクティベートする。
    `activate_skill{name: "tdd-planning"}`
  - SMART目標を宣言し、`.gemini/todo.md` に実行計画を作成する。
  - ユーザーから TDD Plan の承認を得る。

### 2. State: Execution (実行)
- **Action:**
  - `task-management` の `State 2` に入り、`tdd-cycle` スキルをアクティベートする。
    `activate_skill{name: "tdd-cycle"}`
  - 計画されたサイクル（Red-Green-Refactor）を全てのテストケースについて完了させる。

### 3. State: Closing (完了・振り返り)
- **Action:**
  - `task-management` の `State 3` に入り、`tdd-audit` スキルをアクティベートする。
    `activate_skill{name: "tdd-audit"}`
  - 品質監査、PR作成、振り返り、報告を行い、タスクをクローズする。

## 完了条件 (Definition of Done)
- 全てのステートが正常に遷移し、PRがマージ可能な状態で作成されていること。
- プロジェクトの規約（_GEMINI.md）に定義された「プロジェクト進行フレームワーク」を完遂していること。
