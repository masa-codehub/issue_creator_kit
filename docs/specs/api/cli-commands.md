# CLI Commands Specification

## 1. Overview

- **Responsibility**: ユーザー入力を受け取り、適切な UseCase へ処理を委譲するインターフェース層。
- **Collaborators**: 全ての UseCase 層 (`RelayUseCase`, `ScannerService` 等)。

## 2. Data Structures (Models)

### 2.1. Exit Codes

| Code | Meaning          | Description                                                  |
| :--- | :--------------- | :----------------------------------------------------------- |
| `0`  | Success          | 全ての処理が正常に完了。                                     |
| `1`  | Error            | 一般的なエラー。                                             |
| `2`  | Validation Error | 引数不正、または Linter 等による論理的なバリデーション失敗。 |

### 2.2. Common Options

- `--execute`: 副作用を伴う実行を行う（必須）。
- `--dry-run`: 実行内容の表示のみを行う（必須）。
- ※ 上記 2 つは相互排他。

## 3. Interfaces (API/Methods)

### 3.1. `process`

- **Command**: `issue-kit process [--root PATH] (--execute | --dry-run)`
- **Responsibility**: 未処理のタスクおよび ADR をスキャンし、GitHub 起票を実行する。

### 3.2. `relay`

- **Command**: `issue-kit relay --issue-no INT (--execute | --dry-run)`
- **Responsibility**: 単一 Issue の完了をトリガーに後続タスクを活性化する。

### 3.3. `sync-relay`

- **Command**: `issue-kit sync-relay [--label LABEL] (--execute | --dry-run)`
- **Responsibility**: リポジトリ全体のタスク状態を走査し、不整合を修復する。

### 3.4. `check`

- **Command**: `issue-kit check [--root PATH]`
- **Responsibility**: ローカルファイル群の静的検証（循環参照、ID 不一致等）。

### 3.5. `visualize`

- **Command**: `issue-kit visualize [--root PATH]`
- **Responsibility**: 現在のタスク依存関係を Mermaid 形式で標準出力に表示する。
- **Note**: `check` コマンドの可視化機能として実装される場合もある。

## 4. Logic & Algorithms

### 4.1. Safety Guard

副作用を伴うコマンド（`process`, `relay`, `sync-relay` 等）において、`--execute` または `--dry-run` のいずれかが指定されていない場合、Exit Code 2 で終了し、フラグの指定を促す。

### 4.2. UseCase Delegation

CLI 層は UseCase のインスタンスを生成し、解析済み引数を渡すのみとする。直接的な API 通信やファイル操作は行わない。

## 5. Traceability

- **Merged Files**:
  - `cli_commands.md` (Legacy)
- **Handover Constraints**:
  - `issue-kit process` must exclude physical archive directories even if they exist (Constraint 4).
