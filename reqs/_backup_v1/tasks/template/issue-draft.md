---
title: "タスクタイトル"
labels: # △ 推奨: タスク種別・優先度・担当ロールなど必要なラベルを設定すること（詳細は metadata-logic-spec.md 参照）
  - "task"
  - "P1" # Priority: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
  - "BACKENDCODER" # Role: BACKENDCODER, SYSTEM_ARCHITECT, TECHNICAL_DESIGNER, etc.
roadmap: "reqs/roadmap/active/roadmap-xxx.md" # ◯ 必須: 関連するロードマップへの相対パス（同期エンジンが使用）
task_id: "T1-1" # ◯ 必須: ロードマップ WBS と一致するタスクID（同期エンジンが使用。例: T1-1）
depends_on: [] # × 任意: 依存するタスクファイル名のリスト（例: ["issue-T1-1.md"]）。Topological Sort に使用。
next_phase_path: "" # × 任意: フェーズ最終タスクのみ記述。次フェーズの Draft パス（例: "reqs/tasks/drafts/phase-2/"）
status: "Draft" # ◯ 必須: 初期値は "Draft"。有効な値: "Draft" または "Archived"
# issue: # 起票後に ICK が自動追記。手動入力は不要。
---
# {{title}}

## 親Issue / ロードマップ (Context)
- **Roadmap**: {{roadmap}}
- **Task ID**: {{task_id}}

## 1. 目的と背景 (Goal & Context)
<!--
【エージェントへの指示】
このタスクの「Why」と「What」を明確にします。
- As-is (現状): 解決すべき課題、不足している機能、バグの状況。
- To-be (あるべき姿): 完了時にシステムやコードがどうなっているべきか。
- Design Evidence (設計の根拠): 根拠となる ADR や設計書のセクションを明記。
-->
- **As-is (現状)**: 
- **To-be (あるべき姿)**: 
- **Design Evidence (設計の根拠)**: 

## 2. 参照資料・入力ファイル (Input Context)
<!--
【エージェントへの指示】
作業開始時に必ず `read_file` すべきファイルリストです。
仕様書、インターフェース定義、関連する既存コードなどを指定します。
-->
- [ ] `docs/specs/xxx-spec.md`
- [ ] `src/issue_creator_kit/xxx/interface.py`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
<!--
【エージェントへの指示】
「やってはいけないこと」やスコープ外のことを明記します。
-->
- [ ] **変更禁止**: 
- [ ] **スコープ外**: 

### 3.2. 実装手順 (Changes)
<!--
【エージェントへの指示】
具体的な変更内容をステップバイステップで記述します。
-->
- [ ] **ファイル**: `src/issue_creator_kit/xxx.py`
    - **処理内容**: 

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- [ ] **ファイル**: `pyproject.toml`
- [ ] **削除**: 不要になったファイルがあれば指定。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-X-foundation`
- **作業ブランチ (Feature Branch)**: `feature/task-{{task_id}}-{{title_slug}}`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/xxx` がパスすること。
- [ ] **静的解析**: `ruff check .` および `mypy .` がパスすること。
- [ ] **観測される挙動**: 
- [ ] **ファイル状態**: 

## 6. 成果物 (Deliverables)
- (作成・修正したファイルパス)