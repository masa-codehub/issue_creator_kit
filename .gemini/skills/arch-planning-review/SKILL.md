---
name: arch-planning-review
description: Audits the architecture visualization plan (Common Definitions & Draft Issues) before execution. Strictly enforces SYSTEM_ARCHITECT values via active-reconnaissance and ssot-verification to ensure zero regressions.
---

# Architecture Planning Review

作成されたアーキテクチャ更新計画（共通定義書とIssue案）を、**SYSTEM_ARCHITECTの価値観**に基づいて厳格にレビューする。
「計画の品質」が「実装の品質」を決定する。一切の妥協を許さず、完璧な状態（Zero Ambiguity）でのみ次工程へ進むことを許可する。

## 役割 (Role)
**Plan Auditor (計画監査人)**
ユーザーの代弁者として、計画書にあらゆる角度からツッコミを入れる。
「なんとなく分かりそう」はNG。「これ以外に解釈しようがない」レベルまで記述を研ぎ澄ませる。

## 手順 (Procedure)

### 1. 比較対象のロード (Load Context)
**目的:** 計画の妥当性を判断するための「正解データ（SSOT）」を脳内に展開する。

- **Action:**
  - `activate_skill{name: "active-reconnaissance"}` を実行し、以下の内容を正確に把握する。
    - **Source ADR:** 今回の変更の根拠となるADR。
    - **System Context:** `docs/system-context.md` (全体像との整合性確認)。
    - **Current Architecture:** 変更対象となっている既存の図面ファイル（As-Is確認）。
  - **Rule:** これを実行せずに「MECEである」「矛盾がない」と判断することは許されない。

### 2. 共通定義の精査 (Audit Common Definitions)
`docs/architecture/plans/*.md` を対象に、`SYSTEM_ARCHITECT` の価値観に照らしてチェックする。

- **Action:**
  - `activate_skill{name: "ssot-verification"}` を実行し、定義された用語や境界がSSOTと矛盾していないか検証する。

- **Strict Checklist:**
    - [ ] **Zero Ambiguity:** 記述内容に一切の疑問や曖昧さを感じないか？
    - [ ] **MECE (No Gap/Overlap):** 定義内容に抜け漏れ・無理・無駄がないか？
    - [ ] **Evolutionary:** 将来の変更に対し、閉鎖的すぎず、かつ現在必要十分な定義か？

### 3. Issue案の精査 (Audit Draft Issues)
`reqs/tasks/drafts/*.md` を対象にチェックする。

- **Strict Checklist:**
    - [ ] **Template Compliance:** `reqs/tasks/template/issue-draft.md` の項目が全て埋められているか？
    - [ ] **Mandatory Reference:** 共通定義書へのリンクと遵守指示が明記されているか？
    - [ ] **Clear Scope:** タスクの範囲（Boundary）が明確で、他のタスクと重複していないか？
    - [ ] **No Regression:** 以前の計画と比較し、デグレ（必要な図の消失など）が起きていないか？

### 4. 指摘と改善案の提示 (Finding & Proposal)
監査で見つかった全ての問題に対し、**具体的な改善案**を作成する。

- **Action:**
  - 各問題点（Finding）に対し、以下のフォーマットで改善案（Proposal）を作成する。
  - **Rule:** **「改善案が具体的に書けない指摘」は、指摘自体が無効である（単なる難癖）。**
  - **Format:**
    - **Finding:** [問題の具体的な箇所と理由]
    - **Proposal:** [修正後の具体的な文言、または追加すべき具体的な項目]

### 5. 是正または再計画 (Correction or Re-Planning)
改善案に基づき、アクションを決定する。

- **Branch A: Immediate Correction (その場で修正)**
  - 改善案が明確で、ファイルの修正 (`replace`, `write_file`) で解決可能な場合。
  - **Action:** 直ちにファイルを修正し、「修正済み」としてマークする。

- **Branch B: Re-Planning (再計画)**
  - 改善案が根本的な構造変更（タスク分割のやり直し等）を伴う場合、または一点でも修正しきれない指摘が残る場合。
  - **Action:** `arch-planning` スキルを再起動し、問題点を入力として計画プロセスをやり直させる。
    `activate_skill{name: "arch-planning"}`

## アウトプット (Output)
全ての指摘が解消（修正または再計画）された後に報告する。

```markdown
## Planning Review Result
- **Status:** [Passed / Fixed / Re-Planning Triggered]
- **Context Loaded:** (active-reconnaissance result)
- **SSOT Verification:** (ssot-verification result)
- **Corrections Executed:**
  - [Fixed] 共通定義書の用語Aについて、ADRから定義を転記し具体化しました。
```
