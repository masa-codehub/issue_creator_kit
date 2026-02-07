# Architecture to Specification Handover (ADR-008)

## 1. 概要 (Overview)
- **ADR ID:** ADR-008 (Automation Cleanup & Scanner)
- **Status:** Conditional Pass (See Audit Report)
- **Next Phase:** Specification Drafting (007-T3-*)

## 2. 確定したアーキテクチャ (Finalized Architecture)
- **Scanner Foundation:** `docs/architecture/arch-structure-008-scanner.md` が実装の正解（SSOT）である。
- **Lifecycle:** `docs/architecture/arch-state-007-lifecycle.md` に基づき、物理ファイルの移動によって状態遷移を実装すること。
- **Invariants:** Pydantic Model で `arch-state-007-lifecycle.md` に記載された不変条件（ID形式、循環参照禁止）を実装すること。

## 3. 仕様策定への制約・注意点 (Constraints & Guidelines)
### 3.1. 残存課題 (Known Issues)
- **Issue #315:** `docs/architecture/arch-structure-issue-kit.md` の更新が必要。Spec策定前に、またはSpec策定の一部として、このドキュメントと整合性が取れているか確認すること。
- 実装時は `arch-structure-issue-kit.md` ではなく **`arch-structure-008-scanner.md` を優先** すること。

### 3.2. 実装の重点 (Focus Areas)
- **Fail-Fast:** Scanner は不整合（ID重複、循環参照）を検知したら即座に停止する設計とすること。
- **Idempotency:** 冪等性を担保すること（何度実行しても同じ結果、あるいは安全なNo-Opになること）。

## 4. 参照リンク (References)
- [Audit Report](./reviews/integration-audit.md)
- [Design Brief](./design-brief.md)
