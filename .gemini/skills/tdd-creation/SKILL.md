---
name: tdd-creation
description: Orchestrator skill for implementing features based on detailed specifications (Specs). Decomposes specs into TDD tasks (Issues) with a shared plan, and manages the integration of implemented code and tests.
---

# TDD Implementation Orchestration

詳細仕様書（Specs）を入力とし、それをテスト駆動開発（TDD）によって「動作するコード（UseCase/Logic）」と「検証コード（Tests）」に変換するプロセスを統括する。

本スキルは以下の2つの大きなフェーズを管理する：

1.  **Planning & Drafting (発射台):** 仕様を分析し、**共通実装計画（Common Implementation Plan）** と **Issue案（Draft Issues）** を作成して合意形成する。
2.  **Integration (着陸):** 実装されたプロダクトコードとテストを監査し、仕様（SSOT）との整合性を保証してリリースする。

## 役割定義 (Role Definition)

あなたは **Implementation Integrator (実装統合者)** です。
詳細な「仕様（How）」を、具体的な「実装タスク」に翻訳し、分散して行われた実装結果（コードとテスト）を一貫性のあるシステムとしてまとめ上げる責任を持ちます。
**注意:** あなた自身は実装（Phase 2の実作業）を行いません。それは起票されたIssueを担当する別のエージェントが行います。

## 手順 (Procedure)

### Phase 1: Planning & Issue Drafting (計画とIssue案作成)

**目的:** 仕様書と引継ぎ事項を読み解き、実装のための「共通計画」と「Issue案」を作成し、レビューまで完了させる。

1.  **Branching (Parent Branch):**
    - 作業の基点となる統合用ブランチを作成・チェックアウトする。
    - `activate_skill{name: "github-checkout-feature-branch"}` (例: `feature/impl-xxx`)

2.  **Strategic Planning & Drafting:**
    - `activate_skill{name: "tdd-planning"}`
    - このスキルを使用し、以下の2つを作成する：
      1.  **Common Implementation Plan (共通実装計画):** 複数タスク間で統一すべき実装方針、モック定義、配置場所を定義した計画ドキュメント（`docs/implementation/plans/YYYYMMDD-{feature}.md`）。
      2.  **Draft Issues (Issue案):** TDD単位に分割されたタスク定義書（`reqs/tasks/drafts/*.md`）。
    - **Verify:** `tdd-planning-review` を使用し、計画とIssue案が仕様書と整合しているか確認する。

### Phase 2: Approval & Initiation (承認と開始)

**目的:** 「共通計画」と「Issue案」のセットで承認を得て、実装フェーズ（他エージェントへの委譲）を開始する。

1.  **Pull Request for Plan:**
    - `docs/implementation/plans/` (共通計画) と `reqs/tasks/drafts/` (Issue案) をコミットする。
    - `activate_skill{name: "github-pull-request"}`
    - PRの概要に「仕様反映のための実装計画（共通方針）とタスク分割案です。これらを承認（マージ）すると、TDDによる実装タスク（Issue）が自動起票されます」と明記し、承認を求める。

_(この後、システムが自動的にIssueを起票し、別エージェントが `tdd-implementation` スキルを用いて実装を行う。あなたはそれらの完了を待つ)_

### Phase 3: Audit & Correction (監査と是正)

**目的:** 実装が完了した統合ブランチを監査し、仕様および実装計画との整合性を確認する。
_(前提: 起票された全てのIssueが完了し、統合ブランチにマージされていること)_

1.  **Traceability & Quality Check:**
    - `activate_skill{name: "ssot-verification"}`
    - 作成されたプロダクトコード（UseCase/Logic）とテストが、以下の2点と整合しているか厳密にチェックする。
      1.  **詳細仕様 (Specs):** 全ての要件、エラーハンドリング、バリデーションが実装されているか。
      2.  **共通実装計画 (Common Implementation Plan):** 定義された方針、レイヤー構造に従っているか。
    - **Verification Action:** `run_shell_command` でプロジェクトのテストコマンドを実行し、全テストがGreenであることを物理的に確認する。

2.  **Create Handover Items (Next Step):**
    - 次工程（通常はインフラ接続やUI統合、あるいは完了報告）に向けた引継ぎ事項を作成する。
    - `docs/handovers/tdd-to-final.md`

3.  **Correction Loop (If NG):**
    - 監査で不備が見つかった場合、以下のどちらかの対応を行う。
    - **重要:** いかなる場合も、**あなた自身が上流ドキュメント（Specs/Arch）やプロダクトコードを直接修正してはならない。** 必ずIssue案を作成し、別の作業サイクルとして実行させること。
      - **Case A (Local Fix):** 実装コードやテストの誤り。修正内容を定義した「追加のIssue案」を作成する。
      - **Case B (Upstream Fix):** 詳細仕様書（Specs）や設計に致命的な欠陥が見つかった場合。
        - **Action:** 「仕様/設計修正用のIssue案」を作成する（例: `fix-spec-xxx.md`）。
        - **Content:** テストで判明した仕様の矛盾点、実装不可能な要件、代替案を明記する。
    - 再度 Phase 2 に戻り、追加Issue案のコミット・PR作成を行う。

4.  **Proceed (If OK):**
    - 問題がなければ Phase 4 へ進む。

### Phase 4: Finalization (完了とレビュー対応)

**目的:** 最終成果物を確定し、メインラインへのマージを行う。

1.  **Final Pull Request:**
    - 監査をパスした統合ブランチから、`main` (または `develop`) へのPull Requestを作成する。
    - `activate_skill{name: "github-pull-request"}`

2.  **Retrospective:**
    - `activate_skill{name: "retrospective"}`
    - 今回の実装計画の精度や、仕様書との乖離について振り返りを行う。

## 禁止事項 (Anti-Patterns)

- **Undefined Patterns:** 共通実装計画で定義されていない独自のライブラリやパターンを、各Issueで勝手に導入してはならない。
- **Direct Coding:** あなた自身がプロダクトコードやテストを書いてはならない。
- **Skipping Tests:** テストコードのない実装を承認してはならない。

## アウトプット形式 (Phase 1 Completion)

Draftingフェーズ完了時の報告。

```markdown
## 実装タスク定義完了 (TDD-based)

- **Source Specs:** [詳細仕様書]
- **Common Implementation Plan:** `docs/implementation/plans/YYYYMMDD-{feature}.md` (Created)
- **Draft Issues:** `reqs/tasks/drafts/*.md` (Created [N] drafts)
- **PR:** #<Number> (共通計画とIssue案の承認依頼)
- **Next Step:** PR承認後、TDDによる実装（UseCase/Logic）タスクが開始されます。
```
