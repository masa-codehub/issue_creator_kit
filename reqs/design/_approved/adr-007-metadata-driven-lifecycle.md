# [ADR-007] メタデータ駆動型ライフサイクル管理 (Metadata-Driven Lifecycle Management)

- **Status**: Approved (Supersedes [ADR-003](../_approved/adr-003-task-and-roadmap-lifecycle.md))
- **Date**: 2026-02-05

## 状況 / Context
本プロジェクト（Issue Creator Kit）では、これまで物理的なディレクトリ階層（`phase-1-domain` 等）によってタスクの実行順序やレイヤーを表現してきました（ADR-003）。しかし、開発が進むにつれて以下の課題が顕在化しています。

1.  **認知負荷の増大:** ネストが深くなり、人間やAIエージェントが「ファイルをどこに置くべきか」を判断するコストが増大している。
2.  **柔軟性の欠如:** 複数のADRにまたがるタスクや、動的なフェーズ変更に対して、物理フォルダの移動を伴う管理は硬直的である。
3.  **ライフサイクル管理の不透明性:** 「先送り（Postponed）」や「廃止（Superseded）」といった、承認（Approved）以外の状態を管理する標準的なルールがなく、`_inbox` や `_archive` の運用が属人化している。

これらを解決するため、ADR-003 で定義された「物理的な drafts/archive 構造」を廃止し、より柔軟なメタデータ駆動の構造へ移行します。

## 決定 / Decision
「物理構造による管理」を廃止し、**「メタデータ（YAML Frontmatter）による自律的ライフサイクル管理」**へ移行します。

### 1. ディレクトリ構造のフラット化
物理階層は「所有権（Context）」と「保存状態」のみを表すフラットな構造に限定します。

- **`reqs/design/`**:
    - `_inbox/`: 起草中・レビュー中の提案。
    - `_approved/`: 現在のシステムの正解（SSOT）となる承認済みドキュメント。
    - `_archive/`: 先送り（Postponed）、廃止（Superseded）、または役割を終えた記録。
- **`reqs/tasks/`**:
    - `<ADR-ID>/`: 該当する設計ドキュメントに紐づく起票待ちタスクの配置場所。
    - `_archive/`: 起票済み、または完了・中止された全タスクのアーカイブ場所（フラットに配置）。
- **`reqs/*/template/` (非推奨)**:
    - テンプレートの管理は **Skill Assets**（`.gemini/skills/*/assets/`）へ集約します。`reqs/` 配下のテンプレートフォルダは、歴史的経緯の維持またはローカルな一時利用を除き、SSOT としては機能しません。

### 2. メタデータスキーマの定義
すべてのドキュメントとタスクは、以下の Frontmatter を保持することを必須とします。

#### ADR / Design Doc
```yaml
id: adr-007
status: Draft | Approved | Postponed | Superseded
date: 2026-02-04
```

#### Task (Issue Draft)
```yaml
id: 007-T1                 # 形式: [ADR番号]-T[通し番号]。フェーズ（Arch/Spec/TDD）を跨いでも一貫した連番を使用。
                           # 設計思想: ADR毎に名前空間を分けることでプロジェクト全体での一意性を保証し、
                           # フェーズプレフィックスを排除することで依存関係（depends_on）の記述を簡素化する。
parent: adr-007
type: task | integration  # L2統合Issueの場合は integration、L3タスクの場合は task
status: Draft | Ready | Completed | Cancelled
phase: domain | infrastructure | usecase | interface | architecture | spec | tdd
roadmap: [ROADMAP-ID]      # 同期対象のロードマップID
depends_on: ["007-T0"]     # 必須。依存先のタスク ID (例: ["007-T0"]) を記述。依存がない場合は空配列 [] を指定
issue_id: 456              # 【自動追記】手動で設定しないでください
```

### 3. ハイブリッド運用フロー（Hybrid Workflow）
ファイルベースの SSOT と GitHub Issue の利便性を統合した3層構造を採用します。

1.  **L1: ADR Issue (Branch-less Parent)**
    - **役割:** 設計変更全体の進捗を可視化する「管理コンテナ」。GitHub Issue として起票される。
2.  **L2: 統合 Issue (Integration)**
    - **役割:** フェーズ（Architecture, Spec, TDD）ごとの完了責任を持つ。
3.  **L3: 実装タスク (Implementation Task)**
    - **役割:** 具体的なファイル変更。**インクリメンタル・マージ**戦略により、小刻みに `main` へ統合する。

### 4. ステータス遷移と自動移動ルール
`issue_creator_kit` が以下のトリガーに基づき、物理ファイルを自動移動させます。

- **ADR / Design Doc**
    - **Draft -> Approved**: PRマージにより `_inbox` から `_approved` へ移動し、L1/L2 Issue を起票。
- **Task (Issue Draft)**
    - **Draft -> Archived (起票と同時移動)**: 
        - PRマージをトリガーに GitHub Issue を起票。
        - **起票が成功した瞬間、ファイルを `reqs/tasks/_archive/` へ即座に移動**し、`issue_id` を記録する。
        - これにより、`reqs/tasks/<ADR-ID>/` は常に「起票待ちの予約票」のみが存在するクリーンな状態に保たれる。

### 5. 抽象化された SSOT (Invisible File-based SSOT)
- **Backend (Git/File):** `reqs/tasks/` 配下のファイルは、Issue を「発行」するための予約券、および発行後の「控え」として機能します。
- **Frontend (GitHub Issue):** 起票後の唯一の正解（SSOT）は GitHub Issue です。作業者は物理ファイルを意識する必要はありません。

## 検討した代替案 / Alternatives Considered
- **案A: 現状のフォルダ階層（ADR-003）の維持:** 認知負荷が解決せず、AIエージェントの自律性を損なうため却下。
- **案B: 完全なデータベース管理への移行:** File-based SSOT という本プロジェクトのコアコンセプトに反するため却下。

## 結果 / Consequences

### メリット (Positive consequences)
- **ユーザビリティ:** 「どこにファイルを置くか」を迷わなくなり、AIエージェントによるタスク起票がスムーズになる。
- **透明性:** 依存関係が明示されるため、並列実行可能なタスクがシステム的に判断可能になる。

### デメリット (Negative consequences)
- **CLIの複雑化:** 依存関係グラフ（DAG）を解析するロジックの実装が必要になる。
- **移行コスト:** 既存ファイルを新しいスキーマに適合させるマイグレーション作業が発生する。

## 検証基準 / Verification Criteria
- [ ] ADR-007 のステータスが `Supersedes ADR-003` となっていること。
- [ ] `reqs/tasks/_archive/` ディレクトリが存在すること。
- [ ] タスクのメタデータに `roadmap`, `type`, `depends_on` (必須) が含まれていること。

## 実装状況 / Implementation Status
未着手
issue_id: 260
