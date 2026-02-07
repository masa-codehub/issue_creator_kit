# Goal Definition - Issue #308 (Architecture Refactoring)

## 1. 達成目標 (Outcome)

`docs/architecture/arch-structure-issue-kit.md` をADR-008に基づき完全に最新化し、古いコンポーネントの残留がないこと、および新基盤の構成要素が正しく反映されている状態にする。

## 2. 具体的な成果物 (Deliverables)

- 修正済みファイル: `docs/architecture/arch-structure-issue-kit.md`

## 3. 実装詳細 (Implementation Details)

- **Mermaid図の更新:**
  - コンポーネント名を `Scanner Service` から `ScannerService` (CamelCase) に変更。
- **構成要素定義 (Element Definitions) の更新:**
  - `CLI Entrypoint`: `run-workflow` コマンドの削除と `visualize` コマンドのサポートを明記。
  - `ScannerService`: 役割説明に `FileSystemScanner`, `TaskParser`, `GraphBuilder`, `Visualizer` のサブコンポーネントが含まれることを明記。
  - **完全削除の徹底:** `WorkflowUseCase`, `ApprovalUseCase`, `RoadmapSyncUseCase` という単語がファイル内に一切残っていないことを確認。

## 4. 完了条件 (Definition of Done)

- [ ] `WorkflowUseCase`, `ApprovalUseCase`, `RoadmapSyncUseCase` がファイル内から完全に消去されている。
- [ ] `ScannerService` という名称が使用されている。
- [ ] `visualize` というキーワードがCLIの役割説明に含まれている。
- [ ] 自己監査（Self-Audit）を実施し、すべての項目をパスしている。

## 5. 検証手順 (Verification)

- **存在確認 (Negative):**
  ```bash
  grep -E "WorkflowUseCase|ApprovalUseCase|RoadmapSyncUseCase" docs/architecture/arch-structure-issue-kit.md
  # 結果が空であること
  ```
- **存在確認 (Positive):**
  ```bash
  grep "ScannerService" docs/architecture/arch-structure-issue-kit.md
  grep "visualize" docs/architecture/arch-structure-issue-kit.md
  # いずれもヒットすること
  ```
