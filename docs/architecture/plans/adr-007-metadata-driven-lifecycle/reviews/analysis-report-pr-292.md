# 意図分析レポート (Analysis Report)

## 1. 意図の深掘り (Analyze Intent)

- **Why (なぜ必要か):**
  - ADR-007 で定義された「メタデータ主導のライフサイクル管理」を実環境で動かすためには、ドメイン層の抽象（Protocol）を満たす具体的なインフラ実装が不可欠である。
  - 特に `find_file_by_id` は、物理的にアーカイブされたタスクを再特定するために必須。
  - `sync_issue` は、ドキュメントの最新状態を常に GitHub Issue に反映させ、SSOT（Single Source of Truth）を維持するために必要。
- **What (何を達成するか):**
  - `FileSystemAdapter` と `GitHubAdapter` の完全実装。
  - 仕様書（`infra_adapters.md`）通りのエラーハンドリングとロジック。
- **How (どのように実現するか):**
  - `interfaces.py` の Protocol を遵守。
  - `pytest` とモック（`unittest.mock`, `pyfakefs`）による徹底した TDD 実装。

## 2. ギャップ分析 (Gap Analysis)

- **理想 (To-be):** `interfaces.py` のすべてのメソッドが実装され、`GitHubAPIError` などの独自例外が適切に投げられ、`Path | str` などの柔軟な型対応がなされている。
- **現状 (As-is):**
  - `GitHubAdapter` は `RuntimeError` を汎用的に使用しており、例外クラスが未整備。
  - `find_file_by_id` および `sync_issue` が未実装。
  - `find_or_create_issue` のタイトル検索ロジックが未実装。
- **乖離の要因:** 初期実装段階では暫定的なロジックのみが組み込まれており、ADR-007 の詳細な要求（IDベースの検索や正規化された同期）が反映されていない。

## 3. 仮説の立案 (Formulate Hypotheses)

### A. 実証的仮説 (Grounded) - 本命案

- **アプローチ:**
  - `GitHubAdapter` をリファクタリングし、`requests.Response.raise_for_status` をラップして独自例外を投げるように変更。
  - `find_file_by_id` は、対象ディレクトリを順次 `read_document` して ID を照合するシンプルな実装にする。
  - `sync_issue` は、既存の `issue_id` があれば更新、なければタイトル検索してヒットすれば更新、それ以外は新規作成する。
- **メリット:** 確実性が高く、仕様に忠実。
- **リスク:** 検索対象ファイルが多い場合、`read_document` の全スキャンはパフォーマンスに影響する可能性がある。

### B. 飛躍的仮説 (Leap) - 理想案

- **アプローチ:**
  - `find_file_by_id` において、`grep` 等の外部コマンドを併用した超高速なテキスト検索を導入する。
  - `GitHubAdapter` に指数バックオフ（`urllib3` のリトライ設定など）を組み込み、堅牢性を極限まで高める。
- **メリット:** パフォーマンスと堅牢性が最大化される。
- **リスク:** 環境依存（外部コマンドの有無）や実装の複雑性が増す。

### C. 逆説的仮説 (Paradoxical) - 革新案

- **アプローチ:**
  - ファイルシステムを直接走査するのではなく、SQLite 等の軽量 DB に ID とパスの対応をキャッシュする「インデックス管理」を導入する。
- **メリット:** 検索が O(1) になり、非常に高速。
- **リスク:** インデックスの同期（ファイル移動時の更新）という新たな管理コストが発生する。

## 4. 推奨案の決定

**推奨:** 「実証的仮説 (Grounded)」を採用する。
プロジェクトの現状（ファイル数は数百〜数千程度と想定）では、シンプルな走査で十分実用的であり、かつ外部依存や複雑性を避けるべきフェーズであるため。
ただし、`find_file_by_id` 内で全ファイルを `Document.parse` するのは重いため、正規表現で `id: task_id` 行を探す「半高速検索」を実装する。
