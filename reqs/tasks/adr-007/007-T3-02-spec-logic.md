---
id: 007-T3-02
parent: adr-007
type: task
phase: spec
status: Draft
depends_on: ["007-T3-01"]
title: "Update Lifecycle Logic Specifications"
labels:
  - "gemini:spec"
  - "P1" # Priority: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
  - "BACKENDCODER" # Role: BACKENDCODER, SYSTEM_ARCHITECT, etc.
---

# Task: Update Lifecycle Logic Specifications

## 1. Goal & Context
### Goal
DAG解析ロジック、タスクのステータス遷移（Ready判定）、および物理ファイルの Atomic Move ロジックの詳細仕様を策定・更新する。

### As-is
`creation_logic.md` 等は物理ディレクトリの階層構造に依存したロジックとなっており、メタデータ駆動（`depends_on`）による制御に対応していない。

### To-be
`docs/specs/logic/` 配下の仕様書が更新され、ADR-007 の「メタデータによる依存解決」と「フラットな物理移動」が定義されている。

### Design Evidence
- `reqs/design/_approved/adr-007-metadata-driven-lifecycle.md`
- `docs/architecture/plans/adr-007-metadata-driven-lifecycle/arch-to-spec.md`

## 2. Input Context
- `docs/specs/logic/creation_logic.md` (編集対象)
- `docs/specs/logic/promotion_logic.md` (編集対象)
- `docs/specs/plans/adr-007-metadata-driven-lifecycle/definitions.md` (参照: Logic Standards)

## 3. Implementation Steps & Constraints
### Negative Constraints
- GitHub API への具体的なリクエスト詳細（HTTPメソッド等）は `infra_adapters.md` の責務であり、ここではロジック（判定基準）に集中すること。

### Changes
1. **Creation Logic Update (`creation_logic.md`):**
   - 「物理パスによる検索」から「IDによるインデックス検索」へロジックを変更。
   - `depends_on` 解析フローチャートの追加（トポロジカルソートまたは再帰探索）。
   - `Ready` 判定ロジック（全依存タスクの完了確認）の定義。
   - Atomic Move の手順（API成功 -> `_archive/` 移動 -> コミット）の定義。
2. **Promotion Logic Update (`promotion_logic.md`):**
   - Auto-PR（フェーズ連鎖）において、メタデータ `next_phase_path` ではなく、タスク定義内の後続関係から推論、あるいは廃止するかを検討し記述を更新（今回はADR-007で明示されていないため、既存ロジックとADR-007の整合性を取る最小限の修正とする）。

## 4. Branching Strategy
- **Base Branch:** `feature/spec-update-adr007`
- **Feature Branch:** `spec/task-007-T3-02-logic`

## 5. Verification & DoD
### 5.1. Verification Criteria
- [ ] **DAG Logic:** 循環参照の検出とエラーハンドリングが定義されていること。
- [ ] **Idempotency:** 既に `issue_id` を持つタスクに対する再実行時の挙動（Skip or Update）が定義されていること。
- [ ] **TDD Criteria:** `test_creation.py` で検証すべき「依存未達時のSkip」「APIエラー時のロールバック」ケースが記述されていること。

### 5.2. Automated Tests
- `grep "DAG" docs/specs/logic/creation_logic.md`
- `grep "Atomic Move" docs/specs/logic/creation_logic.md`
