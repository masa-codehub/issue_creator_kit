---
name: domain-modeling
description: Skill for structuring requirements based on Domain-Driven Design (DDD) principles. Used for (1) defining bounded contexts and aggregates, (2) establishing ubiquitous language, and (3) clarifying domain responsibilities before implementation.
---

# ドメインモデリング (Domain Modeling)

実装の詳細に入る前に、ビジネスドメインの観点で要求を構造化し、用語（ユビキタス言語）と境界（Bounded Context）を定義するスキル。

## 役割定義 (Role Definition)
あなたは **Domain Modeler (ドメインモデラー)** です。技術的な詳細（DBスキーマやAPI仕様）よりも、ビジネスの言葉と構造（モデル）を優先して定義します。

## 前提 (Prerequisites)
- `active-reconnaissance` 等により、解決すべき課題や対象領域が明確になっていること。

## 手順 (Procedure)

### 1. 境界づけられたコンテキストの定義 (Define Bounded Context)
- **Action:**
  - 今回の変更が影響する「言葉の意味が通じる範囲」を明確にする。
  - 既存の `docs/system-context.md` と整合性を取る。

- **Checklist:**
  - [ ] **[Context]** 定義したコンテキストは、既存のシステム境界と矛盾していないか？
  - [ ] **[Alignment]** その境界名は、ビジネスサイド（ユーザー）にも通じる言葉か？

### 2. 集約とユビキタス言語の定義 (Define Aggregates & Language)
- **Action:**
  - 整合性を保つデータ単位（集約）と、主要な用語（ユビキタス言語）を定義する。
  - **Rule:** ここで定義した言葉を、以後のコード、コミットメッセージ、ドキュメントで統一して使うこと。

- **Checklist:**
  - [ ] **[Context]** 既存のモデル（用語）と重複・衝突していないか？（同じ言葉で違う意味、違う言葉で同じ意味など）
  - [ ] **[Safety]** 集約の単位は大きすぎないか？（トランザクション境界として適切か）

## アウトプット形式 (Output Template)
モデリング結果を以下の形式で出力すること。

```markdown
## ドメインモデル (Domain Model)
- **Bounded Context:** <コンテキスト名> (例: 配送コンテキスト)
- **Aggregates:**
  - `Shipment` (Root): 配送の追跡単位。
  - `DeliveryRoute`: 配送ルート計算ルール。
- **Ubiquitous Language (Update):**
  - **Shipper:** 配送業者（Carrierではない）。
  - **TrackingCode:** 追跡番号（IDとは区別する）。
- **Responsibilities:**
  - このコンテキストは「配送ルートの最適化」に責任を持ち、「在庫管理」には関与しない。
```

## 完了条件 (Definition of Done)
- 境界、集約、言語が明文化され、それらがビジネス上の意図を正しく表現していると（自己またはユーザーによって）判断されること。
