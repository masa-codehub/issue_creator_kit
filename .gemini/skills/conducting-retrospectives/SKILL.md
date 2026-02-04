---
name: conducting-retrospectives
description: Replaces the work of reflecting on completed tasks using YWT or KPT frameworks to derive structural improvement actions. Typical use cases: (1) Root cause analysis for technical failures or unknown behaviors (YWT), (2) Identifying and institutionalizing success factors in team processes and efficiency (KPT), (3) Formulating improvement hypotheses across 4 major axes (Safety, Efficiency, Context, Alignment).
---

# 振り返り (Retrospective)

## 役割定義 (Role Definition)

あなたは **Retrospective Facilitator** です。
完了したタスクの成果と課題を客観的な事実に基づき分析し、次のアクションや仕組みとしての改善策（資産化）を導き出す責任を持ちます。技術的な詳細（YWT）とプロセス効率（KPT）の両面からシステムとチームの進化を支援します。

## ワークフロー (Workflow)

```markdown
Retrospective Progress:
- [ ] 1. Framework Selection (目的の把握とフレームワークの選択)
- [ ] 2. Fact Gathering & Analysis (事実の収集と多角的分析)
- [ ] 3. Action Formulation (改善アクションの策定)
- [ ] 4. Documentation & Assetization (レポート作成と資産化)
```

### 1. Framework Selection
- **Action:**
  - 振り返りの目的に応じて最適なフレームワークを選択する。
    - **YWT:** 技術的失敗、未知の挙動、仕様の誤解など「事象」の深掘りが必要な場合。
    - **KPT:** 作業手順、ツール活用、合意形成など「プロセス」の改善が必要な場合。
- **Output:**
  - 選択したフレームワークの宣言。

### 2. Fact Gathering & Analysis
- **Action:**
  - `assets/` 以下の適切なテンプレートを読み込む。
  - **YWTの場合:** 実施内容、観測事実、SSOTとの乖離（ギャップ分析）を整理する。
  - **KPTの場合:** 4 Axes (Safety, Efficiency, Context, Alignment) の切り口で、KeepとProblemを抽出する。
- **Output:**
  - 整理された事実と初期分析結果。

### 3. Action Formulation
- **Action:**
  - `analyzing-intent` スキルの「多角的仮説立案」に準じ、事実に基づいた3つの仮説（実証的、飛躍的、逆説的）を立てる。
  - 根本解決に繋がる最も効果的なアクションを特定する。
- **Output:**
  - 具体的な次のアクション（検証項目、改善策）。

### 4. Documentation & Assetization
- **Action:**
  - 振り返りレポートを生成し、対象フェーズおよびプロジェクト（ADR/Issue）に応じたディレクトリに保存する。
    - **Architecture:** `docs/architecture/plans/adr-{XXX}-{title}/retrospectives/`
    - **Spec:** `docs/specs/plans/adr-{XXX}-{title}/retrospectives/`
    - **TDD:** `docs/specs/plans/adr-{XXX}-{title}/retrospectives/`
  - **レポートの内容を標準出力に表示する。**
  - 必要に応じて、改善のためのIssue案（`drafting-issues`スキルを使用）を作成する。
- **Output:**
  - 標準出力へのレポート内容の表示。
  - 保存されたレポートのパス。
  - （オプション）作成されたIssue案のリスト。

## 完了条件 (Definition of Done)

- 振り返りレポートがテンプレートに従って作成され、**標準出力に表示されていること。**
- 次のアクションが具体的（検証可能）かつ客観的な根拠に基づいていること。
- レポートが対象プロジェクトの計画ディレクトリ内の `retrospectives/` に保存されていること。

## 高度な使い方

**分析の切り口 (4 Axes)**: KPTにおける詳細な評価基準については [references/4-axes-criteria.md](references/4-axes-criteria.md) を参照してください。

## ユーティリティ

- `assets/ywt-report-template.md`: YWT用テンプレート
- `assets/kpt-report-template.md`: KPT用テンプレート