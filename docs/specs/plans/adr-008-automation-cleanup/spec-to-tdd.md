# Spec to TDD Handover: ADR-008 Scanner Foundation

## 1. 概要 (Overview)

本ドキュメントは、ADR-008「Scanner Foundation」の実装フェーズ（TDD）へ向けた申し送り事項をまとめたものである。
これまでの仕様策定フェーズで確定したモデル、ロジック、および制約に基づき、実装者が迷いなくテスト駆動開発を行えるようにすることを目的とする。

## 2. 確定した仕様 (Finalized Specs)

以下の仕様書を正（SSOT）として実装を行うこと。

| カテゴリ  | 仕様書パス                                 | 概要                                                       | 優先度     |
| :-------- | :----------------------------------------- | :--------------------------------------------------------- | :--------- |
| **Data**  | `docs/specs/data/domain_models_adr008.md`  | TaskID, ADRIDの正規表現、ADR/Taskモデルのスキーマ定義。    | **最優先** |
| **Logic** | `docs/specs/logic/scanner_logic.md`        | 物理ファイルシステム走査、重複検知、Fail-fast ロジック。   | 高         |
| **Logic** | `docs/specs/logic/graph_and_validators.md` | 依存関係グラフ構築、循環参照検知、Mermaid生成。            | 高         |
| **API**   | `docs/specs/api/cli_commands.md`           | CLIコマンド定義（`process-diff` の引数バリデーション等）。 | 中         |

## 3. 実装方針と注意点 (Implementation Guidelines)

### 3.1. SSOTの転換 (Shift to Physical State)

- **Git非依存**: 従来の実装（`WorkflowUseCase` 等）が依存していた `git diff` や `git log` を一切使用しないこと。
- **物理ファイル正**: `reqs/` ディレクトリ内のファイル存在有無と配置場所（`_approved` vs `_archive`）のみを信頼する。

### 3.2. Fail-Fast 原則

- **即時停止**: ID重複、循環参照、フォーマット不正などの異常を検知した時点で、即座に例外（`ValidationError` や `GraphError`）を送出し、処理を中断すること。
- **ログ出力**: エラー発生時は、原因となったファイルパスと具体的な理由（「ID 'task-001' が重複」等）を標準エラー出力に明示すること。

### 3.3. Pydantic v2 の活用

- **Validation**: ドメインモデルのバリデーションには Pydantic v2 の機能を最大限活用し、手動での `if` 分岐によるバリデーションを避けること。
- **Document Model**: 実装上、`Document` は `Union[Task, ADR]` (または共通基底クラスを持つ構造) として扱い、スキャナーやグラフビルダーがこれらを透過的に処理できるようにすること。詳細は `docs/specs/data/domain_models_adr008.md` を参照。

## 4. テスト戦略 (Test Strategy)

### 4.1. ファイルシステムのモック

- **原則**: ユニットテストでは実際のファイルシステムにアクセスせず、`pathlib` や `os` モジュールのモック（または `pyfakefs` 等のライブラリ）を使用すること。
- **ケース**:
  - `_archive` に同名IDがある場合の重複エラーテスト。
  - 権限エラー等によるファイル読み込み失敗テスト。

### 4.2. グラフ理論のテスト

- **循環参照**: 3つ以上のノードによる複雑な循環（A->B->C->A）をテストケースに含めること。
- **自己参照**: 自分自身への依存（A->A）をテストケースに含めること。
- **未定義ID**: 存在しないIDへの依存（A->Z）をテストケースに含めること。

### 4.3. クリーンアップ確認

- **Legacy Code**: `approval_usecase.py` 等の削除対象コードが誤って呼ばれていないか、あるいは正しく削除されていることを確認すること。

## 5. TDD 実装順序 (Recommended Order)

1. **Domain Models**: `src/issue_creator_kit/domain/models/` を実装し、バリデーションロジックをテストする。
2. **Scanner Logic**: `FileSystemScanner` を実装し、ファイル検知と重複チェックをテストする。
3. **Graph Logic**: `TaskGraph` と `GraphBuilder` を実装し、依存関係の構築と検証をテストする。
4. **Visualizer**: `Visualizer` を実装し、Mermaid 文字列生成をテストする。
5. **CLI Integration**: 最後に CLI コマンドと結合する。
