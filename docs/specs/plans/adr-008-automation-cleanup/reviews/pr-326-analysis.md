# Review Analysis Report: PR #326

## 1. Summary

- **Total Comments:** 7
- **Accept (修正受諾):** 7
- **Discuss (議論/確認):** 0
- **Explain (現状維持/説明):** 0

## 2. Analysis Details

### [Accept] docs/specs/data/domain_models_adr008.md (L28)

- **Reviewer's Comment:**
  - "`ADR Model`に`depends_on`フィールドが定義されていません。"
- **Context Analysis:**
  - `arch-structure-008-scanner.md` のクラス図では `ADR` クラスに `depends_on` が定義されており、仕様間の不整合が発生している。
- **Proposed Action:**
  - `ADR Model` に `depends_on` フィールドを追加する。型は `List[TaskID | ADRID]` とする。
- **Verification Plan:**
  - Pydantic モデルの実装時に `depends_on` を含む正常系テストを追加する。

### [Accept] docs/specs/data/domain_models_adr008.md (L25)

- **Reviewer's Comment:**
  - "`ADRID`の制約（Constraints）が、`Data Types`セクションで定義されたRegexと一致していません。"
- **Context Analysis:**
  - セクション間で Regex が異なり（`.*` vs `[a-z0-9-]+`）、Error Path の期待結果とも矛盾している。
- **Proposed Action:**
  - `^adr-\d{3}-[a-z0-9-]+$` に統一する。
- **Verification Plan:**
  - `Error Path` の `adr-008_test` が `ValidationError` になることを確認する。

### [Accept] docs/specs/data/domain_models_adr008.md (L60)

- **Reviewer's Comment:**
  - "このビジネスロジックのガードレールは、`issue_id`が必須となる条件を部分的にしかカバーしていません。"
- **Context Analysis:**
  - `Task Model` 定義では `status` が `Issued` 以上（`Completed` 含む）で `issue_id` 必須としているが、ガードレールには `Issued` のみ記載されていた。
- **Proposed Action:**
  - `status` が `Issued` または `Completed` の場合に `issue_id` が必須であることを明記する。
- **Verification Plan:**
  - `status='Completed'` かつ `issue_id=None` で `ValidationError` が出るテストを追加。

### [Accept] docs/specs/data/domain_models_adr008.md (L61)

- **Reviewer's Comment:**
  - "このガードレール「`parent` に自分自身の ID を指定した場合（自己参照）...」は、現在のモデル定義では論理的に発生し得ません。"
- **Context Analysis:**
  - `id` (TaskID) と `parent` (ADRID) は形式が異なるため一致することはない。
- **Proposed Action:**
  - 当該ガードレールを削除する。
- **Verification Plan:**
  - なし（仕様の整理）。

### [Accept] docs/specs/logic/graph_and_validators.md (L25, L16, L53, L65)

- **Reviewer's Comment:**
  - API名の不整合 (`add_node` vs `add_task`), 例外型の曖昧さ, 実行順序の非決定性, データ構造の不整合 (`Set` vs `List`).
- **Context Analysis:**
  - アーキテクチャ図との不整合および TDD の期待値としての曖昧さが指摘されている。
- **Proposed Action:**
  - `TaskGraph`: API名を `add_task(task)` に変更。
  - `TaskNode`: `dependencies`/`dependents` を `List[TaskNode]` に変更（Arch図に合わせる）。
  - `Self-Reference`: 期待される例外を `GraphError: SELF_REFERENCE` に固定。
  - `Execution Order`: 「ID の昇順」で決定論的に順序を返すことを明記。
- **Verification Plan:**
  - グラフ構築・ソートのテストで、期待される順序と例外メッセージを厳密に検証する。

### [Accept] docs/specs/plans/adr-008-automation-cleanup/reviews/pr-319-spec-audit-report.md (L27)

- **Reviewer's Comment:**
  - "見出しの節番号が ## 2 の次に ## 4 となっており... ## 3 が欠落"
- **Context Analysis:**
  - 単純なタイポ。
- **Proposed Action:**
  - 節番号を `## 3` に修正。
- **Verification Plan:**
  - プレビューで確認。

---

## 3. Execution Plan

- [ ] `docs/specs/data/domain_models_adr008.md` の修正。
- [ ] `docs/specs/logic/graph_and_validators.md` の修正。
- [ ] `docs/specs/plans/adr-008-automation-cleanup/reviews/pr-319-spec-audit-report.md` の修正。
- [ ] `recording-changes` による記録と push。
