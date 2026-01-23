---
title: "[Spec] Update CLI Command Definitions (Orchestration)"
labels:
  - task
  - TECHNICAL_DESIGNER
roadmap: "docs/specs/plans/20260122-spec-adr003-plan.md"
task_id: "S1-6"
depends_on: ["issue-S1-2.md", "issue-S1-3.md"]
next_phase_path: ""
status: "Draft"
---

## 1. Goal & Context (Why & What)

### Goal
- `issue-kit` CLI のコマンド体系を、ADR-003 の「自動起票」と「フェーズ連鎖」に合わせて再定義する。

### As-is (現状)
- ADR-002 ベースのコマンド定義はあるが、マージイベントから呼ばれる `process-diff` (起票用) と `process-merge` (連鎖用) の役割分担が未整理。

### To-be (あるべき姿)
- `docs/specs/api/cli_commands.md` が更新され、以下のコマンド仕様が定義されている。
    - **`run-workflow`**: 後方互換または統合用コマンドとして定義（実体は `process-diff` と `process-merge` を順次呼び出す等）。
    - **`process-diff`**: 仮想キュー検知から一括起票、メタデータ・ロードマップ同期までを一気通貫で実行。
    - **`process-merge`**: マージ済み PR の本文解析から、必要に応じた Auto-PR 作成を実行。
    - **Exit Codes**: 各エラー状態に対応する終了コード。

### Design Evidence
- [Structure Diagram (App Layer)](../../../../../docs/architecture/arch-structure-003-vqueue.md)
- [Creation Behavior Diagram](../../../../../docs/architecture/arch-behavior-003-creation.md)

## 2. Input Context (資料 & 情報)
- **Common Definitions**: `docs/specs/plans/20260122-spec-adr003-plan.md`
- **Current Specs**: `docs/specs/api/cli_commands.md`

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- CLI 層で直接 `subprocess` や `requests` を使用しない。全ての IO は Adapter を介して UseCase を通じて行うこと。

### 3.2. Implementation Steps (実行手順)
1.  **Define Options**: 各コマンドで必須となる引数（`--branch`, `--base-ref` 等）を定義。
2.  **Mapping to UseCases**: 各コマンドがどの UseCase メソッドを呼び出すかを明示。
3.  **Error Propagation**: UseCase で発生した例外をどのようにユーザーへ通知するか（ログ、終了コード）を定義。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/spec-adr003-implementation`
- **Feature Branch**: `feature/task-S1-6-cli-spec`

## 5. Verification & DoD (完了条件)
- [ ] 「引数が不足している場合に、終了コード 1 と適切なメッセージを出力すること」が検証基準に含まれている。
- [ ] 各コマンドの成功・失敗の判定条件が明確である。
