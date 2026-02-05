# Metadata-Driven Architecture Structure (ADR-007)

## Context
- **Bounded Context:** Task Lifecycle Management
- **System Purpose:** ADR-007 で導入された「メタデータ駆動型ライフサイクル」を実現するための、フラットなファイル構造と論理的な依存関係（DAG）の定義。物理的な階層構造を排除し、認知負荷を最小化しつつ、自動化ツールによる精密な制御を可能にする。

## Diagram (C4 Container & DAG)

```mermaid

C4Container

    title Metadata-Driven Container Diagram



    Person(actor, "Developer/Agent", "設計・タスクの作成と実行")



    System_Boundary(fs, "Local/Git File System (Passive SSOT)") {

        Container(design, "Design Docs", "reqs/design/", "ADR, Design Docs (Markdown + Metadata)")

        Container(tasks, "Task Drafts", "reqs/tasks/<ADR-ID>/", "Reservation tickets for Issues")

        Container(archive, "Task Archive", "reqs/tasks/_archive/", "History of processed tasks")

    }



    System_Boundary(gh, "GitHub Environment (Active SSOT)") {

        Container(issues, "GitHub Issues", "L1/L2/L3 Issues", "The actual source of truth for execution")

        Container(actions, "GitHub Actions", "Workflows", "Automation runtime")

    }



    Container(ick, "ick CLI", "src/issue_creator_kit/", "Metadata parser and lifecycle engine")



    Rel(actor, design, "Write/Review", "Git")

    Rel(actor, tasks, "Draft", "Git")

    Rel(ick, design, "Parse metadata/status", "File I/O")

    Rel(ick, tasks, "Parse depends_on/status", "File I/O")

    Rel(ick, archive, "Move files (Archive)", "File I/O")

    Rel(ick, issues, "Create/Update/Sync", "REST API")

    Rel(actions, ick, "Execute", "CLI")



    UpdateElementStyle(ick, $backgroundColor="#336699", $textColor="white")

```



### Logical Dependency (DAG) Conceptual View

```mermaid

graph TD

    subgraph ADR_007 [ADR-007 Container]

        T1[007-T1: Fact Scouting]

        T2[007-T2: Arch Drafting]

        T3[007-T3: Spec Drafting]

        T1 --> T2

        T1 --> T3

    end

    style ADR_007 fill:#f9f,stroke:#333,stroke-width:2px

```



## Invisible SSOT: File vs Issue Mapping

本プロジェクトの核心的な設計思想である「不可視のファイルベースSSOT」を以下の図で定義します。



```mermaid

graph LR

    subgraph Local ["Local / Git (Passive)"]

        F1["Task File (007-T1.md)"]

        F2["Task File (007-T2.md)"]

    end



    subgraph GitHub ["GitHub (Active)"]

        I1["Issue #101 (Fact Scouting)"]

        I2["Issue #102 (Arch Drafting)"]

    end



    F1 -- "Issuance (Move to _archive)" --> I1

    I1 -- "Execution (Active SSOT)" --> I1

    

    F2 -- "Depends on" --> I1

    F2 -- "Issuance" --> I2

    

    linkStyle 0,3 stroke:#336699,stroke-width:4px;

```

- **Local Files:** 「予約票（Reservation Ticket）」および「履歴の控え」として機能。

- **GitHub Issues:** 実作業における「唯一の正解（Active SSOT）」。



## Element Definitions (SSOT)



### reqs/design/ (Design Storage)

- **Type:** `Container`

- **Code Mapping:** `reqs/design/`

- **Role (Domain-Centric):** システムの意思決定（ADR）と詳細設計（Design Doc）を永続化する「設計の正解」。

- **Layer (Clean Arch):** `Domain (Policy)`

- **Dependencies:**

  - **Upstream:** `Architect (Human)`, `ick CLI`

  - **Downstream:** `reqs/tasks/`

- **Tech Stack:** Markdown, YAML Frontmatter

- **Data Reliability:** Sync (Git managed). Status field manages lifecycle (`Draft`, `Approved`).

- **Trade-off:** 物理フォルダを `_inbox`, `_approved`, `_archive` の3つに限定することで、検索性を高める代わりに、詳細なカテゴリ分けはメタデータ（`tags` 等）に委ねている。



### reqs/tasks/ (Task Reservoir)

- **Type:** `Container`

- **Code Mapping:** `reqs/tasks/`

- **Role (Domain-Centric):** 起票待ちのタスク案（予約票）および起票済みタスクの控え。

- **Layer (Clean Arch):** `Use Cases (Execution Plan)`

- **Dependencies:**

  - **Upstream:** `reqs/design/`

  - **Downstream:** `GitHub Issues`

- **Tech Stack:** Markdown, YAML Frontmatter

- **Data Reliability:** `ick CLI` による移動（Atomic Move）により、重複起票を防止。

- **Trade-off:** 物理ファイルをアーカイブとして残すことで、GitHub がダウンしても設計意図とタスクの履歴を Git 上で追跡可能にしている。



### ick CLI (Lifecycle Engine)

- **Type:** `Container`

- **Code Mapping:** `src/issue_creator_kit/`

- **Role (Domain-Centric):** メタデータを解析し、有向非巡回グラフ（DAG）に基づいてタスクの起票・移動・同期を統制する。

- **Layer (Clean Arch):** `Interface Adapters`

- **Dependencies:**

  - **Upstream:** `GitHub Actions`

  - **Downstream:** `FileSystem`, `GitHub API`

- **Tech Stack:** Python, `uv`, `PyYAML`

- **Data Reliability:** 冪等性を担保。起票成功時のみ物理ファイルを `_archive/` へ移動させる。
