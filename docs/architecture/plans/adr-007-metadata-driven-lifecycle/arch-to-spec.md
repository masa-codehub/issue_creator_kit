# Architecture to Spec Handover: ADR-007

## 1. 確定したアーキテクチャ境界
- **Containers:** `reqs/design/`, `reqs/tasks/`, `GitHub Issues`, `ick CLI`, `GitHub Actions`
- **Component Layering:** `ick CLI` は `Interface Adapters` 層として機能し、ユースケースを実行する。
- **Lifecycle States:** ADR-007 に従い、ADR は `Draft`, `Approved`, `Postponed`, `Superseded`、タスクは `Draft`, `Ready`, `Issued`, `Completed`, `Cancelled` を持つ。

## 2. Spec策定時の注意点
### 2.1 ADR-007 の更新が必要
アーキテクチャ定義（`arch-state-007-lifecycle.md`）において、タスクの状態として `Issued` が定義されたが、オリジナルの ADR-007 メタデータスキーマにはこれが含まれていない。
**Spec策定フェーズの冒頭で、ADR-007 の `status` スキーマ定義を更新し、`Issued` を正式なステータスとして追加すること。**

### 2.2 バリデーションロジックの実装
`ick sync` コマンド等の仕様策定において、以下のバリデーションを厳密に定義する必要がある。
- `depends_on` で指定されたタスクのステータスチェック。
- `Issued` ステータスのタスクファイルが `reqs/tasks/_archive/` に存在することの整合性チェック。

## 3. 保留事項
- **ロードマップとの連携:** `roadmap` フィールドの詳細な同期ロジックについては、今回のアーキテクチャ図では抽象化されているため、詳細仕様で詰める必要がある。
