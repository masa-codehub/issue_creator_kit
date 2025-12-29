# アーキテクチャ可視化 (Architecture Visualization)

システムの現状（Current State）を正確に把握し、全体像を見失わないようにするためのプロセスです。コードベースの変更に合わせて定期的に更新し、開発者のメンタルモデルと実際のコードを一致させます。

### Step 0: インプットと現状の把握 (Observe)

1.  **担当Issueと依存関係の確認:**
    1.  `issue_read(method="get", issue_number=XXX)` を実行し、アーキテクチャ更新の目的と範囲を把握する。
    2.  `issue_read(method="get_sub_issues", issue_number=XXX)` を使い、依存タスク（子Issue）が全て **CLOSED** になっていることを確認する。完了していない場合は作業を開始せず報告する。

2.  **先行タスク成果物の実在検証 (Verification of Deliverables):**
    1.  **成果物の特定:** `issue_read(method="get_comments", issue_number=XXX)` を実行し、子Issueの完了報告コメントから「Pull Request番号」や「作成されたファイルパス」の情報を特定する。
    2.  **変更内容の把握:** PR番号が特定できた場合は `pull_request_read(method="get_diff", pullNumber=YYY)` を、ファイルパスのみの場合は `read_file` を実行し、アーキテクチャ図に反映すべき「新しい構造的事実」を抽出する。
    3.  **実在確認:** `list_directory` や `read_file` を使い、特定した主要な変更ファイルがファイルシステム上に実際に存在することを自分の目で確認する。

3.  **コードベースの構造と実行単位の調査:**
    1.  `list_directory(dir_path="src/")` を実行し、最新のパッケージ構成を確認する。
    2.  **インフラ構成の確認:** `read_file(file_path="docker-compose.yml")`, `Dockerfile`, `Procfile` 等を読み込み、システムがどのような「実行プロセス（コンテナ）」で構成されているかを特定する。
    3.  `read_file(file_path="pyproject.toml")` (または `package.json` 等) を読み込み、外部依存ライブラリの追加・変更を確認する。
    4.  `glob(pattern="src/**/*.py")` (プロジェクトの言語に合わせて拡張子を調整) を活用し、主要なエントリポイント、モジュール、クラスの配置を特定する。

4.  **既存アーキテクチャドキュメントの確認:**
    1.  `read_file(file_path="docs/system-context.md")` および `docs/architecture/c4-model.md` を読み込む。
    2.  `read_file(file_path="docs/template/c4-model-template.md")` を読み込み、記述フォーマットを確認する。
    3.  **ギャップ分析:** Step 0-2 (先行成果物) および Step 0-3 (コード実態) と、現在のドキュメントを比較し、As-Is / To-Be の形式で乖離を特定する。

    **分析結果アウトプット例（作業ログ）**
    ```markdown
    ## ギャップ分析レポート

    | 対象コンポーネント | As-Is (コードの実態) | To-Be (ドキュメント記述) | 対応方針 |
    | :--- | :--- | :--- | :--- |
    | `PaymentGateway` | `src/infrastructure/external/` に新規実装済み。 | 外部システムとしてContext図に追加。 | `docs/system-context.md` の更新案を作成 |
    | `UserService` | `NotificationService` に依存。 | 依存関係の矢印が不足している。 | `docs/architecture/c4-model.md` の更新案を作成 |
    ```

### Step 1: 構造化と図解ドラフト作成 (Orient)

Step 0 の**ギャップ分析結果（As-Is/To-Be）に基づき**、更新が必要なコンテナ・コンポーネントを特定して詳細定義を行い、ドラフトを作成します。

1.  **コンテナレベルの分析・定義 (Level 2):**
    1.  **フォーマットの確認:** `read_file(file_path="docs/template/c4-model-template.md")` を読み込む。
    2.  **更新対象の特定:** ギャップ分析レポートに基づき、新規追加・変更があった「実行プロセス（docker-composeのservice等）」に焦点を当てる。
    3.  **選定分析:** 各プロセスについて、アーキテクチャ図に「コンテナ」として載せるべきか判断する。

    **選定分析アウトプット例**
    ```markdown
    | プロセス名 | 採用/不採用 | 判断理由 |
    | :--- | :--- | :--- |
    | `api` | **採用** | システムのメイン機能を担うWeb/APIサーバーであるため。 |
    | `worker` | **採用** | メイル送信や集計など、アーキテクチャ上重要な非同期処理を担うため。 |
    | `redis` | **採用** | キューおよびキャッシュとして、コンテナ間の連携に不可欠なミドルウェアであるため。 |
    | `log-router` | **不採用** | インフラ補助的なサイドカーであり、ビジネスロジックには直接関与しないため省略。 |
    ```

    4.  採用したコンテナの **技術スタック** と **主要な責務** を定義する。

