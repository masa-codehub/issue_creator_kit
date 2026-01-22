# Handover: Spec to TDD (Approval Flow)

## 概要
詳細設計フェーズ（Spec Creation）から実装フェーズ（TDD Creation）への申し送り事項をまとめる。
実装担当者は、`docs/specs/` 配下の仕様書に加え、本ドキュメントの指針に従って実装を進めること。

## 1. 実装の優先順位と依存関係
以下の順序で実装することを推奨する（Slicing Strategyに基づく）。

1.  **Domain (`src/issue_creator_kit/domain/`)**:
    - `Document`, `Metadata` クラス。
    - 外部依存が一切ないため、純粋な単体テストでロジックを確定させる。
    - 特に `Metadata` のキー正規化（小文字扱い）ロジックは、後続の全工程に関わるため念入りにテストすること。

2.  **Infrastructure (`src/issue_creator_kit/infrastructure/`)**:
    - `FileSystemAdapter`, `GitHubAdapter`, `GitAdapter`。
    - `unittest.mock` を活用し、実際のAPIを叩かずに異常系（404, 500エラー等）をシミュレートするテストを作成すること。
    - `GitHubAdapter` の `find_or_create_issue` は、重複起票防止の要であるため、検索クエリの生成ロジックを確実に検証すること。

3.  **UseCase (`src/issue_creator_kit/usecase/`)**:
    - `ApprovalUseCase`。
    - ここでは `Infrastructure` の実体を使わず、Mock Adapter を注入してテストする。
    - **最重要検証項目**: ロールバック処理。途中でエラーが発生した際、ファイルシステムの状態（パス、メタデータ）が「処理前」と完全に同じ状態に戻ることを保証するテストケースを書くこと。

4.  **CLI (`src/issue_creator_kit/cli.py`)**:
    - `run-workflow` コマンド。
    - 引数パースと環境変数のチェックのみを責務とする。

## 2. 特に注意すべき仕様・エッジケース

### 2.1. メタデータの揺らぎ
- ユーザーが書く Markdown のメタデータキーは、`Status`, `status`, `STATUS` など表記揺れがある。
- `Domain` 層でこれを吸収し、内部的には全て小文字の `status` として扱う仕様となっている (`docs/specs/data/document_model.md`)。
- 実装時、辞書のキー検索で `key.lower()` を忘れないようにすること。

### 2.2. ロールバックの限界
- `ApprovalUseCase` の仕様 (`docs/specs/logic/approval_usecase.md`) にある通り、**Issue起票後のID追記失敗時** はロールバック（ファイル移動の取り消し）を行わない。
- このケースでは、二次被害（無限ループや二重起票）を防ぐため、以下の対応を行う実装とすること。
    1.  障害ログへの記録。
    2.  `_approved` ディレクトリ配下に対象ファイルと同名のマーカーファイル（`*.issue_metadata_failed`）を作成する。
    3.  例外を投げて処理を終了する。
- 自動リトライ機能は実装しない。

### 2.3. GitHub トークン
- 環境変数名は `GITHUB_MCP_PAT` である。`GITHUB_TOKEN` ではないので注意。

## 3. テスト戦略 (Test Strategy)
- **Unit Test**: 全てのロジック分岐（特に異常系）を網羅する。
- **Integration Test**: 実際にファイルシステムを操作するテスト（Tempディレクトリ使用）は、`FileSystemAdapter` のテストに限定する。UseCase のテストではファイル操作を行わない（Mockする）こと。

## 4. 完了条件 (DoD)
- 全ての `docs/specs/**/*.md` の要件がコード化されていること。
- `pytest` が全件パスすること。
- `mypy --strict` で型エラーが出ないこと。
