---
title: "docs(arch): 詳細設計書（インターフェース定義）の実装一致（read_document等）"
status: "Open"
roadmap: "reqs/roadmap/active/roadmap-adr002-document-approval-flow.md"
task_id: "T5-1"
labels: ["documentation", "ADR-002"]
---

## 状況 / Context
`docs/specs/interface-spec.md` が旧来の `utils.py` ベースの記述になっている。これを現在の `FileSystemAdapter` および `GitHubAdapter` の実装と完全に一致させる必要がある。

## 期待される成果物 / Deliverables
- `docs/specs/interface-spec.md` の全面刷新
    - **FileSystemAdapter**: `read_document`, `save_document`, `update_metadata`, `safe_move_file` の正確なシグネチャ定義。
    - **GitHubAdapter**: `create_issue` の定義を追加（ADR-002 の核心機能）。
    - **Document Domain**: `parse`, `to_string` の役割を明記。
    - 削除済みファイル (`utils.py`, `create_issues.py`) への言及をすべて削除。

## 検証基準 / Verification Criteria
- メソッド名、引数の型、戻り値が `src/issue_creator_kit/` 配下の実体と 100% 一致していること。
- 「スクリプト」という用語が「Adapter/Usecase」に置換されていること。