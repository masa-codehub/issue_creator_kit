# Task Graph & Validator Specification

## 1. Overview

- **Responsibility**: プロジェクト内の全 ADR および Task の整合性を静的に検証し、循環参照や不適切な依存関係を 100% 阻止する。また、トポロジカルソートによる安全な実行順序の決定と、Mermaid 形式での可視化を担う。
- **Collaborators**: `DocumentParser`, `IGitHubAdapter`, `GraphBuilder`, `Visualizer`.

## 2. Data Structures (Models)

### 2.1. TaskNode

- **Schema**:
  ```python
  class TaskNode:
      id: str
      document: Optional[Document]  # ローカルに存在する場合のみ
      dependencies: List["TaskNode"]
      dependents: List["TaskNode"]
      status: TaskStatus  # GitHub 上の状態 (Resolved/Open/Missing)
  ```
- **Constraints**: 循環参照がない DAG (Directed Acyclic Graph) 構造であること。

### 2.2. ValidationResult

- **Schema**:
  ```python
  class ValidationResult:
      is_valid: bool
      errors: List[ValidationErrorDetail]
      execution_order: List[str]  # トポロジカルソート結果
  ```

### 2.3. ValidationErrorDetail

- **Format**: `[ERROR_CODE] {Message} ({File}:{Line})`
- **Error Codes**: `DEPENDENCY_ORPHAN`, `DEPENDENCY_PREMATURE`, `SELF_REFERENCE`, `CYCLE_DETECTED`, `VALIDATION_NETWORK_FAIL`.

## 3. Interfaces (API/Methods)

### 3.1. TaskGraphValidator.validate()

- **Signature**: `validate(documents: List[Document]) -> ValidationResult`
- **Contract**:
  - **Pre-conditions**: 入力ドキュメントは `DocumentParser` による単体バリデーションを通過していること。
  - **Post-conditions**: 戻り値の `is_valid` が `True` の場合、`execution_order` は有効な DAG のソート順序である。
- **Exceptions**: 通信エラー時は `VALIDATION_NETWORK_FAIL` を結果に含める。

### 3.2. [Planned] IGitHubAdapter.check_task_status()

- **Note**: このメソッドは Hybrid Validation 実装時に追加予定のインターフェース拡張である。
- **Signature**: `check_task_status(task_id: str) -> TaskStatus`
- **Responsibility**: 指定された ID が GitHub 上で `closed` (completed) かどうかを確認する。

## 4. Logic & Algorithms

### 4.1. Hybrid Validation Flow (Constraint 1)

依存関係の解決において、以下の優先順位で実在確認を行う。

1.  **Local Map**: 現在スキャンされた `documents` 内に ID が存在するか。
2.  **Session Cache**: 同一セッション内で既に GitHub API で確認済みか。
3.  **GitHub API**: `IGitHubAdapter.check_task_status(id)` を呼び出し、Issue が存在し `closed` かつ `completed` かを確認する。
    - **Note**: ローカルに存在せず、GitHub 上でも見つからない、または `open` 状態の場合はエラーとする。

### 4.2. 依存関係検証アルゴリズム

1.  全てのローカルドキュメントを `TaskNode` としてグラフに追加。
2.  各ノードの `depends_on` リストを走査：
    - 依存先 ID がローカルにあればエッジを張る。
    - ローカルにない場合、**Hybrid Validation Flow** に従い GitHub を確認。
    - GitHub で `closed` であれば「解決済み外部依存」としてノード（ドキュメント本体は無し）を作成し、正常終了。
    - GitHub で `open` であれば `DEPENDENCY_PREMATURE` エラー。
    - GitHub に存在しなければ `DEPENDENCY_ORPHAN` エラー。
3.  **閉路検知 (3-state DFS)**:
    - 全ノードを `Unvisited` で初期化。
    - `Visiting` 状態のノードに再訪した場合、`CYCLE_DETECTED` とし、循環パスを報告。
4.  **トポロジカルソート**:
    - 入次数が 0 のノードから順にソート。ID の辞書順昇順で決定論的順序を維持。

### 4.3. Mermaid 可視化 (Visualizer)

- 構造定義: `graph TD`
- ノード定義: `ID["Title"]` (特殊文字はエスケープ)
- スタイル: ローカルノードと解決済み外部ノード（GitHub）をスタイル（色・点線等）で区別することを推奨。

## 5. Traceability

- **Merged Files**:
  - `graph_and_validators.md` (Legacy)
  - `spec-012-graph-validator.md` (Legacy)
- **Handover Constraints**:
  - **Constraint 1**: ID 未発見時の GitHub API 呼び出しを 4.1, 4.2 で担保。
