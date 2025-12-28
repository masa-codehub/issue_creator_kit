# Issue案: CLI コマンド (approve) の統合

- **Roadmap**: [roadmap-adr002-document-approval-flow.md](../../../_inbox/roadmap-adr002-document-approval-flow.md)
- **Task ID**: T3-2
- **Depends-On**: issue-T3-1.md
- **Status**: Draft

## 1. 目的と背景
`issue-kit approve` コマンドとして機能を呼び出せるようにします。

## 2. 実装指示 (Implementation Instructions)
- [ ] `src/issue_creator_kit/cli.py` に `approve` サブコマンドを追加せよ。

## 3. 検証基準 (Definition of DoD)
- [ ] CLI 経由で `process_approvals` が実行できること。
