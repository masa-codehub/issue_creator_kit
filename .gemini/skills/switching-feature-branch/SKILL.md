---
name: switching-feature-branch
description: Replaces the task of ensuring development proceeds on the correct branch by switching and synchronizing branches. Typical use cases (1) Creating a new feature branch after incorporating the latest Base Branch changes, (2) Safely returning to existing branches and synchronizing remote changes, (3) Instantly securing a workspace via automatic branch generation with timestamps.
---

# Feature Branch切り替え (Switching Feature Branch)

`references/branching-strategy.md` で規定されたロジックに従い、適切な作業ブランチ（Feature Branch）に切り替える。

## 役割定義 (Role Definition)

あなたは **Context Manager** です。
開発者が正しいブランチで作業を開始し、常に最新のコードベースを反映した状態で開発を進められるよう制御します。

## ワークフロー

```markdown
Checkout Progress:
- [ ] 1. Status Check (現状確認)
- [ ] 2. Base Branch Sync (親ブランチ最新化)
- [ ] 3. Branch Transition (作業ブランチへ移行)
```

### 1. Status Check (現状確認)
- **Action:**
  - 現在のブランチを確認する。
  - `run_shell_command{command: "git branch --show-current"}`

### 2. Base Branch Sync (親ブランチ最新化)
- **Action:**
  - `references/branching-strategy.md` に従い、Base Branch（指定がなければ `main` 等）を最新化する。
  - `run_shell_command{command: "git checkout <base_branch> && git pull --rebase origin <base_branch>"}`

### 3. Branch Transition (作業ブランチへ移行)
- **Action:**
  - **Feature Branch 名の指定がある場合:**
    - 新規作成を試み、失敗した場合は既存ブランチに切り替えて Base Branch を取り込む。
    - `run_shell_command{command: "git checkout -b <feature_branch> <base_branch> || (git checkout <feature_branch> && git merge <base_branch>)"}`
  - **Feature Branch 名の指定がない場合:**
    - 命名規則に従い、タイムスタンプ等を含むブランチを自動生成して新規作成する。
    - `run_shell_command{command: "git checkout -b feature/gemini-update-$(date +%Y%m%d-%H%M%S) <base_branch>"}`

## 完了条件 (Definition of Done)

- 指定（または自動生成）された Feature Branch に切り替わっていること。
- Base Branch の最新内容（同期済み）が反映されていること。
