# Goal Definition: CLI Integration Specification (ADR-008)

## 1. 達成すべき目標 (SMART Goal)
- **Specific**: ADR-008 (Scanner Foundation) を CLI に統合するための詳細仕様書 `docs/specs/components/cli-integration.md` を作成する。
- **Measurable**: `drafting-specs` スキルの自己監査チェックリストをすべてパスし、監査レポートを生成すること。
- **Achievable**: 先行タスクで作成された `scanner_logic.md` および `graph_and_validators.md` の内容に基づき、CLI 層のインターフェースと振る舞いを定義可能である。
- **Relevant**: CLI 統合は ADR-008 の最終ステップであり、ユーザーが新基盤を操作可能にするために不可欠である。
- **Time-bound**: 本セッション内で作成、監査、および PR 提出の準備を完了する。

## 2. 成果物 (Deliverables)
- `docs/specs/components/cli-integration.md`
- `docs/specs/plans/adr-008-automation-cleanup/drafting-audit-report.md` (自己監査レポート)

## 3. 検証方法 (Verification / Definition of Done)

### 3.1. 存在確認
- [ ] `docs/specs/components/cli-integration.md` が作成されている。

### 3.2. 内容の整合性
- [ ] 新コマンド `process` (--dry-run 対応) と `visualize` の引数・振る舞いが定義されている。
- [ ] 既存コマンド（`process-diff`, `run-workflow` 等）の Cleanup 方針（コメントアウト等）が明記されている。
- [ ] `FileSystemScanner` および `Visualizer` への依存関係と呼び出しフローが、アーキテクチャ図と矛盾なく記述されている。

### 3.3. 自己監査
- [ ] `drafting-specs` の audit template に基づく監査レポートで、すべての項目が「PASS」となっている。

## 4. 実行コマンド (Verification Commands)
```bash
ls docs/specs/components/cli-integration.md
grep "process" docs/specs/components/cli-integration.md
grep "visualize" docs/specs/components/cli-integration.md
```
