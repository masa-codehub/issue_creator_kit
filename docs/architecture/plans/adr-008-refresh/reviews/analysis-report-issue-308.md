# Analysis Report - Issue #308 (Architecture Refactoring)

## 1. 意図の深掘り (Analyze Intent)

- **目的:** ADR-008 "Cleanup Scope" に基づき、アーキテクチャ図を最新の状態（Scanner基盤中心）に更新する。
- **価値:** 開発者が「現在の正解」の構造を即座に理解できるようにし、削除済みの旧コンポーネントによる混乱を避ける。
- **制約:** Clean Architecture Lite のレイヤー構造を維持しつつ、新基盤を適切に配置する。

## 2. ギャップ分析 (Gap Analysis)

- **現状:** ワークツリー上で `WorkflowUseCase` 等の削除と `Scanner Service` の追加は既に行われている。
- **理想 (DoD):**
  - 構成要素名が Issue の指示 (`ScannerService`) と一致している。
  - `Scanner Foundation` (ADR-008) の構成要素 (`FileSystemScanner` 等) が適切に統合・説明されている。
  - CLIコマンドの変更 (`run-workflow` 削除, `visualize` 追加) が明文化されている。
- **乖離:** 現状は `Scanner Service` という名称が使われており（スペースあり）、詳細コンポーネントの記述が不足している。また、CLIの役割説明にコマンド名が明示されていない。

## 3. 仮説の立案 (Formulate Hypotheses)

### 3.1 実証的仮説 (Grounded)

- **内容:** 現状の `arch-structure-issue-kit.md` を微修正する。名称を `ScannerService` に統一し、説明文にサブコンポーネント（Parser, Builder, Visualizer）を追加する。
- **メリット:** 変更が最小限で済む。

### 3.2 飛躍的仮説 (Leap)

- **内容:** Mermaid 図においても `ScannerService` を subgraph 化し、その中に `Scanner`, `Parser`, `Builder` を配置する。これにより、Issue Kit 内での Scanner 基盤の重要性と内部構造を視覚的に強調する。
- **メリット:** 内部構造がより明快になり、詳細設計ドキュメントとの整合性が高まる。

### 3.3 逆説的仮説 (Paradoxical)

- **内容:** `arch-structure-issue-kit.md` はあくまで全体像を保つため、`ScannerService` は1つの箱として表現し続け、詳細は `arch-structure-008-scanner.md` へのリンクで済ませる。その代わり、データの流れ（物理ファイル -> DAG -> Issue）の記述を強化する。
- **メリット:** 図の複雑さを抑え、責務の分離を強調できる。

## 4. 推奨案

- **実証的仮説 (Grounded)** をベースに、説明文でのサブコンポーネント明記とCLIコマンド名の更新を行う。Mermaid 図は「Issue Kit 全体」の視点を守るため、あまり細分化しすぎない（逆説的仮説の視点も取り入れる）。
