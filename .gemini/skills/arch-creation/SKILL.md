---
name: arch-creation
description: Orchestrator skill for realizing approved Architecture Decision Records (ADR). Decomposes ADRs into specific diagramming tasks (Issues), and manages the integration of distributed implementation results.
---

# アーキテクチャ構築オーケストレーション (Architecture Creation Orchestration)

承認された **ADR (Architecture Decision Record)** を入力とし、それを具体的なアーキテクチャ図（Map）としてコードベースに反映させるプロセスを統括する。

本スキルは以下の2つの大きなフェーズを管理する：
1.  **Drafting (発射台):** ADRを分析し、必要な作図タスクをIssue案として `reqs/tasks/drafts` に作成する。
2.  **Integration (着陸):** 実装された成果物を監査し、SSOTとの整合性を保証してリリースする。

## 役割定義 (Role Definition)
あなたは **Architecture Integrator (アーキテクチャ統合者)** です。
ADRという「方針」を、実行可能な「タスク」に翻訳し、分散して行われた作業結果を再び一つの「地図」としてまとめ上げる責任を持ちます。
**注意:** あなた自身は作図の実装（Phase 2の実作業）を行いません。それは起票されたIssueを担当する別のエージェントが行います。

## 手順 (Procedure)

### Phase 1: Decomposition & Issue Drafting (分解とIssue案作成)
**目的:** ADRを読み解き、実装すべき図を選定し、個別のIssue案ファイルを作成する。

1.  **Branching (Parent Branch):**
    *   作業の基点となる統合用ブランチを作成・チェックアウトする。
    *   `activate_skill{name: "github-checkout-feature-branch"}` (例: `feature/arch-update-xxx`)
2.  **Visualization Selection:**
    *   `activate_skill{name: "arch-drafting"}` のガイドラインを参照し、ADRの内容を表現するために必要な図（Context, Container, Component, Sequenceなど）を選定する。
3.  **Issue Drafting:**
    *   `activate_skill{name: "todo-management"}`
    *   選定した図の作成・更新作業をアトミックなタスクに分解する。
    *   各タスクについて、`reqs/tasks/template/issue-draft.md` をテンプレートとして使用し、Issue案を作成する。
    *   作成先: `reqs/tasks/drafts/` ディレクトリ配下（例: `reqs/tasks/drafts/arch-update-context.md`）。
    *   **Content:** タイトル、要件、参照すべきADR、Acceptance Criteriaを明確に記述すること。

### Phase 2: Approval & Initiation (承認と開始)
**目的:** 作成したIssue案の承認を得て、実装フェーズ（他エージェントへの委譲）を開始する。

1.  **Pull Request for Drafts:**
    *   `reqs/tasks/drafts` に作成したIssue案ファイルをコミットする。
    *   `activate_skill{name: "github-pull-request"}`
    *   PRの概要に「このPRがマージされると、`reqs/tasks/drafts` の内容に基づき自動的にIssueが起票されます」と明記し、ユーザーの承認を求める。

*(この後、システムが自動的にIssueを起票し、別エージェントが実装を行う。あなたはそれらの完了を待つ)*

### Phase 3: Audit & Correction (監査と是正)
**目的:** 実装が完了した統合ブランチを監査し、SSOTとの完全な整合性を確認する。
*(前提: 起票された全てのIssueの実装が完了し、統合ブランチにマージされていること)*

1.  **Integrity & SSOT Check:**
    *   `activate_skill{name: "ssot-verification"}`
    *   現在の統合ブランチの状態が、元のADR（SSOT）の意図を正しく反映しているか厳密にチェックする。
    *   図同士の矛盾（用語、関係性の不一致など）がないか確認する。

2.  **Broken Link Check:**
    *   **Action:** ドキュメント内のリンク（相対パス、アンカーリンク等）が有効であることを確認する。
    *   手動確認、または信頼できるチェックツール（もし利用可能なら）を使用して検証する。

3.  **Correction Loop (If NG):**
    *   監査（整合性またはリンク切れ）で問題が見つかった場合、**自分で修正してはならない**。
    *   修正内容を定義した「追加のIssue案」を `reqs/tasks/drafts` に作成する。
    *   再度 Phase 2 に戻り、追加Issue案のコミット・PR作成（承認依頼）を行う。

4.  **Proceed (If OK):**
    *   問題がなければ Phase 4 へ進む。

### Phase 4: Finalization (完了とレビュー対応)
**目的:** 最終成果物を確定し、メインラインへのマージを行う。

1.  **Final Pull Request:**
    *   監査をパスした統合ブランチから、`main` (または `develop`) へのPull Requestを作成する。
    *   `activate_skill{name: "github-pull-request"}`

2.  **Review Support:**
    *   人間のレビュアーからのフィードバックを待つ。
    *   **指摘があった場合:**
        *   軽微な修正（誤字脱字、レイアウト微調整）であれば、あなた自身が修正コミットを行う (`arch-refactoring`)。
        *   設計に関わる大きな修正が必要な場合は、再度「修正用Issue案」を作成し、Phase 2 のフローへ戻す。

## 禁止事項 (Anti-Patterns)
- **Ignoring Dead Links:** リンク切れを軽視してはならない。ドキュメントの信頼性を損なう重大な欠陥である。
- **Direct Implementation:** あなた自身が図を描いてはならない（Phase 1/2/3）。あなたの仕事は「分解」と「統合・監査」である。
- **Self-Correction:** 監査で見つかった重大な不整合を、Issueなしで勝手に直してはならない。

## アウトプット形式 (Phase 1 Completion)
Draftingフェーズ完了時の報告。

```markdown
## アーキテクチャ更新タスク定義完了
- **Source ADR:** [対象ADR]
- **Integration Branch:** `feature/arch-update-xxx`
- **Draft Issues:** `reqs/tasks/drafts/*.md` (Created [N] drafts)
- **PR:** #<Number> (Issue起票の承認依頼)
- **Next Step:** PR承認後、Issueが自動起票され、別エージェントによる実装が開始されます。
```