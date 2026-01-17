---
name: issue-drafting
description: Creates detailed issue drafts for task delegation. Ensures clarity, completeness, and executability by filling standardized templates with specific requirements, scope, and acceptance criteria.
---

# Issue Drafting

他者（エージェントまたは人間）に委譲するタスクの「指示書（Issue Draft）」を作成するスキル。
曖昧な指示を排除し、受け取った側が質問なしで作業を開始できるレベルの具体性を担保する。

## 役割 (Role)

**Task Architect (タスク設計者)**
「何をやるか」だけでなく、「どうなれば完了か」を定義する。
文脈（Context）と制約（Constraint）を明記し、作業者の迷いをゼロにする。

## 前提 (Prerequisites)

- タスクの目的、スコープ、参照すべきドキュメント（SSOT/Common Definitions）が明確であること。

## 手順 (Procedure)

### 1. テンプレート準備 (Preparation)

- **Action:**
  - 標準テンプレート `reqs/tasks/template/issue-draft.md` を読み込む。
  - 作成するIssueのファイル名（例: `reqs/tasks/drafts/arch-update-payment.md`）を決定する。

### 2. コンテンツ記述 (Drafting)

- **Action:**
  - テンプレートの各セクションを、以下の基準で埋める。
  - **Title:**
    - 具体的な動詞を使う（"Fix", "Create", "Update"）。
    - 対象（Subject）を明確にする。
    - _Example:_ `[Payment] Update Sequence Diagram for Async Retry Logic`

  - **Context (Background):**
    - 「なぜこのタスクが必要か」をADRや上位設計へのリンクと共に記述する。
    - **Vital:** 共通定義書（Common Definitions）がある場合は、必ずリンクと遵守指示を入れる。

  - **Requirements (What to do):**
    - 「いい感じに」禁止。具体的なアクション（「ファイルXを作成し、Yのロジックを記述せよ」）を書く。
    - 編集対象のファイルパスや、参考にするコード箇所を明記する。

  - **Acceptance Criteria (Definition of Done):**
    - 完了を客観的に判断できる条件を箇条書きにする。
    - _Example:_
      - [ ] `docs/architecture/seq-payment.md` が作成されていること。
      - [ ] メッセージフローに `BillingWorker` が含まれていること。
      - [ ] `docs/architecture/plans/xxx.md` の用語定義に従っていること。

### 3. ファイル生成 (Finalization)

- **Action:**
  - `write_file` を使用して、作成した内容をファイルに書き出す。
  - 保存先: `reqs/tasks/drafts/`

## 品質チェックリスト (Self-Correction)

- [ ] リンクは有効か？（相対パスが正しいか）
- [ ] 誰が読んでも同じ解釈になるか？（主語が抜けていないか）
- [ ] タスクの粒度は適切か？（1ターン/1PRで完結するか）
