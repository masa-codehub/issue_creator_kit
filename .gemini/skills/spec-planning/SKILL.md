---
name: spec-planning
description: Analyzes requirements (Issue/ADR) and existing specs to formulate a concrete plan for specification creation. Defines the "Requirements" for the specs.
---

# Specification Planning

ADRやIssue（Why/What）を分析し、どのような「仕様書（Specs）」を作成すべきか（Howの定義場所）を計画するスキル。

## 役割 (Role)
**Spec Planner (仕様計画者)**
「何を実装するか」ではなく「どのドキュメントに何を定義すれば実装できるか」を設計する。

## 手順 (Procedure)

### 1. 要件の特定 (Context Analysis)
- **Action:**
  - `activate_skill{name: "active-reconnaissance"}` を使い、IssueのAcceptance Criteriaや関連ADRを読み込む。
  - **Question:** 「この機能を実装するために、開発者は何を知る必要があるか？」
    - APIのI/F定義？
    - DBのスキーマ？
    - 複雑な計算ロジック？

### 2. 既存資産の調査 (Asset Reconnaissance)
- **Action:**
  - `glob("docs/specs/**/*.md")` 等で既存の仕様書を確認する。
  - 継承すべき共通仕様（エラーハンドリング、認証フロー）や、修正すべき既存仕様を特定する。

### 3. Spec Plan の策定
- **Action:**
  - 必要な仕様書の種類を選定し、Todoを作成する。
  - **Doc Type Selection:**
    - **API Spec:** 外部/内部インターフェース定義（OpenAPI等）。
    - **Data Spec:** DBスキーマ、データ構造定義。
    - **Logic Spec:** 複雑なアルゴリズム、ステートマシン詳細。

### 4. Todo分解 (Breakdown)
- **Action:**
  - `activate_skill{name: "todo-management"}` を使用し、`.gemini/todo.md` を作成する。
  - **Context (Red) の記述ルール:** 「ADR-XXXに基づき、YYYのAPI仕様が必要である」と記述する。

## アウトプット形式 (.gemini/todo.md)

```markdown
# Goal: [Issueに基づく仕様策定目標]

## Tasks
- [ ] **Step 1: [API Spec] ユーザー登録APIの仕様策定**
  - **Context (Red):** Issue #123により、`POST /users` のI/F定義が必要。
  - **Action (Green):** `spec-drafting` を使用し、`docs/specs/api/user-registration.md` を作成する。
  - **Refine (Refactor):** `spec-refactoring` でエッジケース（重複登録等）の考慮漏れを防ぐ。
  - **Verify:** ファイルが作成され、Request/Responseが厳密に定義されていること。

- [ ] **Step 2: [Data Spec] Usersテーブルのスキーマ定義**
  - **Context (Red):** ユーザー情報を永続化するためのテーブル設計が必要。
  - **Action (Green):** `spec-drafting` を使用し、`docs/specs/data/users-schema.md` を作成する。
...
```
