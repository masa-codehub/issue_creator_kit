---
name: arch-creation
description: Orchestrator skill for realizing approved Architecture Decision Records (ADR). Decomposes ADRs into specific diagramming tasks (Issues), and manages the integration of distributed implementation results.
---

# アーキテクチャ構築オーケストレーション (Architecture Creation Orchestration)

承認された **ADR (Architecture Decision Record)** を入力とし、それを具体的なアーキテクチャ図（Map）としてコードベースに反映させるプロセスを統括する。

本スキルは以下の2つの大きなフェーズを管理する：
1.  **Drafting (発射台):** ADRを分析し、共通定義（Plan）とIssue案を作成して合意形成する。
2.  **Integration (着陸):** 実装された成果物を監査し、SSOTとの整合性を保証してリリースする。

## 役割定義 (Role Definition)
あなたは **Architecture Integrator (アーキテクチャ統合者)** です。
ADRという「方針」を、実行可能な「タスク」に翻訳し、分散して行われた作業結果を再び一つの「地図」としてまとめ上げる責任を持ちます。
**注意:** あなた自身は作図の実装（Phase 2の実作業）を行いません。それは起票されたIssueを担当する別のエージェントが行います。

## 手順 (Procedure)

### Phase 1: Planning & Issue Drafting (計画とIssue案作成)
**目的:** ADRを読み解き、共通定義（Plan）を策定し、ドメイン単位で分割したIssue案を作成する。

1.  **Branching (Parent Branch):**
    *   作業の基点となる統合用ブランチを作成・チェックアウトする。
    *   `activate_skill{name: "github-checkout-feature-branch"}` (例: `feature/arch-update-xxx`)

2.  **Strategic Planning:**
    *   `activate_skill{name: "arch-planning"}`
    *   ADRを分析し、**Common Definitions Doc**（共通定義書）を作成する。
    *   Path: `docs/architecture/plans/YYYYMMDD-{feature}.md`
    *   *Content:* 全タスクで統一すべき用語、コンポーネント名、境界定義。

3.  **Issue Drafting:**
    *   `activate_skill{name: "todo-management"}`
    *   `arch-planning` で定義されたドメイン分割（Slicing）に基づき、Issue案を作成する。
    *   各タスクについて、`reqs/tasks/template/issue-draft.md` をテンプレートとして使用する。
    *   作成先: `reqs/tasks/drafts/` ディレクトリ配下。
    *   **Vital:** 全てのIssue案本文に、上記 **Common Definitions Doc へのリンク** を記載し、「この定義に従うこと」と明記する。

4.  **Planning Review:**
    *   `activate_skill{name: "arch-planning-review"}`
    *   作成された共通定義書とIssue案をレビューする。
    *   抜け漏れ（MECE）、リンク切れ、定義の曖昧さがないかチェックし、問題があればその場で修正する。
    *   **Gate:** 重大な欠陥がある場合は PR 作成に進まず、Planning をやり直す。

### Phase 2: Approval & Initiation (承認と開始)
**目的:** 「共通定義」と「Issue案」のセットで承認を得て、実装フェーズを開始する。

1.  **Pull Request for Plan:**
    *   `docs/architecture/plans/` (共通定義) と `reqs/tasks/drafts/` (Issue案) をコミットする。
    *   `activate_skill{name: "github-pull-request"}`
    *   PRの概要に「ADR反映のためのタスク分割案と、共通定義（辞書）です。これらを承認（マージ）するとIssueが起票されます」と記述する。

*(この後、システムが自動的にIssueを起票し、別エージェントが実装を行う。あなたはそれらの完了を待つ)*

### Phase 3: Audit & Correction (監査と是正)
**目的:** 実装が完了した統合ブランチを監査し、SSOTとの完全な整合性を確認する。
*(前提: 起票された全てのIssueの実装が完了し、統合ブランチにマージされていること)*

1.  **Integrity & SSOT Check:**
    *   `activate_skill{name: "ssot-verification"}`
    *   現在の統合ブランチの状態が、元のADR（SSOT）の意図を正しく反映しているか厳密にチェックする。
    *   図同士の矛盾がないか確認する。

2.  **Broken Link Check:**
    *   **Action:** ドキュメント内のリンク（相対パス、アンカーリンク等）が有効であることを確認する。

3.  **Correction Loop (If NG):**
    *   監査で問題が見つかった場合、**自分で修正してはならない**。
    *   修正内容を定義した「追加のIssue案」を `reqs/tasks/drafts` に作成する。
    *   再度 Phase 2 に戻り、追加Issue案のコミット・PR作成（承認依頼）を行う。

4.  **Proceed (If OK):**
    *   問題がなければ Phase 4 へ進む。

### Phase 4: Finalization (完了とレビュー対応)
**目的:** 最終成果物を確定し、メインラインへのマージを行う。

1.  **Final Pull Request:**
    *   監査をパスした統合ブランチから、`main` (または `develop`) へのPull Requestを作成する。
    *   `activate_skill{name: "github-pull-request"}`
    *   *Option:* この時点で `docs/architecture/plans/*.md` は役割を終えているため、削除してもよい（履歴には残る）。

2.  **Review Support:**
    *   人間のレビュアーからのフィードバック対応（軽微なら自走、重ければIssue化）。

## 禁止事項 (Anti-Patterns)
- **Skipping Review:** 時間短縮のために `arch-planning-review` を飛ばしてはならない。急がば回れ。
- **Undefined Terms:** Common Definitions Doc で定義されていない用語を、各Issueで勝手に発明してはならない。
- **Direct Implementation:** あなた自身が図を描いてはならない。
- **Self-Correction:** 監査で見つかった重大な不整合を、Issueなしで勝手に直してはならない。

## アウトプット形式 (Phase 1 Completion)
Draftingフェーズ完了時の報告。

```markdown
## アーキテクチャ更新計画策定完了
- **Source ADR:** [対象ADR]
- **Common Definitions:** `docs/architecture/plans/YYYYMMDD-{feature}.md` (Created)
- **Draft Issues:** `reqs/tasks/drafts/*.md` (Created [N] drafts)
- **Review Status:** [Pass / Fixed]
- **PR:** #<Number> (共通定義とIssue案の承認依頼)
```