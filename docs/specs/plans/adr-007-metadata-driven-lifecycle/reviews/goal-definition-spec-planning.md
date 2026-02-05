# Goal Definition: Spec Planning for ADR-007

## 1. 概要 (Overview)
- **Goal Name:** Spec Planning for Metadata-driven Lifecycle
- **Related Issue:** (Integration Issue L2 is missing, tracking as 007-T3 context)
- **Objective:** ADR-007で定義されたメタデータ駆動ライフサイクルを実装するため、詳細仕様（Spec）の更新計画とタスク分割を行う。実装者が迷いなくTDDに入れるレベルまで曖昧さを排除する。

## 2. 具体的な目標 (Specific Goals)
- **S1 (Definitions):** `docs/specs/plans/adr-007-metadata-driven-lifecycle/definitions.md` を作成し、メタデータスキーマ、DAG解析ルール、ステータス同期ロジックの共通定義を策定する。
- **S2 (Task Splitting):** 変更が必要な仕様書（Spec）ごとにタスクを分割し、Issue Draft（`reqs/tasks/007-T3-XX.md`）を作成する。
    - CLI仕様 (`specs/api/cli_commands.md`)
    - ドキュメントモデル (`specs/data/document_model.md`)
    - 作成/同期ロジック (`specs/logic/*.md`)
- **S3 (Criteria):** 各タスクに「TDD可能なテスト基準（Happy/Error Path）」を含める。

## 3. 検証条件 (DoD - Definition of Done)
### 3.1. Deliverables Check
- [ ] `docs/specs/plans/adr-007-metadata-driven-lifecycle/definitions.md` が存在すること。
- [ ] 以下の Issue Draft が `reqs/tasks/adr-007/` (※) に作成されていること。
    - `007-T3-01-spec-model.md` (Document Model)
    - `007-T3-02-spec-cli.md` (CLI Commands)
    - `007-T3-03-spec-logic.md` (Lifecycle Logic)
    (※ ADR-007に基づき、タスクフォルダはフラットな `reqs/tasks/<ADR-ID>/` を使用する)

### 3.2. Quality Check
- [ ] 共通定義書に「DAG解析アルゴリズム」と「冪等性担保」の記述があること。
- [ ] Issue Draft の `Verification Criteria` に具体的なテストケース記述があること。

## 4. 制約事項 (Constraints)
- **Architecture Handover:** `docs/architecture/plans/adr-007-metadata-driven-lifecycle/arch-to-spec.md` の制約（DAG解析、Atomic Move）を遵守する。
- **Existing Specs:** 既存の仕様書（`specs/`配下）との整合性を保ち、破壊的変更を最小限にする（または明示的に更新する）。

## 5. 推定工数 (Estimated Effort)
- 計画策定: 1 hour
