---
title: "docs(arch): メタデータ操作ロジック仕様をハイブリッドパース実態に同期"
status: "Open"
roadmap: "reqs/roadmap/active/roadmap-adr002-document-approval-flow.md"
task_id: "T5-2"
labels: ["documentation", "ADR-002"]
---

## 状況 / Context
`docs/specs/metadata-logic-spec.md` が外部ライブラリ (`python-frontmatter`) への完全依存を前提としている。実態は、独自実装のハイブリッドパース（YAML + Markdown List）を行っており、ドキュメントが仕様として機能していない。

## 期待される成果物 / Deliverables
- `docs/specs/metadata-logic-spec.md` の更新
    - YAML Frontmatter と Markdown List の**優先順位**（実装ロジック）を明記。
    - 実装で利用している正規表現パターンの記述。
    - パース失敗時のフォールバック挙動の追記。

## 検証基準 / Verification Criteria
- `Document.parse` のソースコードを読み、その振る舞いが正確にドキュメント化されていること。