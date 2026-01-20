# Document Approval Flow Sequence

## Scenario Overview
- **Goal:** 自動化されたフローにより、設計ドキュメントの承認（メタデータ更新、移動）、トラッキングIssueの起票、およびGitコミットを行う。
- **Trigger:** GitHub Actions (Merge to main or Manual Dispatch) -> `issue-kit` CLI execution.
- **Type:** Batch / Sync (CLI実行中は同期的)

## Contracts (Pre/Post)
- **Pre-conditions (前提):**
    - `reqs/design/_inbox/` に承認対象のマークダウンファイルが存在する。
    - GitHub Actions ランナー上で `gh` コマンドまたは `GITHUB_TOKEN` が利用可能である。
- **Post-conditions (保証):**
    - 対象ファイルが `reqs/design/_approved/` に移動されている。
    - ファイル内の `Status` が `承認済み` に、`Date` が実行日に更新されている。
    - GitHub Issue が起票（または特定）され、そのIDがファイルに記載されている。
    - 変更がGitコミットされている（Pushは呼び出し元が行う想定、またはAdapterが行う）。

## Related Structures
*   `src/issue_creator_kit/cli.py`
*   `src/issue_creator_kit/usecase/approval.py`
*   `src/issue_creator_kit/infrastructure/git_adapter.py`
*   `src/issue_creator_kit/infrastructure/github_adapter.py`

## Diagram (Sequence)
```mermaid
sequenceDiagram
    autonumber
    actor GA as GitHub Actions

    box "CLI Layer" #eee
        participant CLI as CLI Layer
    end

    box "Usecase Layer" #efe
        participant UC as Workflow
    end

    box "Domain Layer" #fff
        participant DOM as Document
    end

    box "Infrastructure Layer" #f9f9f9
        participant INF_GH as GitHubAdapter
        participant INF_FS as FileSystem
        participant INF_GIT as GitAdapter
    end

    GA->>CLI: run-workflow (approve)
    activate CLI
    CLI->>INF_GH: init(token)
    CLI->>INF_GIT: init()
    CLI->>UC: run(adapters)
    activate UC

    UC->>INF_FS: list_files("_inbox/*.md")
    INF_FS-->>UC: file_paths

    loop For each file
        UC->>INF_FS: read_document(path)
        INF_FS-->>UC: document_obj

        Note right of UC: 1. Update Metadata (Persist at _inbox_)
        UC->>INF_FS: update_metadata(path, status="承認済み", date=today)

        Note right of UC: 2. Move File
        UC->>INF_FS: move_file(path, new_path)

        Note right of UC: 3. Create/Link Issue
        UC->>INF_GH: find_or_create_issue(title, body)
        activate INF_GH
        INF_GH-->>UC: issue_number
        deactivate INF_GH
        
        Note right of UC: 4. Update Approved File with Issue ID
        UC->>INF_FS: update_metadata(new_path, issue_id=issue_number)
    end

    Note right of UC: 5. Git Add/Commit/Push (Bulk)
    UC->>INF_GIT: add(".")
    UC->>INF_GIT: commit("Approve design documents")
    activate INF_GIT
    
    alt Commit Success
        INF_GIT-->>UC: success
        Note right of UC: (optional) Push to remote
        UC->>INF_GIT: push()
    else Commit Failure
        INF_GIT-->>UC: error
        UC->>UC: handle_error (log & abort)
    end
    deactivate INF_GIT

    UC-->>CLI: result_summary
    deactivate UC
    CLI-->>GA: exit_code
    deactivate CLI
```

## Reliability & Failure Handling
- **Consistency Model:** Eventual Consistency (File system updates -> Git commit -> Push)
- **Failure Scenarios:**
    - *GitHub API Error:* Issue起票は、(1) メタデータ更新の永続化（`write_file`）、(2) ファイルの移動、(3) Issue起票 の順に行われる。Issue起票に失敗した場合は、直前に行ったファイル移動およびメタデータ更新をロールバックして元の状態に戻し、エラーログを出力した上で次のファイルの処理へ移行する。これにより、最終的にメタデータとIssueの不整合が残らないようにする（短いトランザクション＋ロールバック戦略）。
    - *Git Commit Error:* ローカルでのコミットに失敗した場合、後続のPushも失敗するため、CLIは非ゼロの終了コードを返却し、CIを失敗させる。