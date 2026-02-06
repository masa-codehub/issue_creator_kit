---
id: adr-012
title: "Gemini Relay (Auto-Pilot)"
status: Draft
date: 2026-02-06
---

# ADR-012: Gemini Relay (Auto-Pilot)

## Context
すべての準備が整った Issue 群に対し、イベント駆動による自律的なリレー実行を導入する。Actions の不調等による「詰まり」を解消するためのリカバリ手段も必要である。

## Decision
起動ラベル `gemini` への統合と、Actions およびコマンドによる自律リレーと自己修復を実装する。

### 1. 起動ラベル `gemini` への統合
- 既存の `gemini-handler.yml` 等を、`gemini` ラベルを唯一の起動トリガーとするように修正する。
- 役割（`AGENT_ROLE`）は、静的な属性ラベル（`arch`/`spec`/`tdd`）から決定する。

### 2. Gemini Relay アクション
- **Trigger**: Issue `closed`
- **Logic**: 
  - クローズされた Issue を依存先に持つ後続 Issue を検索。
  - 後続 Issue の本文内チェックリスト（ADR-011で挿入）を `[x]` に更新。
  - 全チェックが完了した Issue に `gemini` ラベルを付与する。

### 3. 自己修復（Sync）コマンド
- **内容**: `ick sync-relay` コマンドの実装。
- **機能**: GitHub 上の全 Issue 状態（Open/Closed）をスキャンし、チェックリストの更新漏れや `gemini` タグの貼り漏れを「あるべき状態」へ一括修正（収束）させる。
- **目的**: Actions の失敗や手動操作によるパイプラインの停止を、コマンド一つで復旧可能にする。

## Consequences
- **Positive**: 人間の介入なしにエージェントが自律的にタスクを消化し続け、かつ運用上の信頼性が担保される。
- **Negative**: リレーの連鎖状況を監視するコストがわずかに発生する。
