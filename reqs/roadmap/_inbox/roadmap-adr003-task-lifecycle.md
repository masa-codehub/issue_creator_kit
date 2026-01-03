# 実装・リファクタリング計画: タスクのライフサイクル管理 (ADR-003)

このドキュメントは、承認済みの ADR-003 を安全に実現するための、段階的な手順と WBS を定義します。

- **Status**: 策定中
- **Target Design**: [ADR-003](../../design/_approved/adr-003-task-and-roadmap-lifecycle.md) (Updated v2: Self-Propelling Workflow)
- **Last Updated**: 2026-01-03

## 1. 実装戦略の要約
「一成果物一タスク」の原則に従い、全ての工程を原子的なステップに分解します。
ADR-003 v2 で定義された「フェーズ連鎖（Auto-PR）」と「原子的な一括アーカイブ」の実現を中核に据え、Phase 1 では実装を一切行わず、詳細設計とテスト要件の定義に充てます。
実装は Phase 2 以降とし、Phase 1 で確定させた「検証基準」をパスさせることを唯一のゴールとします。

## 2. 実装フェーズとWBS (The Journey)

### Phase 1: 詳細設計とテスト要件の定義
(詳細済み - 前回の出力を継承)
**WBS**
| Task ID | Category | タスク内容 | 成果物 | 依存先 | Issue案リンク |
| :---: | :---: | :--- | :--- | :---: | :--- |
| T1-1 | Setup | Phase 1 基点ブランチ `feature/phase-1-foundation` の作成 | ブランチ | - | [issue-T1-1.md](../../tasks/drafts/adr-003/phase-1/issue-T1-1.md) |
| T1-2 | Spike | GitHub API によるブランチ作成・PR作成の実現可能性調査 | 調査メモ | T1-1 | [issue-T1-2.md](../../tasks/drafts/adr-003/phase-1/issue-T1-2.md) |
| T1-3 | Pre | 原子的なアーカイブとフェーズ連鎖の論理フロー設計 | `reqs/design/_inbox/design-003-logic.md` | T1-2 | [issue-T1-3.md](../../tasks/drafts/adr-003/phase-1/issue-T1-3.md) |
| T1-4 | Pre | 制御用メタデータスキーマ定義とテンプレート更新 | `reqs/tasks/template/issue-draft.md` | T1-3 | [issue-T1-4.md](../../tasks/drafts/adr-003/phase-1/issue-T1-4.md) |
| T1-5 | Pre | インフラ層（Git/GitHub Adapter）のインターフェース定義 | `docs/specs/adr-003-infra-interface.md` | T1-3 | [issue-T1-5.md](../../tasks/drafts/adr-003/phase-1/issue-T1-5.md) |
| T1-6 | Pre | 全テストシナリオ（正常・異常・境界値）の定義 | `docs/specs/adr-003-test-criteria.md` | T1-4, T1-5 | [issue-T1-6.md](../../tasks/drafts/adr-003/phase-1/issue-T1-6.md) |
| T1-7 | Review | 設計・テスト要件の最終承認と Main へのマージ | PRマージ | T1-6 | [issue-T1-7.md](../../tasks/drafts/adr-003/phase-1/issue-T1-7.md) |

### Phase 2: テスト駆動実装と検証
- **Goal (狙い)**: Phase 1 で定義された検証基準を 100% 満たす実装を完了する。
- **Deliverables (成果物)**: テストコード、リファクタリングされた UseCase、新規 Auto-PR ロジック。
- **Gate (承認条件)**: 定義された全てのテスト（特に異常系）がパスし、マニュアル検証で動作が証明されること。

