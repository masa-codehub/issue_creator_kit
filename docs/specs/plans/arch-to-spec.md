# Handover: Architecture to Spec (ADR-003)

## 概要

アーキテクチャ設計フェーズ（Arch Creation）から詳細仕様策定フェーズ（Spec Creation）への申し送り事項をまとめる。
Spec Strategist は、本ドキュメントと `docs/architecture/*.md` を入力として、実装可能なレベルの詳細仕様書（Specs）を計画すること。

## 1. 重要な設計方針 (Critical Design Decisions)

### 1.1. 原子性と Fail-fast の厳守

- **Behavior:** `docs/architecture/arch-behavior-003-creation.md`
- **Specへの要求:**
  - `IssueCreationUseCase` の仕様において、「GitHub API エラー発生時は、Git リポジトリ（メタデータ）への書き込みを行わずに例外を送出し、プロセス全体を終了する（Exit 1）」ことを明記すること。
  - **禁止事項:** 1件ごとの逐次コミットや、エラー時のロールバック（Delete Issue）処理を仕様に含めないこと。ADR-003 の決定により、不整合防止のため「二重起票」は許容される。

### 1.2. 仮想キューと状態遷移

- **State:** `docs/architecture/arch-state-003-task-lifecycle.md`
- **Specへの要求:**
  - `Document` ドメインモデルの仕様において、`status` フィールドの値域（Draft, Active, Archived）を定義する際、物理ディレクトリ（`drafts/`, `archive/`）との関係性を明確にすること。
  - 特に「`archive/` にあるが Issue 番号がない状態」をシステムがどう扱うか（= 起票対象）をロジック仕様に含めること。

### 1.3. PRベースのフェーズ連鎖

- **Behavior:** `docs/architecture/arch-behavior-003-autopr.md`
- **Specへの要求:**
  - `WorkflowUseCase` の仕様において、PR 本文からの Issue 番号抽出ロジック（正規表現）を具体的に定義すること。
  - 次フェーズへの遷移（`promote_next_phase`）において、**必ず `main` ブランチをベースとして**新しいブランチを作成する仕様とすること。

## 2. 実装上の注意点 (Implementation Hints)

### 2.1. インフラ層の責務

- `GitHubAdapter` は、レートリミット（403/429）に対するリトライロジックを内包すべきである。
- `GitAdapter` は、`git diff-tree` などの低レベルコマンドを使用する際、出力パースの堅牢性を確保する必要がある。

### 2.2. ロードマップ同期

- `RoadmapSyncUseCase` は、Markdown のテーブル構造を破壊せずにリンクのみを置換する必要がある。正規表現による置換ロジックのテストケースを詳細に設計すること。

## 3. 残存するリスク (Residual Risks)

- **無限ループ:** `next_phase_path` が循環している場合（P1 -> P2 -> P1）、無限に PR が作成されるリスクがある。
  - **対策:** Spec にて「連鎖深度の制限（例: 最大10回）」または「循環検知ロジック」を要件として盛り込むこと。

## 4. 参照すべきアーキテクチャ図

- [Components (Structure)](../architecture/arch-structure-003-vqueue.md)
- [Creation Flow (Behavior)](../architecture/arch-behavior-003-creation.md)
- [Auto-PR Flow (Behavior)](../architecture/arch-behavior-003-autopr.md)
- [Lifecycle (State)](../architecture/arch-state-003-task-lifecycle.md)
