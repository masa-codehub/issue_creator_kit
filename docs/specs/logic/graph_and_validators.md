# Task Graph & Dependency Validation Specification

## Overview
ADR-008 において、走査されたドキュメント（Task/ADR）間の依存関係をグラフ構造として構築し、その整合性を検証するとともに、Mermaid 形式で可視化するロジックを定義する。
不適切な依存関係（循環参照、自己参照、存在しない依存先）を早期に検出し、安全な実行順序を決定および視覚化することを目的とする。

## Data Structures

### TaskNode
単一の `Document` を保持するグラフのノード。

| Property | Type | Description |
| :--- | :--- | :--- |
| `document` | `Document` | 保持するドキュメントオブジェクト |
| `dependencies` | `List[TaskNode]` | このノードが依存しているノード群 (Upstream) |
| `dependents` | `List[TaskNode]` | このノードに依存しているノード群 (Downstream) |

### TaskGraph
ノードの集合を管理し、グラフ全体の操作を行う。

| Method | Return Type | Description |
| :--- | :--- | :--- |
| `add_document(doc)` | `None` | ドキュメントをノードとして追加する |
| `add_edge(from_id, to_id)` | `None` | `from_id` が `to_id` に依存するエッジを張る |
| `validate()` | `None` | グラフの整合性（循環参照等）を検証する |
| `get_execution_order()` | `List[str]` | トポロジカルソートされた ID リストを返す |

## Domain Services

### GraphBuilder
`FileSystemScanner` から渡されたドキュメントリストから `TaskGraph` を構築する。

- **File**: `src/issue_creator_kit/domain/services/builder.py`
- **Method**: `build_graph(documents: List[Document]) -> TaskGraph`

### Visualizer
構築された `TaskGraph` を Mermaid 記法の文字列に変換する。

- **File**: `src/issue_creator_kit/domain/services/visualizer.py`
- **Method**: `to_mermaid(graph: TaskGraph) -> str`

## Algorithm / Flow

### 1. グラフ構築 (Graph Construction)
1.  走査されたすべての `Document` を `TaskGraph.add_document()` で登録する。
2.  各ドキュメントの `metadata.depends_on` リストをループし、`add_edge(doc.metadata.id, dep_id)` を実行する。
3.  `to_id` (依存先) がノードリストに存在しない場合、`ORPHAN_DEPENDENCY` エラーを準備する。
    - **Note**: ただし、依存先が `_archive/` に存在することが明らかな場合は例外とする（スキャン範囲に含まれている必要がある）。

### 2. 循環参照検知 (Cycle Detection)
深さ優先探索（DFS）を用いて実装する。
1.  各ノードの状態を管理する（`UNVISITED`, `VISITING`, `VISITED`）。
2.  `UNVISITED` ノードから探索を開始する。
3.  訪問中のノード（`VISITING`）を再度訪問した場合、循環参照（Cycle）として検知する。
4.  循環を検知した場合、関与しているノード ID のリストを含めて `CYCLE_DETECTED` エラーを送出する。

### 3. トポロジカルソート (Topological Sort)
Kahn's Algorithm または DFS ベースのソートを使用し、依存関係のない順序から実行リストを作成する。
- 依存関係がないドキュメントが複数ある場合、ID の昇順でソートして決定論的な順序を保証する。

### 4. Mermaid 生成 (Mermaid Generation)
以下の形式で Mermaid 文字列を生成する。
1.  ヘッダー: `graph TD`
2.  ノード定義: `ID["Title"]` (タイトルは `Metadata` または `Document` から取得)
3.  エッジ定義: `FromID --> ToID`
4.  スタイリング: 進行状況（Status）に応じたクラス分け（任意）。

## Verify Criteria (TDD)

### Happy Path (DAG & Visualization)
- **Input**:
    - A (title: "Task A", depends_on: [B])
    - B (title: "Task B", depends_on: [])
- **Expected (Order)**: `[B, A]`
- **Expected (Mermaid)**:
    ```mermaid
    graph TD
        A["Task A"]
        B["Task B"]
        A --> B
    ```

### Error Path (Self-Reference)
- **Input**: A(depends_on=[A])
- **Expected**: `GraphError: SELF_REFERENCE 'A' depends on itself`

### Error Path (Circular Dependency)
- **Input**: A -> B, B -> C, C -> A
- **Expected**: `GraphError: CYCLE_DETECTED [A, B, C]`

### Error Path (Orphan Dependency)
- **Input**: A(depends_on=[X]) ※X は存在しない
- **Expected**: `GraphError: ORPHAN_DEPENDENCY 'X' referenced by 'A' not found`

## Edge Cases
- グラフが空の場合、空の Mermaid 文字列（またはヘッダーのみ）と空リストを返す。
- タイトルに特殊文字（`"` や `[` 等）が含まれる場合、適切にエスケープするか除去する。
