---
name: design-doc-creation
description: Orchestrator skill for creating Detailed Design Documents. Sequentially executes active-reconnaissance, domain-modeling, technical-design, reliability-design, and design-doc-drafting to build a solid implementation blueprint.
---

# Design Doc作成オーケストレーション (Design Doc Creation)

Design Doc作成の一連のプロセス（偵察 -> モデリング -> 詳細設計 -> 信頼性設計 -> 起草・合意）を統括・実行するスキル。
`SYSTEM_ARCHITECT.md` の共通プロトコルに準拠し、実装フェーズの手戻りを防ぐための詳細な青写真を作成する。

## 役割定義 (Role Definition)
あなたは **Lead Architect (リードアーキテクト)** です。ビジネス要求を、開発者が迷いなく実装可能な「技術仕様」へと変換する全責任を持ちます。

## 前提 (Prerequisites)
- 具体的な機能追加や変更の要求があり、ADR（方向性の決定）が完了している、または自明であること。

## 手順 (Procedure)

### 0. 共通プロトコルの実行 (Initiate Protocol)
- **Action:**
  - ユーザーの意図（Why）と、今回Design Docを作成する範囲（Scope）について合意する。

### 1. 作業ブランチの作成・切り替え (Phase 0: Branch Setup)
- **Action:**
  - `github-checkout-feature-branch` スキルを使用し、Design Doc作成用のフィーチャーブランチを作成・切り替える。
  - `activate_skill github-checkout-feature-branch`

### 2. 能動的偵察 (Phase 1: Reconnaissance)
- **Action:**
  - `active-reconnaissance` スキルを呼び出し、現状把握とギャップ分析を行う。
  - **Note:** Design Doc用のテンプレートを使用するよう指示すること。
  - `activate_skill active-reconnaissance`

### 3. ドメインモデリング (Phase 2: Modeling)
- **Action:**
  - `domain-modeling` スキルを呼び出し、ユビキタス言語と集約を定義する。
  - `activate_skill domain-modeling`

### 4. 詳細設計 (Phase 3: Technical Specs)
- **Action:**
  - `technical-design` スキルを呼び出し、ER図、API、シーケンス図を設計する。
  - `activate_skill technical-design`

### 5. 信頼性設計 (Phase 4: Reliability)
- **Action:**
  - `reliability-design` スキルを呼び出し、非機能要件（エラー処理、リトライ等）を定義する。
  - `activate_skill reliability-design`

### 6. 起草と合意形成 (Phase 5: Drafting)
- **Action:**
  - `design-doc-drafting` スキルを呼び出し、ドキュメントを完成させて合意を得る。
  - `activate_skill design-doc-drafting`

### 7. コミットとPR作成 (Phase 6: Commit & PR)
- **Action:**
  - `activate_skill github-commit`
  - `activate_skill github-pull-request`

### 8. 振り返り (Phase 7: Retrospective)
- **Action:**
  - `retrospective` スキルを呼び出し、詳細設計プロセスの質を振り返る。
  - **振り返りの観点:**
    - **網羅性:** 異常系やデータ整合性の懸念を、コーディング前に全て洗い出せたか？
    - **伝達性:** 図面や仕様の記述は、初見の実装者が理解できるほど明確だったか？
    - **フロントローディング:** 実装フェーズで手戻りになりそうな論点を、この段階で解消できたか？
  - `activate_skill retrospective`

## アウトプット形式 (Output Template)
全工程完了時の報告。

```markdown
## Design Doc作成プロセス完了
- **Created Doc:** `reqs/design/_inbox/design-XXX-title.md`
- **Pull Request:** #<PR Number>
- **Summary:**
  - 詳細設計、信頼性設計を経て、上記Design Docを作成・合意し、PRを提出しました。
```

## 完了条件 (Definition of Done)
- Design DocのPRが作成され、振り返りまで完了していること。
