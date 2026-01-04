---
title: "インフラ層のインターフェース定義"
labels:
  - "task"
  - "P1"
  - "TECHNICAL_DESIGNER"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T1-4"
depends_on: ["issue-T1-3.md"]
next_phase_path: ""
status: "Draft"
---
# インフラ層のインターフェース定義

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T1-4

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 現在の `infrastructure` 層（GitAdapter, GitHubAdapter）が、PR作成や複雑なブランチ操作、コミットログの取得といった新要件に対応できるか不明確。
- **To-be (あるべき姿)**: ドメイン層が必要とするインフラ操作のメソッドシグネチャが明確に定義され、インターフェース仕様書として文書化されている。
- **Design Evidence (設計の根拠)**: `design-003-logic.md` (T1-3成果物)

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/design/_inbox/design-003-logic.md`
- [ ] `src/issue_creator_kit/infrastructure/` (既存コード)

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **変更禁止**: 既存の `GitHubAdapter` の動作を破壊しない。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `docs/specs/infra-interface.md`
    - **処理内容**:
        - `IGitAdapter`: `get_diff_files`, `checkout_new_branch`, `commit_and_push` 等の定義。
        - `IGitHubAdapter`: `create_pull_request`, `search_issues` 等の定義。
        - 各メソッドの入出力型（Type Hinting）と例外定義。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-1-foundation`
- **作業ブランチ (Feature Branch)**: `feature/T1-4-infra-interface`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: 仕様書が作成され、レビューを通過すること。
- [ ] **ファイル状態**: `docs/specs/infra-interface.md` が存在すること。

## 6. 成果物 (Deliverables)
- 仕様書: `docs/specs/infra-interface.md`
