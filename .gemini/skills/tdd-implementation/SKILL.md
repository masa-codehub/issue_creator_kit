---
name: tdd-implementation
description: Orchestrates the entire TDD process (Planning -> Execution -> Closing). Manages the workflow by invoking specialized sub-skills like tdd-planning, tdd-refactoring, and tdd-audit. Used for (1) implementing complex features requiring high reliability, (2) fixing critical bugs with regression testing, and (3) building new modules with strict architectural alignment.
---

# TDD Implementation (Orchestrator)

複雑な実装タスクを TDD の原則に基づき、構造化されたプロセスで確実に完遂するためのオーケストレーションスキル。
`task-management` スキルのフレームワークを採用し、**仕様書に基づいたユースケース（UseCase）、ドメインロジック（Domain）、およびそれらを検証するテストコードを全て実装する。**

## 役割定義 (Role Definition)
あなたは **TDD Lead** です。テストを「仕様」として捉え、`task-management` のステートマシンを通じて、プロダクトコードが常に期待通りに動作することを保証します。

## 前提 (Prerequisites)
- 実装すべき機能の仕様（Specs）および、共通実装計画（Common Implementation Plan）が明確であること。

## 手順 (Procedure)

### 0. 計画の確認 (Policy Analysis)
- **Action:**
  - `docs/implementation/plans/*.md` および `docs/handovers/spec-to-tdd.md` を読み込む。
  - 今回のタスクで遵守すべきレイヤー構造、モック方針、共通型定義を把握する。

### 1. 計画フェーズ (State 1: Planning)
- **Action:**
  1. タスクマネジメントを開始する。
     `activate_skill{name: "task-management"}`
  2. 要求を分析し、SMART目標を設定する。
     `activate_skill{name: "objective-analysis"}`
     `activate_skill{name: "objective-setting"}`
     *   実装対象の機能（UseCase/Logic）を分析し、検証可能な完了条件（全テストパス、仕様網羅など）を定義する。
  3. Todoを作成・登録する。
     `activate_skill{name: "tdd-planning"}`
     *   `tdd-planning` スキルを活用し、タスク（Issue）で指定されたTDDシナリオに基づいた詳細な実装手順を `.gemini/todo.md` に展開する。

### 2. 実行フェーズ (State 2: Execution)
- **Action:**
  - `task-management` の実行サイクルに従い、Todoを順次消化する。
  - **Red/Greenサイクル:** 
    - **Red:** テストを先に書き、仕様を満たしていないことを確認して失敗させる。
    - **Green:** 最小限の実装（UseCase/Domainロジック等）を行い、テストをパスさせる。
  - **Refactorステップ:**
    `activate_skill{name: "tdd-refactoring"}`
    *   Green状態になった直後に必ず呼び出し、コードの品質向上とアーキテクチャへの適合を行う。

### 3. 完了フェーズ (State 3: Closing)
- **Action:**
  - `task-management` の完了フローに従う。
  - **Audit:**
    `activate_skill{name: "tdd-audit"}`
    *   全テストのパス、および**仕様書に記載されたバリデーションや例外挙動が全てユースケースとして実装されているか**を厳密に検証する。
  - **Retrospective:**
    `activate_skill{name: "retrospective"}`
    *   今回の実装サイクルを振り返る。

## 完了条件 (Definition of Done)
- 仕様書を満たすユースケース、ドメインロジック、およびテストコードがすべて実装・合格していること。
- 全ての品質基準を満たしていること。