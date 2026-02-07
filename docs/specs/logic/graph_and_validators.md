# Task Graph & Dependency Validation Specification

## Overview
ADR-008 において、走査されたタスク間の依存関係をグラフ構造として構築し、その整合性を検証するロジックを定義する。
不適切な依存関係（循環参照、自己参照、存在しない依存先）を早期に検出し、安全な実行順序を決定することを目的とする。

## Data Structures

### TaskNode
単一のタスクまたは ADR を保持するグラフのノード。

| Property | Type | Description |
| :--- | :--- | :--- |
| `task` | `Task | ADR` | 保持するモデルオブジェクト |
| `dependencies` | `Set[TaskNode]` | このノードが依存しているノード群 (Upstream) |
| `dependents` | `Set[TaskNode]` | このノードに依存しているノード群 (Downstream) |

### TaskGraph
ノードの集合を管理し、グラフ全体の操作を行う。

| Method | Return Type | Description |
| :--- | :--- | :--- |
| `add_node(task)` | `None` | タスクをノードとして追加する |
| `add_edge(from_id, to_id)` | `None` | `from_id` が `to_id` に依存するエッジを張る |
| `validate()` | `None` | グラフの整合性（循環参照等）を検証する |
| `get_execution_order()` | `List[str]` | トポロジカルソートされた ID リストを返す |

## Algorithm / Flow

### 1. グラフ構築 (Graph Construction)
1.  走査されたすべての `Task` / `ADR` を `TaskGraph.add_node()` で登録する。
2.  各タスクの `depends_on` リストをループし、`add_edge(task.id, dep_id)` を実行する。
3.  `to_id` (依存先) がノードリストに存在しない場合、`ORPHAN_DEPENDENCY` エラーを準備する。

### 2. 循環参照検知 (Cycle Detection)
深さ優先探索（DFS）を用いて実装する。
1.  各ノードの状態を管理する（`UNVISITED`, `VISITING`, `VISITED`）。
2.  `UNVISITED` ノードから探索を開始する。
3.  訪問中のノード（`VISITING`）を再度訪問した場合、循環参照（Cycle）として検知する。
4.  循環を検知した場合、関与しているノード ID のリストを含めて `CYCLE_DETECTED` エラーを送出する。

### 3. トポロジカルソート (Topological Sort)
Kahn's Algorithm または DFS ベースのソートを使用し、依存関係のない順序から実行リストを作成する。

## Verify Criteria (TDD)

### Happy Path (DAG)
- **Input**: A(depends_on=[B]), B(depends_on=[C]), C(depends_on=[])
- **Expected**: `get_execution_order()` -> `[C, B, A]`

### Error Path (Self-Reference)
- **Input**: A(depends_on=[A])
- **Expected**: `ValidationError` or `GraphError` (Self-reference detected for 'A')

### Error Path (Circular Dependency)
- **Input**: A -> B, B -> C, C -> A
- **Expected**: `GraphError: CYCLE_DETECTED [A, B, C]`

### Error Path (Orphan Dependency)
- **Input**: A(depends_on=[X]) ※X は存在しない
- **Expected**: `GraphError: ORPHAN_DEPENDENCY 'X' referenced by 'A' not found`

## Edge Cases
- グラフが空の場合、空リストを返す。
- 完全に独立したタスクが複数ある場合、ID の昇順などで決定論的な順序を返す。
