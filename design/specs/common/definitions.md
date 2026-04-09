# Common Definitions (ADR-017)

このドキュメントは、システム全体で共有される共通の用語定義、列挙型（Enum）、およびデータ制約を定義する。

## 1. Document Lifecycle Status

### 1.1. ADR/DesignDoc Status

<!-- guardrail-sync: ADR.status -->

| Status        | Description                                   |
| :------------ | :-------------------------------------------- |
| `Draft`       | ドラフト作成中。                              |
| `Approved`    | 承認済み、実装可能。                          |
| `Postponed`   | 保留中。                                      |
| `Superseded`  | 後続の ADR 等により置き換えられた（非推奨）。 |
| `Implemented` | 実装および監査が完了し、アーカイブされた。    |

### 1.2. Task Status

<!-- guardrail-sync: Task.status -->

| Status      | Description                          |
| :---------- | :----------------------------------- |
| `Draft`     | タスクのドラフト段階。               |
| `Ready`     | 依存関係が解消され、起票可能な状態。 |
| `Issued`    | GitHub Issue が起票された状態。      |
| `Completed` | 実装・マージが完了した状態。         |
| `Cancelled` | キャンセルされた状態。               |

## 2. Roles & Phases

### 2.1. Roles

- `arch`: Architecture (System Architect)
- `spec`: Specification (Technical Designer)
- `implement`: Implementation (Coder)

### 2.2. Phases

- `arch`: アーキテクチャ設計。
- `spec`: 詳細設計。
- `implement`: 実装（Implement）。
