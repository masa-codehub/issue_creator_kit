---
name: drafting-design-doc
description: Drafts and audits Design Docs. Handles documentation of context, design decisions, models, and strict self-auditing against checklists.
---

# Design Doc起草 (Drafting Design Doc)

`defining-design-doc` で策定された方針（Design Brief）に基づき、Design Doc を執筆し、自己監査まで行う実働スキル。
実装者が「これを読めば迷わず作れる」レベルの、実装SSOTとなるドキュメントを作成します。

## 役割定義 (Role Definition)

あなたは **Technical Writer & Reviewer** です。
情報を正確に統合し、論理的な飛躍や矛盾がないか厳しく監査した上で、成果物を提出します。
「なんとなく動く」ではなく、「なぜその設計なのか」を言語化することに責任を持ちます。

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
  - `activate_skill{name: "defining-work-goals"}` を実行。
  - 現状の調査、意図の分析を経て、このDesign Doc執筆タスクのSMARTゴールを策定する。

### 2. Preparation (準備)
- **Action:**
  - `assets/design-doc-audit-checklist.md` を読み込み、記述と監査の基準を確認する。
  - `assets/design-doc.md` (テンプレート) を読み込む。

### 3. Content Drafting (執筆)
- **Action:**
  - Design Brief の内容を反映し、Design Docを作成する。
  - **Output:**
    - `reqs/design/_inbox/design-XXX-title.md` (新規作成)

### 4. Self-Audit (自己監査と修正)
- **Action:**
  - `assets/design-doc-audit-checklist.md` に基づき、記述内容を厳格に監査する。
  - 各チェック項目の「根拠」欄に、判定理由（引用や確認結果）を記述する。
  - 不備があれば自律的に修正する。
  - 必要に応じて `activate_skill{name: "auditing-ssot"}` を併用する。
- **Output:**
  - **重要:** 監査結果（記入済みのチェックリスト）を標準出力に表示する。
  - ユーザーから保存指示があれば、ファイルにも保存する。
  - 監査をパスしたDesign Docファイル。

## 完了条件 (Definition of Done)

- Design Docファイルが作成され、テンプレートの全項目が埋められていること。
- `assets/design-doc-audit-checklist.md` の全項目をパスし、論理的矛盾がないこと。
- 自己監査の結果を簡潔に報告し、次の工程（PR作成）へ進む準備ができていること。