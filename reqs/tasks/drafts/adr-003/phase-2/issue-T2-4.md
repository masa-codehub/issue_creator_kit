---
title: "フェーズ連鎖（Auto-PR）の単体テスト実装"
labels: ["task", "P1", "BACKENDCODER"]
roadmap: "reqs/roadmap/_inbox/roadmap-adr003-task-lifecycle.md"
task_id: "T2-4"
depends_on: ["issue-T2-3.md"]
status: "Draft"
---
# {{title}}

## 1. 目的
- **To-be**: 最終タスク検知から次フェーズの PR 作成までのフローを Mock を用いて検証するテストを実装する。

## 5. 検証手順
- `pytest tests/unit/usecase/test_phase_chaining.py` が失敗することを確認。
