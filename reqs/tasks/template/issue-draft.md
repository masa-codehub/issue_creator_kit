---
title: "タスクタイトル"
labels:
  - "task"
  - "P1" # Priority: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
  - "BACKENDCODER" # Role: BACKENDCODER, SYSTEM_ARCHITECT, etc.
roadmap: "reqs/roadmap/active/roadmap-xxx.md" # 関連するロードマップへの相対パス
task_id: "TX-Y" # タスクID (例: T1-1)
depends_on: [] # 依存するIssueファイル名のリスト (例: ["issue-T1-1.md"])
next_phase_path: "" # フェーズ最後のタスクのみ記述。次フェーズの Draft ディレクトリパス
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
- Evidence: 詳細設計書のどのセクション（第X項等）に基づく変更か。
-->
- **As-is (現状)**: 
- **To-be (あるべき姿)**: 
- **Design Evidence (設計の根拠)**: [Design Doc 名] 第 X.X 項

## 2. 参照資料・入力ファイル (Input Context)
<!--
【エージェントへの指示】
作業開始時に必ず `read_file` すべきファイルリストです。
設計書、インターフェース定義、関連する既存コードなどを「これだけ読めば完遂できる」最小セットで指定します。
-->
- [ ] `docs/specs/xxx-spec.md` (仕様書)
- [ ] `src/xxx/interface.py` (準拠すべきインターフェース)

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
<!--
【エージェントへの指示】
「やってはいけないこと」を明記し、サイドエフェクトを最小化します。
-->
- [ ] **変更禁止**: (例: 既存の `Adapter` のメソッドシグネチャは変更しない)
- [ ] **スコープ外**: (例: 共通ユーティリティのリファクタリングは行わない)

### 3.2. 実装手順 (Changes)
<!--
【エージェントへの指示】
「どのファイルを」「どう変更するか」を具体的に記述します。
-->
- [ ] **ファイル**: `src/path/to/target.py`
    - **処理内容**: (例: `design-003-logic.md` 第 2.1 項に基づき、XX メソッドを実装する)

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- [ ] **ファイル**: `pyproject.toml` (依存ライブラリの追加など)
- [ ] **削除**: (不要になるファイルがあれば)

## 4. ブランチ戦略 (Branching Strategy)
<!--
【エージェントへの指示】
作業の隔離とフェーズ統合のためのブランチを指定します。
-->
- **ベースブランチ (Base Branch)**: `feature/phase-X-foundation`
- **作業ブランチ (Feature Branch)**: `feature/{{task_id}}-{{title_slug}}`

## 5. 検証手順・完了条件 (Verification & DoD)
<!--
【エージェントへの指示】
実装が正しいことを客観的に証明するためのコマンドと「観測されるべき挙動」を記述します。
-->
- [ ] **Acceptance Criteria ID**: (例: TC-001, TC-002)
- [ ] **自動テスト**: `pytest tests/unit/test_xxx.py` がパスすること。
- [ ] **観測される挙動**: (例: 実行時に 'Atomic archiving started' というログが出力されること)
- [ ] **ファイル状態**: (例: 失敗時に `_queue/` 内のファイルが維持されていることを `ls` で確認すること)


## 6. 成果物 (Deliverables)
- (作成・修正されたファイルパスのリスト)
