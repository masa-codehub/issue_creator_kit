---
name: managing-pull-requests
description: Manages the lifecycle of GitHub Pull Requests, including creation with conventional titles and bodies, synchronization with base branches, and conflict resolution. Ensures changes are properly reviewed and verified before merging.
---

# GitHub Pull Request Management

このスキルは、GitHubのプルリクエスト作成からマージ前の検証までのプロセスを管理します。

## ワークフロー (Workflow)

以下の手順に従って、標準化されたプルリクエストを作成・管理します。

```markdown
PR作成進捗:
- [ ] 1. 変更のコミット確認 (Ensure Committed)
- [ ] 2. 既存PRの確認 (Check Duplicates)
- [ ] 3. Baseブランチとの同期 (Sync & Rebase)
- [ ] 4. PRの作成 (Create PR using Template)
- [ ] 5. 自動レビュー依頼 (Request Auto-Review)
```

### 1. 変更のコミット確認 (Ensure Committed)

**目的:** PRに含めるべき変更が確実に記録されていることを保証する。

- **Action:**
  - `git status` で未コミットの変更がないか確認する。
  - ある場合は `activate_skill{name: "recording-changes"}` を呼び出してコミットする。

### 2. 既存PRの確認 (Check Duplicates)

**目的:** 重複したPRの作成を防ぐ。

- **Action:**
  - `list_pull_requests` を使用して、同じ目的のPRが既に存在しないか確認する。

### 3. Baseブランチとの同期 (Sync & Rebase)

**目的:** 統合時のコンフリクトを未然に防ぎ、履歴を綺麗に保つ。

- **Action:**
  - マージ先となる `base` ブランチ（通常は `main`）の最新状態を取り込む。
  - `run_shell_command{command: "git pull --rebase origin <base>"}`
  - **コンフリクト時:** 手動で解消し、解決してから次へ進む。

### 4. PRの作成 (Create PR)

**目的:** レビュワーに必要な情報を過不足なく伝えるPRを作成する。

- **Action:**
  - `assets/pull-request-template.md` を参照し、`title` と `body` を作成する。
  - **Labeling (重要):** 
    - 関連するIssueがある場合、そのIssueに付与されている `gemini:*` ラベル（例: `gemini:arch`, `gemini:spec`, `gemini:tdd`）を確認する。
    - **必ず** 同じラベルをPRにも適用する（後続の自動化ワークフロー `gemini-reviewer` のトリガーとなるため）。
    - Issueがない場合は、変更内容（アーキテクチャ、仕様、実装）に応じて適切なラベルを推測して付与する。
  - **必須:** `head` (作業ブランチ) と `base` (マージ先) を明示的に指定する。
  - `create_pull_request` ツールを呼び出す。

### 5. 自動レビュー依頼 (Request Auto-Review)

**目的:** GitHub Copilot による初期レビューを受け、品質を向上させる。

- **Action:**
  - 作成したPR番号を使用して `request_copilot_review` ツールを呼び出す。
  - エラー（非対応リポジトリ等）が出た場合は無視してよい。

## 完了条件 (Definition of Done)

- PRが作成され、テンプレートの項目が適切に埋められていること。
- GitHub Copilot へのレビューリクエストが（可能であれば）送信されていること。
