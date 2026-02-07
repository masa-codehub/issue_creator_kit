# 振り返りレポート (YWT) - PR #282 Infrastructure Adapter Specifications

## 1. Y (やったこと)

- **作業の実施内容:**
  - `docs/specs/components/infra_adapters.md` の更新。
  - `GitHubAdapter` への `sync_issue` メソッドの追加と、`Document` からのタイトル・本文・ラベルのマッピングルールの定義。
  - `FileSystemAdapter` への `find_file_by_id` メソッドの追加と検索ロジックの定義。
  - 「起票 -> メタデータ更新 -> 物理移動」の原子的な連携シーケンスの定義。
  - 失敗時の後続処理抑止などを保証する TDD 基準の追加。
- **事象の観測:**
  - `replace` ツール使用時に、以前の編集でセクション番号が微妙にズレていたため、置換に失敗するケースがあったが、`read_file` で再確認することで修正できた。
- **分析情報の集約:**
  - `docs/specs/components/infra_adapters.md` (As-is)
  - `reqs/design/_approved/adr-007-metadata-driven-lifecycle.md` (SSOT)
  - `src/issue_creator_kit/infrastructure/` 配下のリファレンス実装。

## 2. W (わかったこと)

- **結果の確認:**
  - インフラ層の仕様を具体化することで、UseCase 層が ADR-007 の複雑な状態遷移を管理する負担を軽減できることがわかった。特に `sync_issue` が `Document` オブジェクトを直接受け取ることで、マッピングの責任が明確になった。

### ギャップ分析

- **理想 (To-Be):**
  - インフラ層だけで「どのファイルがどの Issue に対応するか」を完結して判断できること。
- **現状 (As-Is):**
  - ファイル移動と Issue ID 追記が UseCase 層のロジックに散らばっており、不整合が起きやすい構造だった。
- **ギャップ:**
  - `find_file_by_id` のような、アーカイブ内から特定のタスクを探し出すための「逆引き」手段が欠如していた。
- **要因 (Root Cause):**
  - ADR-003 までは物理ディレクトリが状態（draft/archive）を表していたため、検索の必要性が低かったが、ADR-007 のフラット構造への移行により、メタデータベースの検索が不可欠になった。

## 3. T (次やること / 仮説立案)

- **実証的仮説:**
  - 今回定義した `sync_issue` と `find_file_by_id` を実装し、UseCase 層のリファクタリングを行うことで、ADR-007 のライフサイクル管理が安定する。
- **飛躍的仮説:**
  - `InfrastructureTransaction` のような、外部 API とファイルシステムの整合性を保証するラッパーを導入することで、UseCase 層はドメインロジックにさらに集中できるようになる。
- **逆説的仮説:**
  - GitHub Issue 自体にすべてのメタデータを同期し、ローカルファイルは「キャッシュ」として扱うアプローチをとれば、ファイルシステムの原子性問題自体を回避できるのではないか。

### 検証アクション

- [ ] `007-T3-03-infra` 実装フェーズにおいて、今回定義した `TDD Criteria` がすべてパスすることを確認する。
- [ ] `safe_move_file` が異なるファイルシステム間（パーティション越え）でも原子性を保てるか調査する（`shutil.move` の挙動の再確認）。
