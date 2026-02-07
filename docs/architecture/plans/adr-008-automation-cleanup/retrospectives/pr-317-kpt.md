# 振り返りレポート (KPT) - PR #317 (Architecture Refinement)

## 評価の切り口 (4 Axes)

1. **安全性 (Safety):** 不変条件（Invariants）の集約によるバリデーション漏れ防止。
2. **効率性 (Efficiency):** ドキュメント参照の整理による認知負荷の低減。
3. **コンテキスト (Context):** ADR-008 (Scanner Foundation) と既存図面の整合。
4. **合意形成 (Alignment):** レビュアー指摘による高次図面の解像度向上。

## 1. K (Keep): 継続すべき成功パターン

- **[Safety]:**
  - 不変条件（Invariants）を `arch-structure-007-metadata.md` に一括集約したことで、実装（Pydantic Validator / GraphBuilder）が参照すべき SSOT が明確になった。
- **[Context]:**
  - `issue-kit` の構造図を ADR-008 で定義された最新コンポーネント（Scanner Foundation）に同期させ、システム全体の「地図」を更新した。

## 2. P (Problem): 構造的な阻害要因

- **[Context]:**
  - 高次の構造図（Map）で `ScannerService` という抽象名を使用し、詳細定義で `FileSystemScanner` を使用したため、レビュアーに「図と定義の不一致」として指摘された。
- **[Efficiency]:**
  - モジュールレベルの依存関係記述において、下位コンポーネントごとの詳細な依存先を省略したため、図面の意図がテキストで十分に補完されなかった。
- **[Context]:**
  - 重複排除のために説明文を削りすぎた結果、Mermaid 図単体で「何が違反パターンなのか」を直感的に理解しにくくなった。

## 3. T (Try): 具体的な改善策と資産化

- **立案された仮説:**
  - **実証的:**
    - 高次図面（Interface/Module Layer）であっても、ADRで定義された最新のコンポーネント名を使用し、用語の揺れを排除する。
  - **飛躍的:**
    - コンポーネント定義テンプレートに「依存関係の明示（図面との完全同期）」チェックリストを追加する。
  - **逆説的:**
    - 図面の横に常に「読み解きガイド（Bullet points）」を最小限残すルールを明文化し、ドキュメントの「自己完結性」を維持する。

### 資産化アクション

- **選択された改善策:**
  - アーキテクチャ図面の「自己完結性」ガイドラインの策定（図とテキストの相互補完ルールの徹底）。
- **具体的な手順/Issue案:**
  - [ ] `docs/architecture/template/` 内のテンプレートを更新し、図面の下に「キーポイントの箇条書き」を必須とする注釈を追加する。
  - [ ] `Scanner Foundation` に関連する全図面で、`ScannerService` (Legacy/Summary) を `FileSystemScanner` (Current) に置換・統一する。
