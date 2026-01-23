# Phase Promotion Logic (Auto-PR) Specification

## 1. 概要 (Overview)
`WorkflowUseCase` による「フェーズ連鎖 (Phase Chain)」のロジックを定義する。
本機能は、特定のフェーズが完了（マージ）されたことをトリガーに、次フェーズのタスクを `drafts/` から `archive/` へ移動させ、仮想キューへの投入を促すプルリクエストを自動作成する。
「1 PR = 1 Task Transition」の原則に従い、予測可能でシンプルな自動化を実現する。

## 2. 入力 (Input)
| Name | Type | Description |
| :--- | :--- | :--- |
| `pr_body` | `str` | マージされたプルリクエストの本文。GitHub のキーワード（`Closes #123` 等）を解析対象とする。 |
| `archive_dir` | `Path` | タスクファイルが配置されているアーカイブディレクトリ。 |

## 3. ロジック詳細 (Logic Details)

### 3.1. PR 本文の解析 (Trigger Extraction)
GitHub が自動的に Issue を閉じるためのキーワードを対象に、Issue 番号を抽出する。
- **正規表現**: `(?i)(?:close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved)\s*#(\d+)`
- **1PR=1Task 原則**:
    - 本文中に複数のキーワードおよび Issue 番号が含まれる場合、**最初に見つかった 1 件のみ**をトリガーとして採用する。
    - 理由: 複数のフェーズを同時に連鎖させると依存関係が複雑化するため。

### 3.2. タスクファイルの特定 (Task Mapping)
抽出された Issue 番号に対応する物理ファイルを特定する。
1. `archive_dir` 配下の `.md` ファイルを再帰的にスキャンする。
2. 各ファイルのメタデータ（Frontmatter）の `issue` フィールドを確認する。
3. `issue: "#123"` のように、抽出した番号と一致するファイルを特定する。

### 3.3. フェーズ遷移の実行 (Promotion Action)
特定されたタスクファイルに `next_phase_path` メタデータが存在する場合、以下の手順で連鎖を実行する。

1. **ブランチ作成**:
    - 基点: `main` ブランチの最新。
    - 命名規則: `feature/{phase_name}-foundation`
    - `phase_name` は `next_phase_path` の末尾ディレクトリ名を採用する。
2. **ファイル移動**:
    - 移動元: `next_phase_path` (例: `reqs/tasks/drafts/phase-2`)
    - 移動先: `archive/` 下の対応するパス (例: `reqs/tasks/archive/phase-2`)
    - コマンド: `git mv` 相当の操作を実行する。
3. **コミット・プッシュ**:
    - メッセージ: `feat: promote {phase_name} tasks for virtual queue`
    - リモート (`origin`) へプッシュする。
4. **プルリクエスト作成**:
    - タイトル: `feat: promote {phase_name} tasks`
    - 本文: `Automatic promotion of tasks for {phase_name} from drafts to archive.`
    - Base: `main`
    - Head: 作成した新ブランチ。

## 4. 安全機構 (Safety Mechanisms)

### 4.1. 深度制限 (Infinite Loop Guard)
自動 PR の連鎖が無限に続くのを防ぐため、1 回のワークフロー実行における連鎖の深さを制限する。
- **最大深度**: 10
- **挙動**: 深度制限を超えた場合、警告を出力して処理を停止する。

### 4.2. 循環参照検知 (Circular Dependency Check)
同一の `next_phase_path` が同一セッション内で複数回呼び出されるのを防ぐ。
- **挙動**: `visited_phase_paths` セットで管理し、重複した場合は処理をスキップする。

## 5. エッジケース (Edge Cases)
| ケース | 期待される挙動 |
| :--- | :--- |
| `pr_body` が空、またはキーワードが含まれない | 何もしない。 |
| Issue 番号は見つかるが、対応するファイルが `archive/` にない | 何もしない（警告出力）。 |
| `next_phase_path` がメタデータに含まれない | 何もしない。 |
| `next_phase_path` が既に移動先に存在する | 処理をスキップし、不整合（既存ファイルの破壊）を防止する。 |
| 新規ブランチ名が既にリモートに存在する | `git checkout` 失敗時に例外を送出し、処理を中断する（冪等性の担保）。 |
