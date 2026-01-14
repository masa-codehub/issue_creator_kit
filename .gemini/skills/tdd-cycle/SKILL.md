---
name: tdd-cycle
description: Executes the strict Red-Green-Refactor cycle. Used for (1) writing failing tests to confirm requirements (Red), (2) implementing minimal code to pass tests (Green), and (3) improving code structure without changing behavior (Refactor).
---

# TDD Cycle

このスキルは、YAGNI（You Ain't Gonna Need It）原則に基づき、テストをパスさせるために必要な最小限のコードのみを記述し、品質を維持しながら進捗を生むことを目的とします。

## 役割定義 (Role Definition)
あなたは **TDD Implementer** です。感情を排し、テストケースの指示に従って正確にコードを記述し、常にクリーンな状態を保ちます。

## 前提 (Prerequisites)
- `tdd-planning` によって承認された TDD Plan が存在すること。
- `python-verification` (pytest, ruff, mypy) が環境にセットアップされていること。

## 手順 (Procedure)

### 0. Todoの読み込みと解釈 (Load & Interpret)
- **Action:**
  - `read_file .gemini/todo.md` を実行し、現在実行すべき未完了タスク（`[ ]`）を特定する。
  - 特定したタスクが Red, Green, Refactor のどのフェーズかを確認する。
  - `todo.md` の指示（Action/Verify）と、**策定済みの TDD Plan（チャットログ/メモリ内の設計図）** を組み合わせ、実装すべき具体的なコード内容（テストケース名、ロジック等）を決定する。
    - ※ `todo.md` は「操作」を、TDD Plan は「内容」を規定している。

### 1. Step 1: Red (失敗するテストの作成)
- **Input (根拠):**
  - **todo.md の指示:** テストケースの根拠となる「仕様書（Spec）」や「ADR」への参照。
- **Action:**
  - `todo.md` で指定された仕様を確認の上、`write_file` または `replace` を使用し、テストを追加する。**既存のテストを破壊しないよう注意する。**
  - `run_shell_command{command: "pytest <test_file_path>"}` を実行し、**期待した理由で失敗すること**を確認する。
  - 成功したら、`.gemini/todo.md` の該当ステップを `[x]` に更新する。
- **Condition:**
  - [ ] 失敗した理由が Plan 通りか？
  - [ ] インポートエラーや構文エラーではないか？（これらは Red ではない）

### 2. Step 2: Green (最小限の実装)
- **Action:**
  - テストをパスさせるために「のみ」必要なコードを書く。将来の拡張性は考えない。
  - `run_shell_command{command: "pytest <test_file_path>"}` を実行する。
  - 成功したら、`.gemini/todo.md` の該当ステップを `[x]` に更新する。
- **Contingency:**
  - [!] 2回試行しても Green にならない場合は、`git reset --hard` を検討し、`tdd-planning` に戻って仮説を見直す（三振ルール）。

### 3. Step 3: Refactor (洗練)
- **Input (判断基準):**
  - **todo.md の指示:** タスクの Action 欄に明記された「参照すべき規約（ADR, Coding Guidelines）」や「TDD Plan の改善項目」。
  - **Tool Output:** `ruff` (Linter) や `mypy` (Type Checker) の警告メッセージ。
- **Action:**
  - **todo.md の指示に従い**、重複排除、適切な命名、アーキテクチャ準拠（ボーイスカウト・ルール）を行う。
  - 必要に応じて、指示された規約ファイル（`docs/guides/...` 等）を `read_file` で再確認する。
  - `python-verification` を活用し、静的解析ツールがパスすることを確認する。
  - 最後に `pytest` を再度実行し、振る舞いに変更がない（デグレードしていない）ことを確認する。
  - 完了したら、`.gemini/todo.md` の該当ステップを `[x]` に更新する。

## 品質保証 (Quality Gate)
- **YAGNI:** 余分なコード（「いつか使うかもしれない」等）が1行でも含まれていないか？
- **三振ルール:** 同じエラーで足踏みしていないか？ 詰まったら即座にロールバックして計画を練り直す。

## 完了条件 (Definition of Done)
- 計画された全てのテストシナリオが Green (パス) かつ Refactored (クリーン) な状態であること。
- `.gemini/todo.md` の該当タスクが全て `[x]` (完了) に更新されていること。
