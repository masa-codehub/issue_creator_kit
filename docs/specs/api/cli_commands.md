# CLI Interface Specification

## 1. 概要

`issue-kit` CLI のエントリポイント、コマンド構成、および実行環境に関する仕様を定義する。
本 CLI は Clean Architecture Lite の Interface 層として機能し、ユーザー入力を解析して UseCase 層へ処理を委譲する責務を持つ。

## 2. 共通仕様

### 2.1. 終了コード (Exit Codes)

| コード | 意味             | 説明                                                                |
| :----- | :--------------- | :------------------------------------------------------------------ |
| `0`    | Success          | 全ての処理が正常に完了した。                                        |
| `1`    | Error            | 一般的なエラー（環境変数不足、ランタイムエラー等）。                |
| `2`    | Validation Error | コマンドライン引数の形式不正（argparse によるバリデーション失敗）。 |

### 2.2. 共通環境変数

| 変数名              | 必須 | 説明                                                                      |
| :------------------ | :--- | :------------------------------------------------------------------------ |
| `GITHUB_TOKEN`      | Yes  | GitHub API を操作するための Personal Access Token。                       |
| `GITHUB_REPOSITORY` | No   | 操作対象のリポジトリ (`owner/repo`)。引数で指定されない場合に使用される。 |

## 3. コマンド定義

### 3.1. `process`

物理ファイルシステムを走査し、未処理のタスクおよび ADR を処理するメインコマンド。

- **概要**: `reqs/` ディレクトリ配下を走査し、依存関係を考慮してタスクを処理する。
- **オプション引数**:
  - `--root`: 走査対象のベースディレクトリ（デフォルト: `reqs/`）
  - `--dry-run`: 実際のアクション（GitHub 起票等）を行わず、検出されたファイルと実行順序を表示する。
- **UseCase への委譲**: `ScannerService` (または各 Domain Service) を介して処理を実行する。

### 3.2. `visualize`

タスクの依存関係を Mermaid 形式で可視化するコマンド。

- **概要**: 現在のタスク依存関係を DAG として構築し、Mermaid 記法のテキストを出力する。
- **オプション引数**:
  - `--root`: 走査対象のベースディレクトリ（デフォルト: `reqs/`）
- **UseCase への委譲**: `Visualizer.to_mermaid()` を呼び出す。

### 3.3. `process-diff` (Deprecated)

仮想キュー（Virtual Queue）の自動起票を実行するレガシーコマンド。

- **概要**: **本 ADR-008 に基づく新 CLI リリース以降、非推奨（Deprecated）とする。** 後方互換性のためにエントリポイントは維持するが、実行時には常にエラー終了し、新コマンドへの移行を促すメッセージを表示する。
- **振る舞い**: 実行時に "This command is deprecated and no longer supported. Use `ick process` instead." を表示し、終了コード `1` で終了する。

### 3.4. その他のサブコマンド

既存の `cli.py` に実装されている以下のコマンドは、必要に応じて利用される。

- `init`: プロジェクトテンプレートの展開。

## 4. バリデーションとエラーハンドリング

### 4.1. 認証チェック

- 実行時に環境変数 `GITHUB_TOKEN` が設定されていない場合、以下のメッセージを標準エラー出力に表示し、終了コード `1` で終了すること。
  `Error: GitHub token is required.`

### 4.2. 引数バリデーション

- 必要な引数が不足している場合、または引数の型不正（`--adr-id`等）がある場合、エラーメッセージを表示し終了コード `2` で終了する。

## 5. 検証手順 (TDD Criteria)

### 5.1. 環境変数の検証

- **Given**: `GITHUB_TOKEN` が未設定の状態。
- **When**: `issue-kit process-diff` を実行。
- **Then**: 終了コードが `1` であること。

### 5.2. 引数解析とデフォルト値の検証

- **Given**: 引数なしで `process-diff` を実行（必須引数不足）。
- **Then**: 終了コードが `2` であり、ヘルプメッセージが表示されること。
- **Given**: `process-diff --before HEAD~1 --after HEAD` を実行。
- **Then**: `archive_dir` 引数にデフォルト値 `reqs/tasks/_archive/` が渡されること。
- **Given**: `--adr-id adr-007` を指定して `process-diff` を実行。
- **Then**: `IssueCreationUseCase` に `adr_id="adr-007"` がフィルタ引数として渡されること。
- **Given**: `--adr-id invalid-format` を指定して `process-diff` を実行。
- **Then**: 終了コードが `2` であり、バリデーションエラーメッセージが表示されること。

### 5.3. ロジックの分離

- CLI 層の関数が、UseCase のインスタンスを生成し、そのメソッドを呼び出すだけの構造になっていること。
- CLI 層で直接 `requests` や `subprocess` を呼び出していないこと（Adapter を介して UseCase に渡すのは可）。

## 6. 移行に関する注意 (Migration Notes)

- **ADR-003 からの移行**: 以前の仕様では `reqs/tasks/archive/` を使用していたが、ADR-007 以降は `reqs/tasks/_archive/` (アンダースコア付き) がデフォルトとなる。既存のワークフローやスクリプトでパスをハードコードしている場合は、新仕様への追従が必要である。
- **再帰探索の導入**: `process-diff` は `reqs/tasks/` 配下を再帰的に走査するようになったため、ディレクトリ階層によらずタスクファイルを配置可能である。
