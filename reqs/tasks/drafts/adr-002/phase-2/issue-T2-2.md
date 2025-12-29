---
title: "共通ユーティリティ (utils.py) の実装"
labels:
  - "task"
  - "P1"
  - "BACKENDCODER"
roadmap: "reqs/roadmap/active/roadmap-adr002-document-approval-flow.md"
task_id: "T2-2"
depends_on:
  - "issue-T2-1.md"
status: "Draft"
---
# {{title}}

## 親Issue / ロードマップ (Context)
- **Roadmap**: {{roadmap}}
- **Task ID**: {{task_id}}

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: メタデータ操作の仕様 (`docs/specs/metadata-logic-spec.md`) とインターフェース (`docs/specs/interface-spec.md`) は定義されているが、実装が存在しない。
- **To-be (あるべき姿)**: `utils.py` に `load_document`, `save_document`, `safe_move_file` が実装され、`python-frontmatter` を用いて堅牢に動作する。

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/metadata-logic-spec.md` (YAML Frontmatter仕様)
- [ ] `docs/specs/interface-spec.md` (関数シグネチャ)
- [ ] `docs/specs/test-criteria-spec.md` (テストケース)

## 3. 実装手順 (Implementation Steps)

### 3.1. テストコード作成 (TDD)
- [ ] **ファイル**: `tests/unit/test_utils.py`
    - **処理内容**: `docs/specs/test-criteria-spec.md` に定義されたテストケースを `pytest` で実装する。
    - **要件**: `tmp_path` フィクスチャを活用し、実際のファイルI/Oを検証する。

### 3.2. 実装 (Implementation)
- [ ] **ファイル**: `src/issue_creator_kit/utils.py`
    - **処理内容**: `docs/specs/interface-spec.md` で定義された関数 (`load_document`, `save_document`, `update_metadata`, `safe_move_file`) を実装する。
    - **要件**: `python-frontmatter` ライブラリを使用すること。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-2-implementation`
- **作業ブランチ (Feature Branch)**: `feature/T2-2-utils-impl`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/test_utils.py` が全てパスすること。
- [ ] **型チェック**: `mypy src/issue_creator_kit/utils.py` でエラーが出ないこと。

## 6. 成果物 (Deliverables)
- `src/issue_creator_kit/utils.py`
- `tests/unit/test_utils.py`