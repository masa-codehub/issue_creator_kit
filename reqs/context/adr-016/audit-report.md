# Final Audit: ADR-016 TDD Implementation Plan

## 1. Compliance Check (整合性確認)

- **SMART Goals**: ゴールは具体的 (Specific)、測定可能 (Measurable)、達成可能 (Achievable)、関連性がある (Relevant)、期限がある (Time-bound) に適合している。
- **DoD Consistency**: 定義された検証条件は ADR-016 の要件を完全に 網羅している。

## 2. Technical Feasibility (技術的妥当性)

- **Regex**: `(?:adr|design)-(\d{3})` による拡張は安全である。
- **Idempotency**: `PHASE_ORDER` による比較ロジックは冪等性を保証する。
- **Label Sync**: `update_issue_labels` (PUT) による全置換は、メタ データラベルの保持を適切に行えば、最も安全な更新手段である。

## 3. Recommended Process (推奨プロセス)

1. `L1AutomationUseCase` の単体テストを作成し、既存の adr-ID と新規の design-ID の両方に対するラベル生成（arch/spec）をテストする。
2. `RelayEngine` にフェーズ順序定数と `_handle_phase_transition` を追加し、モックを使用して遷移ロジックをテストする。
3. 結合テストで、GitHub API の模擬レスポンスを使用して、フェーズラ ベルの置換と他ラベルの保持を検証する。

## Conclusion

本計画は実行可能であり、ADR-016 の意図を正しく反映していると判定す る。
