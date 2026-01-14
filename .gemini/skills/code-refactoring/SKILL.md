---
name: code-refactoring
description: Orchestrates the entire Code Refactoring process (Planning -> Execution -> Closing). Manages the workflow by invoking specialized sub-skills like refactoring-planning, tdd-refactoring, and tdd-audit.
---

# Code Refactoring (Orchestrator)

このスキルは、大規模なリファクタリングタスクを、安全かつ確実に完遂するための構造化されたプロセスを提供します。

## 役割定義 (Role Definition)
あなたは **Refactoring Lead** です。`task-management` のステートマシンを駆動させ、適切なタイミングで `refactoring-planning`, `tdd-refactoring`, `tdd-audit` を指揮します。

## 前提 (Prerequisites)
- `task-management` スキルが有効であること。
- `refactoring-planning`, `tdd-refactoring`, `tdd-audit` スキルが定義されていること。

## 手順 (Procedure)

### 1. State: Planning (計画)
- **Action:**
  - `task-management` スキルをアクティベートする。
    `activate_skill{name: "task-management"}`
  - `task-management` の `State 1` に入り、`refactoring-planning` スキルをアクティベートする。
    `activate_skill{name: "refactoring-planning"}`
  - SMART目標を宣言し、`.gemini/todo.md` に「Refactoring Plan」に基づく実行計画を作成する。
  - ユーザーから Plan の承認を得る。

### 2. State: Execution (実行)
- **Action:**
  - `task-management` の `State 2` に入り、`.gemini/todo.md` のタスクを順次実行する。
  - **Refactoring Steps:** `tdd-refactoring` スキルをアクティベートし、品質改善サイクルを回す。
    `activate_skill{name: "tdd-refactoring"}`
  - **注意:** リファクタリング中は「機能追加」や「振る舞いの変更」を一切行わないこと。

### 3. State: Closing (完了・振り返り)
- **Action:**
  - `task-management` の `State 3` に入り、`tdd-audit` スキルをアクティベートする。
    `activate_skill{name: "tdd-audit"}`
  - 品質監査、PR作成、振り返り、報告を行い、タスクをクローズする。

## 完了条件 (Definition of Done)
- 全てのステートが正常に遷移し、PRがマージ可能な状態で作成されていること。
- プロジェクトの規約（_GEMINI.md）に定義された「プロジェクト進行フレームワーク」を完遂していること。
