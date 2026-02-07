---
id: task-008-04
parent: adr-008
type: task
title: "Define Scanner Foundation Architecture"
status: Draft
phase: architecture
labels:
  - "gemini:arch"
  - "P1"
  - "SYSTEM_ARCHITECT"
roadmap: "docs/architecture/plans/adr-008-automation-cleanup/design-brief.md"
depends_on: []
issue_id:
---

# Define Scanner Foundation Architecture

## 1. 目的と背景 (Goal & Context)

- **As-is (現状)**: Scanner に関するアーキテクチャ図が存在しない。
- **To-be (あるべき姿)**: 物理ファイルシステムを走査し、メモリ上でDAGを構築する `ScannerService` の構造と振る舞いが定義されている。
- **Design Evidence (設計の根拠)**: ADR-008 "Scanner Foundation".

## 2. 参照資料・入力ファイル (Input Context)

- [ ] `docs/architecture/plans/adr-008-automation-cleanup/definitions.md`
- [ ] `docs/architecture/template/arch-structure-template.md` (あれば使用、なければ標準的なMarkdown)

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 実装手順 (Changes)

- [ ] **ファイル作成**: `docs/architecture/arch-structure-008-scanner.md`
  - **Component View**: `FileSystemScanner` -> `TaskParser` -> `GraphBuilder` の関係を図示。
  - **Process View**: `scan()` メソッドがどのようにファイルを読み、Graph オブジェクトを返すかのシーケンス。
  - **Visualization**: `Graph` オブジェクトから Mermaid Text を生成する `Visualizer` の役割記述。

## 4. ブランチ戦略 (Branching Strategy)

- **ベースブランチ (Base Branch)**: feature/arch-update-adr008
- **作業ブランチ (Feature Branch)**: feature/task-008-04-scanner

## 5. 検証手順・完了条件 (Verification & DoD)

- [ ] **ファイル存在**: `docs/architecture/arch-structure-008-scanner.md` が作成されていること。
- [ ] **内容確認**: Scanner が Git ではなく File System に依存していることが明記されていること。
