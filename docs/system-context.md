# システムコンテキスト: Issue Creator Kit

このドキュメントは、システムの全体像、境界、および主要な依存関係を定義する、プロジェクトの Single Source of Truth (SSOT) です。

- **Status**: 承認済み
- **Last Updated**: 2025-12-27

## 1. ビジネスコンテキストとアウトカム
GitHubを用いたソフトウェア開発において、アーキテクチャ設計（ADR/Design Doc）から実装タスク（Issue）への落とし込みは、手動作業によるコストと「設計と実装の乖離」を生む主要な要因となっている。

本システム（Issue Creator Kit）は、これらのプロセスを「Markdownファイルベース」で自動化するツールキットを提供することで、以下の価値を実現する。
- **一貫性の保証**: 承認された設計のみが実装タスク化されるフローを強制する。
- **管理コストの削減**: Issueの起票、親子関係の設定、ドキュメントのステータス更新を自動化する。
- **導入の迅速化**: 複雑なGitHub Actionsワークフローを、コマンド一つで既存リポジトリに展開可能にする。

## 2. 主要なユビキタス言語 (Ubiquitous Language Core)
| 用語 | 定義 | 備考 |
| :--- | :--- | :--- |
| **Inbox (インボックス)** | 提案段階のドキュメントやIssue案が配置される場所。 | `reqs/_inbox/` など |
| **Approve (承認済み)** | 合意形成されたドキュメントの保管場所。 | `reqs/_approve/` |
| **Draft Issue (Issue案)** | Issueとして起票される前のMarkdownファイル。 | `Depends-On` メタデータを持つ |
| **Archive (アーカイブ)** | 処理が完了した（マージ済みのADRや、起票済みのIssue案）の保管場所。 | `reqs/_issues/created/` など |
| **Kit (キット)** | CLI、自動化スクリプト、ワークフロー定義の総称。 | |

## 3. システムの境界と責務 (System Boundary)

### 3.1 スコープ内 (In-Scope)
- **ワークフローの展開**: 推奨されるディレクトリ構造とGitHub Actions設定をデプロイする。
- **ドキュメント承認管理**: mainブランチへのマージを検知し、ファイルの移動とステータス更新を自動化する。
- **依存関係の解決とIssue起票**: Markdown内のメタデータを解析し、トポロジカルソートを用いて正しい順序でGitHub Issueを起票する。

### 3.2 スコープ外 (Out-of-Scope)
- **コード生成**: 設計ドキュメントから直接ソースコードのボイラープレートを生成する機能は現時点では含まない。
- **エディタ機能**: ドキュメントの執筆そのものは外部ツール（VS Code等）に依存する。

## 4. アクターと外部システム (Actors & External Systems)

### 4.1 アクター (ユーザー・エージェント)
| アクター名 | 役割 / 目的 |
| :--- | :--- |
| **Architect (Human)** | 高レベルな設計（ADR/Design Doc）を作成・承認し、ビジネス価値を定義する。 |
| **AI Agent** | 承認された設計を解析し、依存関係（`Depends-On`）を含む Draft Issue へ分解・作成する。 |
| **Developer (Human/Agent)** | 自動起票されたIssueと紐づいた設計ドキュメントを参照して実装を行う。 |

### 4.2 外部システム
| システム名 | 連携内容 / プロトコル |
| :--- | :--- |
| **GitHub Actions** | 本システムを実行するオートメーションランタイム。 |
| **GitHub REST API** | Issue作成、PR操作のための公式インターフェース。 |

## 5. アーキテクチャ図 (C4 Model - System Context)

```mermaid
C4Context
    title System Context diagram for Issue Creator Kit
    
    Person(arch, "Architect", "設計とタスクの定義")
    System(ick, "Issue Creator Kit", "ドキュメント移動・Issue起票の自動化")
    System_Ext(github, "GitHub (API/Actions)", "リポジトリ管理・自動化実行")

    Rel(arch, github, "設計/Issue案をプッシュ", "Git/HTTPS")
    Rel(github, ick, "ワークフローを起動", "Webhook")
    Rel(ick, github, "Issue作成・ファイル移動", "REST API/Git")

## 6. 戦略的トレードオフと 4 大リスク
- **[標準化 vs 柔軟性]**: 本システムは特定のディレクトリ構造（`reqs/`）を前提とすることで、複雑な設定なしに高度な自動化を実現する。ユーザーには構造への適応を求める。
- **[ファイルベースのSSOT]**: GitHub上のファイルが常に真実であり、Issueはそこから派生する。Issueを直接編集してもファイルには反映されないという制約を、開発プロセスの「一方通行性（一貫性）」として受け入れる。
- **[最大のリスク]**: GitHub APIのレート制限や認証トークンの権限不足。これを防ぐため、最小権限（Least Privilege）での運用ガイドラインを確立する。

## 7. 設計原則とデータ信頼性 (Design Principles & Kleppmann's View)
- **Zero Configuration**: `init` コマンドで即座に動作環境が整い、ユーザーにYAMLの記述を強いない。
- **Idempotency (冪等性)**: 同じ処理が複数回実行されても、同じ結果（重複Issueの回避など）が得られるよう設計する。
- **Fail-Fast Reliability**: APIレート制限の不足や依存関係の不整合（循環参照）を検知した場合、中途半端な状態更新を避け、処理を1件も実行せずに安全に停止する。
- **Dependency First**: タスクは依存先が解決されない限り起票されない。これにより、不完全なタスクがバックログに溢れるのを防ぐ。
- **Human in the Loop**: 自動化は常にプルリクエストやブランチ移動という「人間によるマージ」の後に発生し、意図しない破壊的な変更を防ぐ。