---
name: arch-planning-review
description: Audits the architecture visualization plan (Common Definitions & Draft Issues) before execution. Strictly enforces SYSTEM_ARCHITECT values and ensures zero regressions by validating against loaded SSOT context via active-reconnaissance and ssot-verification.
---

# Architecture Planning Review

作成されたアーキテクチャ更新計画（共通定義書とIssue案）を、**SYSTEM_ARCHITECTの価値観**に基づいて厳格にレビューする。
完璧な状態（Zero Ambiguity）でのみ次工程へ進むことを許可する。

## 役割 (Role)
**Plan Auditor (計画監査人)**
ユーザーの代弁者として、計画書にあらゆる角度からツッコミを入れる。「これ以外に解釈しようがない」レベルまで記述を研ぎ澄ませる。

## 手順 (Procedure)

### 1. 比較対象のロード (Load Context)
- **Action:**
  - `activate_skill{name: "active-reconnaissance"}` を実行し、Source ADR, System Context, および As-Is Architecture の内容を正確に把握する。

### 2. 共通定義の精査 (Audit Common Definitions)
`docs/architecture/plans/*.md` を対象に、`SYSTEM_ARCHITECT` の価値観に照らしてチェックする。

- **Strict Checklist:**
    - [ ] **Zero Ambiguity:** 記述内容に一切の疑問や曖昧さを感じないか？
    - [ ] **MECE (No Gap/Overlap):** 定義内容に抜け漏れ・無理・無駄がないか？
    - [ ] **SSOT Alignment:** 読み込んだADR/Contextと矛盾していないか？
    - [ ] **Evolutionary:** 将来の変更に対し、閉鎖的すぎず、かつ現在必要十分な定義か？

### 3. Issue案の精査 (Audit Draft Issues)
`reqs/tasks/drafts/*.md` を対象にチェックする。

- **Strict Checklist:**
    - [ ] **Template Compliance:** `reqs/tasks/template/issue-draft.md` の項目が全て埋められているか？
    - [ ] **Mandatory Reference:** 共通定義書へのリンクと遵守指示が明記されているか？
    - [ ] **Clear Scope:** タスクの範囲（Boundary）が明確で、他のタスクと重複していないか？
    - [ ] **No Regression:** 以前の計画と比較し、デグレが起きていないか？

### 4. SSOT整合性検証 (SSOT Verification)
- **Action:**
  - `activate_skill{name: "ssot-verification"}` を実行し、概念レベルでの不整合や原則への違反がないかを最終確認する。

### 5. 指摘と改善案の提示 (Finding & Proposal)
監査で見つかった全ての問題に対し、具体的な改善案を作成する。

- **Action:**
  - 各問題点（Finding）に対し、具体的な改善案（Proposal）をセットにする。改善案が書けない指摘は無効とする。

### 6. 是正または再計画 (Correction or Re-Planning)
- **Branch A: Immediate Correction (その場で修正)**
  - ファイルの修正 (`replace`, `write_file`) で解決可能な場合、直ちに修正する。
- **Branch B: Re-Planning (再計画)**
  - 根本的な構造変更が必要な場合、または一点でも修正しきれない指摘が残る場合、`arch-planning` スキルを再起動する。
    `activate_skill{name: "arch-planning"}`

## アウトプット (Output)
レビュー結果レポート。