---
depends_on: []
issue: '#238'
labels:
- task
- TECHNICAL_DESIGNER
next_phase_path: ''
roadmap: docs/specs/plans/20260122-spec-adr003-plan.md
status: Draft
task_id: S1-1
title: '[Spec] Update Document Domain Model (Metadata & Status)'
---

## 1. Goal & Context (Why & What)

### Goal
- `Document` ドメインモデルの仕様を更新し、ADR-003 で要求されるメタデータの厳密な管理（正規化、バリデーション、ステータス定義）を明文化する。

### As-is (現状)
- ADR-002 ベースのドキュメントモデル仕様が存在するが、日本語キーのマッピングや `status` の正確な値域、物理ディレクトリとの紐付けが曖昧。

### To-be (あるべき姿)
- `docs/specs/data/document_model.md` が更新され、以下の要件が TDD 可能なレベルで記述されている。
    - **Normalization**: キーを全て小文字にし、`タイトル` -> `title`, `ラベル` -> `labels` 等のエイリアスを解決するロジック。
    - **Status Values**: `Draft`, `Active`, `Archived` の定義。
    - **Validation**: 必須フィールド (`title`, `status`) のチェック。

### Design Evidence
- [Architecture Plan](../../../../../docs/architecture/plans/20260122-adr003-plan.md)
- [Handover Doc](../../../../../docs/handovers/arch-to-spec.md)

## 2. Input Context (資料 & 情報)
- **Common Definitions**: `docs/specs/plans/20260122-spec-adr003-plan.md`
- **Reference Diagram**: `../../../../../docs/architecture/arch-state-003-task-lifecycle.md`

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- メタデータ解析ロジックの「実装コード」そのものを記述しない（それは Backend Coder の役割）。あくまで「入力と出力の期待値」を記述する。

### 3.2. Implementation Steps (実行手順)
1.  **Read Handover**: 状態遷移と物理パスの紐付けに関する要件を確認。
2.  **Edit Spec**: `docs/specs/data/document_model.md` を更新。
3.  **Define Normalization**: 正規表現やマッピングテーブルを用いて、キー解決ルールを定義。
4.  **Define Validation**: 異常値（未定義のステータス、空タイトル等）に対する挙動を定義。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/spec-adr003-implementation`
- **Feature Branch**: `feature/task-S1-1-document-model-spec`

## 5. Verification & DoD (完了条件)
- [ ] 「日本語キーでパースした際、内部的には英語の標準キーとしてアクセスできること」が検証項目に含まれている。
- [ ] `status` の各値の意味と、それに対応するファイル状態（起票済みかどうか等）が明確である。
