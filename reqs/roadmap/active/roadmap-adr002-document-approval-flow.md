# 実装・リファクタリング計画: ドキュメント承認フローの自動化 (For ADR-002)

このドキュメントは、承認済みの設計決定を安全に実現するための、段階的な手順と WBS を定義します。

- **Status**: 実行中
- **Target Design**: [ADR-002](../../design/_approved/adr-002-document-approval-flow.md)
- **Last Updated**: 2025-12-29

## 1. 実装戦略の要約
既存のシェルスクリプト（`sed`ベース）による暫定的な承認フローを、`issue-creator-kit` パッケージ内の堅牢な Python ロジックに置き換えます。
安全な移行のため、まず Phase 1 で関数インターフェースと詳細なテスト仕様を「設計」として確定させ、実装時の不確実性を排除します。
その後、段階的に基盤実装、コアロジック実装、ワークフロー刷新へと進めます。

## 2. 実装フェーズとWBS (The Journey)

### Phase 1: 設計とテスト要件の確定 (Design & Test Criteria)
- **Goal (狙い)**: 実装開始前にメタデータ操作の「インターフェース定義」と「成功の定義（テストケース）」を完全に一致させ、手戻りを排除する。
- **Input (前提)**: ADR-002, 既存の `create_issues.py`
- **Deliverables (成果物)**:
    - **インターフェース定義案**: `utils.py` に実装すべき関数のシグネチャ（引数・戻り値・例外）の定義。
    - **検証基準リスト (Acceptance Criteria)**: 正常系・異常系・境界値を含むテストシナリオの言語化。
- **Gate (承認条件)**: 定義されたインターフェースとテストシナリオが、ADR-002 の意図を完全に網羅していると合意されること。

**WBS**
| Task ID | Category | タスク内容 | 対象ファイル | 依存先 | Issue案リンク |
| :---: | :---: | :--- | :--- | :---: | :--- |
| T1-1 | Setup | [x] 作業ブランチ `feature/phase-1-foundation` の作成 | - | - | [issue-T1-1.md](../../tasks/archive/adr-002/phase-1/issue-T1-1.md) |
| T1-2 | Spike | [x] 既存ロジックの調査とメタデータ更新用正規表現の机上検証 | - | T1-1 | [issue-T1-2.md](../../tasks/archive/adr-002/phase-1/issue-T1-2.md) |
| T1-3 | Pre | 共通ユーティリティ関数のインターフェース設計（シグネチャ定義） | - | T1-2 | [issue-T1-3.md](../../tasks/archive/adr-002/phase-1/issue-T1-3.md) |
| T1-4 | Pre | 網羅的なテストケース（正常系・異常系）の定義作成 | - | T1-3 | [issue-T1-4.md](../../tasks/archive/adr-002/phase-1/issue-T1-4.md) |
| T1-5 | Review | 設計内容のレビューと Phase 2 (実装フェーズ) の計画確定 | - | T1-4 | [issue-T1-5.md](../../tasks/archive/adr-002/phase-1/issue-T1-5.md) |

### Phase 2: 基盤実装とコアロジックの構築 (Foundation & Core Implementation)
- **Goal (狙い)**: Phase 1 で確定した設計に基づき、ユーティリティおよび承認プロセッサの実装・単体テストを完遂する。
- **Input (前提)**: Phase 1 で確定したインターフェース定義とテストケース。
- **Deliverables (成果物)**:
    - **`utils.py` の実装**: メタデータ解析・置換の共通関数。
    - **`process_approvals.py` の実装**: ファイル移動、Status更新、Issue起票の統合ロジック。
    - **単体テストコード**: Phase 1 で定義したケースを全て網羅したテスト。
- **Gate (承認条件)**: 全ての単体テストがパスし、既存の `create_issues.py` が新ユーティリティ経由で正常動作すること。

**WBS**
| Task ID | Category | タスク内容 | 対象ファイル | 依存先 | Issue案リンク |
| :---: | :---: | :--- | :--- | :---: | :--- |
| T2-1 | Setup | 作業ブランチ `feature/phase-2-implementation` の作成 | - | T1-5 | [issue-T2-1.md](../../tasks/drafts/adr-002/phase-2/issue-T2-1.md) |
| T2-2 | Impl | `utils.py` の実装と単体テスト実行 | `src/issue_creator_kit/utils.py` | T2-1 | [issue-T2-2.md](../../tasks/drafts/adr-002/phase-2/issue-T2-2.md) |
| T2-3 | Impl | `process_approvals.py` の実装と単体テスト実行 | `src/issue_creator_kit/scripts/process_approvals.py` | T2-2 | [issue-T2-3.md](../../tasks/drafts/adr-002/phase-2/issue-T2-3.md) |
| T2-4 | Verify | 既存 `create_issues.py` のリファクタリングと回帰テスト | - | T2-3 | [issue-T2-4.md](../../tasks/drafts/adr-002/phase-2/issue-T2-4.md) |
| T2-5 | Review | 実装コードのレビューと Phase 3 計画の確定 | - | T2-4 | [issue-T2-5.md](../../tasks/drafts/adr-002/phase-2/issue-T2-5.md) |

