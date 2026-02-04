# ドメインモデリングガイド (DDD Modeling Guide)

Eric Evansの**ドメイン駆動設計 (DDD)** 原則に基づき、ビジネス知識を構造化するためのリファレンス。
各設計フェーズにおいて、迷った場合はこのガイドラインに従って用語や構造を決定する。

## 1. 境界づけられたコンテキスト (Bounded Context)
言葉の意味が一貫する範囲を定義する。

- **チェックポイント:**
  - 新しい概念は既存のコンテキストに属するか、独立したコンテキストか？
  - コンテキスト間の関係（Upstream/Downstream, ACL）は明確か？

## 2. 戦術的モデリング (Tactical Modeling)
ドメインの構成要素を明確に区別する。

- **Aggregate Root (集約ルート):**
  - 整合性の維持に責任を持つ唯一のエントリポイント。
  - **Check:** トランザクション整合性を保てる最小限のサイズか？
- **Entity (エンティティ):**
  - ライフサイクルと識別子(ID)を持つオブジェクト。
  - **Check:** IDで管理する必要があるほど重要なライフサイクルを持つか？
- **Value Object (値オブジェクト):**
  - 識別子を持たず、値を表現する不変オブジェクト。
  - **Check:** 可能な限りValue Objectとして定義し、副作用を減らしているか？
- **Invariant (不変条件):**
  - 集約内で「常に守られなければならない整合性ルール」。

## 3. ユビキタス言語 (Ubiquitous Language)
ドキュメントとコードで完全に一致する用語を使用する。

- **Rule:** ここで定義した言葉を、クラス名、メソッド名、変数名として一言一句違わず使用すること。
- **NG:** ドキュメントでは「配送」、コードでは `Shipping` と `Delivery` が混在している状態。

## アウトプット形式例

```markdown
## ドメインモデル (DDD Analysis)

- **Bounded Context:** Delivery Context
- **Model Definition:**
  - **Aggregate Root:** `Shipment` (配送)
    - **Invariant:** 「発送済みステータスの場合、宛先変更はできない」
  - **Entity:** `Parcel` (荷物 - IDで識別)
  - **Value Object:** `DeliveryAddress` (配送先住所 - 不変)
- **Ubiquitous Language:**
  - **Shipper:** 配送業者（Carrierではない）。
  - **TrackingCode:** 追跡番号（IDとは区別する）。
```
