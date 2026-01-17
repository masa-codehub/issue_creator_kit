---
name: arch-planning
description: Formulates a comprehensive strategy for visualizing ADRs. Analyzes the architectural intent, selects necessary diagrams, defines shared definitions, drafts specific issues, and reviews the plan for quality assurance.
---

# Architecture Planning (Visualization Strategy)

**ADR (Architecture Decision Record)** の意図を、第三者に誤解なく伝えるための「図解戦略（Blueprint）」を策定・実行するスキル。
分析、共通定義の策定、Issue案の作成、そして自己レビューまでを一気通貫で行い、高品質な実行計画を作成する。

## 役割 (Role)

**Architecture Strategist (アーキテクチャ戦略家)**
ADRを分析し、「何を描くか」だけでなく、「どう分担するか」を設計する。
全タスクが参照すべき**共通の辞書（Common Definitions）**を作成し、タスク間の依存を疎結合にする。

## 前提 (Prerequisites)

- 入力となる承認済みADR（SSOT）が存在すること。

## 手順 (Procedure)

### 1. 意図の抽出と共通定義 (Intent & Common Definitions)

**目的:** 全タスクで統一すべき「用語」や「境界」を先に定義し、コンフリクトの芽を摘む。
**重要:** タスクが細分化されるため、この共通定義書が唯一の頼みの綱となる。一切の曖昧さを排除せよ。

- **Action:**
  - `activate_skill{name: "active-reconnaissance"}` でADRと現状を分析。
  - **Common Definitions Doc** (`docs/architecture/plans/YYYYMMDD-{feature}-plan.md`) を作成し、以下を定義する。
    - **Ubiquitous Language:** 今回の変更で導入/変更される用語の定義。
    - **Component Naming:** 新規・変更するコンポーネント/クラスの正式名称（Stub）。
    - **Boundaries:** どのドメインがどこまでを担当するか（境界線）。
    - **Tech Decisions:** 全体で統一すべき技術選定（例: 「全APIはgRPCとする」）。
    - **Directory Structure:** 成果物ファイルの配置場所と命名規則。

### 2. 図構成とタスク分割 (Portfolio & Slicing)

**目的:** レビューしやすく、並列作業可能な単位でタスクを分割する。

- **Action:**
  - **Selection Criteria:** ADRの説明に不可欠な図のみを選定する。
  - **Slicing Strategy:** **Atomic Slice (1 Issue = 1 Diagram File)** を原則とする。
    - _原則:_ 1つのアーキテクチャ図ファイルにつき、1つのIssueを発行する。
    - _例外:_ 以下の場合は複数の図を1つのIssueにまとめることを許容する。
      1.  **密結合 (Tight Coupling):** クラス図とシーケンス図など、片方の修正がもう片方に即座に影響し、分離すると不整合リスクが高い場合。
      2.  **微修正 (Trivial Update):** 修正箇所が極めて少なく（数行程度）、分割のオーバーヘッドが見合わない場合。

  - **Output Definition:** 次のステップのために、以下の構成案を確定する。
    1.  **Draft Issue List:** 作成するIssue案のタイトルとファイル名。
    2.  **Target Scope:** 各Issueで作成/更新する具体的な図ファイル名と、その記述範囲。

    **Example:**
    - Issue: `[Context] Update System Context`
      - File: `docs/architecture/context.md`
    - Issue: `[Payment] Create Async Payment Sequence`
      - File: `docs/architecture/seq-payment-async.md`
    - Issue: `[User] Update User Component & State` (Exception: Tight Coupling)
      - Files: `docs/architecture/component-user.md`, `docs/architecture/state-user.md`

### 3. Issue案の作成 (Issue Drafting)

**目的:** 定義された戦略に基づき、具体的なIssue案ファイルを作成する。

- **Action:**
  - `activate_skill{name: "issue-drafting"}`
  - Step 2 で定義した各タスクについて、Issue案を作成する。
  - **Mandatory:** 全てのIssue案本文に、Step 1で作成した **Common Definitions Doc へのリンク** を記載し、「この定義に従うこと」と明記するよう、`issue-drafting` 実行時に指示する。

### 4. 計画レビュー (Planning Review)

**目的:** 作成された計画（共通定義 + Issue案）の品質を保証する。

- **Action:**
  - `activate_skill{name: "arch-planning-review"}`
  - 作成された共通定義書とIssue案をレビューする。
  - 抜け漏れ（MECE）、リンク切れ、定義の曖昧さがないかチェックし、問題があればその場で修正する。
  - **Correction:** 修正が必要な場合は、直ちにファイル (`docs/architecture/plans/*.md`, `reqs/tasks/drafts/*.md`) を更新する。

## アウトプット (Output)

`arch-creation` がコミットすべきアーティファクト一式。

1.  **Common Definitions Doc:** `docs/architecture/plans/{date}-{name}.md`
2.  **Draft Issues:** `reqs/tasks/drafts/*.md`
3.  **Review Report:** (Console Output or Comment)
