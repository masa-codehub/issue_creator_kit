---
name: drafting-issues
description: Generates objective-oriented and verifiable Issue drafts based on templates. Ensures strict alignment with SMART goals, metadata consistency, and verifiable implementation steps.
---

# Issue Drafting (Objective-Oriented & Verifiable)

このスキルは、`assets/issue-draft-template.md` をベースに、エージェントが自律的に実行可能な「完全な指示書」を作成します。

## ワークフロー (Workflow)

以下のチェックリストに従って、高品質なIssueドラフトを作成し、保存してください。

```markdown
ドラフト作成進捗:
- [ ] 1. 個別目標の定義 (SMART Goal)
- [ ] 2. メタデータ定義 (Frontmatter)
- [ ] 3. 目的と背景の記述 (Why & What)
- [ ] 4. 参照資料の特定 (Input Context)
- [ ] 5. 手順と制約の記述 (How & Constraints)
- [ ] 6. ブランチと検証基準の定義 (Branch & Verify)
- [ ] 7. ファイル保存 (Save to Drafts)
- [ ] 8. 品質レビュー (Final Quality Gate)
```

### 1. 個別目標の定義 (SMART目標設定 (Setting SMART Goals))

**目的:** このタスク（Issue）単体で達成すべき成果を明確化する。

- **Action:**
  - 依頼内容から、**このIssueが達成すべきSMART目標**を定義する。
  - 完了を判定するための客観的な検証基準（DoD）を定める。

### 2. メタデータ定義 (Frontmatter)



**目的:** システム連携に必要な属性情報を定義する。



- **id:** Planning段階で振られた一意なID（例: `T-1`）。

- **parent:** 紐づくADRの一意なID（例: `adr-007`）。

- **type:** タスクの種別（`task` | `integration`）。

- **title:** `[Domain] Action + Object` (例: `[Auth] Implementation of JWT Token Issuance`)

- **status:** 初期値は `Draft`。

- **phase:** 実施フェーズ（`domain` | `infrastructure` | `usecase` | `interface` | `architecture` | `spec` | `tdd`）。

- **roadmap:** 参照すべき **刷新計画書（ロードマップ）のパス** (例: `docs/architecture/plans/20260204-adr007-refresh-plan.md`)。

- **depends_on:** 依存するタスクの **ID** リスト（例: `["T-0"]`）。なければ空配列 `[]`。

- **issue_id:** 【自動追記】手動で設定しないでください。

### 3. 目的と背景 (1. Goal & Context)

**目的:** タスクの「Why」と「What」を定義する。

- **Goal:** Step 1で定義したSMART目標。
- **As-is (現状):** 現状のドキュメントやコードにおける具体的な「不足」や「誤り」。
- **To-be (あるべき姿):** このタスク完了後に実現されているべき状態。
- **Design Evidence:** 根拠となる ADR 番号、および設計ドキュメントへのリンク。

### 4. 参照資料・入力ファイル (2. Input Context)

**目的:** 作業開始時に必要な情報を過不足なく渡す。

- 編集対象となるファイルパス、参照すべきコードや仕様書を明記する。
- 存在しないパスや無関係な資料は除外する。

### 5. 実装手順と制約 (3. Implementation Steps & Constraints)

**目的:** 迷いのない「実行手順（How）」を定義する。

- **負の制約 (Negative Constraints):** 「編集してはいけないファイル」や「使用禁止の記法」を明示する。詳細は `references/negative-constraints.md` を参照。
- **実装手順 (Changes):**
  - 作成・編集するファイルパス。
  - 使用するテンプレート (`assets/` 配下のテンプレート等)。
  - ステップバイステップの具体的な指示。
- **構成変更 (Configuration):** ファイルの削除・移動がある場合のみ記述。

### 6. ブランチ戦略と検証手順 (Sections 4 & 5)

**目的:** 作業場所の固定と、目標達成の証明方法。

- **Branching Strategy:** 開発の起点と作業場所を定義する。詳細は `references/branching-strategy.md` を参照。
  - **Base Branch:** 統合先となるブランチ。
  - **Feature Branch:** 作業用ブランチ。命名規則 `<type>/task-{{task_id}}-{{subject}}` に従う。
- **Verification & DoD:**
  - **観測される挙動:** ファイルの存在、内容の非空確認。
  - **ファイル状態:** 構文エラーがないこと。
  - **整合性:** 定義された用語が正確に使われていること。

### 7. ドラフトの保存 (Save Draft)

**目的:** 作成した内容を物理ファイルとして確定させる。

- **Action:**
  - 作成したドラフトを必ず標準出力に表示する。
  - **保存:**
    - ユーザーから保存先パスが指定されている場合は、そのパスに保存する。
    - 指定がない場合は、`reqs/tasks/drafts/issue-{{task_id}}.md` に保存する（**必須**）。

### 8. 品質レビュー (Final Quality Gate)

保存されたファイルを監査し、品質を保証する。

- **Action:**
  - `assets/review-report-template.md` を使用してレビュー結果を生成する。
  - **レポート出力:**
    - レビュー結果を必ず標準出力に表示する。
    - ユーザーからレポートの保存先が指定されている場合のみ、ファイルにも保存する。
  - **是正:**
    - レビューで「Request Changes」となった場合は、Step 7 で保存したファイルを修正し、再度レビューを行う。