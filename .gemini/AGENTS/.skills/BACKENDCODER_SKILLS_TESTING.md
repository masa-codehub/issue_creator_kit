# スキル: テスト戦略と実装 (Skill: Testing Strategy & Implementation)

単にカバレッジ（網羅率）を高めるだけでなく、**仕様（Specs）が満たされていることを検証し、将来の変更からシステムを保護するための「生きたドキュメント」としてのテスト**を構築するプロセスです。

### Step 1: テストレベルの選定と計画 (Observe & Orient)

1.  **対象コードと仕様・価値の分析:**
    - **テスト価値の特定 (User-Value First):** このテストを追加することで、どのようなバグを防ぎ、ユーザー体験を守るのか（リグレッション防止、仕様理解の補助など）を言語化する。
    - `read_file` で以下のファイルを読み込み、テスト対象の実装と期待される振る舞いを詳細に分析する。
        - テストを追加・強化したいプロダクションコード (`src/...`)
        - プロダクションコードが依存しているインターフェース、DTO、定数定義
        - 関連する **SSOT (ADR/Design Doc)** (`reqs/design/_approved/`) と詳細仕様書 (`docs/specs/`) 
    - **テスト不足箇所の特定チェックリスト:**
        - [ ] **正常系の境界条件:** (例: リストの要素数が0, 1, 最大値の場合の挙動)
        - [ ] **異常系・エラー系:** (例: 不正なフォーマット、null/None、権限不足、タイムアウト)
        - [ ] **例外のスロー:** 仕様で定義された例外が、適切な条件で送出されているか？
        - [ ] **副作用の検証:** DB更新、イベント発行、ログ出力などの副次的な振る舞いがテストされているか？
        - [ ] **分岐網羅:** すべての if/else, match/case 分岐を通過するデータパターンが用意されているか？
    - **リスク予兆の検知 (Quantitative Check):**
        - 対象コードが外部依存（DB/API）と密結合しており、Mock化が困難でないか。
        - プライベートメソッドへの依存度が高すぎないか。

2.  **作業ブランチの準備と同期:**
    - **Issueの記述確認:** 担当Issueを確認し、「ベースブランチ」と「作業ブランチ」が明記されているかチェックする。
    - **指定がない場合:** **直ちに作業を中断する。** Issueにコメントし、正しいブランチ名の指示を仰ぐ。（勝手に `main` から作成してはならない）
    - **同期の実行:**
        - 1. ベースブランチ最新化: `run_shell_command("git checkout <base_branch> && git pull origin <base_branch>")`
        - 2. 作業ブランチへ切り替え: `run_shell_command("git checkout <working_branch> || git checkout -b <working_branch> <base_branch>")`
        - 3. 最新ベース取り込み: `run_shell_command("git rebase <base_branch>")`

3.  **テスト実装計画 (Testing Plan) の作成:**
    - 実装前に以下の **「テスト実装計画」** を作成し、ログとして出力する。
    - **制約:** このステップでは計画のみを行い、**プロダクションコードやテストコードの実ファイルを作成してはならない。**
        - **[Scope] テスト範囲:**
            - Type: Unit / Integration / E2E
            - Target: テスト対象のクラス/モジュール名
        - **[Spec] 根拠となる仕様:** どの仕様書のどのセクション（要件IDなど）を検証するか。
        - **[Strategy] 実装戦略:**
            - Data: テストデータの準備方法（Factory, Fixture, Builder）。
            - Mocking: 外部依存（DB, API）をどう処理するか（Mock, Fake, 実物）。
        - **[Scenarios] テストケース一覧:**
            - Case 1: `test_method_name` (Given / When / Then)
            - Case 2: ...
        - **[Contingency] 対応方針:**
            - テスト失敗時（バグ発見時）は修正するか、報告のみか。
            - テスト実装が困難な場合（依存過多など）の代替案。

    **アウトプット例:**
    ```markdown
    ## Testing Plan
    - **Scope:** Unit Test (`tests/domain/test_order.py`)
    - **Spec:** `docs/specs/order-spec.md` Section 3.1 "Order Validation Rules"
    - **Strategy:**
        - Data: `OrderFactory` (tests/factories.py) を使用してテストデータを生成。
        - Mocking: `UserRepository` は Mock を使用し、DB接続は行わない。
    - **Scenarios:**
        - `test_should_raise_error_when_items_are_empty`:
            - Given: 商品リストが空の注文データ, When: Order生成, Then: `DomainException.EmptyItems` 送出
        - `test_should_calculate_total_price_correctly`:
            - Given: 100円の商品2個, When: 合計計算, Then: 200円を返す
    - **Contingency:** テストが失敗した場合、実装コードの修正は行わず、`@pytest.mark.xfail` を付与してバグ報告Issueを作成する。
    ```

4.  **計画の整合性・網羅性チェック:**
    - 作成した Testing Plan が正しいか最終確認を行う。
    - `read_file` で担当Issue、**SSOT（承認済みADR/Design Doc）**、および仕様書を再度読み込む。
    - 以下の観点でセルフチェックを行い、**チェック結果（OK/NG）と、NGの場合の修正内容をログに出力する。**
        - **網羅性:** 仕様書（Spec）の要件がテストケースとして漏れなくリストアップされているか？
        - **効率性:** テストレベル（Unit/Integration）の選択が適切で、重複や無駄なテストが含まれていないか？
        - **整合性:** **SSOT**で定義されたテスト方針や、プロジェクト全体のテスト戦略と一致しているか？

