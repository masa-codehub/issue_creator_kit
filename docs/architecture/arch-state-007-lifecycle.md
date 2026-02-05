# Metadata-Driven Lifecycle (ADR-007)

## Subject Definition
- **Target Objects:** ADR / Design Doc, Task (Issue Draft)
- **Persistence:** File System (`reqs/`) and GitHub Issues
- **Concurrency Strategy:** Git Merge (Physical files) and GitHub API (Status sync)

## Diagram (State Transition)
```mermaid
stateDiagram-v2
    title Document & Task Lifecycle (ADR-007)

    state "ADR / Design Doc" as ADR {
        [*] --> Draft_ADR : Create in reqs/design/_inbox/
        Draft_ADR --> Approved : PR Merge to main
        Approved --> Postponed : status: Postponed
        Approved --> Superseded : status: Superseded
        Postponed --> [*]
        Superseded --> [*]
        
        note right of Approved
            Side Effect: Move to _approved/
            Create L1/L2 Issues
        end
    }

    state "Task (Issue Draft)" as Task {
        [*] --> Draft_Task : Create in reqs/tasks/<ADR-ID>/
        Draft_Task --> Ready : ick sync (valid)
        Ready --> Issued : ick create
        Issued --> Completed : GitHub Issue closed
        Issued --> Cancelled : GitHub Issue cancelled
        Draft_Task --> Cancelled : Manual delete/archive
        Completed --> [*]
        Cancelled --> [*]

        note right of Issued
            Side Effect: Move to _archive/
            Record issue_id
        end
    }
```

## State Definitions & Transitions

### ADR / Design Doc
| State | Definition | Trigger (Transition) | Side Effects |
| :--- | :--- | :--- | :--- |
| `Draft` | 起草・レビュー中。`_inbox/` に配置される。 | ファイル作成。 | なし。 |
| `Approved` | 承認済み。システムの正解（SSOT）。`_approved/` に配置される。 | `_inbox/` からのマージ PR がクローズ。 | `_approved/` へ物理移動。L1 ADR Issue と L2 統合 Issue が起票される。 |
| `Postponed` | 実装を先送りした設計。`_archive/` に配置される。 | メタデータ `status: Postponed` への更新。 | `_archive/` へ物理移動。紐づくタスクの保留。 |
| `Superseded` | 新しい設計に置き換えられた旧版。`_archive/` に配置される。 | 後続 ADR による `Supersedes` 宣言。 | `_archive/` へ物理移動。 |

### Task (Issue Draft)
| State | Definition | Trigger (Transition) | Side Effects |
| :--- | :--- | :--- | :--- |
| `Draft` | 実装タスク案。`reqs/tasks/<ADR-ID>/` に配置される。 | ファイル作成。 | なし。 |
| `Ready` | 全ての `depends_on` が `Issued` (または Completed) になり、起票準備が整った状態。 | `ick sync` による依存関係チェック合格。 | なし。 |
| `Issued` | GitHub Issue として起票され、実作業コンテキストに移行した状態。 | `ick create` コマンド実行。 | `reqs/tasks/_archive/` へ物理移動。`issue_id` をファイルに記録。 |
| `Completed` | GitHub Issue がクローズされ、実装が完了した状態。 | GitHub Issue のステータス変更。 | ロードマップの進捗更新。後続タスクの `Ready` 化。 |
| `Cancelled` | GitHub Issue がキャンセルされるか、Draft 段階のタスクが破棄・アーカイブされた状態。 | GitHub Issue のキャンセル、または手動でのメタデータ変更。 | 対応するタスクファイルの `_archive/` への移動。 |

## Invariants (不変条件)
*   **Unique ID:** `id` (例: `007-T1`) はプロジェクト全域で一意でなければならない。
*   **Strict Dependency:** `depends_on` に指定されたタスクが `Issued` になるまで、そのタスクは起票されてはならない。
*   **Atomic Issue Creation:** GitHub Issue が正常に作成されない限り、ファイルは `_archive/` へ移動してはならない。
*   **Hierarchy Priority:** L3 タスクは必ず親となる L1/L2 Issue が存在（または同時作成）されていなければならない。