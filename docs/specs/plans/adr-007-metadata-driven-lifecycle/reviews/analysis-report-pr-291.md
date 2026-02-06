# Analysis Report - Data Model & Adapter Protocols

## 1. 意図の深掘り (Deep Dive into Intent)
- **Why**: ADR-007 で定義された「メタデータ駆動ライフサイクル」を実現するため。
- **Why**: UseCase 層が特定のインフラ実装（GitHub API やローカルファイルシステム）に強く結合するのを防ぎ、テスト容易性と保守性を向上させるため。
- **Outcome**: 
  - 厳密なスキーマに基づくメタデータ管理。
  - 日本語キーなどの曖昧さを排除した正規化されたデータアクセス。
  - Adapter 間のインターフェース契約の明文化による並列開発の促進。

## 2. ギャップ分析 (Gap Analysis)
- **理想**: 
  - `Document` が `Metadata` オブジェクトを持ち、`metadata.validate()` でエラーを即座に検知。
  - UseCase は `IFileSystemAdapter` などのプロトコルに依存。
- **現実**: 
  - `Document` は `dict` を直接操作しており、パース直後にバリデーションが行われない。
  - `typing.Protocol` によるインターフェース定義が存在しない。
- **制約**:
  - 既存の `Document` クラスのインターフェースを極力維持しつつ、内部的に `Metadata` オブジェクトに移行する必要がある（後方互換性）。

## 3. 仮説の立案 (Hypotheses)

### 3.1. 実証的仮説 (Grounded Hypothesis) - 本命案
- **アプローチ**: 
  - `src/issue_creator_kit/domain/document.py` に `Metadata` クラスを定義。`Document` は `metadata: Metadata` プロパティを持つ。
  - `src/issue_creator_kit/domain/interfaces.py` を作成し、仕様書通りの Protocol を定義。
  - `src/issue_creator_kit/domain/exceptions.py` に `InfrastructureError` 系統の例外を定義。
- **メリット**: 仕様に最も忠実で、実装の確実性が高い。
- **リスク**: `metadata` が `dict` でなくなったことによる、既存 UseCase (`creation.py` 等) への影響。エイリアス（`.get("ID")` 等）の処理を `Metadata` クラス内で完結させる必要がある。

### 3.2. 飛躍的仮説 (Leap Hypothesis) - 理想案
- **アプローチ**: Pydantic を使用して `Metadata` モデルを定義し、自動バリデーションとシリアライズを行う。
- **メリット**: コード量が減り、型安全性が最高レベルになる。
- **リスク**: プロジェクトに Pydantic が導入されているか？（`pyproject.toml` を確認済み、`pydantic` は dependencies に含まれている）。

### 3.3. 逆説的仮説 (Paradoxical Hypothesis) - 最小構成案
- **アプローチ**: `Metadata` を独立したクラスにせず、`dict` のままでバリデーション関数を適用する。プロトコルも最小限のメソッドのみ定義する。
- **メリット**: 既存コードへの影響が極小。
- **リスク**: 長期的に「メタデータ駆動」の複雑化に対応できなくなる可能性がある。

## 4. 推奨案 (Recommendation)
**飛躍的仮説 (Pydantic 利用)** を採用する。
- `pyproject.toml` に `pydantic` が含まれているため、これを利用して `Metadata` スキーマを定義するのが最も効率的で堅牢。
- 日本語キーの正規化は Pydantic の `model_validator` (before) で処理する。
- `Document` クラスは Pydantic モデルをラップするか、あるいは `Document` 自体も Pydantic モデルにする。
