# 目標定義書 (Goal Definition) - PR #288 Spec Fixes

## 1. 核心的目標 (Core Intent / SMART Goal)

- **ゴール:** PR #288 のレビュー指摘を反映し、`creation_logic.md` と `promotion_logic.md` を最新の SSOT (ADR-007) に適合させる。
- **採用した仮説:** 案A（実証的仮説）- 指摘箇所のピンポイント修正と用語の統一。
- **期待される価値:** 実装時の曖昧さを排除し、TDD フェーズへの円滑な移行を保証する。

## 2. 実行の前提条件 (Achievable / Prerequisites)

- **対象ファイル:**
  - `docs/specs/logic/creation_logic.md`
  - `docs/specs/logic/promotion_logic.md`
- **必要な情報:** レビューコメントの内容（分析済み）、ADR-007 の内容。
- **依存タスク:** なし（現在の作業ブランチで完結可能）。

## 3. アクションプラン (Specific / Time-boxed)

1. **[変更] `creation_logic.md`:**
   - Step 3.C に link-replaced body の保存を追記。
   - Step 4.2 の Roadmap Sync 参照を ADR-007 に修正。
2. **[変更] `promotion_logic.md`:**
   - Step 3.3 の Rationale を修正し、`ick create` を明示。
3. **[検証]:** `grep` を用いて、 superseded な ADR-003 への参照が残っていないこと、および修正箇所が反映されていることを確認。

## 4. 完了定義 (Measurable / Definition of Done)

### A. 自動検証 (Automated)

- **検証コマンド:**
  ```bash
  # ADR-003 への不正な参照がないことの確認
  grep -r "ADR-003" docs/specs/logic/ | grep -v "Supersedes" || echo "Reference check passed"
  # 修正キーワードの存在確認
  grep "link-replaced body" docs/specs/logic/creation_logic.md
  grep "ick create" docs/specs/logic/promotion_logic.md
  ```
- **合格基準:** `grep` が期待通りの行を出力し、ADR-003 への意図しない参照が検出されないこと。

### B. 状態検証 (State Check)

- **確認対象:** `docs/specs/logic/creation_logic.md`, `docs/specs/logic/promotion_logic.md`
- **合格基準:** レビュアーの提案（suggestion）が反映され、Markdown 形式が崩れていないこと。

## 5. 制約と安全策 (Constraints & Safety)

- **負の制約:** ADR-007 の根本的な決定事項（Atomic Move 等）を変更しない。
- **安全策:** 修正前にファイルの現在の内容を `read_file` で取得済み。

## 6. SMART 自己評価

- **Specific:** ファイル名と修正内容が明確に特定されている。
- **Measurable:** `grep` による検証が可能。
- **Achievable:** 修正範囲は限定的であり、現ブランチで即時実行可能。
- **Relevant:** レビュアーの懸念を解消し、仕様の品質を高める。
- **Time-boxed:** 1ターンの作業として完結する。
