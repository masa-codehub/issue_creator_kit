# スキル: TDDによる実装 (Skill: TDD Implementation)

Issueで要求されたバグ修正や新機能の実装を、TDDサイクル（Red-Green-Refactor）を用いて安全かつ確実に実装するための標準プロセスです。単にテストを通すだけでなく、上位の設計（**SSOT (ADR/Design Doc/Specs)**）と整合した「正しい実装」を行うことを目的とします。

### Step 1: コンテキストと仕様の整合 (Observe & Orient)

1.  **仕様・設計・価値の完全把握:**
    - **ユーザー価値の特定 (User-Value First):** `issue_read` で要件だけでなく「背景(Why)」を読み解く。この実装がユーザーにどのような具体的な価値（または苦痛の解消）をもたらすかを言語化する。
        - ※ Issueに背景が明記されていない場合は、コンテキストから推測して「仮説」として宣言するか、不明点としてユーザーに質問する。
    - **設計の参照:** 関連する **SSOT (ADR/Design Doc)** (`reqs/design/_approved/`) と詳細仕様書 (`docs/specs/`) を読み込む。**特に「ユビキタス言語」と「依存性のルール」を確認する。**
    - **トレーサビリティの確保:** これから実装するコードが、どの仕様書のどのセクションに対応するかを特定する。

2.  **既存コードとテストの調査:**
    - `read_file` で以下の関連ファイルを読み込み、現状の設計と振る舞いを詳細に把握する。
        - 修正対象、または機能的に類似している既存のプロダクションコード (`src/<package>/<layer>/...`)
        - それらに対応する既存のテストコード (`tests/<test_type>/...`)
        - `src/domain/` 配下の関連するエンティティや値オブジェクトの定義
        - `src/usecase/` 配下の関連するインターフェース（Abstract Base Class）定義
    - **アーキテクチャ・整合性チェック:** 以下のチェック項目を洗い出し、現状を評価する。
        - [ ] **レイヤーの正当性:** 実装対象の機能やクラスは、クリーンアーキテクチャの定義（Domain, UseCase, Interface, Infrastructure）に基づき、正しいレイヤーのディレクトリに配置されているか？
        - [ ] **依存の方向:** 上位レイヤー（例: Domain）が下位レイヤー（例: Infrastructure）のモジュールを直接 import していないか？（依存性逆転の原則の遵守）
        - [ ] **責務の分離:** ビジネスロジックが Interface（Controller等）や Infrastructure（Repositoryの具体的実装等）に漏れ出していないか？
        - [ ] **ユビキタス言語の適用:** クラス名、メソッド名、変数名がプロジェクトで合意された用語と一致しているか？
    - **リスク予兆の検知 (Quantitative Check):**
        - ファイルサイズが大きすぎる（目安: 300行以上）
        - 条件分岐が深すぎる（ネストが3階層以上）
        - 既存ロジックに対するテストが存在しない
        - ※ これらに該当する場合は「高リスク」と判断し、Contingency Planを厚めに設定する。
    - 現状のテストがパスすることを確認する: `run_shell_command("pytest -v -s")`
        - ※ 失敗した場合は `pytest --lf -vv` を実行して詳細な差分と直前の失敗を確認し、原因を特定する。

3.  **作業ブランチの準備と同期:**
    - **Issueの記述確認:** 担当Issueを確認し、「ベースブランチ」と「作業ブランチ」が明記されているかチェックする。
    - **指定がない場合:** **直ちに作業を中断する。** Issueにコメントし、正しいブランチ名の指示を仰ぐ。（勝手に `main` から作成してはならない）
    - **同期の実行:**
        - 1. ベースブランチを最新化: `run_shell_command("git checkout <base_branch> && git pull origin <base_branch>")`
        - 2. 作業ブランチへ切り替え（存在しない場合は作成）: `run_shell_command("git checkout <working_branch> || git checkout -b <working_branch> <base_branch>")`
        - 3. 最新のベースを取り込む: `run_shell_command("git rebase <base_branch>")`
            - ※ コンフリクトが発生した場合は、自動で解決を試みず、直ちに作業を中断し、コンフリクトしているファイルを報告する。

