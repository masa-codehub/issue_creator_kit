---
name: arch-planning-review
description: Audits the architecture visualization plan (Common Definitions & Draft Issues) before execution. Checks for MECE, feasibility, efficiency, and alignment with SYSTEM_ARCHITECT values.
---

# Architecture Planning Review

作成されたアーキテクチャ更新計画（共通定義書とIssue案）をレビューし、実行フェーズに進む前に潜在的な問題を検出・修正提案を行うスキル。

## 役割 (Role)
**Plan Auditor (計画監査人)**
「計画の不備」は「実装の手戻り」に直結する。厳格な基準で計画を審査し、無駄や漏れ、曖昧さを排除する。

## 手順 (Procedure)

### 1. 共通定義の精査 (Audit Common Definitions)
`docs/architecture/plans/*.md` を対象にチェックする。

- **Checklist:**
    - [ ] **Ambiguity Check:** 用語定義に曖昧さはないか？（「適宜」「いい感じに」等はNG）
    - [ ] **Consistency Check:** 定義されたコンポーネント名や境界は、既存のアーキテクチャ（SSOT）やADRと矛盾していないか？
    - [ ] **SYSTEM_ARCHITECT Values:**
        - **Simplicity:** 不要に複雑な構造を定義していないか？ (YAGNI)
        - **Evolutionary:** 将来の変更を阻害するような硬直的な定義になっていないか？
        - **Explicit:** 暗黙の了解に頼らず、明示的に定義されているか？

### 2. タスク分割の妥当性 (Audit Task Slicing)
`reqs/tasks/drafts/*.md` を対象にチェックする。

- **Checklist:**
    - [ ] **MECE Check:** 全てのIssueを合わせると、ADRの要件を「漏れなく」カバーできているか？ また「重複」はないか？
    - [ ] **Independence Check:** Issue間の依存関係は解決されているか？（共通定義書でStub化され、相互参照しなくて済むか？）
    - [ ] **Feasibility Check:** 1つのIssueの粒度が大きすぎないか？（エージェントが1ターンで扱える範囲か？）
    - **Link Check:** Issue内に共通定義書へのリンクが正しく記載されているか？

### 3. 改善提案と是正 (Proposal & Correction)
監査で見つかった問題に基づき、修正を行う。

- **Action:**
  - 問題点（Findings）をリストアップする。
  - **Correction:**
    - 問題がある場合、`arch-planning` の再実行はコストが高いため、**可能であればその場で修正する**（`file-ops` や `replace` 等を使用）。
    - 根本的な見直しが必要な場合（タスク分割が根本的に間違っている等）のみ、再計画を要求するレポートを出力する。

## アウトプット (Output)
レビュー結果レポート。

```markdown
## Planning Review Result
- **Status:** [Pass / Fixed / Failed]
- **Corrections Made:**
  - [Fixed] Issue-02のリンクパスが間違っていたため修正しました。
  - [Fixed] 共通定義書の用語Aの定義が曖昧だったため、ADRの記述を引用して具体化しました。
- **Outstanding Issues (if Failed):**
  - [Critical] タスク分割がドメイン単位になっておらず、レイヤー単位になっているため、再計画が必要です。
```
