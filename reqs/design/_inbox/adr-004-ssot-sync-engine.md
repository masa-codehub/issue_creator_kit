# 概要 / Summary
[ADR-004] タイトル: ドキュメントとGitHub Issueの自動同期 (SSOT同期エンジン)

- **Status**: 提案中
- **Date**: 2026-01-01

## 状況 / Context
現在、Issue Creator Kit (ICK) はドキュメントが `_inbox` から `_approved` へ移動（承認）される際に一度だけ GitHub Issue を作成する。
しかし、承認後のドキュメント（ADR/Design Doc）が修正された場合、その変更内容は GitHub Issue の本文には反映されない。
これにより、「ドキュメント（Git上のファイル）」と「GitHub Issue（トラッキング用）」の間で内容の乖離（情報の断絶）が発生し、Single Source of Truth (SSOT) としての信頼性が損なわれる課題がある。

## 決定 / Decision
ドキュメントの内容と GitHub Issue を常に同期させる「SSOT同期エンジン」を実装する。

### 1. 同期ロジックの改善 (Upsert化)
`ApprovalUseCase` のロジックを「作成のみ」から「作成または更新（Upsert）」へ拡張する。
- **検索**: ファイル内のメタデータから `Issue: #XXX` の有無を確認。
- **更新 (Update)**: 既に Issue 番号が存在する場合、ドキュメントの最新の本文を GitHub API を使用してその Issue に転記（上書き）する。
- **作成 (Create)**: Issue 番号が存在しない場合（新規承認時）、Issue を作成し、番号をドキュメントに追記する。

### 2. コンテンツの完全転記
Issue の本文（Body）には、ADR ドキュメントの Markdown 内容をそのまま転記する。これにより、GitHub 上で設計内容を直接確認可能にする。

### 3. トリガーの拡張
`auto-approve-docs` ワークフローの監視対象に `reqs/design/_approved/**` を追加する。
承認済みのドキュメントに対する変更が `main` ブランチにマージされた際にも同期ロジックが走り、常に Issue が最新化されるようにする。

## 検討した代替案 / Alternatives Considered
- **案A: Issue作成のみを維持し、手動更新とする**
    - 乖離を許容する案。SSOT を維持できないため、大規模な開発や AI エージェントによる開発において致命的な混乱を招くリスクがある。
- **案B: GitHub Issue を主とし、ファイルを従とする**
    - 現在の「ファイルベースのSSOT」原則に反するため却下。

## 結果 / Consequences

### 4大リスク評価結果
- **[価値: 高]**: ドキュメントと Issue の乖離がなくなり、開発者は常に GitHub 上で最新の設計意思決定を参照できる。AI エージェントも Issue を通じて正しい設計を読み取ることが可能になる。
- **[実現可能性: 高]**: `GitHubAdapter` に `update_issue` メソッドを追加し、UseCase を微修正することで実現可能。
- **[ユーザビリティ: 高]**: ユーザーは Git 上のファイルを修正してマージするだけでよく、Issue の更新作業を意識する必要がない。
- **[ビジネス生存性: 高]**: 設計意思決定が GitHub のメタデータとして検索可能になり、ナレッジの蓄積が強化される。

### メリット (Positive consequences)
- 設計と実装の乖離を最小限に抑えられる。
- ドキュメントの変更履歴が GitHub Issue のコメント履歴や更新履歴としても間接的に追跡しやすくなる。

### デメリット (Negative consequences)
- GitHub API の呼び出し回数が増加する。
- 頻繁な修正により Issue の更新ログが溢れる可能性があるが、履歴管理の観点からは許容範囲内。

## 検証基準 / Verification Criteria
- `_approved` 内のドキュメントを修正して `main` にマージした際、対応する GitHub Issue の本文が自動で更新されること。
- Issue 番号がない新規ファイルの場合、正しく Issue が作成され、番号がドキュメントに追記されること。
- ドキュメント内のメタデータ以外の本文が、Issue 本文と一致していること。

## 実装状況 / Implementation Status
未着手
