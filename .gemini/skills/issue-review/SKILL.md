---
name: issue-review
description: Audits created issue drafts for quality, clarity, and template compliance. Ensures each issue is actionable, atomic, and verifiable before it is finalized for execution.
---

# Issue Review

作成された `reqs/tasks/drafts/*.md` を厳格にレビューし、品質基準（Ambiguity-Free, Atomic, Verifiable）に達しているか監査するスキル。

## 役割 (Role)

**Quality Auditor (品質監査人)**
作業担当者の視点に立ち、「この指示だけで迷わず完遂できるか？」を徹底的に追求する。

## 手順 (Procedure)

### 1. 形式監査 (Template Audit)

- **Checklist:**
  - [ ] フロントマターの `roadmap` と `task_id` が正しく埋まっているか？
  - [ ] セクション 1 ～ 6 が全て存在し、テンプレートの構造を保っているか？
  - [ ] `{{title}}` などのプレースホルダーが残っていないか？

### 2. 記述内容の精査 (Content Scrutiny)

- **Checklist:**
  - [ ] **Ambiguity Check:** 「いい感じに」「適宜」「等」という曖昧な表現が含まれていないか？
  - [ ] **Context Check:** なぜこの作業が必要か（Why）が ADR/Plan へのリンクと共に示されているか？
  - [ ] **Constraint Check:** 「やってはいけないこと（負の制約）」が明記されているか？
  - [ ] **Feasibility Check:** この作業量は、エージェントが1ターンまたは1PRで完遂できる範囲（Atomic）か？

### 3. 検証可能性の審査 (Verifiability Scrutiny)

- **Checklist:**
  - [ ] **DoD Check:** 完了条件が具体的で、Yes/Noで判定できるか？
  - [ ] **Link Check:** 参照資料へのリンクパスは有効か？

### 4. 指摘と是正 (Finding & Correction)

- **Action:**
  - 各指摘に対し、**具体的な改善案**をセットで提示する。
  - 修正が容易な場合はその場でファイルを修正し、重大な不備がある場合は `issue-drafting` のやり直しを要求する。

## アウトプット (Output)

レビュー結果レポート。

```markdown
## Issue Review Result: [Issue Title]

- **Status:** [Pass / Fixed / Failed]
- **Improvements:**
  - [Fixed] 「適宜」という表現を排除し、具体的な手順に置き換えました。
  - [Fixed] 共通定義書へのリンク切れを修正しました。
```
