---
title: "[Arch] Create Integration Issue for ADR-003 Architecture"
labels:
  - task
  - SYSTEM_ARCHITECT
roadmap: "docs/architecture/plans/20260122-adr003-plan.md"
task_id: "T1-Integration"
depends_on: ["issue-T1-1.md", "issue-T1-2.md", "issue-T1-3.md", "issue-T1-4.md"]
next_phase_path: ""
status: "Draft"
---

## 1. Goal & Context (Why & What)

### Goal
- 分散して作成されたアーキテクチャ図（Structure, Behavior, State）を統合し、SSOTとしての整合性を監査する。
- 監査完了後、メインラインへのマージリクエスト（PR）を作成する。

### As-is (現状)
- 個別のアーキテクチャ図は作成されるが、それらが相互に矛盾していないか（例: Structureで定義されていないコンポーネントがBehaviorで使われていないか）をチェックするプロセスが必要。

### To-be (あるべき姿)
- 全ての図が統合され、一貫性のあるアーキテクチャドキュメント群としてリリース可能な状態になる。
- `docs/handovers/arch-to-spec.md` が作成され、後続の Spec Strategist への申し送り事項が記載されている。

### Design Evidence
- [Architecture Plan](../../../docs/architecture/plans/20260122-adr003-plan.md)

## 2. Input Context (資料 & 情報)

- **Common Definitions Doc**: `docs/architecture/plans/20260122-adr003-plan.md`
- **Draft Issues**: `T1-1` ~ `T1-4` の成果物。

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- このタスク内で図の大幅な書き直しを行わないこと。不整合が見つかった場合は、修正用のIssueを別途起票するか、軽微であれば修正コミットを行う。

### 3.2. Implementation Steps (実行手順)
1.  **Merge Check**: 全ての依存タスク（T1-1 ~ T1-4）のブランチが `feature/arch-adr003-implementation` にマージされていることを確認する。
2.  **SSOT Audit (Consistency Check)**:
    - **Structure vs Behavior**: Behavior図に登場するコンポーネントがStructure図に存在するか。
    - **State vs Behavior**: State図の遷移トリガーが、Behavior図のイベントと一致しているか。
    - **Terminologies**: Planで定義された用語（Virtual Queue, Atomic Creation 等）が統一されているか。
3.  **Broken Link Check**: ドキュメント間のリンクが有効か確認する。
4.  **Create Handover Doc**:
    - `docs/handovers/arch-to-spec.md` を作成する。
    - 内容: 「Spec Strategistは、`CreationUseCase` と `WorkflowUseCase` の仕様策定において、`arch-behavior-003-creation.md` のエラー処理フローを厳密に守ること」等の指示を記述。
5.  **Create Pull Request**:
    - `feature/arch-adr003-implementation` から `main` へのPRを作成する。
    - タイトル: `docs(arch): Visualize ADR-003 Task Lifecycle Architecture`

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/arch-adr003-implementation` (This is the integration branch itself)
- **Feature Branch**: N/A (Run on base branch or temp branch)

## 5. Verification & DoD (完了条件)
- [ ] 全てのアーキテクチャ図が揃っていること。
- [ ] `docs/handovers/arch-to-spec.md` が作成されていること。
- [ ] `main` へのPRが作成されていること（マージはしない）。
