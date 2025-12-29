# 詳細仕様策定 (Specification Definition)

SYSTEM_ARCHITECTが策定した抽象的な意思決定（ADR/Design Doc）を、開発者が迷いなく実装できる具体的な「実行可能な設計図」に落とし込むプロセスです。

### Step 0: インプットの確認と分析 (Observe)

1.  **担当Issueの確認:**
    1.  `issue_read(method="get", issue_number=XXX)` を実行し、担当Issueの要件、背景、および親Issue/子Issueの情報を正確に把握する。
    2.  `issue_read(method="get_sub_issues", issue_number=XXX)` で依存するタスクが全て完了（CLOSED）していることを確認する。完了していない場合は作業を開始せず報告する。

2.  **決定事項・テンプレート・先行成果物の精読:**
    1.  `read_file(file_path="reqs/design/_approved/adr-XXX.md")` (またはDesign Doc) を読み込み、設計の目的、スコープ、ユビキタス言語、制約、検証基準を完全に把握する。
    2.  `read_file(file_path="docs/template/spec-template.md")` を読み込み、仕様書の標準フォーマットを確認する。
    3.  先行タスク（子Issue）で作成された成果物（ドキュメントやコード）がファイルシステム上に実在することを `list_directory` や `read_file` で検証する。

3.  **既存アーキテクチャ・関連ドキュメントの横断調査:**
    1.  `glob(pattern="docs/specs/**/*.md")` で関連する既存の仕様書を特定し、命名規則、データ構造、通信パターンの一貫性を調査する。
    2.  `read_file(file_path="docs/architecture/system-context.md")` や既存の `reqs/design/_approved/` 内の関連する決定事項を読み込み、システム全体の設計原則（クリーンアーキテクチャのレイヤー定義、エラーハンドリング方針等）を再確認する。
    3.  `search_file_content` を用い、`src/` 内の既存実装パターン（ベースクラス、共通ユーティリティ、インターフェース定義）を調査し、再利用可能な要素を特定する。

    **分析結果アウトプット例（作業ログとして出力）**
    ```markdown
    ## 既存資産・整合性分析レポート
    - **関連仕様書:** `docs/specs/user-auth-api.md` (命名規則チェック: OK)
    - **アーキテクチャ:** `adr-005` (Clean Architecture) に準拠する必要あり。
    - **実装パターン:** `src/shared/base_controller.py` を再利用可能。
    ```

4.  **成果物の定義 (Analysis-Driven Definition):**
    1.  Step 0-3 の分析結果に基づき、**「新規作成が必要なドキュメント」** と **「更新が必要な既存ドキュメント」** を整理し、作成するファイルパスを決定する。
    2.  **選定基準:**
        *   既存の仕様（API定義やDBスキーマ）への変更がある場合は、新規ファイルではなく既存ファイルの更新を優先する。
        *   複雑な新規ロジックやデータ構造が導入される場合は、詳細仕様書（`docs/specs/`）を新規作成する。
        *   アーキテクチャ全体に波及する変更（共通コンポーネントの追加等）がある場合は、アーキテクチャ図（`docs/architecture/`）の更新も成果物に含める。

    **成果物定義アウトプット例（作業ログとして出力）**
    ```markdown
    ## 成果物定義
    - **更新:** `docs/specs/user-api.md` (既存の `GET /users/{id}` への配送先フラグ追加)
    - **新規:** `docs/specs/recipient-registration-logic.md` (新規導入される配送先登録のバリデーション・永続化仕様)
    - **更新:** `docs/architecture/c4-model.md` (コンポーネント層への `RecipientService` の追記)
    ```

### Step 1: 設計案の具体化とドラフト作成 (Orient)

インプット情報を元に、**まず具体的な実装設計案を立案し、その後に整合性を検証します。**

1.  **コンポーネント・クラス設計 (Drafting):**
    1.  必要なクラス、モジュール、関数を洗い出す。
    2.  各コンポーネントの**責務、主要メソッド、依存関係**を定義し、既存のベースクラスやインターフェースをどのように継承・実装するかを明記する。

    **アウトプット例**
    ```markdown
    ### コンポーネント詳細
    - **`RecipientController` (src/interface/controllers/recipient_controller.py)**
        - **継承:** `BaseController`
        - **責務:** HTTPリクエストのバリデーション、Serviceの呼び出し、レスポンスの整形。
        - **依存:** `RecipientService`
    - **`RecipientService` (src/usecase/recipient_service.py)**
        - **責務:** 配送先登録のビジネスロジック（重複チェック、ドメインイベント発行）。
        - **主要メソッド:** `register_recipient(user_id: str, address: dict) -> Recipient`
        - **依存:** `RecipientRepository`, `EventDispatcher`
    - **`RecipientRepository` (src/infrastructure/db/recipient_repository.py)**
        - **実装:** `IRecipientRepository`
        - **責務:** `recipients` テーブルへのCRUD操作。SQLAlchemyモデルとのマッピング。
    ```

