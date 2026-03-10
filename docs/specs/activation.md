# Task Activation & Initial Ignition Specification

## 1. Overview

- **Responsibility**: `Task` ドメインモデルを GitHub Issue として起票し、依存関係を構築し、親 Issue (L1) との同期を行い、最終的に独立したタスクに着火（ラベル付与）を行うオーケストレーター。
- **Collaborators**:
  - `IssueRenderer`: Issue の本文・メタデータ・ラベルの生成。
  - `GitHubAdapter`: Issue の作成、ラベルの付与、既存 Issue の検索。
  - `L1SyncService`: 親 Issue (ADR) のチェックリスト更新。
  - `GraphBuilder`: 依存関係に基づく実行順序（Topological Sort）の決定。

## 2. Data Structures

### 2.1. ActivationStatus (Enum)

| Value             | Description                                                                                                                                                                             |
| :---------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SUCCESS`         | 全てのタスクが正常に処理（起票またはアーカイブ済みの検知）され、L1 との同期も完了した。着火はベストエフォートで試行するが、失敗しても `SUCCESS` から `PARTIAL_SUCCESS` には変更しない。 |
| `PARTIAL_SUCCESS` | 一部のタスクでエラーが発生したが、少なくとも 1 つ以上のタスクが正常に処理された。                                                                                                       |
| `FAILED`          | 全てのタスクの処理に失敗した、またはスキャン・ソート段階で致命的なエラーが発生した。                                                                                                    |

### 2.2. ActivationResult (Value Object)

| Field               | Type               | Description                                     |
| :------------------ | :----------------- | :---------------------------------------------- |
| `successful_issues` | `list[int]`        | 正常に起票または検知された Issue 番号のリスト。 |
| `failed_tasks`      | `list[str]`        | 処理に失敗した Task ID のリスト。               |
| `status`            | `ActivationStatus` | プロセス全体の最終ステータス。                  |

## 3. Interfaces (API/Methods)

### 3.1. `TaskActivationUseCase.execute(root_path, l1_id, ...) -> ActivationResult`

- **Signature**: `execute(root_path: Path | str, l1_id: int, ...) -> ActivationResult`
- **Contract**:
  - 指定された `root_path` 内のタスクドラフトをスキャンし、依存関係順に起票する。
  - 起票完了後、`l1_id` で指定された親 Issue のチェックリストを更新する。
  - **Terminal Step**: すべての同期の試行が終了した後に、`Initial Ignition` を実行する。
- **Timing Constraint**: `Initial Ignition` は、L1 Sync の試行が終了した**後**、かつ `execute()` が `ActivationResult` を返す直前に実行しなければならない。

### 3.2. `TaskActivationUseCase._ignite_independent_tasks(in_memory_map)`

- **Signature**: `_ignite_independent_tasks(in_memory_map: dict[str, int]) -> None`
- **Contract**:
  - `in_memory_map` から復元可能なタスク群（実装上は `execute` 内で保持される `tasks` コレクション）のうち `Ignition Filter` に合致するものを抽出し、対応する Issue 番号に `gemini` ラベルを付与する。
  - 本メソッドの外部インターフェースはアーキテクチャ図（`behavior-activation.md`）に合わせて `in_memory_map` のみを受け取るものとする。
  - このメソッドは例外を外部に伝播させず、内部でログ出力とエラーハンドリングを完結させる。

## 4. Logic & Algorithms

### 4.1. Sequential Creation & Idempotency

1. `GraphBuilder` により、トポロジカルソートされた `execution_order` を取得する。
2. 各タスクについて、アーカイブ済みファイルまたは GitHub 上のタイトル一致により、既に Issue が存在するか確認する（べき等性の確保）。
3. 存在しない場合のみ、`IssueRenderer.render` を呼び出し、`github.create_issue` で新規起票する。

### 4.2. L1 Checklist Sync

1. 起票された全てのタスクの ID と Issue 番号のマップ (`in_memory_map`) を `L1SyncService` に渡す。
2. `L1SyncService` は、親 Issue の本文中の ID を対応する `#IssueNo` に置換し、チェックボックス形式で更新する。

### 4.3. Initial Ignition (事後着火)

全ての起票および L1 同期の試行が終了した後に実行される、自律稼働開始のためのステップ。

#### 4.3.1. Ignition Filter (判定ロジック)

以下の条件を**すべて満たす**タスクを「独立したタスク（Independent Task）」と判定し、着火対象とする。

- `depends_on` が `[]` (空リスト) または `None` である。
- 今回の `execute()` 呼び出しにおいて、正常に起票された、または既に Issue が存在することが確認された。

#### 4.3.2. Execution Flow

1. 正常に処理されたタスクのリストを走査し、`Ignition Filter` に合致する Issue 番号を抽出する。
2. 抽出された各 Issue 番号に対し、`github.add_labels(issue_no, ["gemini"])` を実行する。
3. **重複防止**: `add_labels` はべき等性が保たれるべきだが、UseCase 側でも既にラベルが付与されているかどうかのチェックは行わず、無条件に `add_labels` を呼び出す仕様とする（GitHub 側での重複排除に委ねる）。

#### 4.3.3. Negative Constraints (負の制約)

- **RelayEngine への干渉禁止**: `RelayEngine` のスキャンロジックやイベントトリガーには一切触れないこと。
- **起票時ラベルの排除**: `IssueRenderer` が生成する初期ラベルリストには `gemini` を含めてはならない。必ず事後的に `add_labels` で付与すること。

## 5. Error Handling & Reliability

### 5.1. Ignition Failure

- `add_labels` の呼び出し中に API エラーが発生した場合、エラーをキャッチしてログ (`logger.warning`) に記録する。
- **Recovery Path**: 1 つ以上のタスクで着火に失敗しても、`execute()` 自体は中断せず、残りのタスクの着火を継続する。
- **Status Impact**: 着火の失敗は、既に起票・同期が成功している場合、`SUCCESS` ステータスを `PARTIAL_SUCCESS` に変更する要因とはしない（着火は「ベストエフォート」の付加的プロセスと位置づける。詳細は `definitions.md` 参照）。

### 5.2. L1 Sync Failure

- L1 同期に失敗した場合も、タスクの起票自体は完了しているため、プロセスは継続し、`Initial Ignition` ステップへ進む。

## 6. Verification Criteria (DoD)

### 6.1. Happy Path

- `depends_on: []` のタスク A と `depends_on: ["A"]` のタスク B を起票。
- A には `gemini` ラベルが付与され、B には付与されないことを確認。
- A の着火が、L1 同期の試行が終了した後に行われていることをシーケンス（またはログ）で確認。

### 6.2. Error Path

- 着火（`add_labels`）時に API エラーが発生しても、プログラムがクラッシュせず、ログが出力されること。
- 再実行時に、既に `gemini` ラベルが付いている Issue に対して再度 `add_labels` が呼ばれても、GitHub 上でエラーにならない（または適切にハンドルされる）こと。
