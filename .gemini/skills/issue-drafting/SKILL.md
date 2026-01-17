---
name: issue-drafting
description: Creates detailed issue drafts by strictly filling the 'issue-draft.md' template. Defines explicit rules for every section to ensure zero ambiguity, no redundancy, and perfect alignment with the architectural plan.
---

# Issue Drafting (Template-Driven Task Architecture)

`reqs/tasks/template/issue-draft.md` を、一切の抜け漏れ・無理・無駄なく埋めるためのスキル。
テンプレートの各セクションに対して「書くべきこと」と「書いてはいけないこと」を厳密に定義し、エージェントが自律的に実行可能な「完全な指示書」を生成する。

## 役割 (Role)
**Task Architect (タスク設計者)**
テンプレートの「枠」を、具体的で矛盾のない「指示」で埋める。
メタデータ（Frontmatter）の整合性と、本文（Content）の検証可能性を両立させる。

## 前提 (Prerequisites)
- `reqs/tasks/template/issue-draft.md` を読み込んでいること。
- 参照すべき **Common Definitions Doc (Plan)** が存在し、パスが判明していること。

## 手順 (Procedure)

### 1. メタデータ定義 (Frontmatter)
**目的:** システム連携に必要な属性情報を定義する。

- **Action:**
  - **title:** `[Domain] Action + Object`
  - **labels:** `task` および担当ロール（例: `TECHNICAL_DESIGNER`）を設定。
  - **roadmap:** Common Definitions Doc のパスを指定。
  - **task_id:** 振られた一意なID（例: `T-01`）。
  - **depends_on:** 依存するIssueのファイル名（なければ `[]`）。
  - **status:** `Draft` (固定)

### 2. 目的と背景 (1. Goal & Context)
- **書くべきこと:**
  - **As-is (現状):** 具体的な「不足」や「誤り」。
  - **To-be (あるべき姿):** 完了後に実現されているべき状態（SMART目標）。
  - **Design Evidence:** 根拠となる ADR や Common Definitions Doc へのリンク。
- **書いてはいけないこと:** 曖昧な願望（「いい感じにする」等）。

### 3. 参照資料・入力ファイル (2. Input Context)
- **書くべきこと:** 共通定義書、編集対象の図、参照すべきソースコード等の具体的なパス。
- **書いてはいけないこと:** 存在しないパス、無関係な資料。

### 4. 実装手順と制約 (3. Implementation Steps & Constraints)
- **3.1. 負の制約:** 「編集してはいけないファイル」「使用してはいけない記法」等を明記。
- **3.2. 実装手順:** 作成・編集するファイルパス、使用するテンプレート、記述すべき具体的な内容をステップバイステップで記述。
- **3.3. 構成変更:** ファイルの削除・移動があれば記述。なければ「なし」。

### 5. ブランチ戦略と検証手順 (Sections 4 & 5)
- **4. Branching Strategy:** ベースブランチと、一意な作業ブランチ名を定義。
- **5. Verification & DoD:** Yes/Noで判定可能な客観的判定基準（Mermaid構文エラーなし、用語一致等）を記述。

### 6. 品質レビュー (Final Quality Gate)
- **Action:**
  - `activate_skill{name: "issue-review"}`
  - 作成したIssue Draftをレビューし、品質基準に達しているか確認する。
  - 指摘があれば直ちに修正し、完璧な状態にする。

## アウトプット (Output)
- `reqs/tasks/drafts/` 配下に生成され、レビューをパスしたMarkdownファイル。