# 概要 / Summary
[ADR-011] Context & Metadata Integration: 実行リレーのための情報統合

- **Status**: 提案中
- **Date**: 2026-02-06

## 状況 / Context
GitHub 上でエージェントを自律的に動かすためには、作成された Issue に「誰がやるべきか（役割）」と「誰を待っているか（進捗）」の情報が機械可読な形で埋め込まれている必要がある。

## 決定 / Decision
Issue 本文へのチェックリスト挿入と、静的属性ラベルによる役割の明文化を行う。

### 1. 依存チェックリストの自動挿入
- **内容**: `issue-kit` が起票時、Issue 本文末尾に `- [ ] #111` 形式の依存先 Issue 番号リストを挿入する。
- **目的**: 後の Actions がこのリストを更新（チェック入れ）することで、依存関係の進捗を Issue 自身に集約させる。

### 2. 静的属性ラベルの付与
- **役割ラベル**: タスクの性質に応じて `arch`, `spec`, `tdd` ラベルを付与する。
- **接着剤の波及**: 親の ADR ラベル (`adr:xxx`) および階層ラベル (`L2`, `L3`) を付与し、GitHub 上での管理構造を完成させる。

## 検討した代替案 / Alternatives Considered
- **案A: フロントマターをそのまま本文に載せる**: 人間にとって見づらく、Actions でのパースや部分更新が複雑になるため却下。専用のチェックリスト形式が最適。

## 結果 / Consequences

### メリット (Positive consequences)
- **Feasibility**: Issue を見るだけで、現在のブロック状況（あと誰待ちか）が人・機械の両方から一目瞭然になる。
- **Automation**: リレー Actions (ADR-012) が動作するための完全な「材料」が揃う。

### デメリット (Negative consequences)
- **Complexity**: `issue-kit` の起票ロジックにおいて、Issue 本文の組み立て（文字列操作）の責任が増大する。

## 検証基準 / Verification Criteria
- [ ] 起票された Issue の本文末尾に、正しい依存先番号を含むチェックリストが表示されていること。
- [ ] `arch`/`spec`/`tdd` 等の分類ラベルが正しく付与されていること。

## 実装状況 / Implementation Status
未着手
