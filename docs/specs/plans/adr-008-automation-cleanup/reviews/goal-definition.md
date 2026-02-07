# 目標定義書 (Goal Definition) - ADR-008 Specification Planning

## 1. 核心的目標 (Core Intent / SMART Goal)

- **ゴール:** ADR-008 (Cleanup & Scanner Foundation) の意図を正確に反映し、実装者がTDDを開始できるレベルの詳細仕様策定計画（共通定義、タスク分割、Issue案）を完遂する。
- **採用した仮説:** Full Cycle プロセス (Arch -> Spec -> TDD) に基づき、アーキテクチャで確定した Scanner 構造を詳細な仕様タスクに落とし込む。
- **期待される価値:** 実装フェーズにおける曖昧さを排除し、堅牢な物理状態スキャナー基盤を最短経路で構築可能にする。

## 2. 実行の前提条件 (Achievable / Prerequisites)

- **対象ファイル:**
  - `docs/architecture/plans/adr-008-automation-cleanup/arch-to-spec.md` (Handover)
  - `docs/architecture/arch-structure-008-scanner.md` (SSOT)
  - `docs/architecture/arch-structure-issue-kit.md`
- **必要な情報:** アーキテクチャフェーズで確定したコンポーネント構成と不変条件（Invariants）。
- **依存タスク:** なし（Archフェーズ完了済み）

## 3. アクションプラン (Specific / Time-boxed)

1. **[準備]:** Handoverドキュメントとアーキテクチャ図を読み込み、コンテキストを同期する。
2. **[策定]:** `docs/specs/plans/adr-008-automation-cleanup/definitions.md` を作成し、用語・型・エラー・削除対象コードを定義する。
3. **[分割]:** 仕様策定タスクを分割し、`drafting-issues` で個別Issue案を作成する（ダイヤモンド型依存構造を意識）。
4. **[統合]:** 仕様策定フェーズ全体を管理するための統合Issue案を作成する。
5. **[監査]:** 自己監査レポートを作成し、計画の品質を保証する。

## 4. 完了定義 (Measurable / Definition of Done)

### A. 状態検証 (State Check)

- **確認対象:** `docs/specs/plans/adr-008-automation-cleanup/`
- **合格基準:**
  - `definitions.md` が存在し、必要な定義（削除リスト、Scanner構成）が記述されている。
  - `reqs/tasks/drafts/` 配下に仕様策定用のタスク案が複数（最低3つ以上）生成されている。
  - `self-audit.md` が作成され、自己監査の内容が記述されている。

## 5. 制約と安全策 (Constraints & Safety)

- **負の制約:** プロダクトコードの実装は一切行わない。
- **安全策:** 既存の `arch-to-spec.md` の制約を最優先で遵守する。

## 6. SMART 自己評価

- **Specific:** 成果物パスとアクションが明確。
- **Measurable:** ファイルの存在と内容で判定可能。
- **Achievable:** 確立されたスキルセット (`planning-specs`) で実行可能。
- **Relevant:** ADR-008 の実装に向けた必須ステップ。
- **Time-boxed:** 計画策定として適切な分量。
