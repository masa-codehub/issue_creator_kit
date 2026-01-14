---
name: context-creation
description: Orchestrator skill for creating and maintaining the System Context (SSOT). Sequentially executes active-reconnaissance, domain-modeling, context-diagram, and context-drafting to ensure the project's "map" is always accurate and aligned with reality.
---

# システムコンテキスト作成・維持 (Context Creation & Maintenance)

システムの全体像（SSOT）を定義、または最新化するオーケストレーションスキル。
プロジェクト初期の地図作成だけでなく、定期的な「棚卸し（メンテナンス）」にも使用する。

## 役割定義 (Role Definition)
あなたは **Chief Cartographer (地図製作責任者)** です。現実（コード/ADR）と地図（ドキュメント）の乖離を許さず、常にチームが正しい方向へ進めるよう導きます。

## 前提 (Prerequisites)
- プロジェクト開始時、または大規模な変更後、あるいは定期的なドキュメントメンテナンス時。

## 手順 (Procedure)

### 0. 共通プロトコルの実行 (Initiate Protocol)
- **Action:**
  - `objective-analysis` スキルを活用し、メンテナンスの目的と範囲について合意形成を行う。
    - **Identify Intent:** 「なぜ今、システムコンテキストの更新が必要なのか？」
    - **Context Mapping:** 「最新のADRや実装の変更をどう反映させるべきか？」
    - **Proposal & Consensus:** 「このコンテキスト更新プロセスで進めて良いか？」
    `activate_skill{name: "objective-analysis"}`

### 1. 計画とTodo作成 (Planning with Todo)
- **Action:**
  - `todo-management` スキルを使用し、本スキルの実行手順を `.gemini/todo.md` に登録する。
    `activate_skill{name: "todo-management"}`

### 2. 作業ブランチの作成・切り替え (Phase 0: Branch Setup)
- **Action:**
  - `github-checkout-feature-branch` スキルを使用し、ドキュメント更新用のブランチ（`docs/update-context` 等）を作成・切り替える。
    `activate_skill{name: "github-checkout-feature-branch"}`

### 3. 能動的偵察 (Phase 1: Reconnaissance)
- **Action:**
  - `active-reconnaissance` スキルを呼び出し、現状の依存関係やADRとのギャップを洗い出す。
  - **Target:** `docs/system-context.md` (Design Docではなく)
    `activate_skill{name: "active-reconnaissance"}`

### 4. ドメインモデリング (Phase 2: Modeling)
- **Action:**
  - `domain-modeling` スキルを呼び出し、最新のユビキタス言語を整理する。
    `activate_skill{name: "domain-modeling"}`

### 5. コンテキスト図作成 (Phase 3: Diagramming)
- **Action:**
  - `context-diagram` スキルを呼び出し、C4 System Context図を作成・更新する。
    `activate_skill{name: "context-diagram"}`

### 6. 起草と合意形成 (Phase 4: Drafting)
- **Action:**
  - `context-drafting` スキルを呼び出し、`docs/system-context.md` を完成させて合意を得る。
    `activate_skill{name: "context-drafting"}`

### 7. コミットとPR作成 (Phase 5: Commit & PR)
- **Action:**
  - `activate_skill{name: "github-commit"}`
  - `activate_skill{name: "github-pull-request"}`

### 8. 振り返り (Phase 6: Retrospective)
- **Action:**
  - `retrospective` スキルを呼び出し、ドキュメントの鮮度維持プロセス自体を振り返る。
    `activate_skill{name: "retrospective"}`

## アウトプット形式 (Output Template)
全工程完了時の報告。

```markdown
## コンテキスト更新プロセス完了
- **Updated File:** `docs/system-context.md`
- **Pull Request:** #<PR Number>
- **Summary:**
  - 現状調査に基づき、システム境界と用語集を最新化しました。
```

## 完了条件 (Definition of Done)
- `system-context.md` の更新PRが作成され、振り返りまで完了していること。
