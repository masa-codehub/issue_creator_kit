# Analysis Report - Issue #315

## 1. 真の意図の推測 (Inferred Intent)

- **本質的な課題**: ADR-008 での「引き算のリファクタリング（自動化の簡素化）」により、システムの全体構造が「オーケストレーション型（UseCase中心）」から「スキャン型（Domain/Scanner中心）」へと変化した。この構造変化を SSOT に反映させ、開発者が迷いなく Scanner 基盤を実装できるようにすることが本質的な目的である。
- **期待されるアウトカム**:
  - `issue-kit` の内部構造が最新化され、不要な `UseCase` が排除されている。
  - メタデータの制約が「構造定義（metadata.md）」に集約され、バリデーション実装の根拠が明確になる。

## 2. ギャップ分析 (Gap Analysis)

- **現状**: `arch-structure-issue-kit.md` は CLI が複数の UseCase を使い分ける図になっている。
- **理想**: CLI が `ScannerService` を起動し、その背後で Parser や Builder が動作する図。
- **リスク**: `Invariants` を `metadata.md` に追加する際、既存の `lifecycle.md` との不整合や重複が生じる可能性がある。単なるコピーではなく、構造上の制約（Structure）としての集約を行う。

## 3. 解決策の仮説 (Hypotheses)

### 3.1. 実証的仮説 (Grounded - 本命案)

- **構造修正**: `arch-structure-issue-kit.md` のコンポーネント図から `UC_WF`, `UC_APP` を削除。代わりに `Scanner Foundation` を Application Core に配置し、`cli.py` との連携を図示する。
- **不変条件の集約**: `arch-structure-007-metadata.md` に `## Invariants (Validation Rules)` を新設。ID形式、依存整合性（循環参照・自己参照禁止）を記述する。`lifecycle.md` 側は「状態遷移に伴う制約」に絞り、構造的制約は `metadata.md` に移譲する。

### 3.2. 飛躍的仮説 (Leap - 理想案)

- **レイヤーの再定義**: Clean Architecture の UseCase 層を「Scanner Service」が担うものとし、Domain 層に Pydantic Models (Guardrails) を配置。Infrastructure は純粋な FileSystem / GitHub API に限定する。これにより、テスト容易性を維持しつつロジックを集約する。

### 3.3. 逆説的仮説 (Paradoxical - 刷新案)

- **Issue Kit を「Scanner-first」なツールとして再定義**: CLI は単なる薄いラッパーとし、コアロジックをすべて `ScannerService` (Domain Service) に閉じ込める。これにより、将来的に Web UI や別ツールからの利用も可能にする。

## 4. 推奨アプローチ (Recommended Approach)

- **実証的仮説 (3.1)** を採用。ADR-008 の方針（負債削除とスキャナー構築）に最も忠実であり、実装への橋渡しとして最適。
