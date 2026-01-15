# [Subsystem Name] Data Model

## Data Context
<!-- 
このデータモデルの前提情報を定義します。
- **Bounded Context:** このデータモデルが属するドメイン（他のコンテキストと混ざらないように）。
- **Database Technology:** `[PostgreSQL | DynamoDB | Redis]` - 採用しているDB技術。
-->

## Diagram (ER)
```mermaid
erDiagram
    %% ここにMermaid記法でER図を描画します。
    %% ENTITY ||--o{ OTHER : relates
```

## Entity Definitions (Conceptual)
<!-- 
実装詳細（SQL型定義）ではなく、ドメインモデルとしての意味とデータ特性を定義します。
-->

### [Entity Name] (Aggregate Root)
- **Concept:** `[このテーブル/コレクションが表す現実世界の概念]`
- **Life-cycle:** `[参照: link-to-state-diagram]`
  <!-- 複雑なライフサイクルを持つ場合は、State Diagramへのリンクを貼る。 -->
- **PII (Personal Info):** `[Yes/No - どの項目が個人情報に該当するか]`
  <!-- セキュリティ/プライバシー観点での重要度。 -->
- **Key Attributes:**
  - `id`: PK (UUIDv7)
  - `...`: ...

## Scalability & Reliability
<!-- Data-Intensiveな観点（非機能要件）での設計を記述します。 -->
- **Sharding/Partitioning:** `[パーティションキー: tenant_id]`
  <!-- データ量が増えた場合の分散戦略。 -->
- **Indexing Strategy:** `[検索パターンに基づくインデックス]`
  <!-- どのようなクエリが頻発するか、それに対してどうインデックスを貼るか。 -->
- **Archiving Policy:** `[ホットデータ期間: 1年, 以降はS3へアーカイブ]`
  <!-- 古くなったデータの扱い（削除するのか、退避するのか）。 -->
