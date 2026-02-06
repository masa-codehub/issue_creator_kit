# 概要 / Summary
[ADR-009] ADR L1 Automation & Glue Labels: 設計ドキュメントの自動起票と識別基盤

- **Status**: 提案中
- **Date**: 2026-02-06

## 状況 / Context
ADR-008 で整理された基盤の上に、設計ドキュメント（ADR）の自動起票機能を再構築する必要がある。また、今後の L2/L3 タスクとの階層的な紐付けを機械的に行うための識別子（接着剤）が必要である。

## 決定 / Decision
`reqs/design/_approved/` にマージされた ADR を L1 Issue として自動起票し、接着剤ラベル（Glue Labels）による紐付け基盤を導入する。

### 1. ADR 自動起票と冪等性
- マージされた ADR ファイルを検知し、GitHub L1 Issue を作成する。
- **検索ベースの冪等性**: 起票前に `label:adr:xxx label:L1` で GitHub を検索し、既に存在する場合はスキップする。これにより、Git への書き戻しなしで二重起票を防止する。

### 2. 接着剤ラベル (Glue Labels) の導入
- **ADR識別ラベル**: `adr:xxx` (例: `adr:009`) を自動生成し、L1 Issue に付与する。
- **階層ラベル**: `L1` (ADR) ラベルを付与する。
- **自動作成**: 必要なラベルが GitHub 上にない場合は、ツールが API 経由で自動作成する。

## 検討した代替案 / Alternatives Considered
- **案A: Issue ID の ADR ファイルへの書き戻し**: Git の履歴を汚し、コンフリクトを誘発するため却下。ラベル検索の方がクリーンかつ確実である。

## 結果 / Consequences

### メリット (Positive consequences)
- **Traceability**: 設計の承認と管理 Issue が自動で同期され、ラベル一つで関連リソースを抽出できる。
- **Git Cleanliness**: Issue 番号を記録するための余計なコミットが不要になる。

### デメリット (Negative consequences)
- **API Dependency**: 起票前の検索により GitHub API の呼び出し回数が増加するが、レートリミットの範囲内で許容可能。

## 検証基準 / Verification Criteria
- [ ] `_approved` に新ファイルをマージした際、対応する L1 Issue が 1 件のみ作成されること。
- [ ] 作成された Issue に適切な `adr:xxx` および `L1` ラベルが付与されていること。

## 実装状況 / Implementation Status
未着手
