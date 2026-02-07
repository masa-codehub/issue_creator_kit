# 概要 / Summary

[ADR-008] Cleanup & Scanner Foundation: 自動化パイプラインの単純化と基盤再構築

- **Status**: 承認済み
- **Date**: 2026-02-06

## 状況 / Context

ADR-007 においてメタデータ駆動型ライフサイクルが定義されたが、実装上は ADR-003 時代の物理ディレクトリ依存や GitHub Actions の複雑な同期ロジックが負債として残存している。これらは現在、不整合や混乱を避けるために意図的に停止（コメントアウト）されている状態にある。

現状の課題：

1. **負債の混在**: 自動移動スクリプト (`auto-approve-docs.yml`) と手動運用が混在し、SSOT（Single Source of Truth）の遷移プロセスが不明確。
2. **脆弱な検知**: `git diff-tree` (SHA) ベースの検知は、CI 失敗時のリトライや手動実行時に未処理ファイルを容易に取りこぼす。
3. **過剰な同期**: Markdown ファイル（計画書）への Issue 番号書き戻しは、Git 履歴を汚し、コンフリクトを誘発する二重管理となっている。

## 決定 / Decision

「引き算のリファクタリング」を徹底し、物理状態（ファイル配置）を正とする堅牢なスキャナー基盤を構築する。

### 1. 負債の完全削除

- **自動承認の廃止**: `_inbox` から `_approved` への移動は「手動PR/マージ」を正本とし、関連する Actions や UseCase (`WorkflowUseCase`, `ApprovalUseCase`) を完全に削除する。
- **書き戻しの廃止**: 計画ドキュメント（Markdown）への Issue 番号追記ロジックをすべて削除し、二重管理を解消する。

### 2. 物理状態ベースのスキャナー基盤

- **脱 diff-tree**: Git 差分に依存せず、`reqs/` ディレクトリ内のファイルを物理的に走査し、`_archive/` に存在しないものを「未処理」として特定するロジックへ移行する。
- **検証モード (`--dry-run`)**: 実際の副作用を起こす前に、起票予定リストを表示する機能を実装する。
- **可視化 (`visualize`)**: 依存関係（DAG）を Mermaid 形式で出力し、マージ前の安全性を人間が確認可能にする。

### 3. ドメイン層によるガードレール (Domain Guardrails)

- **制約の集約**: `id` 形式、`depends_on` の整合性（自己参照、循環参照禁止）を検証するバリデーションを Domain 層（Pydantic モデル）に集約し、ツール全体で一貫した不変条件を保証する。

## 検討した代替案 / Alternatives Considered

- **案A: 現状の `process-diff` の修正**: 履歴管理が複雑になり、リトライ耐性が向上しないため却下。
- **案B: GitHub 検索のみによる未処理検知**: API レートリミットや検索遅延のリスク、および「Git 上に予約票がある」という File-based SSOT の思想と乖離するため却下。

## 結果 / Consequences

### メリット (Positive consequences)

- **Feasibility**: 実装がシンプルになり、開発サイクルが大幅に高速化される。
- **Safety**: 物理的なファイル状態を正とすることで、検知漏れや二重起票のリスクが低減する。
- **Usability**: `visualize` により、複雑な依存関係をマージ前に視覚的に確認できる。

### デメリット (Negative consequences)

- **Usability**: 計画ドキュメント上から Issue 番号が消えるため、進捗確認は GitHub 上で行う必要がある。
- **Manual Effort**: ADR の承認移動が手動となるが、これは確実性を優先した意図的なトレードオフである。

## 検証基準 / Verification Criteria

- [ ] `issue-kit` から不要なコード（自動承認・書き戻し）が一掃されていること。
- [ ] `process-diff --dry-run` が `reqs/tasks/` 内の未処理ファイルを正確にリストアップできること。
- [ ] 循環参照を含むメタデータが Pydantic バリデーションで正しくエラーとなること。

## 実装状況 / Implementation Status

未着手
