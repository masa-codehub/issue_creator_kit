# 振り返りレポート (YWT): Infrastructure Implementation (PR #292)

## 1. Y (やったこと)
- **作業の実施内容:**
  - `IGitHubAdapter`, `IFileSystemAdapter` の Protocol 遵守を確認。
  - `GitHubAdapter` において `sync_issue`, `find_or_create_issue` を実装し、独自例外（`GitHubAPIError`, `GitHubRateLimitError`）によるハンドリングを導入。
  - `FileSystemAdapter` において `find_file_by_id` を regex ベースの高速検索で実装。
  - `pytest` による 17件（既存含む）のテスト実施とカバレッジ（GitHub: 86%, FS: 75%）の達成。
- **事象の観測:**
  - `FileSystemAdapter` の既存実装が既に `find_file_by_id` を持っていたが、`Document.parse` を使用した低速なものだった。
  - `pyfakefs` の `create_file` 引数が `content` ではなく `contents` であることに起因するテスト失敗に遭遇。
  - `Metadata` モデルのバリデーションが厳格であり、テストデータ不足による `ValidationError` が発生した。
- **分析情報の集約:**
  - `src/issue_creator_kit/domain/document.py` (Metadata定義)
  - `docs/specs/components/infra_adapters.md` (インフラ仕様)
  - `src/issue_creator_kit/domain/interfaces.py` (Protocol定義)

## 2. W (わかったこと)
- **結果の確認:**
  - `pydantic` を使用したドメインモデルが厳格であるため、インフラ層のテストデータ作成時にもドメイン知識（必須フィールド等）が必要。
  - `Protocol` の遵守を `isinstance(obj, Protocol)` で検証するためには `@runtime_checkable` デコレータが必要であること（既に付与されていたためスムーズに検証できた）。

### ギャップ分析
- **理想 (To-Be):** 仕様書通りの例外送出と、Protocol と完全一致するメソッドシグネチャ。
- **現状 (As-Is):** 既存実装の一部で `RuntimeError` が使われていたり、引数にデフォルト値があったりした。
- **ギャップ:** 実装の不統一と Protocol への不適合。
- **要因 (Root Cause):** 初期実装が暫定的なものであり、ADR-007 の詳細仕様（`infra_adapters.md`）が策定される前に書かれたため。

## 3. T (次やること / 仮説立案)
- **実証的仮説:** 
    - 今回追加した `sync_issue` のマッピングロジックを UseCase が利用し始めることで、Issue #292 の目的が完全に達成される。
- **飛躍的仮説:** 
    - `Document` から `GitHub Issue` へのマッピングルールを、コード内ハードコードではなく YAML 設定ファイル等で定義可能にすれば、他プロジェクトへの転用が容易になる。
- **逆説的仮説:** 
    - `find_file_by_id` はファイルシステムを直接走査しているが、Git 管理下にあるファイルであれば `git grep` 等をラップした方が高速かつ確実かもしれない。

### 検証アクション
- [x] インフラ層の Protocol 適合性テストを CI に組み込み、将来の破壊的変更を検知する。
- [ ] `find_or_create_issue` の検索精度向上のための追加テスト（特殊文字を含むタイトル等）を検討する。
