---
name: issue-drafting
description: Creates detailed issue drafts by filling the standardized 'issue-draft.md' template. Ensures metadata correctness and verifiable task descriptions based on objective-oriented analysis.
---

# Issue Drafting (Template-Driven Task Architecture)

`reqs/tasks/template/issue-draft.md` を正しく、かつ高品質に埋めるためのスキル。
`objective-setting` の成果をテンプレートの各セクションへ正確にマッピングし、エージェントが自律的に実行可能な「完全な指示書」を生成する。

## 役割 (Role)
**Task Architect (タスク設計者)**
テンプレートの「枠」を、具体的で矛盾のない「指示」で埋める。
メタデータ（Frontmatter）の整合性と、本文（Content）の検証可能性を両立させる。

## 前提 (Prerequisites)
- `reqs/tasks/template/issue-draft.md` を読み込んでいること。
- 参照すべき Common Definitions Doc や ADR のパスが判明していること。

## 手順 (Procedure)

### 1. メタデータ定義 (Frontmatter Setup)
**目的:** システム連携に必要な属性情報を正しく設定する。

- **Action:**
  - 以下の項目を、`arch-planning` の戦略に基づいて決定する。
  - **title:** `[Domain] Action + Object`
  - **labels:** 担当ロール（例: `TECHNICAL_DESIGNER`）と優先度を設定。
  - **roadmap / task_id:** 関連するロードマップと WBS ID を紐付ける。
  - **depends_on:** 依存する他のIssueがあればファイル名をリストアップ。

### 2. 目的・背景・入力の記述 (Sections 1 & 2)
**目的:** タスクの「Why」と「前提知識」を定義する。

- **Action:**
  - **1. 目的と背景:**
    - **As-is (現状):** SSOTと現在のコード/図の具体的な乖離を記述（Red）。
    - **To-be (あるべき姿):** このタスク完了後の理想状態（Goal）。
    - **Design Evidence:** 根拠となる ADR のセクションや Common Definitions へのリンクを明記。
  - **2. 参照資料・入力ファイル:**
    - 作業開始時に `read_file` すべきファイルを具体的にリストアップする。

### 3. 実装手順と制約の記述 (Section 3)
**目的:** 迷いのない「実行手順（How）」を定義する。

- **Action:**
  - **3.1. 負の制約:** 「触ってはいけないファイル」や「今回のスコープ外」を明示し、余計な変更を防ぐ。
  - **3.2. 実装手順:**
    - `Action (Green)` に相当する具体的な操作を記述する。
    - 使用すべきテンプレート（`docs/template/arch-*.md` 等）を明示する。
  - **3.3. 構成変更:** 不要なファイルの削除や設定ファイルの変更があれば記述。

### 4. ブランチ戦略と検証手順の記述 (Sections 4 & 5)
**目的:** プロセスの整合性と「完了（DoD）」を定義する。

- **Action:**
  - **4. ブランチ戦略:** ロードマップに基づくベースブランチと、一意な作業ブランチ名を定義。
  - **5. 検証手順:**
    - `Verify (Check)` に相当する客観的な確認方法を記述。
    - アーキテクチャ図の場合、Mermaidの構文チェックや、Common Definitions との用語一致を必須項目とする。

### 5. 自己検証 (Final Check)
- **Action:**
  - 生成したMarkdownがテンプレートの構造を壊していないか。
  - `{{title}}` などの変数が適切に置換（または具体的な値で上書き）されているか。
  - **Zero Ambiguity:** 指示内容に「適宜」「いい感じに」が含まれていないか。

## アウトプット (Output)
- `reqs/tasks/drafts/` 配下に、テンプレートを完全に埋めた状態で出力されたMarkdownファイル。
