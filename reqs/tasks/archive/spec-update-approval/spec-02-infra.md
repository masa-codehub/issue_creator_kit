---
depends_on:
- spec-01-domain.md
issue: '#215'
labels:
- task
- P1
- TECHNICAL_DESIGNER
roadmap: reqs/roadmap/archive/roadmap-adr002-document-approval-flow.md
status: Draft
task_id: SPEC-02
title: '[Spec] Define Infrastructure Adapters'
---
# [Spec] Define Infrastructure Adapters

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/archive/roadmap-adr002-document-approval-flow.md
- **Task ID**: SPEC-02
- **Common Definitions**: docs/specs/plans/20260120-approval-flow.md

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: Git操作やGitHub API操作の仕様が明文化されておらず、実装者の裁量に任されている。
- **To-be (あるべき姿)**: `Infrastructure` 層の各Adapter（GitHub, Git, FS）のインターフェースと振る舞いが定義される。
- **Design Evidence**: `docs/architecture/arch-structure-issue-kit.md` (Infrastructure Layer)

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/plans/20260120-approval-flow.md`
- [ ] `docs/architecture/arch-behavior-approval-flow.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **詳細隠蔽**: 特定のライブラリ（PyGithub等）の内部実装詳細を書きすぎないこと。インターフェース（入力と出力）に集中する。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `docs/specs/components/infra_adapters.md`
    - **処理内容**: 以下のAdapterのメソッドシグネチャと期待動作を定義する。
      - `GitHubAdapter`: `find_or_create_issue(title, body) -> int`
      - `GitAdapter`: `commit(message) -> void`
      - `FileSystemAdapter`: `safe_move_file(src_path, dst_dir, ...)`, `write_file(path, content)`
    - **Verify (TDD Criteria)**:
      - 「APIエラー時に例外 `InfrastructureError` が送出されること」
      - 「Gitコミット失敗時の挙動（再試行するか、エラーにするか）」

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/spec-update-approval-flow`
- **作業ブランチ (Feature Branch)**: `feature/spec-02-infra`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **レビュー**: `docs/specs/components/infra_adapters.md` が作成されていること。
- [ ] **Mock可能性**: 定義されたインターフェースが Mock オブジェクトとして表現可能か確認する。

## 6. 成果物 (Deliverables)
- `docs/specs/components/infra_adapters.md`