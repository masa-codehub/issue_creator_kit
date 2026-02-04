---
name: drafting-specs
description: Replaces the actual work of drafting and updating detailed specifications that can be used directly as input for TDD. Merges drafting, TDD criteria verification, and quality refactoring.
---

# Specification Drafting

計画フェーズ(`planning-specs`)で作成された個別Issueに基づき、詳細仕様書（Spec）を作成・更新する実装スキル。
**記述（Drafting）**、**TDD適合性検証**、および**リファクタリング**を一気通貫で行い、実装者がそのままテストコードを書ける仕様書を作成する。

## 役割定義 (Role Definition)

あなたは **Technical Specification Writer** です。
「たぶんこういうことだろう」という推測を許さず、厳密な契約（Contract）とロジックを定義します。
あなたの成果物は、TDDにおける「テストコードの設計図」となります。

## ワークフロー (Workflow)

```markdown
Drafting Progress:
- [ ] 1. Goal Setting (目標設定)
- [ ] 2. Preparation (ブランチ作成)
- [ ] 3. Template Selection & Preparation (テンプレート選択と準備)
- [ ] 4. Detailed Drafting (詳細記述)
- [ ] 5. Refactoring & Ambiguity Check (リファクタリングと曖昧さ排除)
- [ ] 6. Self-Audit (自己監査)
- [ ] 7. Retrospective (振り返り)
- [ ] 8. Pull Request Submission (PR作成)
```

### 1. Goal Setting (目標設定)
- **Action:**
  - `activate_skill{name: "defining-work-goals"}` を実行する。
  - 現状の調査、意図の分析を経て、この仕様策定タスクのSMARTゴールを策定する。

### 2. Preparation (ブランチ作成)
- **Action:**
  - `activate_skill{name: "switching-feature-branch"}` を実行し、作業用のFeature Branchを作成・切り替えを行う。

### 3. Template Selection & Preparation (テンプレート選択と準備)
- **Action:**
  - 以下のテンプレートから適切なものを選択する。
    - **API Spec:** `.gemini/skills/drafting-specs/assets/spec-api.md`
    - **Data Spec:** `.gemini/skills/drafting-specs/assets/spec-data.md`
    - **Logic Spec:** `.gemini/skills/drafting-specs/assets/spec-logic.md`
  - 対象ドキュメント（`docs/specs/*.md`）を作成または開き、テンプレートを適用する。

### 4. Detailed Drafting (詳細記述)
- **Action:**
  - `planning-specs` で策定された **Common Definitions** を参照し、それに従う。
  - **Strict Typing:** 言語の曖昧な型ではなく、具体的制約（例: `integer (min 0, max 100)`）まで記述する。
  - **Error Handling:** 発生しうるエラーケースとコードを網羅的にリストアップする。
  - **Verify Criteria:** Issueに記載された検証条件（Happy/Error/Boundary）を仕様書内に反映させる。

### 5. Refactoring & Ambiguity Check (リファクタリングと曖昧さ排除)
- **Action:**
  - **Forbidden Terms:** "TBD", "Pending", "Any" などの曖昧語を検索し、排除する。
  - **Formatting:** Markdownのテーブル崩れやインデントを修正する。
  - **Link Fix:** リンク切れを修正する。

### 6. Self-Audit (自己監査)
- **Action:**
  - `read_file .gemini/skills/drafting-specs/assets/drafting-audit-template.md` を実行してテンプレートを確認する。
  - 作成した仕様書を監査し、日本語でレポートを作成する。
  - **重要:** 「TDD適合性（そのままテストが書けるか）」を最重要視し、各チェック項目に具体的な「根拠」を記述すること。
- **Output:**
  - 監査レポートを標準出力に表示する（保存先指定があればファイル出力）。

### 7. Retrospective (振り返り)
**目的:** 仕様策定プロセスの成果と課題を振り返り、より厳密で効率的な仕様記述のための知見を蓄積する。

- **Action:**
  - `activate_skill{name: "conducting-retrospectives"}` を実行する。
  - 仕様の曖昧さ、TDD適合性、ドメイン定義の正確性などを軸に振り返り、改善アクションを策定する。

### 8. Pull Request Submission (PR作成)
**目的:** 仕様書をレビューに回し、統合ブランチへ反映させる。

- **Action:**
  - `activate_skill{name: "managing-pull-requests"}` を実行する。
  - 仕様の主要なポイントと、検証基準（Verify Criteria）の網羅性をPRの記述で強調する。

## 完了条件 (Definition of Done)

- 仕様書から曖昧な表現が排除されていること。
- Common Definitions に準拠していること。
- 自己監査レポートが作成され、すべてのチェックをパスしていること。
- 振り返り（Retrospective）が実施され、レポートが標準出力に表示されていること。
- **プルリクエスト（PR）が作成され、成果物が提出されていること。**
