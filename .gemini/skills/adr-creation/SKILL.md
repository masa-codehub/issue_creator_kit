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
  - 作業を開始する前に、以下の問いかけを行い、ユーザーとの認識を合わせる。
    - 「なぜ今、その変更が必要なのか？」（意図の解釈）
    - 「現状のSSOTとどう整合させるか？」（コンテキストマッピング）
    - 「このADR作成プロセスで進めて良いか？」（提案と合意）

### 1. 作業ブランチの作成・切り替え (Phase 0: Branch Setup)
- **Action:**
  - 合意が得られたら、`github-checkout-feature-branch` スキルを使用し、ADR作成用のフィーチャーブランチを作成・切り替える。
  - `activate_skill github-checkout-feature-branch`

### 2. 能動的偵察 (Phase 1: Reconnaissance)
- **Action:**
  - `active-reconnaissance` スキルを呼び出し、ファクト、コンテキスト、およびギャップを調査し、ラフドラフトを作成する。
  - `activate_skill active-reconnaissance`

### 3. ドメインモデリング (Phase 2: Modeling)
- **Action:**
  - 偵察結果を元に `domain-modeling` スキルを呼び出し、用語と境界を定義する。
  - `activate_skill domain-modeling`

### 4. 仮説立案 (Phase 3: Hypothesis)
- **Action:**
  - `architecture-hypothesis` スキルを呼び出し、技術的解決策と代替案を策定し、ADRドラフトを更新する。
  - `activate_skill architecture-hypothesis`

### 5. 起草と合意形成 (Phase 4: Drafting)
- **Action:**
  - `adr-drafting` スキルを呼び出し、ユーザーとの対話を通じてADRを完成させ、承認を得る。
  - `activate_skill adr-drafting`

### 6. コミットとPR作成 (Phase 5: Commit & PR)
- **Action:**
  - 合意形成が完了したADRファイルをコミットし、プルリクエストを作成する。
  - `activate_skill github-commit`
  - `activate_skill github-pull-request`

### 7. 振り返り (Phase 6: Retrospective)
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
