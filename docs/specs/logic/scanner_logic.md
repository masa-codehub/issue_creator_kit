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
1.  `root_path` を起点として、以下のディレクトリ（相対パス）を再帰的に検索する。
    - `design/_approved/`
    - `tasks/*/` (ただし `_archive/` ディレクトリは除外)
2.  見つかった `*.md` ファイルのうち、`exclude_patterns` に一致しないものを対象とする。
3.  対象ファイルを `TaskParser` を用いてパースし、`Task` または `ADR` モデルに変換する。
4.  **グローバル ID 重複チェック (Fail-fast)**:
    - 抽出した `id` が既に `processed_ids` に存在する場合、`ValidationError` (DUPLICATE_ID) を送出する。
    - 現在のスキャン対象リスト内で ID が重複している場合も、`ValidationError` (DUPLICATE_ID) を送出する。
    - **Rationale**: アーカイブ済み ID との衝突は、ユーザーが意図せず ID を再利用したことを示し、未処理ファイルがサイレントに無視されるリスクを防ぐため Fail-fast とする。
5.  **結果リストへの追加**:
    - バリデーションを通過したモデルを結果リストに追加する。

### 3. モデル変換とバリデーション (Model Conversion)
1.  `TaskParser` は Pydantic モデルを用いてメタデータの型と形式を検証する。
2.  不正なメタデータを持つファイルが見つかった場合、即座に `ValidationError` を送出し中断する (Fail-fast)。

## Edge Cases

### アーカイブと承認済み両方に同一 ID が存在する場合
- ステップ 2.4 により `ValidationError` (DUPLICATE_ID) となる。

### 同一 ID を持つ複数の「承認済み」ファイルがある場合
- ステップ 2.4 により `ValidationError` (DUPLICATE_ID) となる。

### 物理ファイルが空、または YAML ヘッダーがない場合
- `TaskParser` により `ValidationError` (INVALID_METADATA) となる。

### 指定された `root_path` が存在しない場合
- `FileNotFoundError` を送出する。

## Verify Criteria (TDD)

### Happy Path
| Scenario | Input Files | Expected Output |
| :--- | :--- | :--- |
| 全て未処理 | `design/_approved/task-1.md` | `[Task(id='task-1')]` |
| 複数未処理 | `design/_approved/adr-1.md`, `tasks/adr-008/task-1.md` | `[ADR(id='adr-1'), Task(id='task-1')]` |

### Error Path (Fail-fast)
| Scenario | Input Files | Expected Result |
| :--- | :--- | :--- |
| アーカイブと衝突 | `tasks/adr-008/task-1.md`, `tasks/_archive/task-1.md` | `ValidationError: DUPLICATE_ID 'task-1'` |
| 承認済み間で重複 | `design/_approved/task-1.md`, `tasks/adr-008/task-1.md` | `ValidationError: DUPLICATE_ID 'task-1'` |
| 不正なメタデータ | `design/_approved/task-1.md` (invalid YAML) | `ValidationError: INVALID_METADATA` |

### Boundary Path
| Scenario | Input | Expected Result |
| :--- | :--- | :--- |
| ディレクトリが空 | Empty `reqs/` | `[]` (Empty list) |
| 除外パターン適用 | `design/_inbox/task-1.md` (exclude: `_inbox/**`) | `[]` (無視される) |
| 対象外ディレクトリ | `docs/guides/note.md` | `[]` (無視される) |
