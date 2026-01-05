# 概要 / Overview
デザインドキュメント: 仮想キューとフェーズ連鎖の論理フロー詳細設計 (ADR-003 実装詳細)

- **Author(s)**: Developer Experience チーム
- **Status**: 下書き
- **Last Updated**: 2026-01-04

## 背景と課題 / Background
ADR-003 において、物理的な `_queue` フォルダを廃止し、`archive/` へのマージ差分をトリガーとする「仮想キュー」方式への移行が決定された。
しかし、以下の詳細なロジックが未定義であり、実装上の曖昧さが残っている。
1.  **差分検知の厳密性**: 他の変更と混ざった場合に、起票対象ファイルだけを正確に抽出する方法。
2.  **原子性の保証**: ネットワークエラー等で一部の Issue 起票が失敗した際の状態不整合（二重起票や書き込み漏れ）の防止。
3.  **ロードマップ同期の確実性**: ロードマップ内のリンク（Markdown テーブル）を破壊せずに、正規表現等で安全に置換・追記する方法。
4.  **フェーズ連鎖の安全装置**: 自己増殖的な PR 作成による無限ループや、コンフリクト発生時の自動停止。

## ゴール / Goals
- 開発者が PR をマージするだけで、後続フェーズの準備（Auto-PR）とロードマップ更新が全自動かつ安全に完了する。
- 異常発生時には「何もしない（Fail-fast）」ことで、SSOT である Git リポジトリの整合性を 100% 維持する。
- スパイク調査（`docs/spikes/git-diff-logic.md`）で得られた知見を統合し、実機で動作可能なアルゴリズムを確定させる。

## 設計 / Design

### ハイレベル設計 / High-Level Design
GitHub Actions (push to main) を起点とした一連のフローを以下に示す。

```mermaid
sequenceDiagram
    participant GitHub as GitHub Actions (push)
    participant ICK as Issue Creator Kit (CLI)
    participant Repo as Git Repository (main)
    participant API as GitHub API

    GitHub->>ICK: 実行 (before_sha, after_sha)
    ICK->>Repo: git diff-tree で archive/ への追加ファイルを特定
    ICK->>ICK: ファイル内容の Frontmatter を読み取り
    Note right of ICK: issue 番号がないものだけを抽出

    rect rgb(200, 230, 255)
        Note over ICK, API: 【原子的一括起票】
        ICK->>API: 各ファイルの Issue を作成
        API-->>ICK: Issue 番号取得
        ICK->>ICK: メモリ上のファイルバッファに番号を書き戻し
    end

    rect rgb(230, 255, 230)
        Note over ICK, Repo: 【ロードマップ同期】
        ICK->>Repo: 関連ロードマップを特定・読み込み
        ICK->>ICK: リンクを Draft -> Archive へ置換、番号追記
        ICK->>Repo: ロードマップを書き換え
    end

    rect rgb(255, 230, 230)
        Note over ICK, Repo: 【フェーズ連鎖 (Auto-PR)】
        ICK->>ICK: next_phase_path の有無を確認
        ICK->>Repo: 次フェーズ用 Foundation ブランチ作成
        ICK->>Repo: on new branch: ファイル移動 (Draft -> Archive)
        ICK->>API: 起票用 PR を作成
    end

    ICK->>Repo: 全変更をコミット & Push
```

### 詳細設計 / Detailed Design

#### 1. 差分検知アルゴリズム (Virtual Queue Detection)
- **コマンド**: `git diff-tree -r --no-commit-id --name-status --diff-filter=A --no-renames ${before} ${after} -- reqs/tasks/archive/`
- **フィルタリングルール**:
    1.  取得したファイルリストのうち、拡張子が `.md` であるもの。
    2.  各ファイルの YAML Frontmatter をパースし、`issue` フィールドが存在しない、あるいは空であるもの。
- **エッジケース**: 一つの PR で複数のフェーズ（フォルダ）のファイルが `archive/` に入った場合も、ICK はそれらを一括で処理対象とする。

#### 2. 原子的一括起票 (Atomic Batch Creation)
- **All-or-Nothing 戦略**:
    - 全ての対象ファイルについて、Issue 作成 API をコールする。
    - **1件でも失敗した場合**:
        - すでに作成された Issue を削除（または Close）しようとするのではなく、処理を中断してエラーを吐き、Git への書き戻しコミット（Frontmatter の `issue` フィールド更新およびロードマップ更新）を一切行わない。
        - このため、失敗したバッチ内のファイルは全て `issue` フィールドが空のままとなり、差分検知アルゴリズム（「`issue` フィールドが存在しない、あるいは空であるもの」を対象とする）により、再実行時に再度一括起票の対象となる。
        - 途中まで作成された Issue が存在する場合でも、それらは Frontmatter から参照されていない「孤立 Issue」として一時的に残る。再実行時には、失敗したバッチ内の全ファイルが再度一括起票の対象となるため、これら孤立 Issue に対応する新規 Issue が追加で作成され（二重起票が発生する）。この二重起票は、Git 上の原子性と一貫性を優先するために許容する fail-fast 戦略上のトレードオフとみなす。
        - 孤立 Issue の扱いについては、運用ポリシーとして定期的な手動 Close（またはラベル付け）を行うか、別途クリーンアップジョブを検討する。
    - **成功時**:
        - メモリ上の各ファイルオブジェクトに Issue 番号をセットし、次の処理ステップへ渡す。
        - 全ての Issue 作成が完了した後にのみ、一括してファイルへの書き戻しとコミットを実行する。

