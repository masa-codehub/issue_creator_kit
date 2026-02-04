# Task Document Lifecycle (ADR-003)

> **DEPRECATED: This document is based on ADR-003 and has been superseded by the new architecture defined in ADR-007.**
> Please refer to the new architecture documents, such as `arch-structure-007-metadata.md` and `arch-state-007-lifecycle.md`.

## Subject Definition
ADR-003 で導入された「仮想キュー」と「自己推進型ワークフロー」に基づく、タスク ドキュメント（Markdown ファイル）のライフサイクルを定義します。
- **Target Object:** Task Document (`reqs/tasks/**/*.md`)
- **Persistence:** `File System (reqs/tasks/)`
- **Concurrency Strategy:** Git Push/Merge (Conflict detection by Git)
