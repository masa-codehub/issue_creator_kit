---
name: github-branch-strategy
description: Defines standard branch management logic. Typical use cases include (1) Creating a new feature branch from main to start work, (2) Switching to an existing feature branch to continue work or review, and (3) Moving local commits from main to a new feature branch for PR creation.
---

# GitHub Branch Strategy

プロジェクトにおけるブランチの定義と運用ルール（Git Flow）を規定する。
他のGit関連スキル（checkout, commit, pull-request）はこの戦略に従う。

## ブランチの定義 (Definitions)

### 1. Base Branch (統合元/マージ先)

- **役割:** 開発の起点となり、最終的な統合先となるブランチ。
- **決定ロジック:**
  1. **明示的な指定:** ユーザーが指定した場合はそのブランチ。
  2. **デフォルト:** 指定がない場合、`main` または `master`。

### 2. Feature Branch (作業ブランチ)

- **役割:** 特定のタスク、機能追加、バグ修正を行うための短命なブランチ。
- **決定ロジック:**
  1. **明示的な指定:** ユーザーが指定した場合はそのブランチ。
  2. **自動生成:** 指定がない場合、以下の命名規則で新規作成する。
     - 規則: `<type>/<subject>`
     - **Type の例:**
       - `feat`: 新機能の追加
       - `fix`: バグ修正
       - `docs`: ドキュメントの変更
       - `refactor`: リファクタリング
       - `chore`: その他保守
     - **Subject の例:** (英語推奨、ハイフン繋ぎ)
       - `add-user-registration`
       - `fix-login-auth-bug`
       - `update-readme`
     - **例:** `feat/add-user-registration`

## 運用ルール (Rules)

1. **最新化 (Sync):**
   作業開始前には必ず `Base Branch` の最新状態をリモートから取り込む。
   `git pull --rebase origin <base_branch>`

2. **統合 (Integration):**
   既にある `Feature Branch` で作業を再開する場合も、`Base Branch` の最新変更を取り込む（マージまたはリベース）。

3. **保護 (Protection):**
   `Base Branch` (main/master) への直接コミットは禁止。必ず `Feature Branch` を介する。
