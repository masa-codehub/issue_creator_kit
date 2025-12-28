# Issue案: GitHub Actions ワークフローの刷新

- **Roadmap**: [roadmap-adr002-document-approval-flow.md](../../../../roadmap/_inbox/roadmap-adr002-document-approval-flow.md)
- **Task ID**: T3-3
- **Depends-On**: issue-T3-2.md
- **Status**: Draft

## 1. 目的と背景
`sed` ベースの旧ワークフローを廃止します。

## 2. 実装指示 (Implementation Instructions)
- [ ] `.github/workflows/auto-approve-docs.yml` を書き換え、`issue-kit approve` を使用するようにせよ。

## 3. 検証基準 (Definition of DoD)
- [ ] 統合テスト（ローカル実行）が成功すること。
