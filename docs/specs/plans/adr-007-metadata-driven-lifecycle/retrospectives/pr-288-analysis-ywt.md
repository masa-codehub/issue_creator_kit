# 振り返りレポート (YWT) - PR #288 Review Analysis

## 1. Y (やったこと)

- **作業の実施内容:**
  - ADR-007 に基づく `creation_logic.md` および `promotion_logic.md` の詳細設計。
  - GitHub Reviewer (masa-codehub) による指摘事項の分析と SSOT (ADR-007) 監査。
- **事象の観測:**
  - レビュアーより、Step 3 (Issue起票) から Step 4 (Git書き戻し) への文脈（リンク置換後の本文）の受け渡しが不明確であるとの指摘。
  - 旧 ADR-003 への参照が残存しており、新旧仕様の混在が懸念された。
  - Promotion Logic における「Ready」状態と「Issue作成（ick create）」の関係性について、チームの認知負荷を下げるための表現修正が提案された。
- **分析情報の集約:**
  - `docs/specs/logic/creation_logic.md` (L51, L65)
  - `docs/specs/logic/promotion_logic.md` (L34)
  - `reqs/design/_approved/adr-007-metadata-driven-lifecycle.md` (SSOT)

## 2. W (わかったこと)

- **結果の確認:**
  - マルチステップの処理（API実行とGit書き戻し）を定義する際、中間状態（特に破壊的な変換を伴う本文）のメモリ上での管理方法を明示しないと、実装時にコンテキストの欠落や再計算による不整合が生じるリスクがある。
  - ADR の Supersede が発生した際、関連する Spec 内の参照を機械的に更新するプロセスが不足していた。

### ギャップ分析

- **理想 (To-Be):**
  - 仕様書が実装の曖昧さを完全に排除し、正しい SSOT (ADR-007) のみを参照している。
  - 各ステップの入出力データ（バッファ）が明確に定義されている。
- **現状 (As-Is):**
  - ステップ間でのデータ受け渡しが暗黙的。
  - Supersede された ADR-003 への参照が残っていた。
- **ギャップ:**
  - メモリバッファの定義不足による実装の自由度（＝不確実性）の混入。
  - 古い設計ドキュメントへの依存。
- **要因 (Root Cause):**
  - 設計時の「状態管理」に対する定義意識の欠如。
  - 旧 Spec テンプレートや過去の文脈を引きずったことによる、新 ADR への完全な切り替え漏れ。

## 3. T (次やること / 仮説立案)

- **実証的仮説:**
  - 指摘された箇所の修正（バッファへの記録明示、ADR-007 への参照変更、用語の明確化）により、実装の確実性が向上しチームの誤解が解消される。
- **飛躍的仮説:**
  - ロジック仕様書のテンプレートに「Memory Buffer Schema / Session State」という項目を標準化することで、この種のコンテキスト欠落を構造的に防ぐ。
- **逆説的仮説:**
  - 実装クラス（`IssueCreationUseCase` 等）のメソッドシグネチャや DTO が先に定義されていれば、仕様書レベルでのバッファ定義は不要だったのではないか（今回は設計先行のため、仕様書での定義がクリティカル）。

### 検証アクション

- [x] `creation_logic.md` にリンク置換後本文の保存を明記する。
- [x] `creation_logic.md` の Roadmap Sync 参照を ADR-007 に修正する。
- [x] `promotion_logic.md` の Rationale を「ready for issue creation (via ick create)」に修正する。
- [ ] `drafting-specs` スキルのチェックリストに「 superseded ADR 参照の有無」と「状態遷移バッファの定義」を追加検討する。
