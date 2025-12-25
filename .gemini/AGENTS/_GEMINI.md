# 1. 基本操作 (Core Operations)

## 1. Gitによるバージョン管理

- 作業開始前にローカルブランチをリモートの最新状態に完全に同期させるために次の操作を実行する。
  `run_shell_command{command: "git pull --rebase origin <base_branch>"}`

- 作業ブランチを新規に作成する時は、通常 `base_branch` を明示的に指定して `feature_branch` を作成する。
  `run_shell_command{command: "git checkout -b <feature_branch> <base_branch>"}`

- 変更内容を確認する時は、次の操作を実行する。
  `run_shell_command{command: "git status"}`

- 変更内容をコミット対象にする時は、すべての変更をステージングエリアに追加する。
  `run_shell_command{command: "git add ."}`

- 変更内容をローカルリポジトリに記録する時は、次の操作を実行する。
  `run_shell_command{command: "git commit -m \"...\""}`

  **コミットメッセージの書き方:**
  `...` の部分には、変更内容を分かりやすく記述する。
  以下の形式が推奨される。

  `<type>: <subject>`

  - **type の例:**
    - `feat`: 新機能の追加
    - `fix`: バグ修正
    - `docs`: ドキュメントの変更
    - `chore`: 上記以外の変更（保守作業など）
  - **subject の例:**
    - `ユーザー登録機能を追加`
    - `ログイン時の認証バグを修正`

- 作業完了後、コンフリクトをチェックしてからリモートに反映させるために次の手順で操作する。
  1. まず、マージ先の最新の変更を取り込む。
     `run_shell_command{command: "git pull --rebase origin <base_branch>"}`
  2. **マージコンフリクトが発生した場合:**
     以下の手順でコンフリクトを解消する。
     1. まず`run_shell_command{command: "git status"}`でコンフリクトしているファイルをすべて特定する。
     2. 各ファイルの内容を`read_file`で読み込み、コンフリクトマーカー(`<<<<<<<`, `=======`, `>>>>>>>`)を確認する。
     3. 手動で解決策を構築し、`write_file`や`replace`を使ってファイルを修正する。
     4. 修正後、`run_shell_command{command: "git add ."}`で解決済みとしてマークし、`run_shell_command{command: "git status"}`で解消されたことを確認する。
        `run_shell_command{command: "git add . && git status"}`
  3. コンフリクトがなければ、プッシュを実行する。
`run_shell_command{command: "git push"}`

- プルリクエストの管理
  変更のマージレビューを依頼する時や、その後の運用は次の手順で操作する。

  1. **コミット前の品質チェック:**
     すべての変更をコミットする前に、`pre-commit`フックをフル実行して品質を保証する。
     `run_shell_command{command: "pre-commit run --all-files"}`
  
  2. **既存PRの確認:**
     まず、既存のプルリクエストがないか確認する。
     `list_pull_requests`

  3. **新規作成:**
     プルリクエストがなければ、タイトルと本文を指定して新規作成する。
     `create_pull_request --title "<title>" --body "<body>" --head "<feature_branch>" --base "<base_branch>"`

     **タイトル (`title`) の書き方:**
     `<type>(<scope>): <subject>` という形式が推奨される。
     - 例: `feat(api): ユーザー認証機能を追加`

     **本文 (`body`) の書き方:**
     以下の項目を記述することが推奨される。
     - **関連Issue:** `Closes #<Issue番号>`
     - **変更の概要:**
     - **変更の目的:**
     - **検証方法:**

  4. **更新通知:**
     既存のプルリクエストに新しいコミットをプッシュした後は、次の操作で更新を通知する。
     `add_issue_comment --issue_number <PR番号> --body "<コメント内容>"`

     **コメント内容 (`body`) のテンプレート:**
     ```
     ## 更新内容
     - (変更点1)
     - (変更点2)
     
     レビューをお願いします。 @Copilot
     ```

  5. **レビュアーの指定:**
     プルリクエストにレビュアーを指定する時は、次の操作を実行する。
     `update_pull_request --pull_number <PR番号> --reviewers Copilot`

## 2. ファイル操作

- 自分のコンテキストを把握するために次の操作を実行する。
  `read_file ~/.gemini/GEMINI.md`
  `read_file .gemini/AGENTS/_GEMINI.md`

- ファイルの内容を確認する時は、次の操作を実行する。
  `read_file <file_path>`

- ファイルを安全に部分置換するために、次の手順で操作する。
  1. 書き換え対象のファイルを読み込む。
     `read_file <file_path>`
  2. 取得した内容を基準に、`old_string`と`new_string`を指定して置換する。
     `replace --file_path <file_path> --old_string "..." --new_string "..."`
  3. 最後に `read_file <file_path>` でファイルの内容を確認する。

