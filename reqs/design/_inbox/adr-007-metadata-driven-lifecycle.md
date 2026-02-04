# [ADR-007] メタデータ駆動型ライフサイクル管理 (Metadata-Driven Lifecycle Management)

- **Status**: 提案中
- **Date**: 2026-02-04

## 状況 / Context
本プロジェクト（Issue Creator Kit）では、これまで物理的なディレクトリ階層（`phase-1-domain` 等）によってタスクの実行順序やレイヤーを表現してきました。しかし、開発が進むにつれて以下の課題が顕在化しています。

1.  **認知負荷の増大:** ネストが深くなり、人間やAIエージェントが「ファイルをどこに置くべきか」を判断するコストが増大している。
2.  **柔軟性の欠如:** 複数のADRにまたがるタスクや、動的なフェーズ変更に対して、物理フォルダの移動を伴う管理は硬直的である。
3.  **ライフサイクル管理の不透明性:** 「先送り（Postponed）」や「廃止（Superseded）」といった、承認（Approved）以外の状態を管理する標準的なルールがなく、`_inbox` や `_archive` の運用が属人化している。

## 決定 / Decision
「物理構造による管理」を廃止し、**「メタデータ（YAML Frontmatter）による自律的ライフサイクル管理」**へ移行します。

### 1. ディレクトリ構造のフラット化
物理階層は「所有権（Context）」と「保存状態」のみを表すフラットな構造に限定します。

- **`reqs/design/`**:
    - `_inbox/`: 起草中・レビュー中の提案。
    - `_approved/`: 現在のシステムの正解（SSOT）となる承認済みドキュメント。
    - `_archive/`: 先送り（Postponed）、廃止（Superseded）、または役割を終えた記録。
- **`reqs/tasks/`**:
    - `<ADR-ID>/`: 該当する設計ドキュメントに紐づくタスクをフラットに配置する。例: `reqs/tasks/adr-007/task-1.md`

### 2. メタデータスキーマの定義
すべてのドキュメントとタスクは、以下の Frontmatter を保持することを必須とします。

#### ADR / Design Doc
ADR自体は GitHub Issue 化せず、PRによるレビューとマージ後のファイル保存によって SSOT を維持します。
```yaml
id: adr-007
status: Draft | Approved | Postponed | Superseded
date: 2026-02-04
```

#### Task (Issue Draft)
タスクは `issue_creator_kit` によって GitHub Issue 化され、実作業の管理に使用されます。
```yaml
id: T-1
parent: adr-007  # 紐づくADRのIDを記述
status: Draft | Ready | Completed | Cancelled
phase: domain | infrastructure | usecase | interface
depends_on: [T-0] # 必須: L3同士の前後関係（依存先ID）を記述。先行タスクが Completed になるまで着手不可。
issue_id: 456    # 起票後に自動追記される
```

### 3. ハイブリッド運用フロー（Hybrid Workflow）
ファイルベースの SSOT と GitHub Issue の利便性を統合した3層構造を採用します。

1.  **L1: ADR Issue (Branch-less Parent)**
    - **役割:** 設計変更全体の進捗を可視化する「管理コンテナ」。
    - **実体:** GitHub Issue。特定の Git ブランチには紐付かない。
    - **ライフサイクル:** ドキュメント承認時に自動起票され、全子タスク完了時にクローズされる。

2.  **L2: 統合 Issue (Integration)**
    - **役割:** フェーズ（Architecture, Spec, TDD）ごとの完了責任を持つ。
    - **実体:** GitHub Issue。ADR Issue の子として紐づく。
    - **メタデータ:** `type: integration` を指定。

3.  **L3: 実装タスク (Implementation Task)**
    - **役割:** 具体的なファイル変更（コード/ドキュメント）。
    - **実体:** GitHub Issue および Pull Request。
    - **マージ戦略:** **インクリメンタル・マージ**。巨大なPRを避けるため、タスク単位で小刻みに `main` へマージし、その都度 L2 Issue の進捗を更新する。

### 4. ステータス遷移と自動移動ルール
`issue_creator_kit` が以下のトリガーに基づき、物理ファイルを自動移動させます。

1.  **ADR / Design Doc**
    - **Draft -> Approved**: PRマージにより `_inbox` から `_approved` へ移動し、L1/L2 Issue を起票。
    - **Approved -> Superseded**: 上書き・廃止時に `_archive` へ移動。

2.  **Task (Issue Draft)**
    - **Draft -> Archived (起票と同時移動)**: 
        - PRマージをトリガーに GitHub Issue を起票。
        - **起票が成功した瞬間、ファイルを `reqs/tasks/_archive/` へ即座に移動**し、`issue_id` を記録する。
        - これにより、`reqs/tasks/<ADR-ID>/` は常に「起票待ちの予約票」のみが存在するクリーンな状態に保たれ、作業者はファイルの存在を意識せず GitHub Issue のみを参照して実装を行う。
    - **クローズ時**: GitHub Issue がクローズされても、ファイル側の操作（追加のコミット）は行わない。状態の同期が必要な場合は、CLI ツールがメモリ上で GitHub API から情報を取得する。

### 5. 抽象化された SSOT (Invisible File-based SSOT)
- **Backend (Git/File):** `reqs/tasks/` 配下のファイルは、Issue を「発行」するための予約券、および発行後の「控え」として機能します。
- **Frontend (GitHub Issue):** 起票後の唯一の正解（SSOT）は GitHub Issue です。
- **Noisy Commit の回避:** Issue のクローズ（実装完了）に連動したファイル移動を行わないことで、リポジトリへの不要な自動コミットや PR の発生を抑制します。

### 6. 責務の分離
- **人間 / AI エージェント:** GitHub Issue を中心に活動。タスク作成時のみ `tasks/<ADR-ID>/` へファイルを投入する。
- **CLI ツール:** 「裏方」としてファイルと Issue の整合性を保ち、物理ファイルのライフサイクルを隠蔽する。
- **GitHub:** 作業者との主たる対面窓口。

## 検討した代替案 / Alternatives Considered
- **案A: 現状のフォルダ階層の維持とマニュアル更新:** 認知負荷が解決せず、AIエージェントの自律性を損なうため却下。
- **案B: 完全なデータベース管理への移行:** File-based SSOT という本プロジェクトのコアコンセプト（Gitによるトレーサビリティ）に反するため却下。

## 結果 / Consequences

### メリット (Positive consequences)
- **ユーザビリティ:** 「どこにファイルを置くか」を迷わなくなり、AIエージェントによるタスク起票がスムーズになる。
- **透明性:** 依存関係（`depends_on`）が明示されるため、並列実行可能なタスクがシステム的に判断可能になる。
- **管理の堅牢性:** `_archive` の運用ルールが明確になり、SSOTの鮮度が保たれる。

### デメリット (Negative consequences)
- **CLIの複雑化:** ディレクトリトラバーサルではなく、依存関係グラフ（DAG）を解析するロジックの実装が必要になる。
- **移行コスト:** 既存ファイルを新しいスキーマに適合させるマイグレーション作業が発生する。

## 検証基準 / Verification Criteria
- [ ] `reqs/tasks/` 配下のファイルが2階層（`ADR-ID/file.md`）に収まっていること。
- [ ] 各ファイルに定義通りの YAML Frontmatter が含まれていること。
- [ ] CLIツールが `depends_on` を正しく解釈し、実行順序を提示できること（実装フェーズにて検証）。

## 実装状況 / Implementation Status
未着手（本ADRの承認後、移行ロードマップを作成予定）
