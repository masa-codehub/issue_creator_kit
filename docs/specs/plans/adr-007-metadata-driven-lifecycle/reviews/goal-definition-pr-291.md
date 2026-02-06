# Goal Definition - Data Model & Adapter Protocols

## 1. 達成目標 (SMART Goals)
- **Specific**: ADR-007 準拠の `Metadata` モデル (Pydantic) を実装し、`Document` クラスをリファクタリングして統合する。また、`IFileSystemAdapter`, `IGitHubAdapter`, `IGitAdapter` の Protocol を `interfaces.py` に定義する。
- **Measurable**: 
  - `pytest tests/unit/domain/test_document.py` が 100% パスする。
  - `mypy src/issue_creator_kit/domain/` がエラーなしでパスする。
  - `interfaces.py` に 3 つの Protocol が定義されていることを `grep` で確認。
- **Achievable**: Pydantic は既にプロジェクトの依存関係に含まれており、Protocol 定義は Python 3.13 の標準機能で実現可能。
- **Relevant**: 後続の実装タスク (T4-02 ～ T4-04) および UseCase のリファクタリングに不可欠な基盤である。
- **Time-bound**: 本セッション中に実装・検証を完了し、PR を作成する。

## 2. 成果物 (Deliverables)
- `src/issue_creator_kit/domain/exceptions.py`: インフラ例外クラス
- `src/issue_creator_kit/domain/interfaces.py`: Adapter Protocol 定義
- `src/issue_creator_kit/domain/document.py`: `Metadata` モデル導入と `Document` リファクタリング
- `tests/unit/domain/test_document.py`: バリデーションと正規化の網羅テスト

## 3. 検証手順 (Verification)
1. **ドメインモデル検証**:
   - `pytest tests/unit/domain/test_document.py`
   - 不正な ID, ステータス, 型、必須フィールド欠落時に Pydantic の `ValidationError` (またはそれをラップした独自例外) が発生することを確認。
   - 日本語キー (`ID`, `ステータス` 等) が正しく正規化されることを確認。
2. **インターフェース検証**:
   - `src/issue_creator_kit/domain/interfaces.py` に `IGitHubAdapter`, `IFileSystemAdapter`, `IGitAdapter` が定義されている。
   - `sync_issue`, `find_file_by_id`, `get_added_files` 等のメソッドシグネチャが `infra_adapters.md` と一致している。
3. **静的解析**:
   - `ruff check src/issue_creator_kit/domain/`
   - `mypy src/issue_creator_kit/domain/`

## 4. 実行計画 (Action Plan)
1. `exceptions.py` の作成。
2. `interfaces.py` の作成。
3. `test_document.py` に失敗するテストを追加 (Red)。
4. `document.py` に `Metadata` を実装し `Document` を修正 (Green)。
5. リファクタリングと静的解析 (Refactor)。
6. 自己監査と PR 作成。
