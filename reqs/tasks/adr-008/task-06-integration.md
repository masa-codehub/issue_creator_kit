---
id: 008-integrate
parent: adr-008
type: integration
title: "[Arch Integration] ADR-008 Architecture Refactoring"
status: Draft
phase: architecture
labels:
  - "gemini:arch"
  - "P1"
  - "SYSTEM_ARCHITECT"
roadmap: "docs/architecture/plans/adr-008-automation-cleanup/design-brief.md"
depends_on: ["008-01", "008-02", "008-03", "008-04", "008-05"]
issue_id:
---
# [Arch Integration] ADR-008 Architecture Refactoring

## 1. 目的と背景 (Goal & Context)
- **Goal**: ADR-008 に基づくアーキテクチャ図のリファクタリング（削除・更新・新規作成）を統合し、SSOT を確定させる。
- **Context**: 個別の図面更新が完了した後、全体の一貫性を最終確認し、`main` ブランチへマージする。

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/architecture/plans/adr-008-automation-cleanup/design-brief.md`
- [ ] `docs/architecture/` 全体

## 3. 統合手順 (Integration Steps)

### 3.1. マージと競合解決
- [ ] 各Feature Branch (`task-008-01` ~ `05`) を `feature/arch-update-adr008` にマージ。
- [ ] 競合が発生した場合は、`definitions.md` および ADR-008 の記述を優先して解決。

### 3.2. 全体監査 (Auditing)
- [ ] `activate_skill{name: "auditing-architecture"}` を実行。
    - **リンク検証**: 残存するファイルから、アーカイブされたファイルへのリンクが意図せず残っていないか。
    - **用語統一**: "Physical State", "Scanner" 等の用語が全ドキュメントで統一されているか。
    - **構造整合性**: `issue-kit` の図と `scanner` の詳細図に矛盾がないか。

## 4. ブランチ戦略 (Branching Strategy)
- **統合ブランチ**: feature/arch-update-adr008
- **ターゲット**: main

## 5. 完了条件 (Definition of Done)
- [ ] 全てのサブタスクが完了（Closed）していること。
- [ ] `auditing-architecture` のレポートが Pass していること。
- [ ] `main` への Pull Request が作成され、Approved 状態になること。
