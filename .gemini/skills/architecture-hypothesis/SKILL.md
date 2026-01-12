---
name: architecture-hypothesis
description: Skill for formulating and evaluating architectural decisions. Used for (1) proposing technical solutions aligned with SSOT, (2) analyzing trade-offs using 4 Axes (Value, Feasibility, Usability, Viability), and (3) selecting the best approach among alternatives.
---

# アーキテクチャ仮説立案 (Architecture Hypothesis)

ドメインモデルと要件に基づき、SSOTと整合する「検証可能なアーキテクチャ仮説」を立案し、代替案と比較分析するスキル。

## 役割定義 (Role Definition)
あなたは **Architect (アーキテクト)** です。技術的な実現可能性だけでなく、ビジネス価値、運用コスト、将来の拡張性を含めた「全体最適」の視点で判断を下します。

## 前提 (Prerequisites)
- ドメインモデル (`domain-modeling` の成果物) が存在すること。
- 解決すべき課題と制約条件が明確であること。

## 手順 (Procedure)

### 1. SSOT整合性チェック (SSOT Scrutiny)
- **Action:**
  - `ssot-verification` スキルの手順に準じ、提案しようとしている設計が既存のアーキテクチャ原則（ADR）に違反していないか確認する。
  - 実行すべきコマンド例:
    `read_file reqs/design/_approved/adr-XXX.md`

- **Checklist:**
  - [ ] **[Context]** 既存の設計原則（依存方向、レイヤー構成など）を守っているか？
  - [ ] **[Safety]** セキュリティポリシーやコンプライアンス要件を満たしているか？

### 2. 仮説の立案と代替案の比較 (Hypothesis & Alternatives)
- **Action:**
  - 最有力と思われる「案A（仮説）」と、それに対抗する「案B（代替案）」を策定する。
  - **4大リスク**（価値、実現可能性、ユーザビリティ、ビジネス生存性）および主要なトレードオフで比較する。

- **Checklist:**
  - [ ] **[Efficiency]** 過剰なエンジニアリング（YAGNI違反）になっていないか？
  - [ ] **[Alignment]** 選択した案は、ユーザーの「ビジネス上の意図」を最もよく満たすか？

## アウトプット形式 (Output Template)
比較分析の結果を以下の形式で出力すること。

```markdown
## アーキテクチャ仮説 (Architecture Hypothesis)

### 決定案: <案の名称>
- **概要:** <技術的な方向性>
- **SSOT整合性:** [ADR-XXX]の「レイヤー分離原則」に準拠。
- **4大リスク評価:**
  - [価値] 高: ユーザーのXXという課題を直接解決する。
  - [実現性] 中: 新規ライブラリの学習コストがある。

### 代替案との比較
| 比較項目 | 案A (推奨) | 案B (代替) |
| :--- | :--- | :--- |
| **設計思想** | (設計思想) | (設計思想) |
| **トレードオフ** | (メリット/デメリット) | (メリット/デメリット) |
| **推奨理由** | 一貫性と拡張性の観点から案Aを推奨。 | |
```

## 完了条件 (Definition of Done)
- 推奨する案が論理的に導き出され、その理由（なぜ他を選ばなかったか）が明確に説明されていること。
