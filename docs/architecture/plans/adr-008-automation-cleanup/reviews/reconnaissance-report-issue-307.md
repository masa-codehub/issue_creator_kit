# 能動的偵察レポート (Reconnaissance Report)

## 1. 調査対象と意図 (Scope & Context)
- **ユーザー依頼のキーワード:** `Metadata`, `Domain Guardrails`, `Validation Rules`, `Pydantic`, `ADR-008`
- **調査の目的:** アーキテクチャドキュメント `docs/architecture/arch-structure-007-metadata.md` に、ドメインガードレール（ID形式や依存関係の制約）を追記するための事実収集。
- **調査時のブランチ (Branch Context):** `main` (Issueでは `feature/task-008-03-metadata` での作業が指定されているが、ベースの事実は `main` および `origin/feature/arch-update-adr008` に存在)

## 2. 収集された事実 (Evidence)

### A. ドキュメント上の規定 (SSOT)
- **[Source]:** `docs/architecture/plans/adr-008-automation-cleanup/definitions.md`
  - **事実・規定:** Domain Guardrails として ID 形式と依存関係の制約が定義されている。
  - **引用:**
    > ### Domain Guardrails (ドメイン・ガードレール)
    > - **Definition**: Invariant checks implemented in the Domain Layer (Pydantic Models) to prevent invalid states.
    > - **Checks**:
    >   - **ID Format**: Must match `adr-\d{3}-.*` for ADRs, or `task-\d{3}-\d{2,}` for Tasks (e.g., `task-008-01`).
    >   - **Dependency**: `depends_on` must reference valid IDs. No self-reference. No cycles.
- **[Source]:** `docs/architecture/arch-structure-007-metadata.md`
  - **事実・規定:** メタデータ駆動型アーキテクチャの構造を定義しているが、具体的なフィールド毎のバリデーションルールは未記述。

### B. 実装の現状 (Codebase Reality)
- **[File]:** `src/issue_creator_kit/domain/document.py`
  - **責務:** メタデータの Pydantic モデル (`Metadata`) とドキュメントのパースを担当。
  - **事実:** 現在の `id` のバリデーションは `pattern=r"^[a-z0-9-]+$"` となっており、ADR-008 の規定より緩い。また `depends_on` の循環参照チェックはモデル内には未実装（スカウターサービス等での実装が予定されている）。
  - **コード抜粋:**
    ```python
    class Metadata(BaseModel):
        # ...
        id: str = Field(..., pattern=r"^[a-z0-9-]+$")
        # ...
        depends_on: list[str] = Field(default_factory=list)
        # ...
    ```

### C. 物理構造と依存関係 (Structure & Dependencies)
- **ディレクトリ:** `src/issue_creator_kit/domain/`
- **依存関係:** `pydantic` を使用してガードレールを実装している。

## 3. 発見された制約と矛盾 (Constraints & Contradictions)
- **SSOTとの乖離:** `definitions.md` で定義された ID 形式 (`adr-\d{3}-.*` 等) が、現在の `arch-structure-007-metadata.md` や `document.py` の実装に反映されていない。
- **実装マッピングの不足:** アーキテクチャドキュメントにおいて、どのコードがバリデーションを担うか（`src/issue_creator_kit/domain/models` へのマッピング）の記述が欠落している。

## 4. 補足・未調査事項 (Notes & Unknowns)
- Issue では `src/issue_creator_kit/domain/models` へのマッピングが言及されているが、現状そのディレクトリは存在せず、`document.py` にモデルが混在している。リファクタリングで移動する予定があるのか、単なる誤記かの確認が必要（分析フェーズで検討）。
