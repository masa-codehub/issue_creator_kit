# Architecture to Specification Handover (ADR-008)

## 1. 概要 (Overview)
- **ADR ID:** ADR-008 (Automation Cleanup & Scanner)
- **Status:** ✅ PASS (Final Audit Completed)
- **Next Phase:** Specification Drafting (007-T3-*)

## 2. 確定したアーキテクチャ (Finalized Architecture)
- **Scanner Foundation:** `docs/architecture/arch-structure-008-scanner.md` および `docs/architecture/arch-structure-issue-kit.md` が実装の正解（SSOT）である。
- **Lifecycle:** `docs/architecture/arch-state-007-lifecycle.md` に基づき、物理ファイルの移動（`_inbox` -> `_approved` -> `_archive`）によって状態遷移を実装すること。
- **Invariants:** Pydantic Model で `docs/architecture/arch-structure-007-metadata.md` に集約された不変条件（ID形式、循環参照禁止）を実装すること。

## 3. 仕様策定への制約・注意点 (Constraints & Guidelines)
### 3.1. 残存課題 (Known Issues)
- 現時点で本ADRに紐づく既知の残存課題はありません。
- `docs/architecture/arch-structure-issue-kit.md` は本PRで `arch-structure-008-scanner.md` と整合するよう更新済みであることを前提とし、今後の変更時も両ドキュメントの整合性を維持すること。実装時は `arch-structure-issue-kit.md` ではなく **`arch-structure-008-scanner.md` を優先** すること。

### 3.2. 実装の重点 (Focus Areas)
- **Fail-Fast:** Scanner は不整合（ID重複、循環参照）を検知したら即座に停止する設計とすること。
- **Idempotency:** 冪等性を担保すること（何度実行しても同じ結果、あるいは安全なNo-Opになること）。

## 4. 参照リンク (References)
- [Audit Report](./reviews/integration-audit.md)
- [Design Brief](./design-brief.md)
- [Review Analysis](./reviews/pr-316-analysis.md)
