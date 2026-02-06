# Reconnaissance Report - Data Model & Adapter Protocols

## 1. 調査範囲 (Scope)
- `docs/specs/data/document_model.md`: `Document`/`Metadata` モデルの仕様
- `docs/specs/components/infra_adapters.md`: 各 Adapter インターフェースの仕様
- `src/issue_creator_kit/domain/document.py`: 既存の `Document` 実装
- `src/issue_creator_kit/infrastructure/`: 各 Adapter の既存実装
- `tests/unit/domain/test_document.py`: 既存のドキュメントテスト

## 2. 収集された事実 (Facts)

### 2.1. Document / Metadata モデルの現状
- **既存実装**: `src/issue_creator_kit/domain/document.py` に `Document` クラスが存在。
  - `parse` メソッドで YAML Frontmatter と Markdown List をサポート。
  - `to_string` でシリアライズ。
  - **不足点**: `Metadata` クラスが未定義（`dict`を使用）。ADR-007 に基づく厳密なバリデーション、正規化（日本語キー対応）が未実装。
- **仕様 (`document_model.md`)**:
  - `Metadata` クラスが必要。必須フィールド: `id`, `status` (共通)、`parent`, `type`, `phase`, `depends_on` (タスク固有)。
  - `status` は `Draft`, `Ready`, `Issued`, `Completed` 等の Enum 的な値を許容。
  - 正規化ルール: キーの小文字化、日本語キーから英語キーへのエイリアスマッピング。
  - シリアライズ: 常に YAML Frontmatter 形式を優先。

### 2.2. Adapter インターフェースの現状
- **既存実装**: `infrastructure/` 配下に具象クラス (`FileSystemAdapter`, `GitHubAdapter`, `GitAdapter`) が存在。
  - **問題点**: 抽象インターフェース (Python Protocol) が定義されていない。UseCase が具象クラスに依存している（`tests/unit/usecase/test_creation.py` を参照）。
- **仕様 (`infra_adapters.md`)**:
  - `IFileSystemAdapter`, `IGitHubAdapter`, `IGitAdapter` の定義が必要。
  - 各 Adapter で送出すべき例外 (`InfrastructureError`, `GitHubAPIError`, `FileSystemError` 等) が定義されている。
  - `GitHubAdapter` には `sync_issue` などの高度なメソッドが要求されている（現状未実装）。

### 2.3. テストの現状
- `tests/unit/domain/test_document.py` に基本的なパーステストがあるが、バリデーションや正規化のテストは不足。

## 3. ギャップ分析 (Gap Analysis)
1. **Domain Model**: `Metadata` クラスの導入とバリデーションロジックの実装が必要。
2. **Interfaces**: `domain/interfaces.py` を新規作成し、`typing.Protocol` で各 Adapter の契約を定義する必要がある。
3. **Exceptions**: `domain/exceptions.py` (あるいは `interfaces.py` 内) に仕様に基づいた例外クラスを定義する必要がある。
4. **Validation**: `id` のフォーマットチェック (`^[a-z0-9-]+$`) やステータス整合性チェックの実装が必要。

## 4. 証拠 (Evidence)
- `src/issue_creator_kit/domain/document.py` (L1-L93): 現状のパース・シリアライズロジック。
- `docs/specs/data/document_model.md` (L45-L100): メタデータフィールドと正規化ルール。
- `docs/specs/components/infra_adapters.md` (L10-L20): インフラ例外の定義。
