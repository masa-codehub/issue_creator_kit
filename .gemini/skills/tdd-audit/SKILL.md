---
name: tdd-audit
description: Performs final quality checks and formalizes deliverables. Used for (1) verifying overall system integrity and SSOT compliance, (2) creating high-quality pull requests with audit trails, and (3) conducting retrospectives to improve future TDD cycles.
---

# TDD Audit

このスキルは、個別のテストパスを超えて、システム全体としての整合性とプロジェクト基準への準拠を最終確認することを目的とします。

## 役割定義 (Role Definition)
あなたは **Quality Auditor** です。客観的なデータ（テスト結果、解析ログ）と設計原則に基づき、成果物をプロフェッショナルなレベルで納品します。

## 前提 (Prerequisites)
- `tdd-cycle` が完了していること。
- `github-pull-request`, `github-commit`, `python-verification` スキルが利用可能であること。

## 手順 (Procedure)

### 1. 最終監査 (Full Audit)
- **Action:**
  - 全テスト実行: `pytest -v`
  - 静的解析: `python-verification` スキルを実行。
    `activate_skill{name: "python-verification"}`
  - **SSOT整合性:** `ssot-verification` を再実行し、実装が当初の ADR や仕様書から逸脱していないか最終確認する。
    `activate_skill{name: "ssot-verification"}`

### 2. 成果物の定着
- **Action:**
  - `git status` と `git diff` で意図しない変更（デバッグコード、不要なコメント）が含まれていないか確認する。
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
- [ ] 全てのテストがパスしているか？
- [ ] Linter/Formatter/Type Check の警告はゼロか？
- [ ] ドメイン層に技術的詳細（外部ライブラリ、DB、FW等）が混入していないか？
- [ ] Issue の受け入れ基準 (Acceptance Criteria) を全て満たしているか？

## 完了条件 (Definition of Done)
- プルリクエストが作成され、レビュアー（Copilot）が指定されていること。
- 振り返りが完了し、活動報告が Issue にコメントされていること。
