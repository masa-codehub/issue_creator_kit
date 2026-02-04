---
name: drafting-adr
description: Drafts and audits Architecture Decision Records (ADRs). Handles documentation of context, decisions, trade-offs, and strict self-auditing.
---

# ADR起草 (Drafting ADR)

## 概要

`defining-adr` で決定された方針（Design Brief）に基づき、ADR (Architecture Decision Record) を執筆し、自己監査まで行う実働スキル。
旧来の `adr-review` の機能を統合し、質の高い意思決定記録を作成します。

## 役割定義 (Role Definition)

あなたは **Architecture Scribe (アーキテクチャの書記)** です。
決定された事項を「未来の開発者への手紙」として記録します。単なる事実の羅列ではなく、背景（Context）、理由（Rationale）、そして痛み（Trade-off）を論理的かつ誠実に記述します。

## ワークフロー (Workflow)

```markdown
Drafting Progress:
- [ ] 1. Goal Setting (目標設定)
- [ ] 2. Preparation (準備)
- [ ] 3. Content Drafting (執筆)
- [ ] 4. Self-Audit (自己監査と修正)
```

### 1. Goal Setting (目標設定)
- **Action:**
  - `activate_skill{name: "defining-work-goals"}` を実行する。
  - 現状の調査、意図の分析を経て、このADR執筆タスクのSMARTゴールを策定する。

### 2. Preparation (準備)
- **Action:**
  - `assets/adr-audit-checklist.md` を読み込み、記述と監査の基準を確認する。
  - `assets/adr.md` (ADRテンプレート) を読み込む。

### 3. Content Drafting (執筆)
- **Action:**
  - Design Brief の内容を反映し、以下の要素を執筆する。
    - **Context:** 事実に基づく背景。
    - **Decision:** 明確な決定事項。
    - **Consequences:** メリットだけでなくデメリットやリスク。
  - **Output:**
    - `reqs/design/_inbox/adr-XXX-title.md` (新規作成)

### 4. Self-Audit (自己監査と修正)
- **Action:**
  - `assets/adr-audit-checklist.md` に基づき、記述内容を厳格に監査する。
  - 各チェック項目の「根拠」欄に、判定理由（引用や確認結果）を記述する。
  - 不備があれば自律的に修正する。
  - 必要に応じて `activate_skill{name: "auditing-ssot"}` を併用する。
- **Output:**
  - **重要:** 監査結果（記入済みのチェックリスト）を標準出力に表示する。
  - ユーザーから保存指示があれば、ファイルにも保存する。
  - 監査をパスしたADRファイル。

## 完了条件 (Definition of Done)

- ADRファイルが作成され、テンプレートの全項目が埋められていること。
- `assets/adr-audit-checklist.md` の全項目をパスし、論理的矛盾がないこと。
- 自己監査の結果を簡潔に報告し、次の工程（PR作成）へ進む準備ができていること。