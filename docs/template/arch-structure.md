# [System/Component Name] Structure

## Context
<!-- 
このアーキテクチャ要素が置かれている背景と目的を定義します。
- **Bounded Context:** この構造が属するドメイン境界（例：決済コンテキスト、会員管理コンテキスト）。
- **System Purpose:** なぜこのコンポーネント群が必要なのか？ビジネス上の究極の目的（Why）を一言で。
-->

## Diagram (C4 [Context/Container/Component])
```mermaid
%% ここにMermaid記法でC4モデルを描画します。
%% Context図: SystemとPersonの関係
%% Container図: アプリケーション、DB、外部システムの関係
%% Component図: Container内部の論理構造（Controller, Service, Repository）
```

## Element Definitions (SSOT)
<!-- 
図に登場する主要な要素（コンテナ、コンポーネント）を1つずつ詳細に定義します。
ここに書かれた内容が、実装時の「仕様」となります。
-->

### [Element Name]
- **Type:** `[Container | Component | Boundary]`
- **Code Mapping:** `[src/path/to/module or ClassName]`
  <!-- この要素がコード上のどこにあるか（ファイルパスやクラス名）を明記し、図とコードの乖離を防ぎます。 -->
- **Role (Domain-Centric):** `[ユビキタス言語での責務定義]`
  <!-- 技術的な役割（「DBへ保存する」）ではなく、ビジネス上の意味（「注文を確定させる」）を記述します。 -->
- **Layer (Clean Arch):** `[Entities | Use Cases | Interface | Infrastructure]`
  <!-- Clean Architectureのどのレイヤーに属するかを宣言します。 -->
- **Dependencies:**
  - **Upstream:** `[依存されている（呼ばれる）相手]`
  - **Downstream:** `[依存している（呼ぶ）相手]`
  <!-- 依存ルール（外側から内側への依存のみ許可）に違反していないかチェックするために記述します。 -->
- **Tech Stack:** `[Language, Framework, Library]`
  <!-- 実装に使用する具体的な技術（Python 3.11, FastAPI, SQLAlchemy等） -->
- **Data Reliability:** `[Sync/Async, Retry Policy, Consistency Level]`
  <!-- データの一貫性要件（結果整合性で良いか、ACID必須か）や、信頼性担保の仕組み（リトライ等）。 -->
- **Trade-off:** `[採用理由と許容したデメリット]`
  <!-- なぜこの設計を選んだのか？代替案と比較して何を優先し、何を犠牲にしたか（例：速度優先で整合性を犠牲）。 -->
