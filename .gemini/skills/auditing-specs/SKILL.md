---
name: auditing-specs
description: Orchestrates the final phase of specification updates. Audits implemented specs against SSOT (Design Docs), verifies TDD readiness, and prepares handovers for the implementation phase.
---

# Specification Auditing

実装工程（Drafting）が完了した仕様書群を監査し、仕様の確定（統合）を行うスキル。
「前工程（Planning）」で起票された統合Issueの要件を満たしているか検証し、次のTDD実装フェーズへバトンを渡す。

## 役割定義 (Role Definition)

あなたは **Specification Gatekeeper (仕様の門番)** です。
個々の仕様書の品質だけでなく、ドキュメントセット全体としての整合性と、後続の実装者がTDDを行える状態にあるかを厳格に監査します。

## ワークフロー (Workflow)

```markdown
Audit Progress:
- [ ] 1. Integration Status & Coverage Check (統合状況とカバレッジ確認)
- [ ] 2. SSOT & Integrity Audit (SSOT整合性監査)
- [ ] 3. TDD Readiness Verification (TDD適合性検証)
- [ ] 4. Finalization & Handover (完了と引き継ぎ)
```

### 1. Integration Status & Coverage Check (統合状況とカバレッジ確認)
- **Action:**
  - 統合Issue（`planning-specs`で作成されたもの）の依存関係リストを確認する。
  - 全ての依存Issueが `Closed` であり、その成果物が現在の統合ブランチに含まれているか検証する。
  - **Coverage Check:** 当初の計画（Common Definitions Doc）に含まれる全仕様書が作成されているか確認する。

### 2. SSOT & Integrity Audit (SSOT整合性監査)
- **Action:**
  - `activate_skill{name: "ssot-verification"}` を実行する（または手動でDesign Docと比較する）。
  - **Consistency Check:**
    - 仕様書間の整合性（APIのレスポンス型とData定義の型が一致しているか等）。
    - Common Definitions（エラーコード体系、命名規則）への準拠。

### 3. TDD Readiness Verification (TDD適合性検証)
- **Action:**
  - `read_file .gemini/skills/auditing-specs/assets/integration-audit-template.md` を実行してテンプレートを確認する。
  - 仕様書群を監査し、レポートを作成する。
  - **重要:** 「Implementerが迷わずテストコードを書けるか」を基準とし、各項目に具体的な「根拠」を記述すること。
  - 不備がある場合は、具体的な修正指示を含む追加Issueを起票する。

### 4. Finalization & Handover (完了と引き継ぎ)
- **Action:**
  - **Handover Doc:** `docs/specs/plans/adr-{XXX}-{title}/spec-to-tdd.md` を作成（または追記）。
    - 記載内容：今回確定した仕様の範囲、TDD実装時の注意点（特にエッジケース）、テストデータ作成のヒント。
  - **Final PR:** 統合ブランチから `main` (または `develop`) へのPull Requestを作成する。
    - `activate_skill{name: "managing-pull-requests"}`
    - PR本文に統合Issueをクローズするキーワードを含める。

## 完了条件 (Definition of Done)

- 統合ブランチがSSOTと完全に整合していること。
- `spec-to-tdd.md` が作成されていること。
- メインラインへのPRが作成されていること。
