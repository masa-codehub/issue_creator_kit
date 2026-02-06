---
id: adr-011
title: "Context & Metadata Integration"
status: Draft
date: 2026-02-06
---

# ADR-011: Context & Metadata Integration

## Context
起票された Issue に、リレー実行や管理に必要な付加情報を統合する。

## Decision
Issue 本文へのチェックリスト挿入と、静的ラベルによる役割の明文化を行う。

### 1. 依存チェックリストの自動挿入
- `issue-kit` が起票時、Issue 本文末尾に `- [ ] #111` 形式の機械可読なチェックリストを自動挿入する。

### 2. 静的属性ラベルの付与
- タスクの性質に応じて `arch`, `spec`, `tdd` ラベルを付与する。
- 接着剤ラベル (`adr:xxx`) を L2/L3 にも波及させ、階層（`L2`, `L3`）ラベルを付与する。

## Consequences
- **Positive**: 実行リレーに必要な「材料」が Issue 上に出揃う。
- **Negative**: Issue 本文がツールによって自動更新されるため、フォーマットの不変性が求められる。
