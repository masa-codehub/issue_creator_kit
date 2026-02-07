# Architecture to Specification Handover: ADR-007

## 1. 確定した設計方針 (Confirmed Architecture)

- **フラットな物理構造:** `reqs/tasks/` 配下は ADR ごとのフォルダに限定し、サブフォルダによるフェーズ管理は行わない。
- **メタデータによる DAG 制御:** タスクの実行順序は物理フォルダではなく `depends_on` メタデータによって制御する。
- **Atomic Move:** `ick create` 成功時にのみ物理ファイルを `_archive/` へ移動させる。

## 2. Spec 策定時の制約と注意点 (Constraints for Spec)

- **DAG 解析ロジック:** `ick CLI` が `depends_on` を解析し、トポロジカルソート等を用いて実行順序を決定する仕様を詳細化すること。
- **冪等性の担保:** 起票失敗時のリトライや、手動でのファイル移動が発生した場合の整合性チェック仕様を定義すること。
- **ステータス同期:** GitHub Issue のクローズ（Completed）をどのようにローカルの `ick sync` に反映させるかのデータフローを策定すること。

## 3. 保留された懸念事項 (Outstanding Concerns)

- 物理ファイルを移動させた後の `git log` の追跡可能性（`git mv` 相当の操作が CLI で行われるか）。
- L2 統合Issueが物理ファイルとして存在しない場合の、`ick` によるフェーズ完了判定ロジック。
