---
name: architecture-visualization
description: Orchestrator skill for updating and maintaining architecture documentation. Sequentially executes planning, implementation, refactoring, and audit to ensure the "map" matches the "territory".
---

# Architecture Visualization Orchestration

アーキテクチャ図（Map）をコード実態（Territory）に同期させるプロセスを統括するスキル。
`task-management` を利用し、調査・作図・リファクタリング・監査のループを確実に実行する。

## 役割 (Role)
**Cartographer (地図製作者)**
変わり続けるコードベースを正確に追跡し、信頼できるナビゲーションマップ（ドキュメント）を提供する。

## 前提 (Prerequisites)
*   コードベースに意味のある変更（機能追加、構成変更）があった場合。
*   または、定期的なドキュメントメンテナンスのタイミング。

## 手順 (Procedure)

### 1. 計画フェーズ (State 1: Planning)
*   **Action:**
    1.  `activate_skill{name: "task-management"}` を起動。
    2.  `activate_skill{name: "architecture-planning"}` を呼び出し、SSOTに基づいた図の更新計画（Gap Analysis）を特定する。
    3.  `activate_skill{name: "todo-management"}` を使い、特定されたギャップを埋めるための `.gemini/todo.md` を作成する。

### 2. 実行フェーズ (State 2: Execution)
*   **Action:**
    *   `task-management` のサイクルに従い、Todoを順次消化する。
    *   **各タスク（図面の更新）ごとに以下の TDD サイクルを回す:**
        1.  **Targeting (Red):** Todoリストから着手するGap（要件）を確認し、「現在の図がその要件を満たしていないこと」を確認する。
        2.  **Drafting (Green):** `activate_skill{name: "architecture-drafting"}` を呼び出し、SSOTに基づいた正確な定義と図を記述する。
        3.  **Refining (Refactor):** `activate_skill{name: "architecture-refactoring"}` を呼び出し、記述した図のレイアウトや可読性を即座に改善する。
        4.  **Git:** `activate_skill{name: "github-commit"}` を行い、その図面が完成した状態でコミットする。

### 3. 完了フェーズ (State 3: Closing)
*   **Action:**
    *   **Audit:** `activate_skill{name: "architecture-audit"}` を呼び出し、最終的な整合性をチェックする。NGなら修正に戻る。
    *   **PR:** `activate_skill{name: "github-pull-request"}` で変更を提出する。
    *   **Retrospective:** `activate_skill{name: "retrospective"}` でプロセスを振り返る。

## 完了条件 (Definition of Done)
*   監査リスト（Audit Checklist）が全てPassしていること。
*   更新されたドキュメントを含むPRが作成されていること。
