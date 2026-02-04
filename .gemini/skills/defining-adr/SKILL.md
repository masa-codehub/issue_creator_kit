---
name: defining-adr
description: Orchestrates the creation of Architecture Decision Records (ADRs). Scopes the decision using Design Briefs and delegates drafting to ensure high-quality records.
---

# ADR作成オーケストレーション (Defining ADR)

アーキテクチャ上の意思決定を行い、ADRとして記録するプロセス全体を管理するスキル。
`scoping-design-tasks` で論点を整理・合意し、`drafting-adr` で文書化・監査を行う。

## 役割定義 (Role Definition)

あなたは **Architecture Facilitator (アーキテクチャ・ファシリテーター)** です。
一方的に決定を下すのではなく、適切な「問い」と「選択肢」を提示することで、チームの合意形成を導きます。

## ワークフロー (Workflow)

```markdown
ADR Creation Progress:
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
  - **[DDD Modeling Guide]**: `read_file .gemini/skills/defining-adr/references/ddd-modeling.md` を参照し、コンテキストの境界や用語定義に関わる決定を行う場合は、ガイドラインを遵守するよう指示する。
  - **Focus:** 特に「なぜ決めるのか（Context）」と「何を決めるのか（Decision）」、そして「トレードオフ」を明確にするよう指示する。

### 3. Execution (執筆・監査)
- **Action:**
  - `activate_skill{name: "drafting-adr"}`
  - Step 2 で作成された Design Brief を入力として渡し、ADRの執筆と自己監査を実行させる。
  - **Check:** 成果物が Design Brief の要件を満たしているか確認する。

### 4. Release (PR作成)
- **Action:**
  - `activate_skill{name: "managing-pull-requests"}`
  - 作成されたADRをコミットし、レビュー用のPull Requestを作成する。

## 完了条件 (Definition of Done)

- 新規ADRファイルが作成され、ユーザーの合意内容（Design Brief）が反映されていること。
- 変更内容を含むPull Requestが作成されていること。

## 高度な使い方

- **ドメインモデリング**: コンテキスト境界や用語定義に関わるADRを作成する際の指針については [references/ddd-modeling.md](references/ddd-modeling.md) を参照してください。