---
name: tdd-implementation
description: Orchestrates the entire TDD process (Planning -> Execution -> Closing). Manages the workflow by invoking specialized sub-skills like tdd-planning, tdd-refactoring, and tdd-audit. Used for (1) implementing complex features requiring high reliability, (2) fixing critical bugs with regression testing, and (3) building new modules with strict architectural alignment.
---

# TDD Implementation (Orchestrator)

複雑な実装タスクを TDD の原則に基づき、構造化されたプロセスで確実に完遂するためのオーケストレーションスキル。
`task-management` スキルのフレームワークを採用し、品質と信頼性を極限まで高めた開発を実現する。

## 役割定義 (Role Definition)
あなたは **TDD Lead** です。テストを「仕様」として捉え、`task-management` のステートマシンを通じて、コードが常に期待通りに動作することを保証します。

## 前提 (Prerequisites)
- 実装すべき機能、または修正すべきバグの仕様（Design Doc等）が明確であること。

## 手順 (Procedure)

### 1. 計画フェーズ (State 1: Planning)
- **Action:**
  1. タスクマネジメントを開始する。
     `activate_skill{name: "task-management"}`
  2. 要求を分析し、SMART目標を設定する。
     `activate_skill{name: "objective-analysis"}`
     `activate_skill{name: "objective-setting"}`
     *   実装対象の機能や修正内容を分析し、検証可能な完了条件（テストパス、カバレッジ達成率など）を定義する。
  3. Todoを作成・登録する。
     `activate_skill{name: "tdd-planning"}`
     *   `tdd-planning` スキルを活用し、テストシナリオに基づいた詳細な実装計画を `.gemini/todo.md` に展開する。
     *   この計画には、Red/Green/Refactorの各サイクル、必要なテストケースの実装順序、および品質チェック（Audit）のステップが論理的に組み込まれていなければならない。

### 2. 実行フェーズ (State 2: Execution)
- **Action:**
  - `task-management` の実行サイクルに従い、Todoを順次消化する。
  - **Red/Greenサイクル:** 通常のツール（`write_file`, `run_shell_command`）を使用し、まずはテストを失敗させ（Red）、次に最小限の実装でパスさせる（Green）。
  - **Refactorステップ:**
    `activate_skill{name: "tdd-refactoring"}`
    *   Green状態になった直後に必ず呼び出し、重複の排除、可読性の向上、アーキテクチャへの適合を行う。機能追加は行わない。

### 3. 完了フェーズ (State 3: Closing)
- **Action:**
  - `task-management` の完了フローに従う。
  - **Audit:**
    `activate_skill{name: "tdd-audit"}`
    *   全テストのパス、Linter/Type Checkの通過、および実装漏れがないかを厳密に検証する。問題があればExecutionフェーズに戻る。
  - **Retrospective:**
    `activate_skill{name: "retrospective"}`
    *   TDDサイクルが機能したか、テストは書きやすかったか、設計上の問題はなかったかを振り返り、次回の実装効率向上につなげる。

## 完了条件 (Definition of Done)
- 全てのテストケースがパスし、カバレッジと品質基準を満たしていること。
- PRが作成され、振り返りまで完了していること。