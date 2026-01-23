---
depends_on: []
issue: '#239'
labels:
- task
- TECHNICAL_DESIGNER
next_phase_path: ''
roadmap: docs/specs/plans/20260122-spec-adr003-plan.md
status: Draft
task_id: S1-5
title: '[Spec] Update Infrastructure Adapters Spec (Git & GitHub Enhancements)'
---

## 1. Goal & Context (Why & What)

### Goal
- Infrastructure 層のアダプター仕様を ADR-003 の要件に合わせて更新し、低レベルな Git 操作や GitHub API の抽象化を強化する。

### As-is (現状)
- ADR-002 ベースの仕様はあるが、`git diff-tree` や PR 作成時のレートリミット考慮、ブランチ作成の基点指定などの詳細が不足。

### To-be (あるべき姿)
- `docs/specs/components/infra_adapters.md` が更新され、以下のメソッド定義が含まれている。
    - **GitAdapter**:
        - `get_added_files(base_ref, head_ref, path)`: マージ差分の特定。
        - `checkout(branch, create, base)`: 基点ブランチを指定した作成・切り替え。
        - `move_file(src, dst)`: `git mv` 相当。
    - **GitHubAdapter**:
        - `create_pull_request(title, body, head, base)`: 自動連鎖用。
        - `Retry Policy`: レートリミット (429, およびヘッダーやボディでレートリミットと判断できる403) 時の内部リトライ挙動。

### Design Evidence
- [Structure Diagram](../../../../../docs/architecture/arch-structure-003-vqueue.md)
- [Handover Doc Section 2.1](../../../../../docs/handovers/arch-to-spec.md)

## 2. Input Context (資料 & 情報)
- **Common Definitions**: `docs/specs/plans/20260122-spec-adr003-plan.md`
- **Current Specs**: `docs/specs/components/infra_adapters.md`

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- Adapter 内でビジネスロジック（例: 「ステータスが Draft なら移動する」等）を実装させない。あくまで「物理的な移動」や「API コール」に徹する。

### 3.2. Implementation Steps (実行手順)
1.  **Refine Signatures**: 各メソッドの引数名、型、戻り値を確定。
2.  **Define Exception Mapping**: 基盤層の例外を `InfrastructureError` 等の独自例外にどう変換するかを記述。
3.  **Specify Retry Strategy**: GitHub API のリトライ回数や待機時間の推奨値を定義。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/spec-adr003-implementation`
- **Feature Branch**: `feature/task-S1-5-infra-adapter-spec`

## 5. Verification & DoD (完了条件)
- [ ] 「`git diff-tree` の出力形式の考慮」が注意書きとして含まれている。
- [ ] `create_pull_request` の戻り値（URL と 番号）が明記されている。
