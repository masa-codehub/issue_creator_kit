---
id: T-<TaskID> # 例: T-1
parent: adr-<ADR-ID> # 例: adr-007
type: task # task | integration
title: "<Task Title>"
status: Draft # Draft | Ready | Completed | Cancelled
phase: domain # domain | infrastructure | usecase | interface | architecture | spec | tdd
roadmap: "docs/architecture/plans/<Plan-File>.md"
depends_on: [] # 必須: 依存するタスク ID (例: ["T-1"])。依存がない場合は []
issue_id: # 【自動追記】手動で設定しないでください
---
# <Task Title>

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
- **ベースブランチ (Base Branch)**: main
- **作業ブランチ (Feature Branch)**: feature/task-<ID>-<title_slug>

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/xxx` がパスすること。
- [ ] **静的解析**: `ruff check .` および `mypy .` がパスすること。
- [ ] **観測される挙動**: 
- [ ] **ファイル状態**: 

## 6. 成果物 (Deliverables)
- (作成・修正したファイルパス)
