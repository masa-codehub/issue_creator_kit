# Self-Review: Goal Definition (PR-291)

## 1. SMART 性の確認

- [x] **Specific**: 何を作るか、どのファイルを修正するか明確か？
- [x] **Measurable**: 完了を判定するためのコマンドや条件が具体的か？
- [x] **Achievable**: 現在のスキルとツールで達成可能か？
- [x] **Relevant**: ユーザーの本来の意図（ADR-007 準拠）に沿っているか？
- [x] **Time-bound**: 期限（本セッション）が意識されているか？

## 2. リスクと対策

- **リスク**: `Document.metadata` が `dict` から `Metadata` オブジェクトに変わることで既存 UseCase が壊れる。
- **対策**: `Metadata` クラスを `dict` のように振る舞わせる（`__getitem__` の実装）か、UseCase 側も同時に修正する。今回は Domain レイヤーのタスクなので、後方互換性を重視して `__getitem__` などのエイリアスを提供しつつ、移行を促す。

## 3. 判定

**合格 (Approved)**
