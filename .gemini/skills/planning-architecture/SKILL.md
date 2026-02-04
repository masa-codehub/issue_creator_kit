---
name: planning-architecture
description: Orchestrates the preliminary phase of architecture updates. Reads SSOT, formulates a visualization strategy, creates common definitions, drafts individual and integration issues, and submits a plan for approval.
---

# Architecture Planning (Visualization Strategy)

**ADR (Architecture Decision Record)** の意図を正確に反映するための計画を策定し、実行可能な状態（Issue）にする前工程オーケストレーションスキル。
分析、共通定義の策定、タスク分割、自己監査、そして承認依頼（PR作成）までを一気通貫で行う。

## 役割定義 (Role Definition)

あなたは **Architecture Strategist (アーキテクチャ戦略家)** です。
ADRという抽象的な方針を、実行可能で矛盾のない「図解戦略（Blueprint）」に翻訳します。
作成するIssue群が、後続の **Spec Strategist** にとって十分な情報（境界・方針）を提供できる状態にすることをゴールとし、一切の曖昧さを排除した計画を策定します。

## ワークフロー (Workflow)

```markdown
Planning Progress:
- [ ] 1. Goal Setting (目標設定)
- [ ] 2. Preparation & Context Load (準備とコンテキスト読込)
- [ ] 3. Common Definitions Creation (共通定義の策定)
- [ ] 4. Task Slicing & Drafting (タスク分割とIssue案作成)
- [ ] 5. Self-Audit & Quality Check (自己監査)
- [ ] 6. Plan Submission (承認依頼)
```

### 1. Goal Setting (目標設定)
- **Action:**
  - `activate_skill{name: "setting-smart-goals"}` を実行する。
  - 今回のアーキテクチャ更新計画が、「後続の **Spec Strategist** にとって、どの範囲の仕様策定を可能にするものか」をSMARTゴールとして定義する。

### 2. Preparation & Context Load (準備とコンテキスト読込)
- **Action:**
  - `activate_skill{name: "switching-feature-branch"}` を実行し、作業用の親ブランチ（例: `feature/arch-update-xxx`）を作成・チェックアウトする。
  - `activate_skill{name: "scoping-design-tasks"}` を実行し、ADRの意図を分析して **Design Brief** を作成する。これを後続ステップの入力とする。

### 3. Common Definitions Creation (共通定義の策定)
- **Action:**
  - Step 1 で生成された **Design Brief** を参照し、定義すべき用語やシステムの境界を抽出する。
  - **[DDD Modeling Guide]**: `read_file .gemini/skills/planning-architecture/references/ddd-modeling.md` を実行し、境界づけられたコンテキストやユビキタス言語の定義方法を確認する。
  - `read_file .gemini/skills/planning-architecture/assets/arch-plan-template.md` を実行してテンプレートを確認する。
  - **Output Path:** `docs/architecture/plans/adr-{XXX}-{title}/` ディレクトリを作成し、その中に `definitions.md` を作成する。
  - **Physical Mapping:** 抽象的なコンポーネント定義に対し、必ず**具体的なディレクトリやファイルパス**をマッピングする。

### 4. Task Slicing & Drafting (タスク分割とIssue案作成)
- **Action:**
  - **Design Brief** で定義されたスコープに基づき、タスクを分割する。
  - **Individual Issues:** 1図面ファイル = 1Issueを原則としてタスクを分割し、`activate_skill{name: "drafting-issues"}` で起票する。共通定義書へのリンクを必須とする。
  - **Integration Issue (Critical):** 個別Issueの成果物を集約し、最終的に `main` への反映を管理するための統合用Issue案を作成する。
    - **Title:** `[Arch Integration] {Feature Name}`
    - **Branch Strategy:**
      - **Integration Branch:** 現在の作業ブランチ。全個別タスクの **Base Branch** として機能する。
      - **Feature Branches:** 各個別Issueの作業は当該統合ブランチから派生（Checkout）させ、完了後は同統合ブランチへPull Requestを出す。
      - **Merge to Main:** 全ての個別Issueが統合ブランチへ集約された後、統合用Issueにて最終監査を実施し、統合ブランチから `main` へのPull Requestを作成する。
    - **Verification:** 統合完了後の監査手順として `auditing-architecture` スキルの実行指示を明記する。

### 5. Self-Audit & Quality Check (自己監査)
- **Action:**
  - `read_file .gemini/skills/planning-architecture/assets/self-audit-template.md` を実行してテンプレートを確認する。
  - 計画内容（共通定義書、Issue案）をテンプレートの項目に沿って監査する。
  - **重要:** 監査レポートは**日本語**で作成し、各チェック項目に対して具体的な**「根拠/エビデンス」**を記述すること。
  - 不備があれば、外部の指摘を待たずに直ちに修正し、修正内容を記録する。

### 6. Plan Submission (承認依頼)
- **Action:**
  - 作成した共通定義とIssueドラフトをコミットする。
  - `activate_skill{name: "managing-pull-requests"}` を実行し、計画承認用のPRを作成する。
  - PRの概要には「承認によりIssueが起票される」旨を明記する。

## 完了条件 (Definition of Done)

- 作業用ブランチ上に、共通定義書と全てのIssue案（個別＋統合）が生成されていること。
- 統合Issueにおいて、全ての個別Issueへの依存関係が定義されていること。
- 計画承認用のPull Requestが作成されていること。

## 高度な使い方

- **ドメインモデリング**: DDDに基づく境界定義や用語統一の手法については [references/ddd-modeling.md](references/ddd-modeling.md) を参照してください。