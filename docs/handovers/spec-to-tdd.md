# Handover: Spec to TDD (ADR-003 Implementation)

## 1. Overview
本ドキュメントは、ADR-003（仮想キューと自己推進型ワークフロー）の詳細仕様策定フェーズから、実装フェーズ（TDD Creation / Backend Coder）へ引き継ぐための重要事項をまとめたものである。

## 2. 実装の優先順位 (Implementation Priority)
1.  **Core Domain**: `Document` および `Metadata` のパース・バリデーション・正規化ロジック。
2.  **Issue Creation Logic**: 依存関係の解決（トポロジカルソート）を含む原子的な起票プロセス。
3.  **Infrastructure Adapters**: Git/GitHub/FileSystem との具象連携。
4.  **Workflow & CLI**: フェーズ連鎖（Auto-PR）および CLI エントリポイントの統合。

## 3. 重要事項と実装上のヒント (Critical Tips)

### 3.1. 原子性 (Atomicity) の徹底
- **Fail-fast Zone**: `IssueCreationUseCase` の起票ループ内で 1 件でも API エラーが発生した場合は、**即座に処理を中断すること。**
- Git への書き戻し（Issue番号の付与）は、全件起票が成功した後の「Commit Phase」まで一切行わない。

### 3.2. 仮想キューの検知
- `GitAdapter.get_added_files` では、`--no-renames` オプションを必須とする。
- これにより、`drafts/` から `archive/` へのファイル移動が「追加」として正しく検知され、起票対象となる。

### 3.3. 依存関係の解決
- `depends_on` に基づくトポロジカルソートには、Python 標準の `graphlib.TopologicalSorter` (3.9+) の使用を推奨する。
- 循環参照（CycleError）が発生した場合のハンドリングを単体テストで網羅すること。

### 3.4. テストとモックの方針
- **Adapter Layer**: 外部コマンド（git）や外部 API（GitHub）を直接叩かず、スタブまたはモックを使用して例外送出（429 Rate Limit等）をシミュレートすること。
- **UseCase Layer**: アダプターを注入（Dependency Injection）し、ビジネスロジック（順序、原子性、メタデータ更新）の正しさを検証すること。

## 4. 重点テスト項目 (Key Test Scenarios)
- [ ] **正常系**: 複数ファイルの移動（仮想キュー）からの一括起票と、ロードマップのリンク置換。
- [ ] **異常系 (API)**: 起票途中の API エラーによる処理中断と、Git ファイルが未更新（番号なし）で保たれることの検証。
- [ ] **異常系 (Cycle)**: タスク間の循環依存による起票前の停止。
- [ ] **境界値**: メタデータが日本語キー（タイトル、ラベル等）で記述されている場合の正規化。

## 5. 関連ドキュメント (SSOT)
- ADR-003: `reqs/design/_approved/adr-003-task-and-roadmap-lifecycle.md`
- Logic Spec: `docs/specs/logic/creation_logic.md`
- Adapter Spec: `docs/specs/components/infra_adapters.md`