2.  **コンポーネントレベルの分析・定義 (Level 3):**
    1.  **更新対象の特定:** ギャップ分析で特定されたコンテナ、またはモジュール構成に変更があったコンテナを選択する。
    2.  **コンポーネント分析:** パッケージ構造や主要クラスを調査し、アーキテクチャ的に意味のある「論理グループ」を特定・グルーピングする。

    **コンポーネント分析アウトプット例**
    ```markdown
    | パッケージ/クラス | 分析 | コンポーネント定義 |
    | :--- | :--- | :--- |
    | `src/interface/controllers/payment_*.py` | 複数のControllerクラスが存在するが、責務は「決済APIの提供」で共通。 | **PaymentController** (Group) |
    | `src/usecase/payment_service.py` | ビジネスロジックの中核。単独で重要。 | **PaymentService** (Single Class) |
    | `src/domain/payment/validator.py` | Serviceから呼ばれる補助クラス。単独で図示すると細かすぎる。 | -> PaymentServiceに内包させる（図示しない） |
    | `src/infra/db/payment_repo.py` | DBアクセスの抽象化。アーキテクチャ的に重要。 | **PaymentRepository** |
    ```

    3.  特定したコンポーネントの **種類** と **責務** を定義する。

3.  **関係性の定義 (Relationship):**
    1.  特定した要素間の **「依存の向き」** と **「通信手段/呼び出し方法」** を定義する。

4.  **Mermaidドラフトの作成:**
    1.  定義した内容を統合し、テンプレートに沿って Mermaid 記法のドラフトを作成する。
    2.  L1 (System Context) の更新が必要な場合は、`docs/system-context.md` の修正案も併せて作成する。

    **Mermaidドラフト例**
    ```mermaid
    C4Component
    title Component Diagram - Payment Service
    
    Container_Boundary(api, "API Application") {
        Component(ctrl, "PaymentController", "FastAPI", "Handles payment requests")
        Component(svc, "PaymentService", "Python", "Business logic for payments")
        Component(repo, "PaymentRepository", "SQLAlchemy", "Persists payment data")
        
        Rel(ctrl, svc, "Uses")
        Rel(svc, repo, "Uses")
    }
    ```

### Step 2: 自己レビューとドキュメントの更新 (Act)

作成したドラフトを客観的な視点で検証し、公式ドキュメントに反映させます。

1.  **ドラフトと基準情報の読み込み:**
    1.  `read_file(file_path="...")` を使用して、Step 1 で作成した図解のドラフト内容を読み込む。
    2.  **基準情報の再確認:** 検証の基準として、以下の情報を読み込み（または再確認）する。
        - 担当Issue: `issue_read(method="get", issue_number=XXX)`
        - システムコンテキスト: `read_file(file_path="docs/system-context.md")`
        - 関連するADR: `read_file(file_path="reqs/design/_approved/adr-XXX.md")`
    3.  作成したドラフトが、Step 0 で特定したギャップ（As-Is/To-Be）を過不足なく解消しているか再確認する。

2.  **自己レビュー (Self-Review):**
    1.  以下の **「アーキテクチャ図品質チェックリスト」** に基づいて検証を行う。

    **アーキテクチャ図品質チェックリスト**
    - [ ] **抽象度の統一:** C1にクラス名が混ざっていないか？ C3に詳細なインフラ設定が混ざっていないか？
    - [ ] **凡例と方向:** 矢印の意味は明確か？ 向きは正しいか（通常は依存元 -> 依存先）？
    - [ ] **現状一致:** 図の内容は「現在のコード（現実）」を正確に反映しているか？
    - [ ] **説明責任:** 図だけでは伝わらない設計意図が、テキストで補足されているか？
    - [ ] **整合性 (Consistency):** 担当Issueの要件、`docs/system-context.md`、関連ADRと矛盾していないか？
    - [ ] **適正範囲 (Scope):** 必要な要素の漏れ（不足）や、要求されていない過剰な構造（Over-Engineering）がないか？

3.  **ドキュメントの更新:**
    1.  `write_file` または `replace` を使用して、対象ファイル（`docs/system-context.md` または `docs/architecture/c4-model.md`）を更新する。

4.  **完了通知:**
    1.  更新した内容と背景をIssue等で報告し、アーキテクチャの同期完了を伝える。