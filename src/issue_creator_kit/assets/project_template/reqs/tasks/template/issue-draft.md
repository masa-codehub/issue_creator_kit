---
title: "タスクタイトル"
labels:
  - "task"
  - "P1" # Priority: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
  - "BACKENDCODER" # Role: BACKENDCODER, SYSTEM_ARCHITECT, etc.
roadmap: "reqs/roadmap/active/roadmap-xxx.md" # 関連するロードマップへの相対パス
task_id: "TX-Y" # タスクID (例: T1-1)
depends_on: [] # 依存するIssueファイル名のリスト (例: ["issue-T1-1.md"])
status: "Draft"
---

# {{title}}

## 親Issue / ロードマップ (Context)

- **Roadmap**: {{roadmap}}
- **Task ID**: {{task_id}}

## 1. 目的と背景 (Goal & Context)

<!--
【エージェントへの指示】
このタスクの「Why」と「What」を明確にします。
- As-is: 現在のコードや仕様のどこに問題/不足があるか。
- To-be: このタスク完了時にどうなっているべきか（最終形）。
-->

- **As-is (現状)**:
- **To-be (あるべき姿)**:

## 2. 参照資料・入力ファイル (Input Context)

<!--
【エージェントへの指示】
作業開始時に必ず `read_file` すべきファイルリストです。
設計書、インターフェース定義、関連する既存コードなどを指定します。
-->

- [ ] `docs/specs/xxx-spec.md` (仕様書)
- [ ] `src/xxx/interface.py` (準拠すべきインターフェース)

## 3. 実装手順 (Implementation Steps)

<!--
【エージェントへの指示】
「どのファイルを」「どう変更するか」をファイル単位で具体的に記述します。
クラス名、関数名、シグネチャが確定している場合は明記してください。
-->

### 3.1. 新規作成・変更 (Changes)

- [ ] **ファイル**: `src/path/to/target.py`
  - **処理内容**: (例: `process_data` 関数を実装する)
  - **要件**: (例: 入力値が空の場合は `ValueError` を送出すること)

### 3.2. 構成変更・削除 (Configuration / Cleanup)

- [ ] **ファイル**: `pyproject.toml` (依存ライブラリの追加など)
- [ ] **削除**: (不要になるファイルがあれば)

## 4. ブランチ戦略 (Branching Strategy)

- **ベースブランチ (Base Branch)**: `feature/phase-X-foundation`
- **作業ブランチ (Feature Branch)**: `feature/{{task_id}}-{{title_slug}}`

## 5. 検証手順・完了条件 (Verification & DoD)

<!--
【エージェントへの指示】
実装が正しいことを証明するための具体的なコマンドと基準を記述します。
「テストが通ること」ではなく「どのテストコマンドを実行するか」を書きます。
-->

- [ ] **自動テスト**: `pytest tests/unit/test_xxx.py` がパスすること。
- [ ] **静的解析**: `ruff check .` および `mypy .` でエラーが出ないこと。
- [ ] **マージ**: 作業ブランチがベースブランチにコンフリクトなくマージされていること。

## 6. 成果物 (Deliverables)

- (作成・修正されたファイルパスのリスト)
