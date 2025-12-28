# 実装・リファクタリング計画: ドキュメント承認フローの自動化 (For ADR-002)

このドキュメントは、承認済みの設計決定を安全に実現するための、段階的な手順と WBS を定義します。

- **Status**: 作成中
- **Target Design**: [ADR-002](reqs/_approve/adr-002-document-approval-flow.md)
- **Last Updated**: 2025-12-28

## 1. 実装戦略の要約
既存のシェルスクリプト（`sed`ベース）による暫定的な承認フローを、`issue-creator-kit` パッケージ内の堅牢な Python ロジックに置き換えます。
これにより、ADR-002 で定義された「トラッキング Issue の起票」および「Issue 番号のドキュメントへの自動追記」を確実に実現します。
安全な移行のため、まずコアロジックを実装し、単体テストで品質を担保した後に、GitHub Actions ワークフローを刷新します。

## 2. 実装フェーズとWBS (The Journey)

### Phase 1: 設計と基盤整備 (Design & Foundation)
- **Goal (狙い)**: メタデータ操作の「あるべき仕様」をコードレベル（ユーティリティ関数）で確立し、既存ロジックと共存可能な基盤を作る。
- **Input (前提)**: ADR-002, 既存の `create_issues.py`
- **Deliverables (成果物)**:
    - **共通ユーティリティ (`utils.py`)**:
        - **目的**: 正規表現による堅牢なメタデータ抽出・置換ロジックを提供するため。
    - **リファクタリングされた `create_issues.py`**:
        - **目的**: 新しいユーティリティを利用し、既存機能が回帰していないことを証明するため。
- **Gate (承認条件)**: ユーティリティの単体テストがパスし、既存スクリプトが新ユーティリティ経由で正常に動作すること。

**WBS**
| Task ID | Category | タスク内容 | 対象ファイル | 依存先 | Issue案リンク |
| :---: | :---: | :--- | :--- | :---: | :--- |
| T1-1 | Setup | 作業ブランチ `feature/phase-1-foundation` の作成 | - | - | [issue-adr002-T1-1.md](../_issues/issue-adr002-T1-1.md) |
| T1-2 | Spike | 既存のメタデータ解析ロジックの共通化検討 | `src/issue_creator_kit/scripts/create_issues.py` | T1-1 | [issue-adr002-T1-2-T1-3-T1-4.md](../_issues/issue-adr002-T1-2-T1-3-T1-4.md) |
| T1-3 | Pre | メタデータ置換およびファイル操作ユーティリティの実装 | `src/issue_creator_kit/utils.py` | T1-2 | [issue-adr002-T1-2-T1-3-T1-4.md](../_issues/issue-adr002-T1-2-T1-3-T1-4.md) |
| T1-4 | Verify | ユーティリティの単体テスト実装と実行 | `tests/unit/test_utils.py` | T1-3 | [issue-adr002-T1-2-T1-3-T1-4.md](../_issues/issue-adr002-T1-2-T1-3-T1-4.md) |
| T1-5 | Review | Phase 1 成果物のレビューと Phase 2 計画の確定 | - | T1-4 | [issue-adr002-T1-5.md](../_issues/issue-adr002-T1-5.md) |

### Phase 2: コアロジックの実装と検証 (Core Implementation & Verification)
- **Goal (狙い)**: 承認フローの全ロジック（移動、追記、APIコール）をPython上で完成させ、単体テストで品質を保証する。
- **Input (前提)**: Phase 1で確立された `utils.py`
- **Deliverables (成果物)**:
    - **承認プロセッサ (`process_approvals.py`)**:
        - **目的**: ファイル移動、Status更新、Issue起票の一連の流れを制御するため。
    - **単体テスト (`test_process_approvals.py`)**:
        - **目的**: GitHub APIやファイルシステムをモックし、ロジックの正当性を担保するため。
- **Gate (承認条件)**: 承認フローの全パターン（正常系、APIエラー系、メタデータ欠損系）のテストがパスすること。

