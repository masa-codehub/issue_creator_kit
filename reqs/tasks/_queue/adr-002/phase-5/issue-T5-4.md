---
title: "chore: pyproject.toml の Lint 設定クリーンアップ"
status: "Open"
roadmap: "reqs/roadmap/active/roadmap-adr002-document-approval-flow.md"
task_id: "T5-4"
labels: ["cleanup", "ADR-002"]
---

## 状況 / Context
削除済みのレガシーファイルに対する Lint 無視設定が `pyproject.toml` に残存しており、保守上のノイズとなっている。

## 期待される成果物 / Deliverables
- `pyproject.toml` の更新
    - `tool.ruff.lint.per-file-ignores` から、存在しないファイル（`scripts/*.py`, `utils.py`）への参照を完全に削除。

## 検証基準 / Verification Criteria
- `ruff check .` が正常に終了し、不要な設定による警告が出ないこと。