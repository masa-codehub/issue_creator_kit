# Architecture Planning: Document Approval Flow (ADR-002)

## 1. 概要 / Overview
ADR-002 で決定された「ドキュメント承認フローとライフサイクル管理の自動化」を可視化するための戦略。
Clean Architecture Lite に基づく内部構造と、GitHub Actions を介した動的な承認プロセスを明確にする。

## 2. ユビキタス言語 / Ubiquitous Language
- **Inbox (`_inbox`):** 承認待ちのドキュメントが配置される場所。
- **Approved (`_approved`):** 承認済み（マージ済み）のドキュメントが公式に保管される場所。
- **Tracking Issue:** 承認されたドキュメントの「実装」を追跡するために自動起票される GitHub Issue。
- **Adapter (Infrastructure):** Git や GitHub API などの外部 IO を抽象化した部品。
- **Workflow (Usecase):** 承認プロセス全体の順序制御。

## 3. 境界と責任 (Boundaries & Responsibilities)
- **CLI Layer:** コマンド入力を受け取り、Usecase をキックする。
- **Usecase Layer:** ビジネスルール（「ファイルを移動する」「ステータスを書き換える」「Issueを立てる」）の順序を制御する。
- **Domain Layer:** `Document` エンティティ。メタデータ（Status, Date, Issue番号）の保持。
- **Infrastructure Layer:** 実際のファイル移動、Git コミット、GitHub API 呼び出しの実行。

## 4. 作図戦略 (Diagram Strategy)
以下の 3 つの図を作成し、`docs/architecture/` に配置する。

| 図の種類 | ファイル名 | 目的 |
| :--- | :--- | :--- |
| **C4 Container** | `arch-structure-issue-kit.md` | Clean Architecture Lite に基づくパッケージ構成と依存方向。 |
| **Sequence** | `arch-behavior-approval-flow.md` | GitHub Actions からのトリガー、Usecase による順序制御、Infrastructure の IO。 |
| **State** | `arch-state-doc-lifecycle.md` | ドキュメントの Status (`Draft` -> `In Review` -> `Approved`) と物理配置の遷移。 |

## 5. 技術選定と規約
- **Diagram Tool:** Mermaid.js
- **Architecture Style:** Clean Architecture (Dependency Inversion)
- **Output Path:** `docs/architecture/`
- **Reference:** `reqs/design/_archive/adr-002-document-approval-flow.md`
