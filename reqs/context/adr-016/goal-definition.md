# Goal Definition: ADR-016 TDD Phase Implementation

## 1. Context & Outcome (背景と期待される成果)

ADR-016 に基づき、ADR/DesignDoc のフェーズ遷移（arch -> spec -> tdd）を自動化する。これにより、手動によるラベル管理コストを削減し、実態に即したプロジェクト進捗の可視化を実現する。

## 2. SMART Goals (具体的目標)

- **Specific**:
  1. `L1AutomationUseCase.get_labels` を修正し、`adr-` (arch) と `design-` (spec) をサポート。
  2. `RelayEngine._handle_phase_transition` を実装し、`integration` + `audit` タスク完了時に上位 Issue のフェーズを更新。
  3. `GitHubAdapter` に `arch`, `spec`, `tdd`, `plan`, `audit` ラベルの属性（色・説明）を定義。
- **Measurable**: 新規作成するテストコードを含め、全てのテストがパスすること。
- **Achievable**: 既存の `GitHubAdapter.update_issue_labels` (PUT) を活用し、安全に実装可能。
- **Relevant**: ADR-016 の「自動化」「冪等性」要件を完全に満たす。
- **Time-bound**: 本実装タスクの完了をもって達成とする。

## 3. Verification Methods (DoD & Commands)

### Definition of Done (完了定義)

- [ ] `L1AutomationUseCase` が `design-XXX` 形式を正しく処理し、初期ラベル `spec` を付与する。
- [ ] `RelayEngine` が `integration` タスク完了時に、上位 Issue のフェーズラベルのみを置換する。
- [ ] フェーズ遷移において、`arch < spec < tdd` の順序を守り、巻き戻りが発生しない。
- [ ] `GitHubAdapter` が新規ラベルを適切な色（Green, Yellow, Blue 等）で作成・認識する。

### Verification Commands

```bash
# Unit tests for label generation
pytest tests/unit/usecase/test_l1_automation_usecase.py

# Unit tests for phase transition logic (New)
pytest tests/unit/usecase/test_relay_engine_phase.py

# Integration tests for full flow (New)
pytest tests/integration/test_adr016_phase_transition.py
```

## 4. Risks & Mitigations (リスクと対策)

- **Risk**: 他のメタデータラベル（`L1`, `adr:NNN` 等）が誤って消去される。
- **Mitigation**: `_handle_phase_transition` において、フェーズラベル（`arch`, `spec`, `tdd`）のみを抽出し、それ以外を保持したまま `update_issue_labels` を呼び出す。
