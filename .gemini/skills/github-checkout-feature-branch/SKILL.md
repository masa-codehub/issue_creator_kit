---
name: github-checkout-feature-branch
description: 常に適切な作業ブランチ上で開発が進められるよう、ブランチの切り替えと同期を保証する作業を代替します。代表的なユースケース：(1) 最新の Base Branch を取り込んだ上での作業ブランチの新規作成。(2) 既存のブランチへの安全な復帰とリモート変更の同期。(3) タイムスタンプ付きの自動ブランチ生成による作業場所の即時確保。
---

# GitHub Checkout Feature Branch

`github-branch-strategy` で規定されたロジックに従い、適切な作業ブランチ（Feature Branch）に切り替える。

## 手順

1. **現状確認:**
   現在のブランチを確認する。
   `run_shell_command{command: "git branch --show-current"}`

2. **Base Branch の準備:**
   `github-branch-strategy` の定義に従い、Base Branch（指定がなければ `main` 等）を最新化する。
   `run_shell_command{command: "git checkout <base_branch> && git pull --rebase origin <base_branch>"}`

3. **Feature Branch への切り替え:**
   `github-branch-strategy` の定義に従い、Feature Branch に切り替える。

   - **Feature Branch 名の指定がある場合:**
     （新規作成を試み、失敗したら既存ブランチに切り替えて Base Branch を取り込む）
     `run_shell_command{command: "git checkout -b <feature_branch> <base_branch> || (git checkout <feature_branch> && git merge <base_branch>)"}`

   - **Feature Branch 名の指定がない場合:**
     （自動生成して新規作成する）
     `run_shell_command{command: "git checkout -b feature/gemini-update-$(date +%Y%m%d-%H%M%S) <base_branch>"}`
