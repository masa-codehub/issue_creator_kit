# 概要 / Summary

[ADR-010] Task Activation & Issue ID Propagation: タスクの自動起票と ID 伝播ロジック

- **Status**: 提案中
- **Date**: 2026-02-06

## 状況 / Context

ADR (L1) に紐づく具体的な実装タスク (L2/L3) の自動起票を実現する必要がある。同一 PR 内で複数のタスクが一度にマージされる場合、先行タスクの Issue 番号が確定するまで後続タスクが起票できない「解決待ち」のデッドロックを解消しなければならない。

## 決定 / Decision

一時 ID を用いた順序解決と、起票成功時の「Issue 番号伝播（Propagation）」方式を導入する。

### 1. ID の二段構え管理

- **起票前**: エージェントは意味のある slug 等の一時 ID を付与し、`depends_on` を記述する。
- **起票後**: GitHub から発行された「Issue 番号」を唯一の正の ID とする。

### 2. 起票・伝播サイクル (Issue ID Propagation)

- **逐次起票**: 準備が整ったタスク（一時 ID または Issue 番号で依存が解決されているもの）から順に起票する。
- **即時アーカイブ**: 起票成功時、即座にファイルを `_archive/` へ移動し、`adr-xxx-Issue番号-slug.md` とリネームして履歴を固定する。
- **物理置換 (Rewrite)**: 起票したタスクの「一時 ID」を、残りのドラフトファイル内の `depends_on` 記述から「GitHub 番号 (#xxx)」へ物理的に書き換える。

## 検討した代替案 / Alternatives Considered

- **案A: 親の起票を待って PR を分ける**: 開発スピードが著しく低下するため却下。同一 PR 内で一括処理できる必要がある。

## 結果 / Consequences

### メリット (Positive consequences)

- **Safety**: 状態（番号）がファイルに物理的に書き込まれるため、処理が中断しても確実に続きから再開できる。
- **Uniqueness**: GitHub 番号を ID に採用することで、ID の重複や競合を物理的に排除できる。

### デメリット (Negative consequences)

- **File Mutation**: 起票プロセス中に手元のファイルが書き換わる副作用が発生するが、これは不整合を防ぐための意図的な設計である。

## 検証基準 / Verification Criteria

- [ ] T1, T2（T2 depends on T1）を同時にマージした際、T1 が起票され、T2 の中身が `#番号` に書き換わってから T2 が起票されること。
- [ ] `_archive/` 内のファイル名が Issue 番号を含む形式になっていること。

## 実装状況 / Implementation Status

未着手
