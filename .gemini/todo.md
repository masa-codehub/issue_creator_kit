# Goal: ADR-005: グラフ理論に基づくタスク構造化支援ツールの導入 の作成・承認・PR提出

## Tasks
- [x] **Step 1:** ADR作成用フィーチャーブランチの作成
  - Action: `git checkout -b feat/adr-005-roadmap-tool`
  - Verify: `git branch --show-current` が期待通りであること
- [x] **Step 2:** 能動的偵察 (Active Reconnaissance)
  - Action: `active-reconnaissance` スキルを実行し、現在の `task-structuring` スキルの限界と、ADR/Design Doc 完了に向けた依存関係管理の課題を精査する。
  - Verify: 現状のギャップが言語化され、ラフドラフトの `Context` に反映されること
- [x] **Step 3:** ドメインモデリング (Modeling)
  - Action: `domain-modeling` スキルを実行し、ツールが扱う「タスク」「成果物(Artifact)」「依存関係(Edge)」の定義と境界を明確にする。
  - Verify: ツールとスキルの間で共有される用語集（Ubiquitous Language）が定義されること
- [x] **Step 4:** 技術的仮説の立案 (Hypothesis)
  - Action: `architecture-hypothesis` スキルを実行し、CLIツールの具体的インターフェース案と、分解される3つのスキルの責務分担を策定する。
  - Verify: 代替案（ツールを使わない場合等）との比較がなされ、最適なアプローチが選択されること
- [x] **Step 5:** ADR起草 (Drafting)
  - Action: `adr-drafting` スキルを実行し、`reqs/design/_inbox/adr-005-roadmap-cli-tool.md` を作成する。
  - Verify: ユーザーからの合意が得られ、ステータスが「提案中」になること
- [ ] **Step 6:** 最終監査とPR作成
  - Action: `tdd-audit` スキルを参考に最終チェックを行い、`github-pull-request` でPRを作成する。
  - Verify: PR URL が生成されること
- [ ] **Step 7:** 振り返り (Retrospective)
  - Action: `retrospective` スキルを実行し、今回のハイブリッド設計プロセスの質を評価する。
  - Verify: YWT/KPTの結果が記録されること
