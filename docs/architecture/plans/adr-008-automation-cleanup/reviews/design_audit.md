# 目標定義監査レポート (Design Audit) - Issue #315

## 1. ドキュメントの要件 (Requirements for Documentation)
- [x] **アウトプット定義:** 作成すべきドキュメントの種類とファイル名が明確か？
  - **根拠:** `docs/architecture/arch-structure-issue-kit.md` および `arch-structure-007-metadata.md` の更新。
- [x] **記述の観点:** ドキュメントに含めるべき主要な論点や決定事項がリストアップされているか？
  - **根拠:** UseCase 削除、Scanner 追加、Invariants (ID形式, 依存関係) の集約を定義済み。

## 2. 整合性と品質 (Consistency & Quality)
- [x] **SSOT整合性:** 上位の設計や既存のADRと矛盾する内容を書こうとしていないか？
  - **根拠:** ADR-008 および `arch-structure-008-scanner.md` (SSOT) に基づく。
- [x] **テンプレート:** 使用すべきテンプレートが指定されているか？
  - **根拠:** 既存ファイルの更新であるため、現在の構成を維持しつつ `drafting-architecture` の資産（C4, arch-structure 等）を参考にする。

## 3. 改善提案 (Improvement Proposals)
- **[Invariants の転記]:**
  - **現状の問題:** `arch-state-007-lifecycle.md` にも Invariants があり、重複する可能性がある。
  - **改善案:** `metadata.md` に構造的制約を集約し、`lifecycle.md` からは `metadata.md` を参照する形式に整理する。
