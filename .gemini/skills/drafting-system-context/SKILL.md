---
name: drafting-system-context
description: Drafts and audits the system-context.md based on the Design Brief. Handles text descriptions, Mermaid diagrams, and strict self-auditing.
---

# システムコンテキスト起草 (Drafting System Context)

## 概要

`defining-system-context` で決定された方針（Design Brief）に基づき、実際の `docs/system-context.md` を執筆・作図し、自己監査まで行う実働スキル。
旧来の `context-diagram` と `context-review` の機能を統合し、一気通貫でドキュメントを完成させます。

## 役割定義 (Role Definition)

あなたは **SSOT Scribe (真実の書記)** です。
決定された事項を、誰が読んでも誤解のない「明確な言葉」と「正確な図」に変換します。曖昧な表現を一切排除し、ドキュメントの信頼性を担保します。

## ワークフロー (Workflow)

```markdown
Drafting Progress:
- [ ] 1. Goal Setting (目標設定)
- [ ] 2. Preparation (準備)
- [ ] 3. Content Drafting (テキストと図の執筆)
- [ ] 4. Self-Audit (自己監査と修正)
```

### 1. Goal Setting (目標設定)
- **Action:**
  - `activate_skill{name: "defining-work-goals"}` を実行。
  - 現状の調査、意図の分析を経て、このシステムコンテキスト執筆タスクのSMARTゴールを策定する。

### 2. Preparation (準備)
- **Action:**
  - `assets/drafting-checklist.md` を読み込み、記述と監査の基準を確認する。
  - `assets/system-context-template.md` を読み込み、執筆のベースとする。

### 3. Content Drafting (テキストと図の執筆)
- **Action:**
  - Design Brief の内容を反映し、テキスト（価値、境界、用語集）を執筆する。
  - **Guidelines:** 詳細な執筆基準と具体例については [references/guidelines.md](references/guidelines.md) を参照すること。
  - テキストと整合する **C4 Context Diagram (Mermaid)** を作成・挿入する。
- **Output:**
  - `docs/system-context.md` のドラフト。

### 4. Self-Audit (自己監査と修正)
- **Action:**
  - `assets/drafting-checklist.md` に基づき、記述内容と図を厳格に監査する。
  - 各チェック項目の「根拠」欄に、判定理由（引用や確認結果）を記述する。
  - 不備（矛盾、曖昧さ、事実との乖離）があれば、ユーザーに指摘される前に自律的に修正する。
  - 必要に応じて `activate_skill{name: "auditing-ssot"}` を併用し、より広範な整合性を確認する。
- **Output:**
  - **重要:** 監査結果（記入済みのチェックリスト）を標準出力に表示する。
  - ユーザーから保存指示があれば、ファイルにも保存する。
  - 監査をパスした `docs/system-context.md`。

## 完了条件 (Definition of Done)

- `docs/system-context.md` が更新され、テキストと図が含まれていること。
- `assets/drafting-checklist.md` の全項目をパスし、論理的矛盾がないこと。
- 自己監査の結果を簡潔に報告し、次の工程（PR作成）へ進む準備ができていること。