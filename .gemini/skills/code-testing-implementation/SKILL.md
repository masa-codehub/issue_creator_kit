---
name: code-testing-implementation
description: Orchestrates the Testing Strategy & Implementation process (Planning -> Execution -> Closing). Manages the workflow by invoking specialized sub-skills like code-testing-planning, tdd-refactoring, and tdd-audit. Used for (1) adding missing coverage for legacy code, (2) reproducing reported bugs with regression tests (xfail), and (3) verifying edge cases or error handling for existing logic.
---

# Code Testing Implementation (Orchestrator)

このスキルは、既存コードに対するテスト追加を、体系的かつ高品質に行うためのワークフローを提供します。

## 役割定義 (Role Definition)
あなたは **Test Engineer** です。`task-management` のステートマシンを駆動させ、適切なタイミングで `code-testing-planning`, `tdd-refactoring`, `tdd-audit` を指揮します。

## 前提 (Prerequisites)
- `task-management` スキルが有効であること。
- `code-testing-planning`, `tdd-refactoring`, `tdd-audit` が利用可能であること。

## 手順 (Procedure)

### 1. State: Planning (計画)
- **Action:**
  - `task-management` スキルをアクティベートする。
    `activate_skill{name: "task-management"}`
  - `task-management` の `State 1` に入り、`code-testing-planning` スキルをアクティベートする。
    `activate_skill{name: "code-testing-planning"}`
  - テスト対象を分析し、`.gemini/todo.md` にテスト計画を作成する。

### 2. State: Execution (実装)
- **Action:**
  - `task-management` の `State 2` に入り、`.gemini/todo.md` のタスクを順次実行する。
  - **Test Implementation:**
    - テストコードを実装し、`pytest` で検証する。
    - **バグ発見時:** 実装コードは修正せず、`@pytest.mark.xfail` を付与してバグとして記録する（別途Issue化）。
  - **Test Refactoring:**
    - `tdd-refactoring` スキルをアクティベートし、**追加したテストコード自体の品質**（可読性、重複排除、Factory利用）を高める。
    - ※ プロダクションコードのリファクタリングはこのタスクのスコープ外とする（必要なら別タスク化）。
    `activate_skill{name: "tdd-refactoring"}`

### 3. State: Closing (完了・監査)
- **Action:**
  - `task-management` の `State 3` に入り、`tdd-audit` スキルをアクティベートする。
    `activate_skill{name: "tdd-audit"}`
  - **品質監査:** 全テストパス、Linterパスを確認。
  - **網羅性監査:** 計画したシナリオが全て実装されているか確認。
  - 振り返りを行い、タスクをクローズする。

## 完了条件 (Definition of Done)
- 計画された全てのテストケースが実装・実行されていること。
- バグが発見された場合、再現テスト（xfail）としてコード化されていること。
- PRが作成され、カバレッジへの影響が報告されていること。
