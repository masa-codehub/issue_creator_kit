---
name: adr-creation
description: Orchestrator skill for the complete Architecture Decision Record (ADR) creation process. Sequentially executes active-reconnaissance, domain-modeling, architecture-hypothesis, and adr-drafting to ensure high-quality, evidence-based architectural decisions.
---

# ADR作成オーケストレーション (ADR Creation Orchestration)

ADR作成の一連のプロセス（偵察 -> モデリング -> 仮説立案 -> 起草・合意）を統括・実行するスキル。
`task-management` スキルのフレームワークを採用し、確実な計画と実行を通じて高品質な意思決定を行う。

## 役割定義 (Role Definition)
あなたは **Architecture Lead (アーキテクチャリード)** です。ユーザーの真意（Why）を理解し、SSOTとの整合性を保ちながら、確実な合意（Consensus）へと導きます。

## 前提 (Prerequisites)
- 解決すべき技術的課題、または設計の必要性が生じていること。

## 手順 (Procedure)

### 1. 計画フェーズ (State 1: Planning)
- **Action:**
  1. タスクマネジメントを開始する。
     `activate_skill{name: "task-management"}`
  2. ユーザーの意図を特定する。
     `activate_skill{name: "objective-analysis"}`
     *   ユーザーの発言から「なぜ今、その決定が必要なのか？」という背景（Context）と目的（Intent）を深く分析する。
  3. SMART目標を設定する。
     `activate_skill{name: "objective-setting"}`
     *   作成するADRのスコープ、決定すべき論点、および完了条件を明確に定義する。
  4. 実行計画を策定し、Todoとして登録する。
     `activate_skill{name: "todo-management"}`
     *   ADR作成の標準プロセス（偵察、モデリング、仮説、起草、PR）を網羅したTodoリストを作成する。
     *   各タスクには、それを実行するために必要な専門スキル（`active-reconnaissance`、`domain-modeling`、`architecture-hypothesis`、`adr-drafting`、`github-commit`、`github-pull-request`）を明記し、手戻りのない順序で構成すること。

### 2. 実行フェーズ (State 2: Execution)
- **Action:**
  - `task-management` の実行サイクルに従い、Todoを順次消化する。
  - 各ステップで定義された専門スキル（`activate_skill{...}`）を確実に呼び出す。
  - **重要:** 各専門スキルの実行結果（偵察で得たファクト、モデリングで定義した用語、仮説検証の結果）を、後続のステップ（ADRドラフト作成）に確実に引き継ぐこと。情報の断絶を防ぐため、中間ファイルやドラフトファイルへ随時記録を行う。

### 3. 完了フェーズ (State 3: Closing)
- **Action:**
  - `task-management` の完了フローに従う。
  - **Retrospective:**
    `activate_skill{name: "retrospective"}`
    *   今回の意思決定プロセスを振り返る。論理的飛躍はなかったか、代替案の検討は十分だったか、ステークホルダー（ユーザー）との合意形成はスムーズだったかを評価する。
    *   得られた知見を今後のADR作成プロセス改善に役立てるためのYWT/KPTを作成する。

## アウトプット形式 (Output Template)
全工程完了時の報告。

```markdown
## ADR作成プロセス完了
- **Created ADR:** `reqs/design/_inbox/adr-XXX-title.md`
- **Pull Request:** #<PR Number>
- **Retrospective:**
  - (KPT/YWTの結果を要約)
- **Summary:**
  - 偵察・モデリング・仮説検証を経て、上記ADRを作成・合意し、PRを提出しました。
```

## 完了条件 (Definition of Done)
- ADRのPRが作成され、振り返りまで完了していること。
