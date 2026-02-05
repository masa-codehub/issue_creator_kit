# 目標定義書 (Goal Definition) - ADR-007 TDD Implementation Planning

## 1. 核心的目標 (Core Intent / SMART Goal)
- **ゴール:** ADR-007（メタデータ駆動型ライフサイクル管理）の TDD 実装に向けた、実行可能なテスト戦略とタスク分割計画を策定する。
- **採用した仮説:** 地に足のついた計画 (Grounded Planning) - 手戻りを最小限にするため、Domain -> Infra -> UseCase -> Interface の順で実装する。
- **期待される価値:** 実装者が迷わず Red/Green/Refactor のサイクルを回せるようになり、物理フォルダに依存しない堅牢なタスク管理システムが構築される。

## 2. 実行の前提条件 (Achievable / Prerequisites)
- **対象ファイル:** `docs/specs/**/*.md`, `src/issue_creator_kit/**/*.py`
- **必要な情報:** `spec-to-tdd.md` の引継ぎ事項、既存のテストコード構成。
- **依存タスク:** なし（計画フェーズのため）。

## 3. アクションプラン (Specific / Time-boxed)
1. **[環境準備]:** `feature/impl-adr007-lifecycle` ブランチを作成し、最新の `main` を反映。
2. **[戦略策定]:** `tdd-plan.md` を作成し、共有フィクスチャ（サンプルドキュメント群）とモック方針（Git/GitHub/FileSystem）を定義。
3. **[タスク分割]:** `Document Model`, `Infrastructure Adapters`, `Creation Logic`, `CLI` の 4 つの実装 Issue Draft を作成。
4. **[自己監査]:** `self-audit-report.md` を作成し、計画の網羅性と一貫性を検証。

## 4. 完了定義 (Measurable / Definition of Done)
### A. 状態検証 (State Check)
- **確認対象:** `docs/specs/plans/adr-007-metadata-driven-lifecycle/` 配下のファイル
- **合格基準:** 
    - `tdd-plan.md` が存在し、テストデータとモック方針が記述されていること。
    - 実装タスクの Draft Issue 群が作成されていること。
    - `integration-audit-report.md` (または self-audit) が PASS 判定であること。

## 5. 制約と安全策 (Constraints & Safety)
- **負の制約:** 本フェーズではプロダクトコードの修正は行わず、設計（計画）に徹する。
- **安全策:** 既存の ADR-003 用テストコードを破壊せず、新仕様用のテストスイートを並行して構築する計画を立てる。

## 6. SMART 自己評価
- **Specific:** 各レイヤー（Domain, Infra, UseCase, CLI）のテスト観点が特定されている。
- **Measurable:** 計画ドキュメントの存在と自己監査の結果で判定可能。
- **Achievable:** 既に仕様が確定（PR #289 マージ済み）しているため可能。
- **Relevant:** 実装フェーズへの移行というユーザーの目的を解決する。
- **Time-boxed:** 計画策定は 1〜2 ターンの作業として適切。
