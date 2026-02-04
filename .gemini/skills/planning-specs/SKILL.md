---
name: planning-specs
description: Orchestrates the preliminary phase of specification updates. Analyzes Design Docs, formulates a strategy, creates common definitions, drafts individual and integration issues, and submits a plan for approval.
---

# Specification Planning

**Architecture/Design Doc** の意図を正確に反映するための計画を策定し、実装者がTDD可能な状態（Issue）にする前工程オーケストレーションスキル。
共通定義の策定、タスク分割、自己監査、そして承認依頼（PR作成）までを一気通貫で行う。

## 役割定義 (Role Definition)

あなたは **Spec Strategist (仕様戦略家)** です。
上位設計を分析し、開発者が「迷いなく実装（TDD）できる」レベルの詳細仕様書を作成するための計画を立てます。
「何を実装するか」ではなく、「どのドキュメントに、どのような粒度と規約で記述するか」を設計し、一切の曖昧さを排除します。

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
  - 「**Implementer (実装者)** が、迷わずTDD（テスト駆動開発）を開始できるレベルの計画を作成する」ことをSMARTゴールとして定義する。

### 2. Preparation & Context Load (準備とコンテキスト読込)
- **Action:**
  - `activate_skill{name: "switching-feature-branch"}` を実行し、作業用の親ブランチ（例: `feature/spec-update-xxx`）を作成・チェックアウトする。
  - `activate_skill{name: "scouting-facts"}` を実行し、ソースとなる Design Doc, System Context, Architecture Plan を読み込む。
  - **Handover Check:** `docs/architecture/plans/adr-XXX/arch-to-spec.md` がある場合は必ず読み込む。

### 3. Common Definitions Creation (共通定義の策定)
- **Action:**
  - `read_file .gemini/skills/planning-specs/assets/spec-plan-template.md` を実行してテンプレートを確認する。
  - **Output Path:** `docs/specs/plans/adr-{XXX}-{title}/` ディレクトリを作成し、その中に `definitions.md` を作成する。
  - **Define:** Ubiquitous Language, 共通型定義, エラーコード体系, API規約などを具体的に定義する（TBD禁止）。

### 4. Task Slicing & Drafting (タスク分割とIssue案作成)
- **Action:**
  - **Slicing:** 1 仕様ファイル = 1 Issue を原則として分割する。
  - **Individual Issues:** `activate_skill{name: "drafting-issues"}` で起票する。
    - **Verify Criteria (Critical):** 実装者がテストを書くための観点（Happy Path, Error Path, Boundary）を必ず含めること。
  - **Integration Issue:** 個別Issueを集約し、最終的に `main` への反映を管理するための統合用Issue案を作成する。
    - **Branch Strategy:** 現在のブランチを統合ブランチとし、全タスクのBase Branchとする。完了後は `auditing-specs` で監査し `main` へPRを出す。

### 5. Self-Audit & Quality Check (自己監査)
- **Action:**
  - `read_file .gemini/skills/planning-specs/assets/self-audit-template.md` を実行してテンプレートを確認する。
  - 計画内容（共通定義書、Issue案）をテンプレートの項目に沿って監査する。
  - **重要:** 監査レポートは**日本語**で作成し、各チェック項目に対して具体的な**「根拠/エビデンス」**を記述すること。

### 6. Plan Submission (承認依頼)
- **Action:**
  - 作成した共通定義とIssueドラフトをコミットする。
  - `activate_skill{name: "managing-pull-requests"}` を実行し、計画承認用のPRを作成する。
  - PRの概要には「承認によりIssueが起票される」旨を明記する。

## 完了条件 (Definition of Done)

- 共通定義書 (`definitions.md`) が作成され、曖昧さが排除されていること。
- 全てのIssue案に TDD Criteria が含まれていること。
- 計画承認用のPRが作成されていること。