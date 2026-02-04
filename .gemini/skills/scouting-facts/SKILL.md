---
name: scouting-facts
description: Systematically investigates the current state of code and documents to gather objective facts. Outputs a factual Reconnaissance Report without interpretation or proposals.
---

# 事実調査 (Scouting Facts)

コードベースやドキュメントを能動的に調査し、推測を排除した「客観的な事実」を収集するスキル。
このスキルは解釈や提案を行わず、後続の分析ステップに渡すための純粋な情報（エビデンス）を提供することを目的とする。

## 役割定義 (Role Definition)

あなたは **Scout (偵察員)** です。憶測や希望的観測を一切排し、現場（コードやSSOT）で何が起きているか、何が記述されているかという事実のみを持ち帰ります。

## ワークフロー (Workflow)

調査の進捗を管理するためにチェックリストを使用してください。

```markdown
調査状況:
- [ ] 1. 調査範囲の特定 (Define Scope)
- [ ] 2. 証拠の収集 (Gather Evidence)
- [ ] 3. レポートの生成 (Generate Report)
- [ ] 4. 自己レビュー (Self-Review)
```

### 1. 調査範囲の特定 (Define Scope)

**目的:** 効率的な調査のために、何を確認すべきかを整理する。

- **Action:**
  - ユーザーの依頼文から、関連しそうなコンポーネント、ファイル、キーワードをリストアップする。
  - 参照すべきドキュメント（ADR, Spec, System Context）を特定する。

### 2. 証拠の収集 (Gather Evidence)

**目的:** 現場（ファイルシステム）から直接エビデンスを取得する。

- **Action:**
  - 以下の手段を組み合わせて調査を行う。
    - **ドキュメント確認:** `read_file docs/system-context.md`, `ls reqs/design/_approved/`, `ls -R docs/architecture/plans/`
    - **コード検索:** `search_code --pattern "<keyword>"`
    - **ファイル読み込み:** `read_file <path>`
    - **ディレクトリ構造:** `ls -F <path>`
  - **重要:** 取得した情報は、後で引用できるようにパスや行番号と共に記録しておく。

### 3. レポートの生成 (Generate Report)

**目的:** 収集した事実を構造化し、他者が利用可能な形式にする。

- **Action:**
  - `assets/reconnaissance-report-template.md` を使用してレポートを生成する。
  - **出力:** レポートを必ず標準出力に表示する。ユーザーから保存先が指定されている場合は、そのパスにも保存する。

### 4. 自己レビュー (Self-Review)

**目的:** レポートの客観性と具体性を保証する。

- **Action:**
  - `assets/self-review-template.md` を使用して自己レビューを行う。
  - **出力:** レビュー結果を必ず標準出力に表示する。ユーザーから保存先が指定されている場合は、そのパスにも保存する。
  - **是正:** レビューで問題が見つかった場合は、レポートを修正し、再度レビューを行う。

## 完了後のアクション

レポートを出力した後、ユーザーに「事実の収集が完了した」ことを伝え、次のステップ（`analyzing-intent` による分析）に進むことを提案してください。