### Phase 3: ワークフローの差し替えと統合 (Swap & Release)
- **Goal (狙い)**: CI/CDパイプラインを刷新し、本番環境で Python ベースの安全な承認フローを稼働させる。
- **Input (前提)**: 検証済みの実装コード。
- **Deliverables (成果物)**:
    - **CLI コマンド追加 (`cli.py`)**: `issue-kit approve` の追加。
    - **新ワークフロー定義**: GitHub Actions ワークフローの置換。
- **Gate (承認条件)**: ローカル統合テスト（`act`等）において、ドキュメント移動からIssue起票までの全フローが成功すること。

**WBS**
| Task ID | Category | タスク内容 | 対象ファイル | 依存先 | Issue案リンク |
| :---: | :---: | :--- | :--- | :---: | :--- |
| T3-1 | Setup | 作業ブランチ `feature/phase-3-integration` の作成 | - | T2-5 | [issue-T3-1.md](../../tasks/drafts/adr-002/phase-3/issue-T3-1.md) |
| T3-2 | Impl | CLI サブコマンド `approve` の統合 | `src/issue_creator_kit/cli.py` | T3-1 | [issue-T3-2.md](../../tasks/drafts/adr-002/phase-3/issue-T3-2.md) |
| T3-3 | Impl | GitHub Actions ワークフローの差し替え | `.github/workflows/auto-approve-docs.yml` | T3-2 | [issue-T3-3.md](../../tasks/drafts/adr-002/phase-3/issue-T3-3.md) |
| T3-4 | Review | 統合検証結果のレビューと Phase 4 計画の確定 | - | T3-3 | [issue-T3-4.md](../../tasks/drafts/adr-002/phase-3/issue-T3-4.md) |

### Phase 4: 資産の同期とクリーンアップ (Sync & Cleanup)
- **Goal (狙い)**: 配布用テンプレートを最新化し、旧負債を完全に排除する。
- **Input (前提)**: 稼働中の新ワークフロー。
- **Deliverables (成果物)**:
    - **テンプレート更新**: `assets/` 内の最新化。
- **Gate (承認条件)**: 全てのドキュメントとコードが一貫した最新状態にあること。

**WBS**
| Task ID | Category | タスク内容 | 対象ファイル | 依存先 | Issue案リンク |
| :---: | :---: | :--- | :--- | :---: | :--- |
| T4-1 | Setup | 作業ブランチ `feature/phase-4-cleanup` の作成 | - | T3-4 | [issue-T4-1.md](../../tasks/drafts/adr-002/phase-4/issue-T4-1.md) |
| T4-2 | Clean | `assets/workflows` 内のテンプレート同期と旧スクリプト削除 | - | T4-1 | [issue-T4-2.md](../../tasks/drafts/adr-002/phase-4/issue-T4-2.md) |
| T4-3 | Review | 最終成果物のレビューとロードマップ完了承認 | - | T4-2 | [issue-T4-3.md](../../tasks/drafts/adr-002/phase-4/issue-T4-3.md) |

## 3. リスク管理とロールバック
- **リスク**: 設計（インターフェース）の考慮漏れによる実装時の大幅な修正。
- **対策/切り戻し**: Phase 1 で「実装エージェントが迷わないレベル」まで詳細に定義を行い、早期レビューを受ける。
- **リスク**: 正規表現によるメタデータ置換の誤爆。
- **対策/切り戻し**: Phase 1 で定義するテストケースに、エッジケース（複雑な Markdown 構造）を必ず含める。

## 4. 完了の定義
- [ ] 承認済みドキュメントのステータスが「承認済み」に自動更新される。
- [ ] 承認されたドキュメントに対応するトラッキング Issue が GitHub 上に作成される。
- [ ] ドキュメント内に作成された Issue 番号（例: `#123`）が追記される。
- [ ] 全てのテスト（Unit/Integration）がパスする。
- [ ] アセット内のテンプレートが刷新されている。