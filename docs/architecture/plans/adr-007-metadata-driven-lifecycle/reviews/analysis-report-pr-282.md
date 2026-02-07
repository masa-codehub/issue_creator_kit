# Analysis Report - Update Infrastructure Adapter Specifications

## 1. 意図の分析 (Intent Analysis)

- **核心的ニーズ**: ADR-007 で定義された「物理ファイルを予約券として扱い、起票後にアーカイブへ自動移動する」というライフサイクルを、インフラ層のインターフェースとして具現化すること。
- **Why**: 物理構造に依存しないタスク管理を実現し、AIエージェントが「どのファイルが起票済みか」をメタデータ（`status: Issued`, `issue_id: 123`）と物理配置（`_archive/`）の両面から確実に判断できるようにするため。

## 2. ギャップ分析 (Gap Analysis)

- **FileSystem**:
  - 現在は `safe_move_file` しかなく、アーカイブされた大量のファイルから特定の `id` (e.g., `007-T1`) を持つファイルを特定する `find_by_id` のようなロジックが欠如している。
  - 「原子性」の定義が、単なるファイル移動を指すのか、メタデータ更新を含めた一連の処理を指すのかが不明確。
- **GitHub**:
  - Issue 起票時のマッピング（どのメタデータが `title` や `body` に入るか）が UseCase 任せになっており、インフラ層としての規約が弱い。
  - 起票成功後に取得した `issue_id` を、どのタイミングで誰がメタデータに書き戻すかの契約が未定義。

## 3. 仮説の立案 (Formulate Hypotheses)

### 3.1. 実証的仮説 (Grounded - 本命案)

- **FileSystem**: `find_by_id(id: str, search_dirs: list[str])` を追加し、メタデータの `id` フィールドを grep 的に検索する仕様を定義。移動は「GitHub 起票成功」を条件とする UseCase 側のトランザクション管理に従う。
- **GitHub**: `create_issue_from_document(doc: Document)` を追加。`Document` オブジェクトを直接受け取り、内部でマッピング規約（Title: `doc.metadata.get("id") + ": " + (doc.metadata.get("title") or doc.metadata.get("タイトル") or "")`, Body: `doc.content + footer`）を適用する。

### 3.2. 飛躍的仮説 (Leap - 理想案)

- **Unit of Work パターン**: `InfrastructureTransaction` を導入し、GitHub 起票とファイル移動をコミット/ロールバック可能な形式でラップする。これにより UseCase 側のロジックを極限までシンプルにする。

### 3.3. 逆説的仮説 (Paradoxical - 規約による解決)

- ファイル移動を廃止し、メタデータの `status: Issued` だけですべてを管理する。しかし、これは ADR-007 の「物理配置による認知負荷低減」という目的に反するため、今回は採用しない。

## 4. 推奨案 (Recommended Approach)

**実証的仮説 (Grounded)** をベースに、以下のインターフェースを `infra_adapters.md` に追加・洗練させる。

1. `FileSystemAdapter.find_file_by_id(task_id: str) -> Path`: 特定のIDを持つファイルを検索。
2. `GitHubAdapter.sync_issue(doc: Document) -> int`: 起票または更新を行い、`issue_id` を返す。`phase`, `type` メタデータをラベルにマッピングする。
3. **Atomic Sequence Definition**: 「GitHub Response -> Metadata Injection -> Atomic Move」のシーケンス図的な記述を仕様に加える。
