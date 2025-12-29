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

## 目的と背景 (Goal & Context)
<!--
現状の課題 (As-is) と、このタスクで達成したい状態 (To-be) を記述します。
-->

## 実装指示 (Implementation Instructions)
<!--
具体的な作業手順や実装の詳細を記述します。
-->
1. 
2. 

## ブランチ戦略 (Branching Strategy)
このタスクは以下のブランチ戦略に従って実行します。
- **ベースブランチ (Base Branch)**: `feature/phase-X-foundation`
  - ※ フェーズ開始時に作成した基点となるブランチを指定します。
- **作業ブランチ (Feature Branch)**: `feature/task-ID-description`
  - ※ このタスクの実装を行うための専用ブランチです。
- **マージフロー**: `作業ブランチ` -> `ベースブランチ`

## 完了条件 (Definition of Done)
- [ ] 実装コードおよびテストコードがコミットされていること。
- [ ] すべてのテストがパスしていること。
- [ ] 作業ブランチがベースブランチにマージされていること。

## 成果物 (Deliverables)
- (例: `src/module.py`)

## 参照資料 (References)
- (例: ADR, API Spec, 外部資料など)