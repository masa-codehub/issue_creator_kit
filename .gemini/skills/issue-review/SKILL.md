---
name: issue-review
description: Audits created issue drafts for quality, clarity, and template compliance. Ensures alignment with SSOT by mandating context loading via active-reconnaissance and executing ssot-verification checks.
---

# Issue Review (Value & Reality Driven Audit)

作成された `reqs/tasks/drafts/*.md` を厳格にレビューするスキル。
形式的な品質だけでなく、**実際に読み込んだSSOT（ADR/Context）との整合性**を検証し、物理的な誤り（リンク切れ等）も排除する。

## 役割 (Role)
**Quality Auditor (品質監査人)**
作業担当者の視点に立ち、「この指示だけで迷わず完遂できるか？」を問うとともに、アーキテクトの視点で「これは正しい方向への一歩か？」を問う。
比較対象を持たずにレビューを行ってはならない。

## 手順 (Procedure)

### 1. 比較対象のロード (Load Context)
**目的:** レビューに必要な「正解データ」を脳内に展開する。

- **Action:**
  - レビュー対象のIssueドラフトを読み込む。
  - `activate_skill{name: "active-reconnaissance"}` を実行し、Issue内で参照されている **ADR**, **Common Definitions Doc**, および **`docs/system-context.md`** の内容を正確に把握する。
  - **Rule:** これを実行せずに「整合性OK」と判断することは許されない。

### 2. 形式と物理的整合性の監査 (Formal & Physical Audit)
**目的:** 実行不可能なエラーを排除する。

- **Checklist:**
    - [ ] **Meta Integrity:** `roadmap`, `task_id`, `labels` が正しく埋まっているか？
    - [ ] **Link Validation:** リンクされているファイルパス（`../../docs/...`等）は実在するか？（または今回の計画で作られる予定か？）
    - [ ] **Structure:** セクション 1 ～ 6 が全て存在し、テンプレート構造を維持しているか？
    - [ ] **No Placeholders:** `{{title}}` 等の変数が残っていないか？

### 3. 価値観とSSOT整合性の監査 (Value & SSOT Audit)
読み込んだドキュメントと比較し、各エージェントの行動規範に合致しているか精査する。

- **Action:**
  - `activate_skill{name: "ssot-verification"}` を実行し、Issueの内容がSSOT（ADR/Context）と矛盾していないか、概念レベルでの整合性を検証する。

- **Perspective Checklist:**
    - [ ] **Outcome-Oriented:** 「作業（Output）」だけでなく「達成すべき状態（Outcome）」がゴールとして定義されているか？
    - [ ] **Domain-Centric:** システム内部の技術用語だけでなく、ドメイン（ビジネス）の用語で意図が語られているか？
    - [ ] **Clarity & Rigor:** 「適宜」「いい感じに」等の曖昧な表現が排除されているか？
    - [ ] **Simplicity (YAGNI):** タスクの範囲が必要最小限に絞られているか？
    - [ ] **Negative Constraints:** 「やってはいけないこと」が明記されているか？

### 4. 指摘と是正 (Finding & Correction)
- **Action:**
  - 各指摘に対し、**具体的な改善案**をセットで提示する。
  - **Rule:** 「もっとわかりやすく」は指摘ではない。「〇〇という記述を△△に変更せよ」と提案する。
  - 修正が容易な場合はその場でファイルを修正し、重大な不備がある場合は `issue-drafting` のやり直しを要求する。

## アウトプット (Output)
レビュー結果レポート。

```markdown
## Issue Review Result: [Issue Title]
- **Status:** [Pass / Fixed / Failed]
- **Context Loaded:** (active-reconnaissance result summary)
- **SSOT Verification:** (ssot-verification result summary)
- **Improvements:**
  - [Fixed] リンク切れを修正しました。
```