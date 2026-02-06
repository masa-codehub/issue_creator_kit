# Goal Definition - Issue #306: Update Architecture Lifecycle

## 1. 達成目標 (SMART Goal)
- **Specific**: `docs/architecture/arch-state-007-lifecycle.md` を更新し、ADR-008 の「物理状態スキャナー」および「手動承認フロー」に基づいたライフサイクル定義を完成させる。
- **Measurable**:
    - 「将来的な自動化」に関する記述が削除されていること。
    - 状態遷移トリガーが「物理移動を伴う PR マージ」であることが明記されていること。
    - Mermaid ダイアグラムが physical paths との状態の対応を正確に示していること。
- **Achievable**: アーキテクトとしてドキュメントを修正可能。
- **Relevant**: ADR-008 "Scanner Foundation" の実装に伴う必須のドキュメント整合。
- **Time-bound**: 本セッションの完了までに実施。

## 2. 成果物 (Deliverables)
- [ ] 修正済みファイル: `docs/architecture/arch-state-007-lifecycle.md`

## 3. 検証方法 (Verification / DoD)
- **DoD 1 (Physical Alignment)**: `grep -E "将来的な自動化|run-workflow" docs/architecture/arch-state-007-lifecycle.md` の実行結果が空であること。
- **DoD 2 (Transition Clarity)**: `_inbox/` から `_approved/` への遷移トリガーに「Manual PR Merge」が含まれ、かつそのプロセスに「物理的な移動」が必要であることが記述されていることを確認。
- **DoD 3 (Visual Consistency)**: Mermaid ダイアグラム内の各状態に、対応する `reqs/` 配下のディレクトリパスが注釈として含まれていることを確認。

## 4. 依存関係とリスク (Dependencies & Risks)
- **Dependency**: `docs/architecture/plans/adr-008-automation-cleanup/definitions.md` の定義に従う。
- **Risk**: 既存の `arch-state-doc-lifecycle.md` との混同を避ける必要がある（修正対象を間違えない）。