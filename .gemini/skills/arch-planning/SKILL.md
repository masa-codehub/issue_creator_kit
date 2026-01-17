---
name: arch-planning
description: Formulates a comprehensive strategy for visualizing ADRs. Analyzes the architectural intent, selects necessary diagrams (Context, Container, Sequence, etc.) to minimize redundancy, and defines precise drafting requirements for parallel execution.
---

# Architecture Planning (Visualization Strategy)

**ADR (Architecture Decision Record)** の意図を、第三者に誤解なく伝えるための「図解戦略（Blueprint）」を策定するスキル。
「何を描くか」だけでなく、「何を強調し、何を省略するか」を厳密に定義し、後続の並列作図タスク（Issue）の品質と整合性を担保する。

## 役割 (Role)

**Architecture Strategist (アーキテクチャ戦略家)**
ADRを単なる図の羅列に変換するのではない。読み手（開発者・ステークホルダー）が設計意図を最短時間で理解できるよう、最適な図の組み合わせと、各図の**記述粒度（Abstraction Level）**を設計する。

## 前提 (Prerequisites)

- 入力となる承認済みADR（SSOT）が存在すること。
- システムの現状（As-Is）を示すドキュメントまたはコードが存在すること。

## 手順 (Procedure)

### 1. 意図の抽出 (Intent Extraction)

**目的:** ADRの本質的な価値と、図解すべき「複雑さ」の所在を特定する。

- **Action:**
  - `activate_skill{name: "active-reconnaissance"}` を使い、対象のADRと関連コード/ドキュメントを分析する。
  - 以下の質問に答える形で**Core Intent**を定義する。
    - 「このADRで最も重要な変更は、構造（Structure）か、振る舞い（Behavior）か、データ（Data）か？」
    - 「開発者が実装時に最も迷いそうな（＝図解が必要な）ポイントはどこか？」

### 2. 図構成の選定 (Portfolio Selection)

**目的:** 説明責任を果たすための「必要十分かつ最小限」の図を選定する（MECE）。

- **Action:**
  - 以下の基準で、作成・更新すべき図を決定する。**「あれば良い」レベルの図は捨て、必要に応じて選定した図解の中で文書による補足説明を行う。**
  - **Selection Criteria:**
    - **System Context / Container:** システム境界やデプロイ単位に変更がある場合。（※ほぼ必須）
    - **Component:** 内部の責務分担や依存ルールに変更がある場合。
    - **Sequence:** 非同期処理、分散トランザクション、複雑な条件分岐など「時系列」が重要な場合。
    - **State:** オブジェクトのライフサイクル管理が肝となる場合。
    - **ERD:** データモデルや整合性ルールに変更がある場合。

### 3. 記述内容の詳細化 (Definition of Content)

**目的:** 各図について、Drafting担当者が迷わないレベルまで記述要件を具体化する。

- **Action:**
  - 選定した各図について、以下の項目を定義する。
  - **Scope:** どこからどこまでを描くか（例：決済サービス内部のみ、外部API連携含む等）。
  - **Focus:** 特に詳細に記述すべき箇所（例：エラー時のリトライフロー）。
  - **Abstraction Level:** 抽象度（クラス名まで書くか、コンポーネント名で止めるか）。
  - **Constraints:** 守るべき制約（依存方向、レイヤー構造）。

### 4. 依存解決とタスク設計 (Dependency Resolution)

**目的:** 並列作業時の不整合を防ぐための「共通認識」を作る。

- **Action:**
  - 図同士の依存関係（例: Container図が決まらないとSequence図の登場人物が決まらない）を特定する。
  - **Decoupling Strategy:**
    - 依存がある場合、**「仮の定義（Stub）」** をこの場で決定してしまう。
    - _例:_ 「新コンポーネント名は `BillingWorker` とする。これを前提にSequence図を描くこと。」
  - これにより、各タスクが完全に並列で実行可能になるようにする。

## アウトプット (Output)

`arch-creation` がIssueDraftを作成するための構造化データ（JSON形式またはリスト）。

```markdown
## Visualization Plan

1. **[Update] C4 Container Diagram**
   - **Requirement:** 新設された `BillingWorker` コンテナを追加。APIからの非同期メッセージングを描画。
   - **Stub:** コンテナ名は `billing-worker`、Queue名は `payment-queue` で統一する。
2. **[New] Payment Sequence Diagram**
   - **Requirement:** ユーザー決済から領収書メール送信までの非同期フロー。特にRedis障害時のリトライを描くこと。
   - **Reference:** ADR-005 Section 3.2 "Retry Policy"
```
