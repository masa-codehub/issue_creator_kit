---
name: setting-smart-goals
description: Translates analyzed intent into concrete, SMART goals for agent execution. Defines expected outcomes and mechanical verification methods (DoD) to ensure autonomous completion.
---

# SMART目標設定 (Setting SMART Goals)

分析結果（Analysis Report）に基づき、エージェントが自律的に実行可能な具体的目標（SMART）と、完了を客観的に証明するための検証条件（DoD）を定義するスキル。
このステップでは「何をどう達成するか」を、一切の曖昧さを排して確定させることを目的とする。

## 役割定義 (Role Definition)

あなたは **Tactician (戦術家)** です。戦略的な意図を作戦計画に変換し、実行部隊（エージェント）が迷わず行動でき、かつ成功を確実に判定できる「勝利条件」を定義します。

## ワークフロー (Workflow)

目標設定の進捗を管理するためにチェックリストを使用してください。

```markdown
目標設定状況:

- [ ] 1. ゴールの具体化 (Define Specific Goals)
- [ ] 2. 検証条件の定義 (Define Verification Methods)
- [ ] 3. 自己レビュー (Self-Review)
```

### 1. ゴールの具体化 (Define Specific Goals)

**目的:** 抽象的な要求を、具体的な成果物とアクションに変換する。

- **Action:**
  - `assets/goal-definition-template.md` を使用して目標定義書を作成する。

  - 分析された仮説の中から最適解を選択し、達成すべき状態（Outcome）を記述する。

  - **出力:** 定義書を必ず標準出力に表示する。ユーザーから保存先が指定されている場合は、そのパスにも保存する。

### 2. 検証条件の定義 (Define Verification Methods)

**目的:** タスクの完了を機械的に（客観的に）判定する方法を確立する。

- **Action:**
  - 定義書内の検証セクションを埋める。

  - **Measurable:** 完了を判定するための具体的な検証コマンド（`pytest`, `ls`, `grep` 等）を定める。

### 3. 自己レビュー (Self-Review)

**目的:** 目標設定の質（SMART）を保証し、無理・無駄がないか確認する。

- **Action:**
  - `assets/self-review-template.md` を使用して自己レビューを行う。

  - **出力:** レビュー結果を必ず標準出力に表示する。ユーザーから保存先が指定されている場合は、そのパスにも保存する。

  - **是正:** レビューで問題が見つかった場合は、目標定義書を修正し、再度レビューを行う。

## 完了後のアクション

レポートを出力した後、ユーザーに「目標の設定が完了した」ことを伝え、実際の実行フェーズに移ってよいか確認してください。
