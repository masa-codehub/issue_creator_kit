# Orchestrator Flow (Orchestration & L1 Sync)

## Scenario Overview

- **Goal:** ADR-014に基づき、外部プロジェクトからの再利用を可能にするため、任意ディレクトリの走査（将来的にカスタム設定の読み込み）を行い、ドキュメントの同期とタスク起票を統括する。
- **Trigger:** CLI コマンド実行 (`issue-kit process --root <path>`)
- **Type:** `[Batch]`

## Contracts (Pre/Post)

- **Pre-conditions (前提):**
  - 処理対象の `root` ディレクトリが存在し、ADR/Taskファイルが配置されている。
- **Post-conditions (保証):**
  - 指定された `root` 配下の未起票ドキュメントがすべてGitHub Issueとして起票される。
  - L1 Issue のチェックリストが最新の Issue 番号で更新される。

## Related Structures

- `OrchestratorService` (see `src/issue_creator_kit/usecase/orchestrator_service.py`)
- `Agent Dispatcher (Planned: ADR-014)`
- `L1AutomationUseCase` / `TaskActivationUseCase`
- `L1SyncService` (Checklist Sync logic)

## Overall Orchestration Flow

```mermaid
sequenceDiagram
    autonumber
    participant User
    participant CLI as Agent Dispatcher (CLI)
    participant ORCH as OrchestratorService
    participant SCAN as FileSystemScanner
    participant L1UC as L1AutomationUseCase
    participant TUC as TaskActivationUseCase
    participant SYNC as L1SyncService

    User->>CLI: issue-kit process --root <path>

    Note over CLI: Load Config (Planned: External File > Defaults)
    CLI->>ORCH: execute(root_path, dry_run)

    ORCH->>SCAN: scan(root_path)
    SCAN-->>ORCH: documents, processed_ids

    rect rgb(240, 240, 240)
        Note right of ORCH: ADR (L1) Sync Phase
        ORCH->>L1UC: execute(root_path, config, documents)
        L1UC-->>ORCH: L1 Issue Details
    end

    rect rgb(230, 240, 255)
        Note right of ORCH: Task (L2) Activation Phase
        ORCH->>TUC: execute(root_path, config, l1_id, documents)
        TUC->>SYNC: sync_checklist(l1_id, id_map)
        Note right of SYNC: See "Checklist Sync Flow" below for details
        SYNC-->>TUC: sync_result
        TUC-->>ORCH: activation_result
    end

    ORCH-->>CLI: OrchestrationResult
    CLI-->>User: Success Summary
```

---

## Checklist Sync Flow (Read-Modify-Write)

### Scenario Overview (Sub-flow)

- **Goal:** 親Issue (L1) の本文内にある一時IDチェックリストを、起票された実Issue番号へ一括更新し、進捗状況をGitHub上で可視化する。
- **Trigger:** `TaskActivationUseCase` における全タスクの起票完了。
- **Type:** `Batch (Update)`

### Diagram (Sequence)

```mermaid
sequenceDiagram
    autonumber
    participant UC as TaskActivationUseCase
    participant SY as L1SyncService
    participant GH as GitHubAdapter

    UC->>SY: sync_checklist(l1_id, in_memory_map)

    rect rgb(240, 240, 240)
        Note over SY, GH: Read-Modify-Write Loop (with Retry)
        loop Max 3 Retries
            Note right of GH: Pending implementation of ETag support
            SY->>GH: get_issue(l1_id)
            GH-->>SY: {body, etag}

            SY->>SY: apply_replacement(body, in_memory_map)
            Note right of SY: Replace temporary IDs with issue numbers, preserving checkbox state

            SY->>GH: patch_issue(l1_id, new_body, if_match=etag)

            alt Success (200 OK)
                GH-->>SY: updated_issue
                Note over SY: Break Loop
            else Conflict (409) or Precondition Failed (412)
                GH-->>SY: Error (Conflict)
                Note over SY: Wait (Exponential Backoff) & Retry
            end
        end
    end

    SY-->>UC: result (success/fail)
```

## Reliability & Failure Handling

- **Consistency Model:** `Eventual Consistency`. L1の更新は、タスク起票そのものの成功とは独立しており、失敗しても次回実行時にリトライ可能。
- **Failure Scenarios:**
  - **Conflict (409/412):** 他のユーザーやボットが同時にL1を編集した場合に発生。ETagを用いた楽観的ロックにより、データの消失（Lost Update）を防ぐ。失敗時は最新の `body` を再取得してリトライする。
  - **Regex Mismatch:** `task-ID` の前後に予期せぬ文字がある場合、置換がスキップされる可能性がある。そのため、正規表現は `r"- \[\s*\]\s+"` (チェックリスト構文) をプレフィックスとして厳密にマッチングさせる。
  - **API Rate Limit:** 多数のタスクがある場合でも、更新は1回の `PATCH` で一括して行うため、API消費は最小限に抑えられる。

## Replacement Logic Details

Pythonコード片レベルでの置換ロジック案（**冪等性を考慮**）：

```python
import re
from typing import Dict

# in_memory_map: 一時ID ('task-010-01' など) -> 実Issue番号 (int, 例: 123)
def replace_body(body: str, in_memory_map: Dict[str, int]) -> str:
    if not in_memory_map:
        return body

    # 1. 部分的なマッチを避けるため、IDを長さの降順でソート
    sorted_ids = sorted(in_memory_map.keys(), key=len, reverse=True)

    # 2. 置換パターンの構築
    # 既に '#123' 形式に置換されているものはマッチさせない (Negative Lookahead は使わず、
    # プレフィックスとしてチェックリスト構文を厳密にマッチさせる)
    pattern = r"(- \[[ x]\]\s+)(" + "|".join(re.escape(tid) for tid in sorted_ids) + ")"

    def repl(match):
        prefix = match.group(1)  # '- [ ] ' or '- [x] '
        temp_id = match.group(2)
        issue_no = in_memory_map[temp_id]

        # 既に置換済みかどうかの簡易チェック（行全体のコンテキストを確認する場合）
        # ただし re.sub 内では prefix が一致している時点で「一時ID」が残っていることを意味する
        return f"{prefix}#{issue_no}"

    # 3. 単一の正規表現で一括置換
    # すでに '#[0-9]+' になっている箇所は match.group(2) の temp_id に合致しないため、
    # 自然に置換がスキップされ、冪等性が保たれる。
    new_body = re.sub(pattern, repl, body)
    return new_body
```
