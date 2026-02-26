# CLI UX Specification

## 1. Overview

- **Responsibility**: `issue-kit` CLI におけるメッセージ出力形式、ステータス表示、および対話的なフィードバック（安全ガード）の標準化。
- **Collaborators**: CLI 層 (`cli.py`)、および各 UseCase 層から返されるエラーハンドリング部。

## 2. Data Structures (Models)

### 2.1. Status Prefixes

| Prefix   | Recommended Color | Description                          |
| :------- | :---------------- | :----------------------------------- |
| `[DONE]` | Green / Bold      | 成功。副作用が発生したことを示す。   |
| `[SKIP]` | Yellow            | スキップ。既知の状態であり変更不要。 |
| `[FAIL]` | Red               | 失敗。エラーメッセージが続く。       |
| `[INFO]` | Cyan              | 情報。スキャン結果や中間状態。       |

## 3. Interfaces (API/Methods)

### 3.1. Safety Guard Pattern

副作用（GitHub への書き込み、ファイルの移動）を伴う全コマンドにおいて、以下の挙動を強制する。

- `--execute` または `--dry-run` が指定されていない場合はエラー。
- デフォルトでの副作用実行は禁止。

## 4. Logic & Algorithms

### 4.1. Message Formatting

- **Standard**: `[PREFIX] {Message}`
- **Success Example**: `[DONE] Created Issue #123. URL: ...`
- **Error Example**: `[FAIL] [ERROR_CODE] {Message} ({File}:{Line})`

### 4.2. Summary Generation

コマンド終了時に必ず以下の形式で集計結果を表示する。

- Dry-run 時: `Dry-run summary: X to be created, Y skipped, Z errors.`
- Execute 時: `Execution summary: X created, Y skipped, Z errors.`

## 5. Traceability

- **Merged Files**:
  - `cli-ux-spec.md` (Legacy)
- **Handover Constraints**:
  - Standardized error format: `[ERROR_CODE] {Message}`.
