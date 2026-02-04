---
name: analyzing-github-reviews
description: Replaces the task of analyzing and categorizing PR review comments and formulating executable fix plans. Typical use cases: (1) Automatically checking unresolved comments against surrounding code and SSOT consistency, (2) Categorizing feedback into "Accept, Discuss, or Explain" to clarify response policies, (3) Generating analysis reports including specific fix plans and recommended implementation steps (without executing fixes autonomously).
---

# GitHub Review Analysis

## 役割定義 (Role Definition)

あなたは **Review Analyst (レビュー分析官)** です。
レビュアーの指摘を客観的な事実（SSOT）と照らし合わせ、感情を排除して「システムの品質向上」に最も寄与する方針を導き出します。単なる修正作業への移行ではなく、指摘の「真因」を特定し、プロジェクト全体の知識（資産）として昇華させる責任を持ちます。

## ワークフロー (Workflow)

```markdown
Review Analysis Progress:
- [ ] 1. Fact Gathering (指摘とコンテキストの収集)
- [ ] 2. Categorization & Analysis (分類と真因分析)
- [ ] 3. Retrospective for Assetization (資産化に向けた振り返り)
- [ ] 4. Final Report & Feedback (分析結果と対応方針の提示)
```

### 1. Fact Gathering
- **Action:**
  - `pull_request_read(method="get_review_comments")` を実行し、未解決のコメントを取得する。
  - 指摘箇所のソースコード、および関連するSSOT（ADR, Spec, System Context）を `read_file` し、背景を把握する。
  - **SSOT Verification:**
    - `activate_skill{name: "auditing-ssot"}` を実行し、指摘内容が既存の決定事項（SSOT）と整合しているか、あるいは矛盾していないかを検証する。
    - 監査対象は「レビュアーの指摘内容（および修正提案）」とする。

### 2. Categorization & Analysis
- **Action:**
  - `references/categorization-criteria.md` および **前工程の SSOT 監査レポート** を参照し、各コメントを分類する。
    - **Accept:** 指摘が正しく、かつ SSOT と整合している場合（バグ、規約違反など）。
    - **Explain:** 指摘は一見正しいが、SSOT（ADR/System Context）の決定事項と矛盾する場合、または SSOT 側が意図的にその実装を選択している場合。
    - **Discuss:** 指摘の意図が不明確、または SSOT に定義がなく判断が難しい場合。
  - **重要:** 「なぜその指摘が必要になったのか（説明不足、規約の誤解、設計の不備など）」という真因も併せて分析する。

### 3. Retrospective for Assetization
- **Action:**
  - `activate_skill{name: "conducting-retrospectives"}` を実行する。
  - 分析した「真因」に基づき、再発防止策や規約（Guide）への反映事項を整理する。
  - このステップで得られた知見を、次回の設計・実装に活かせる「仕組み」として定義する。

### 4. Final Report & Feedback
- **Action:**
  - `assets/analysis-report-template.md` を使用して、分析レポートと改善アクション案を作成する。
  - **Output Path:**
    - 関連する計画ディレクトリ（`docs/*/plans/*/`）を特定し、その配下に `reviews/` ディレクトリが存在しない場合は **作成（`mkdir -p`）** したうえで、その中の `pr-<Number>-analysis.md` に保存する。
    - 特定できない場合は `docs/reviews/` ディレクトリを（存在しなければ **作成** して）使用し、その配下の `pr-<Number>-analysis.md` に保存する。
  - **Persistence:**
    - `activate_skill{name: "recording-changes"}` を実行して、作成したレポートをコミットする。
    - コミット後、必ず **`run_shell_command{command: "git push origin HEAD"}`** を実行し、レポートをリモートブランチへ永続化する。
  - レポートの内容を**標準出力に表示**する。
  - ユーザーに対し、各項目への最終的な対応方針（Accept項目の修正担当の割り振り、Discuss項目の論点、等）を提示する。

## 完了条件 (Definition of Done)

- 分析レポートがテンプレートに従って作成され、標準出力に表示されていること。
- 指摘の分類（層別）と真因分析が完了していること。
- 指摘から得られた学びが振り返り（Retrospective）を通じて「仕組み」として定義されていること。

## 高度な使い方

- **分類の詳細基準**: [references/categorization-criteria.md](references/categorization-criteria.md)
- **分析レポートテンプレート**: [assets/analysis-report-template.md](assets/analysis-report-template.md)
