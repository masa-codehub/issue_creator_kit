---
name: spec-audit
description: Performs final verification of the specifications. Ensures they meet the Acceptance Criteria and project standards before closing.
---

# Specification Audit

仕様策定フェーズの最終ゲートキーパー。

## 手順 (Procedure)

### 1. 最終監査 (Final Audit)
- **Action:**
  - `ssot-verification` を実行し、SSOT（ADR, Context）との完全一致を確認する。
  - Issueの **Acceptance Criteria** を1つずつ確認し、全ての要件が仕様書に落とし込まれているかチェックする。
  - **判定:** もし修正が必要な不備が見つかった場合、**直ちに `spec-creation` の実行フェーズ（Drafting/Refactoring）に戻り、修正を行うこと。**

### 2. 成果物の定着
- **Action:**
  - `activate_skill{name: "github-commit"}`
  - `activate_skill{name: "github-pull-request"}`

### 3. Closing
- **Action:**
  - `activate_skill{name: "retrospective"}`

## 監査チェックリスト
- [ ] 全てのAcceptance Criteriaが仕様化されているか？
- [ ] 実装者が迷う「曖昧な点」はゼロか？
- [ ] アーキテクチャルール違反はないか？
