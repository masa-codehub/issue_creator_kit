# Use Case Orchestrator Specification

## 1. Overview

- **Responsibility**: ドラフトの走査、検証、起票、および事後処理（削除）の一連のワークフロー（Relay/Activation）を統括する。システム全体の状態を同期させ、不整合のない起票プロセスを保証する。
- **Collaborators**: `FileSystemScanner`, `TaskGraphValidator`, `IGitHubAdapter`, `L1SyncService`, `FileArchiver` (Removal).

## 2. Data Structures (Models)

### 2.1. OrchestrationConfig

- **Schema**:
  ```python
  class OrchestrationConfig:
      root_path: Path
      l1_id: int
      dry_run: bool  # ADR-013 必須ガードレール
  ```

### 2.2. SessionCache

- **Schema**:
  ```python
  class SessionCache:
      # task_id -> issue_number (e.g., "task-013-23" -> 565)
      resolved_ids: Dict[str, int]
  ```

## 3. Interfaces (API/Methods)

### 3.1. TaskActivationUseCase.execute()

- **Signature**: `execute(config: OrchestrationConfig) -> ActivationResult`
- **Contract**:
  - **Pre-conditions**: `l1_id` が GitHub 上に実在すること。
  - **Post-conditions**: 起票に成功したファイルは物理的に削除され（Pure Active Git）、L1 Issue のチェックリストが更新されている。

## 4. Logic & Algorithms

### 4.1. Overall Flow (ADR-013 Updated)

1.  **Scanning**: `FileSystemScanner.scan()` で Active なドキュメントを収集。
2.  **Validation**: `TaskGraphValidator.validate()` で整合性を検証。
    - この際、ローカルにない依存先は GitHub API で解決される (Hybrid Validation)。
3.  **Topological Creation Loop**:
    - 各ドラフトについて：
      - **GitHub Idempotency Check**: 同一 `task_id` を持つ Issue が既に GitHub 上に存在するか検索する。
      - **Dependency Resolution**: `depends_on` 内の ID を `SessionCache` または GitHub 検索結果に基づき実 Issue 番号（`#123`）に置換。
      - **Issue Creation**: `IGitHubAdapter.create_issue()` を呼び出し。
      - **Success Registration**: 成功した `IssueNo` を `SessionCache` に登録。
4.  **L1 Checklist Sync**: 親 Issue (L1) のチェックリストを実 Issue 番号で一括更新。
5.  **Physical Removal (ADR-013 Cleanup)**:
    - 起票に成功したファイルを物理的に削除する。アーカイブディレクトリへの移動は行わない。

### 4.2. Error Handling & Safety

- **Guardrail**: 全ての破壊的変更（Issue 作成、ファイル削除）は `config.dry_run` が `False` の場合のみ実行する。
- **Transactional Atomicity**: ファイル削除に失敗しても、起票の事実は GitHub に残るため、次回の実行時に GitHub Idempotency Check で「処理済み」としてスキップされる。

## 5. Traceability

- **Merged Files**:
  - `adr-010-usecase-orchestration.md` (Legacy)
  - `spec-012-relay-engine.md` (Legacy)
- **Handover Constraints**:
  - **Constraint 4**: GitHub API 優先参照とアーカイブ除外の統括。
