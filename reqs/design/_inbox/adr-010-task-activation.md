---
id: adr-010
title: "Task Activation & Issue ID Propagation"
status: Draft
date: 2026-02-06
---

# ADR-010: Task Activation & Issue ID Propagation

## Context
ADR の下に紐づく具体的な実装タスク (L2/L3) の自動起票と、一時 ID から GitHub 番号への移行を実現する。

## Decision
`reqs/tasks/` 内のタスク案を自動起票し、確定した番号を残りのファイルへ伝播させる。

### 1. タスク自動起票
- `reqs/tasks/adr-xxx/` 配下のファイルを L2/L3 Issue として起票する。

### 2. Issue番号伝播 (Propagation)
- **サイクル**: 1つ起票 → GitHub 番号取得 → 残りのドラフトファイル内の `depends_on` を一時IDから GitHub 番号へ置換。
- **アーカイブ**: 起票成功時、ファイルを `_archive/` へ移動し、名前を `adr-xxx-Issue番号-slug.md` にリネームする。

## Consequences
- **Positive**: 同一PR内での複雑な依存関係が、GitHub 側の起票を待たずに物理置換によって解決される。
- **Negative**: 一時的なファイル書き換えが発生するため、起票プロセス中の並列実行に注意が必要。
