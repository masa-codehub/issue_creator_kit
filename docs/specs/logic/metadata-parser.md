# Metadata Parser Specification

## 1. Overview

- **Responsibility**: Markdown ファイルの YAML フロントマターを抽出し、Pydantic モデルを用いて厳格に検証・変換する。ADR-013 に基づき、`type` フィールドの必須化とスキーマ厳格化を強制する。
- **Collaborators**: `Document` (ADR/Task models).

## 2. Data Structures (Models)

### 2.1. RawMetadata

- **Schema**:
  - `id`: str (regex: `(task|adr)-\d{3}(?:-\d+)?`)
  - `type`: Literal["adr", "task", "integration"] (**Required**, no default)
  - `title`: str
  - `status`: str
  - `depends_on`: List[str] (Optional, default: [])
  - `parent`: str (Required if `type == "task"`)

## 3. Interfaces (API/Methods)

### 3.1. DocumentParser.parse()

- **Signature**: `parse(content: str) -> Document`
- **Exceptions**: `MetadataNotFoundError` (Missing metadata), `MetadataParseError` (JSON/Format error), `MetadataValidationError` (Schema mismatch).

## 4. Logic & Algorithms

### 4.1. Strict Parsing Flow

1.  **Frontmatter Extraction**: `python-frontmatter` 等を用いて YAML セクションを抽出。
2.  **Type Constraint Enforcement (ADR-013)**:
    - `type` フィールドが存在しない場合、即座に `MetadataValidationError` (Missing field) エラー。
    - 値が `adr`, `task`, `integration` 以外の場合、`MetadataValidationError` エラー。
3.  **Pydantic Validation**:
    - 抽出した辞書を Pydantic モデル（`ADR` or `Task`）へ流し込む。
    - フィールド欠落や型不整合は `MetadataValidationError` として詳細を報告。

## 5. Traceability

- **Merged Files**:
  - `spec-012-metadata-parser.md` (Legacy)
- **Handover Constraints**:
  - **Constraint 3**: `type` フィールドのデフォルト値排除と明示的エラーメッセージ。
