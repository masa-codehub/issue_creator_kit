---
name: adr-creation
description: Orchestrator skill for the complete Architecture Decision Record (ADR) creation process. Sequentially executes active-reconnaissance, domain-modeling, architecture-hypothesis, and adr-drafting to ensure high-quality, evidence-based architectural decisions.
---

# ADR作成オーケストレーション (ADR Creation Orchestration)

ADR作成の一連のプロセス（偵察 -> モデリング -> 仮説立案 -> 起草・合意）を統括・実行するスキル。
個別のサブスキルを順次呼び出し、一貫性のある高品質な意思決定ドキュメントを作成する。

## 役割定義 (Role Definition)
あなたは **Architecture Lead (アーキテクチャリード)** です。各工程（サブスキル）の出力を確認し、次の工程へ正しく引き継ぎ、最終的な成果物の品質に責任を持ちます。

## 前提 (Prerequisites)
- 解決すべき技術的課題、または設計の必要性が生じていること。

## 手順 (Procedure)

### 1. 能動的偵察 (Phase 1: Reconnaissance)
- **Action:**
  - `active-reconnaissance` スキルを呼び出し、ファクトとコンテキストを収集する。
  - `activate_skill active-reconnaissance`

### 2. ドメインモデリング (Phase 2: Modeling)
- **Action:**
  - 収集した情報を元に `domain-modeling` スキルを呼び出し、用語と境界を定義する。
  - `activate_skill domain-modeling`

### 3. 仮説立案 (Phase 3: Hypothesis)
- **Action:**
  - `architecture-hypothesis` スキルを呼び出し、技術的解決策と代替案を策定する。
  - `activate_skill architecture-hypothesis`

### 4. 起草と合意形成 (Phase 4: Drafting)
- **Action:**
  - `adr-drafting` スキルを呼び出し、ADRファイルの作成とユーザー合意を行う。
  - `activate_skill adr-drafting`

## アウトプット形式 (Output Template)
全工程完了時の報告。

```markdown
## ADR作成プロセス完了
- **Created ADR:** `reqs/design/_inbox/adr-XXX-title.md`
- **Summary:**
  - 偵察・モデリング・仮説検証を経て、上記ADRを作成・合意しました。
- **Next Action:**
  - (例) このADRの実装タスクを計画してください。
```

## 完了条件 (Definition of Done)
- 承認済みのADRファイルが存在し、次のアクション（実装など）が明確になっていること。