- ファイルの末尾に行を追加する時は、次の手順で操作する。
  1. `read_file <file_path>` でファイルの内容を全て読み込む。
  2. 読み込んだ内容の末尾に、追加したい文字列を結合する。
  3. `write_file --file_path <file_path> --content "<結合した内容>"` でファイルを上書きする。
  4. 最後に `read_file <file_path>` でファイルの内容を確認する。

- ファイルの特定の行間にコードを追加する時は、次の手順で操作する。
  1. `read_file <file_path>` でファイルの内容を全て読み込む。
  2. 読み込んだ内容（文字列）に対して、追加したい箇所に新しいコードを挿入する。
  3. `write_file --file_path <file_path> --content "<挿入後の内容>"` でファイルを上書きする。

---

# 2. 品質保証 (Quality Assurance)

## 1. Pythonにおける静的解析とテスト
コードの品質を保証するため、以下の手順でチェックを実行する。

1.  **Linterと型チェック (事前):**
    まず、Linterと型チェッカーを実行し、問題を修正する。
    `run_shell_command{command: "ruff check . && ruff format ."}`
    `run_shell_command{command: "mypy ."}`

2.  **自動テストとデバッグ:**
    次に、自動テストを実行する。テストが失敗した場合は、以下のワークフローで効率的に修正と確認を行う。

    1.  **失敗箇所の特定:**
        まず `-v` オプションをつけて実行し、どのテストが失敗しているか把握する。
        `run_shell_command{command: "pytest -v"}`
    2.  **失敗テストへの集中:**
        前回失敗したテストのみを対象に実行し、確認サイクルを高速化する。
        `run_shell_command{command: "pytest --lf"}`
    3.  **詳細なデバッグ:**
        `-s` (print文の表示) や `--pdb` (対話的デバッガの起動) と組み合わせて原因を調査する。
        `run_shell_command{command: "pytest --lf -s"}` または `run_shell_command{command: "pytest --lf --pdb"}`
    4.  **修正と再実行:**
        コードを修正し、`run_shell_command{command: "pytest --lf"}` で素早く確認する。
    5.  **最終確認:**
        失敗したテストがすべて通ったら、最後に全テスト (`run_shell_command{command: "pytest"}`) を実行して他に影響がないか確認する。

3.  **Linterと型チェック (事後):**
    自動テストの修正が他の問題を引き起こしていないか確認するため、再度Linterと型チェックを実行する。
    `run_shell_command{command: "ruff check . && ruff format ."}`
    `run_shell_command{command: "mypy ."}`

---

# 3. プロジェクト進行 (Project Progression)

## 1. コミュニケーション

- タスクの進捗を関連Issueに報告する時は、次の操作を実行する。
  `add_issue_comment`

- 活動報告テンプレート
    ```
    ## 1. 目的とゴール
    - **解決したいIssue:** #
    - **この作業の目的:**
    - **ゴール(完了条件):**

    ## 2. 実施内容
    - **作業ブランチ:**
    - **主要な変更ファイル:**
    - **コミットリスト:**

    ## 3. 検証結果
    - **実行したテスト:**
    - **テスト結果:**

    ## 4. 影響範囲と今後の課題
    - **影響範囲:**
    - **残課題と次のアクション:**
    ```

- 確認事項の問い合わせテンプレート
    ```
    ## 要確認事項
    現在、Issue #xxx の対応を進めておりますが、判断に必要な情報が不足しているため、作業を中断いたしました。お手数ですが、以下の点についてご確認の上、ご指示いただけますでしょうか。

    ---

    ### 1. 状況の概要
    - **実行していたタスク:**
    - **参照していたドキュメント:**

    ### 2. 発生した問題・不明点
    (何が、なぜ問題となったのかを具体的に説明します。)

    ### 3. 判断のための具体的な質問
    (はい/いいえ、または具体的な値で答えられる質問を箇条書きで記述します。)
    1.  質問1
    2.  質問2

    ### 4. 提案（任意）
    (可能であれば、解決策の選択肢を提示し、人間の意思決定をサポートします。)

    ### 5. 現在の状態と次のアクション
    - **現在の状態:** 作業前のクリーンな状態です。
    - **次のアクション:** ご回答をいただき次第、ご指示に沿って作業を再開します。
    ```

## 2. エラーからの回復 (トラブル対応)

### 1. 基本原則
- ツール実行時にエラーが発生した場合、決して同じコマンドを再実行せず、エラーメッセージを分析し、別のアプローチを検討する。

### 2. ケース別対応
- **`git push`失敗時 (`non-fast-forward`エラー):**
  次の操作でローカルブランチを更新する。
  `run_shell_command{command: "git pull --rebase"}`
