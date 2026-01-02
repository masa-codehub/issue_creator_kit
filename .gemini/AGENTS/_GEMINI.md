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

- プルリクエストの管理 (PR Protocol)
  ドキュメントやコード実装の完了後、以下の規約（ガードレール）を遵守してプルリクエストを作成・管理する。

  1. **品質チェック (Quality Gate):**
     コミット前に、必ずプロジェクト指定のチェック（例: `pre-commit run --all-files`）をフル実行し、全項目パスさせる。
  
  2. **既存PRの確認:**
     重複を防ぐため、`list_pull_requests` で関連する既存PRがないか確認する。

  3. **新規作成 (Creation):**
     `create_pull_request` を実行する際は、**`head` (作業ブランチ) と `base` (マージ先) を必ず明示的に指定する**。デフォルト値に依存してはならない。
     - **Title:** `<type>(<scope>): <subject>` 形式。
     - **Body:**
       - **関連Issue:** `Closes #<Issue番号>`
       - **変更の概要:** 何をどのように変更したか。
       - **変更の目的:** なぜこの変更が必要か（背景とアウトカム）。
       - **検証方法:** 実施したテストや動作確認の手順。

  4. **更新通知:**
     既存PRへの追記時は `add_issue_comment` で変更点を要約して通知する。
     **コメント内容 (`body`) のテンプレート:**
     ```
     ## 更新内容
     - (変更点1)
     - (変更点2) 
     
     レビューをお願いします。 @Copilot
     ```

  5. **レビュアー指定:**
     `update_pull_request --pull_number <PR番号> --reviewers Copilot` を実行する。

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

## 1. プロジェクト進行フレームワーク (State Machine)
タスクを確実に遂行するための状態遷移モデルです。現在の自分の状態（State）を意識して行動してください。

### State 1: Planning (計画)
- **いつ:** タスク開始時、または予期せぬエラーで計画が破綻した時。
- **Action:** 
    1. **目標設定 (Goal Setting):** ユーザーとの会話から具体的な目標を特定し、**SMARTの法則**に基づいて自身が実行すべき内容を宣言する。
        - **エージェントのためのSMARTの法則:** 
            - **Specific (具体性):** 「どのファイルを」「どう変更するか」を特定する。曖昧な要求を具体的なツール操作（read_file, replace 等）に変換する。
            - **Measurable (計量性):** 完了を客観的に判定する基準（テストのパス、ビルド成功、特定のファイル生成など）を設ける。
            - **Achievable (達成可能性):** 現在利用可能なツールと権限の範囲内で、確実に完遂可能なステップに分解する。
            - **Relevant (関連性):** ユーザーの最終目的（Issue解決や機能追加）に対し、プロジェクトの規約やアーキテクチャに沿った価値を提供できるか確認する。
            - **Time-bound (期限):** 現在のターン（1回の応答）で確実にアウトプットを出せる範囲にスコープを限定し、進捗を明確にする。
        - **宣言の例:** 
          `run_shell_command{command: "echo '## Goal: <目標の内容> (SMARTに基づいた記述)'"}`
    
    2. **Todo作成 (`save_memory`):** 目的達成に必要な手順をTodoリストとして作成し、`save_memory` ツールを使用して自身の記憶に保存・提示する。
        - **ステータス管理テンプレート:** 
            - `[ ]`: 未実行 (Pending)
            - `[x]`: 完了 (Completed)
            - `[!]`: 失敗・要分析 (Failed / Needs Analysis)
            - `[-]`: スキップ (Skipped)
                - **ツールの使用例:** 
                  `save_memory{fact: "Current Todo: [x] タスク1, [ ] タスク2"}`
        
            3. **リスク評価 (Risk Assessment):**
               作成した計画がプロジェクトの成功を脅かさないか、以下の4点（4 Big Risks）で評価し、必要な対策をTodoに追加する。
                - **価値 (Value):** この作業は本当にユーザーやビジネスの価値向上に繋がるか？
                - **ユーザビリティ (Usability):** 提供する機能やコードは、利用者（開発者含む）にとって使いやすいか？
                - **実現可能性 (Feasibility):** 現在の技術スタック、スキル、時間内で現実的に完了できるか？
                - **ビジネス生存性 (Viability):** 法務、コスト、セキュリティ、コンプライアンス上の致命的な問題はないか？
        
        ### State 2: Execution (実行)- **いつ:** Todoリストがあり、Todoの内容に僅かな懸念も消えたとき
- **Action:** 
    1. **実行と適応:** Todoを順次実行する。
        - 適宜 `save_memory` を更新し、自身の進捗状況を把握し続ける。
        - **タスクが失敗または想定外の結果になった場合:** その場ですぐに修正を試みず、ステータスを `[!]`（失敗）として記録した上で、直ちに次のTodoへ進む。失敗したタスクを前提とする後続タスクがある場合はそれらを `[-]`（スキップ）とし、可能な限り全てのTodoを一通りやり遂げることを最優先する。

### State 3: Closing (完了・振り返り)
- **いつ:** 全てのTodoが `[x]` または `[-]` になった時。
- **Action:** 
    1. **振り返り (Retrospective):** 完了後、成果と課題を振り返り、**次のアクションを決定するため**の宣言を行う。状況に応じて以下のいずれか（または両方）を選択する。
        - **YWT (技術・タスクの深掘り):** 技術的な失敗や未知の挙動に直面した際に選択する。
            - **Y (やったこと):** 実行した操作と結果の事実。
            - **W (わかったこと):** 失敗のトリガー、ツールの制約、コードの依存関係など、次回の成功率を高めるための知見。
            - **T (次やること):** **仮説検証の提案**。「〇〇が原因だと推測されるため、次回は××というアプローチで検証する」という形式で記述する。**ここで提案した内容は、必ず次サイクルの最初のTodoに組み込むこと。**
        - **KPT (プロセス・効率の改善):** 作業の進め方やコミュニケーションに課題を感じた際に選択する。
            - **K (Keep):** スムーズに進行した手順、効果的だった判断。
            - **P (Problem):** 停滞の要因（情報の不足、スコープの肥大化など）。
            - **T (Try):** **具体的な作業手順の修正案、または新しい作業手順の定義**。次回からどのステップをどう変えるかを具体的に記述する。
        - `run_shell_command{command: "echo '## Retrospective: <選択した形式での内容>'"}`
    
    2. **メモリクリア (Memory Clear):** 次のタスクに備え、今回のタスクで使用した記憶を整理する。
        - `save_memory` に保存したTodoリストの内容を削除（または完了済みとしてクリア）する。
    
    3. **次のサイクルへ:** 必要に応じてState 1へ戻り、新たな目標を設定する。
        - **直前の振り返りで YWT の T (仮説検証) が出された場合は、その検証を最初の目標・Todoとして設定する。**

# 4. エラーからの回復 (トラブル対応)

## 1. 基本原則
- ツール実行時にエラーが発生した場合、決して同じコマンドを再実行せず、エラーメッセージを分析し、別のアプローチを検討する。

## 2. ケース別対応
- **`git push`失敗時 (`non-fast-forward`エラー):**
  次の操作でローカルブランチを更新する。
  `run_shell_command{command: "git pull --rebase"}`