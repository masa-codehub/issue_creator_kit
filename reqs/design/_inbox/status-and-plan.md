---
id: status-memo-20260206
title: "現状整理と今後のプロセス方針"
status: Draft
date: 2026-02-06
---
# 現状整理と今後のプロセス方針

## 1. 設計・タスク管理の基本思想
- **計画 (Plans)**: `docs/**/plans/` に配置。設計の意図や分割方針を示す「参照用ドキュメント」。WBS等の進捗管理は行わない（二重管理の廃止）。
- **タスク案 (Issue Drafts)**: `reqs/tasks/adr-xxx/` に配置。GitHub Issueを起票するための「予約票」。
- **実行事実 (Active SSOT)**: GitHub Issues。進捗、親子関係、ステータスの唯一の正解とする。

## 2. 現状の承認フロー
- **ルール**: `reqs/design/_inbox` から `_approved` への移動は、自動スクリプトではなく **手動のプルリクエストとマージ** によって行う。
- **背景**: 物理的なディレクトリ移動（Gitマージ）をもって「承認」と定義し、不透明な自動移動を排除する。

## 3. 段階的な改善ロードマップ (ADR-008 〜 ADR-012)

### STEP 1: ADR-008 - Cleanup & Scanner Foundation
- **内容**: 負債（`auto-approve-docs.yml`、不要なUseCase/CLIコマンド、書き戻しロジック）の完全削除。
- **技術**: `diff-tree` に依存しない、`reqs/` フォルダの物理走査ベースのスキャナー基盤の構築。

### STEP 2: ADR-009 - ADR L1 Automation & Glue Labels
- **内容**: `_approved` にマージされた ADR の L1 Issue 自動起票。
- **技術**: 接着剤ラベル (`adr:xxx`) の自動生成と、GitHub 検索による冪等性（二重起票防止）の確保。

### STEP 3: ADR-010 - Task Activation & Issue ID Propagation
- **内容**: `reqs/tasks/` 内のタスク (L2/L3) の自動起票。
- **技術**: 一時IDを用いた依存解決と、起票後の GitHub Issue 番号への置換・アーカイブ時のリネーム。

### STEP 4: ADR-011 - Context & Metadata Integration
- **内容**: Issue 本文への依存チェックリスト (`- [ ] #111`) の自動挿入。
- **技術**: 静的な属性ラベル (`arch`, `spec`, `tdd`) の付与によるメタデータ統合。

### STEP 5: ADR-012 - Gemini Relay (Auto-Pilot)
- **内容**: 起動ラベル `gemini` への統合と、Actions によるクローズ検知・リレー。
- **技術**: エージェントの自律実行リレーの完成。

## 4. 直近の作業予定（TODO）
1. ADR-008 〜 012 の草案を `_inbox` に作成。
2. ADR-008 に基づくクリーンアップの実施。
