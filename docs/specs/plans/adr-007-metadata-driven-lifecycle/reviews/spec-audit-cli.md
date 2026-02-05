# Specification Drafting Self-Audit Report - CLI Specification Update

## 1. Overview
- **Target File:** `docs/specs/api/cli_commands.md`
- **Related Issue:** GitHub Issue #283

## 2. Audit Checklist

### 2.1. TDD Readiness (TDD適合性)
- [x] **Concrete Inputs/Outputs:** 各コマンドの引数（`--before`, `--after`, `--archive-dir`, `--adr-id` 等）が具体的に定義されている。
  - **根拠:** Section 3.2, 3.3.
- [x] **Validation Rules:** 必須引数とオプション引数が区別され、不足時の挙動が定義されている。
  - **根拠:** Section 4.2 および Section 5.2.
- [x] **Test Cases (Edge Cases):** 引数不足時のエラー、`--adr-id` によるフィルタリング、デフォルト値の適用が TDD Criteria に含まれている。
  - **根拠:** Section 5.2.

### 2.2. SSOT Integrity
- [x] **Common Defs Compliance:** ADR-007 で定義された `reqs/tasks/_archive/` というパス名に準拠している。
  - **根拠:** Section 3.2, 3.3, 6.
- [x] **Design Alignment:** ADR-007 の「メタデータ駆動」「再帰探索」という意図を反映している。
  - **根拠:** Section 3.2 概要およびオプション引数。

### 2.3. No Ambiguity
- [x] **Forbidden Terms:** "TBD", "Pending", "Any" は含まれていない。
  - **根拠:** grep による確認済み。

## 3. Improvement Proposals (改善提案)
- **Proposal 1:** 今回の Spec 更新に合わせて、`argparse` での具体的な実装方法（`choices` や `type`）についても言及があると、実装者が迷わなくなる可能性があるが、Interface 層の仕様としては現在の記述で十分と判断。

## 4. Final Verdict
- [x] **PASS**
