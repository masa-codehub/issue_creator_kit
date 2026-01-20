# Architecture to Spec Handoff (ADR-002)

## 概要 (Overview)
本ドキュメントは、Architecture Phase (ADR-002 Visualization) から Specification Phase への引継ぎ事項をまとめたものである。
後続の Spec Strategist および Developer は、以下のアーキテクチャ意図を遵守して詳細設計（Spec）と実装を行うこと。

## 1. アーキテクチャ原則の遵守 (Architectural Principles)

### 1.1. Clean Architecture Lite の厳格な適用
- **Structure Diagram** (`docs/architecture/arch-structure-issue-kit.md`) に示された依存方向（CLI -> Usecase -> Domain <- Infrastructure）を厳守すること。
- **禁止事項**:
    - `usecase` 層から `infrastructure` の具象クラス（`GitHubAdapter` など）を直接 import してはならない。必ず Interface (Protocol) または DI されたインスタンスを使用すること。
    - `domain` 層が外部ライブラリ（`PyGithub` や `GitPython`）に依存してはならない。

### 1.2. テスト容易性の確保
- **DI (Dependency Injection)**: `cli.py` で Adapter を生成し、Usecase に注入する構造を維持すること。これにより、ユニットテスト時に Mock Adapter への差し替えが可能となる。
- **Pure Logic**: Usecase 内の条件分岐（`if status == "approved"` 等）は、外部IOから分離してテスト可能な状態に保つこと。

## 2. 振る舞いとデータ整合性 (Behavior & Consistency)

### 2.1. 承認フローの順序 (Sequence)
- **Behavior Diagram** (`docs/architecture/arch-behavior-approval-flow.md`) の順序を遵守すること。
    1. **Metadata Update (Inbox)**: まず `_inbox` 内で `Status` を更新し、ファイルシステムの変更を確定させる。
    2. **Move File**: `_inbox` から `_approved` へ移動する。
    3. **Create Issue**: ここで初めて GitHub API をコールする。
    4. **Link Issue**: 起票された Issue ID を `_approved` 内のファイルに追記する。
- **理由**: API コールが失敗した場合でも、ファイルシステム上の変更をロールバック（または手動復旧）しやすくするため、不可逆な操作（Git Commit）を最後に配置している。

### 2.2. 一括コミット戦略 (Bulk Commit)
- 個別のファイルごとに `git commit` を発行せず、全ての処理が完了した後に **1回だけ** `git add .` && `git commit` を行うこと。
- これにより、CI の実行時間を短縮し、Git 履歴をクリーンに保つ。

## 3. ライフサイクル定義 (Lifecycle)
- **State Diagram** (`docs/architecture/arch-state-doc-lifecycle.md`) に従い、`_approved` 配下のファイルは「不変（Immutable）」に近い扱いとすること。
- 自動化ツール以外が `_approved` 内のファイルを直接変更することを（運用上）禁止または抑制するロジックを検討すること。

## 4. 残存課題・申し送り (Open Issues)
- **ロールバックロジック**: `arch-behavior-approval-flow.md` に記載の「Failure Scenarios」におけるロールバック処理（エラー時にファイルを `_inbox` に戻す等）は、実装難易度が高いため、Spec 作成時に「どこまで自動化し、どこから手動リカバリとするか」を明確に定義すること。
