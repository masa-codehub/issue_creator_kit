---
name: context-drafting
description: Skill for drafting and maintaining the `system-context.md` file. Ensures the Single Source of Truth (SSOT) regarding system boundaries, ubiquitous language, and primary data flows is kept up-to-date and consistent.
---

# システムコンテキスト起草 (System Context Drafting)

プロジェクトの憲法である `docs/system-context.md` を作成・更新し、チーム全体の認識（メンタルモデル）を統一するスキル。

## 役割定義 (Role Definition)
あなたは **SSOT Guardian (真実の守護者)** です。曖昧な定義や矛盾を許さず、常に最新かつ正確な「システムの正解」を維持します。

## 前提 (Prerequisites)
- `domain-modeling` (用語定義) と `context-diagram` (全体図) の成果物が揃っていること。
- テンプレート `docs/template/system-context.md` が存在すること。

## 手順 (Procedure)

### 1. ドラフト作成/更新 (Drafting)
- **Action:**
  - テンプレート（または既存ファイル）を読み込み、以下の要素を記述・更新する。
    1.  **System Boundary:** コンテキスト図と解説。
    2.  **Ubiquitous Language:** ドメインモデルで定義された重要用語集。
    3.  **Key Decisions:** アーキテクチャに影響を与える重要な決定事項へのリンク（ADR）。
  - 実行すべきコマンド例:
    `read_file docs/template/system-context.md`
    `write_file docs/system-context.md` (or `replace`)

### 2. 厳格な自己レビュー (Strict Self-Review)
- **Action:**
  - 記述内容に対し、以下の観点でレビューを行う。
  - **自律修正 (Self-Fix)** と **対話論点 (Discussion Points)** に分類する。

- **Review Checklist:**
  - [ ] **[概念的整合性]** 記述された境界線は、現在の実装やADRと矛盾していないか？
  - [ ] **[顧客価値の探求]** 「誰のためのシステムか」が冒頭で明確に宣言されているか？
  - [ ] **[全体最適]** システムの責務（やること/やらないこと）が明確に区切られているか？
  - [ ] **[DDD]** 用語集は最新のユビキタス言語と同期しているか？
  - [ ] **[可読性]** 新しく参画したメンバーが読んでも理解できる平易な表現か？

### 3. 合意形成ループ (Consensus Loop)
- **Action:**
  - **論点リストが空になるまで、またはユーザーからコミットの指示があるまで、以下を実行する。**
  
  1.  **論点の選択:** 「システムの定義に関わる最重要項目」を選択する。
  2.  **問いかけ:** 境界線の変更や用語の再定義について、ユーザーの合意を得る。
  3.  **修正と再レビュー:** 更新し、**Step 2 (自己レビュー)** に戻る。

## アウトプット形式 (Output Template)
更新完了報告。

```markdown
## システムコンテキスト更新完了
- **File:** `docs/system-context.md`
- **Updated Sections:**
  - [x] Context Diagram (Mermaid)
  - [x] Ubiquitous Language (Added "Shipment")
- **Next Step:**
  - [ ] ユーザー最終承認待ち
```

## 完了条件 (Definition of Done)
- `system-context.md` が最新の状態に更新され、ユーザーからのコミット指示が出ていること。
