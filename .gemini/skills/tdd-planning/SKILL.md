---
name: tdd-planning
description: Analyzes requirements and SSOT to formulate a concrete TDD plan. Used for (1) translating ambiguous requirements into verifiable test scenarios, (2) ensuring new features align with existing architecture before coding, and (3) defining the "Red-Green-Refactor" strategy for complex logic.
---

# TDD Planning

このスキルは、実装に入る前に「何を」「なぜ」「どのように」テストし実装するかを明確にし、手戻りを防ぐための計画策定を目的とします。

## 役割定義 (Role Definition)
あなたは **TDD Architect** です。要件を厳密なテスト仕様に変換し、ドメインの整合性とアーキテクチャの遵守を保証する計画を立てます。

## 前提 (Prerequisites)
- 既存スキル `active-reconnaissance`, `ssot-verification`, `todo-management` が利用可能であること。
- 実装対象の Issue または要件が特定されていること。

## 手順 (Procedure)

### 1. 能動的偵察 (Active Reconnaissance)
- **Action:**
  - `todo-management` スキルをアクティベートする。
    `activate_skill{name: "todo-management"}`
  - `issue_read` を実行し、表面的な要件だけでなく「ユーザー価値（Why）」を特定する。
  - `active-reconnaissance` スキルを活用し、関連するSSOT（ADR、仕様書、ガイドライン等）を読み込む。
    `activate_skill{name: "active-reconnaissance"}`
  - `read_file` で実装対象周辺の既存コードと既存テストを確認する。

### 2. 設計整合性チェック (SSOT Verification)
- **Action:**
  - `ssot-verification` スキルを活用し、以下の観点で現在の理解と設計を照合する。
    `activate_skill{name: "ssot-verification"}`
    - [ ] **ユビキタス言語:** 提案するメソッド名や引数名が、ドキュメントで定義された用語と一致しているか？
    - [ ] **レイヤー構造:** 実装箇所がクリーンアーキテクチャの責務（Domain, UseCase等）に合致しているか？
    - [ ] **依存の方向:** 下位レイヤーへの直接的な依存や、ビジネスロジックの漏洩がないか？

### 3. TDD Plan の策定
- **Action:**
  - 収集した情報に基づき、以下のテンプレートを用いて具体的なシナリオを作成する。
  - **Checklist:**
    - [ ] **Red:** 失敗すべき振る舞いの **根拠 (Basis: ADR/Spec)** は明確か？
    - [ ] **Green:** 実装すべきロジックの **最小限の定義** は何か？
    - [ ] **Refactor:** 準拠すべき **規約 (Styleguide/ADR)** はどれか？

### 4. Todo分解 (via todo-management)
- **Action:**
  - `todo-management` の「タスク分解フレームワーク」に従い、策定した「TDD Plan」を `.gemini/todo.md` の形式に変換する。
  - **マッピングルール:**
    - **Task Name:** [Red/Green/Refactor] + 簡潔な作業名
    - **Action:** 具体的なツール操作（`write_file`, `replace` 等）と、**その根拠となるドキュメントの参照**。
    - **Verify:** 成功を判定するコマンド（`pytest`, `ruff`, `mypy` 等）と、期待される結果。

### 5. レビューと洗練 (Review & Refinement)
- **Action:**
  - 以下の「4大リスク」の観点でTDD Plan全体を自己評価し、懸念があれば計画を修正する。
    - [ ] **価値 (Value):** 本当にこの実装でユーザー課題が解決されるか？
    - [ ] **ユーザビリティ (Usability):** 実装されるインターフェース（API, CLI等）は使いやすいか？
    - [ ] **実現可能性 (Feasibility):** 計画された時間と技術で完遂できるか？
    - [ ] **ビジネス生存性 (Viability):** セキュリティ、保守性、コストに問題はないか？
  - `todo-review` を実行し、計画が原子レベルまで砕かれているか、論理的な飛躍がないかを最終確認する。
    `activate_skill{name: "todo-review"}`
  - **修正フロー:**
    - **要件・設計レベルの不備:** Step 3 (TDD Plan の策定) に戻る。
    - **タスク粒度・記述の不備:** Step 4 (Todo分解) に戻る。
  - 指摘事項が完全になくなり、承認条件（Approve）を満たすまでループする。

## アウトプット形式 (Output Template)

```markdown
## TDD Plan: [Issue Title/ID]
- **Goal:** [SMART目標]
- **Context:** [参照ドキュメント一覧]

### Scenarios
1. **Red (Test Case)**
   - **Basis:** [ADR-XXX / Spec Name]
   - **Plan:** [ファイルパス] に [テスト名] を追加。
   - **Expectation:** [期待される失敗理由] で失敗する。

2. **Green (Implementation)**
   - **Basis:** [ロジックの仕様/要件]
   - **Plan:** [ファイルパス] に最小限の [ロジック] を実装。
   - **Expectation:** テストがパスする。

3. **Refactor (Quality)**
   - **Basis:** [Coding Guidelines / Styleguide]
      - **Plan:** `tdd-refactoring` を起動し、[改 善対象] を整理。
   - **Expectation:** Linter/Type Check パス、かつテストがGreen維持。

- **Risks:** [4 Big Risks]
```

---
※ 詳細な実行ステップは上記マッピングルールに従い `.gemini/todo.md` に展開されました。


## 完了条件 (Definition of Done)
- ユーザーに TDD Plan を提示し、合意を得ていること。
- `todo-management` によって、実行フェーズの具体的かつ原子的なステップが `.gemini/todo.md` に定義されていること。

