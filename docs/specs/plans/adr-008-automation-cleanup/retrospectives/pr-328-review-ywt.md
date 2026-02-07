# 振り返りレポート (YWT): PR #328 Review Feedback

## 1. Y (やったこと)

- **作業の実施内容:**
  - ADR-008 の `GraphBuilder` および `Visualizer` の仕様ドラフト作成。
  - Copilot および gemini-code-assist[bot] による 10 件のレビューコメントの受信。
  - `analyzing-github-reviews` スキルを用いたコメントの分析と分類。
- **事象の観測:**
  - `ORPHAN_DEPENDENCY` の判定におけるアーカイブディレクトリ（`_archive/`）の扱いが曖昧であるとの指摘。
  - Mermaid の出力（ソート順、エスケープ、空の状態）が未定義で、TDD の期待値が不安定になる可能性の指摘。
  - アーキテクチャ図（ADR-008）と仕様書の間で用語（Task vs Document）やインターフェース（`build_graph` の引数）に不整合。
- **分析情報の集約:**
  - `docs/specs/logic/graph_and_validators.md` (仕様)
  - `docs/architecture/arch-structure-008-scanner.md` (SSOT)
  - `src/issue_creator_kit/domain/document.py` (実装上の用語確認)

## 2. W (わかったこと)

- **結果の確認:**
  - 可視化ツールの仕様（Visualizer）においては、単に「生成する」だけでなく、テストの安定性を確保するために「決定論的な出力順序」や「境界値のエスケープルール」を厳密に定義する必要がある。
  - ADR（抽象設計）から Spec（詳細設計）に落とし込む際、用語の一般化（Task -> Document）が不十分で、混乱を招いた。

### ギャップ分析

- **理想 (To-Be):**
  - 仕様書を読めば実装者が迷うことなく、一意に TDD ケースを記述できる状態。
- **現状 (As-Is):**
  - タイトル抽出の優先順位やソート順などが実装者に委ねられており、テストが不安定になる余地があった。
- **ギャップ:**
  - 文字列生成ロジックにおける決定論的規約の欠如。
- **要因 (Root Cause):**
  - 「詳細仕様」の定義において、データ構造（Property）だけでなく、生成アルゴリズムの「順序」や「エスケープ」といった副作用のない変換ロジックの厳密性が不足していた。

## 3. T (次やること / 仮説立案)

- **実証的仮説:**
  - Mermaid 生成ロジックに「ID昇順」などのソート規約を追加し、エスケープルールを明文化することで、TDD の安定性が向上する。
- **飛躍的仮説:**
  - `Document` モデルに `title` プロパティを（メタデータからの抽出ロジックを含めて）定義し、各コンポーネントが直接参照できるようにすれば、抽出ロジックの重複と仕様の曖昧さを排除できる。
- **逆説的仮説:**
  - `GraphBuilder` に `archived_ids` を渡すのではなく、`FileSystemScanner` が「有効な依存先ID集合」をあらかじめ集計して渡すべきではないか。

### 検証アクション

- [ ] `docs/specs/logic/graph_and_validators.md` に決定論的ルール（ソート、エスケープ、タイトル解決）を追記する。
- [ ] `GraphBuilder` のインターフェースに `archived_ids` (または有効IDセット) を追加する。
- [ ] ADR-008 の構成図と用語を `Document` に統一する。
