# Analysis Report: ADR-008 Domain Models Specification

## 1. 意図の深掘り (Analyze Intent)

- **Why**: ADR-003 の Git-diff ベースの走査は、コミット履歴に依存するため、未処理タスクの漏れや同期の複雑さが課題であった。ADR-008 では「物理的なファイルの状態（Physical State）」を唯一の正解（SSOT）とし、確実に未処理タスクを検出・処理可能にすることを目指す。
- **What**: そのための基盤として、厳密な型制約（Guardrails）を持つドメインモデル（Task, ADR, Graph）を再定義する。
- **Outcome**: 開発者が TDD で迷いなく実装できる、厳密かつ詳細な仕様書を提供すること。

## 2. ギャップ分析 (Gap Analysis)

- **As-is**: `src/issue_creator_kit/domain/document.py` に汎用的な `Metadata` モデルが存在するが、ADR と Task の区別が曖昧で、ID 形式の制約も緩い（`^[a-z0-9-]+$`）。グラフ構造や循環参照検知のロジックは未実装。
- **To-be**:
  - `TaskID`, `ADRID` に特化した正規表現制約を導入。
  - `Task`, `ADR` を別個の、あるいは継承関係にある Pydantic モデルとして定義。
  - `TaskGraph` による依存関係管理と、循環参照（Circular Dependency）の即時検知。
- **Gap**: 既存の `Metadata` クラスが大きくなりすぎており、ADR-008 の要件を満たすにはリファクタリング（モジュール分割）と制約の強化が必要。

## 3. 仮説の立案 (Formulate Hypotheses)

### 3.1. 実証的仮説 (Grounded): 特化型モデルへの分割

- **Approach**: 既存の `Metadata` を基盤としつつ、`Task` と `ADR` の特化型モデルを `src/issue_creator_kit/domain/models/` 配下に新規作成する。
- **Reason**: 既存コードへの影響を最小限にしつつ、ADR-008 の新規要件（厳密な ID、グラフ管理）をクリーンに実装できる。

### 3.2. 飛躍的仮説 (Leap): 階層型 ID による自動スコープ管理

- **Approach**: ID 自体に階層構造（`adr-008-task-01`）を持たせ、親 ADR の特定を ID から自動的に行えるようにする。
- **Reason**: メタデータの記述量を減らし、ヒューマンエラーをさらに削減できる。ただし、既存 ID との互換性維持が課題。

### 3.3. 逆説的仮説 (Paradoxical): ファイルパスベースの ID 管理

- **Approach**: ID をメタデータから排除し、`reqs/tasks/adr-008/task-01.md` という「ファイルパス」自体を ID として扱う。
- **Reason**: メタデータの重複定義を排除できる。しかし、ファイル移動時に ID が変わってしまうため、GitHub Issue との紐付けが困難になるリスクがある。

## 4. 推奨案 (Recommendation)

- **仮説 3.1 (Grounded)** を採用する。
- 理由: ADR-008 の `definitions.md` にある方針に最も忠実であり、プロジェクトの安定性を維持しつつ目的を達成できるため。