### Step 2: テストの実装と検証 (Act & Verify)

1.  **テストコードの実装 (Implementation):**
    - **ファイル操作の注意:**
        - **新規作成:** `write_file` を使用する。
        - **既存追記:** `read_file` で既存内容を読み込み、新しいテストケースを追記した内容で `write_file` (上書き) するか、`replace` で適切な位置に挿入する。**既存のテストコードを消してはならない。**
    - **命名規則:** ユビキタス言語を用い、テストの意図（仕様）がメソッド名だけで伝わるようにする。
    
    **コード例:**
    ```python
    def test_should_reject_order_when_user_is_blacklisted():
        # Given: ブラックリスト入りしたユーザー
        user = UserFactory.create(status='BLACKLISTED')
        
        # When & Then: 注文しようとするとエラーになる
        with pytest.raises(DomainException.UserBlacklisted):
            OrderService.place_order(user, items=[ItemFactory.create()])
    ```

2.  **テストデータの準備 (Data Preparation):**
    - テストコード内で複雑なオブジェクト生成を行わず、**Factoryパターン**（オブジェクト生成を専門に行うクラス/関数）や **Builderパターン**（複雑なオブジェクトを段階的に構築する仕組み）を利用して可読性を高める。
    
    **Factoryパターンの例 (Helper Function):**
    ```python
    class UserFactory:
        @staticmethod
        def create(user_id="user-123", status="ACTIVE", **kwargs):
            # デフォルト値を持ち、必要な属性だけ上書き可能にする
            return User(
                id=user_id,
                status=Status[status],
                email=kwargs.get("email", "test@example.com")
            )
    ```

3.  **実行と検証:**
    - **Unit Test:** `run_shell_command("pytest -v -s tests/unit/...")`
    - **Integration Test:** `run_shell_command("pytest -v -s tests/integration/...")`
    - **失敗した場合:**
        - **再分析 (1回のみ):** エラーログを分析し、テストコードの実装ミスか、プロダクションコードのバグかを切り分ける。テスト側のミスであれば修正して再試行する。
        - **撤退:**
            - **Case A (バグ発見):** プロダクションコードのバグと特定された場合、**コードは修正せず**、テストを `pytest.mark.xfail` (またはコメントアウト) にしてコミットし、「バグ発見報告」としてPRを作成する。
            - **Case B (解決不能):** 原因不明の場合は、以下のコマンドで作業を破棄してベースブランチに戻り、終了する。
                - `run_shell_command("git reset --hard && git checkout <base_branch>")`

4.  **仕様との整合性チェック (Final Verification):**
    - テストが成功したとしても、「仕様書の意図」を正しく反映しているか、以下のチェックリストで最終確認する。
        - [ ] **振る舞いの検証:** `Assertion` は、内部の実装詳細（プライベートな属性や呼び出し順序）ではなく、外部から観測可能な「結果（戻り値、状態変化、発行されたイベント）」を対象としているか？
        - [ ] **ドメイン言語の反映:** `Assertion` やテストデータに、SSOTで定義された「ユビキタス言語」が正しく使われているか？
        - [ ] **境界値の網羅:** 計画（Step 1）で定義した境界条件が、実際のテストコードで全て検証されているか？
        - [ ] **説明的なエラーメッセージ:** テストが失敗した際、どの仕様のどの条件に違反したのかが容易に理解できるか？
        - [ ] **テストの独立性:** 他のテストの実行順序や、共有データの状態に依存せず、常に同じ結果（決定論的）を返すか？
        - [ ] **ドキュメント性:** テストコードを読むだけで、その機能の「正しい挙動」が仕様書を読まなくても理解できるほど明確か？

### Step 3: 品質保証と完了 (Verify & Finalize)

1.  **プロジェクト全体の静的解析:**
    - `run_shell_command("ruff check . && ruff format . && mypy .")` を実行し、プロジェクト全体の型安全性とスタイルを保証する。
    - **対応:** エラーが発生した場合は修正し、再度実行してパスすることを確認する。
        - **注意:** 修正対象は原則として**今回変更したファイル、およびその影響範囲**に限定する。既存の無関係なファイルのエラー（技術的負債）まで無理に修正しようとしてはいけない。

2.  **最終テスト実行:**
    - `run_shell_command("pytest -v -s")` を実行し、全体のリグレッションがないことを確認する。

3.  **プルリクエストの作成・更新:**
    - `list_pull_requests(head="<working_branch>")` で既存のPRを確認する。
    - **PRが存在しない場合:** `create_pull_request` で新規作成する。
    - **PRが存在する場合:** `update_pull_request` でタイトルや本文（下記内容）を更新する。
    - **記述内容:**
        - **User Value:** テスト追加によって保証された仕様や、発見されたバグの詳細。
        - **SSOT準拠:** どの仕様書（Spec）と紐付いているか。
        - **Coverage Impact:** カバレッジの向上度合い（定量的な数値があれば望ましい）。

4.  **活動報告:**
    - `add_issue_comment` で以下の内容を報告する。
        - **実装の成果:** 追加したテストと検証結果。
        - **設計整合性:** SSOTとの整合性確認結果。
        - **残課題 (Technical Debt Note):** まだテストできていない領域や、Mock化が難しくテストを断念した箇所があれば記録に残す。