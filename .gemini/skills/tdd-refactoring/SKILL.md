---
name: tdd-refactoring
description: Executes the Refactoring Loop to improve code quality without changing behavior. Iterates through analysis, improvement, and verification until all standards (SSOT, Linter) are met.
---

# TDD Refactoring Cycle

このスキルは、機能実装（Green）が完了したコードに対し、品質基準（SSOT、Linter、可読性）を満たすまで **「分析 → 改善 → 検証」** のサイクルを反復する。

## 役割定義 (Role Definition)
あなたは **Code Craftsman** です。動くコード（Working Code）を、維持可能なコード（Clean Code）へと昇華させます。

## 前提 (Prerequisites)
- テストがパスしている状態（Green）であること。
- `.gemini/todo.md` にリファクタリングの指針（Coding Guidelines, ADR参照など）が含まれていること。

## 手順 (Procedure)

### 1. 現状分析 (Analyze with Active Reconnaissance)
- **Input:**
  - **前サイクルの自己レビュー結果（改善提案）。**
  - `python-verification` (Linter/Type Checker) の出力。
    `activate_skill{name: "python-verification"}`
  - プロジェクトの規約 (`docs/guides/coding-guidelines.md`, `styleguide.md`)。
  - TDD Plan で指摘された「あるべき構造」。
- **Action:**
  - **コードの匂い、重複、命名の不一致、型ヒントの欠落を特定するために**、`active-reconnaissance` スキルを呼び出す。
    `activate_skill{name: "active-reconnaissance"}`
  - 現在のコード（Reality）とSSOT/規約（Intent）の間のギャップを分析する。
    - ここでのIntentは「SSOTに準拠したClean Codeであること」と定義し、そこからの乖離をリファクタリングの対象とする。
  - **判定:** 改善すべきギャップがなければサイクルを終了する。

### 2. 改善 (Refactor)
- **Action:**
  - **振る舞いを変えずに** 構造のみを変更する（ボーイスカウト・ルール）。
  - `replace` や `write_file` を使用してコードを修正する。
  - 必要に応じて小さなステップに分割する。

### 3. 検証 (Verify)
- **Action:**
  - `pytest` を実行し、**テストが引き続きGreenであること**を確認する（デグレードチェック）。
  - `python-verification` を実行し、静的解析のエラーが減ったことを確認する。
    `activate_skill{name: "python-verification"}`

### 4. 自己レビューと改善提案 (Self-Review & Proposal)
- **Action:**
  - 以下のチェックリストに基づき、各観点で「改善の余地はないか？」を自問する。
  - 発見された課題に対し、具体的な改善案（Proposal）を作成する。

  - **Checklist & Proposal:**
    - [ ] **Simplicity (YAGNI):** 不要な抽象化、過剰な汎用化、未使用のコードはないか？
      - *Proposal:* ...
    - [ ] **Clean Architecture:** ドメイン層がインフラ層の詳細を知ってしまっていないか？依存の方向は正しいか？
      - *Proposal:* ...
    - [ ] **Naming (Ubiquitous Language):** 変数・メソッド名は「実装の詳細」ではなく「ドメインの意図」を語っているか？
      - *Proposal:* ...
    - [ ] **Readability:** メソッドは長すぎないか？（1つのことだけをしているか？）コメントなしで理解できるか？
      - *Proposal:* ...
    - [ ] **User Value:** この複雑さはユーザーのメリットにつながっているか？

  - 提案の中から、**最も効果が高く、リスクが低い1つ**を選択し、宣言する。次ステップ（Iterate）へのインプットとする。

### 5. 反復 (Iterate)
- **Input:**
  - Step 4 で選択された改善提案。
- **Action:**
  - 改善提案が存在する場合、その内容をターゲットとして **Step 1 (Analyze) に戻る**。
    - ※ このループは機械的に実行される。
  - 改善提案がない場合、リファクタリングサイクルを終了する。

## 完了条件 (Definition of Done)
- 全てのテストがパスしている。
- Linter/Formatter の警告がゼロである。
- プロジェクトの規約（SSOT）に準拠していることが確認された。

