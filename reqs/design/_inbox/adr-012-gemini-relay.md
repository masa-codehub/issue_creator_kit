# 概要 / Summary

[ADR-012] Gemini Relay (Auto-Pilot): イベント駆動による自律実行リレー

- **Status**: 提案中
- **Date**: 2026-02-06

## 状況 / Context

全ての準備が整った Issue 群に対し、人間が手動でラベルを貼ることなく、先行タスクの完了（Closed）に合わせて後続タスクが自動的に動き出す「オートパイロット」状態を実現したい。

## 決定 / Decision

起動ラベル `gemini` への統合と、Actions によるクローズ検知リレー、および自己修復機能を導入する。

### 1. 起動ラベル `gemini` への統合

- **トリガー**: `gemini` ラベルのみを起動トリガーとする。
- **役割決定**: 既存の `gemini-handler.yml` 等を、属性ラベル (`arch`/`spec`/`tdd`) を見て `AGENT_ROLE` を切り替えるロジックに修正する。

### 2. Gemini Relay (タグ・リレー)

- **Trigger**: Issue `closed` イベント。
- **Logic**:
  - クローズされた Issue を依存先に持つ後続 Issue を検索。
  - 後続 Issue の本文内チェックリストを `[x] #先行番号` に更新する。
  - **すべてのチェックが埋まった瞬間** に、その Issue に `gemini` ラベルを付与し、エージェントを「着火」させる。

### 3. 自己修復（Sync）コマンドの用意

- **機能**: `ick sync-relay` コマンドの実装。
- **役割**: GitHub 上の状態を全走査し、Actions の不調等で漏れたチェックリスト更新やタグ付けを一括で「あるべき状態」へ収束させる。

## 検討した代替案 / Alternatives Considered

- **案A: 毎時バッチによるポーリング**: リアルタイム性に欠け、API の無駄な消費が発生するため却下。GitHub イベント（Closed）ベースが最も効率的である。

## 結果 / Consequences

### メリット (Positive consequences)

- **Outcome**: 人間の介入なしにエージェントが自律的にタスクを消化し続け、開発スピードが飛躍的に向上する。
- **Resilience**: 自己修復コマンドにより、外部要因によるパイプラインの停止からいつでも復旧できる。

### デメリット (Negative consequences)

- **Monitoring**: 依存関係のループなどでリレーが止まっていないか、定期的な観測が必要になる。

## 検証基準 / Verification Criteria

- [ ] 先行 Issue を閉じると、後続のチェックリストが更新され、最後に `gemini` ラベルが付与されること。
- [ ] `sync-relay` を実行した際、手動で付けた `gemini` 漏れなどが正しく修復されること。

## 実装状況 / Implementation Status

未着手
