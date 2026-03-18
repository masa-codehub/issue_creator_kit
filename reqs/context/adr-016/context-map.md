# Context Map: ADR-016 ADR Phase Transition Automation

## 1. Current Phase (現在のフェーズ)

- **Target Phase**: Arch
- **Input Document**: `reqs/design/_approved/adr-016.md`

## 2. Concretized Specifications (具体化・紐付けされた仕様)

ADRから抽出した要件のうち、確定済みの具体情報が発見されたもの（事実）。

| ADR/DesignDoc の要件 (抽象) | 確定した具体情報・参照先 (事実) | 具体的な内容の要約 (無駄なく) |
| :--- | :--- | :--- |
| [REQ-3] ADR_ID_PATTERN | `src/issue_creator_kit/domain/models/document.py` | `^(adr|design)-\d{3}(?:-[a-z0-9-]+)?$` にて実装済み。 |
| [REQ-4] ADR type | `src/issue_creator_kit/domain/models/document.py` | `Literal["adr", "design-doc"]` にて実装済み。 |
| [REQ-5] Task.adr_number | `src/issue_creator_kit/domain/models/document.py` | `(?:adr|design)-(\d{3})` にて実装済み。 |
| [REQ-6] update_issue_labels | `src/issue_creator_kit/infrastructure/github_adapter.py` | `PUT /repos/{owner}/{repo}/issues/{issue_number}/labels` を使用して実装済み。 |
| [REQ-11] Trigger | `docs/architecture/structure-relay.md` | `relay-trigger.yml` が `issue-kit relay --issue-no #123` を呼び出す構成が定義済み。 |

## 3. Formulated Hypotheses (隙間を埋める実現可能な仮説)

具体情報が見つからなかった要件（Gap）。現フェーズにおいて未確定な情報や、今後決定されるべき仕様はここが主体となります。

| 紐付かなかった要件 (Gap) | 設定した仮説 (Hypothesis) | 矛盾がない理由 (Feasibility Rationale) |
| :--- | :--- | :--- |
| [REQ-1, 2] 初期ラベル付与ロジック | `L1AutomationUseCase.get_labels` にて `(?:adr|design)-(\d{3})` を使用。`adr-` なら `adr:NNN` + `arch`、`design-` なら `design:NNN` + `spec` を返却する。 | プレフィックスに応じた適切な初期フェーズ設定により、ADRとDesignDocのライフサイクル管理を共通化できる。 |
| [REQ-7, 8, 9, 10] フェーズ遷移の冪等性 | `RelayEngine._handle_phase_transition` にて、現在のラベルを取得し「遷移先フェーズが現在より進んでいる場合のみ更新」するガードを実装。 | 意図しないフェーズの巻き戻りを防ぎ、リトライ時などの安全性を確保できる。 |
| [REQ-1, 2] ラベルパターン拡張 | `GitHubAdapter.ADR_LABEL_PATTERN` を `(adr|design):(\d{3})` に拡張し、両方のプレフィックスに対して適切な説明文を生成する。 | ADRとDesignDocの両方をGitHub Issue上で識別・管理するために必要。 |
| [REQ-1, 2] ラベル属性定義 (Colors) | `arch`: `#0E8A16` (Green), `spec`: `#FBCA04` (Yellow), `tdd`: `#1D76DB` (Blue), `plan`: `#D4C5F9` (Purple), `audit`: `#D93F0B` (Red) | 既存のGitHub標準色やプロジェクトの視認性に基づいた配色案。 |

## 4. Next Actions for Downstream (後工程がすべきこと)

- [ ] **Fact & Hypothesis Validation**: 上記の仕様と仮説を前提として、Spec（詳細設計）フェーズに進み、具体的なメソッドシグネチャやテストケースを定義すること。
- [ ] **Implementation of Idempotency Guard**: `RelayEngine` におけるフェーズ順序（arch < spec < tdd）の定義と、それに基づく更新判定ロジックを詳細化すること。
- [ ] **Label Attribute Finalization**: `GitHubAdapter.LABEL_ATTRIBUTES` に定義した色と説明文（例: `arch`: "Architecture design phase"）を反映すること。
