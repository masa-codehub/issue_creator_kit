# L1 Initial Labeling Strategy Specification

## Overview

L1 起票時（ADR/DesignDoc の自動起票時）に、そのドキュメントの種類（フェーズ）と「計画中」であることを示すラベルを自動で付与するロジックを定義する。

> [!NOTE] > **実装ステータス**: 本仕様は ADR-016 に基づく将来の実装予定であり、現時点の `L1AutomationUseCase` の実装とは一部異なります。実装フェーズにおいて順次適用されます。

## Related Documents

- ADR: `reqs/design/_approved/adr-016.md`

## Input

| Name     | Type | Description                                               |
| :------- | :--- | :-------------------------------------------------------- |
| `adr_id` | str  | ADR または DesignDoc の ID（例: `adr-016`, `design-001`） |

## Output

| Type        | Description                                                         |
| :---------- | :------------------------------------------------------------------ |
| `list[str]` | 付与すべきラベルのリスト（例: `["arch", "plan", "L1", "adr:016"]`） |

## Algorithm / Flow

`L1AutomationUseCase.get_labels` メソッドにおいて、以下のステップでラベルを生成する。

1.  **メタデータ抽出**:
    - `adr_id` に対して正規表現 `(adr|design)-(\d{3})` を適用する。
    - プレフィックス（`adr` または `design`）と 3桁の数値（`XXX`）を抽出する。
2.  **フェーズラベルの決定**:
    - プレフィックスが `adr` の場合: `arch` を選択。
    - プレフィックスが `design` の場合: `spec` を選択。
3.  **メタデータラベルの構築**:
    - `{prefix}:{number}` 形式のラベルを作成する（例: `adr:016`）。
4.  **ラベルリストの構築**:
    - 以下の順序でラベルをリストに格納する。
      1.  フェーズラベル (`arch` / `spec`)
      2.  計画ラベル (`plan`)
      3.  階層ラベル (`L1`)
      4.  メタデータラベル (`adr:XXX` / `design:XXX`)

## Edge Cases

- **不正な ID 形式**:
  - `(adr|design)-(\d{3})` にマッチしない場合。
  - **Fallback**: `["plan", "L1", f"adr:{adr_id}"]` を返す（不正な ID であっても「計画中」であることを示すために `plan` を必ず付与する）。
- **既に ID がメタデータ形式でない場合**:
  - スキャナー側でバリデーションされているはずだが、メソッドの堅牢性のためにフォールバックを維持する。

## Verification Criteria

- [ ] `get_labels("adr-016")` -> `["arch", "plan", "L1", "adr:016"]`
- [ ] `get_labels("design-001")` -> `["spec", "plan", "L1", "design:001"]`
- [ ] `get_labels("adr-999-slug")` -> `["arch", "plan", "L1", "adr:999"]`
- [ ] `get_labels("invalid-id")` -> `["plan", "L1", "adr:invalid-id"]` (Fallback)
