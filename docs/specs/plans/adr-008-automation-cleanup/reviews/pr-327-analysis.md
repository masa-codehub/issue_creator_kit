# Review Analysis Report: PR #327

## 1. Summary
- **Total Comments:** 7
- **Accept (修正受諾):** 7
- **Discuss (議論/確認):** 0
- **Explain (現状維持/説明):** 0

## 2. Analysis Details

### [Accept] docs/specs/logic/scanner-logic.md (L32, L32)
- **Reviewer's Comment:**
  - `root_path` からの相対パスとして定義するのが明確
  - `root_path` 配下という説明と矛盾する表記を修正
- **Context Analysis:**
  - アルゴリズム内で `reqs/design/_approved/` のように `root_path` (通常 `reqs/`) を含むパスが例示されており、二重結合のリスクがある。
- **Proposed Action:**
  - パス表記を `design/_approved/`, `tasks/*/` 等の相対パスに統一する。
- **Verification Plan:**
  - 修正後の仕様が `root_path` 起点の相対パスで一貫しているか目視確認。

### [Accept] docs/specs/logic/scanner-logic.md (L12, L33)
- **Reviewer's Comment:**
  - `exclude_patterns` がどのように使用されるか記載されていない
- **Context Analysis:**
  - Input には定義されているが、Algorithm/Flow 内で適用ステップが抜けている。
- **Proposed Action:**
  - 走査ステップ（未処理ファイルの抽出）において、glob/Path.match による除外フィルタリングを明記する。
- **Verification Plan:**
  - TDD 基準に `exclude_patterns` による除外のケース（Boundary Path）を追加する。

### [Accept] docs/specs/logic/scanner-logic.md (L52)
- **Reviewer's Comment:**
  - アーカイブと承認済み両方に存在する場合の Fail-fast ガードレール
- **Context Analysis:**
  - YWT で「アーカイブ済みIDとの衝突リスク」を検知しているにもかかわらず、仕様では「アーカイブ優先で無視」となっていた。これは安全性を重視する ADR-008 の方針と矛盾する。
- **Proposed Action:**
  - 判定ロジックを「アーカイブ含め全スキャン対象で一意」であることを求める Fail-fast 方式に修正。重複時は `DUPLICATE_ID` を送出する。
- **Verification Plan:**
  - TDD 基準の ID重複ケースに、アーカイブとの衝突シナリオを追加。

### [Accept] docs/specs/logic/scanner-logic.md (L37)
- **Reviewer's Comment:**
  - `DUPLICATE_ID` が共通定義（definitions.md）に存在しない
- **Context Analysis:**
  - ADR-008 の共通定義において、例外コードとして定義が漏れていた。
- **Proposed Action:**
  - `docs/specs/plans/adr-008-automation-cleanup/definitions.md` に `DUPLICATE_ID` を追記。
- **Verification Plan:**
  - `definitions.md` の更新を確認。

### [Accept] docs/specs/logic/scanner-logic.md (L79)
- **Reviewer's Comment:**
  - TDD の入力ファイル例を実ディレクトリ名に合わせる
- **Context Analysis:**
  - `approved/...` となっており、実際の `design/_approved/` 等と乖離していた。
- **Proposed Action:**
  - TDD Criteria のパスを `design/_approved/`, `tasks/_archive/` 等に更新。
- **Verification Plan:**
  - 修正後の TDD 表が物理構造と一致しているか確認。

### [Accept] docs/specs/logic/scanner-logic.md (L1)
- **Reviewer's Comment:**
  - ファイル名の命名規則（ハイフン vs アンダーバー）
- **Context Analysis:**
  - `docs/specs/logic/` 配下はスネークケースが主流。`definitions.md` にはハイフン指定があるが、既存ファイルとの一貫性を優先すべき。
- **Proposed Action:**
  - `scanner-logic.md` を `scanner_logic.md` にリネーム。
- **Verification Plan:**
  - `ls docs/specs/logic/` でリネームを確認。

## 3. Execution Plan
- [ ] `scanner-logic.md` を `scanner_logic.md` にリネーム。
- [ ] `scanner_logic.md` のパス表記、除外ロジック、重複判定（Fail-fast）、TDD基準を修正。
- [ ] `definitions.md` に `DUPLICATE_ID` を追加。
- [ ] 変更内容をコミットしプッシュ。
