---
id: 007-T4-04
parent: adr-007
type: task
title: "[TDD] CLI Integration (Interface)"
status: Draft
phase: interface
date: 2026-02-05
labels:
  - "gemini:tdd"
  - "P1"
  - "BACKENDCODER"
roadmap: "docs/specs/plans/adr-007-metadata-driven-lifecycle/tdd-plan.md"
depends_on: ["007-T4-03"]
---

# [TDD] CLI Integration (Interface)

## 1. 目的と背景 (Goal & Context)

- **As-is (現状)**: CLI コマンドの引数定義や UseCase への繋ぎ込みが ADR-003 仕様のまま。
- **To-be (あるべき姿)**: `process-diff` コマンドが `--before`, `--after`, `--adr-id` を正しく受け取り、バリデーションした上で新 UseCase を呼び出せるようになっている。
- **Design Evidence (設計の根拠)**:
  - `docs/specs/api/cli_commands.md`

## 2. 参照資料・入力ファイル (Input Context)

- [ ] `docs/specs/api/cli_commands.md`
- [ ] `src/issue_creator_kit/cli.py`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)

- [ ] **ロジックの分離**: CLI 層で直接 GitHub API や Git コマンドを実行しないこと。必ず UseCase 経由で行う。

### 3.2. 実装手順 (Changes)

- [ ] **ファイル**: `src/issue_creator_kit/cli.py`
  - **処理内容**:
    - `process-diff` サブコマンドの引数（--before, --after, --adr-id）を追加。
    - `--adr-id` のフォーマットバリデーション（`adr-XXX`）の実装。
    - `IssueCreationUseCase.create_issues()` へのパラメータ受け渡し。
- [ ] **ファイル**: `tests/unit/test_cli.py`
  - **処理内容**:
    - 正常系: 正しい引数でのコマンド実行（UseCase の呼び出し検証）。
    - 異常系: `--adr-id` のフォーマット不正時のエラー終了（終了コード 1）。

## 4. ブランチ戦略 (Branching Strategy)

- **ベースブランチ (Base Branch)**: feature/impl-adr007-lifecycle
- **作業ブランチ (Feature Branch)**: tdd/task-007-T4-04-impl-cli

## 5. 検証手順・完了条件 (Verification & DoD)

- [ ] **自動テスト**: `pytest tests/unit/test_cli.py` がパスすること。
- [ ] **静的解析**: `ruff check .` および `mypy .` がパスすること。
- [ ] **観測される挙動**: `issue-kit process-diff --help` で新しい引数が表示されること。

## 6. 成果物 (Deliverables)

- `src/issue_creator_kit/cli.py`
- `tests/unit/test_cli.py`
