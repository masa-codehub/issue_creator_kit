# Task Graph & Dependency Validation Specification

## Overview

ADR-008 において、走査されたドキュメント（Task/ADR）間の依存関係をグラフ構造として構築し、その整合性を検証するとともに、Mermaid 形式で可視化するロジックを定義する。
不適切な依存関係（循環参照、自己参照、存在しない依存先）を早期に検出し、安全な実行順序を決定および視覚化することを目的とする。

## Data Structures

### DocumentNode

単一の `Document` を保持するグラフのノード。

| Property       | Type                 | Description                                   |
| :------------- | :------------------- | :-------------------------------------------- |
| `document`     | `Document`           | 保持するドキュメントオブジェクト              |
| `dependencies` | `List[DocumentNode]` | このノードが依存しているノード群 (Upstream)   |
| `dependents`   | `List[DocumentNode]` | このノードに依存しているノード群 (Downstream) |

### TaskGraph

ノードの集合を管理し、グラフ全体の操作を行う。

| Method                     | Return Type | Description                                                                      |
| :------------------------- | :---------- | :------------------------------------------------------------------------------- |
| `add_document(doc)`        | `None`      | ドキュメントをノードとして追加する                                               |
| `add_edge(from_id, to_id)` | `None`      | `from_id` が `to_id` に依存するエッジを張る                                      |
| `validate(valid_ids)`      | `None`      | グラフの整合性（循環参照等）を検証する。`valid_ids` にない依存先はエラーとする。 |
| `get_execution_order()`    | `List[str]` | トポロジカルソートされた ID リストを返す                                         |

## Domain Services

### GraphBuilder

`FileSystemScanner` から渡されたドキュメントリストから `TaskGraph` を構築する。

- **File**: `src/issue_creator_kit/domain/services/builder.py`
- **Method**: `build_graph(documents: List[Document], archived_ids: Set[str]) -> TaskGraph`

### Visualizer

構築された `TaskGraph` を Mermaid 記法の文字列に変換する。

- **File**: `src/issue_creator_kit/domain/services/visualizer.py`
- **Method**: `to_mermaid(graph: TaskGraph) -> str`

## Algorithm / Flow

### 1. グラフ構築 (Graph Construction)

1.  走査されたすべての `Document` を `TaskGraph.add_document()` で登録する。
2.  各ドキュメントの `metadata.depends_on` リストをループし、`add_edge(doc.metadata.id, dep_id)` を実行する。
3.  `validate(valid_ids)` を実行する。ここで `valid_ids` は「現在走査されたドキュメントの ID 集合」と `archived_ids` の和集合とする。
4.  `to_id` (依存先) が `valid_ids` に存在しない場合、`ORPHAN_DEPENDENCY` エラーを送出する。
    - **Note**: 依存先ドキュメントが `_archive/` ディレクトリ配下に存在する場合（`archived_ids` に含まれる場合）、その依存関係は有効とみなし、エラーの対象外とする。

### 2. 循環参照検知 (Cycle Detection)

深さ優先探索（DFS）を用いて実装する。

1.  各ノードの状態を管理する（`UNVISITED`, `VISITING`, `VISITED`）。
2.  `UNVISITED` ノードから探索を開始する。
3.  訪問中のノード（`VISITING`）を再度訪問した場合、循環参照（Cycle）として検知する。
4.  循環を検知した場合、関与しているノード ID のリストを含めて `CYCLE_DETECTED` エラーを送出する。

### 3. トポロジカルソート (Topological Sort)

Kahn's Algorithm または DFS ベースのソートを使用し、依存関係のない順序から実行リストを作成する。

- 依存関係がないドキュメントが複数ある場合、ID の辞書順昇順でソートして決定論的な順序を保証する。

### 4. Mermaid 生成 (Mermaid Generation)

以下の形式および順序規則で Mermaid 文字列を生成する。

1.  ヘッダー: 常に `graph TD` を返す（グラフが空の場合も同様）。
2.  ノード定義: `ID["Title"]`
    - タイトル取得優先順位: `metadata.extra["title"]` → 本文先頭の H1 見出し (`# ...`) → `metadata.id`
    - 特殊文字の変換ルール:
      - `"` : `\"` にエスケープ
      - `[` : `(` に置換
      - `]` : `)` に置換
      - 改行 (`\n`) : `<br/>` に置換
3.  エッジ定義: `FromID --> ToID`
    - 矢印は、**依存元のタスクから依存先のタスク（前提となるタスク）**に向かって引かれる。
4.  スタイリング: 進行状況（Status）に応じたクラス分け（任意）。
5.  **出力順序の固定**:
    - ノード定義: ID の辞書順昇順。
    - エッジ定義: `(FromID, ToID)` のタプルによる辞書順昇順。

## Verify Criteria (TDD)

### Happy Path (DAG & Visualization)

- **Input**:
  - task-001 (title: "Task 1", depends_on: ["task-002"])
  - task-002 (title: "Task 2", depends_on: [])
- **Expected (Order)**: `["task-002", "task-001"]`
- **Expected (Mermaid)**:
  ```mermaid
  graph TD
      task-001["Task 1"]
      task-002["Task 2"]
      task-001 --> task-002
  ```

### Error Path (Self-Reference)

- **Input**: task-001 (depends_on=["task-001"])
- **Expected**: `GraphError: SELF_REFERENCE 'task-001' depends on itself`

### Error Path (Circular Dependency)

- **Input**: task-001 -> task-002, task-002 -> task-003, task-003 -> task-001
- **Expected**: `GraphError: CYCLE_DETECTED [task-001, task-002, task-003]`

### Error Path (Orphan Dependency)

- **Input**: task-001 (depends_on=["unknown-task"])
- **Expected**: `GraphError: ORPHAN_DEPENDENCY 'unknown-task' referenced by 'task-001' not found`

## Edge Cases

- グラフが空の場合、Mermaid 文字列として必ずヘッダーのみ `graph TD` を返し、実行順序は空リスト `[]` を返す。
- タイトルに特殊文字が含まれる場合の変換例:
  - 入力タイトル: `Task [P0] "critical"`
  - 変換後ノード定義: `task-001["Task (P0) \"critical\""]`
