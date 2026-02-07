# Goal Definition - Archive Obsolete Architecture Docs

## 1. 達成すべき目標 (Outcome)
- `docs/architecture/` にある ADR-003 関連の4ファイルが `docs/architecture/archive/` に完全に移動（git mv）されていること。
- 移動された4ファイルすべてに DEPRECATED 警告が含まれていること。
- 移動された4ファイル内の相対リンクが、新しいディレクトリ階層に合わせて修正されていること。
- すべての変更がステージングされ、コミット可能な状態であること。

## 2. 実行アクション (Steps)
1. `docs/architecture/archive/arch-state-003-task-lifecycle.md` の相対リンクを修正する。
2. `docs/architecture/archive/arch-structure-003-vqueue.md` の相対リンクを修正する。
3. すべての変更を `git add` する。

## 3. 検証条件 (Definition of Done)
- [ ] **物理配置:** `ls docs/architecture/*.md` で対象ファイルが表示されず、`ls docs/architecture/archive/*.md` で表示されること。
- [ ] **警告文:** `grep "DEPRECATED" docs/architecture/archive/*.md` で4ファイルすべてがヒットすること。
- [ ] **リンク整合性:** `grep -L "\.\./" docs/architecture/archive/*.md` (root参照を期待するリンクがある場合) で、必要なパス調整が行われていることを確認する。
- [ ] **Git状態:** `git status` で rename と modified が適切に表示されていること。
