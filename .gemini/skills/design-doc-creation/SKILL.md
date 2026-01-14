---
name: design-doc-creation
description: Orchestrator skill for creating Detailed Design Documents. Sequentially executes active-reconnaissance, domain-modeling, technical-design, reliability-design, and design-doc-drafting to build a solid implementation blueprint.
---

# Design Doc作成オーケストレーション (Design Doc Creation)

Design Doc作成の一連のプロセス（偵察 -> モデリング -> 詳細設計 -> 信頼性設計 -> 起草・合意）を統括・実行するスキル。
`task-management` スキルのフレームワークを採用し、実装フェーズの手戻りを防ぐための詳細な青写真を作成する。

## 役割定義 (Role Definition)
あなたは **Lead Architect (リードアーキテクト)** です。ビジネス要求を、開発者が迷いなく実装可能な「技術仕様」へと変換する全責任を持ちます。

## 前提 (Prerequisites)
- 具体的な機能追加や変更の要求があり、ADR（方向性の決定）が完了している、または自明であること。

## 手順 (Procedure)

### 1. 計画フェーズ (State 1: Planning)
- **Action:**
  1. タスクマネジメントを開始する。
     `activate_skill{name: "task-management"}`
  2. 詳細設計の目的とスコープを特定する。
     `activate_skill{name: "objective-analysis"}`
     *   実装により達成すべきビジネス価値と、影響範囲（Bounded Context）を明確にする。既存のADRや要件定義書を参照し、設計の前提条件を洗い出す。
  3. SMART目標を設定する。
     `activate_skill{name: "objective-setting"}`
     *   成果物となるDesign Docのファイル名、対象機能、およびレビュー基準（誰の合意が必要か）を定義する。
  4. 実行計画を策定し、Todoとして登録する。
     `activate_skill{name: "todo-management"}`
     *   詳細設計の標準プロセス（偵察、モデリング、技術設計、信頼性設計、起草、PR）を網羅したTodoリストを作成する。
     *   各タスクには、対応する専門スキル（`active-reconnaissance`、`domain-modeling`、`technical-design`、`reliability-design`、`design-doc-drafting`、`github-commit`、`github-pull-request`）を割り当て、依存関係を考慮した順序で構成すること。

### 2. 実行フェーズ (State 2: Execution)
- **Action:**
  - `task-management` の実行サイクルに従い、各専門スキル (`activate_skill{...}`) を呼び出してTodoを順次消化する。
  - **重要:** 各設計ステップでの決定事項（データモデル、API仕様、非機能要件）が相互に矛盾しないよう、常に整合性を確認しながら進めること。特に `reliability-design` で定義したエラー処理やリトライ方針が、`technical-design` のシーケンス図やAPI定義に反映されていることを確認する。

### 3. 完了フェーズ (State 3: Closing)
- **Action:**
  - `task-management` の完了フローに従う。
  - **Retrospective:**
    `activate_skill{name: "retrospective"}`
    *   設計プロセスの質を振り返る。
    *   「実装者が迷う曖昧さは残っていないか」「エッジケースの考慮漏れはないか」といった観点で自身の設計アウトプットを評価し、次回の設計品質向上につなげる。

## アウトプット形式 (Output Template)
全工程完了時の報告。

```markdown
## Design Doc作成プロセス完了
- **Created Doc:** `reqs/design/_inbox/design-XXX-title.md`
- **Pull Request:** #<PR Number>
- **Summary:**
  - 詳細設計、信頼性設計を経て、上記Design Docを作成・合意し、PRを提出しました。
```

## 完了条件 (Definition of Done)
- Design DocのPRが作成され、振り返りまで完了していること。