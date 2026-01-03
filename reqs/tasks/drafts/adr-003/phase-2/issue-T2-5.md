---
title: "フェーズ連鎖（次フェーズ検知・PR作成）のロジック実装"
labels: ["task", "P1", "BACKENDCODER"]
roadmap: "reqs/roadmap/_inbox/roadmap-adr003-task-lifecycle.md"
task_id: "T2-5"
depends_on: ["issue-T2-4.md"]
status: "Draft"
---
# {{title}}

## 1. 目的
- **To-be**: メタデータに基づき次フェーズを `_queue` に移動し、PR を自動起票するロジックを実装し、T2-4 をパスさせる。

## 5. 検証手順
- `pytest tests/unit/usecase/test_phase_chaining.py` がパスすること。
