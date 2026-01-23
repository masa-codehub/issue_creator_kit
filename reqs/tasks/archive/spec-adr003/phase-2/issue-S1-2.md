---
title: "[Spec] Define Issue Creation Logic (Virtual Queue & Atomicity)"
labels:
  - task
  - TECHNICAL_DESIGNER
roadmap: "docs/specs/plans/20260122-spec-adr003-plan.md"
task_id: "S1-2"
depends_on: ["issue-S1-1.md"]
next_phase_path: ""
status: "Draft"
---

## 1. Goal & Context (Why & What)

### Goal
- `IssueCreationUseCase` の詳細な動作アルゴリズムを定義し、「仮想キュー検知」「依存解決」「原子的な起票」を確実に実装できるようにする。

### As-is (現状)
- ADR-002 の「承認プロセス」としての起票ロジックはあるが、ADR-003 の「Git 差分ベースの一括起票」および「Fail-fast」の厳密なアルゴリズムが未定義。

### To-be (あるべき姿)
- `docs/specs/logic/issue_creation_logic.md` が作成され、以下のロジックが定義されている。
    - **Detection**: `GitAdapter` から得たファイルリストのうち、「採番済み (`issue` フィールドあり)」を除外するフィルタリング。
    - **Dependency Resolution**: `depends_on` に基づく Topological Sort。
    - **Atomicity**: 全件の `create_issue` 成功後のみ、ファイルへの書き戻しを行うトランザクション境界。
    - **Error Handling**: API 失敗時に例外を送出し、Git を更新せずに終了する手順。

### Design Evidence
- [Creation Behavior Diagram](../../../docs/architecture/arch-behavior-003-creation.md)
- [Handover Doc Section 1.1](../../../docs/handovers/arch-to-spec.md)

## 2. Input Context (資料 & 情報)
- **Common Definitions**: `docs/specs/plans/20260122-spec-adr003-plan.md`
- **Adapter Spec (Ref)**: `docs/specs/components/infra_adapters.md`

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- 1件ごとにコミットする挙動は ADR-003 で禁止されているため、一括コミットのみを許容する仕様とすること。

### 3.2. Implementation Steps (実行手順)
1.  **Define Algorithm**: 入力ファイルリストから最終的なコミットまでの擬似コード、または詳細なステップを記述。
2.  **Verify Topological Sort**: 循環参照があった場合の例外挙動を定義。
3.  **Define Fail-fast Zone**: どのステップでエラーが起きたらプロセスを終了するかを明記。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/spec-adr003-implementation`
- **Feature Branch**: `feature/task-S1-2-creation-logic-spec`

## 5. Verification & DoD (完了条件)
- [ ] 「1件起票に成功し、2件目で失敗した場合に、1件目の番号もファイルに書き込まれないこと」が検証基準（TDD観点）として含まれている。
