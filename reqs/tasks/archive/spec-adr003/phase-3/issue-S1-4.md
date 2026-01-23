---
title: "[Spec] Define Roadmap Sync Logic (Regex & WBS Update)"
labels:
  - task
  - TECHNICAL_DESIGNER
roadmap: "docs/specs/plans/20260122-spec-adr003-plan.md"
task_id: "S1-4"
depends_on: ["issue-S1-2.md"]
next_phase_path: ""
status: "Draft"
---

## 1. Goal & Context (Why & What)

### Goal
- `RoadmapSyncUseCase` の仕様を定義し、Markdown の WBS テーブルを安全に更新するための置換ルールを確定させる。

### As-is (現状)
- 「リンクを置換する」という方針はあるが、具体的な正規表現や、テーブルの行フォーマットが異なる場合の対応が曖昧。

### To-be (あるべき姿)
- `docs/specs/logic/roadmap_sync_logic.md` が作成され、以下のロジックが定義されている。
    - **Pattern Matching**: Markdown リンク `[...](path/to/file.md)` を検出し、`drafts/` から `archive/` へパスを置換する正規表現。
    - **Issue Mapping**: リンクの末尾に `(#123)` を追記するフォーマット。
    - **Idempotency**: 既に置換済みのリンクを二重に置換しないためのガード。

### Design Evidence
- [Architecture Plan Section 4 (Behavior)](../../../../../docs/architecture/plans/20260122-adr003-plan.md)
- [Handover Doc Section 2.2](../../../../../docs/handovers/arch-to-spec.md)

## 2. Input Context (資料 & 情報)
- **Common Definitions**: `docs/specs/plans/20260122-spec-adr003-plan.md`
- **Existing Roadmaps**: `reqs/roadmap/active/*.md` (現状のテーブル形式の確認)

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- ロードマップ全体（ヘッダー等）を書き換えないこと。あくまで WBS テーブル内の、対象タスクに対応する行のみを置換対象とする。

### 3.2. Implementation Steps (実行手順)
1.  **Define Regex Patterns**: 入力パスと出力パスのペア、および Issue 番号追記のパターンを定義。
2.  **Edge Case Handling**: 同一ファイル名のタスクが複数ある場合や、既にリンクが `archive/` を指している場合の挙動。
3.  **Validation**: 置換対象が見つからなかった場合の警告/エラー方針。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/spec-adr003-implementation`
- **Feature Branch**: `feature/task-S1-4-roadmap-sync-spec`

## 5. Verification & DoD (完了条件)
- [ ] 「テーブル内の相対リンクが、Draft から Archive へ正確に置換されるテストケース」が検証基準に含まれている。
- [ ] 置換後のリンク文字列の期待値（例: `[Title](../../tasks/archive/file.md) (#123)`）が明示されている。
