---
name: issue-drafting
description: Creates detailed issue drafts for task delegation. Ensures clarity, completeness, and executability by structuring tasks into verifiable Red/Green/Verify steps, strictly adhering to templates and SSOT.
---

# Issue Drafting (Verifiable Task Architecture)

他者（エージェントまたは人間）に委譲するタスクの「指示書（Issue Draft）」を作成するスキル。
`task-management` の哲学を継承し、指示内容を「検証可能なRed/Green/Verifyサイクル」として構造化することで、曖昧さを完全に排除する。

## 役割 (Role)
**Task Architect (タスク設計者)**
「何をやるか」だけでなく、「どうなれば完了か」を定義する。
文脈（Context）と制約（Constraint）を明記し、作業者の迷いをゼロにする。

## 前提 (Prerequisites)
- タスクの目的、スコープ、参照すべきドキュメント（SSOT/Common Definitions）が明確であること。
- `reqs/tasks/template/issue-draft.md` が存在すること。

## 手順 (Procedure)

### 1. 構成検討 (Structuring)
**目的:** タスクを「検証可能な最小単位」に分解し、論理的な手順を構築する。

- **Action:**
  - 依頼内容を分析し、以下の3要素を明確にする。
    1.  **Context (Red):** 現状の何が問題で、SSOT（ADR/Plan）とどう乖離しているか？
    2.  **Action (Green):** その乖離を埋めるために、具体的に「どのファイルを」「どう操作」すべきか？
    3.  **Verify (Check):** 作業完了を客観的に判断するための基準は何か？

### 2. コンテンツ記述 (Drafting)
**目的:** テンプレートを埋め、実行可能な指示書を作成する。

- **Action:**
  - `reqs/tasks/template/issue-draft.md` を読み込み、以下の基準で記述する。

  - **Title:**
    - `[Domain/Subject] Verb + Object` (例: `[Payment] Update Sequence Diagram for Async Retry`)
  
  - **Context (Background & SSOT):**
    - **Why:** タスクの背景（ADR-xxxにより決定された非同期処理を可視化するため）。
    - **Reference:** **Common Definitions Doc** へのリンクを「必須」で含める。
    - **Current State:** 現状（As-Is）の不足点を指摘する（例: `seq-payment.md` が未作成である）。

  - **Requirements (Execution Steps):**
    - 作業手順を `Red/Green/Verify` の構造を意識して記述する。
    - *Example:*
      1. **Setup:** `arch-behavior.md` テンプレートをコピーして `docs/architecture/seq-payment.md` を作成する。
      2. **Drafting:** Common Definitions の用語定義（`BillingWorker`等）に従い、Mermaidでシーケンスを記述する。
      3. **Refining:** `arch-refactoring` の基準に従い、Noteで例外処理を補足する。

  - **Acceptance Criteria (Definition of Done):**
    - 完了条件を具体的かつ機械的に検証可能なレベルで記述する。
    - *Example:*
      - [ ] `docs/architecture/seq-payment.md` が存在し、Mermaid構文エラーがないこと。
      - [ ] `BillingWorker` コンテナが登場していること。
      - [ ] Redis接続エラー時のリトライ処理が記述されていること。

### 3. ファイル生成と自己検証 (Finalization & Check)
**目的:** 生成物の品質を保証する。

- **Action:**
  - 作成した内容をファイル（`reqs/tasks/drafts/*.md`）に書き出す。
  - 以下のチェックリストで自己検証を行う。

- **Self-Correction Checklist:**
  - [ ] **No Ambiguity:** 「いい感じに」「適宜」という言葉を使っていないか？
  - [ ] **Link Validity:** 参照しているドキュメント（Common Definitions, ADR）へのパスは正しいか？
  - [ ] **Atomic:** 1つのIssueで扱う範囲は適切か？（原則 1 Issue = 1 File）
  - [ ] **Verifiable:** Acceptance Criteria はYes/Noで判定できるか？

### 4. 品質レビュー (Final Quality Gate)
- **Action:**
  - `activate_skill{name: "issue-review"}`
  - 作成したIssue Draftをレビューし、品質基準に達しているか確認する。
  - 指摘があれば直ちに修正し、完璧な状態にする。

## アウトプット (Output)
- `reqs/tasks/drafts/` 配下に生成されたMarkdownファイル。
