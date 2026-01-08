# インフラ層 インターフェース定義 (Infrastructure Interface Spec)

- **Author(s)**: TECHNICAL_DESIGNER
- **Status**: 下書き
- **Last Updated**: 2026-01-04

## 概要
ADR-003 で定義された「仮想キュー」および「フェーズ連鎖」を実現するために、ドメイン層（UseCase）がインフラ層に対して要求する操作を抽象化したインターフェース定義である。
これにより、ドメインロジックが具体的な Git コマンドや GitHub API の実装詳細から分離され、テスト容易性と保守性が向上する。

## 関連ドキュメント
- ADR: [ADR-003: 仮想キューと自己推進型ワークフロー](../../reqs/design/_approved/adr-003-task-and-roadmap-lifecycle.md)
- Design Doc: [仮想キューとフェーズ連鎖の論理フロー詳細設計](../../reqs/design/_inbox/design-003-logic.md)
- ドメインモデル: [Document クラス](../../src/issue_creator_kit/domain/document.py)

## インターフェース定義 (Interface Definition)

Python の `abc.ABC` または `typing.Protocol` を用いた実装を想定したシグネチャを定義する。

### 0. 共通型定義 (Shared Types)
インターフェースの戻り値等で使用される主要な型。

#### Document
Markdown ファイルの内容を表現するドメインオブジェクト。
- `title: str`: タスクのタイトル。
- `content: str`: Markdown の本文。
- `metadata: dict`: YAML Frontmatter の内容（`labels`, `depends_on`, `issue`, `next_phase_path` 等を含む）。
- `body`: （便宜上の属性）`content` から Frontmatter を除いた、Issue 本文として使用される文字列。

### 1. IGitAdapter
Git リポジトリに対する物理的な操作を担当する。
**使い分け**: ファイル操作が Git のインデックス管理（`git add`, `git mv`）を伴う必要がある場合に使用する。

| メソッド名 | 引数 | 戻り値 | 説明 |
| :--- | :--- | :--- | :--- |
| `get_added_files` | `base_ref: str, head_ref: str, path: str` | `list[str]` | `git diff-tree` を使用し、指定パス配下で追加（Added）されたファイルリストを取得する。 |
| `checkout` | `branch: str, create: bool = False, base: str | None = None` | `None` | 指定したブランチに切り替える。既存ブランチへ切り替える場合（`create=False`）は `base` の指定は不要。新規ブランチを作成する場合（`create=True`）は `base` を起点にブランチを作成する。 |
| `add` | `paths: list[str]` | `None` | 指定したファイルをステージングエリアに追加する。 |
| `commit` | `message: str` | `None` | ステージングされた変更をコミットする。 |
| `push` | `remote: str, branch: str, set_upstream: bool = False` | `None` | 指定したリモート・ブランチへプッシュする。 |
| `move_file` | `src: str, dst: str` | `None` | `git mv` を使用してファイルまたはディレクトリを移動する。 |

### 2. IGitHubAdapter
GitHub REST API を介した操作を担当する。

| メソッド名 | 引数 | 戻り値 | 説明 |
| :--- | :--- | :--- | :--- |
| `create_issue` | `title: str, body: str, labels: list[str]` | `int` | 指定したリポジトリに Issue を作成し、Issue 番号を返す。 |
| `create_pull_request` | `title: str, body: str, head: str, base: str` | `tuple[str, int]` | プルリクエストを作成し、PR の URL と番号を返す。 |
| `add_labels` | `issue_number: int, labels: list[str]` | `None` | 指定した Issue または PR にラベルを付与する。 |
| `add_comment` | `issue_number: int, body: str` | `None` | 指定した Issue または PR にコメントを投稿する（エラー通知等に利用）。 |

### 3. IFileSystemAdapter
ローカルファイルシステム上の Markdown ファイルのパースと書き換えを担当する。
**使い分け**: Git の履歴管理とは無関係な純粋なファイル読み書き、あるいはメタデータの部分更新に使用する。

| メソッド名 | 引数 | 戻り値 | 説明 |
| :--- | :--- | :--- | :--- |
| `read_document` | `path: str` | `Document` | 指定された Markdown ファイルを読み込み、YAML Frontmatter と Content を持つドメインオブジェクトを返す。 |
| `update_metadata` | `path: str, metadata: dict` | `None` | 指定されたファイルの Frontmatter を指定された辞書の内容で更新（マージ）する。 |
| `safe_move_file` | `src: str, dst_dir: str, overwrite: bool = False` | `None` | ファイルを指定ディレクトリへ移動する。OS レベルの移動であり Git インデックスは操作しない。 |
| `read_file` | `path: str` | `str` | ファイルを文字列として読み込む。 |
| `write_file` | `path: str, content: str` | `None` | 文字列をファイルに書き込む。 |

## シーケンス図 (Sequence Diagram)
UseCase がこれらのインターフェースを介してどのように協調するかを示す。

```mermaid
sequenceDiagram
    participant UC as WorkflowUseCase
    participant Git as IGitAdapter
    participant GH as IGitHubAdapter
    participant FS as IFileSystemAdapter

    Note over UC, FS: 仮想キュー検知 & 起票
    UC->>Git: get_added_files(base_ref, head_ref, "reqs/tasks/archive/")
    Git-->>UC: added_files
    loop each file
        UC->>FS: read_document(file)
        FS-->>UC: doc
        UC->>GH: create_issue(doc.title, doc.body, doc.metadata.labels)
        GH-->>UC: issue_number
        UC->>UC: メモリ上のバッファに (file, issue_number) を保存
    end
    Note over UC, FS: 全 Issue 作成成功後、一括書き戻し
    UC->>FS: update_metadata(all_processed_files)
    UC->>Git: add(all_processed_files)
    UC->>Git: commit("docs: update issue numbers")

    Note over UC, FS: ロードマップ同期
    UC->>FS: read_file(roadmap_path)
    FS-->>UC: content
    UC->>UC: リンク置換 (Draft -> Archive)
    UC->>FS: write_file(roadmap_path, new_content)
    UC->>Git: add([roadmap_path])
    UC->>Git: commit("docs: sync roadmap links")

    Note over UC, FS: フェーズ連鎖 (Auto-PR)
    UC->>Git: checkout(new_branch, create=True, base="main")
    UC->>Git: move_file(draft_dir, archive_dir)
    Note right of Git: Move contents of draft_dir to archive_dir
    UC->>Git: commit("feat: promote tasks")
    UC->>Git: push("origin", new_branch, set_upstream=True)
    UC->>GH: create_pull_request(title, body, head=new_branch, base="main")
```

## 補足・制約事項
- **エラーハンドリング**: 各インターフェースの実装（アダプター）は、基盤層のエラー（ネットワークエラー、Git コンフリクト等）を捕捉し、ドメイン層が解釈可能な例外（例: `InfrastructureError`）として再送出することが期待される。
- **レートリミット**: `IGitHubAdapter` の実装は、GitHub API のレート制限を考慮し、内部的にリトライロジックを持つべきである。詳細は Logic Design Doc を参照。