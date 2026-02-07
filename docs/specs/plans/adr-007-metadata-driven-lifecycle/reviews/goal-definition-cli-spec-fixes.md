# Goal Definition: CLI Spec Fixes (PR #286 Review Response)

## 1. 達成目標 (SMART Goal)

PR #286 のレビュー指摘に基づき、`docs/specs/api/cli_commands.md` を修正し、仕様の欠落（UseCase シグネチャ）と曖昧さ（引数フォーマット）を解消する。

- **Specific:** `IssueCreationUseCase` のメソッド名と引数 (`adr_id`) を明記し、`--adr-id` のバリデーションルールを追加する。
- **Measurable:** 修正後のファイルに対し `auditing-ssot` を実行し、指摘事項が全て解消されていることを確認する。
- **Achievable:** 既にレビュー指摘と分析が完了しており、既存ドキュメントの修正のみで完結する。
- **Relevant:** ADR-007 に基づくメタデータ駆動ライフサイクル管理の正確な実装を担保するために不可欠。
- **Time-bound:** 本セッション内で完了させる。

## 2. 完了条件 (Definition of Done)

- [ ] `docs/specs/api/cli_commands.md` に `IssueCreationUseCase.create_issues_from_virtual_queue(..., adr_id=...)` の記述が追加されている。
- [ ] `docs/specs/api/cli_commands.md` に `--adr-id` のフォーマット（`adr-` + 3桁の数字）とバリデーション（失敗時終了コード 1）が追記されている。
- [ ] `docs/specs/api/cli_commands.md` の TDD Criteria に、不正な `--adr-id` 指定時のテストケースが追加されている。
- [ ] 自己レビューおよび `auditing-ssot` をパスしている。

## 3. 検証方法 (Verification Methods)

- **静的検証:**
  - `grep "adr_id" docs/specs/api/cli_commands.md` で追加箇所を確認。
  - `grep "adr-" docs/specs/api/cli_commands.md` でフォーマット定義を確認。
- **SSOT監査:**
  - `activate_skill{name: "auditing-ssot"}` を実行し、修正後の Spec が ADR-007 およびレビュー指摘と整合していることを確認。
