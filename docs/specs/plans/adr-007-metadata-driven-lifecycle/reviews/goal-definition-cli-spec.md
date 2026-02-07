# Goal Definition - CLI Specification Update (ADR-007)

## 1. 達成目標 (Goals)

`docs/specs/api/cli_commands.md` を更新し、ADR-007 で定義された「メタデータ駆動型ライフサイクル」および「新しいディレクトリ構造」に完全に適合した CLI 仕様を定義する。

## 2. 具体的な成果物 (Deliverables)

- 更新済みの `docs/specs/api/cli_commands.md`

## 3. 必要な変更点 (Changes)

1. **パス定義の更新**:
   - `archive/` -> `_archive/` への置換（`process-diff`, `process-merge`）。
2. **`process-diff` コマンドの挙動定義の更新**:
   - 走査対象ディレクトリの説明を「`reqs/tasks/` 配下の再帰探索」に変更。
   - `--adr-id` オプション（指定された ADR ID に紐づくタスクのみをフィルタリング）の追加。
3. **`run-workflow` コマンドの整合性確認**:
   - デザインドキュメント用のパス（`reqs/design/_inbox`, `_approved`）が ADR-007 と一致していることを確認（現状で一致しているはずだが、明記する）。

## 4. 検証方法 (Verification / DoD)

### 4.1. 機械的検証 (Automated Check)

- [ ] `grep "reqs/tasks/_archive/" docs/specs/api/cli_commands.md` がヒットすること。
- [ ] `grep "\-\-adr-id" docs/specs/api/cli_commands.md` がヒットすること。

### 4.2. 内容検証 (Contextual Review)

- [ ] `process-diff` の説明文に「再帰探索」または「recursive search」という文言が含まれていること。
- [ ] 依存関係の検証基準（TDD Criteria）に、`--adr-id` フィルタの動作確認が含まれていること。

## 5. 実行のリスクと対策 (Risks & Mitigations)

- **リスク**: 既存の `cli.py` の実装と乖離が生じる。
- **対策**: 今回は「仕様書（Spec）」の更新であるため、実装への反映は後続のタスク（007-T3-04-impl 等）で行う。仕様書内に「移行期間」や「後方互換性」への配慮を記述する。
