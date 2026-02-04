---
name: recording-changes
description: Replaces the work of recording changes to the repository following specific conventions. Typical use cases (1) Batch staging and committing product code and tests after implementation, (2) Reliably recording design artifacts such as architectural diagrams or ADR drafts, (3) Managing automatic fix and retry processes when pre-commit hooks fail.
---

# 変更の記録 (Recording Changes)

作業の区切りで変更内容をリポジトリに記録する。
`references/branching-strategy.md` の規約を厳守し、意味のある履歴を作成する。

## 役割定義 (Role Definition)

あなたは **Gatekeeper** です。
すべての変更をステージングし、規約に沿ったメッセージでコミットします。Pre-commit フック等のエラーに対しても適切に対処し、リポジトリの整合性を守ります。

## ワークフロー

```markdown
Commit Progress:
- [ ] 1. Branch Validation (ブランチ確認)
- [ ] 2. Staging & Commit (記録実行)
- [ ] 3. Error Recovery (エラー対応)
```

### 1. Branch Validation (ブランチ確認)
- **Action:**
  - 作業ブランチにいることを確認する。
  - **警告:** Base Branch (`main`/`master`) への直接コミットは禁止。その場合は `switching-feature-branch` を実行してブランチを移ること。

### 2. Staging & Commit (記録実行)
- **Action:**
  - 変更をステージングしてコミットする。
  - `run_shell_command{command: "git add . && git commit -m \"<type>: <subject>\""}`
  - **Type/Subject:** `references/branching-strategy.md` の規約に厳密に従う。

### 3. Error Recovery (エラー対応)
- **Action:**
  - コミット時に pre-commit フックなどでエラーが発生した場合、内容を確認して修正を行う。
  - 修正後、再度 Step 2 を実行する。

## 完了条件 (Definition of Done)

- 変更がローカルリポジトリにコミットされていること。
- コミットメッセージが規約（`<type>: <subject>`）に準拠していること。
- Pre-commit フック等を通過していること。
