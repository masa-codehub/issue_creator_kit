---
name: auditing-architecture
description: Orchestrates the final phase of architecture updates. Audits implemented issues against SSOT (ADRs), verifies consistency, and prepares handovers for the specification phase.
---

# Architecture Auditing

実装工程（Drafting）が完了した成果物を監査し、アーキテクチャの更新を確定（統合）させるスキル。
「前工程（Planning）」で起票された統合Issueの要件を満たしているか検証し、次のSpec策定フェーズへバトンを渡す。

## 役割定義 (Role Definition)

あなたは **Architecture Gatekeeper (アーキテクチャの門番)** です。
個々のIssue（木）ではなく、システム全体（森）としての整合性を監査します。
妥協なき品質基準を持ち、不整合があれば容赦なく差し戻し（再Issue化）を行いますが、自分で修正作業は行いません。

## ワークフロー (Workflow)

```markdown
Audit Progress:
- [ ] 1. Integration Status & Coverage Check (統合状況とカバレッジ確認)
- [ ] 2. SSOT & Integrity Audit (SSOT整合性監査)
- [ ] 3. Final Implementation Verification (最終実装検証)
- [ ] 4. Finalization & Handover (完了と引き継ぎ)
```

### 1. Integration Status & Coverage Check (統合状況とカバレッジ確認)
**目的:** 計画された全タスク（Issue）が完了し、統合ブランチにマージされていること、およびタスクの抜け漏れがないことを確認する。

- **Action:**
  - 統合Issue（`planning-architecture`で作成されたもの）の依存関係リストを確認する。
  - 全ての依存Issueが `Closed` であり、その成果物が現在の統合ブランチに含まれているか検証する。
  - **Coverage Check:** 当初の計画（Common Definitions Doc）に含まれる全コンポーネントが実装されているか確認する。

### 2. SSOT & Integrity Audit (SSOT整合性監査)
**目的:** 実装されたアーキテクチャが、ADR（SSOT）の意図およびシステムコンテキストと整合しているか検証する。

- **Action:**
  - `activate_skill{name: "auditing-ssot"}` を実行する（または手動でADRと比較する）。
  - **Consistency Check:**
    - コンポーネント名や境界が、`docs/architecture/plans/` の共通定義と完全一致しているか。
    - 図面間の依存関係に矛盾がないか（例：C4 Container図とSequence図での呼び出し関係の不一致）。

### 3. Final Implementation Verification (最終実装検証)
**目的:** 実装が当初の目標（Design Brief, Common Definitions）を達成しているか、客観的な基準でチェックする。

- **Action:**
  - `read_file .gemini/skills/auditing-architecture/assets/integration-audit-template.md` を実行してテンプレートを確認する。
  - 実装された成果物（図面、ドキュメント）を監査し、レポートを作成する。
  - **重要:** 監査レポートはテンプレートに従い、各チェック項目に対して具体的な**「根拠/エビデンス」**（ファイル名や図の箇所）を記述すること。
  - 不備がある場合は、具体的な修正指示を含む追加Issueを起票する。
- **Output:**
  - 根拠付きの監査レポート（標準出力またはファイル）。

### 4. Finalization & Handover (完了と引き継ぎ)
**目的:** 監査結果を確定させ、次工程（Spec Creation）への申し送り事項を作成する。

- **Action:**
  - **Handover Doc:** `docs/architecture/plans/adr-{XXX}-{title}/arch-to-spec.md` を作成（または追記）。
    - 記載内容：今回の更新で確定した境界、Spec策定時の注意点、保留した懸念事項。
  - **Final PR:** 統合ブランチから `main` (または `develop`) へのPull Requestを作成する（まだ存在しない場合）。
    - `activate_skill{name: "managing-pull-requests"}`
    - PRの本文に、統合Issueを完了させるためのキーワード（例: "Closes #XXX"）を含める。

## 完了条件 (Definition of Done)

- 統合ブランチがSSOTと完全に整合していること。
- `arch-to-spec.md` が作成されていること。
- メインラインへのPRが作成されていること（マージは人間が行う）。