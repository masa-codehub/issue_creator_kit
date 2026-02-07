# FileSystemScanner Logic Specification

## Overview
ADR-008「Scanner Foundation」において、物理ファイルシステムから未処理のタスクおよび ADR を検出し、Domain Model に変換するロジックを定義する。
Git の差分情報に依存せず、ディレクトリ構造（`_approved`, `_archive`）のみを信頼の唯一のソース (SSOT) とする。

## Input
| Name | Type | Description |
| :--- | :--- | :--- |
| `root_path` | `PathLike` | 走査対象のベースディレクトリ（通常は `reqs/`） |
| `exclude_patterns` | `List[str]` | スキャンから除外するグロブパターン（例: `_inbox/**`） |

## Output
| Type | Description |
| :--- | :--- |
| `List[Union[Task, ADR]]` | 検出された未処理タスクおよび ADR オブジェクトのリスト |

## Algorithm / Flow

### 1. 処理済み ID の収集 (Collect Processed IDs)
まず、既に処理されアーカイブされたタスクを特定する。
1.  `root_path` 配下のすべての `_archive` ディレクトリを再帰的に検索する。
2.  見つかった `_archive/*.md` ファイルをすべて読み込む。
3.  各ファイルの YAML ヘッダーから `id` を抽出する。
4.  抽出した ID を `processed_ids` セットに追加する。
    - **注意**: アーカイブ内での ID 重複は許容される（履歴のため）が、読み込みエラーは無視せず報告する。

### 2. 未処理ファイルの走査 (Scan Unprocessed Files)
次に、承認済みだが未処理のファイルを検索する。
1.  `root_path` 配下の以下のディレクトリを再帰的に検索する。
    - `reqs/design/_approved/`
    - `reqs/tasks/*/` (ただし `_archive/` ディレクトリは除外)
2.  見つかった `*.md` ファイルを対象とする。
3.  各ファイルを `TaskParser` を用いてパースし、`Task` または `ADR` モデルに変換する。
4.  変換されたモデルの `id` を取得する。
5.  **ID 重複チェック**:
    - 現在のスキャン対象リスト内で ID が重複している場合、`ValidationError` (DUPLICATE_ID) を送出する。
    - 異なるファイルパスで同じ ID が指定されている状態を禁ずる。
6.  **未処理判定**:
    - `id` が `processed_ids` セットに含まれて**いない**場合のみ、結果リストに追加する。

### 3. モデル変換とバリデーション (Model Conversion)
1.  `TaskParser` は Pydantic モデルを用いてメタデータの型と形式を検証する。
2.  不正なメタデータを持つファイルが見つかった場合、即座に `ValidationError` を送出し中断する (Fail-fast)。

## Edge Cases

### アーカイブと承認済み両方に存在する場合
- `id` が `processed_ids` に含まれるため、結果リストには含まれない（正解：処理済みとして扱う）。

### 同一 ID を持つ複数の「承認済み」ファイルがある場合
- ステップ 2.5 により `ValidationError` となる（不正な状態）。

### 物理ファイルが空、または YAML ヘッダーがない場合
- `TaskParser` により `ValidationError` となる。

### 指定された `root_path` が存在しない場合
- `FileNotFoundError` を送出する。

## Verify Criteria (TDD)

### Happy Path
| Scenario | Input Files | Expected Output |
| :--- | :--- | :--- |
| 全て未処理 | `approved/task-1.md` | `[Task(id='task-1')]` |
| 一部処理済み | `approved/task-1.md`, `archive/task-1.md` | `[]` (Empty) |
| 混在 | `approved/task-1.md`, `approved/task-2.md`, `archive/task-1.md` | `[Task(id='task-2')]` |

### Error Path
| Scenario | Input Files | Expected Result |
| :--- | :--- | :--- |
| ID 重複 | `approved/dir1/task-1.md`, `approved/dir2/task-1.md` | `ValidationError: DUPLICATE_ID 'task-1'` |
| 不正なメタデータ | `approved/task-1.md` (invalid YAML) | `ValidationError: INVALID_METADATA` |

### Boundary Path
| Scenario | Input | Expected Result |
| :--- | :--- | :--- |
| ディレクトリが空 | Empty `reqs/` | `[]` (Empty list) |
| 対象外ディレクトリ | `_inbox/task-1.md` | `[]` (無視される) |
