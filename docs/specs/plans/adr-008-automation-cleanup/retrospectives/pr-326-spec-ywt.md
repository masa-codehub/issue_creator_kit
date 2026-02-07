# 振り返りレポート (YWT): PR #326 仕様策定レビュー分析

## 1. Y (やったこと)

- **作業の実施内容:**
  - ADR-008「Scanner Foundation」の仕様ドラフト（PR #326）に対するレビューコメント 7 件の分析を実施。
  - `analyzing-github-reviews` スキルをアクティベートし、コメントを「Accept」として分類。
  - `auditing-ssot` を実行し、指摘内容と既存のアーキテクチャ図（`arch-structure-008-scanner.md`）および共通定義（`definitions.md`）との整合性を確認。
- **事象の観測:**
  - 指摘の多くが「設計書（Arch）と仕様書（Spec）の間の不整合」や「仕様書内での定義の矛盾（Regex等）」に関するものであった。
  - 特に `ADR Model` への `depends_on` 欠落は、後続のグラフ構築ロジックの前提を崩す重要な指摘であった。
- **分析情報の集約:**
  - 参照 SSOT: `docs/architecture/arch-structure-008-scanner.md`, `docs/specs/plans/adr-008-automation-cleanup/definitions.md`

## 2. W (わかったこと)

- **結果の確認:**
  - ドラフト作成時に「上位設計（Arch）との逐次的な同期確認」が不足していたことが原因で、クラス定義やメソッド名の乖離が発生した。
  - Pydantic モデルのガードレール定義において、エッジケース（status=Completed 時の issue_id）や論理的な冗長性（異なる ID 型同士の自己参照チェック）への考慮が甘かった。

### ギャップ分析

- **理想 (To-Be):**
  - 詳細仕様（Spec）がアーキテクチャ設計（Arch）および共通定義（Definitions）と完全に一致し、TDD の期待値が曖昧さなく定義されている状態。
- **現状 (As-Is):**
  - メソッド名やフィールド、ID 形式の Regex 等に複数の不整合や定義漏れが存在した。
- **ギャップ:**
  - フィールド欠落（ADR.depends_on）、Regex不一致（ADRID）、メソッド名不一致（add_node vs add_task）など、複数の具体的乖離。
- **要因 (Root Cause):**
  - 仕様執筆時のチェックリストに「上位ドキュメントとの一貫性チェック」が明示されておらず、単独ファイル内での整合性に終始してしまった。

## 3. T (次やること / 仮説立案)

- **実証的仮説:**
  - 指摘された 7 項目を仕様書に反映し、SSOT との完全な同期を図れば、実装時の迷いや手戻りを排除できる。
- **飛躍的仮説:**
  - Pydantic の正規表現や共通の列挙値（Status等）を `definitions.md` で管理し、Spec/Implementation 双方から参照（または自動生成）する仕組みがあれば、定義のブレを物理的に防げる。
- **逆説的仮説:**
  - Arch 図と Spec の不整合を許容し、Spec を「実装時の最新真実」として優先させる運用も考えられるが、現状のプロジェクト規模では SSOT の分散を招くため、Arch 側へのフィードバックもセットで必要。

### 検証アクション

- [ ] `docs/specs/data/domain_models_adr008.md` および `docs/specs/logic/graph_and_validators.md` を修正し、レビュー指摘をすべて反映する。
- [ ] 修正後の Spec が Arch 図と一致していることを `auditing-ssot` で再検証する。
- [ ] `docs/specs/plans/adr-008-automation-cleanup/reviews/pr-319-spec-audit-report.md` の番号ミスを修正する。
