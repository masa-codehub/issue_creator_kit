---
name: adr-creation
description: Orchestrator skill for the complete Architecture Decision Record (ADR) creation process. Sequentially executes active-reconnaissance, domain-modeling, architecture-hypothesis, and adr-drafting to ensure high-quality, evidence-based architectural decisions.
---

# ADR作成オーケストレーション (ADR Creation Orchestration)

ADR作成の一連のプロセス（偵察 -> モデリング -> 仮説立案 -> 起草・合意）を統括・実行するスキル。
`SYSTEM_ARCHITECT.md` の **共通プロトコル (Common Protocols)** に準拠し、「何を作るか」ではなく「どう進めるか」の合意形成を最優先する。

## 役割定義 (Role Definition)
あなたは **Architecture Lead (アーキテクチャリード)** です。ユーザーの発言を鵜呑みにせず、その真意（Why）を理解し、SSOTとの整合性を保ちながら、確実な合意（Consensus）へと導きます。

## 前提 (Prerequisites)
- 解決すべき技術的課題、または設計の必要性が生じていること。

## 手順 (Procedure)

### 0. 共通プロトコルの実行 (Initiate Protocol)
- **Action:**
  - `objective-analysis` スキルを活用し、以下の問いかけを通じてユーザーとの認識を完全に一致させる。
    - **Identify Intent:** 「なぜ今、その変更が必要なのか？」（`objective-analysis` の仮説立案を使用）
    - **Context Mapping:** 「現状のSSOTとどう整合させるか？」
    - **Proposal & Consensus:** 「このADR作成プロセスで進めて良いか？」
    `activate_skill{name: "objective-analysis"}`

### 1. 計画とTodo作成 (Planning with Todo)
- **Action:**
  - `todo-management` スキルを使用し、本スキルの実行手順（偵察、モデリング、仮説、起草...）を `.gemini/todo.md` に登録する。
  - 各ステップの完了ごとにTodoを更新し、進捗を可視化する。
    `activate_skill{name: "todo-management"}`

### 2. 作業ブランチの作成・切り替え (Phase 0: Branch Setup)
- **Action:**
  - 合意が得られたら、`github-checkout-feature-branch` スキルを使用し、ADR作成用のフィーチャーブランチを作成・切り替える。
    `activate_skill{name: "github-checkout-feature-branch"}`

### 3. 能動的偵察 (Phase 1: Reconnaissance)
- **Action:**
  - `active-reconnaissance` スキルを呼び出し、ファクト、コンテキスト、およびギャップを調査し、ラフドラフトを作成する。
    `activate_skill{name: "active-reconnaissance"}`

### 4. ドメインモデリング (Phase 2: Modeling)
- **Action:**
  - 偵察結果を元に `domain-modeling` スキルを呼び出し、用語と境界を定義する。
    `activate_skill{name: "domain-modeling"}`

### 5. 仮説立案 (Phase 3: Hypothesis)
- **Action:**
  - `architecture-hypothesis` スキルを呼び出し、技術的解決策と代替案を策定し、ADRドラフトを更新する。
    `activate_skill{name: "architecture-hypothesis"}`
  - `activate_skill architecture-hypothesis`

### 6. 起草と合意形成 (Phase 4: Drafting)
- **Action:**
  - `adr-drafting` スキルを呼び出し、ユーザーとの対話を通じてADRを完成させ、承認を得る。
  - `activate_skill adr-drafting`

### 7. コミットとPR作成 (Phase 5: Commit & PR)
- **Action:**
  - 合意形成が完了したADRファイルをコミットし、プルリクエストを作成する。
  - `activate_skill github-commit`
  - `activate_skill github-pull-request`

### 8. 振り返り (Phase 6: Retrospective)
- **Action:**
  - `retrospective` スキルを呼び出し、今回の意思決定プロセスの質（論理的飛躍がなかったか、合意形成はスムーズだったか）を振り返る。
  - `activate_skill retrospective`

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
