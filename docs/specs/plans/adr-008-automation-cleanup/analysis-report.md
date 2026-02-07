# Analysis Report: CLI Integration with Scanner Foundation (ADR-008)

## 1. 意図の深掘り (Analyze Intent)
- **Why (目的)**: Git の差分に依存する旧来の自動化ロジック（ADR-003）は、同期漏れや複雑な状態管理が課題であった。ADR-008 では物理ファイルの状態を唯一のソース（Physical State Scanner）とすることで、この複雑さを解消し、信頼性の高いタスク管理を実現する。
- **What (成果物)**: 新しい `FileSystemScanner` および `GraphBuilder` を利用して動作する CLI コマンド（`process`, `visualize`）の実装。
- **How (手段)**: `cli.py` に新しいサブコマンドを追加し、Domain Services をインスタンス化して処理を委譲する。また、旧 UseCase への依存を整理する。

## 2. ギャップ分析 (Gap Analysis)
- **現状**: `cli.py` は Git 差分前提の UseCase (`IssueCreationUseCase`, `RoadmapSyncUseCase`) に依存しており、`init`, `process-diff` コマンドが実装されている。
- **理想**: `cli.py` が `ScannerService` (あるいはその構成要素) を利用し、ファイルシステムの状態から直接タスクを検出し、依存関係グラフに基づいて処理できること。
- **乖離**: 
    - `ScannerService` という統合サービスが未定義（`scanner.py`, `builder.py`, `visualizer.py` は個別）。
    - 既存の `process-diff` コマンドと新しい `process` コマンドの役割分担が不明確。
    - `cli.py` におけるレガシーコマンド（`process-diff`）の Cleanup 方針が未確定。

## 3. 仮説の立案 (Formulate Hypotheses)

### 3.1. 実証的仮説 (Grounded Hypothesis) - 本命案
- **アプローチ**: 既存の `cli.py` に `process` および `visualize` コマンドを追加し、`process-diff` は Deprecated とする。
- **詳細**:
    - `process` コマンドは `--dry-run` オプションを必須とし、`FileSystemScanner` -> `GraphBuilder` を実行して、実行順序を標準出力に表示する（実際の起票処理は今後のタスク）。
    - `visualize` コマンドは `FileSystemScanner` -> `GraphBuilder` -> `Visualizer` を実行し、Mermaid 形式を標準出力に出力する。
    - 既存の `process-diff` は削除せず、「Deprecated」として実行時にエラーと移行案内を表示する。
- **メリット**: 既存機能への影響を最小限にしつつ、新機能を提供できる。

### 3.2. 飛躍的仮説 (Leap Hypothesis) - 理想案
- **アプローチ**: `cli.py` を完全に刷新し、ADR-008 準拠の新しいエントリポイントとする。
- **詳細**:
    - 旧コマンドをすべて削除し、`init`, `process`, `visualize` のみに絞る。
    - `ScannerService` という Facade を Domain Layer に導入し、CLI からの呼び出しを極限までシンプルにする。
- **メリット**: コードが極めてクリーンになり、ADR-008 の意図（Cleanup）を最大限に反映できる。

### 3.3. 逆説的仮説 (Paradoxical Hypothesis) - 最小構成案
- **アプローチ**: 新しい CLI コマンドを `cli.py` ではなく、別のスクリプト（例: `scanner_cli.py`）として実験的に実装する。
- **詳細**:
    - `ick-scanner` のような別コマンドとして提供し、十分な検証の後に `ick` コマンドへ統合する。
- **メリット**: 既存の安定した（？）自動化パイプラインを壊さずに、新しい基盤の検証が可能。

## 4. 推奨案 (Recommendation)
- **仮説 3.1 (Grounded)** をベースに、仕様を策定する。
- 理由: 本タスク（Task-008-05）の Issue 記述には `src/issue_creator_kit/cli.py` の更新が含まれており、完全な刷新や別ファイルの作成はスコープを逸脱する可能性があるため。ただし、旧 UseCase への依存コードは ADR-008 の "Cleanup" の一環としてコメントアウトまたは削除を検討する。
