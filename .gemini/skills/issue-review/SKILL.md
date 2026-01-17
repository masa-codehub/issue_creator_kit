---
name: issue-review
description: Audits created issue drafts for quality, clarity, and template compliance. Ensures each issue aligns with the core values of SYSTEM_ARCHITECT, TECHNICAL_DESIGNER, and BACKENDCODER, guaranteeing actionability and value.
---

# Issue Review (Value-Driven Audit)

作成された `reqs/tasks/drafts/*.md` を厳格にレビューし、形式的な品質だけでなく、プロジェクトの核心的な価値観（Values）に合致しているかを監査するスキル。

## 役割 (Role)
**Quality Auditor (品質監査人)**
作業担当者の視点に立ち、「この指示だけで迷わず完遂できるか？」を問うとともに、アーキテクトの視点で「これは正しい方向への一歩か？」を問う。

## 手順 (Procedure)

### 1. 形式監査 (Template & Syntax Audit)
- **Checklist:**
    - [ ] **Meta Integrity:** `roadmap`, `task_id`, `labels` が正しく埋まっているか？
    - [ ] **Structure:** セクション 1 ～ 6 が全て存在し、テンプレート構造を維持しているか？
    - [ ] **No Placeholders:** `{{title}}` 等の変数が残っていないか？

### 2. 価値観に基づく監査 (Value-Driven Audit)
各エージェントの行動規範に基づき、内容を精査する。

#### A. SYSTEM_ARCHITECT Perspective (全体最適と価値)
- [ ] **Outcome-Oriented:** 「作業（Output）」だけでなく「達成すべき状態（Outcome）」がゴールとして定義されているか？
- [ ] **Domain-Centric:** システム内部の技術用語だけでなく、ドメイン（ビジネス）の用語で意図が語られているか？
- [ ] **Context Integrity:** SSOT（ADR/Context）との整合性が取れているか？

#### B. TECHNICAL_DESIGNER Perspective (明確性と厳密性)
- [ ] **Clarity & Rigor:** 「適宜」「いい感じに」等の曖昧な表現が排除されているか？ 解釈の余地はないか？
- [ ] **Implementation-Aware:** 実装者が迷わないレベルまで、参照ファイルや手順が具体的か？
- [ ] **Visual/Explicit:** 複雑なロジックが必要な場合、図解（Mermaid）や具体的なコード例への言及があるか？

#### C. BACKENDCODER Perspective (実装と品質)
- [ ] **Simplicity (YAGNI):** タスクの範囲が必要最小限に絞られているか？（過剰な要件が含まれていないか）
- [ ] **Test-Driven / Verifiable:** 完了条件（DoD）に「テストのパス」や「具体的な観測結果」が含まれているか？
- [ ] **Negative Constraints:** 「やってはいけないこと（破壊してはいけない既存機能）」が明記されているか？

### 3. 指摘と是正 (Finding & Correction)
- **Action:**
  - 各指摘に対し、**具体的な改善案**をセットで提示する。
  - **Rule:** 「もっとわかりやすく」は指摘ではない。「〇〇という記述を△△に変更せよ」と提案する。
  - 修正が容易な場合はその場でファイルを修正し、重大な不備がある場合は `issue-drafting` のやり直しを要求する。

## アウトプット (Output)
レビュー結果レポート。

```markdown
## Issue Review Result: [Issue Title]
- **Status:** [Pass / Fixed / Failed]
- **Value Alignment:**
  - [OK] Domain-Centric: 決済用語が正しく使われている。
  - [Fixed] Simplicity: 不要なリファクタリング指示を削除しました。
- **Improvements:**
  - [Fixed] 完了条件が曖昧だったため、「テストケースXがパスすること」と具体化しました。
```