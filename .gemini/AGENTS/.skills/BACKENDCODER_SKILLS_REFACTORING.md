# スキル: リファクタリング (Skill: Refactoring)

「ボーイスカウト・ルール」に基づき、既存コードの内部品質を改善するプロセスです。単にコードを綺麗にするだけでなく、**SSOT (ADR/Design Doc/Specs)** で定義されたアーキテクチャの境界（Architecture Boundaries）を強化し、依存性のルールを遵守させることを主眼に置きます。

### Step 1: 構造分析と計画 (Observe & Orient)

1.  **構造分析と価値・リスクの把握:**
    - **改善価値の特定 (User-Value First):** なぜ今このリファクタリングが必要なのか？（可読性向上によるバグ予防、機能追加の準備など）を言語化する。
    - `read_file` で以下のファイルを読み込み、**コードの匂い (Code Smells)** と **アーキテクチャ違反 (Architectural Violations)** を特定する。
        - リファクタリング対象のプロダクションコード (`src/...`)
        - 対象に関連する上位レイヤーのインターフェース定義 (`src/domain/` または `src/usecase/`)
        - 依存関係を確認するための `__init__.py` や import セクション
    - **アーキテクチャ・チェック項目:**
        - [ ] **依存性の逆転:** Domain層が詳細（Infrastructure）に依存していないか？（import文の精査）
        - [ ] **責務の凝集度:** クラスやメソッドが複数の責務（例: ロジックと入出力、ロジックと永続化）を抱え込んでいないか？
        - [ ] **インターフェースの整合性:** リポジトリやサービスが、詳細なデータ構造を上位レイヤーに露出させていないか？
        - [ ] **コードの重複:** 複数のレイヤーで同じバリデーションや計算ロジックが分散して存在していないか？
    - `read_file` で関連する **SSOT (ADR/Design Doc/Specs)** を確認し、あるべき姿を再認識する。
    - **リスク予兆の検知 (Quantitative Check):**
        - 対象コードが巨大（300行超）または複雑（ネスト3階層超）でないか。
        - テストカバレッジが低い場合、リファクタリングは危険（High Risk）と判断する。

2.  **作業ブランチの準備と同期:**
    - **Issueの記述確認:** 担当Issueを確認し、「ベースブランチ」と「作業ブランチ」が明記されているかチェックする。
    - **指定がない場合:** **直ちに作業を中断する。** Issueにコメントし、正しいブランチ名の指示を仰ぐ。（勝手に `main` から作成してはならない）
    - **同期の実行:**
        - 1. ベースブランチ最新化: `run_shell_command("git checkout <base_branch> && git pull origin <base_branch>")`
        - 2. 作業ブランチへ切り替え: `run_shell_command("git checkout <working_branch> || git checkout -b <working_branch> <base_branch>")`
        - 3. 最新ベース取り込み: `run_shell_command("git rebase <base_branch>")`

3.  **安全網（テスト）の確認:**
    - `run_shell_command("pytest -v -s")` を実行し、リファクタリング前の状態で全てのテストがパスすることを確認する。
        - ※ 失敗時はリファクタリングを開始せず、まずバグ修正を行うか、テストを修正する。