4.  **TDDサイクルの設計 (TDD Planの作成):**
    - Step 2に進む前に、以下の項目を含む **「TDD実装計画」** を作成し、ログ（またはコメント）として出力する。
    - **制約:** このステップでは計画のみを行い、**プロダクションコードやテストコードの実ファイルを作成してはならない。**
        - **[Red] テスト設計:**
            - 作成するテストファイルパス: `tests/...`
            - テストケース名（ユビキタス言語）: `test_...`
            - シナリオ (Given/When/Then): 「XXの状態でYYした時、ZZとなること」
            - **期待される失敗 (Red Condition):** 具体的にどのようなエラーで失敗することを期待するか（例: `AssertionError`, `ModuleNotFoundError` はNGとし、インターフェース定義後は `NotImplementedError` や `AssertionError` を狙う）
        - **[Green] 実装設計:**
            - 修正対象ファイルパス: `src/...`
            - クラス/メソッドのシグネチャ: `def method_name(arg: Type) -> ReturnType:`
            - 依存関係: どのインターフェースやクラスを利用するか（アーキテクチャ違反がないか事前確認）
        - **[Refactor] 改善仮説:**
            - 予想されるコードの匂いと、適用予定のリファクタリング手法（例: 「条件分岐が複雑になるため、Strategyパターンを検討する」）
        - **[Contingency] 想定外時の対応方針:**
            - テストが想定通りに失敗しない（既にパスしてしまう）場合の対応: （例: テスト条件を見直す、または実装済みとみなして次へ進む）
            - 実装が想定より複雑化した場合の撤退ライン: （例: 「変更ファイルが3つを超えたら設計を再考する」）
            - **撤退時の手順:** 作業ブランチの変更を破棄し、ベースブランチに戻る手順を明記する。（例: `git reset --hard && git checkout <base_branch>`）

    **アウトプット例:**
    ```markdown
    ## TDD Plan
    - **Red:** `tests/domain/test_user.py` に `test_cannot_change_email_when_account_locked` を追加。
      - Given: ロックされたUser, When: email変更, Then: DomainException送出。
      - **Expected Failure:** まだガード節を実装していないため、例外が発生せず `pytest.raises(DomainException)` が `AssertionError` で失敗する。
    - **Green:** `src/domain/user.py` の `change_email` メソッドに `is_locked` チェックを追加。
    - **Refactor:** `is_locked` 判定ロジックが複数箇所にある場合、プロパティまたはガード節として共通化する。
    - **Contingency:** 既存ロジックと競合してGreenにならない場合は、無理に修正せず変更を破棄(`git reset --hard`)し、ベースブランチ(`main`)に戻って仕様担当に問い合わせる。
    ```

5.  **計画の整合性・網羅性チェック:**
    - 作成したTDD Planが正しいか最終確認を行う。
    - `read_file` で担当Issue、**SSOT（承認済みADR/Design Doc）**、および仕様書を再度読み込む。
    - 以下の観点でセルフチェックを行い、**チェック結果（OK/NG）と、NGの場合の修正内容をログに出力する。**
        - **網羅性:** Issueや仕様書の要件（Acceptance Criteria）が、テストケースとして漏れなくリストアップされているか？
        - **シンプルさの追求 (YAGNI):** 「念のため」の汎用化や、仕様にない機能が含まれていないか？ 最もシンプルな実装になっているか？
        - **整合性:** **SSOT**で禁止されているパターン（例: Infrastructureへの直接依存）が含まれていないか？

### Step 2: 実行 (Act)

1.  **Red (失敗するテストの作成):**
    - **ファイル操作の注意:**
        - **新規作成:** `write_file` を使用する。
        - **既存追記:** `read_file` で既存内容を読み込み、新しいテストケースを追記した内容で `write_file` (上書き) するか、`replace` で適切な位置に挿入する。**既存のテストコードを消してはならない。**
    - **検証:** `run_shell_command("pytest <path_to_new_test>")` を実行。
        - **成功 (OK):** **TDD Planで定義した「期待される失敗」と一致する理由**で失敗した場合。
        - **失敗 (NG):** コンパイルエラー、Importエラー、または**テストがパスしてしまった**場合。
            - **再試行 (1回のみ):** `read_file` で関連コードを再確認し、テストコードまたはインポートパスを修正して再度 `pytest` を実行する。
            - **撤退:** それでも期待通りの失敗にならない場合、以下のコマンドで作業を完全に破棄してベースブランチに戻り、状況を報告して終了する。
                - `run_shell_command("git reset --hard && git checkout <base_branch>")`
    - `run_shell_command("git add . && git commit -m 'test: add failing test for [feature/bug] linked to [Spec/SSOT]'")`

