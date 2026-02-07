# Review Analysis Report: PR #330

## 1. Fact Gathering (指摘とコンテキストの収集)
- **対象 PR:** #330 (CLI Integration with Scanner Foundation)
- **レビュアー:** Copilot, gemini-code-assist[bot]
- **主な指摘事項:**
  - `reconnaissance-report.md`, `analysis-report.md` における現状（As-Is）の記述が、実際のコードベース（`cli.py` 等）と乖離している。
  - `cli-integration.md` における `archived_ids` の取得元が不明確。
  - `ick process` の `--dry-run` オプションの仕様（必須かデフォルトか）が曖昧。
  - レガシーコマンドの Cleanup 方針が曖昧。
  - タイポ（プロセルフロー）。

## 2. Categorization & Analysis (分類と真因分析)

| ID | 指摘内容 | 分類 | 真因 |
| :--- | :--- | :--- | :--- |
| 1 | `archived_ids` の取得元不明 | **Accept** | 仕様定義（Spec）における入出力の定義不足。 |
| 2 | 偵察/分析レポートの事実誤認 | **Accept** | コードベースの物理的な確認（`ls`, `read_file`）を行わず、推測や旧仕様に基づき起草したことによる。 |
| 3 | `domain/services/` 未作成の指摘 | **Accept** | 計画（Planned）と実装済み（Implemented）の混同。 |
| 4 | レガシーコマンド cleanup 方針の曖昧さ | **Accept** | 移行期における挙動の決定（仕様の確定）を避けたことによる。 |
| 5 | `--dry-run` 仕様の曖昧さ | **Accept** | ユーザーの利便性と安全性のトレードオフの検討不足。 |

## 3. Retrospective for Assetization (資産化に向けた振り返り)

### YWT (やったこと・わかったこと・つぎやること)
- **やったこと:** ADR-008 CLI統合仕様の策定とドキュメント化。
- **わかったこと:**
  - 偵察（Reconnaissance）段階での「事実の裏取り」が不足すると、後続の分析や仕様が砂上の楼閣になる。
  - `cli.py` の現状は、以前のドキュメントで示唆されていたよりもシンプル（コマンドが少ない）であった。
- **つぎやること:**
  - 偵察スキル実行時は、必ず `ls -R`, `grep`, `read_file` を並行して使い、物理的な証拠をレポートに明記する「エビデンス・ファースト」を徹底する。
  - 仕様書作成時は、データフロー（シーケンス図）と本文の不整合をセルフチェックする。

## 4. Final Report & Feedback (分析結果と対応方針)

### 対応方針案
1. **仕様の明確化 (`cli-integration.md`):**
   - `FileSystemScanner.scan` が `(documents, archived_ids)` を返すように定義を修正する。
   - `ick process` の `--dry-run` は、Task-008-05 のスコープにおいては **必須（指定がない場合はエラーまたは警告を表示して終了）** とする。安全性を最優先する。
   - レガシーコマンドは、Copilot の提案通り「Deprecated（警告＋エラー終了）」と「Remove（完全削除）」に明確に分ける。
2. **事実の修正 (`reconnaissance-report.md`, `analysis-report.md`):**
   - 現状の `cli.py` に存在するコマンド（`init`, `process-diff`）のみを事実として記載する。
   - `domain/services/` が未作成であることを明記する。
3. **タイポ修正:**
   - 「プロセルフロー」→「プロセスフロー」

### 次のアクション
- [ ] `docs/specs/components/cli-integration.md` の修正。
- [ ] `docs/specs/plans/adr-008-automation-cleanup/reconnaissance-report.md` の修正。
- [ ] `docs/specs/plans/adr-008-automation-cleanup/analysis-report.md` の修正。
- [ ] 修正後のセルフ監査 (`auditing-ssot`)。
