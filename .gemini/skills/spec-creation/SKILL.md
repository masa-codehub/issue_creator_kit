---
name: spec-creation
description: Orchestrator skill for creating detailed technical specifications (API, DB, Component). Sequentially executes planning, drafting, refactoring, and audit to transform abstract requirements into actionable specs.
---

# Specification Creation Orchestration

ADRやIssueで定義された「要求」を、開発者が実装可能な「詳細仕様（Specs）」に変換するプロセスを統括するスキル。
`task-management` を利用し、計画・策定・洗練・監査のループを確実に実行する。

## 役割 (Role)
**Spec Designer (詳細設計者)**
抽象的な決定事項（What）を、具体的かつ厳密な実装指示（How）に翻訳する。

## 前提 (Prerequisites)
- 解決すべき課題（Issue）や方針（ADR）が明確であること。

## 手順 (Procedure)

### 1. 計画フェーズ (State 1: Planning)
*   **Action:**
    1.  `activate_skill{name: "task-management"}` を起動。
    2.  `activate_skill{name: "spec-planning"}` を呼び出し、作成すべき仕様のスコープと要件を定義する。
    3.  `activate_skill{name: "todo-management"}` を使い、仕様策定のためのTodoリスト（`.gemini/todo.md`）を作成する。

### 2. 実行フェーズ (State 2: Execution)
*   **Action:**
    *   `task-management` のサイクルに従い、Todoを順次消化する。
    *   **各タスク（仕様書の作成）ごとに以下のサイクルを回す:**
        1.  **Targeting (Red):** 要件（Issue/ADR）を確認し、まだ仕様が存在しない（または不足している）ことを認識する。
        2.  **Drafting (Green):** `activate_skill{name: "spec-drafting"}` を呼び出し、テンプレートを用いて仕様を記述する。
        3.  **Refining (Refactor):** `activate_skill{name: "spec-refactoring"}` を呼び出し、曖昧さの排除や整合性の確認を行う。
        4.  **Git:** `activate_skill{name: "github-commit"}` を行い、仕様書をコミットする。

### 3. 完了フェーズ (State 3: Closing)
*   **Action:**
    *   **Audit:** `activate_skill{name: "spec-audit"}` を呼び出し、実装可能性とSSOT整合性を最終チェックする。
    *   **PR:** `activate_skill{name: "github-pull-request"}` で変更を提出する。
    *   **Retrospective:** `activate_skill{name: "retrospective"}` でプロセスを振り返る。

## 完了条件 (Definition of Done)
*   監査リスト（Audit Checklist）が全てPassしていること。
*   作成された仕様書を含むPRが作成されていること。
