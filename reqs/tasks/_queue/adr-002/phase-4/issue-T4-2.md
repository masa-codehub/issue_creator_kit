---
title: "資産の同期と不要スクリプトの削除"
labels:
  - "task"
  - "P2"
  - "SYSTEM_ARCHITECT"
roadmap: "reqs/roadmap/active/roadmap-adr002-document-approval-flow.md"
task_id: "T4-2"
depends_on:
  - "issue-T4-1.md"
status: "Draft"
---
# {{title}}

## 親Issue / ロードマップ (Context)
- **Roadmap**: {{roadmap}}
- **Task ID**: {{task_id}}

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 
    - `src/issue_creator_kit/` がフラットなスクリプト構成で、IO処理（ファイル操作、Git、GitHub API）とロジックが混在している。
    - 不要な `visualize_app.egg-info/` や古いエージェント定義が残存している。
    - アセット構造がプロジェクト構成を反映していない。
- **To-be (あるべき姿)**: 
    - 「関心の分離」を重視した **Clean Architecture Lite** 構成へ再編され、テスト容易性が向上している。
    - 不要ファイルが完全に削除され、アセットは `project_template/` 形式で再構成されている。

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `src/issue_creator_kit/utils.py`
- [ ] `src/issue_creator_kit/scripts/`
- [ ] `src/issue_creator_kit/cli.py`

## 3. 実装手順 (Implementation Steps)

### 3.1. ディレクトリ再編とコード移動 (Restructuring)
- [ ] **ディレクトリ作成**: `domain/`, `usecase/`, `infrastructure/` を `src/issue_creator_kit/` 下に作成。
- [ ] **コード分解・移動**:
    - **Domain**: `domain/models.py` (ドキュメントやメタデータのデータ構造定義)
    - **Infrastructure**: `infrastructure/filesystem.py`, `infrastructure/git_adapter.py`, `infrastructure/github_adapter.py` (IOの実装)
    - **Usecase**: `usecase/approval.py`, `usecase/creation.py` (IOに依存しない純粋なロジック)
- [ ] **CLI修正**: 新構造に合わせて `cli.py` のインポートと依存注入 (DI) を修正。

### 3.2. 不要ファイル削除とアセット再編 (Cleanup & Assets)
- [ ] **削除**: `visualize_app.egg-info/`, `.gemini/AGENTS/old/`, `messages/`, `reqs/template/` (空の場合)。
- [ ] **アセット構造化**: `src/issue_creator_kit/assets/project_template/` 配下に `.github/`, `reqs/`, `docs/` のディレクトリ構成を維持してテンプレートを配置。
- [ ] **CLI修正**: `init` コマンドが `project_template/` を再帰的にコピーするように修正。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ**: `feature/phase-4-cleanup`
- **作業ブランチ**: `feature/T4-2-arch-and-cleanup`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **静的解析**: `ruff` / `mypy` でインポートエラーや型エラーが出ないこと。
- [ ] **動作確認**: `issue-kit init` で新構造のアセットが正しく展開されること。