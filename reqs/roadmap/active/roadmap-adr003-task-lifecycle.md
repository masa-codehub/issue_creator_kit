# 実装・リファクタリング計画: 仮想キューと自己推進型ワークフロー (ADR-003)

このドキュメントは、承認済みの ADR-003 v3（仮想キュー、自己推進、再帰的ブランチ戦略）を安全に実現するための、段階的な手順と WBS を定義します。

- **Status**: 策定中
- **Target Design**: [ADR-003](../../design/_approved/adr-003-task-and-roadmap-lifecycle.md)
- **Last Updated**: 2026-01-03

## 1. 実装戦略の要約
物理フォルダとしての `_queue/` を廃止し、GitHub Actions が `archive/` へのマージ差分を検知して起票を行う「仮想キュー」へ移行します。
「一成果物一タスク」の原則を徹底し、Phase 1 では詳細設計（Logic, Schema, Interface）とテスト要件を確定させます。
Phase 2 では、実装を「差分検知」「一括起票」「ロードマップ同期」「Auto-PR」の 4 つの独立したロジックに分解して TDD で進めます。

## 2. 実装フェーズとWBS (The Journey)

### Phase 1: 詳細設計とテスト要件の定義
- **Goal (狙い)**: 「マージ差分からの起票」と「最終タスクからの Auto-PR」の論理的整合性を 100% 確定させる。
- **Input (前提)**: ADR-003 v3
- **Deliverables (成果物)**: 詳細設計書、テスト仕様書、更新された Issue テンプレート。
- **Gate (承認条件)**: 全ての設計がマージされ、実装者が迷わずテストコードを書ける状態。

**WBS**
| Task ID | Category | タスク内容 | 成果物 | 依存先 | リンク / Issue |
| :---: | :---: | :--- | :--- | :---: | :--- |
| T1-1 | Setup | Phase 1 Foundation ブランチ `feature/phase-1-foundation` の作成 | ブランチ | - | [issue-T1-1.md](../../tasks/archive/adr-003/phase-1/issue-T1-1.md) (#92) |
| T1-2 | Spike | `git diff` によるマージ差分（`archive/` への新規ファイル）特定ロジックの実機検証 | 調査メモ | T1-1 | [issue-T1-2.md](../../tasks/archive/adr-003/phase-1/issue-T1-2.md) (#93) |
| T1-3 | Pre | 仮想キューとフェーズ連鎖の論理フロー詳細設計（エラー時の停止位置含む） | `design-003-logic.md` | T1-2 | [issue-T1-3.md](../../tasks/archive/adr-003/phase-1/issue-T1-3.md) (#94) |
| T1-4 | Pre | インフラ層（PR作成・ブランチ操作）のインターフェース定義（シグネチャ確定） | `infra-interface.md` | T1-3 | [issue-T1-4.md](../../tasks/archive/adr-003/phase-1/issue-T1-4.md) (#95) |
| T1-5 | Pre | 制御用メタデータスキーマ確定（`next_phase_path`）とテンプレート最終更新 | `reqs/tasks/template/issue-draft.md` | T1-3 | [issue-T1-5.md](../../tasks/archive/adr-003/phase-1/issue-T1-5.md) (#96) |
| T1-6 | Pre | 全テストシナリオ（正常・異常・境界値）の定義（期待されるログ出力含む） | `test-criteria.md` | T1-4, T1-5 | [issue-T1-6.md](../../tasks/archive/adr-003/phase-1/issue-T1-6.md) (#97) |
| T1-7 | Review | Phase 1 成果物の最終監査と main マージ | Phase 1 PRマージ | T1-6 | [issue-T1-7.md](../../tasks/archive/adr-003/phase-1/issue-T1-7.md) (#98) |

### Phase 2: テスト駆動実装と検証
- **Goal (狙い)**: 仮想キュー方式での起票と、フェーズの自動連鎖を完全に実現する。
- **Input (前提)**: Phase 1 の設計書とテスト要件。
- **Deliverables (成果物)**: `WorkflowUseCase` 拡張、`GitHubAdapter` 拡張、統合テスト。
- **Gate (承認条件)**: 最終タスクのマージにより、次フェーズの PR が自動作成されるサイクルの実証。

**WBS**
| Task ID | Category | タスク内容 | 成果物 | 依存先 |
| :---: | :---: | :--- | :--- | :---: |
| T2-1 | Setup | Phase 2 Foundation ブランチ `feature/phase-2-foundation` の作成 | ブランチ | T1-7 |
| T2-2 | Impl | マージ差分検知と一括起票（仮想キュー）の TDD 実装 | `creation.py` | T2-1 |
| T2-3 | Impl | ロードマップ WBS リンク自動置換ロジックの TDD 実装 | `roadmap_sync.py` | T2-2 |
| T2-4 | Impl | 次フェーズ PR 自動作成（Auto-PR）とブランチ自動作成ロジックの TDD 実装 | `workflow.py` | T2-3 |
| T2-5 | Impl | Issue起票オートメーション・ワークフローの新規作成 | `.github/workflows/issue-automator.yml` | T2-4 | [issue-T2-5.md](../../tasks/archive/adr-003/phase-2/issue-T2-5.md) (#124) |
| T2-6 | Verify | 統合検証（フェーズ 1→2 の自動リレー確認） | 検証ログ | T2-5 |
| T2-7 | Review | Phase 2 成果物の最終監査と main マージ | PRマージ | T2-6 |

### Phase 3: リファクタリングと SSOT 同期
- **Goal (狙い)**: 旧 `_queue` 方式の残骸を清掃し、システム全体の整合性を取る。
- **Input (前提)**: Phase 2 の完了。
- **Deliverables (成果物)**: 最新化された `system-context.md`、クリーンなコード。
- **Gate (承認条件)**: 旧コードが完全に削除され、ドキュメントと実装に矛盾がないこと。

**WBS**
| Task ID | Category | タスク内容 | 成果物 | 依存先 |
| :---: | :---: | :--- | :--- | :---: |
| T3-1 | Setup | Phase 3 Foundation ブランチ `feature/phase-3-foundation` の作成 | ブランチ | T2-7 |
| T3-2 | Clean | 物理 `_queue` フォルダ関連コードの完全削除 | コード削除 | T3-1 |
| T3-3 | Docs | システムコンテキストと運用ガイド（新しい起票手順）の最新化 | `docs/` 更新 | T3-2 |
| T3-4 | Review | ロードマップ完了宣言とアーカイブ | 移動 | T3-3 |

## 3. リスク管理とロールバック
- **リスク**: Auto-PR で無限ループ（例: P1 が完了して P1 を再度呼ぶ）が発生する可能性。
- **対策**: T1-3 の設計で「既処理フェーズの記録」または「パスの一方向性検証」を定義し、循環参照を物理的に防止する。
- **リスク**: 一括移動（Auto-PR作成）時の Git コンフリクト。
- **対策**: **Fail-fast 戦略**を採用する。自動解消は試みず、コンフリクトを検知した時点で処理を停止し、エラーログを出力して人間に手動解決を促す通知（Issue コメント等）を行う。これにより、誤ったマージによるリポジトリ破損を防ぐ。

## 4. 移行完了の定義
- 開発者がマージボタンを押すだけで、次のフェーズの準備が整う「自己推進状態」が確立されていること。
- ロードマップのリンクが常に最新の Issue を指し示していること。
