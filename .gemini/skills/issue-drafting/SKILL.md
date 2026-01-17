---
name: issue-drafting
description: Creates detailed issue drafts for task delegation. Ensures clarity and executability by integrating SMART goal setting into each issue and structuring tasks into verifiable Red/Green/Verify steps.
---

# Issue Drafting (Objective-Oriented Task Architecture)

他者（エージェントまたは人間）に委譲するタスクの「指示書（Issue Draft）」を作成するスキル。
単なる作業リストではなく、`objective-setting` に基づくSMART目標をIssueの核に据え、達成すべき成果を「検証可能な構造」で記述する。

## 役割 (Role)
**Task Architect (タスク設計者)**
「何をやるか」だけでなく、「なぜ、どうなれば成功か」を定義する。
SMART目標をIssue本文に焼き付け、作業者の迷いをゼロにする。

## 前提 (Prerequisites)
- タスクの目的、スコープ、参照すべきドキュメント（SSOT/Common Definitions）が明確であること。
- `reqs/tasks/template/issue-draft.md` が存在すること。

## 手順 (Procedure)

### 1. 目標定義と構造化 (Objective & Structuring)
**目的:** タスクの成功基準を明確にし、検証可能な手順へ分解する。

- **Action:**
  - `activate_skill{name: "objective-setting"}` (思考プロセスとして使用)
  - 依頼内容から、**このIssueが達成すべきSMART目標**を定義する。
    - *Specific:* どのファイルをどう変えるか？
    - *Measurable:* 完了をどう数値や事実で確認するか？
  - 目標を達成するための論理的な手順を構築する。
    1.  **Context (Red):** 理想（SSOT）と現状（As-Is）の乖離。
    2.  **Action (Green):** 乖離を埋めるための具体的アクション。
    3.  **Verify (Check):** 成果物の客観的検証方法。

### 2. コンテンツ記述 (Drafting)
**目的:** テンプレートを埋め、SMART目標を軸にした指示書を作成する。

- **Action:**
  - `reqs/tasks/template/issue-draft.md` を読み込み、以下の基準で記述する。

  - **Title:** `[Domain] Verb + Object`
  
  - **Goal (Added Section or Header):**
    - Step 1で定義した **SMART目標** を明記する。
    - *Example:* 「ADR-005に基づき、決済完了後のメール送信シーケンスを、リトライフローを含めて完全に可視化する。」

  - **Context (Background & SSOT):**
    - **Why:** 共通定義書（Common Definitions）へのリンクと、その中のどの部分に関連するかを記述。
    - **Gap:** 現状の不足点（Red）。

  - **Requirements (Execution Steps):**
    - 作業手順を `Red/Green/Verify` の構造で記述する。

  - **Acceptance Criteria (Definition of Done):**
    - 完了条件を「目標が達成された事実」として記述する。

### 3. ファイル生成と自己検証 (Finalization & Check)
**目的:** 生成物の品質を保証する。

- **Action:**
  - 作成した内容をファイル（`reqs/tasks/drafts/*.md`）に書き出す。
  - 以下のチェックリストで自己検証を行う。

- **Self-Correction Checklist:**
  - [ ] **Objective-Oriented:** Issueの冒頭に「達成すべき目標」が明記されているか？
  - [ ] **No Ambiguity:** 逃げ言葉（「適宜」等）を排除できているか？
  - [ ] **Atomic:** 1つのIssueで扱う目標は1つに絞られているか？
  - [ ] **Verifiable:** 誰がやっても同じ「完了」の判定ができるか？

## アウトプット (Output)
- `reqs/tasks/drafts/` 配下に生成された、目標設定済みのMarkdownファイル。