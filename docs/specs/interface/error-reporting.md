# Enhanced Validation & Error Reporting UX Specification

## 1. 概要 (Overview)

本ドキュメントは、Issue Creator Kit (ICK) におけるバリデーションエラー出力のユーザーエクスペリエンス (UX) を向上させるための仕様を定義する。
複雑なエラーメッセージを、ユーザーが即座に理解し修正アクションを取れる形式に変換することを目的とする。

## 2. 関連ドキュメント (Related Documents)

- ADR: [ADR-014: Modular Reusability and External Integration](../plans/adr-014-modular-reusability/definitions.md) (Section 6)
- Issue: [#607 task-014-16: Spec - Enhanced Validation & Error Reporting UX](../../../reqs/tasks/adr-014/task-014-16.md)

## 3. エラーメッセージ翻訳マップ (Error Message Mapping)

生の Pydantic エラーやドメインエラーを、以下の親切なメッセージに変換する。

| 元のエラー (Regex/Type)              | 変換後のメッセージ (Friendly Message)                                                |
| :----------------------------------- | :----------------------------------------------------------------------------------- |
| `ValueError: Invalid Task ID format` | ID 形式が不正です。期待される形式: `task-XXX-NN` (例: task-014-01)                   |
| `Field required`                     | `{field_name}` は必須項目です。YAML Frontmatter に追加してください                   |
| `Parse Error (YAML/JSON)`            | 設定ファイルの構文が不正です。カンマやクォーテーションの不足がないか確認してください |
| `DUPLICATE_ID`                       | この ID は既に使用されています（アーカイブ済みまたは他のファイルと重複）。           |
| `CYCLE_DETECTED`                     | 循環依存が検出されました。依存関係を見直してください。                               |

## 4. 出力レイアウト (Output Layout)

エラー出力は以下のフォーマットに統一する。

```text
[FAIL] <Path>:<Line> (<Field>): <Friendly Message>
       Current: <Actual Value>
       Expected: <Expected Value/Format>
```

### 具体例

```text
[FAIL] reqs/tasks/task-014-01.md:5 (id): ID 形式が不正です。期待される形式: `task-XXX-NN` (例: task-014-01)
       Current: 014-S1
       Expected: task-014-01
```

## 5. 色のセマンティクス (Color Semantics)

ANSI Color を使用して、ステータスを視覚的に区別する。

| ステータス | プレフィックス | 色 (ANSI)   | 用途                                 |
| :--------- | :------------- | :---------- | :----------------------------------- |
| SUCCESS    | `[DONE]`       | Green (32)  | コマンドの正常終了、タスクの成功     |
| FAILURE    | `[FAIL]`       | Red (31)    | バリデーションエラー、致命的エラー   |
| WARNING    | `[WARN]`       | Yellow (33) | 注意が必要だが処理は継続可能な警告   |
| SKIP       | `[SKIP]`       | Yellow (33) | スキップ。既知の状態であり変更不要。 |
| INFO       | `[INFO]`       | Cyan (36)   | 処理状況、ドライランのプレビュー情報 |

### `--no-color` フラグ

- `--no-color` フラグ（または環境変数 `NO_COLOR`）が指定されている場合、ANSI 色コードを一切出力してはならない。

## 6. エラー特定と変換ロジック (Conversion Logic)

### 6.1. 構造化エラーの保持

`DomainValidationError` クラスを拡張し、以下の属性を保持可能にする。

- `code`: エラー識別子 (例: `INVALID_ID`, `MISSING_FIELD`)
- `path`: ファイルパス
- `line`: 行番号
- `field`: フィールド名
- `current_value`: 現在の値
- `expected_value`: 期待される値

### 6.2. Pydantic エラーからの変換

Pydantic の `ValidationError.errors()` から返される各エラーオブジェクトを解析し、上記の構造化データにマッピングする。

- `loc` からフィールド名を特定。
- `type` からエラー種別を特定。
- `msg` または `ctx` から詳細情報を抽出。

### 6.3. 行番号の特定

1. Pydantic エラーの `loc` を使用。
2. YAML パーサーが位置情報 (line/column) を保持している場合はそれを利用する。
3. 保持していない場合は、既存のキーワード検索 (`id:`, `depends_on:`) をフォールバックとして使用する。

## 7. 補足・制約事項 (Notes)

- 既存の `ick check` コマンドにおいて、複数のファイルでエラーが発生した場合、全てのファイルを走査して一括でエラーを表示すること（Fail-fast せず集約する）。
- 集約後の最終的な終了コードは、エラーがあれば非ゼロとする。
