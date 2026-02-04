# 設計指針 (Design Brief)

## 1. 作成する成果物 (Target Artifacts)
- **種類:** (例: ADR, System Context, Specification)
- **出力ファイル名:** (例: `reqs/design/_inbox/adr-005-auth.md`)
- **使用テンプレート:** (例: `reqs/design/template/adr.md`)

## 2. 解決すべき課題と方針 (Strategic Intent)
- **課題 (Problem):** (分析フェーズで特定された核心的な問題)
- **採用された方針 (Decision):** (対話フェーズで合意した解決策の方向性)
- **主な理由 (Rationale):** (なぜその方針を選んだか、決定的な要因)

## 3. ドキュメントに含めるべき内容 (Content Requirements)
*(後工程の執筆者が迷わないための具体的な指示)*

- **必須セクション:**
  - (例: トークン有効期限のセキュリティリスク評価)
  - (例: 既存の認証ミドルウェアとの互換性検証)
- **検討すべき論点 (Key Discussion Points):**
  - (例: ステートレス性を維持する方法)
- **除外する項目 (Out of Scope):**
  - (例: 今回はOAuth連携については触れない)

## 4. 制約と評価基準 (Constraints & Evaluation)
- **技術的制約:** (偵察レポートで判明した技術的な壁など)
- **受容するリスク (Accepted Risks):** (対話で合意したトレードオフ)
- **完了条件 (Definition of Done):** (ドキュメントがどのような状態になれば完了か)

## 5. 推奨される次のアクション (Next Actions)
- **推奨スキル:** (例: `adr-creation`)