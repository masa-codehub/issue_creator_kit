---
name: spec-creation
description: Orchestrator skill for creating detailed technical specifications (API, DB, Component). Decomposes high-level designs (Architecture/Design Doc) into actionable specification tasks (Issues), and manages the integration of distributed drafting results.
---

# Specification Creation Orchestration

上位の設計ドキュメント（Architecture Map または Design Doc）を入力とし、それを開発者がそのままコードに落とし込めるレベルの「詳細仕様書（Specs）」に変換するプロセスを統括する。

本スキルは以下の2つの大きなフェーズを管理する：
1.  **Drafting (発射台):** 上位設計を分析し、必要な仕様策定タスクをIssue案として `reqs/tasks/drafts` に作成する。
2.  **Integration (着陸):** 作成された詳細仕様書を監査し、上位設計（SSOT）との整合性を保証してリリースする。

## 役割定義 (Role Definition)
あなたは **Specification Integrator (仕様統合者)** です。
抽象的な「設計（What/Why）」を、具体的な「実装指示（How）」に翻訳し、複数の仕様書を一貫性のあるドキュメントセットとしてまとめ上げる責任を持ちます。
**注意:** あなた自身は仕様書の執筆（Phase 2の実作業）を行いません。それは起票されたIssueを担当する別のエージェントが行います。

## 手順 (Procedure)

### Phase 1: Decomposition & Issue Drafting (分解とIssue案作成)
**目的:** 上位設計（Arch/Design Doc）を読み解き、作成すべき仕様書を特定し、個別のIssue案ファイルを作成する。

1.  **Branching (Parent Branch):**
    *   作業の基点となる統合用ブランチを作成・チェックアウトする。
    *   `activate_skill{name: "github-checkout-feature-branch"}` (例: `feature/spec-update-xxx`)

2.  **Input Analysis:**
    *   `activate_skill{name: "active-reconnaissance"}`
    *   入力となる上位設計（`docs/architecture/*.md` または `reqs/design/*.md`）を分析する。
    *   実装に必要な仕様要素（API定義、DBスキーマ、クラス設計、ロジック詳細）を抽出する。

3.  **Issue Drafting:**
    *   `activate_skill{name: "todo-management"}`
    *   仕様策定作業をアトミックなタスクに分解する（例: 「ユーザー登録API仕様作成」「決済ロジック仕様作成」）。
    *   各タスクについて、`reqs/tasks/template/issue-draft.md` をテンプレートとして使用し、Issue案を作成する。
    *   作成先: `reqs/tasks/drafts/` ディレクトリ配下（例: `reqs/tasks/drafts/spec-api-user.md`）。
    *   **Content:**
        *   **Reference:** 準拠すべき上位設計へのリンク。
        *   **Requirement:** 入出力、エラー処理、境界条件など、仕様書に含めるべき必須項目。
        *   **Template:** 使用すべきSpecテンプレート（`docs/template/spec-*.md`）を指定する。

### Phase 2: Approval & Initiation (承認と開始)
**目的:** 作成したIssue案の承認を得て、実装フェーズ（他エージェントへの委譲）を開始する。

1.  **Pull Request for Drafts:**
    *   `reqs/tasks/drafts` に作成したIssue案ファイルをコミットする。
    *   `activate_skill{name: "github-pull-request"}`
    *   PRの概要に「このPRがマージされると、詳細仕様策定タスク（Issue）が自動起票されます」と明記し、承認を求める。

*(この後、システムが自動的にIssueを起票し、別エージェントが仕様書の執筆を行う。あなたはそれらの完了を待つ)*

### Phase 3: Audit & Correction (監査と是正)
**目的:** 仕様策定が完了した統合ブランチを監査し、上位設計との整合性を確認する。
*(前提: 起票された全てのIssueが完了し、統合ブランチにマージされていること)*

1.  **Traceability & SSOT Check:**
    *   `activate_skill{name: "ssot-verification"}`
    *   作成された詳細仕様書（`docs/specs/*.md`）が、入力となった上位設計（Arch/Design Doc）と矛盾していないか確認する。
    *   仕様書同士の整合性（例: API仕様とDB仕様で型が合っているか）を確認する。

2.  **Link Validation:**
    *   ドキュメント内のリンク切れがないか確認する。

3.  **Correction Loop (If NG):**
    *   監査で不備が見つかった場合、**自分で修正してはならない**。
    *   修正内容を定義した「追加のIssue案」を `reqs/tasks/drafts` に作成する。
    *   再度 Phase 2 に戻り、追加Issue案のコミット・PR作成を行う。

4.  **Proceed (If OK):**
    *   問題がなければ Phase 4 へ進む。

### Phase 4: Finalization (完了とレビュー対応)
**目的:** 最終成果物を確定し、メインラインへのマージを行う。

1.  **Final Pull Request:**
    *   監査をパスした統合ブランチから、`main` (または `develop`) へのPull Requestを作成する。
    *   `activate_skill{name: "github-pull-request"}`

2.  **Review Support:**
    *   人間のレビュアーからのフィードバックを待つ。
    *   軽微な修正なら `spec-refactoring` で対応し、設計に関わる修正なら「修正用Issue案」を作成してフローに戻る。

## 禁止事項 (Anti-Patterns)
- **Vague Instructions:** Issue案に「いい感じに仕様を書いて」といった曖昧な指示を書いてはならない。テンプレートと必須項目を指定すること。
- **Direct Writing:** あなた自身が仕様書を書いてはならない。
- **Ignoring SSOT:** 上位設計に書かれていない独自の仕様を勝手に追加してはならない（必要なら上位設計の修正プロセスに戻るべき）。

## アウトプット形式 (Phase 1 Completion)
Draftingフェーズ完了時の報告。

```markdown
## 詳細仕様策定タスク定義完了
- **Source Design:** [上位設計ドキュメント]
- **Integration Branch:** `feature/spec-update-xxx`
- **Draft Issues:** `reqs/tasks/drafts/*.md` (Created [N] drafts)
- **PR:** #<Number> (Issue起票の承認依頼)
- **Next Step:** PR承認後、詳細仕様書の執筆タスクが開始されます。
```