**WBS**
| Task ID | Category | タスク内容 | 対象ファイル | 依存先 | Issue案リンク |
| :---: | :---: | :--- | :--- | :---: | :--- |
| T2-1 | Setup | 作業ブランチ `feature/phase-2-core` の作成と T1 のマージ | - | T1-5 | |
| T2-2 | Impl | ドキュメント承認プロセッサのコアロジック実装（移動・Status更新） | `src/issue_creator_kit/scripts/process_approvals.py` | T2-1 | |
| T2-3 | Impl | トラッキング Issue 起票・Issue番号追記機能の実装 | `src/issue_creator_kit/scripts/process_approvals.py` | T2-2 | |
| T2-4 | Verify | メタデータ更新と Issue ペイロードの単体テスト | `tests/unit/test_process_approvals.py` | T2-3 | |
| T2-5 | Review | Phase 2 成果物のレビューと Phase 3 計画の確定 | - | T2-4 | |

### Phase 3: ワークフローの差し替え (Swap & Release)
- **Goal (狙い)**: CI/CDパイプラインを切り替え、本番環境（GitHub Actions）で新ロジックを稼働させる。
- **Input (前提)**: 検証済みの `process_approvals.py`
- **Deliverables (成果物)**:
    - **CLI コマンド追加 (`cli.py`)**:
        - **目的**: `issue-kit approve` コマンドとして機能を外部公開するため。
    - **新ワークフロー定義 (`auto-approve-docs.yml`)**:
        - **目的**: 脆弱な `sed` コマンドを廃止し、Python CLI を呼び出す安全なフローへ切り替えるため。
- **Gate (承認条件)**: ローカルでの統合テスト（`act`等）またはテストリポジトリでの実行において、一連のフローが正常終了し、Issueが起票されること。

**WBS**
| Task ID | Category | タスク内容 | 対象ファイル | 依存先 | Issue案リンク |
| :---: | :---: | :--- | :--- | :---: | :--- |
| T3-1 | Setup | 作業ブランチ `feature/phase-3-swap` の作成と T2 のマージ | - | T2-5 | |
| T3-2 | Impl | CLI サブコマンド `approve` の追加 | `src/issue_creator_kit/cli.py` | T3-1 | |
| T3-3 | Impl | GitHub Actions ワークフローの差し替え | `.github/workflows/auto-approve-docs.yml` | T3-2 | |
| T3-4 | Review | Phase 3 成果物のレビューと Phase 4 計画の確定 | - | T3-3 | |

### Phase 4: 資産の同期とクリーンアップ (Sync & Cleanup)
- **Goal (狙い)**: 配布用テンプレート（Assets）を最新化し、プロジェクト全体の一貫性を回復する。
- **Input (前提)**: 稼働中の新ワークフロー
- **Deliverables (成果物)**:
    - **テンプレート更新 (`assets/workflows/`)**:
        - **目的**: 新規ユーザーが `init` した際に、最新の承認フローが展開されるようにするため。
- **Gate (承認条件)**: `init` コマンドで展開・上書きされたファイルが、Phase 3 で作成したものと同一であること。

**WBS**
| Task ID | Category | タスク内容 | 対象ファイル | 依存先 | Issue案リンク |
| :---: | :---: | :--- | :--- | :---: | :--- |
| T4-1 | Setup | 作業ブランチ `feature/phase-4-cleanup` の作成と T3 のマージ | - | T3-4 | |
| T4-2 | Verify | 統合検証（ローカルまたはテスト環境） | - | T4-1 | |
| T4-3 | Clean | `assets/workflows` 内のテンプレート同期 | `src/issue_creator_kit/assets/workflows/auto-approve-docs.yml` | T4-2 | |
| T4-4 | Review | 最終成果物のレビューとロードマップ完了承認 | - | T4-3 | |

## 3. リスク管理とロールバック
- **リスク**: メタデータ置換時の正規表現の誤りによるファイル破損。
- **対策/切り戻し**: 破壊的な置換の前にバックアップ（Git管理下なので `git checkout` で復旧可能）を前提とし、徹底したテストを行う。
- **リスク**: GitHub API のレート制限。
- **対策/切り戻し**: 指数バックオフの導入（将来検討）または最小限の API コールへの最適化。

## 4. 完了の定義
- [ ] 承認済みドキュメントのステータスが「承認済み」に自動更新される。
- [ ] 承認されたドキュメントに対応するトラッキング Issue が GitHub 上に作成される。
- [ ] ドキュメント内に作成された Issue 番号（例: `#123`）が追記される。
- [ ] 全てのテスト（Unit/Integration）がパスする。
- [ ] アセット内のテンプレートが刷新されている。
