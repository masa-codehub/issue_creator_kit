---
title: "[TDD] Implement Roadmap Sync Logic"
labels: ["gemini:tdd"]
roadmap: "docs/implementation/plans/adr-003/tdd-plan.md"
task_id: "T-5"
depends_on: ["issue-T-4.md"]
status: "Draft"
---

## 1. Goal & Context (Why & What)

### Goal
- タスク起票時に、ロードマップ（WBS）内のリンクパスを `drafts/` から `archive/` へ置換し、Issue 番号を追記するロジックを実装する。

### As-is (現状)
- ロードマップの手動更新が必要であり、リンク切れや番号の転記ミスが発生しやすい。

### To-be (あるべき姿)
- `RoadmapSyncUseCase` (または Creation UseCase の一部) が、正規表現を用いてロードマップファイルを安全に更新する。

### Design Evidence
- [Logic Spec](../../../../docs/specs/logic/roadmap_sync_logic.md)

## 2. Input Context (資料 & 情報)
- **Logic**: `src/issue_creator_kit/usecase/roadmap_sync.py`
- **Spec**: `docs/specs/logic/roadmap_sync_logic.md`

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- 単純な `str.replace` で置換すること（誤爆のリスクがあるため、Markdown リンク構文 `[text](path)` を解析すること）。

### 3.2. Implementation Steps (実行手順)
1.  **Red Phase**:
    - `tests/usecase/test_roadmap_sync.py` を作成。
    - ロードマップのサンプルテキストに対し、リンク置換と `(#123)` の追記が行われることを検証。
    - 既に置換済みの行が二重に置換されないことを検証。
2.  **Green Phase**:
    - 正規表現 `\[(.*?)\]\((.*drafts.*?)\)` を用いてリンクを特定し、`archive` へ置換するロジックを実装。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/impl-adr003`
- **Feature Branch**: `feature/task-T-5-roadmap-sync`

## 5. Verification & DoD (完了条件)
- [ ] ロードマップ内のリンクが正しく `archive/` を指すように更新されること。
- [ ] Issue 番号がリンクの横に追記されること。

## 6. TDD Scenarios
- **Scenario 1 (Sync)**:
    - Input: `| T-1 | [Task](drafts/t1.md) |`
    - Output: `| T-1 | [Task](archive/t1.md) (#101) |`
