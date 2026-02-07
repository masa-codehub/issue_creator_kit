# Specification Drafting Self-Audit Report: CLI Integration

## 1. Overview
- **Target File:** `docs/specs/components/cli-integration.md`
- **Related Issue:** #323 (ADR-008: Integrate CLI with Scanner Foundation)

## 2. Audit Checklist

### 2.1. TDD Readiness (TDD適合性)
- [x] **Concrete Inputs/Outputs:** 入力パラメータと期待される戻り値（型、フォーマット）が具体的に定義されているか？
  - **根拠:** "コマンド定義" セクションにて、各コマンドの引数（`--root`, `--dry-run`）と、標準出力への期待される形式（ID リスト、Mermaid 文字列）を定義している。
- [x] **Validation Rules:** すべての入力項目に対して、具体的なバリデーションルールが書かれているか？
  - **根拠:** `process` コマンドにおいて、依存関係エラー（循環参照等）が発生した場合の終了コード `1` とエラーメッセージ表示について記述している。
- [x] **Test Cases (Edge Cases):** Null、空文字、境界値、異常系などのエッジケースが網羅されているか？
  - **根拠:** エラーハンドリングセクションで、ドメイン層から発生する各種バリデーションエラーに対する CLI の挙動を定義している。

### 2.2. SSOT Integrity
- [x] **Common Defs Compliance:** 用語、エラーコード、データ型は `Common Definitions` に準拠しているか？
  - **根拠:** `definitions.md` で定義された用語（`Physical State Scanner` 等）を使用し、アーキテクチャ図（`arch-structure-008-scanner.md`）のコンポーネント構成に従っている。
- [x] **Design Alignment:** 上位のDesign Docの意図を正しく反映しているか？
  - **根拠:** ADR-008 の「Cleanup」の意図を汲み、旧コマンドの削除/非推奨方針を明記している。

### 2.3. No Ambiguity
- [x] **Forbidden Terms:** "TBD", "Pending", "Any" などの曖昧な表現が含まれていないか？
  - **根拠:** ファイル全体を検索し、曖昧な表現がないことを確認済み。

## 3. Improvement Proposals (改善提案)
- **Proposal 1:** 実際の `ick process` で起票（Action）を行う際の仕様は、将来のタスク（Task-008-06等）で定義することを注記しておくと、実装者が迷わなくて済む。

## 4. Final Verdict
- [x] **PASS**
