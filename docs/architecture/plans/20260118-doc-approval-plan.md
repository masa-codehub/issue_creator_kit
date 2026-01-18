# Architecture Visualization Plan: Document Approval Flow (ADR-002)

- **Status**: Draft
- **Author**: SYSTEM_ARCHITECT
- **Source ADR**: `reqs/design/_archive/adr-002-document-approval-flow.md`

## 1. コンテキストと目的 (Context & Objective)
- **Objective:** ADR-002 で決定された「ドキュメント承認フローの自動化」のアーキテクチャを可視化する。特に「Clean Architecture Lite」による責務分離と、GitHub Actions を介した動的なフローを開発者が理解できるようにする。
- **Key Decision:**
    - ロジックを Python スクリプト (`src/issue_creator_kit/`) に集約し、YAML は最小限にする。
    - CLI, Usecase, Domain, Infrastructure の 4 層に分離し、依存性逆転原則を適用する。

## 2. 参照したSSOT一覧 (SSOT Audit Log)
- [x] `reqs/design/_archive/adr-002-document-approval-flow.md`
- [x] `docs/system-context.md`
- [x] `src/issue_creator_kit/` (Source Code Structure)

## 3. 共通定義とマッピング (Common Definitions & Mapping)

### 3.1. ユビキタス言語 (Ubiquitous Language)
| 用語 (Term) | 定義 (Definition) | コード上の表現 (Class/Variable) |
| :--- | :--- | :--- |
| **Inbox** | 承認待ちドキュメントの置き場 | `reqs/design/_inbox/` (Path) |
| **Approved** | 承認済みドキュメントの保管場所 | `reqs/design/_approved/` (Path) |
| **Adapter** | 外部システムとのIOを担うクラス | `infrastructure.*_adapter.py` |
| **Workflow** | 承認プロセス全体の制御を行うクラス | `usecase.workflow.Workflow` (想定) |

### 3.2. レイヤーとコンポーネント (Layers & Components)
| レイヤー名 | 責務 (Responsibility) | 具体的なディレクトリ/ファイル (Physical Path) | 禁止事項 (Anti-Pattern) |
| :--- | :--- | :--- | :--- |
| **CLI Layer** | ユーザー入力の受付とDI構成 | `src/issue_creator_kit/cli.py` | ビジネスロジックの実装 |
| **Usecase Layer** | ビジネスルールと順序制御 | `src/issue_creator_kit/usecase/*.py` | `infrastructure` への直接依存 (Interface経由ならOK) |
| **Domain Layer** | データ構造と純粋なロジック | `src/issue_creator_kit/domain/*.py` | 外部ライブラリへの依存 |
| **Infrastructure Layer** | 外部API/Git/FS操作の実装 | `src/issue_creator_kit/infrastructure/*.py` | ドメインルールの実装 |

## 4. 作図戦略 (Diagram Strategy)

| 図の種類 (Type) | ファイル名 (File Name) | 描く範囲 (Scope/Boundary) | 目的・伝えたいこと (Intent) |
| :--- | :--- | :--- | :--- |
| **C4 Container** | `arch-structure-issue-kit.md` | `src/issue_creator_kit/` 全体 | パッケージ構成と「Clean Architecture Lite」の依存方向（外から内へ）を可視化する。 |
| **Sequence** | `arch-behavior-approval-flow.md` | GitHub Actions トリガーからコミット完了まで | 外部イベント駆動でシステムがどう動くか、特に `Workflow` Usecase がどう `Adapter` を利用するかを示す。 |
| **State** | `arch-state-doc-lifecycle.md` | ドキュメントファイルのライフサイクル | マージ前後でファイルの「ステータス」と「場所」がどう変化するかを定義する。 |

## 5. 技術選定 (Technical Decisions)
- **Diagram Tool:** Mermaid.js
- **Style:** Clean Architecture Lite (ADR-002準拠)