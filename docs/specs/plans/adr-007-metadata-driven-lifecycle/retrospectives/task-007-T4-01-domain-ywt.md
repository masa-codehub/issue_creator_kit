# 振り返りレポート (YWT) - Data Model & Adapter Protocols

## 1. Y (やったこと)
- **作業の実施内容:**
  - `src/issue_creator_kit/domain/exceptions.py` の作成。
  - `src/issue_creator_kit/domain/interfaces.py` の作成 (Protocol 定義)。
  - `src/issue_creator_kit/domain/document.py` のリファクタリング (Pydantic `Metadata` モデル導入)。
  - `tests/unit/domain/test_document.py` の新規作成と TDD サイクルの実施。
  - `ruff` および `mypy` による静的解析と修正。
- **事象の観測:**
  - Pydantic を導入することで、バリデーションロジック（`id` フォーマットや必須フィールド）を宣言的に記述でき、テストの網羅性が向上した。
  - 日本語キーのエイリアスマッピングを `model_validator(mode="before")` で行うことで、パース部分を汚さずに正規化を実現できた。
  - Python 3.13 環境において、`typing.Union` や `typing.Optional` を `X | Y` 形式に自動変換（`ruff --fix`）することで、コードが大幅にクリーンになった。

## 2. W (わかったこと)
- **結果の確認:**
  - ドメイン層で厳密な Protocol を定義することで、Adapter の具象実装（T4-02 ～ T4-04）において「何を実装すべきか」が明確になった。
  - `Metadata` クラスに `__getitem__` を実装したことで、既存の `doc.metadata["id"]` 形式のアクセスを壊さずに移行が可能。

### ギャップ分析
- **理想 (To-Be):** 全てのメタデータが ADR-007 のライフサイクルルールに基づき、パース時点で完全にバリデーションされていること。
- **現状 (As-Is):** 主要なバリデーションは実装済み。
- **ギャップ:** Markdown List 形式（YAML Frontmatter 以外）でのパース時のエラーハンドリングが、YAML に比べてやや寛容。
- **要因 (Root Cause):** 既存の正規表現ベースのパースロジックを流用しているため、YAML ほど厳密な構文チェックが困難。

## 3. T (次やること / 仮説立案)
- **実証的仮説:**
  - 次のタスク (T4-02: Infrastructure Implementation) では、今回定義した `IGitHubAdapter` 等の Protocol に `runtime_checkable` を付けているため、`isinstance` による検証が可能になる。
- **飛躍的仮説:**
  - `Document.to_string` を、Pydantic の `model_dump_json()` や YAML 出力に完全に寄せることで、シリアライズロジックの重複を排除できる。
- **逆説的仮説:**
  - 今回 `Metadata` クラスを `domain/document.py` に入れたが、依存関係の整理（特に循環参照の回避）のために `domain/models/metadata.py` のように別ファイルに分けた方が、将来的な拡張性は高いのではないか。

### 検証アクション
- [ ] T4-02 において、`FileSystemAdapter` が `IFileSystemAdapter` プロトコルに適合しているか `mypy` で検証する。
- [ ] UseCase 層の既存テストを、新しい `Metadata` オブジェクトを使用して正常に動作するか再確認する。