#### 3. ロードマップ同期 (Roadmap Sync Engine)
- **置換ロジック**:
    - ロードマップ Markdown ファイルを 1 行ずつスキャン、または正規表現置換を行う。
    - `| (Task ID) | ... | [ファイル名](../../tasks/drafts/(パス)) |` 形式の行を特定。
    - `../../tasks/drafts/` を `../../tasks/archive/` に置換。
    - リンクテキストの末尾、または備考欄に ` (#IssueNumber)` を追記する。
- **安全策**: 置換対象のリンクが見つからない場合は、ロードマップとタスクファイルの不整合が発生している可能性が高いため、単なる警告ではなくエラーとして扱い処理を中断する。原因が解消されるまで自動同期処理を完了済みとみなさない。

#### 4. フェーズ連鎖と Auto-PR (Phase Chaining)
- **トリガー条件**:
    - 今回起票された（`archive/` に入った）ファイルの中に、`next_phase_path` メタデータを持つものが存在すること。
- **処理フロー**:
    1.  `next_phase_path` (例: `reqs/tasks/drafts/phase-2/`) の存在を確認。
    2.  `git checkout -b feature/phase-N-foundation` を実行。
    3.  `next_phase_path` で指定されたディレクトリ（例: `reqs/tasks/drafts/phase-2/`) 内の全ファイルを、`drafts` を `archive` に置換したパス（例: `reqs/tasks/archive/phase-2/`）へ `git mv` を使って移動する。
    4.  `git add . && git commit -m "feat: promote phase-N tasks for virtual queue"`
    5.  `git push origin feature/phase-N-foundation`
    6.  GitHub API で PR を作成。`base: main`, `head: feature/phase-N-foundation`。
- **無限ループ防止**:
    - `next_phase_path` から算出される**移動先**ディレクトリ（例: `reqs/tasks/archive/phase-2/`）が既に存在する場合は、二重処理とみなして無視する。
    - フェーズ連鎖処理中は、「訪問済み `next_phase_path` セット（例: `visited_phase_paths`）」を保持し、各ステップで次に処理しようとしている `next_phase_path` がこのセットに既に含まれている場合は「循環参照」と判断して、後続のフェーズ連鎖（Auto-PR 作成）を即座に中止し、警告ログを出力する。
    - さらに安全装置として、フェーズ連鎖の最大深度（例: `MAX_PHASE_CHAIN_DEPTH = 10`）を定義し、連鎖回数がこの上限を超える場合も異常系とみなして処理を停止する（新規 PR は作成しない）。
    - PR 作成時に、同一の `head` ブランチ名が既に存在する場合も、安全のため処理をスキップする。

#### 5. 安全装置 (Safety Mechanisms)
- **Fail-fast**: 以下のいずれかで失敗した場合は、即座に終了し、Git リポジトリを汚さない（Push しない）。
    - ネットワークエラーによる API 失敗。
    - `git push` 時のコンフリクト（別の Actions や人間による変更）。
- **冪等性**: `issue` 番号が既に Frontmatter にあるファイルは無視するため、Actions が再試行されても二重起票は発生しない。

## パフォーマンスとレートリミット / Performance & Rate Limiting
- GitHub Issue 作成 API のセカンダリレート制限（最大 80 件/60 秒）を考慮し、Issue 起票は 1 バッチあたり最大 50 件とする。
- バッチ間に 60 秒のインターバル（例: `sleep 60`）を設けることで、100 件以上の一括起票時にもレートリミットエラーを回避する。
- レートリミットエラー（HTTP 403 かつ `retry-after` ヘッダあり）を受け取った場合は、`retry-after` の秒数に安全マージン 5 秒を加えた時間だけ待機してから、未処理分の起票をリトライする。

## 検討した代替案 / Alternatives Considered
- **案: Issue 作成直後に逐次コミット**: コミットログが汚れ、ロードマップ更新との整合性が取りにくいため却下。「一括処理・一括コミット」を採用。
- **案: `archive/` 移動を Actions 内で行う**: 人間が PR で「どのタスクを完了とするか」を明示的に操作する（レビューする）プロセスを重視するため、現在の「マージ後に起票」案を採用。

## セキュリティとプライバシー / Security & Privacy
- `GITHUB_TOKEN` の権限として、`contents: write` (コミット用) および `issues: write` (起票用) が必要。
- 秘密情報の漏洩はないが、自動 PR 作成により意図しない通知が飛ぶ可能性があるため、ロードマップでの事前定義を SSOT とする。

## 未解決の問題 / Open Questions & Unresolved Issues
- 特になし。GitHub Issue 作成 API のレートリミット対策は設計に取り込んだ。

## 検証基準 / Verification Criteria
- [ ] 模擬リポジトリにおいて、`drafts/` から `archive/` へのファイル移動を含む PR をマージした際、Actions が発火し、Issue が起票されること。
- [ ] 起票された Issue の番号が、元の md ファイルの Frontmatter に正しく書き戻されていること。
- [ ] ロードマップ内のリンクが `drafts` から `archive` に書き換わり、Issue 番号が付与されていること。
- [ ] `next_phase_path` がある場合、次フェーズの移動 PR が自動作成されること。
- [ ] 途中でネットワークを切断した際、中途半端な Issue 番号の書き込みやロードマップ更新が行われないこと（原子性）。
