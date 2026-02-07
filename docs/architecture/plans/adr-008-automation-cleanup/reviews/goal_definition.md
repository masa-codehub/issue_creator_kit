# Goal Definition - Issue #315: Architecture Fix for ADR-008

## 1. 達成すべき目標 (SMART Goals)

- **Specific**: `arch-structure-issue-kit.md` と `arch-structure-007-metadata.md` を更新し、ADR-008 (Scanner Foundation) の構造と制約を正しく記述する。
- **Measurable**:
  - `arch-structure-issue-kit.md` から `WorkflowUseCase`, `ApprovalUseCase` の記述が消え、`Scanner Foundation` の記述が追加されていること。
  - `arch-structure-007-metadata.md` に `## Invariants` セクションが追加され、ID形式と依存関係の制約が明文化されていること。
  - Mermaid 図面が正しくレンダリングされ、依存関係の方向が Clean Architecture に準拠していること。
- **Achievable**: `scouting-facts` で必要な情報をすべて収集済みであり、参照ドキュメントも特定されているため達成可能。
- **Relevant**: プロジェクトの SSOT を最新化し、実装の不整合を防ぐために不可欠。
- **Time-bound**: 本セッション中に完了させる。

## 2. 完了条件 (Definition of Done)

- [ ] `docs/architecture/arch-structure-issue-kit.md` が更新され、旧コンポーネントが削除されている。
- [ ] `docs/architecture/arch-structure-issue-kit.md` に `Scanner Foundation` (FileSystemScanner, TaskParser, GraphBuilder) が追加されている。
- [ ] `docs/architecture/arch-structure-007-metadata.md` に `Invariants` セクションが追加されている。
- [ ] すべての Mermaid 図面が構文エラーなく、依存の方向が正しい。
- [ ] 自己監査レポート（`drafting-audit-template.md` ベース）を作成し、合格している。

## 3. 検証方法 (Verification Methods)

- **ファイル存在・内容確認**: `grep` で削除・追加キーワードを確認。
  - `grep "WorkflowUseCase" docs/architecture/arch-structure-issue-kit.md` -> 0件
  - `grep "Scanner Foundation" docs/architecture/arch-structure-issue-kit.md` -> 1件以上
  - `grep "## Invariants" docs/architecture/arch-structure-007-metadata.md` -> 1件以上
- **構造整合性**: `arch-structure-issue-kit.md` が `arch-structure-008-scanner.md` と矛盾していないことを目視（および自己監査）で確認。
