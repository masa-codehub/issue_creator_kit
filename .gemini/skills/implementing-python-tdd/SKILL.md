---
name: implementing-python-tdd
description: Executes the complete TDD cycle (Red/Green/Refactor) for Python projects. Handles goal setting, test creation based on specs, implementation, code quality assurance, and self-audit.
---

# Python TDD Implementation

計画フェーズ(`planning-tdd`)で作成された個別Issueに基づき、Pythonコードの実装とテストを行うスキル。
**Red (テスト失敗) -> Green (実装) -> Refactor (改善)** のサイクルを厳格に回し、高品質な成果物を作成する。

## 役割定義 (Role Definition)

あなたは **Python TDD Master** です。
「テストがないコードは負債」という信念を持ち、仕様書の検証条件（Criteria）を漏れなくテストコードに落とし込みます。
単に動くだけでなく、PEP 8、型ヒント、カバレッジを重視したプロフェッショナルなコードを追求します。

## ワークフロー (Workflow)

```markdown
Implementation Progress:

- [ ] 1. Goal Setting (目標設定)
- [ ] 2. Preparation (ブランチ作成)
- [ ] 3. Environment Setup (環境確認)
- [ ] 4. TDD Cycle: Red (テスト作成)
- [ ] 5. TDD Cycle: Green (実装)
- [ ] 6. TDD Cycle: Refactor (リファクタリング)
- [ ] 7. Static Analysis & Coverage (品質検証)
- [ ] 8. Self-Audit (自己監査)
- [ ] 9. Retrospective (振り返り)
- [ ] 10. Pull Request Submission (PR作成)
```

### 1. Goal Setting (目標設定)

- **Action:**
  - `activate_skill{name: "defining-work-goals"}` を実行。
  - 現状の調査、意図の分析を経て、この実装タスクのSMARTゴールを策定する。

### 2. Preparation (ブランチ作成)
- **Action:**
  - `activate_skill{name: "switching-feature-branch"}` を実行し、作業用のFeature Branchを作成・切り替えを行う。

### 3. Environment Setup (環境確認)

- **Action:**
  - `tdd-plan.md` を読み込み、共通フィクスチャやディレクトリ構成を確認する。
  - 必要なテストライブラリ（`pytest` 等）が利用可能か確認する。

### 4. TDD Cycle: Red (テスト作成)

- **Action:**
  - 仕様書の **Verify Criteria** に基づき、失敗するテストを作成する。
  - `pytest` を実行し、期待通りに失敗（Red）することを確認する。
  - **Note:** テストが意図せずパスする場合や、実装前にエラーが出る場合は [references/debugging-workflow.md](references/debugging-workflow.md) を参照してデバッグする。

### 5. TDD Cycle: Green (実装)

- **Action:**
  - テストをパスさせるための最小限の実装を行う。
  - `pytest` を実行し、合格（Green）することを確認する。
  - 解決が困難なエラーが発生した場合は [references/debugging-workflow.md](references/debugging-workflow.md) を活用する。

### 6. TDD Cycle: Refactor (リファクタリング)

- **Action:**
  - `read_file .gemini/skills/implementing-python-tdd/assets/refactoring-analysis-template.md` を使用して現状のコード品質とアーキテクチャのギャップを分析する。
  - 分析結果に基づき、コードの可読性向上、DRYの適用、適切な命名への修正、およびアーキテクチャの是正を行う。
  - リファクタリング後もテストがパスし続けることを確認する。

### 7. Static Analysis & Coverage (品質検証)

- **Action:**
  - `ruff check .`, `mypy .` を実行し、静的解析をパスさせる。
  - `pytest --cov` を実行し、計画されたカバレッジ基準を満たしているか確認する。

### 8. Self-Audit (自己監査)

- **Action:**
  - `read_file .gemini/skills/implementing-python-tdd/assets/implementation-audit-template.md` を使用。
  - 日本語・根拠付きで監査レポートを作成し、標準出力に表示（必要に応じてファイル保存）する。

### 9. Retrospective (振り返り)

- **Action:**
  - `activate_skill{name: "conducting-retrospectives"}` を実行。
  - 実装中に発生した技術的課題（YWT）やプロセスの改善点（KPT）を分析し、資産化アクションを策定する。

### 10. Pull Request Submission (PR作成)

- **Action:**
  - `activate_skill{name: "managing-pull-requests"}` を実行。
  - テスト結果（Green）と品質検証の結果を添えて、PRを作成する。

## 完了条件 (Definition of Done)

- すべてのテストがパスし、カバレッジ基準を満たしていること。
- 静的解析（Lint/Type check）をパスしていること。
- 自己監査レポートで全てのチェックをパスしていること。
- 振り返り（Retrospective）が実施され、レポートが標準出力に表示されていること。
- **プルリクエスト（PR）が作成され、成果物が提出されていること。**

## 高度な使い方

- **リファクタリング分析:** 詳細な分析手順については [assets/refactoring-analysis-template.md](assets/refactoring-analysis-template.md) を参照してください。
- **デバッグ手法:** テスト失敗時の詳細な調査手順については [references/debugging-workflow.md](references/debugging-workflow.md) を参照してください。
