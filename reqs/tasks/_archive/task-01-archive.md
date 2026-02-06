---
id: task-008-01
parent: adr-008
type: task
title: "Archive Obsolete Architecture Docs (ADR-003)"
status: Draft
phase: architecture
labels:
  - "gemini:arch"
  - "P2"
  - "SYSTEM_ARCHITECT"
roadmap: "docs/architecture/plans/adr-008-automation-cleanup/design-brief.md"
depends_on: []
issue_id:
---
# Archive Obsolete Architecture Docs (ADR-003)

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: ADR-003 時代の「自動承認」「仮想キュー」に関するドキュメントが残存しており、ADR-008 の方針と矛盾している。
- **To-be (あるべき姿)**: 古いドキュメントが `docs/architecture/archive/` に移動され、開発者が参照すべき最新のアーキテクチャ図のみがルートに残っている状態。
- **Design Evidence (設計の根拠)**: ADR-008 "Cleanup Scope".

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/architecture/plans/adr-008-automation-cleanup/design-brief.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **削除禁止**: 歴史的経緯の保存のため、物理削除（git rm）ではなく移動（git mv）を行うこと。

### 3.2. 実装手順 (Changes)
- [ ] **ディレクトリ作成**: `docs/architecture/archive/` がなければ作成。
- [ ] **ファイル移動**: 以下のファイルを移動。
    - `docs/architecture/arch-behavior-003-autopr.md`
    - `docs/architecture/arch-behavior-003-creation.md`
    - `docs/architecture/arch-state-003-task-lifecycle.md`
    - `docs/architecture/arch-structure-003-vqueue.md`
- [ ] **リンク修正**: 移動したファイル内のリンク切れは許容する（アーカイブのため）。ただし、移動先からルートへの相対パスが変わる点に注意。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: feature/arch-update-adr008
- **作業ブランチ (Feature Branch)**: feature/task-008-01-archive-docs

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **ファイル状態**: 元のパスにファイルが存在せず、`docs/architecture/archive/` に存在すること。
