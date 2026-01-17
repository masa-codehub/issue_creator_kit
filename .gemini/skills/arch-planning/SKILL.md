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
特に、**後続の「Spec Strategist（仕様戦略家）」が、仕様策定計画を立てるために必要な「境界」と「方針」を明確にすること**を重視する。

## 前提 (Prerequisites)

- 入力となる承認済みADR（SSOT）が存在すること。

## 手順 (Procedure)

### 1. 目標設定 (Objective Setting)

**目的:** 今回のPlanning活動のゴールと成功基準を明確にする。

- **Action:**
  - `activate_skill{name: "objective-setting"}`
  - 今回のADR反映作業において、「誰に」「何を」伝えることが最も重要か（Value）を定義し、それを満たすためのSMART目標を設定する。
  - _Goal:_ 「**Spec Strategist (仕様戦略家)** が、迷わず仕様書（Specs）の分割・計画を行えるレベルのIssue案と共通定義を作成し、レビューをパスする。」

### 2. 意図の抽出と共通定義 (Intent & Common Definitions)

**目的:** 全タスクで統一すべき「用語」や「境界」を先に定義し、コンフリクトの芽を摘む。
**重要:** タスクが細分化されるため、この共通定義書が唯一の頼みの綱となる。一切の曖昧さを排除せよ。

- **Action:**
  - `activate_skill{name: "active-reconnaissance"}` でADRと現状を分析。
  - **Common Definitions Doc** (`docs/architecture/plans/YYYYMMDD-{feature}-plan.md`) を作成し、以下を定義する。
    - **Ubiquitous Language:** 今回の変更で導入/変更される用語の定義。
    - **Boundaries (Critical):** コンポーネント間の境界線。どのロジックがどのコンテナ/クラスに属するかをSpec Strategistに伝える。
    - **Tech Decisions:** 全体で統一すべき技術選定（例: 「全APIはgRPCとする」）。
    - **Directory Structure:** 成果物ファイルの配置場所と命名規則。

### 3. 図構成とタスク分割 (Portfolio & Slicing)

**目的:** レビューしやすく、並列作業可能な単位でタスクを分割する。

- **Action:**
  - **Slicing Strategy:** **Atomic Slice (1 Issue = 1 Diagram File)** を原則とする。
    - _原則:_ 1つのアーキテクチャ図ファイルにつき、1つのIssueを発行する。
    - _例外:_ 密結合、微修正の場合はまとめることを許容する。

  - **Output Definition:** 次のステップのために、以下の構成案を確定する。
    1.  **Draft Issue List:** 作成するIssue案のタイトルとファイル名（例: `arch-update-payment.md`）。
    2.  **Target Scope:** 各Issueで作成/更新する具体的な図ファイル名と、その記述範囲（Boundary）。

    **Example:**
    - Issue: `[Payment Domain] Update Architecture Diagrams`
      - Files: `context.md`, `container.md`, `seq-payment.md`
      - Scope: 決済コンテナの内部構造と、API/Redisとの境界を記述。Spec StrategistがAPI仕様を計画するための入力となる。

### 4. Issue案の作成 (Issue Drafting)

**目的:** 定義された戦略に基づき、具体的なIssue案ファイルを作成する。

- **Action:**
  - `activate_skill{name: "issue-drafting"}`
  - Step 3 で定義した各タスクについて、Issue案を作成する。
  - **Mandatory:** 全てのIssue案本文に以下を含めるよう指示する：
    1.  Step 2で作成した **Common Definitions Doc へのリンク**。
    2.  **成果物のターゲット:** 「このアーキテクチャ図の主な読者は **Spec Strategist (仕様戦略家)** であり、彼らが詳細仕様の計画を立てるのに十分な情報（境界、責務、データの流れ）を提供すること」という旨の指示。

### 5. 計画レビュー (Planning Review)

**目的:** 作成された計画（共通定義 + Issue案）の品質を保証する。

- **Action:**
  - `activate_skill{name: "arch-planning-review"}`
  - 作成された共通定義書とIssue案をレビューする。
  - **Resulting Value Check:** 「このIssue案の通りに成果物が作成された場合、Spec Strategistは迷わず仕様書の計画を立てられるか？」という視点でチェックする。
  - **Correction:** 修正が必要な場合は、直ちにファイル (`docs/architecture/plans/*.md`, `reqs/tasks/drafts/*.md`) を更新する。

## アウトプット (Output)

`arch-creation` がコミットすべきアーティファクト一式。

1.  **Common Definitions Doc:** `docs/architecture/plans/{date}-{name}.md`
2.  **Draft Issues:** `reqs/tasks/drafts/*.md`
3.  **Review Report:** (Console Output or Comment)
