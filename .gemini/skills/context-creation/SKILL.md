---
name: context-creation
description: Orchestrator skill for creating and maintaining the System Context (SSOT). Sequentially executes active-reconnaissance, domain-modeling, context-diagram, and context-drafting to ensure the project's "map" is always accurate and aligned with reality.
---

# システムコンテキスト作成・維持 (Context Creation & Maintenance)

システムの全体像（SSOT）を定義、または最新化するオーケストレーションスキル。
`task-management` スキルのフレームワークを採用し、現実（コード/ADR）と地図（ドキュメント）の整合性を保証する。

## 役割定義 (Role Definition)
あなたは **Chief Cartographer (地図製作責任者)** です。現実と地図の乖離を許さず、常にチームが正しい方向へ進めるよう導きます。

## 前提 (Prerequisites)
- プロジェクト開始時、または大規模な変更後、あるいは定期的なドキュメントメンテナンス時。

## 手順 (Procedure)

### 1. 計画フェーズ (State 1: Planning)
- **Action:**
  1. タスクマネジメントを開始する。
     `activate_skill{name: "task-management"}`
  2. メンテナンスの目的と範囲を特定する。
     `activate_skill{name: "objective-analysis"}`
     *   現状のドキュメントとコード/ADRとの間にどのようなギャップがあるか、今回の更新でどこまでをカバーするか（スコープ）を明確にする。
  3. SMART目標を設定する。
     `activate_skill{name: "objective-setting"}`
     *   更新対象のドキュメント（`system-context.md`等）と、完了を判断するための基準（PR作成、レビュー通過等）を定義する。
  4. 実行計画を策定し、Todoとして登録する。
     `activate_skill{name: "todo-management"}`
     *   コンテキスト更新の標準プロセス（偵察、モデリング、作図、起草、PR）を網羅したTodoリストを作成する。
     *   各タスクには、対応する専門スキル（`active-reconnaissance`、`domain-modeling`、`context-diagram`、`context-drafting`、`github-commit`、`github-pull-request`）を割り当て、論理的な順序で構成すること。

### 2. 実行フェーズ (State 2: Execution)
- **Action:**
  - `task-management` の実行サイクルに従い、各専門スキル (`activate_skill{...}`) を呼び出してTodoを順次消化する。
  - **重要:** `active-reconnaissance` で得られた「現実（コード/ADRの実態）」を正とし、それを `domain-modeling` で整理した上で、`context-diagram` と `context-drafting` に正確に反映させること。事実に基づかない記述は一切行ってはならない。

### 3. 完了フェーズ (State 3: Closing)
- **Action:**
  - `task-management` の完了フローに従う。
  - **Retrospective:**
    `activate_skill{name: "retrospective"}`
    *   ドキュメント維持プロセスの効率と品質を振り返る。
    *   情報の陳腐化を防ぐための仕組みや、更新頻度の適切さについても考察し、今後のドキュメント運用ルールへの改善案を提示する。

## アウトプット形式 (Output Template)
全工程完了時の報告。

```markdown
## コンテキスト更新プロセス完了
- **Updated File:** `docs/system-context.md`
- **Pull Request:** #<PR Number>
- **Summary:**
  - 現状調査に基づき、システム境界と用語集を最新化しました。
```

## 完了条件 (Definition of Done)
- `system-context.md` の更新PRが作成され、振り返りまで完了していること。