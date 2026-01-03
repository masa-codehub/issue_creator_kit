---
title: "原子的なアーカイブ（一括移動・ロールバック）のロジック実装"
labels: ["task", "P1", "BACKENDCODER"]
roadmap: "reqs/roadmap/_inbox/roadmap-adr003-task-lifecycle.md"
task_id: "T2-3"
depends_on: ["issue-T2-2.md"]
status: "Draft"
---
# {{title}}

## 1. 目的
- **To-be**: 起票と移動を分離し、全件成功時のみ移動するロジックを実現し、T2-2 のテストをパスさせる。

## 5. 検証手順
- `pytest tests/unit/usecase/test_atomic_archiving.py` がパスすること。
