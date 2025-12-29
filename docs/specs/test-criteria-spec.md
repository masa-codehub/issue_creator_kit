# 詳細設計: 検証基準（テストケース）定義 (ADR-002)

## 1. 目的
Phase 2 での実装において、`utils.py` の各関数が ADR-002 の要件を満たし、かつ既存の Markdown 構造を破壊しないことを保証するためのテストシナリオを定義する。

## 2. `parse_metadata` のテストケース

### 2.1. 正常系 (Success Cases)
| ID | シナリオ | 入力例 (Markdown) | 期待される戻り値 (Dict) |
| :--- | :--- | :--- | :--- |
| P-1 | 標準形式 | `- **Status**: Draft` | `{"Status": "Draft"}` |
| P-2 | マーカー違い | `* **Status**: Draft` | `{"Status": "Draft"}` |
| P-3 | 太字なし | `- Status: Draft` | `{"Status": "Draft"}` |
| P-4 | 複数項目 | `- **Key1**: V1
- **Key2**: V2` | `{"Key1": "V1", "Key2": "V2"}` |
| P-5 | 空白の揺らぎ | `-**Status**:Value` | `{"Status": "Value"}` |

### 2.2. 異常系・準正常系 (Negative Cases)
| ID | シナリオ | 入力例 (Markdown) | 期待される挙動 |
| :--- | :--- | :--- | :--- |
| P-E1 | インデントあり | `  - **Status**: Draft` | 抽出対象外 (`{}`) |
| P-E2 | 本文中の擬似メタデータ | `Some text
- **Status**: Draft` | 解析範囲外なら無視 |
| P-E3 | ファイルが空 | ` ` | `{}` |

## 3. `update_metadata` のテストケース

### 3.1. 正常系 (Success Cases)
- **入力データ**: `content`, `updates={"Status": "Approved"}`
- **期待値**: 指定されたキーの値のみが書き換わり、他の部分は維持される。

| ID | シナリオ | 入力例 (Markdown) | 期待される出力 (Markdown) |
| :--- | :--- | :--- | :--- |
| U-1 | 単一置換 | `- **Status**: Draft` | `- **Status**: Approved` |
| U-2 | マーカー維持 | `* **Status**: Draft` | `* **Status**: Approved` |
| U-3 | 装飾維持 | `- Status: Draft` | `- Status: Approved` |
| U-4 | 複数置換 | `- **S**: D
- **A**: N` | `- **S**: A
- **A**: N` (Sのみ指定時) |

### 3.2. エッジケース (Edge Cases)
| ID | シナリオ | 入力 | 期待される挙動 |
| :--- | :--- | :--- | :--- |
| U-E1 | キー非存在 | `- **Other**: V` | 元のコンテンツを維持 (or 追記: 要件に従う) |
| U-E2 | 値が空 | `- **Status**: ` | `- **Status**: Approved` |
| U-E3 | キーが本文中 | `Text - **Status**: D` | 置換されないこと |

## 4. `safe_move_file` のテストケース

### 4.1. 正常系 (Success Cases)
- **S-1**: 移動先ディレクトリが存在しない場合、自動作成して移動に成功すること。
- **S-2**: 移動後、元のファイルが存在しないこと。

### 4.2. 異常系 (Error Cases)
- **S-E1**: 移動元ファイルが存在しない場合、`FileNotFoundError` を送出すること。
- **S-E2**: 移動先に同名ファイルがあり `overwrite=False` の場合、`FileExistsError` を送出すること。

## 5. テスト実行方針
- Phase 2 において `pytest` を使用して実装する。
- 上記のテストデータ（Markdown文字列）をパラメータ化テスト (`@pytest.mark.parametrize`) で効率的に実行する。
