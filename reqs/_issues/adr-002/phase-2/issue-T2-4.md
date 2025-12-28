# Issue案: 既存スクリプトの回帰テスト

- **Roadmap**: [roadmap-adr002-document-approval-flow.md](../../../_inbox/roadmap-adr002-document-approval-flow.md)
- **Task ID**: T2-4
- **Depends-On**: issue-T2-3.md
- **Status**: Draft

## 1. 目的と背景
新ユーティリティの導入が既存機能 (`create_issues.py`) を破壊していないか確認します。

## 2. 実装指示 (Implementation Instructions)
- [ ] `create_issues.py` をリファクタリングし、新 `utils.py` を使用するように変更せよ。
- [ ] 既存機能が正常に動作することを確認せよ。

## 3. 検証基準 (Definition of DoD)
- [ ] 既存の Issue 起票フローが正常に動作すること。
