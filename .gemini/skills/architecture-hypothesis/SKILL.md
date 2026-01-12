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

### 1. 戦略的評価軸の選定 (Strategy Selection)
- **Action:**
  - 今回の意思決定において、特に重要視すべき **3つの設計原則（評価軸）** をリストから選択する。これが「案A」の設計思想の核となる。
    - **依存性:** Robert C. Martin (Clean Architecture)
    - **特性:** Mark Richards (Architecture Characteristics)
    - **データ:** Martin Kleppmann (Data Consistency)
    - **進化性:** Martin Fowler (Evolutionary Architecture)
    - **ドメイン:** Eric Evans (DDD)

### 2. 多角的仮説の構築 (Hypothesis Formulation)
- **Action:**
  - 以下の3つのアプローチで仮説を構築する。
  
    1.  **案A (実証的仮説 - Grounded):** 
        - **構築ロジック:** 選定した3つの評価軸（戦略）に基づき、以下の3要素を統合して導き出す。
            - **ドメインモデル:** ビジネス構造と境界 (`domain-modeling` 成果物)
            - **SSOT:** 既存の設計原則と制約 (ADR, システム境界)
            - **ユーザーの意図:** 解決すべき課題と期待値 (`active-reconnaissance` 成果物)
        - 「ドメイン構造Xを実現するため、戦略Y（評価軸）に従い、技術Zを採用する」という論理で構築する。

    2.  **案B (飛躍的仮説 - Leap):** 
        - 将来の拡張性や新技術の導入に重きを置いた、リスクはあるがリターンも大きい「挑戦案」。
    
    3.  **案C (逆説的仮説 - Paradoxical):** 
        - 「そもそも今の仕組みで良いのでは？」「YAGNIではないか？」という視点に立った「ミニマム/回避案」。

- **Checklist:**
  - [ ] **[Context]** 案Aは既存のADR（既決事項）と矛盾していないか？（整合性チェック）
  - [ ] **[Alignment]** 3つの案はそれぞれ異なるトレードオフ（メリット/デメリット）を持っているか？

### 3. 比較分析と決定 (Comparison & Decision)
- **Action:**
  - 3つの案を **4大リスク（価値、実現性、ユーザビリティ、生存性）** で評価し、最も「無理・無駄・ムラ」が少ない案を採用する。
  - アウトプットの比較表を埋める。

## アウトプット形式 (Output Template)
比較分析の結果を以下の形式で出力し、ADRドラフトの `## 検討した代替案` セクション等に追記する。

```markdown
## アーキテクチャ仮説 (Architecture Hypothesis)

### 1. 採用した戦略（評価軸）
今回、以下の3点を最優先事項として設計を行いました。
1. **[原則名]:** (選定理由: 例「頻繁な仕様変更に耐えるため」)
2. **[原則名]:** ...
3. **[原則名]:** ...

### 2. 多角的仮説の比較
| 項目 | 案A (実証的: 本命) | 案B (飛躍的: 挑戦) | 案C (逆説的: 回避) |
| :--- | :--- | :--- | :--- |
| **設計思想** | 選択した3原則に準拠 | (拡張性/新技術重視) | (YAGNI/現状維持) |
| **4大リスク** | (価値/実現/UI/生存) | (価値/実現/UI/生存) | (価値/実現/UI/生存) |
| **判定** | **採用 (Recommended)** | 却下 (理由...) | 却下 (理由...) |

### 3. 結論
案Aを採用します。理由は、[原則名]を満たしつつ、案Bのような[リスク]を回避し、案Cでは満たせない[要件]をクリアできるためです。
```

## 完了条件 (Definition of Done)
- 推奨する案が論理的に導き出され、代替案との比較（4大リスクおよび設計原則に基づく）が明確に記述されていること。
