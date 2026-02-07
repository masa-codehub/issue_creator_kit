# CLI Interface Specification

## 1. 概要

`issue-kit` CLI のエントリポイント、コマンド構成、および実行環境に関する仕様を定義する。
本 CLI は Clean Architecture Lite の Interface 層として機能し、ユーザー入力を解析して UseCase 層へ処理を委譲する責務を持つ。

## 2. 共通仕様

### 2.1. 終了コード (Exit Codes)

| コード | 意味    | 説明                                                                     |
| :----- | :------ | :----------------------------------------------------------------------- |
| `0`    | Success | 全ての処理が正常に完了した。                                             |
| `1`    | Error   | 一般的なエラー（バリデーション失敗、環境変数不足、ランタイムエラー等）。 |

### 2.2. 共通環境変数

| 変数名              | 必須 | 説明                                                                      |
| :------------------ | :--- | :------------------------------------------------------------------------ |
| `GITHUB_MCP_PAT`    | Yes  | GitHub API を操作するための Personal Access Token。                       |
| `GITHUB_REPOSITORY` | No   | 操作対象のリポジトリ (`owner/repo`)。引数で指定されない場合に使用される。 |

## 3. コマンド定義

### 3.1. `run-workflow`

承認フローのオーケストレーションを実行するメインコマンド。

- **概要**: Inbox ディレクトリから Approved ディレクトリへのドキュメント移動、Issue 起票、Git コミットまでを一連のワークフローとして実行する。
- **必須引数**:
  - `--branch`: 変更をプッシュする先のブランチ名。
- **オプション引数**:
  - `--inbox-dir`: 承認待ちドキュメントのディレクトリ（デフォルト: `reqs/design/_inbox`）
  - `--approved-dir`: 承認済みドキュメントのディレクトリ（デフォルト: `reqs/design/_approved`）
- **UseCase への委譲**: `WorkflowUseCase.run()` を呼び出す。

### 3.2. `process-diff`

仮想キュー（Virtual Queue）の自動起票を実行するコマンド。

- **概要**: `reqs/tasks/` ディレクトリ配下を再帰的に探索し、新しく追加された未採番のタスクファイルを検知して GitHub Issue を起票する。起票されたファイルは `--archive-dir` へ移動される。
- **必須引数**:
  - `--before`: 比較元（Base）の Git Ref。
  - `--after`: 比較先（Head）の Git Ref。
- **オプション引数**:
  - `--archive-dir`: タスクアーカイブの移動先ディレクトリ（デフォルト: `reqs/tasks/_archive/`）
  - `--adr-id`: 指定した ADR ID に紐づくタスクのみを処理対象とするフィルタリングオプション。
    - **形式**: `adr-` に続けて 3 桁のゼロパディング済み数字を指定する（例: `adr-001`, `adr-007`）。
    - **バリデーション**: 上記形式に一致しない値が指定された場合、本 CLI はバリデーションエラーとして扱い、終了コード `1` を返すこと。
  - `--roadmap`: ロードマップファイルのパス。
  - `--use-pr`: 直接 Push せず、メタデータ同期用の PR を作成するフラグ。
  - `--base-branch`: メタデータ同期 PR のマージ先ブランチ（デフォルト: `main`）。
- **UseCase への委譲**: `IssueCreationUseCase.create_issues_from_virtual_queue(adr_id=...)` を呼び出す。

### 3.3. `process-merge`

フェーズ連鎖（Auto-PR）を実行するコマンド。

- **概要**: マージされた PR の本文を解析し、次フェーズのタスクを Draft から Archive へプロモーションする PR を作成する。
- **オプション引数**:
  - `--pr-body`: PR の本文（文字列）。
  - `--event-path`: GitHub Event JSON ファイルのパス。
  - `--archive-dir`: アーカイブディレクトリ（デフォルト: `reqs/tasks/_archive/`）
- **UseCase への委譲**: `WorkflowUseCase.promote_from_merged_pr()` を呼び出す。

### 3.4. その他のサブコマンド

既存の `cli.py` に実装されている以下のコマンドは、必要に応じて利用される。

- `init`: プロジェクトテンプレートの展開。
- `approve`: 単一ファイルの承認。
- `approve-all`: 全ファイルのバッチ承認。

## 4. バリデーションとエラーハンドリング

### 4.1. 認証チェック

- 実行時に環境変数 `GITHUB_MCP_PAT` が設定されていない場合、以下のメッセージを標準エラー出力に表示し、終了コード `1` で終了すること。
  `Error: GitHub token is required via GITHUB_MCP_PAT environment variable.`

### 4.2. 引数バリデーション

- 必要な引数（`run-workflow` におけるブランチ名など、UseCase が要求するもの）が不足している場合、エラーメッセージを表示し終了コード `1` で終了する。

## 5. 検証手順 (TDD Criteria)

### 5.1. 環境変数の検証

- **Given**: `GITHUB_MCP_PAT` が未設定の状態。
- **When**: `issue-kit run-workflow` を実行。
- **Then**: 終了コードが `1` であること。

### 5.2. 引数解析とデフォルト値の検証

- **Given**: 引数なしで `process-diff` を実行（必須引数不足）。
- **Then**: 終了コードが `1` であり、ヘルプメッセージが表示されること。
- **Given**: `process-diff --before HEAD~1 --after HEAD` を実行。
- **Then**: `archive_dir` 引数にデフォルト値 `reqs/tasks/_archive/` が渡されること。
- **Given**: `--adr-id adr-007` を指定して `process-diff` を実行。
- **Then**: `IssueCreationUseCase` に `adr_id="adr-007"` がフィルタ引数として渡されること。
- **Given**: `--adr-id invalid-format` を指定して `process-diff` を実行。
- **Then**: 終了コードが `1` であり、バリデーションエラーメッセージが表示されること。

### 5.3. ロジックの分離

- CLI 層の関数（`run_workflow` 等）が、`WorkflowUseCase` のインスタンスを生成し、その `run` メソッドを呼び出すだけの構造になっていること。
- CLI 層で直接 `requests` や `subprocess` を呼び出していないこと（Adapter を介して UseCase に渡すのは可）。

## 6. 移行に関する注意 (Migration Notes)

- **ADR-003 からの移行**: 以前の仕様では `reqs/tasks/archive/` を使用していたが、ADR-007 以降は `reqs/tasks/_archive/` (アンダースコア付き) がデフォルトとなる。既存のワークフローやスクリプトでパスをハードコードしている場合は、新仕様への追従が必要である。
- **再帰探索の導入**: `process-diff` は `reqs/tasks/` 配下を再帰的に走査するようになったため、ディレクトリ階層によらずタスクファイルを配置可能である。
