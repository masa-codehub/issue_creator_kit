---
depends_on: []
issue: '#226'
labels:
- task
- TECHNICAL_DESIGNER
next_phase_path: ''
roadmap: docs/architecture/plans/20260122-adr003-plan.md
status: Draft
task_id: T1-1
title: '[Arch] Create Structure Diagram for Virtual Queue & Adapters'
---

## 1. Goal & Context (Why & What)

### Goal
- ADR-003 v3 に基づき、新しいコンポーネント構造（仮想キュー検知、Auto-PR制御）を示す C4 Container Diagram を作成する。
- 特に、`WorkflowUseCase` がどのように `GitAdapter` (差分検知) と `GitHubAdapter` (PR操作) を使い分けるか、依存関係と責務の境界を明確にする。

### As-is (現状)
- ADR-003 は承認されたが、その実装詳細を示す最新のアーキテクチャ図（構造図）が存在しない。
- 既存の `arch-structure-issue-kit.md` は ADR-002 ベースであり、新しいコンポーネント（RoadmapSync, VirtualQueue Logic）が反映されていない。

### To-be (あるべき姿)
- `docs/architecture/arch-structure-003-vqueue.md` が作成され、以下の要素が正確に描画されている。
    - **App (CLI)**: Entrypoint.
    - **Domain (UseCases)**: `WorkflowUseCase`, `CreationUseCase`, `RoadmapSyncUseCase`.
    - **Infra (Adapters)**: `GitAdapter`, `GitHubAdapter`, `FileSystemAdapter`.
    - **Data Flow**: CLI -> Workflow -> UseCases -> Adapters の依存方向。

### Design Evidence
- [ADR-003](../../../design/_approved/adr-003-task-and-roadmap-lifecycle.md)
- [Architecture Plan](../../../docs/architecture/plans/20260122-adr003-plan.md)

## 2. Input Context (資料 & 情報)

- **Common Definitions Doc**: `docs/architecture/plans/20260122-adr003-plan.md`
    - セクション 3.2 (Layers & Components) の定義を厳守すること。
- **Source Code (Reference)**:
    - `src/issue_creator_kit/` 配下の現状のディレクトリ構造を確認し、実態と乖離しないようにする（ただし、未実装の `creation.py` 等は「あるべき姿」として描く）。
- **Template**: `docs/template/arch-structure.md`

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- ビジネスロジックの詳細（IF文やループ）を図中に記述しないこと。あくまで静的な構造（依存関係）にフォーカスする。
- `docs/system-context.md` (System Context) の境界を変更しないこと。

### 3.2. Implementation Steps (実行手順)
1.  **Read Plan**: `docs/architecture/plans/20260122-adr003-plan.md` を読み込み、コンポーネント定義を確認する。
2.  **Create File**: `docs/architecture/arch-structure-003-vqueue.md` を作成する（テンプレート `docs/template/arch-structure.md` を使用）。
3.  **Draft Diagram (Mermaid)**:
    - `classDiagram` または `C4Container` (Mermaid) を使用する。
    - **Core Components**:
        - `CreationUseCase` (New): 仮想キュー検知と一括起票を担当。
        - `RoadmapSyncUseCase` (New): ロードマップのリンク置換を担当。
        - `WorkflowUseCase` (Update): 全体のオーケストレーション。
    - **Adapters**:
        - `GitAdapter`: `get_added_files` 等のGit操作。
        - `GitHubAdapter`: `create_pull_request` 等のAPI操作。
    - **Dependencies**: UseCase -> Adapter の依存矢印を描く。
4.  **Description**: 各コンポーネントの責務を箇条書きで記述する（Planの定義を転記・整形）。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/arch-adr003-implementation`
- **Feature Branch**: `feature/task-T1-1-structure-diagram`

## 5. Verification & DoD (完了条件)
- [ ] `docs/architecture/arch-structure-003-vqueue.md` が存在し、空でないこと。
- [ ] Mermaid 図がレンダリング可能であり（構文エラーがない）、上記 "To-be" のコンポーネントが全て含まれていること。
- [ ] UseCase から Adapter への依存方向が一方向（上位 -> 下位）になっていること。
