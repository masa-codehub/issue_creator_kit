# Graph Engine Service Specification

## 1. Overview

- **Responsibility**: タスク間の依存関係 (`depends_on`) を解析し、デッドロック（循環参照）の検知および、最適な実行順序（トポロジカルソート）を決定するドメインサービス。
- **Collaborators**: `ScannerService` (入力データの提供), `OrchestratorService` (ソート結果の利用)。

## 2. Data Structures (Models)

### 2.1. Task Node

- **Schema**: 依存関係を保持する `Task` ドメインモデル。
- **Constraints**: `depends_on` に含まれる `TaskID` がリスト外（解決済み想定）であってもエラーとせず、グラフ上は無視する。

## 3. Interfaces (API/Methods)

### 3.1. `GraphEngine.sort(tasks: list[Task]) -> list[Task]`

- **Signature**: `sort(tasks: list[Task]) -> list[Task]`
- **Contract**:
  - **Input**: ソート対象の `Task` オブジェクトのリスト。
  - **Output**: 依存関係に従ってソートされた新しい `Task` リスト。
  - **Pre-condition**: 入力される `Task` リストはスキーマ検証済みであること。
- **Exceptions**: `CircularDependencyError` (循環参照検知時)。

## 4. Logic & Algorithms

### 4.1. Topological Sort

`graphlib.TopologicalSorter` を使用して実装する。

1. `Task.id` をノード、`Task.depends_on` を依存先としてグラフを構築。
2. `sorter.prepare()` を実行。
3. `sorter.get_ready()` で準備完了ノードを取得。
4. **Deterministic Ordering**: 同時に準備完了となったノード間では、`TaskID` の文字列昇順でソートし、決定論的な実行順序を保証する。
5. `sorter.done()` を呼び出して処理を継続。

### 4.2. Cycle Detection

`graphlib.CycleError` を捕捉し、パス情報を含む `CircularDependencyError` へ変換して送出する。

## 5. Traceability

- **Merged Files**:
  - `adr-010-graph-service.md` (Legacy)
- **Handover Constraints**:
  - N/A