2.  **データモデル設計 (Drafting):**
    1.  データベースのテーブル構造（ER図）、カラム定義、データ型、制約を設計する。
    2.  既存テーブルへのカラム追加やリレーション変更がある場合、移行（Migration）の安全性も考慮する。
    3.  APIのリクエスト/レスポンスボディのJSONスキーマを設計する。

    **アウトプット例**
    ```markdown
    ### データモデル詳細
    - **Table: `recipients`**
        - `id`: `UUID` (PK, default=uuid4)
        - `user_id`: `UUID` (FK -> `users.id`, ON DELETE CASCADE, Indexあり)
        - `address_json`: `JSONB` (Not Null, 構造化された住所データ)
        - `created_at`: `DateTime` (default=now)
    - **Migration Plan:**
        - ファイル名: `versions/xxxx_create_recipients_table.py`
        - 安全性: 新規テーブル作成のため、既存データへのロック影響はなし。ダウンタイム不要。
    ```

3.  **インタラクション設計 (Drafting):**
    1.  コンポーネント間の連携やデータフローをシーケンス図（Mermaid記法）で表現する。
    2.  **トランザクション境界**や**例外発生時のフロー**（ロールバック等）を明確にする。
    3.  既存の通信パターンやエラーハンドリングガイドラインに従っていることを確認する。

    **アウトプット例**
    ```markdown
    ### インタラクション詳細
    #### 正常系シーケンス
    ```mermaid
    sequenceDiagram
        participant C as Client
        participant Ctrl as RecipientController
        participant Svc as RecipientService
        participant Repo as RecipientRepository
        
        C->>Ctrl: POST /recipients
        Ctrl->>Svc: register_recipient(data)
        Note over Svc, Repo: Transaction Start
        Svc->>Repo: save(entity)
        Repo-->>Svc: Success
        Svc->>Svc: publish_event("Registered")
        Note over Svc, Repo: Transaction Commit
        Svc-->>Ctrl: RecipientEntity
        Ctrl-->>C: 201 Created
    ```
    - **例外系:**
        - 重複エラー (`IntegrityError`) -> Serviceでキャッチし `DomainException.DuplicateRecipient` を送出 -> Controllerで `409 Conflict` に変換。
    ```

4.  **整合性とインパクトの分析 (Validation):**
    1.  **概念的整合性:** 上記で立案した設計案が、Step 0 で確認した既存の「ユビキタス言語」や「アーキテクチャ特性」と矛盾しないか検証する。
    2.  **インパクト分析:** 既存のAPIエンドポイントや共通モジュールへの変更が、他の機能に悪影響を与えないか（リグレッションリスク）を評価する。

    **アウトプット例**
    ```markdown
    ### 検証結果
    - **概念的整合性:**
        - OK: `User` と `Recipient` の分離は ADR-010 の指針に合致。
        - OK: `JSONB` 型の採用は、将来の住所フォーマット変更に備えるというアーキテクチャ特性（進化性）を満たす。
    - **インパクト分析:**
        - 注意: `user_id` に外部キー制約を貼るため、`users` テーブルの物理削除ができなくなる（論理削除への移行が必要か確認済み -> 問題なし）。
    ```

5.  **トレードオフの最終検討 (Final Decision):**
    1.  「既存パターンへの準拠」と「今回の要件への最適化」の間のトレードオフを検討し、採用した設計の理由（Why）を明確にする。

    **アウトプット例**
    ```markdown
    ### トレードオフ検討
    - **検討事項:** 住所のバリデーションロジックの配置場所
    - **案A (採用):** Domain Service (`RecipientValidationService`) に配置。
        - **理由:** 複数のユースケース（登録、更新）で再利用するため。また、バリデーションルールが複雑化する見込みがあるため。
    - **案B (却下):** Pydantic Model (`RecipientCreateRequest`) に配置。
        - **理由:** UI層のバリデーションにビジネスルールが漏れ出し、凝集度が下がるため。
    ```

6.  **仕様書ドラフトの作成:**
    1.  `docs/template/spec-template.md` の構造に基づき、上記の設計案を統合した**初稿（ドラフト）**を作成する。
    2.  `write_file(file_path="docs/specs/xxx.md")` を実行してファイルを保存する。

### Step 2: 自己レビューと仕様書の完成 (Act)

作成したドラフトを客観的な視点でレビューし、品質を高めてから完成版とします。

1.  **ドラフトの再読込:**
    1.  `read_file(file_path="docs/specs/xxx.md")` を実行し、Step 1 で作成した内容を客観的に読み返す。

2.  **自己レビュー (Self-Review):**
    1.  以下の **「品質保証チェックリスト」** に基づいて検証を行う。

    **品質保証チェックリスト**
    - [ ] **明確性:** 「多分」「おそらく」といった曖昧な表現がないか？
    - [ ] **具体性:** 全てのフィールドに型定義があり、主要なメソッドにシグネチャがあるか？
    - [ ] **網羅性:** 正常系だけでなく、異常系（エラー）やエッジケースの挙動が記述されているか？
    - [ ] **一貫性:** 既存のドキュメントやユビキタス言語と用語が統一されているか？
    - [ ] **視覚化:** 複雑なロジックやデータ構造が Mermaid で図解されているか？
    - [ ] **追跡可能性:** この仕様がどの ADR/Design Doc に基づくか、リンクが明記されているか？

3.  **修正と完成:**
    1.  チェックリストでの指摘事項があれば `replace` ツールで修正する。
    2.  修正が完了したら、関連するIssueやPRにコメントし、仕様書の作成完了を報告する。
    3.  次の担当者（PRODUCT_MANAGERや開発者）に実装タスクの開始を促す。
