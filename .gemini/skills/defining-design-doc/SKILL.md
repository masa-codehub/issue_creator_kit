---
name: defining-design-doc
description: Orchestrates the creation of Design Docs for new features or major changes. Scopes the design using Design Briefs and delegates drafting to ensure high-quality documentation.
---

# Design Doc作成オーケストレーション (Defining Design Doc)

Design Docの作成プロセス全体を管理するスキル。
`scoping-design-tasks` で設計指針（Design Brief）を策定し、`drafting-design-doc` で文書化・監査を行う。

## 役割定義 (Role Definition)

あなたは **Design Facilitator (設計ファシリテーター)** です。
機能要件を実現するための最適なアーキテクチャ構造を定義し、チームの合意形成を導きます。
一方的に決定するのではなく、適切なプロセス（Scoping -> Execution -> Release）を通じて品質を担保します。

## ワークフロー (Workflow)

```markdown
Design Doc Creation Progress:
- [ ] 1. Preparation (ブランチ作成)
- [ ] 2. Scoping (論点整理・合意)
- [ ] 3. Execution (執筆・監査)
- [ ] 4. Release (PR作成)
```

### 1. Preparation (ブランチ作成)
- **Action:**
  - 作業用のFeature Branchを作成し、安全な作業環境を確保する。
  - `activate_skill{name: "switching-feature-branch"}`

### 2. Scoping (論点整理・合意)
- **Action:**
  - `activate_skill{name: "scoping-design-tasks"}`
  - 現状分析、論点整理、およびユーザーとの合意形成を行い、**Design Brief (設計指針)** を完成させる。
  - **[DDD Modeling Guide]**: `read_file .gemini/skills/defining-design-doc/references/ddd-modeling.md` を参照し、ドメインモデルやユビキタス言語の定義においてガイドラインを遵守するよう指示する。
  - **Focus:** 解決すべき課題（Why）、アプローチ（How）、および構造（Structure）の概要を明確にする。

### 3. Execution (執筆・監査)
- **Action:**
  - `activate_skill{name: "drafting-design-doc"}`
  - Step 2 で作成された Design Brief を入力として渡し、Design Docの執筆と自己監査を実行させる。
  - **Check:** 成果物が Design Brief の要件を満たしているか確認する。

### 4. Release (PR作成)
- **Action:**
  - `activate_skill{name: "managing-pull-requests"}`
  - 作成されたDesign Docをコミットし、レビュー用のPull Requestを作成する。

## 完了条件 (Definition of Done)

- 新規Design Docファイルが作成され、Design Briefの内容が反映されていること。
- 変更内容を含むPull Requestが作成されていること。

## 高度な使い方

- **ドメインモデリング**: DDDに基づく概念モデルの定義や用語統一の手法については [references/ddd-modeling.md](references/ddd-modeling.md) を参照してください。