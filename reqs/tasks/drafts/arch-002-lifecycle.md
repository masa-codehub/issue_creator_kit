---
title: "[Arch] Visualize Document Lifecycle (State Diagram) for ADR-002"
status: open
priority: normal
labels: ["architecture", "adr-002"]
---

# 目的 / Objective
ドキュメントのステータスと物理配置の遷移を状態遷移図として可視化する。

# 完了条件 / Acceptance Criteria
- `docs/architecture/arch-state-doc-lifecycle.md` が作成されていること。
- `Status` フィールドの値（Draft, Approved）とディレクトリ（`_inbox`, `_approved`）の対応が表現されていること。

# 手順 / Steps
1. `docs/template/arch-state.md` を使用する。
2. ドキュメントがマージされる前後の「状態（State）」を定義する。
3. `arch-refactoring` を呼び出して品質を向上させる。

# ターゲット読者
**Spec Strategist (仕様戦略家)**: ファイル移動ロジックやステータスバリデーションの仕様を策定する際の入力とする。
