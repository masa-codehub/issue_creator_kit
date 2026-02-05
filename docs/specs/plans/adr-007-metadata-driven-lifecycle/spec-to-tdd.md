# Handover: Spec to TDD (ADR-007 Metadata-Driven Lifecycle)

## 1. Overview
本ドキュメントは、ADR-007（メタデータ駆動型ライフサイクル管理）の仕様策定フェーズから実装フェーズへ引き継ぐための重要事項をまとめたものである。ADR-003（物理フォルダ管理）からの完全な移行を目指す。

## 2. 実装の優先順位 (Implementation Priority)
1.  **Document Model (007-T3-01)**: `Metadata` スキーマの正規化、日本語キー対応、およびバリデーションロジック。
2.  **Infrastructure (007-T3-03)**: `FileSystemAdapter.find_file_by_id` の追加と、`GitHubAdapter.sync_issue` (既存Issueの更新対応) の実装。
3.  **Creation Logic (007-T3-02)**: Git Diff からのファイル検知、`depends_on` による DAG 解析（トポロジカルソート）、原子的な起票と移動のシーケンス。
4.  **CLI (007-T3-04)**: `process-diff` の `--adr-id` バリデーションと、デフォルトパスの `_archive/` への更新。

## 3. 重要事項と実装上のヒント (Critical Tips)

### 3.1. メタデータアクセスの安全性
- `Document` クラスには `title` 属性は存在しない。必ず `doc.metadata.get("title")` または `doc.metadata.get("タイトル")` を使用すること。
- 日本語キーはパース時に英語キーへ正規化することを推奨する。

### 3.2. DAG 解析と Ready 判定
- 依存関係の解決には Python 標準の `graphlib.TopologicalSorter` の使用を検討すること。
- 依存タスクが今回のバッチ（Git Diff）に含まれていない場合は、`_archive/` ディレクトリを検索し、それでも見つからない場合は GitHub API で `issue_id` の有無を確認する。

### 3.3. 原子性の保証 (Fail-fast)
- 起票ループ（Step 3）でエラーが発生した場合、それまで起票に成功したタスクも含め、**一切のファイル移動やメタデータ更新（Step 4）を行わないこと。**
- これにより、不整合な状態（Issueはあるがファイルが元の場所で採番されていない状態）を最小限に抑える。

### 3.4. テスト方針
- **FileSystemAdapter**: `_archive/` 配下の大量のファイルから ID で検索する `find_file_by_id` の性能と正確性を検証すること。
- **UseCase**: 循環参照を含む DAG や、一部の依存タスクが未起票の場合の `Ready` 判定ロジックを網羅すること。

## 4. 関連ドキュメント (SSOT)
- `docs/specs/data/document_model.md`
- `docs/specs/logic/creation_logic.md`
- `docs/specs/components/infra_adapters.md`
- `docs/specs/api/cli_commands.md`

## 5. 完了条件 (Definition of Done)
- [ ] すべてのメタデータ駆動ロジックが TDD でカバーされていること。
- [ ] `ick create` (または `process-diff`) が `_archive/` を正しく扱えること。
- [ ] 既存の ADR-003 用の実装（もしあれば）が、ADR-007 仕様で完全に置き換えられていること。
