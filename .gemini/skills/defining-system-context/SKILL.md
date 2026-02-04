---
name: defining-system-context
description: Orchestrates the definition and maintenance of the system's "Map" (SSOT). Aligns codebase reality with design intent to produce a verified system-context.md.
---

# システムコンテキスト定義 (Defining System Context)

システムの全体像（SSOT）である `docs/system-context.md` を定義・更新するオーケストレーションスキル。
`scoping-design-tasks` で設計方針を固め、`drafting-system-context` で文書化・監査を行う一連 flow を管理する。

## 役割定義 (Role Definition)

あなたは **Chief Cartographer (地図製作責任者)** です。
プロジェクトの「地図」を常に最新かつ正確に保つため、分析・合意・執筆・リリースの全工程を監督します。

## ワークフロー (Workflow)

```markdown
Context Creation Progress:
- [ ] 1. Preparation (ブランチ作成)
- [ ] 2. Scoping (方針策定・合意)
- [ ] 3. Execution (執筆・監査)
- [ ] 4. Release (PR作成)
```

### 1. Preparation (ブランチ作成)
- **Action:**
  - 作業用のFeature Branchを作成し、安全な作業環境を確保する。
  - `activate_skill{name: "switching-feature-branch"}`

### 2. Scoping (方針策定・合意)
- **Action:**
  - `activate_skill{name: "scoping-design-tasks"}`
  - 現状分析 (`scouting-facts`)、論点整理、およびユーザーとの合意形成を行い、**Design Brief (設計指針)** を完成させる。
  - **[DDD Modeling Guide]**: `read_file .gemini/skills/defining-system-context/references/ddd-modeling.md` を参照し、システム境界とコンテキストマップ（Context Map）の定義においてガイドラインを遵守するよう指示する。
  - **Focus:** 特に「システム境界」と「ビジネス価値」の定義に注力するよう指示する。

### 3. Execution (執筆・監査)
- **Action:**
  - `activate_skill{name: "drafting-system-context"}`
  - Step 2 で作成された Design Brief を入力として渡し、ドメインの執筆と作図、および自己監査を実行させる。
  - **Check:** 成果物 (`docs/system-context.md`) が Design Brief の要件を完全に満たしているか確認する。

### 4. Release (PR作成)
- **Action:**
  - `activate_skill{name: "managing-pull-requests"}`
  - 作成された変更をコミットし、レビュー用のPull Requestを作成する。
  - **Output:** 作成されたPRのURLをユーザーに報告する。

## 完了条件 (Definition of Done)

- `docs/system-context.md` が更新され、ユーザーの合意内容（Design Brief）が反映されていること。
- 変更内容を含むPull Requestが作成されていること。

## 高度な使い方

- **ドメインモデリング**: DDDに基づく境界定義や用語統一の手法については [references/ddd-modeling.md](references/ddd-modeling.md) を参照してください。

