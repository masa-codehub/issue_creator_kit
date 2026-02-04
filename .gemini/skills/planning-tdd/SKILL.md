---
name: planning-tdd
description: Orchestrates the preliminary phase of TDD implementation. Analyzes specifications, formulates test strategies (mocking, fixtures), drafts individual and integration issues, and submits a plan for approval.
---

# TDD Planning

**詳細仕様書 (Spec)** を入力とし、開発者が迷わず実装（Red/Green/Refactor）を開始できるための計画を策定するスキル。
テスト戦略の構築、共通フィクスチャの定義、タスク分割、自己監査を一気通貫で行う。

## 役割定義 (Role Definition)

あなたは **TDD Strategist (TDD戦略家)** です。
仕様を「テスト可能な単位」に分解し、外部依存（DB, API等）の扱いを明確にします。
実装者が「テストの書き方」で迷う時間をゼロにし、ロジックの実装に集中できる環境を整えます。

## ワークフロー (Workflow)

```markdown
Planning Progress:
- [ ] 1. Goal Setting (目標設定)
- [ ] 2. Preparation & Context Load (準備とコンテキスト読込)
- [ ] 3. Test Strategy Formulation (テスト戦略の策定)
- [ ] 4. Task Slicing & Drafting (タスク分割とIssue案作成)
- [ ] 5. Self-Audit & Quality Check (自己監査)
- [ ] 6. Plan Submission (承認依頼)
```

### 1. Goal Setting (目標設定)
- **Action:**
  - `activate_skill{name: "setting-smart-goals"}` を実行する。
  - 「実装者が、迷わずテストコードを書き始め、仕様を満たす実装を完了できる状態」をSMARTゴールとして定義する。

### 2. Preparation & Context Load (準備とコンテキスト読込)
- **Action:**
  - `activate_skill{name: "switching-feature-branch"}` を実行し、統合ブランチ（例: `feature/impl-xxx`）を作成・チェックアウトする。
  - `activate_skill{name: "scouting-facts"}` を実行し、対象の仕様書 (`docs/specs/`) と引継ぎ資料 (`spec-to-tdd.md`) を読み込む。

### 3. Test Strategy Formulation (テスト戦略の策定)
- **Action:**
  - `read_file .gemini/skills/planning-tdd/assets/tdd-plan-template.md` を確認。
  - **Output Path:** `docs/specs/plans/adr-{XXX}-{title}/` ディレクトリを作成し、その中に `tdd-plan.md` を作成する。
  - **Shared Fixtures:** 共通で使うテストデータやユーティリティを定義。
  - **Mock Policy:** 外部依存のモック方法を具体的に指定（使用ライブラリ等）。

### 4. Task Slicing & Drafting (タスク分割とIssue案作成)
- **Action:**
  - **Slicing:** 1 クラス/モジュール = 1 Issue を原則とする。
  - **Individual Issues:** `activate_skill{name: "drafting-issues"}` で起票。
    - 仕様書の **Verify Criteria** をタスクの完了条件に含める。
  - **Integration Issue:** 最終監査 (`auditing-tdd`) を担当する統合Issueを作成。
    - 現在のブランチを Base Branch とし、全成果物を集約する。

### 5. Self-Audit & Quality Check (自己監査)
- **Action:**
  - `read_file .gemini/skills/planning-tdd/assets/self-audit-template.md` を使用。
  - 監査レポートを日本語・根拠付きで作成し、不備があれば修正する。

### 6. Plan Submission (承認依頼)
- **Action:**
  - `activate_skill{name: "managing-pull-requests"}` を実行し、計画承認用のPRを作成する。

## 完了条件 (Definition of Done)

- 共通テスト戦略 (`tdd-plan.md`) が作成されていること。
- 全てのIssue案に具体的なテスト観点が含まれていること。
- 計画承認用のPRが作成されていること。