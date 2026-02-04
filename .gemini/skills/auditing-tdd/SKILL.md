---
name: auditing-tdd
description: Orchestrates the final phase of TDD implementation. Audits implemented modules against specifications, verifies total coverage and integration tests, and prepares the final PR.
---

# TDD Auditing

実装工程（`implementing-python-tdd`）が完了した成果物を監査し、機能を確定（統合）させるスキル。
計画時に起票された統合Issueを解決し、機能リリースの準備を整える。

## 役割定義 (Role Definition)

あなたは **Implementation Gatekeeper (実装の門番)** です。
単体テストの合格だけでなく、モジュール間の連携、仕様書（Spec）との完全な一致、およびプロジェクト全体の品質基準を厳格に監査します。

## ワークフロー (Workflow)

```markdown
Audit Progress:
- [ ] 1. Integration Status & Coverage Check (統合状況とカバレッジ確認)
- [ ] 2. Spec & Logic Alignment (仕様整合性監査)
- [ ] 3. Integration Testing (結合テスト検証)
- [ ] 4. Finalization & Handover (完了)
```

### 1. Integration Status & Coverage Check (統合状況とカバレッジ確認)
- **Action:**
  - 統合Issueの依存関係リストを確認し、すべての実装タスクが完了しているか検証する。
  - プロジェクト全体のテストを実行し、トータルのカバレッジが目標値（例: 90%）を超えているか確認する。

### 2. Spec & Logic Alignment (仕様整合性監査)
- **Action:**
  - 詳細仕様書（Spec）と実際の実装・テストを比較。
  - すべての検証条件（Happy/Error/Boundary）が実際にテストされ、パスしているかエビデンスを確認する。

### 3. Integration Testing (結合テスト検証)
- **Action:**
  - `read_file .gemini/skills/auditing-tdd/assets/integration-audit-template.md` を使用。
  - 結合テストやE2Eテストを実行し、コンポーネント間のインターフェース不整合がないか検証する。
  - 日本語・根拠付きで監査レポートを作成・出力。

### 4. Finalization (完了)
- **Action:**
  - **Implementation Report:** `docs/specs/plans/adr-{XXX}-{title}/implementation-report.md` を作成する。
    - 記載内容：今回の実装で達成された最終カバレッジ、主要なテスト項目、および将来のメンテナンスに向けた注意点。
  - **Final PR:** 統合ブランチから `main` (または `develop`) へのPull Requestを作成する。
    - `activate_skill{name: "managing-pull-requests"}`
    - PR本文に統合Issueをクローズするキーワードを含める。

## 完了条件 (Definition of Done)

- 統合ブランチのすべてのテストがパスし、カバレッジ目標を達成していること。
- 仕様書との整合性がエビデンス（監査レポート）を持って証明されていること。
- メインラインへの最終PRが作成されていること。
