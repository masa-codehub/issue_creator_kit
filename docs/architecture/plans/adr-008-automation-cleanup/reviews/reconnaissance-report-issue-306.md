# Reconnaissance Report - Issue #306: Update Architecture Lifecycle

## 1. 調査対象 (Scope)

- `docs/architecture/arch-state-007-lifecycle.md` (Target)
- `docs/architecture/plans/adr-008-automation-cleanup/definitions.md` (Reference)
- `docs/architecture/arch-state-doc-lifecycle.md` (Comparison)

## 2. 現在の状況 (Current State)

- `arch-state-007-lifecycle.md` は "Physical State Lifecycle (ADR-008)" というタイトルで更新されている (Commit `2712c2d` による)。
- 以下の点で ADR-008 との不整合がある：
  - 「手動または将来的な自動化」という表現が含まれており、「Auto-script による遷移を削除」という方針に反している。
  - 遷移トリガーが「Manual PR Merge」となっているが、ファイル移動（`mv`）を PR に含めるべきであることを明記していない。
- `arch-state-doc-lifecycle.md` は依然として古い `issue-creator-kit run-workflow` に依存した定義を保持しているが、今回の修正対象は `arch-state-007-lifecycle.md` である。

## 3. 事実の断片 (Evidence)

- **arch-state-007-lifecycle.md**:
  - States: `Draft (Inbox)`, `Approved`, `Done (Archive)`.
  - Mapping: `_inbox/`, `_approved/`, `_archive/`.
  - Trigger (Draft -> Approved): `_inbox/` から `main` ブランチへの Pull Request マージ。
  - Side Effect: 「スキャナーによる検知」。
- **definitions.md**:
  - "No automated script shall perform this move (from \_inbox to \_approved)."
  - "The physical location in the file system is the Single Source of Truth (SSOT)."

## 4. 懸念事項 (Risks/Concerns)

- 「将来的な自動化」という言葉が、ADR-008 の「自動化の排除」の意図と混同される可能性がある。
- 物理的な位置が SSOT であるなら、マージされただけでは不十分で、`_approved/` に配置されていることが Approved の定義である。PR 自体で移動を行うべきであることを明記する必要がある。

## 5. 次のステップ (Next Steps)

- `analyzing-intent` にて、上記懸念事項に基づき、修正が必要な箇所の特定と方針の策定を行う。
