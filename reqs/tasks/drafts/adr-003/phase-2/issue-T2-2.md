---
title: "原子的なアーカイブ（Atomic Archiving）の単体テスト実装"
labels: ["task", "P1", "BACKENDCODER"]
roadmap: "reqs/roadmap/_inbox/roadmap-adr003-task-lifecycle.md"
task_id: "T2-2"
depends_on: ["issue-T2-1.md"]
status: "Draft"
---
# {{title}}

## 1. 目的
- **To-be**: `docs/specs/adr-003-test-criteria.md` に基づき、一括移動の正常系・異常系を検証するテストコードを先行実装する。

## 5. 検証手順
- `pytest tests/unit/usecase/test_atomic_archiving.py` が（実装未完了のため）失敗することを確認。
