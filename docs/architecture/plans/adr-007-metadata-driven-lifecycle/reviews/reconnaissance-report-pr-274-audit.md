# Reconnaissance Report: ADR-007 Architecture Audit

## 1. 目的 (Objective)
ADR-007「メタデータ駆動型ライフサイクル管理」のアーキテクチャ設計フェーズにおける成果物の現状を把握し、監査（Audit）の準備を整える。

## 2. 調査対象 (Scope)
- **SSOT:** `reqs/design/_approved/adr-007-metadata-driven-lifecycle.md`
- **成果物:** 
    - `docs/architecture/arch-state-007-lifecycle.md`
    - `docs/architecture/arch-structure-007-metadata.md`
- **計画/履歴:**
    - `docs/architecture/plans/adr-007-metadata-driven-lifecycle/`
    - `reqs/tasks/_archive/issue-007-T*.md`

## 3. 収集された事実 (Gathered Facts)

### 3.1 ADR-007 の定義 (SSOT)
- **ID:** `adr-007`
- **Status:** `Approved` (物理配置は `_approved/` だが、ファイル内記述は `提案中` となっている)
- **核心的決定:** YAML Frontmatter によるライフサイクル管理、ディレクトリのフラット化、L1/L2/L3の3層Issue構造。

### 3.2 アーキテクチャ設計の現状
- **State Diagram (`arch-state-007-lifecycle.md`):**
    - ADR と Task の状態遷移図。
    - PR #274 での指摘（`Archived_ADR` の分割、副作用の note 化）が反映済み。
- **Structure Diagram (`arch-structure-007-metadata.md`):**
    - C4 Container 図と「Invisible SSOT」のマッピング図。
    - `ick CLI` のレイヤー名が `Interface Adapters` に修正済み。

### 3.3 タスクの進捗
- `issue-007-T1` (Fact Scouting), `issue-007-T2` (Arch Drafting) は `_archive/` へ移動済み。
- ユーザーの申告通り、統合Issue（L2）の物理ファイルや起票記録は見当たらない。

### 3.4 レビューの証跡
- `pr-274-analysis.md` にて 12 件の指摘と対応方針が記録されており、現状のドキュメントに反映されていることが確認された。

## 4. 特記事項 (Findings)
- **統合Issueの欠如:** ADR-007 の運用ルールでは「L2: 統合 Issue」がフェーズの完了責任を持つことになっているが、これが未作成のままタスクが完了している。
- **ドキュメント内ステータスの不整合:** `adr-007` ファイル内の `Status` 記述が `提案中` のまま更新されていない可能性がある。
