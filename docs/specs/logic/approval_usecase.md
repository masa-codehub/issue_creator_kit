# Approval UseCase Specification

## 1. 概要
ドキュメントの承認プロセス（メタデータ更新、ファイル移動、GitHub Issue 起票）を管理するビジネスロジックの仕様を定義する。
本 UseCase は、単一ファイルの承認処理 (`process_single_file`) と、ディレクトリ内の全ファイルを対象とした一括処理 (`process_all_files`) の 2 つの主要な機能を持つ。

## 2. 関連ドキュメント
- ADR: `reqs/design/_archive/adr-002-document-approval-flow.md`
- Architecture (Sequence): `docs/architecture/arch-behavior-approval-flow.md`
- Data Model Spec: `docs/specs/data/document_model.md`
- Infrastructure Adapter Spec: `docs/specs/components/infra_adapters.md`

## 3. ApprovalUseCase

### 3.1. `process_single_file(file_path: Path, approved_dir: Path) -> None`

単一のドキュメントファイルを承認状態に移行させる。

#### 実行フロー
1.  **ドキュメントの読み込み**: `FileSystemAdapter.read_document(file_path)` を呼び出す。ステップ2でメタデータを更新する前に、この初期状態を `original_doc` として保持する。
2.  **メタデータの更新 (メモリ内)**:
    - 読み込んだドキュメントオブジェクトのメタデータを以下のように更新し、一時的にメモリ内で保持する（この段階ではファイルシステムへの書き込みは行わない）。
        - `status`: `承認済み`
        - `date`: 現在の日付 (YYYY-MM-DD)
    - 補足: キーは `document_model.md` の定義に従い、全て小文字に正規化されたキー (`status`, `date`) を使用する。
3.  **ファイルの移動とメタデータの反映**:
    - `moved_path = FileSystemAdapter.safe_move_file(file_path, approved_dir)` を呼び出し、承認済みディレクトリへ移動する。戻り値として移動後のパス `moved_path` を受け取る。
    - ステップ2で更新したメタデータ内容を、`FileSystemAdapter.update_metadata(moved_path, ...)` を用いて移動後のファイルに反映する。
4.  **GitHub Issue の起票 (Try-Except ブロック)**:
    - **Issue タイトル**: ドキュメントのタイトル（メタデータの `title`。存在しない場合はファイル名 `file_path.stem`）を使用する。
        - 注: 日本語キー `タイトル` が存在する場合、`document_model.md` の正規化/エイリアスルールに従い `title` として解決される想定。
    - **Issue 本文**: ファイルへの相対パスと、本文の冒頭 200 文字を要約として含める。
    - **Issue ラベル**: ドキュメントのメタデータから `labels` を読み取り、配列として使用する。存在しない場合は `["documentation", "approved"]` をデフォルト値として用いる。
        - 注: 日本語キー `ラベル` も同様に `labels` として解決される想定。
    - `GitHubAdapter.find_or_create_issue(title, body, labels)` を呼び出す。
    - 成功時: `FileSystemAdapter.update_metadata(moved_path, {"issue_id": f"#{issue_number}"})` を呼び出し、ファイルに Issue ID を追記する。
5.  **エラーハンドリングとロールバック**:
    - **GitHub 操作失敗時**:
        - 移動したファイル (`moved_path`) を元のパス (`file_path`) に戻す (`safe_move_file(overwrite=True)`)。
        - ファイルのメタデータを `original_doc` の状態に上書きして戻す（メタデータ更新のロールバック）。
        - 例外を再送出する。
        - **ADR-002 対応注記**: ADR-002 で指摘された「ロールバック時のメタデータ不整合」問題は、`original_doc` を用いた完全な状態復元により解決されている。
    - **メタデータ追記 (Issue ID) 失敗時**:
        - **重要**: ここではロールバック（ファイル移動の取り消し）を行わない。
        - エラー内容・対象ファイルパス・起票済み Issue 番号を障害ログに記録する。
        - 対象ファイルと同名の一時マーカーファイル（例: `<ファイル名>.issue_metadata_failed`）を `_approved` 配下に作成し、「メタデータ追記失敗」状態であることを明示する。
        - 例外を上位 (`WorkflowUseCase`) に伝播させる。

### 3.2. `process_all_files(inbox_dir: Path, approved_dir: Path) -> bool`

Inbox ディレクトリ内の全ファイルをスキャンし、承認処理を実行する。

#### 実行フロー
1.  **ファイル一覧の取得**: `FileSystemAdapter.list_files(inbox_dir)` を呼び出す。
2.  **ループ実行**:
    - 各ファイルに対し `process_single_file(file_path, approved_dir)` を呼び出す。
3.  **例外ハンドリング**:
    - いずれかのファイルで例外が発生した場合、即座に中断し例外を上位（WorkflowUseCase）へ伝播させる (Fail-fast)。
4.  **戻り値**: 1つ以上のファイルが正常に処理された場合は `True`、そうでなければ `False` を返す。

## 4. 異常系フロー (Compensating Transactions)

GitHub API の一時的なエラー等で起票に失敗した場合、不整合を防ぐために以下の補償トランザクションを実行する。

| 失敗フェーズ | 補償アクション (Rollback) | 最終状態 |
| :--- | :--- | :--- |
| GitHub Issue 起票 | 1. ファイルを `approved_dir` から `inbox_dir` へ戻す。 <br> 2. メタデータを `original_doc` の状態に戻す。 | ファイルは `_inbox` に残り、ステータスも更新されない。 |
| メタデータ追記 (Issue ID) | 1. 障害ログへの記録。<br> 2. マーカーファイル（`*.issue_metadata_failed`）の作成。<br> 3. 例外送出（処理中断）。 | ファイルは `_approved` にあり、`issue_id` が欠落しているが、マーカーファイルにより手動復旧対象として識別可能。 |

### 4.1. メタデータ追記 (Issue ID) 失敗時の手動介入手順
「メタデータ追記 (Issue ID)」フェーズで例外が発生した場合、ファイル移動や承認ステータス更新は完了しているが、ファイル内に Issue 番号が記録されていない状態となる。この場合、以下の手順で整合性を確保する。
1. 障害ログおよび `_approved` 配下のマーカーファイル（例: `<ファイル名>.issue_metadata_failed`）を確認し、対象ファイルと対応する GitHub Issue 番号を特定する。
2. 対象ファイルのメタデータに `issue_id: #<番号>` を手動で追記する。
3. 手動追記が完了したら、対応するマーカーファイルを削除し、障害ログ上のステータスを「解消済み」に更新する。


## 5. 検証手順 (TDD Criteria)

### 5.1. 正常系の検証
- `status` が `承認済み` に更新され、ファイルが `_approved/` に移動されていること。
- GitHub Issue が起票され、その番号がファイルに `#123` の形式（キー: `Issue`）で記録されていること。

### 5.2. 異常系の検証
- GitHub API 呼び出しが失敗した際、ファイルが `_inbox/` に戻っていること。
- GitHub API 呼び出しが失敗した際、メタデータのステータスが `承認済み` のままになっていないこと。
