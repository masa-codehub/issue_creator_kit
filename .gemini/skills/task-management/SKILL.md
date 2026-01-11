---
name: task-management
description: Framework for systematic task execution using a state machine (Planning, Execution, Closing). Used for (1) complex feature implementation requiring multiple steps, (2) root-cause analysis and bug fixing, and (3) creation and organization of comprehensive design documents.
---

# タスクマネジメントフレームワーク (Task Management Framework)

タスクを確実に遂行するための状態遷移モデル。現在の自分の状態（State）を意識して行動する。

## State 1: Planning (計画)
- **いつ:** タスク開始時、または予期せぬエラーで計画が破綻した時。
- **Action:**
    1. **目標設定 (Goal Setting):** `objective-setting` スキルを使用して、具体的かつ実行可能な目標（SMART目標）を定義する。
    
    2. **Todo作成 (`save_memory`):** 目的達成に必要な手順をTodoリストとして作成し、記憶に保存・提示する。
        - **ステータス:** `[ ]` (Pending), `[x]` (Completed), `[!]` (Failed/Needs Analysis), `[-]` (Skipped)
        - **実行:** `save_memory{fact: "Current Todo: [x] タスク1, [ ] タスク2"}`
        
    3. **リスク評価 (Risk Assessment):**
       作成した計画がプロジェクトの成功を脅かさないか、以下の4点（4 Big Risks）で評価し、必要な対策をTodoに追加する。
        - **価値 (Value):** ユーザーやビジネスの価値向上に繋がるか？
        - **ユーザビリティ (Usability):** 利用者にとって使いやすいか？
        - **実現可能性 (Feasibility):** 現実的に完了できるか？
        - **ビジネス生存性 (Viability):** 法務・コスト・セキュリティ上の致命的問題はないか？

## State 2: Execution (実行)
- **いつ:** Todoリストがあり、Todoの内容について一切の懸念がなくなったとき。
- **Action:**
    1. **実行と適応:** Todoを順次実行する。
        - 適宜 `save_memory` を更新し、進捗を把握し続ける。
        - **失敗時:** すぐに修正せず、ステータスを `[!]` とし、直ちに次のTodoへ進む。前提が崩れた後続タスクは `[-]` とする。

## State 3: Closing (完了・振り返り)
- **いつ:** 全てのTodoが `[x]` または `[-]` になった時。
- **Action:**
    1. **振り返り (Retrospective):** 成果と課題を振り返り、次のアクションを決定する。
        - **YWT (技術・タスクの深掘り):** 技術的失敗や未知の挙動に対し、事実(Y)、知見(W)、仮説検証案(T)を記述。
        - **KPT (プロセス改善):** プロセス課題に対し、継続点(K)、問題点(P)、改善案(T)を記述。
    
    2. **メモリクリア (Memory Clear):**
        - `save_memory` のTodoリストを削除（または完了済みとしてクリア）する。

    3. **次のサイクルへ:**
        - 必要に応じてState 1へ戻る。YWTのTが出された場合は、それを次の最初のTodoにする。