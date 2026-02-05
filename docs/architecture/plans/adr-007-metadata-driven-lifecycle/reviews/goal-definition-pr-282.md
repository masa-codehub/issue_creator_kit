# Goal Definition - Update Infrastructure Adapter Specifications

## 1. 達成目標 (Goal / Outcome)
`docs/specs/components/infra_adapters.md` を更新し、ADR-007 に準拠した FileSystem (Atomic Move/Search) および GitHub (Issue Sync) のインターフェース仕様を確定させる。

## 2. 実行アクション (Action Items)
- [ ] **FileSystemAdapter 仕様の拡張**:
  - `find_file_by_id(task_id: str, search_dirs: list[str]) -> Path` の追加。
  - `safe_move_file` の「原子性」に関する定義の厳密化（メタデータ更新との順序関係の明記）。
- [ ] **GitHubAdapter 仕様の拡張**:
  - `sync_issue(document: Document) -> int` の追加。
  - `Document` オブジェクトから Issue Title/Body へのマッピングルールの定義。
  - レートリミットハンドリングと独自例外クラスの再定義。
- [ ] **原子操作シーケンスの記述**:
  - 起票 -> メタデータ更新 -> アーカイブ移動 の一連のフローを Markdown テーブルまたは擬似コードで記述。
- [ ] **TDD 検証基準の追加**:
  - APIエラー時にファイル移動が実行されないことを保証するためのテストケース要件を記述。

## 3. 検証方法 (DoD / Verification)
- [ ] **Document Syntax**: `docs/specs/components/infra_adapters.md` が適切な Markdown 形式で保存されていること。
- [ ] **Content Check**: 
  - `grep "find_file_by_id" docs/specs/components/infra_adapters.md` がヒットすること。
  - `grep "sync_issue" docs/specs/components/infra_adapters.md` がヒットすること。
  - `grep "TDD Criteria" docs/specs/components/infra_adapters.md` 配下に失敗時の振る舞いが記載されていること。
- [ ] **Consistency Check**: 追加された仕様が ADR-007 のディレクトリ構造（`_archive/`）と矛盾していないこと。

## 4. 制約事項 (Constraints)
- 既存のメソッド（`create_issue` など）との互換性を維持する（推奨）。
- 推測を排除し、実装者が迷わず `pytest` でモックを書けるレベルの厳密さを保つ。
