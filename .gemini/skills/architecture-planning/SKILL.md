---
name: architecture-planning
description: Formulates a plan to update architecture diagrams based on SSOT (ADR/Specs). Defines the "To-Be" state of the diagrams to match the approved design.
---

# Architecture Planning (SSOT-based Gap Analysis)

SSOT（ADR/Design Doc）に基づいて、アーキテクチャ図をどのように更新すべきか（To-Be）を定義するスキル。
「コードにあるから描く」のではなく、「設計として決定されたから描く」という原則を貫く。

## 役割 (Role)
**Architecture Planner (設計計画者)**
承認された設計情報（ADR）を図解要件に変換する。現状の図（As-Is）とあるべき姿（To-Be）のギャップを特定する。

## 前提 (Prerequisites)
- `active-reconnaissance` (SSOT取得用), `todo-management` が利用可能であること。
- 変更の根拠となる SSOT (ADR, Design Doc, Issue) が存在すること。

## 手順 (Procedure)

### 1. To-Beの特定 (Extract To-Be from SSOT)
- **Action:**
  - `activate_skill{name: "active-reconnaissance"}` を使い、今回の作業の根拠となるドキュメント（ADR, Spec）を読み込む。
  - 以下の要素を抽出する（これが描くべき正解となる）。
    - **Boundaries:** 新しいサブシステムや境界。
    - **Containers:** 新規/変更されるプロセス（API, Worker, DB等）。
    - **Components:** 主要な論理要素（Service, Repository等）とその責務。
    - **Relations:** 要素間の依存方向と通信方式（Sync/Async）。

### 2. As-Isの確認 (Check Current Diagram)
- **Action:**
  - 現在の `docs/architecture/*.md` を確認する（ファイルが存在しない場合は「空」とみなす）。
  - SSOTで定義された要素が、現状の図に既に存在するか確認する。

### 3. Gap分析とUML選定 (Gap Analysis & UML Selection)
- **Action:**
  - SSOTの全要件を表現するために最適なUML図を選定し、既存図とのGapを定義する。
  - **UML Selection Criteria (MECE):** SSOTの要件特性に合わせて、最適な図を選択する。
    *   **Caution:** 以下の全ての図を作る必要はない。**「その要件を説明するために不可欠か？」「メンテナンスコストに見合う価値があるか？」** を常に問い、無理・無駄・ムラのない選定を行うこと。
    - **全体像・境界 (Structure):** `C4 System Context` / `C4 Container` (必須)
    - **詳細構造 (Structure):** `C4 Component` / `Class Diagram` (クラス間の静的な依存関係が重要な場合)
    - **振る舞い・通信 (Behavior):** `Sequence Diagram` (時系列、非同期フロー、APIコールの順序が重要な場合)
    - **状態変化 (State):** `State Diagram` (ライフサイクルやステータス遷移が複雑なドメインオブジェクトがある場合)
    - **データ構造 (Data):** `ER Diagram` (永続化データのスキーマやリレーション定義が必要な場合)
  - **補足情報の記述:** 図だけでは表現しきれない「例外的な処理」「異常系」「複雑なビジネスルールの詳細」については、具体的な文章を用いて詳細かつ厳密に記述する計画を立てる。
  - **Plan Formulation:** 選定した各図について、追加・修正・削除すべき内容をリストアップする。

### 4. Todo分解 (Breakdown)
- **Action:**
  - `activate_skill{name: "todo-management"}` を使用し、計画を原子的なタスクに分解して `.gemini/todo.md` を作成する。
  - **Task Name:** 「[UML名] SSOTのXXに基づき、YYを追加する」という形式にする。
  - **Context (Red) の記述ルール:**
    - 「○○が存在しない」というネガティブな事実ではなく、**「SSOTによれば、本来どうあるべきか（To-Be）」**というポジティブな要件として記述する。
    - *Bad:* 「PaymentWorkerが図にない。」
    - *Good:* 「ADR-005に基づき、決済はWorkerプロセスで非同期に処理される構成でなければならない。」

## アウトプット形式 (.gemini/todo.md)

```markdown
# Goal: [Objective-settingで定義したアーキテクチャ更新目標]

## Tasks
- [ ] **Step 1: [C4 Container] SSOT(ADR-005)に基づき、PaymentWorkerコンテナを追加する**
  - **Context (Red):** ADR-005「決済処理は、APIからの要求をキューに積み、独立したWorkerプロセスで非同期実行する」という構成が図面に反映されている必要がある。
  - **Action (Green):** `arch-drafting` を使用し、`docs/architecture/container.md` にコンテナ定義とMermaidノードを追加する。
  - **Refine (Refactor):** `arch-refactoring` を使用し、Queueとの関係が見やすいようにレイアウトを調整する。
  - **Verify:** `PaymentWorker` ノードが存在し、API -> Redis -> Worker の依存関係で描画されていること。

- [ ] **Step 2: [Sequence Diagram] SSOT(ADR-005)に基づき、非同期決済フローを新規作成する**
  - **Context (Red):** 「APIが受付けレスポンスを返した後、Redisを介してWorkerが決済処理を開始する」という時系列の振る舞いが厳密に定義されている必要がある。
  - **Action (Green):** `arch-drafting` (Template: arch-behavior) を使用し、`docs/architecture/seq-payment-async.md` を作成する。
  - **Refine (Refactor):** `arch-refactoring` を使用し、例外フローのNoteを整理する。
  - **Verify:** ファイルが作成され、メッセージフローがSSOTの時系列要件と一致していること。

- [ ] **Final Step: 全ての更新図面とSSOTの整合性を確認する**
  - Action: `ssot-verification` スキルを実行し、ドキュメントのリンクチェックを行う。
  - Verify: SSOTとの整合性に問題がないこと。
```