---
name: architecture-audit
description: Performs final quality checks and formalizes deliverables. Used for (1) verifying overall system integrity and SSOT compliance, (2) creating high-quality pull requests with audit trails, and (3) conducting retrospectives to improve future architecture cycles.
---

# Architecture Audit

このスキルは、個別の図の整合性チェックを超えて、システム全体としてのSSOT準拠とプロジェクト基準への適合を最終確認することを目的とします。

## 役割定義 (Role Definition)
あなたは **Quality Auditor** です。客観的なデータ（Gap分析結果、Linter結果）と設計原則に基づき、成果物をプロフェッショナルなレベルで納品します。

## 前提 (Prerequisites)
- `architecture-refactoring` が完了していること（自己検証チェックリストがAll Greenであること）。
- `github-pull-request`, `github-commit` スキルが利用可能であること。

## 手順 (Procedure)

### 1. 最終監査 (Full Audit)
- **Action:**
  - **SSOT整合性:** `ssot-verification` を実行し、更新されたアーキテクチャ図が上位の設計方針（ADR等）と矛盾していないか確認する。
    `activate_skill{name: "ssot-verification"}`
  - **リンク切れチェック:** ドキュメント内のリンクが有効であることを確認する（手動またはツール使用）。

### 2. 成果物の定着
- **Action:**
  - `git status` と `git diff` で意図しない変更が含まれていないか確認する。
  - `github-commit` スキルを用い、規約に沿ったメッセージでコミットする。
    `activate_skill{name: "github-commit"}`
  - `github-pull-request` スキルを用い、テンプレートに従ってPRを作成する。
    `activate_skill{name: "github-pull-request"}`

### 3. プロジェクト進行のクローズ (Closing Protocol)
- **Action:**
  - `retrospective` スキルを活用し、YWT または KPT で振り返りを行う。
    `activate_skill{name: "retrospective"}`
  - `add_issue_comment` で成果と、振り返りから得られた「次の方策」を報告する。
  - 全てのタスクが完了したことを確認し、`todo-management` スキルで `.gemini/todo.md` を完了状態（またはアーカイブ）にする。
    `activate_skill{name: "todo-management"}`

## 監査チェックリスト (Final Audit Checklist)
- [ ] `architecture-refactoring` のチェックリストを全てパスしているか？
- [ ] 変更内容が当初の計画（Gap Analysis）と合致しているか？
- [ ] PRのテンプレートは適切に埋められているか？
- [ ] 今回の更新で判明した「コード側の課題」がIssue化されているか？

## 完了条件 (Definition of Done)
- プルリクエストが作成され、レビュアーが指定されていること。
- 振り返りが完了し、活動報告が Issue にコメントされていること。