# Dynamic Dispatcher Logic 詳細仕様書

## 概要

本ドキュメントは、PR ラベルとプロジェクト固有の設定ファイル (`.github/issue-kit-config.json`) を照合し、実行すべきエージェントロール (`AGENT_ROLE`) を動的に決定する `ick dispatch` コマンドの詳細仕様を定義する。

この機能により、ハードコードされた役割判定ロジックを排除し、リポジトリごとの柔軟な役割割当を実現する。

## 関連ドキュメント

- **Architecture**: `docs/architecture/behavior-dynamic-dispatch.md`
- **Common Definitions**: `reqs/context/specs/adr-014-modular-reusability/definitions.md`
- **ADR**: ADR-014 Modular Reusability and External Configuration

## データモデル (Data Model)

設定ファイルは Pydantic モデルを用いてバリデーションを行う。
実装場所の推奨: `src/issue_creator_kit/domain/models/config.py` (新規作成)

### `RoleMapping` クラス

特定のロール名と、それをトリガーするラベルのリストを定義する。

| フィールド名 | 型          | 説明                                          |
| :----------- | :---------- | :-------------------------------------------- |
| `name`       | `str`       | エージェントロール名 (例: `SYSTEM_ARCHITECT`) |
| `labels`     | `List[str]` | このロールをトリガーするラベルのリスト。      |

### `Config` クラス

設定ファイル全体の構造を定義する。

| フィールド名   | 型                               | 説明                                                           | デフォルト値 |
| :------------- | :------------------------------- | :------------------------------------------------------------- | :----------- |
| `roles`        | `List[RoleMapping]`              | ロールとラベルのマッピングリスト。**定義順が優先順位となる。** | (必須)       |
| `triggers`     | `Optional[Dict[str, List[str]]]` | 将来的な拡張用のイベントベーストリガー。                       | `None`       |
| `default_role` | `Optional[str]`                  | ラベルがマッチしなかった場合のフォールバックロール名。         | `None`       |

## CLI 仕様 (API Specification)

### `ick dispatch`

- **概要:** PR ラベルと設定ファイルを照合し、決定されたロール名を標準出力に返す。
- **Arguments:**
  - `--labels`: (必須) カンマ区切りの PR ラベルリスト。 (例: `arch,gemini:arch`)
  - `--config-path`: (オプション) 設定ファイルのパス。デフォルトは `.github/issue-kit-config.json`。
- **Behavior:**
  1. 設定ファイルを読み込み、`Config` モデルでバリデーションする。
  2. 後述の判定アルゴリズムを実行する。
  3. マッチしたロール名を標準出力（stdout）に出力する。
  4. 成功時は `Exit Code 0` で終了する。
- **Exit Codes & Errors:**
  - `0`: 成功。
  - `1`: 異常終了。以下のエラーメッセージを標準エラー出力（stderr）に出力する。
    - 設定ファイル不在: `[FAIL] {config_path}:0 (config): Configuration file not found.`
    - マッチするロールなし（かつ `default_role` 未定義）: `[FAIL] {config_path}:0 (roles): No matching role found for labels: {labels}.`
    - JSON パース失敗/型エラー: `[FAIL] {config_path}:{line} (config): Invalid configuration format. {details}`

## 判定アルゴリズム (Logic / Algorithm)

### 判定ロジック (先勝ち)

複数のロールに合致するラベルが PR に付与されている場合、設定ファイルの `roles` 配列の**定義順**に従い、最初に一致したものを採用する。

```python
def dispatch(pr_labels: List[str], config: Config) -> str:
    pr_labels_set = set(pr_labels)
    # 1. roles 配列を定義順に走査
    for role in config.roles:
        # 2. ロールに定義されたラベルのいずれかが PR ラベルに含まれているか確認
        if any(label in pr_labels_set for label in role.labels):
            return role.name

    # 3. マッチしない場合は default_role を返す
    if config.default_role:
        return config.default_role

    # 4. default_role もない場合はエラー送出
    raise NoMatchingRoleError(f"No matching role found for labels: {pr_labels}")
```

## TDD Criteria (検証手順・完了条件)

実装時、以下のテストケースをパスすることを保証すること。

| ID   | ケース                   | 入力 (labels, config)                                                                                         | 期待される結果                                        |
| :--- | :----------------------- | :------------------------------------------------------------------------------------------------------------ | :---------------------------------------------------- |
| TC-1 | 先勝ち判定               | `labels=["arch", "spec"]`<br>`roles=[{"name": "SA", "labels": ["arch"]}, {"name": "TD", "labels": ["spec"]}]` | `SA` が返ること                                       |
| TC-2 | フォールバックなしエラー | `labels=["unknown"]`<br>`roles=[...]`, `default_role=None`                                                    | `Exit Code 1` となり stderr にメッセージが出ること    |
| TC-3 | JSON 型エラー            | `roles="not an array"` (不正な型)                                                                             | 適切なエラーメッセージと共に `Exit Code 1` となること |

## 補足・制約事項

- **大文字小文字の区別**: ラベルのマッチングは完全一致（Case-sensitive）とする。
- **拡張性**: `triggers` フィールドは本仕様では判定に使用しないが、モデルには含めておく（ADR-014 準拠）。
- **Fail-fast**: 設定ミスや不整合がある場合は、曖昧な動作をせず即座にエラー終了することを徹底する。
