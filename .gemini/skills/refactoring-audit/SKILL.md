---
name: refactoring-audit
description: Performs final quality checks for refactoring tasks. Verifies that code smells are removed, architecture is compliant, and no regression occurred.
---

# Refactoring Audit

このスキルは、リファクタリング後のコードが、振る舞いを変えずに内部品質のみを向上させたことを最終確認し、成果物を定着させることを目的とします。

## 役割定義 (Role Definition)
あなたは **Quality Auditor** です。客観的なデータ（テスト結果、依存関係グラフ、解析ログ）に基づき、リファクタリングの成功を証明します。

## 前提 (Prerequisites)
- `tdd-refactoring` (Execution Phase) が完了していること。
- `github-pull-request`, `github-commit`, `python-verification` スキルが利用可能であること。

## 手順 (Procedure)

### 1. 最終監査 (Full Audit)
- **Action:**
  - **回帰テスト:** `pytest -v` を実行し、**全てのテストがパスすること**を確認する。失敗した場合、リファクタリングは失敗とみなされる。
  - **静的解析:** `python-verification` スキルを実行。
    `activate_skill{name: "python-verification"}`
  - **成果確認:**
    - 当初特定した「コードの匂い」や「アーキテクチャ違反」が解消されたか確認する。
    - `ssot-verification` を実行し、新しい構造がSSOTに準拠しているか確認する。
      `activate_skill{name: "ssot-verification"}`

### 2. 成果物の定着
- **Action:**
  - `git status` と `git diff` で意図しない変更（デバッグコード、不要なコメント）が含まれていないか確認する。
  - `github-commit` スキルを用い、規約に沿ったメッセージでコミットする。
    - Msg: `refactor: [What] to improve [Why] based on [SSOT]`
    `activate_skill{name: "github-commit"}`
  - `github-pull-request` スキルを用い、テンプレートに従ってPRを作成する。
    - Bodyには「Before/After」や「改善された指標」を明記する。
    `activate_skill{name: "github-pull-request"}`

### 3. プロジェクト進行のクローズ (Closing Protocol)
- **Action:**
  - `retrospective` スキルを活用し、YWT または KPT で振り返りを行う。
    `activate_skill{name: "retrospective"}`
  - `add_issue_comment` で成果と、振り返りから得られた「次の方策」を報告する。
  - 全てのタスクが完了したことを確認し、`todo-management` スキルで `.gemini/todo.md` を完了状態にする。
    `activate_skill{name: "todo-management"}`

## 監査チェックリスト (Final Audit Checklist)
- [ ] 全てのテストがパスしているか？（機能等価性）
- [ ] 外部からの振る舞い（APIレスポンス等）が変わっていないか？
- [ ] Linter/Formatter/Type Check の警告はゼロか？
- [ ] コードの重複は排除されたか？
- [ ] 依存関係（循環参照など）は整理されたか？

## 完了条件 (Definition of Done)
- プルリクエストが作成され、レビュアー（Copilot）が指定されていること。
- 振り返りが完了し、活動報告が Issue にコメントされていること。
