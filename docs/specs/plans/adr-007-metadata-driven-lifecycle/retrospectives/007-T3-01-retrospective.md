# 振り返りレポート (YWT): Update Document Model Specification

## 1. Y (やったこと)

- **作業の実施内容:**
  - `docs/specs/data/document_model.md` を更新し、ADR-007 および `definitions.md` と整合させた。
  - Mermaid クラス図の更新、必須フィールド (`id`, `parent`, `type`, `phase`, `depends_on`) の追加、ステータス Enum の刷新（ADR用/Task用）、バリデーションルールの再定義を行った。
  - `scouting-facts`, `analyzing-intent`, `setting-smart-goals` スキルを使用して、現状調査から目標設定までを自律的に実施した。
- **事象の観測:**
  - 既存の `document_model.md` には、ADR-003 時代の「物理フォルダ移動（archive/）」を前提とした論理ステータスやバリデーションルールが色濃く残っていた。
  - `replace` ツール使用時、日本語文字列の微細な違い（`file` か `ファイル` か）により置換に失敗した。
- **分析情報の集約:**
  - 参照 SSOT: `reqs/design/_approved/adr-007-metadata-driven-lifecycle.md`
  - 参照 Common Definitions: `docs/specs/plans/adr-007-metadata-driven-lifecycle/definitions.md`

## 2. W (わかったこと)

- **結果の確認:**
  - ADR-007 のメタデータ駆動への移行は、単なるフィールド追加ではなく「物理パスへの依存を完全に排除する」というドメインモデルの思想的転換を意味することがわかった。
  - 日本語を含む仕様書の更新では、`read_file` の結果を極めて正確に (`copy-paste` レベルで) `replace` の `old_string` に反映させる必要がある。

### ギャップ分析

- **理想 (To-Be):**
  - メタデータのみでライフサイクルが完結し、物理フォルダは「保存場所」としての役割に特化している。
- **現状 (As-Is):**
  - 既存のコードや一部の古いドキュメントにはまだ「フォルダ移動による状態表現」の前提が残っている可能性がある。
- **ギャップ:**
  - ドメインモデル（エンティティ）の仕様は最新化されたが、それを扱うユースケース（`creation.py`, `workflow.py` 等）の実装はまだ旧仕様のままである。
- **要因 (Root Cause):**
  - ADR-007 への移行が大規模であり、段階的な更新を行っているため。

## 3. T (次やること / 仮説立案)

- **実証的仮説:**
  - 次のタスクである `007-T3-02-spec-logic` (Logic Spec) において、今回定義した `Metadata` フィールドを使用した DAG 解析と状態遷移のロジックを策定する。
- **飛躍的仮説:**
  - `definitions.md` のテーブル定義から Markdown の仕様書を自動生成する仕組みがあれば、SSOT との不整合をゼロにできる。
- **逆説的仮説:**
  - バリデーションルールの一部（`depends_on` の整合性など）は、ドメインモデルではなく、複数のドキュメントを俯瞰できるリポジトリ層やユースケース層で管理すべきではないか。

### 検証アクション

- [ ] `ick` コマンドの単体テスト (`test_document.py`) を今回定義した必須フィールドおよび新ステータスに対応させる。
- [ ] `docs/specs/data/document_model.md` の内容が `007-T3-02` (Logic Spec) の策定に十分な情報を提供しているか、後続タスクの偵察フェーズで確認する。
