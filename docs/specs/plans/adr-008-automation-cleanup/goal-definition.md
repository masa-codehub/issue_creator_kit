# 目標定義書 (Goal Definition)

## 1. 核心的目標 (Core Intent / SMART Goal)
- **ゴール:** ADR-008に基づき、レガシーな自動化コード（Workflow, Approval関連）を完全に削除し、関連する参照とテストを整理する。
- **採用した仮説:** 案A (Grounded) - 物理削除と最小限の参照修正。
- **期待される価値:** 新しいScannerベースのアーキテクチャへの円滑な移行と、メンテナンス負荷の軽減。

## 2. 実行の前提条件 (Achievable / Prerequisites)
- **対象ファイル:** 
    - 削除: `.github/workflows/auto-approve-docs.yml`, `src/issue_creator_kit/usecase/workflow.py`, `src/issue_creator_kit/usecase/approval.py`, `tests/unit/usecase/test_workflow.py`, `tests/unit/usecase/test_approval.py`
    - 修正: `src/issue_creator_kit/cli.py`, `src/issue_creator_kit/usecase/creation.py`, `tests/unit/test_cli.py`
- **必要な情報:** `cli.py` における削除対象コマンドの使用箇所（特定済み）。
- **依存タスク:** なし。

## 3. アクションプラン (Specific / Time-boxed)
1. **[削除]:** 指定された5つのファイルを物理削除する。
2. **[修正: cli.py]:** `approve`, `approve-all`, `process-merge` コマンドに関連するインポート、初期化、コマンド定義、パーサー、ディスパッチ処理を削除する。
3. **[修正: creation.py]:** `WorkflowUseCase` のインポートと `__init__` での引数/属性保持を削除する。
4. **[修正: test_cli.py]:** 削除されたコマンドに関連するテストケースおよびモックパッチを削除する。
5. **[検証]:** `pytest` の実行と、CLIヘルプでコマンドが削除されていることを確認する。

## 4. 完了定義 (Measurable / Definition of Done)
### A. 自動検証 (Automated)
- **検証コマンド:**
  ```bash
  pytest tests/unit/
  ruff check .
  mypy .
  ```
- **合格基準:** 全てのテストがパスし、静的解析でインポートエラーや未定義名エラーが出ないこと。

### B. 状態検証 (State Check)
- **確認対象:** ファイルの存在とCLIヘルプ。
- **合格基準:** 
    - `ls` コマンドで削除対象ファイルが存在しないこと。
    - `python -m issue_creator_kit.cli --help` を実行した際、`approve`, `approve-all`, `process-merge` が一覧に表示されないこと。

## 5. 制約と安全策 (Constraints & Safety)
- **負の制約:** 新しい Scanner 実装には一切手を加えない。削除と参照整理のみを行う。
- **安全策:** 削除前に `git status` で現在の状態を確認し、各修正ステップごとに差分を確認する。

## 6. SMART 自己評価
- **Specific:** 削除対象ファイルと修正箇所が明確にリストアップされている。
- **Measurable:** `pytest` と `ls`, `--help` で客観的に判定可能。
- **Achievable:** 影響範囲は `cli.py` と `creation.py`, テストコードに限定されており、調査済み。
- **Relevant:** ADR-008のクリーンアップ要件に直接対応している。
- **Time-boxed:** 一連の削除と参照整理は1ターンの作業として完結可能。
