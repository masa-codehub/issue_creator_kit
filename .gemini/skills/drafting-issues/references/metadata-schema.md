# メタデータ定義スキーマ (Metadata Schema)

本プロジェクトの設計（ADR）およびタスク（Issue Draft）で必須となる YAML Frontmatter の仕様を定義します。

## 1. 共通設計思想
- **IDの一意性:** タスクIDは `[ADR-ID]-T[通し番号]` (例: `007-T1`) とし、プロジェクト全体での衝突を回避する。
- **依存管理の単純化:** フェーズプレフィックスを排除し、ADR内での通し番号を使用することで、`depends_on` の記述を簡素化する。
- **ハイブリッドSSOT:** ファイルはバックエンド（予約券・控え）、GitHub Issue はフロントエンド（作業・議論の場）として役割を分離する。

## 2. ADR / Design Doc スキーマ
`reqs/design/` 配下のドキュメントで使用します。

| フィールド | 必須 | 説明 | 例 |
| :--- | :---: | :--- | :--- |
| `id` | ◯ | ADRの一意な識別子 | `adr-007` |
| `status` | ◯ | `Draft`, `Approved`, `Postponed`, `Superseded` | `Approved` |
| `date` | ◯ | 最終更新日 (YYYY-MM-DD) | `2026-02-04` |
| `issue_id` | × | 自動起票された親Issue番号 | `123` |

## 3. Task (Issue Draft) スキーマ
`reqs/tasks/<ADR-ID>/` 配下のタスクファイルで使用します。

| フィールド | 必須 | 説明 | 例 |
| :--- | :---: | :--- | :--- |
| `id` | ◯ | `[ADR番号]-T[連番]` 形式の不変ID | `007-T1` |
| `parent` | ◯ | 紐づくADRのID | `adr-007` |
| `type` | ◯ | `task` (L3実装) または `integration` (L2統合) | `task` |
| `title` | ◯ | GitHub Issue のタイトル | `[Auth] Implement JWT` |
| `status` | ◯ | `Draft`, `Ready`, `Completed`, `Cancelled` | `Draft` |
| `phase` | ◯ | 実施フェーズ (`domain` | `infrastructure` | `usecase` | `interface` | `architecture` | `spec` | `tdd`) | `usecase` |
| `roadmap` | ◯ | 関連する計画書（ロードマップ）のファイルパス | `docs/architecture/plans/20260204-adr007-refresh-plan.md` |
| `depends_on` | ◯ | 依存するタスクIDのリスト。依存なしは `[]` | `["007-T0"]` |
| `issue_id` | × | 【自動追記】手動で設定しないでください | `456` |