**WBS**
| Task ID | Category | タスク内容 | 成果物 | 依存先 | Issue案リンク |
| :---: | :---: | :--- | :--- | :---: | :--- |
| T2-1 | Setup | Phase 2 基点ブランチ `feature/phase-2-foundation` の作成 | ブランチ | T1-7 | [issue-T2-1.md](../../tasks/drafts/adr-003/phase-2/issue-T2-1.md) |
| T2-2 | Impl | 原子的なアーカイブ（Atomic Archiving）の単体テスト実装 | `tests/unit/usecase/test_atomic_archiving.py` | T2-1 | [issue-T2-2.md](../../tasks/drafts/adr-003/phase-2/issue-T2-2.md) |
| T2-3 | Impl | 原子的なアーカイブ（一括移動・ロールバック）のロジック実装 | `src/issue_creator_kit/usecase/creation.py` | T2-2 | [issue-T2-3.md](../../tasks/drafts/adr-003/phase-2/issue-T2-3.md) |
| T2-4 | Impl | フェーズ連鎖（Auto-PR）の単体テスト実装 | `tests/unit/usecase/test_phase_chaining.py` | T2-3 | [issue-T2-4.md](../../tasks/drafts/adr-003/phase-2/issue-T2-4.md) |
| T2-5 | Impl | フェーズ連鎖（次フェーズ検知・PR作成）のロジック実装 | `src/issue_creator_kit/usecase/workflow.py` | T2-4 | [issue-T2-5.md](../../tasks/drafts/adr-003/phase-2/issue-T2-5.md) |
| T2-6 | Verify | 統合検証（実際に `_queue` に複数フォルダを配置しての動作確認） | 検証ログ | T2-5 | [issue-T2-6.md](../../tasks/drafts/adr-003/phase-2/issue-T2-6.md) |
| T2-7 | Review | Phase 2 完了承認と Main へのマージ | PRマージ | T2-6 | [issue-T2-7.md](../../tasks/drafts/adr-003/phase-2/issue-T2-7.md) |

### Phase 3: リファクタリングと SSOT 同期
- **Goal (狙い)**: 実装後のシステムを整理し、最新の運用ガイドラインを確立する。
- **Deliverables (成果物)**: 最新化されたシステムコンテキスト、開発ガイド、クリーンなコードベース。
- **Gate (承認条件)**: 旧プロトタイプコードが完全に削除され、ドキュメントと実装に矛盾がないこと。

**WBS**
| Task ID | Category | タスク内容 | 成果物 | 依存先 | Issue案リンク |
| :---: | :---: | :--- | :--- | :---: | :--- |
| T3-1 | Setup | Phase 3 基点ブランチ `feature/phase-3-foundation` の作成 | ブランチ | T2-7 | [issue-T3-1.md](../../tasks/drafts/adr-003/phase-3/issue-T3-1.md) |
| T3-2 | Clean | デバッグ用コードの削除とコードスタイルの最終調整 | クリーンコード | T3-1 | [issue-T3-2.md](../../tasks/drafts/adr-003/phase-3/issue-T3-2.md) |
| T3-3 | Docs | システムコンテキスト（境界・用語・フロー図）の最新化 | `docs/system-context.md` | T3-2 | [issue-T3-3.md](../../tasks/drafts/adr-003/phase-3/issue-T3-3.md) |
| T3-4 | Docs | 開発者向けセットアップ・運用ガイドの更新 | `docs/guides/` | T3-3 | [issue-T3-4.md](../../tasks/drafts/adr-003/phase-3/issue-T3-4.md) |
| T3-5 | Review | ロードマップの完了宣言とアーカイブ | ロードマップ移動 | T3-4 | [issue-T3-5.md](../../tasks/drafts/adr-003/phase-3/issue-T3-5.md) |

## 3. リスク管理とロールバック
- **リスク**: 一括移動フェーズで Git の競合が発生し、アーカイブに失敗する。
- **対策**: 移動は常に最新の `main` をベースにした作業ブランチで行い、ECK（エージェント）が自動でコンフリクト解消を試みる。

## 4. 移行完了の定義
- タスクがフェーズを跨いで自動的に PR 化され、プロジェクトが自律的に進行する状態。