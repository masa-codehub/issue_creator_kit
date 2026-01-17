---
name: issue-drafting
description: Creates detailed issue drafts by strictly filling the 'issue-draft.md' template. Defines explicit rules for every section, integrating Red/Green/Verify verifiable task structure, and enforces quality review.
---

# Issue Drafting (Template-Driven & Verifiable)

`reqs/tasks/template/issue-draft.md` を、一切の抜け漏れ・無理・無駄なく埋めるためのスキル。
テンプレートの各セクションに対して「書くべきこと」と「書いてはいけないこと」を厳密に定義し、`Red/Green/Verify` の思考プロセスを用いてエージェントが自律的に実行可能な「完全な指示書」を生成する。

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
  - **title:** `[Domain] Action + Object` (例: `[Payment] Update Sequence for Async Retry`)
  - **labels:** `task` および担当ロール（例: `TECHNICAL_DESIGNER`）を設定。
  - **roadmap:** **Common Definitions Doc のパス** を指定する（例: `docs/architecture/plans/20240101-payment.md`）。
  - **task_id:** Planning段階で振られた一意なID（例: `T-01`）。
  - **depends_on:** 依存するIssueのファイル名（なければ空配列 `[]`）。
  - **status:** `Draft` (固定)

### 2. 目的と背景 (1. Goal & Context)

**目的:** タスクの「Why」と「What」を定義し、作業者の目的意識を統一する。

- **書くべきこと:**
  - **As-is (現状):** 現状のドキュメントやコードにおける具体的な「不足」や「誤り」。(Red)
  - **To-be (あるべき姿):** このタスク完了後に実現されているべき状態（SMART目標）。
  - **Design Evidence:** 根拠となる ADR 番号、および Common Definitions Doc へのリンク。
- **書いてはいけないこと:**
  - 曖昧な願望（「いい感じにする」「使いやすくする」）。
  - タスクの範囲外にある壮大なビジョン。

### 3. 参照資料・入力ファイル (2. Input Context)

**目的:** 作業開始時に必要な情報を過不足なく渡す。

- **書くべきこと:**
  - Common Definitions Doc のパス。
  - 編集対象となる既存のアーキテクチャ図のパス。
  - 参照すべきソースコードや既存の仕様書。
- **書いてはいけないこと:**
  - 存在しないファイルパス。
  - 今回のタスクに全く関係のない資料（ノイズになるため）。

### 4. 実装手順と制約 (3. Implementation Steps & Constraints)

**目的:** 迷いのない「実行手順（How）」を定義する。

- **3.1. 負の制約 (Negative Constraints):**
  - **書くべきこと:** 「編集してはいけないファイル」「依存してはいけないモジュール」「使用してはいけない記法」。
  - **例:** 「`docs/system-context.md` は参照のみとし、変更してはならない。」
- **3.2. 実装手順 (Changes):**
  - **書くべきこと:** (Green)
    - 作成・編集するファイルパス。
    - 使用するテンプレート（`docs/template/arch-*.md`）。
    - 記述すべき具体的な内容（クラス名、シーケンスの流れ、使用する用語）。
  - **書いてはいけないこと:**
    - 「適宜実装する」「よしなに計らう」等の丸投げ。
- **3.3. 構成変更 (Configuration):**
  - ファイルの削除や移動がある場合のみ記述。なければ「なし」と明記。

### 5. ブランチ戦略と検証手順 (Sections 4 & 5)

**目的:** 作業場所の固定と、客観的な完了判定。

- **4. Branching Strategy:**
  - **Base Branch:** 統合用ブランチ名（例: `feature/arch-update-xxx`）。
  - **Feature Branch:** `feature/task-{{task_id}}-{{title_slug}}` の形式に従ったブランチ名。
- **5. Verification & DoD:**
  - **書くべきこと:** (Verify)
    - **観測される挙動:** 生成されたファイルが存在し、内容が空でないこと。
    - **ファイル状態:** Mermaidの構文エラーがないこと（プレビューで確認可能であること）。
    - **整合性:** Common Definitions Doc で定義された用語（Stub）が正確に使われていること。
  - **書いてはいけないこと:**
    - 「品質が高いこと」「わかりやすいこと」などの主観的評価。

### 6. 品質レビュー (Final Quality Gate)

- **Action:**
  - `activate_skill{name: "issue-review"}`
  - 作成したIssue Draftをレビューし、品質基準（Ambiguity-Free, Atomic, Verifiable）に達しているか確認する。
  - 指摘があれば直ちに修正し、完璧な状態にする。

## アウトプット (Output)

- `reqs/tasks/drafts/` 配下に生成され、レビューをパスしたMarkdownファイル。
