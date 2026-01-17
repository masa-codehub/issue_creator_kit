---
name: adr-domain-modeling
description: Skill for structuring requirements based on Domain-Driven Design (DDD) principles. Used for (1) defining bounded contexts and aggregates, (2) establishing ubiquitous language, and (3) clarifying domain responsibilities before implementation.
---

# ドメインモデリング (Domain Modeling)

実装の詳細に入る前に、Eric Evansの**ドメイン駆動設計 (DDD)** 原則に基づき、ビジネスの知識をコードに落とし込める構造（モデル）へと変換するスキル。

## 役割定義 (Role Definition)

あなたは **Domain Modeler (ドメインモデラー)** です。技術的な詳細（DBスキーマやAPI）よりも、ビジネスの**不変条件 (Invariants)** と **ユビキタス言語** の定義を最優先します。

## 前提 (Prerequisites)

- `active-reconnaissance` 等により、解決すべき課題や対象領域が明確になっていること。

## 手順 (Procedure)

### 1. 境界づけられたコンテキストの定義 (Bounded Context & Map)

- **Action:**
  - 言葉（モデル）の意味が一貫する境界を定義する。
  - **Context Map:** 既存のコンテキストとの関係（Upstream/Downstream, ACL, OHSなど）を明示する。

- **Checklist:**
  - [ ] **[Context]** 新しい概念は既存のコンテキストに属するか、新しいコンテキストか？
  - [ ] **[Safety]** コンテキスト間の結合度（腐敗防止層など）は考慮されているか？

### 2. 戦術的モデリング (Tactical Modeling)

- **Action:**
  - ドメインの主要な構成要素を以下の区分で定義する。
    - **Aggregate Root (集約ルート):** 整合性の維持に責任を持つ唯一のエントリポイント。
    - **Entity (エンティティ):** ライフサイクルと識別子(ID)を持つオブジェクト。
    - **Value Object (値オブジェクト):** 識別子を持たず、値を表現する不変オブジェクト。
  - **不変条件 (Invariant):** 集約内で「常に守られなければならない整合性ルール」を定義する。

- **Checklist:**
  - [ ] **[Safety]** 集約はトランザクション整合性を保てる最小限のサイズか？
  - [ ] **[Alignment]** 識別子(ID)で管理すべきか、値(Value)として扱うべきか、ビジネス意図と合致しているか？

### 3. ユビキタス言語の統一 (Ubiquitous Language)

- **Action:**
  - ドメインエキスパート（ユーザー）と開発者が共通して使う用語を定義する。
  - **Rule:** ここで定義した言葉を、コード上のクラス名、メソッド名、変数名として**一言一句違わず**使用すること。

## アウトプット形式 (Output Template)

モデリング結果を以下の形式で出力し、ADRドラフト等に反映させる。

```markdown
## ドメインモデル (DDD Analysis)

- **Bounded Context:** <Context Name> (関係: Customer Contextの下流)
- **Model Definition:**
  - **Aggregate Root:** `Shipment` (配送)
    - **Invariant:** 「発送済みステータスの場合、宛先変更はできない」
  - **Entity:** `Parcel` (荷物 - IDで識別)
  - **Value Object:** `DeliveryAddress` (配送先住所 - 不変)
- **Ubiquitous Language:**
  - **Shipper:** 配送業者（Carrierではない）。
  - **TrackingCode:** 追跡番号（IDとは区別する）。
```

## 完了条件 (Definition of Done)

- DDDの原則（集約、エンティティ、値オブジェクト）に基づいてモデルが構造化され、ビジネスルール（不変条件）が明文化されていること。
