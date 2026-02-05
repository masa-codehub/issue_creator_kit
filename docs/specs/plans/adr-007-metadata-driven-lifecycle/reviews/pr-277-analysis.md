# Review Analysis Report: PR #277

## 1. 概要 (Overview)
- **分析日:** 2026-02-05
- **対象PR:** #277 (Spec Planning)
- **分析者:** Review Analyst

## 2. 指摘の分類と対応方針 (Categorization & Actions)

### 2.1. 命名規則・タスク不整合 (Accept)
| ファイル | 指摘内容 | 対応方針 |
| :--- | :--- | :--- |
| `definitions.md` | タスクファイル名規則が実態と不一致 | 定義を `id-desc.md` 形式に修正。 |
| `goal-definition.md` | ファイル名と内容の不整合 | 最新の並列化計画に合わせて修正。 |
| `007-T3-04-spec-cli.md` | ブランチ名が古い (`03`) | `spec/task-007-T3-04-cli` に修正。 |

### 2.2. SSOT (ADR-007) との不整合 (Accept)
| ファイル | 指摘内容 | 対応方針 |
| :--- | :--- | :--- |
| `adr-007.md` | `Issued` ステータス未定義 | ADR-007 を更新して `Issued` を追加。 |
| `adr-007.md` | `date` フィールド未定義 | ADR-007 を更新して `date` を追加。全ドラフトにも追加。 |

### 2.3. L2 Issue / ロードマップ (Accept/Discuss)
| ファイル | 指摘内容 | 対応方針 |
| :--- | :--- | :--- |
| `007-T3-L2` | `depends_on` が空 | 全L3タスク (`01`, `02`, `03`, `04`) を依存に追加。 |
| `007-T3-L2` | `issue_id` 手動入力禁止 | 事後リンクのため例外的に許容するが、注釈を追記する。 |
| `007-T3-L2` | `roadmap` パス無効 | 無効なパスを削除。 |

### 2.4. レポートの時系列 (Explain)
| ファイル | 指摘内容 | 対応方針 |
| :--- | :--- | :--- |
| `reconnaissance-report` | ADRステータスの矛盾 | 「調査時点の記録である」旨の注釈を追記。 |

## 3. 実行アクション (Execution Plan)
1.  **SSOT Update:** `adr-007-metadata-driven-lifecycle.md` に `Issued` ステータスと `date` フィールド定義を追加。
2.  **Definitions Update:** `definitions.md` のファイル名規則を修正。
3.  **Drafts Update:**
    - L2 (`007-T3-L2`): `depends_on`, `roadmap` 修正、`issue_id` 注釈追加。
    - L3 (`007-T3-04`): ブランチ名修正。
    - All Drafts: `date` フィールド追加。
4.  **Reports Update:** 過去レポートに注釈追記。

## 4. 資産化 (Assetization)
- **教訓:** タスク番号を変更する際は、grep等で全ファイルの参照を一括チェックする必要がある。
- **教訓:** L2 Issueのような「事後作成」パターンの扱い（issue_idの手動入力）を運用ルールとして定義する必要がある。
