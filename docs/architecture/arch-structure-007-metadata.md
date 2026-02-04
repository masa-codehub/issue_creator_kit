# ADR-007 Metadata-Driven Structure

## Context
- **Bounded Context:** Lifecycle & Task Management
- **System Purpose:** ADR-003 での物理階層による管理の限界を克服し、メタデータ（YAML Frontmatter）によってドキュメントとタスクのライフサイクルを自律的に管理するフラットな構造を実現する。

## Diagram (C4 Container)
```mermaid
graph TD
    subgraph "reqs/ (File-based SSOT)"
        D_IN["design/_inbox/ (Drafts)"]
        D_APP["design/_approved/ (SSOT)"]
        D_ARC["design/_archive/ (History)"]
        T_ADR["tasks/<ADR-ID>/ (Pending)"]
        T_ARC["tasks/_archive/ (Issued)"]
    end

    subgraph "GitHub (Frontend)"
        ISS_L1["L1: ADR Issue"]
        ISS_L2["L2: Integration Issue"]
        ISS_L3["L3: Task Issue"]
    end

    subgraph "Issue Creator Kit (CLI)"
        CLI["CLI Tool (process-diff/workflow)"]
    end

    D_IN -- "Draft/Approved" --> CLI
    CLI -- "Move to _approved" --> D_APP
    CLI -- "Create L1/L2 Issues" --> ISS_L1
    CLI -- "Create L1/L2 Issues" --> ISS_L2
    
    T_ADR -- "Metadata: Draft/Ready" --> CLI
    CLI -- "Move to _archive & Set issue_id" --> T_ARC
    CLI -- "Create L3 Issue" --> ISS_L3

    ISS_L3 -- "Merged/Closed" --> CLI
    CLI -- "Trigger Next Task (Ready)" --> T_ADR
```

## Element Definitions (SSOT)

### File-based SSOT (reqs/)
- **Type:** `Boundary`
- **Code Mapping:** `reqs/`
- **Role (Domain-Centric):** 全ての設計意図（ADR）と作業予約（Task Draft）の永続化層。
- **Layer (Clean Arch):** Infrastructure (External State)
- **Trade-off:** 物理階層をフラットにすることで、認知負荷を下げつつ、メタデータによる複雑な依存管理を許容する。

### Metadata-Driven CLI
- **Type:** `Component`
- **Code Mapping:** `src/issue_creator_kit/`
- **Role (Domain-Centric):** ファイルのメタデータを解析し、GitHub Issue の状態と同期させる「ライフサイクル・オーケストレーター」。
- **Layer (Clean Arch):** Use Cases
- **Tech Stack:** Python 3.13, GitHub API (PyGithub/gh cli)

### 3-Layer Hybrid Management
- **Type:** `Boundary`
- **Role (Domain-Centric):** 
    - **L1 (ADR):** 戦略的目標。
    - **L2 (Phase):** 戦術的マイルストーン。
    - **L3 (Task):** 実装アクション。
- **Data Reliability:** 結果整合性。GitHub Issue の起票が成功した後に、ローカルファイルをアーカイブ（移動）することで、不整合を防ぐ。