4.  **リファクタリング計画 (Refactoring Plan) の作成:**
    - 実行前に以下の **「リファクタリング計画」** を作成し、ログとして出力する。
    - **制約:** このステップでは計画のみを行い、**プロダクションコードやテストコードの実ファイルを作成してはならない。**
        - **[Target] 対象:** 修正対象の具体的なファイルパスとシンボル。
        - **[As-Is] 現状の課題:** **コードの匂い**や**アーキテクチャ違反**と、SSOT（アーキテクチャルール）とのギャップ。
        - **[To-Be] あるべき姿:** SSOTに完全に準拠した理想的な状態。
        - **[Options] 解決案の比較:** To-Beに近づけるための複数のアプローチ。
            - 案A: （抜本的修正）
            - 案B: （暫定的/小規模修正）
        - **[Selection] 採用案と理由:** 最も変更リスクが小さく、かつ効果的な案を選択する。
        - **[Steps] 実行手順:** 選択した案の段階的な適用ステップ。
        - **[Contingency] 撤退ライン:** 作業時間の目安や、許容できない副作用。

    **アウトプット例:**
    ```markdown
    ## Refactoring Plan
    - **Target:** `src/interface/controllers/user_controller.py`
    - **As-Is:** `register` メソッド内で `email` のフォーマットチェック（正規表現）を直接行っている（Domainロジックの漏洩）。
    - **To-Be:** バリデーションロジックは全て Domain 層にカプセル化され、Controller はそれを利用するだけにする（ADR-005）。
    - **Options:**
        - **Option A (Full):** `EmailAddress` ValueObject を作成し、システム全体のメールアドレス扱いをこれに置き換える。
        - **Option B (Minimal):** `src/domain/rules.py` に `validate_email` 関数を作成し、Controllerから呼ぶ。
    - **Selection:** **Option B** (まずはロジックの移動のみを行い、型変更による広範な影響（Option A）を避けるため)
    - **Steps:**
        1. `src/domain/rules.py` に `validate_email` を実装（TDD）。
        2. Controller のロジックを `validate_email` 呼び出しに置換。
        3. テスト実行。
    - **Contingency:** 既存のテストケース修正が5件を超えたら、影響範囲過大としてRevertする。
    ```

5.  **計画の整合性・網羅性チェック:**
    - 作成した Refactoring Plan が正しいか最終確認を行う。
    - `read_file` で担当Issue、**SSOT (承認済みADR/Design Doc/Specs)** を再度読み込む。
    - 以下の観点でセルフチェックを行い、**チェック結果（OK/NG）と、NGの場合の修正内容をログに出力する。**
        - **網羅性:** 修正によって解決すべき課題が、SSOTの要求事項と一致しているか？ 修正漏れがないか？
        - **効率性:** 修正範囲が最小限に抑えられており、不要な変更（Over-engineering）が含まれていないか？
        - **整合性:** **SSOT**で定義されたアーキテクチャの原則や、依存性のルールを遵守しているか？

### Step 2: 実行と検証 (Act & Verify)

1.  **段階的な適用:**
    - 一度に多くのことをやらず、**「1回の移動につき1回のテスト実行」** を厳守する。
    - `read_file` で修正対象の最新内容を確認する。
    - `replace` (または `write_file`) を使用してコードを修正する。
        - **Tool Tip:** `replace` を使用する際は、`old_string` に十分なコンテキスト（前後3行程度）を含め、対象が一意に定まるようにする。

2.  **アーキテクチャの検証:**
    - コードを移動した後、import文を確認し、**「外側から内側への依存」** というルールが守られているかチェックする。
    - `run_shell_command("mypy .")` を実行し、型の不整合がないか確認する。

3.  **即時検証:**
    - `run_shell_command("pytest <relevant_test_path>")` を実行。
    - **失敗した場合:**
        1. **復元と再計画 (1回のみ):** `run_shell_command("git checkout .")` で変更を戻す。エラーログを分析し、より安全な手順（例: ステップをもっと細かくする）でPlanを修正して再試行する。
        2. **撤退:** 再度失敗した場合、以下のコマンドで作業を完全に破棄してベースブランチに戻り、状況を報告して終了する。
            - `run_shell_command("git reset --hard && git checkout <base_branch>")`

4.  **コミット:**
    - `run_shell_command("git add . && git commit -m 'refactor: [What] to improve [Why] based on [SSOT]'")`

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
        - **User Value:** このリファクタリングが将来の開発や保守にどう貢献するか。
        - **SSOT準拠:** どの設計原則（ADR/Clean Architecture）に基づく改善か。
        - **Architecture Check:** 依存性の循環などが解消されたことの自己申告。

4.  **活動報告:**
    - `add_issue_comment` で以下の内容を報告する。
        - **実装の成果:** 完了したリファクタリングと検証結果。
        - **設計整合性:** SSOTとの整合性確認結果。
        - **残課題 (Technical Debt Note):** 今回のスコープでは修正しきれなかったコードの匂いや、将来的にリファクタリングすべき箇所があれば記録に残す。