2.  **Green (最小限の実装):**
    - `read_file` で修正対象の最新内容を確認する。
    - `write_file` または `replace` を使い、`src/` ディレクトリにコードを実装する。
        - **Tool Tip:** `replace` を使用する際は、`old_string` に十分なコンテキスト（前後3行程度）を含め、対象が一意に定まるようにする。
    - **制約:**
        - **YAGNI:** テストをパスさせるために**絶対に必要なコード以外は1行も書いてはならない。** 将来のための汎用化や、予備的な実装は禁止する。
        - **依存ルール:** レイヤー間の依存ルール（外側から内側への依存）は絶対に遵守する。
    - **検証:** `run_shell_command("pytest <path_to_new_test>")` を実行。
        - **失敗した場合:**
            - **再試行 (1回のみ):** `read_file` で実装とエラーログを再確認し、修正を行って再度 `pytest` を実行する。
            - **撤退:** 再度失敗した場合、以下のコマンドで作業を完全に破棄してベースブランチに戻り、状況を報告して終了する。
                - `run_shell_command("git reset --hard && git checkout <base_branch>")`
    - `run_shell_command("git add . && git commit -m 'feat(TDD): implement minimum logic to pass test'")`

3.  **Refactor (アーキテクチャ準拠のリファクタリング):**
    - `read_file` で対象コードの最新内容を確認する。
    - **改善:**
        - **Clean Code:** 重複の排除、長いメソッドの分割。
        - **Naming:** 変数名やメソッド名を、より実態を表すユビキタス言語にリネームする。
        - **Boy Scout Rule:** 変更箇所の周辺にある小さな「コードの匂い」も修正する。ただし、**編集中のファイル内のみに限定し、関係ないファイルには触れないこと。**
    - **検証:** `run_shell_command("pytest")` を実行し、リグレッションがないことを確認する。
        - **失敗した場合:**
            - **復元と再計画 (1回のみ):** `run_shell_command("git checkout .")` で変更を戻す。その後、コードを再読込してより安全なリファクタリング計画を立て直し、再試行する。
            - **撤退:** 再度失敗した場合（またはリスクが高いと判断した場合）、以下のコマンドで作業を完全に破棄してベースブランチに戻り、状況を報告して終了する。
                - `run_shell_command("git reset --hard && git checkout <base_branch>")`
    - `run_shell_command("git add . && git commit -m 'refactor(TDD): align with architecture boundaries'")`

### Step 3: 品質保証と完了 (Verify & Finalize)

1.  **プロジェクト全体の静的解析:**
    - `run_shell_command("ruff check . && ruff format . && mypy .")` を実行し、プロジェクト全体の型安全性とスタイルを保証する。
    - **対応:** エラーが発生した場合は修正し、再度実行してパスすることを確認する。
        - **注意:** 修正対象は原則として**今回変更したファイル、およびその影響範囲**に限定する。既存の無関係なファイルのエラー（技術的負債）まで無理に修正しようとしてはいけない。

2.  **最終テスト実行:**
    - 静的解析や自動整形による意図しない不具合が発生していないか確認するため、再度全てのテストを実行する。
    - `run_shell_command("pytest -v -s")`

3.  **プルリクエストの作成・更新:**
    - `list_pull_requests(head="<working_branch>")` で既存のPRを確認する。
    - **PRが存在しない場合:** `create_pull_request` で新規作成する。
    - **PRが存在する場合:** `update_pull_request` でタイトルや本文（下記内容）を更新する。
    - **記述内容:**
        - **User Value:** この変更がユーザーにどのような具体的なメリットをもたらすか。
        - **SSOT準拠:** どの仕様書（Spec）のどの項目を満たし、どの設計（ADR）に従ったか。
        - **Architecture Check:** 依存性のルールや責務分離が守られていることの自己申告。

4.  **活動報告:**
    - `add_issue_comment` で以下の内容を報告する。
        - **実装の成果:** 完了したタスクと検証結果。
        - **設計整合性:** SSOTとの整合性確認結果。
        - **残課題 (Technical Debt Note):** 今回のスコープでは修正しきれなかったコードの匂いや、将来的にリファクタリングすべき箇所があれば記録に残す。