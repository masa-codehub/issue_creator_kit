# Relay Engine Phase Transition Logic Specification

## Overview

`RelayEngine` において、`integration` タスク（かつ `audit` ラベル保持）の完了をトリガーに、上位の ADR/DesignDoc のフェーズラベルを自動的に遷移させるロジックを定義する。

## 1. Input

| Name             | Type        | Description                                                         |
| :--------------- | :---------- | :------------------------------------------------------------------ |
| `task`           | `Task`      | クローズされたタスクのメタデータモデル。                            |
| `current_labels` | `list[str]` | クローズされたタスクに現在付与されているラベルのリスト。            |
| `parent_issue`   | `dict`      | 親 Issue (ADR/DesignDoc) の GitHub API レスポンス（ラベルを含む）。 |

## 2. Output

| Type        | Description                                       |
| :---------- | :------------------------------------------------ |
| `list[str]` | 親 Issue に新しく設定すべきラベルの完全なリスト。 |
| `None`      | 遷移条件を満たさない場合。                        |

## 3. Algorithm / Flow

### 3.1. トリガー判定 (Guard Clauses)

以下の条件をすべて満たさない場合、処理を中断する（`None` を返す）。

1. `task.type == "integration"`
2. `"audit"` in `current_labels`
3. `task.parent` が有効な ADR ID である（`ADR_ID_PATTERN = r"^(adr|design)-\d{3}(?:-[a-z0-9-]+)?$"` にマッチすること）。

### 3.2. フェーズ判定と次フェーズの特定

クローズされたタスクの `role` に基づき、現在のフェーズと次フェーズを特定する。`role` が存在しない、または `(arch, spec, tdd)` のいずれでもない場合は `phase` をフォールバックとして使用する。

| Task Phase/Role | Current Parent Phase | Next Parent Phase             |
| :-------------- | :------------------- | :---------------------------- |
| `arch`          | `arch`               | `spec`                        |
| `spec`          | `spec`               | `tdd`                         |
| `tdd`           | `tdd`                | 現状維持 (`tdd` ラベルを維持) |

### 3.3. ラベルの集合演算 (Label Set Operation)

親 Issue のラベルリスト (`parent_issue["labels"]`) に対して以下の演算を行う。

1. **保持すべきラベルの抽出 (Keep List)**:
   - `L1`
   - `adr:\d{3}` にマッチするもの
   - `design:\d{3}` にマッチするもの
   - `plan`
   - その他、フェーズラベル (`arch`, `spec`, `tdd`) **以外**のすべてのラベル。
2. **新しいフェーズラベルの適用**:
   - ステップ 3.2 で特定した `Next Parent Phase` を追加する。
   - 重複は排除する（`set` などの順不同な集合構造を用いてよいが、後述の最終リスト生成時に順序を正規化する）。
3. **最終リストの生成**:
   - `Keep List` と `Next Parent Phase` を統合し、L1 初期ラベル付与仕様（`docs/specs/logic/l1-initial-labeling.md`）と同じ順序付けルールに従ってソートした最終ラベルリストを生成する。

### 3.4. 更新の実行

1. 生成されたラベルリストと現在の親ラベルリストの**ラベル集合**が異なる場合のみ（順序は無視して比較するか、3.3 で定義した順序付けルールを双方に適用したうえでリストとして比較する）、`github.update_issue_labels` を呼び出す。

## 4. Edge Cases

- **親 Issue が既に対応する次フェーズのラベルを持っている場合**:
  - 重複して追加しない（冪等性を担保）。
- **タスクのフェーズが不明な場合**:
  - 遷移を行わず、ログを出力して終了する。
- **親 Issue にフェーズラベルが存在しない場合**:
  - 完了したタスクのフェーズ (`role`/`phase`) から現在のフェーズを推測し、その次フェーズへの遷移を行う。
  - 例: `arch` タスクが完了した場合、親 Issue には `spec` ラベルが付与される。

## 5. Traceability

- **ADR Reference**: ADR-016
- **Implementation Goal**: Goal Definition (task-016-04)
- **Merged Files**: None (New Specification)
