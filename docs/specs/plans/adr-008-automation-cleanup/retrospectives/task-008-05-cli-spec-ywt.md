# Retrospective (YWT): CLI Integration Specification (Task-008-05)

## 1. やったこと (Y: What I did)
- ADR-008 に基づく CLI 統合仕様書 (`docs/specs/components/cli-integration.md`) の策定。
- `FileSystemScanner`, `GraphBuilder`, `Visualizer` を用いた新しい `process` および `visualize` コマンドの定義。
- 旧 UseCase への依存コマンド（`process-diff` 等）の Cleanup 方針（非推奨・削除）の決定。
- `drafting-specs` スキルを用いた自己監査の実施。

## 2. わかったこと (W: What I learned)
- **SSOT の重要性**: 物理ファイルシステムを SSOT とすることで、CLI のコマンド構造を大幅に簡略化（`approve` や `run-workflow` の削除）できることが再確認できた。
- **依存関係の可視化**: `visualize` コマンドが Mermaid を出力することで、複雑な依存関係を持つタスク群の実行前検証が容易になる。
- **Cleanup のタイミング**: 大規模な基盤変更時には、既存コマンドをいつ削除するかの明確な方針（今回は仕様レベルで非推奨を宣言）が、後続の実装フェーズでの迷いを減らす。

## 3. 次にやること (T: Next steps)
- **実装フェーズへの引き継ぎ**: 本仕様に基づき、`cli.py` の実装および `test_cli.py` の TDD 実装を開始する。
- **Action 部分の具体化**: 今回スコープ外とした「実際の起票・移動ロジック」について、次フェーズでの仕様策定に向けた準備（インフラ層のアダプター仕様確認等）を行う。
