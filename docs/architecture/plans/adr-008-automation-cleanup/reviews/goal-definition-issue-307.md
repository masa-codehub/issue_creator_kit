# 目標定義書 (Goal Definition)

## 1. 核心的目標 (Core Intent / SMART Goal)

- **ゴール:** `docs/architecture/arch-structure-007-metadata.md` を更新し、ADR-008 で定義された ID 形式や依存関係の制約（Domain Guardrails）を仕様として追記する。また、これらの制約が `src/issue_creator_kit/domain/models` で実装される旨をマッピングする。
- **採用した仮説:** 案A (実証的仮説) + 案B (Mermaidでの依存関係図解)
- **期待される価値:** システムの健全性を保つためのバリデーションルールが SSOT として明文化され、Scanner 等の自動化ツールの実装根拠が明確になる。

## 2. 実行の前提条件 (Achievable / Prerequisites)

- **対象ファイル:** `docs/architecture/arch-structure-007-metadata.md`
- **必要な情報:** `docs/architecture/plans/adr-008-automation-cleanup/definitions.md` に記載された制約ルール。
- **依存タスク:** なし（既存ファイルの更新のみ）。

## 3. アクションプラン (Specific / Time-boxed)

1. **[ブランチ作成]:** `feature/task-008-03-metadata` ブランチを作成し、切り替える。
2. **[ドキュメント更新]:** `docs/architecture/arch-structure-007-metadata.md` に以下の内容を追記する。
   - 「Metadata Field Definitions & Guardrails」セクション。
   - `id`, `depends_on`, `status`, `issue_id` の各フィールドに対する Regex や論理制約の表。
   - `depends_on` の循環参照禁止を説明する Mermaid 図。
   - 実装が `src/issue_creator_kit/domain/models` にマッピングされる旨の注記。
3. **[検証]:** `grep` 等を用いて追記内容が正しく反映されているか、Mermaid 記法に誤りがないかを確認する。

## 4. 完了定義 (Measurable / Definition of Done)

### A. 自動検証 (Automated)

- **検証コマンド:**
  ```bash
  grep -q "Metadata Field Definitions & Guardrails" docs/architecture/arch-structure-007-metadata.md &&
  grep -q "adr-\d{3}-.*" docs/architecture/arch-structure-007-metadata.md &&
  grep -q "src/issue_creator_kit/domain/models" docs/architecture/arch-structure-007-metadata.md
  ```
- **合格基準:** すべての `grep` が成功（終了コード 0）すること。

### B. 状態検証 (State Check)

- **確認対象:** `docs/architecture/arch-structure-007-metadata.md` の末尾付近。
- **合格基準:** `Metadata Field Definitions & Guardrails` という見出しと、その下にバリデーションルールの表が存在すること。

## 5. 制約と安全策 (Constraints & Safety)

- **負の制約:** 既存の C4 図面や Element Definitions セクションを破壊しない。
- **安全策:** 編集前にファイルの全体内容を読み込み、慎重に `replace` または追記を行う。

## 6. SMART 自己評価

- **Specific:** 更新対象ファイル、追記内容、マッピング先が具体的に特定されている。
- **Measurable:** `grep` コマンドでキーワードの存在を確認できる。
- **Achievable:** 必要な制約ルールは `definitions.md` から収集済み。
- **Relevant:** Issue #307 の要求を直接的に解決する。
- **Time-boxed:** ドキュメントの追記作業であり、1ターンで完遂可能。
