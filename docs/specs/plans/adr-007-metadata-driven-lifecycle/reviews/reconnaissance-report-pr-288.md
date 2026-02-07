# 能動的偵察レポート (Reconnaissance Report) - PR #288 Spec Fixes

## 1. 調査対象と意図 (Scope & Context)

- **ユーザー依頼のキーワード:** `creation_logic.md`, `promotion_logic.md`, `PR #288`, `review comments`
- **調査の目的:** PR #288 で受けたレビュー指摘に基づき、仕様書の現状と SSOT (ADR-007) の整合性を確認し、修正が必要な箇所を特定する。

## 2. 収集された事実 (Evidence)

### A. ドキュメント上の規定 (SSOT)

- **[Source]:** `reqs/design/_approved/adr-007-metadata-driven-lifecycle.md`
  - **事実・規定:**
    - 物理階層を廃止し、メタデータ駆動のライフサイクル管理へ移行。
    - `Ready -> Issued` 時の「Atomic Move」と `issue_id` 記録を規定。
    - ロードマップ同期はベストエフォート（ADR-007 第4.3項）。
  - **引用:**
    > 起票が成功した瞬間、ステータスを `Issued` に更新し、ファイルを `reqs/tasks/_archive/` へ即座に移動し、`issue_id` を記録する。

### B. 実装の現状 (Codebase Reality)

- **[File]:** `docs/specs/logic/creation_logic.md`

  - **責務:** `IssueCreationUseCase.create_issues()` の詳細アルゴリズム定義。
  - **事実:**
    - Step 3.C で `issue_id` の記録は記載されているが、リンク置換後の本文（updated_content）の保存が明記されていない。
    - Step 4.2 で「ADR-003 に準拠したベストエフォート型同期」という古い参照が残っている。
  - **コード抜粋:**

    ```markdown
    ### Step 3: Atomic Issue Creation (Fail-fast Zone)

    ...

    - **C. Handle Success**: - Update status to `Issued`. - Record `issue_id`.
      ...

    ### Step 4: Atomic Move & Status Transition (Transaction Commit)

    ... 2. **Roadmap Sync**: Best-effort sync as per ADR-003.
    ```

- **[File]:** `docs/specs/logic/promotion_logic.md`
  - **責務:** `WorkflowUseCase.promote_tasks()` の詳細アルゴリズム定義。
  - **事実:**
    - Step 3.3 の Rationale に「ready for virtual queue」という ADR-003 の用語が残っている。
  - **コード抜粋:**
    ```markdown
    4.  Rationale: This alerts the team that new tasks are ready for `ick create`.
    ```
    (※これは提案された修正後。現状は `ready for virtual queue` となっている)

### C. 物理構造と依存関係 (Structure & Dependencies)

- **ディレクトリ:** `docs/specs/logic/`
- **依存関係:**
  - `creation_logic.md` は `FileSystemAdapter`, `GitHubAdapter`, `RoadmapSyncUseCase` に依存。
  - `promotion_logic.md` は `creation_logic.md` 内の Ready 判定ロジックに依存。

## 3. 発見された制約と矛盾 (Constraints & Contradictions)

- **SSOTとの乖離:** `creation_logic.md` が supersede された ADR-003 を参照している。
- **論理的欠落:** `creation_logic.md` の Step 3 から Step 4 へのデータ受け渡しにおいて、更新済み本文の保持が明示されていないため、再計算が必要になるかコンテキストが失われる恐れがある。

## 4. 補足・未調査事項 (Notes & Unknowns)

- `promotion_logic.md` の修正提案では `ick create` への言及が求められているが、これは ADR-007 で導入された概念（コマンド）であり、仕様書全体で用語を統一する必要がある。
