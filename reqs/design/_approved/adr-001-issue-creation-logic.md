# 概要 / Summary
[ADR-001] タイトル: 依存関係解決型Issue起票のロジックとテスト戦略の採用

- **Status**: 提案中
- **Date**: 2025-12-27

## 状況 / Context
現在、設計ドキュメントから複数のタスク（Issue）を生成する際、タスク間の依存関係（例：タスクAが完了しないとタスクBに着手できない）を考慮して起票する標準的な仕組みが存在しない。
無秩序な起票は依存関係の不透明化を招き、開発者の着手順序の誤りやバックログの混乱を引き起こす。
また、GitHub Actions を用いた自動化において、実環境でのデバッグは「テスト用 Issue の乱立」や「API 制限の浪費」を招くため、ローカルで完結する高速なテスト戦略が不可欠である。

## 決定 / Decision
以下の方式を厳密に採用し、**Dependency First**（依存関係優先）かつ **Test-Driven**（テスト駆動）な開発を実現する。

### 1. 責務と技術的手段の完全対応表 (Strict Mapping)

| 担当 (Actor) | 技術的手段 (Technical Means) | 具体的な成果物・動作 |
| :--- | :--- | :--- |
| **AI Agent** | **静的依存定義** | `reqs/_issues/*.md` 作成時、メタデータ部に `- **Depends-On**: ./issue-A.md` 形式で相対パスを記述する。 |
| **issue-kit (src/)** | **依存関係解析** | Python の `graphlib.TopologicalSorter` を用い、`Depends-On` から有向非巡回グラフ (DAG) を構築・ソートする。 |
| **issue-kit (src/)** | **Fail-Fast 検証** | 起票開始前に GitHub API `GET /rate_limit` を確認し、起票予定数以上の残弾がない場合は、1件も起票せずに `sys.exit(1)` する。 |
| **issue-kit (src/)** | **循環参照の可視化** | `CycleError` 検知時、循環パス（例: `A -> B -> A`）をログに出力し、処理を停止する。 |
| **issue-kit (src/)** | **動的番号解決** | `POST /issues` 直後に取得した実 Issue 番号を保持し、後続 Issue の本文内にある「ファイル名」を `#123` 形式へ動的に置換する。 |
| **issue-kit (src/)** | **ライフサイクル管理** | 起票に成功した Markdown ファイルは、`os.rename` を用いて `reqs/_issues/created/` へ即座に移動（アーカイブ）する。 |
| **AI / Developer** | **単体テスト (pytest)** | `tests/` 内に `unittest.mock` で GitHub API 通信を擬似化したテストを「実装前」に作成し、ロジックを検証する。 |
| **GitHub Actions** | **統合テスト (act)** | ワークフロー変更時、`act` を用いてローカルの Docker 環境で Actions の完遂（終了コード 0）を確認する。 |

### 2. 詳細仕様規定
- **置換アルゴリズム**: 本文 (Body) 全体をスキャンし、依存グラフに含まれるファイル名（例: `issue-001.md`）と一致する文字列を、実 Issue 番号（例: `#101`）へ置換する。
- **認証**: `GH_TOKEN` 環境変数を使用し、`requests` の Header に `Authorization: token ...` を付与して通信する。
- **ディレクトリ制約**: `reqs/_issues/` 直下の `.md` ファイルのみを対象とし、サブディレクトリは走査しない。

## 検討した代替案 / Alternatives Considered
- **案B: 並列起票**: 依存関係を無視して起票する。管理コストが増大するため不採用。
- **案C: GitHub 上での直接テスト**: 開発サイクルが遅く、API 制限を浪費するため不採用。

## 結果 / Consequences
### メリット (Positive consequences)
- 依存解決済みの Issue 群が GitHub 上に生成され、開発者が正しい順序で作業を開始できる。
- TDD と `act` により、不整合や設定ミスを GitHub プッシュ前に 100% 検知可能になる。
- Fail-Fast 設計により、中途半端な起票によるリポジトリの汚染を防止できる。

### デメリット (Negative consequences)
- ローカル環境への Docker および `act` のセットアップが必須となる。

## 検証基準 / Verification Criteria
1.  **依存順序**: ファイル A, B (B が A に依存) を配置し、起票順が A -> B であること。
2.  **番号置換**: Issue B の本文内の `issue-A.md` が実際の `#<Aの番号>` に置換されていること。
3.  **Fail-Fast**: 循環参照（A<->B）配置時、`Cycle detected: A -> B -> A` と表示され、1件も起票されないこと。
4.  **Integration**: `act` を用いたローカルワークフロー実行が正常終了すること。

## 実装上の制約 (Constraints)
- **WBS設計時**: 依存構造を Mermaid 等で視覚化し、循環がないことをセルフチェックする指示を `migration-roadmap.md` に含めること。

## 実装状況 / Implementation Status
進行中
