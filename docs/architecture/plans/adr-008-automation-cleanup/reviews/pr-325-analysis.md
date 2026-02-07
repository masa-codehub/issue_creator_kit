# Review Analysis Report: PR #325

## 1. Fact Gathering (指摘とコンテキストの収集)

### レビュアーからの指摘事項

1. **[docs/specs/api/cli_commands.md]** `--adr-id` の型バリデーションエラー時の終了コードが仕様（`1`）と実装（`2`）で不一致。
2. **[docs/specs/api/cli_commands.md]** UseCase のメソッド名および引数名が仕様（`create_issues_from_virtual_queue`）と実装（`create_issues`）で不一致。
3. **[docs/specs/api/cli_commands.md]** GitHub トークンの環境変数名が仕様（`GITHUB_MCP_PAT`）と実装（`GITHUB_TOKEN`/`GH_TOKEN`）で不一致。
4. **[docs/specs/plans/.../self-review.md]** タイポ「制約의 明示」の指摘。
5. **[src/issue_creator_kit/cli.py]** (Suppressed) CLIオプション `--roadmap`, `--use-pr`, `--base-branch` が UseCase へ渡されていない。

### 関連 SSOT

- **ADR-008**: レガシー自動化の削除とスキャナー基盤の再構築。
- **cli_commands.md**: CLI 仕様の SSOT。
- **cli.py / creation.py**: 現行実装。

---

## 2. Categorization & Analysis (分類と真因分析)

| ID  | 指摘内容         | 分類       | 真因                                                             | 対応方針                        |
| :-- | :--------------- | :--------- | :--------------------------------------------------------------- | :------------------------------ |
| 1   | 終了コード不一致 | **Accept** | `argparse` のデフォルト挙動（2）を仕様側が考慮していなかった。   | 仕様を `2` に更新。             |
| 2   | メソッド名不一致 | **Accept** | 実装時にメソッド名を簡略化した際、仕様書への反映が漏れた。       | 仕様を実装に合わせる。          |
| 3   | 環境変数名不一致 | **Accept** | 旧プロジェクトの名残（`GITHUB_MCP_PAT`）が仕様書に残存していた。 | 仕様を `GITHUB_TOKEN` に更新。  |
| 4   | タイポ           | **Accept** | 言語混在（韓国語の助詞 `의` が混入）。                           | 修正。                          |
| 5   | 引数渡し漏れ     | **Accept** | CLIへの引数追加とUseCaseへの統合が不完全だった。                 | `cli.py` を修正して引数を渡す。 |

---

## 3. Retrospective for Assetization (資産化に向けた振り返り)

### 真因の抽象化

- **仕様と実装の乖離**: 高速なリファクタリング（ADR-008）の過程で、コード側の変更が先行し、ドキュメント（Spec）の同期が後手に回った。
- **外部ライブラリ挙動の未確認**: `argparse` 等の標準的なエラー挙動を、仕様定義段階で明示的に規定・確認できていなかった。

### 再発防止策（仕組み化）

- **Spec-Implementation 同期チェック**: PR作成前の自己チェックリストに「CLI仕様（引数、環境変数、終了コード）と実装の完全一致」を明文化する。
- **GitHub Actions 環境変数の統一**: プロジェクト全体で `GITHUB_TOKEN` または `GH_TOKEN` を標準とすることを `coding-guidelines.md` に明記する。

---

## 4. Final Report & Feedback (分析結果と対応方針の提示)

全ての指摘を受け入れ、仕様書および実装の修正を行います。特に、CLIからUseCaseへの引数渡し漏れは機能欠落に繋がるため、最優先で修正します。

### 改善アクション案

1. `docs/specs/api/cli_commands.md` の終了コード、メソッド名、環境変数名を修正。
2. `src/issue_creator_kit/cli.py` の `run_automation` を修正し、全ての引数を UseCase に渡す。
3. `docs/specs/plans/adr-008-automation-cleanup/self-review.md` のタイポ修正。
