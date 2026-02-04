---
title: "[TDD] Implement Core Document & Metadata Logic"
labels: ["gemini:tdd"]
roadmap: "../../../../../docs/implementation/plans/adr-003/tdd-plan.md"
task_id: "T-1"
depends_on: []
status: "Draft"
---

## 1. Goal & Context (Why & What)

### Goal
- `Document` および `Metadata` クラスの実装を完了させ、正規化ロジック、バリデーション、ステータス遷移が詳細仕様書通りに動作することを単体テストで証明する。

### As-is (現状)
- `src/issue_creator_kit/domain/` 配下にコードが存在しない、または不完全。
- 日本語メタデータ（`タイトル`等）のサポートが未実装である可能性が高い。

### To-be (あるべき姿)
- `Document` クラスが Markdown ファイルを適切にパースし、メタデータを構造化できる。
- `Metadata` クラスが全てのキーを小文字に正規化し、エイリアス（日本語キー）を正しくマッピングできる。
- 不正なステータス値や必須項目の欠落に対し、`ValidationError` が送出される。

### Design Evidence
- [Document Domain Model Spec](../../../../../docs/specs/data/document_model.md)
- [TDD Plan](../../../../../docs/implementation/plans/adr-003/tdd-plan.md)

## 2. Input Context (資料 & 情報)
- **Domain Logic**: `src/issue_creator_kit/domain/document.py`
- **Spec**: `docs/specs/data/document_model.md`

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- 外部ライブラリ（`frontmatter` 以外）への依存を増やさないこと。Domain 層は Pure Python であるべき。
- ファイルシステムへの直接アクセス（`open()` 等）を Domain 層に記述しないこと。

### 3.2. Implementation Steps (実行手順)
1.  **Red Phase (Metadata)**:
    - `tests/domain/test_metadata.py` を作成。
    - 日本語キー（`タイトル: ...`）が `title` として取得できることを検証するテストケースを作成。
    - `status` が `Draft`, `Active`, `Archived` 以外の場合にエラーとなるテストケースを作成。
2.  **Green Phase (Metadata)**:
    - `src/issue_creator_kit/domain/document.py` に `Metadata` クラスを実装。
    - Pydantic または Dataclass を使用して正規化ロジックを実装。
3.  **Red Phase (Document)**:
    - `tests/domain/test_document.py` を作成。
    - YAML Frontmatter と Markdown List 形式の両方が正しくパースされることを検証するテストケースを作成。
4.  **Green Phase (Document)**:
    - `src/issue_creator_kit/domain/document.py` に `Document` クラスを実装。
    - `python-frontmatter` をラップした解析ロジックを実装。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/impl-adr003`
- **Feature Branch**: `feature/task-T-1-domain-model`

## 5. Verification & DoD (完了条件)
- [ ] `docs/specs/data/document_model.md` の全要件（正規化、バリデーション、パース）がテストコードで網羅されていること。
- [ ] `pytest tests/domain/` が全件パスすること。
- [ ] `mypy --strict src/issue_creator_kit/domain/` がエラーなしであること。

## 6. TDD Scenarios
- **Scenario 1 (Normalization)**: `metadata = Metadata({"タイトル": "foo", "Status": "Draft"})` -> `metadata.title == "foo"`, `metadata.status == "Draft"`.
- **Scenario 2 (Validation)**: `Metadata({"status": "Unknown"})` -> Raises `ValidationError`.
- **Scenario 3 (Parsing)**: `Document.parse("---\ntitle: foo\n---\nbody")` -> Correctly parses YAML.
