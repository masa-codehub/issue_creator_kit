# 振り返りレポート (YWT) - Spec Drafting for Graph Builder & Visualizer

## 1. Y (やったこと)

- **作業の実施内容:**
  - `scouting-facts` を使用して `arch-structure-008-scanner.md` および `graph_and_validators.md` の現状を調査。
  - `analyzing-intent` にて、既存仕様の更新が最適であると判断。
  - `docs/specs/logic/graph_and_validators.md` を更新し、`GraphBuilder` サービスと `Visualizer` の Mermaid 出力ロジック、検証基準を追加した。
  - `drafting-audit-template.md` に基づき自己監査を実施し、PASS を確認。
- **事象の観測:**
  - `src/issue_creator_kit/domain/services/scanner.py` が Issue 本文では「Task-03 成果物」とされていたが、リポジトリ内（`feature/spec-update-adr008` ブランチ）にはまだ存在していなかった。
- **分析情報の集約:**
  - `docs/architecture/arch-structure-008-scanner.md` (Scanner SSOT)
  - `src/issue_creator_kit/domain/document.py` (Current Model)
  - `docs/specs/logic/graph_and_validators.md` (Original Spec)

## 2. W (わかったこと)

- **結果の確認:**
  - 既存の `graph_and_validators.md` には `TaskGraph` のコアロジックはあったが、それを呼び出すサービス層の定義や、ユーザーが求める「Mermaid出力」の詳細が不足していた。
  - 物理ファイルシステムを SSOT とする ADR-008 の方針に合わせ、`Document` モデルをベースとした仕様に更新する必要があった。

### ギャップ分析

- **理想 (To-Be):** ADR-008 のアーキテクチャ定義に基づき、`GraphBuilder` と `Visualizer` が独立したコンポーネントとして定義され、TDD が可能な詳細仕様（入出力、例外、Mermaidフォーマット）が存在する。
- **現状 (As-Is):** `GraphBuilder` の具体的なサービス定義が未整備で、`Visualizer` に関しては全く記述がなかった。
- **ギャップ:** `Visualizer` の Mermaid 生成ルールおよび、サービス層のインターフェース定義が欠落していた。
- **要因 (Root Cause):** 旧来の仕様（ADR-003ベース等）からの移行過程であり、最新の ADR-008 方針を詳細仕様レベルまで落とし込めていなかったため。

## 3. T (次やること / 仮説立案)

- **実証的仮説:** 今回策定した仕様に基づき、`builder.py` と `visualizer.py` の実装タスク（TDD）を開始すれば、ADR-008 の目的を達成できる。
- **飛躍的仮説:** Mermaid 生成において、単なるノードとエッジだけでなく、タスクの `Status`（Ready/Issued/Completed）をサブグラフやスタイルで表現するルールを自動生成できれば、進捗管理ツールとしての価値がさらに高まる。
- **逆説的仮説:** もし `FileSystemScanner` の実装が大幅に遅れる場合、`TaskGraph` のみを独立して検証するためのモックデータ生成ツールを先に用意すべきかもしれない。

### 検証アクション

- [x] 作成した `docs/specs/logic/graph_and_validators.md` が `arch-structure-008-scanner.md` と矛盾していないことを最終確認する。
- [ ] PR を作成し、メンテナーのレビューを受ける。
