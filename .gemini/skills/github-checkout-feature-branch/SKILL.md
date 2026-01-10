---
name: github-checkout-feature-branch
description: Ensure work is done on a feature branch. Uses the strategy defined in github-branch-strategy to determine branches and switch/create them.
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
