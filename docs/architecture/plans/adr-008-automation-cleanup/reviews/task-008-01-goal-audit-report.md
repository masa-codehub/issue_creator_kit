# 目標定義監査レポート - Archive Obsolete Architecture Docs

## 1. ドキュメントの要件 (Requirements for Documentation)
- [x] **アウトプット定義:** アーカイブされた4つの Markdown ファイルの修正が目標となっている。
  - **根拠:** `task-008-01-goal-definition.md` に対象ファイル名が明記されている。
- [x] **記述の観点:** DEPRECATED 警告と相対リンクの修正が記述項目として挙げられている。
  - **根拠:** `task-008-01-goal-definition.md` の Outcome セクション。

## 2. 整合性と品質 (Consistency & Quality)
- [x] **SSOT整合性:** ADR-008 の「クリーンアップ」方針に完全に合致している。
  - **根拠:** `design-brief.md` の 3.1 節。
- [x] **テンプレート:** 既存のドキュメントの修正であるため、特定の新規テンプレートは不要だが、リンク修正のガイドラインが示されている。
  - **根拠:** `task-008-01-goal-definition.md` の Steps セクション。

## 3. 改善提案 (Improvement Proposals)
- **リンク修正の具体化:**
  - **現状の問題:** `arch-state-003-task-lifecycle.md` 内のリンクが root 相対のままである可能性。
  - **改善案:** `arch-structure-007-metadata.md` への参照を `../arch-structure-007-metadata.md` に書き換える。
