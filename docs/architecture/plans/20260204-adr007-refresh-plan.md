# 目標定義書 (Goal Definition)

## 1. 核心的目標 (Core Intent / SMART Goal)
ADR-007 の新思想に基づき、旧来の自動化ワークフローを無効化し、アーキテクチャ設計図の刷新（Structure/State）を開始する。

- **採用した仮説:** 分析レポートの「仮説B（トリガーの無効化）」および「Full Cycle プロトコルに基づくアーキテクチャ刷新」。
- **期待される価値:** 移行期間中の誤作動防止と、新構造に即した「正しいシステムの地図」の再構築。

## 2. 実行の前提条件 (Achievable / Prerequisites)
- **対象ファイル:**
    - `.github/workflows/auto-approve-docs.yml`
    - `.github/workflows/auto-create-issues.yml`
    - `.github/workflows/auto-phase-promotion.yml`
    - `docs/architecture/arch-structure-003-vqueue.md`
    - `docs/architecture/arch-state-003-task-lifecycle.md`
- **必要な情報:** ADR-007 の決定事項。

## 3. アクションプラン (Specific / Time-boxed)

1. **[無効化]:** 3つのワークフローファイルの `on:` トリガーをコメントアウトし、`# DISABLED for ADR-007 migration` を追記する。

2. **[設計刷新 - Structure]:** `docs/architecture/arch-structure-007-metadata.md` を新規作成し、フラットな配置とメタデータによる依存管理構造を定義する。

3. **[設計刷新 - State]:** `docs/architecture/arch-state-007-lifecycle.md` を新規作成し、ADR-007 の新ステータス遷移（Draft/Approved/Archived）を定義する。

4. **[クリーンアップ]:** 旧ドキュメント (`*-003-*`) の冒頭に以下の警告文言を追記し、削除準備を行う。

   > **DEPRECATED: This document is based on ADR-003 and has been superseded by the new architecture defined in ADR-007.** Please refer to the new architecture documents, such as `arch-structure-007-metadata.md` and `arch-state-007-lifecycle.md`.



## 4. 完了定義 (Measurable / Definition of Done)

### A. 自動検証 (Automated)

- **検証コマンド:**

    ```bash

    grep -E '^[[:space:]]*#+[[:space:]]*on:' .github/workflows/auto-*.yml

    ls docs/architecture/arch-*-007-*.md

    ```

- **合格基準:** 全対象ファイルのトリガーがコメントアウトされ、新設計 図が2ファイル存在すること。

### B. 状態検証 (State Check)
- **確認対象:** `docs/architecture/`
- **合格基準:** ADR-007 に即した「フラット構造」と「3層ハイブリッド管理」が Mermaid 図等で正しく表現されていること。

## 5. 制約と安全策 (Constraints & Safety)
- **安全策:** ワークフローは削除せず、コメントアウトに留めることで元のロジックを参照可能にする。

