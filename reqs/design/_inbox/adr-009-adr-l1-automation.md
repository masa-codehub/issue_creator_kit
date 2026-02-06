---
id: adr-009
title: "ADR L1 Automation & Glue Labels"
status: Draft
date: 2026-02-06
---

# ADR-009: ADR L1 Automation & Glue Labels

## Context
ADR-008 で整理された基盤の上に、設計ドキュメント（ADR）の自動起票機能を再構築する。

## Decision
`reqs/design/_approved/` に配置された ADR ファイルを L1 Issue として自動起票する。

### 1. ADR 自動起票
- マージされた ADR ファイルを検知し、L1 Issue を作成する。
- **検索ベースの冪等性**: 起票前に GitHub API で `label:adr:xxx label:L1` を検索し、既に存在する場合は二重起票をスキップする。

### 2. 接着剤ラベル (Glue Labels)
- **ADR識別ラベル**: `adr:xxx` を自動生成し、L1 Issue に付与する。
- **階層ラベル**: `L1` を付与。
- **自動作成**: 必要なラベルが GitHub 上にない場合はツールが自動作成する。

## Consequences
- **Positive**: 設計の承認と GitHub 上の管理 Issue が自動的に同期される。
- **Negative**: ラベル検索のため GitHub API の呼び出し回数がわずかに増加する。
