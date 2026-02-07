---
id: task-008-07
parent: adr-008
type: task
title: "[Arch Fix] Update arch-structure-issue-kit.md for ADR-008"
status: Issued
phase: architecture
labels:
  - "gemini:arch"
  - "P1"
roadmap: "docs/architecture/plans/adr-008-automation-cleanup/design-brief.md"
depends_on: []
issue_id: 315
---
# [Arch Fix] Update arch-structure-issue-kit.md for ADR-008

## Context
監査において、`docs/architecture/arch-structure-issue-kit.md` が依然として削除済みの `WorkflowUseCase` や `ApprovalUseCase` を記述しており、新設された `Scanner` 基盤を反映していないことが判明した。SSOTとしての信頼性を回復するため、記述を更新する。

## Requirements
- **Remove Legacy Components**: `WorkflowUseCase`, `ApprovalUseCase` および関連する図のノードを削除する。
- **Add Scanner Components**: `Scanner Foundation` (FileSystemScanner, TaskParser, etc.) の記述を追加する（または `arch-structure-008-scanner.md` への参照を追加する）。
- **Update Diagram**: コンポーネント図を更新し、Scanner ベースの構造（CLI -> Scanner -> Parser/Builder）を反映させる。

## Acceptance Criteria
- `arch-structure-issue-kit.md` が現状の実装計画と整合していること。
- `arch-structure-008-scanner.md` との間に矛盾がないこと。
