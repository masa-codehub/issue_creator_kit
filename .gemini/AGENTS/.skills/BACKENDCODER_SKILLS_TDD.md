# スキル: TDDによる実装 (Skill: TDD Implementation)

**Issueで要求されたバグ修正や新機能の実装を、TDDサイクル（Red-Green-Refactor）を用いて安全かつ確実に実装するための標準プロセスです。**

このドキュメントは、BACKENDCODER が `~/.gemini/GEMINI.md` の「プロジェクト進行フレームワーク（State Machine）」を実行する際に参照するデータソースです。

---

## 1. Planning Phase Inputs (for State 1)

実装計画策定時に、以下のステップで情報を収集し、Todoリストを具体化してください。

### 1.1 プロジェクト進行の初期化 (Protocol)
まず、`~/.gemini/GEMINI.md` の「3. プロジェクト進行（State Machine）」に従い、以下の手順を実行します。
1.  **SMART目標の設定:** 実装タスクの具体的なゴール（どのファイルのどのメソッドを実装し、どのテストを通すか）を定義する。
2.  **Todoリストの作成:** **ステータス管理テンプレート**を用いてTodoを作成し、`save_memory` に保存する。

### 1.2 能動的偵察 (Active Reconnaissance)
以下のコマンドと視点を用いて、実装に必要なコンテキストを収集し、Todoの詳細を埋めます。

*   **仕様・設計・価値の完全把握:**
    *   **ユーザー価値の特定 (User-Value First):** `issue_read` で要件だけでなく「背景(Why)」を読み解く。
    *   **設計の参照:** 関連する **SSOT (ADR/Design Doc)** (`reqs/design/_approved/`) と詳細仕様書 (`docs/specs/`) を読み込み、**「ユビキタス言語」と「依存性のルール」**を確認する。
    *   **既存コード調査:** `read_file` で関連ファイル（プロダクションコード、テスト、ドメイン定義）を読み込む。
*   **アーキテクチャ・整合性チェック:**
    *   [ ] **レイヤーの正当性:** 実装対象の機能は、クリーンアーキテクチャの定義（Domain, UseCase, Interface, Infrastructure）に基づき、正しいディレクトリに配置されているか？
    *   [ ] **依存の方向:** 上位レイヤーが下位レイヤーを直接 import しないか？
    *   [ ] **責務の分離:** ビジネスロジックが Interface や Infrastructure に漏れ出していないか？
    *   [ ] **ユビキタス言語:** クラス名、メソッド名がプロジェクトで合意された用語と一致しているか？

### 1.3 作業ブランチの計画
*   **Action:** `~/.gemini/GEMINI.md` の **「1. Gitによるバージョン管理」** に従い、作業用ブランチを作成するタスクをTodoの先頭に追加する。
    *   Naming: `feat/issue-{Issue番号}` 等

### 1.4 TDD Plan の作成 (Detailed Output)
Todoリストを作成・更新する際、以下のフォーマットで具体的な「TDD Plan」を策定し、ログに出力してください。**実ファイル作成前に計画を立てることで手戻りを防ぎます。**

**アウトプット例 (TDD Plan):**
```markdown
## TDD Plan
- **Red:** `tests/domain/test_user.py` に `test_cannot_change_email_when_account_locked` を追加。
  - **Scenario:** Given: ロックされたUser, When: email変更, Then: DomainException送出。
  - **Expected Failure:** まだガード節を実装していないため、例外が発生せず `AssertionError` で失敗する。
- **Green:** `src/domain/user.py` の `change_email` メソッドに `is_locked` チェックを追加。
- **Refactor:** `is_locked` 判定ロジックが複数箇所にある場合、プロパティまたはガード節として共通化する。
- **Contingency:** 既存ロジックと競合してGreenにならない場合は、無理に修正せず変更を破棄(`git reset --hard`)し、ベースブランチに戻る。
```

---

## 2. Execution Phase Actions (for State 2)

Todoを実行する際、以下の **TDDサイクル** を厳守して実装を進めます。

### 2.1 The TDD Cycle (Strict Protocol)

#### Step 1: Red (失敗するテストを書く)
*   **Action:** 新規作成には `write_file`、追記には `read_file` -> `write_file` (または `replace`) を使用する。**既存のテストを消してはならない。**
*   **Verify:** `pytest <path>` を実行。
    *   **Success:** TDD Planで定義した「期待される理由」で失敗した。
    *   **Failure:** コンパイルエラー、Importエラー、または**パスしてしまった**場合。
        *   -> 再試行 (1回のみ) または撤退 (Reset & Report)。

#### Step 2: Green (最小限の実装)
*   **Action:** `src/` ディレクトリにコードを実装する。
*   **Constraint (YAGNI):** テストをパスさせるために**絶対に必要なコード以外は1行も書いてはならない。** 将来のための汎用化は禁止。
*   **Verify:** `pytest <path>` を実行。失敗した場合は再試行または撤退。

#### Step 3: Refactor (アーキテクチャ準拠)
*   **Action:**
    *   **Clean Code:** 重複排除、長いメソッドの分割。
    *   **Naming:** ユビキタス言語へのリネーム。
    *   **Boy Scout Rule:** 変更箇所の周辺にある小さな「コードの匂い」も修正（**編集中のファイル内限定**）。
*   **Verify:** `pytest` (全体または関連範囲) を実行。

### 2.2 自律的解決と撤退 (Autonomy & Contingency)
*   **三振ルール:** 同じアプローチで2回失敗したら、立ち止まって仮説を見直す。
*   **撤退手順:** 解決不能と判断した場合、`git reset --hard && git checkout <base_branch>` でベースに戻り、状況を報告して終了する。

---

## 3. Closing Phase Criteria (for State 3)

タスク完了時に、以下の完全性チェックを実行してください。

### 3.1 最終監査 (Final Audit)
実装したコードとテストに対して、以下の監査を行います。

*   **[品質]**
    *   [ ] 全てのテストがパスしているか？ (`pytest -v -s`)
    *   [ ] Linter/Formatter (ruff, mypy) のチェックをパスしているか？（**今回変更した範囲限定**）
    *   [ ] デバッグコードが残っていないか？
*   **[SSOT整合性]**
    *   [ ] ドメイン層に技術的詳細（フレームワーク依存）が混入していないか？
    *   [ ] 依存性のルール（外側から内側への依存）は守られているか？
    *   [ ] IssueのAcceptance Criteriaを全て満たしているか？

**判定:** チェックリストに一つでも「No」がある、または少しでも「懸念」が残る場合は、**必ずコードを修正し、再度この監査を実行してください（合格するまで繰り返す）。**

### 3.2 成果物の定着

1.  **PR作成/更新:** `create_pull_request` または `update_pull_request`。
    *   **Body:** User Value（ユーザーへの価値）、SSOT準拠（どのSpec/ADRに従ったか）、Architecture Check（自己申告）を含める。

### 3.3 プロジェクト進行の完了 (Closing Protocol)
`~/.gemini/GEMINI.md` の「3. プロジェクト進行（State Machine）」に従い、以下の手順を実行してタスクをクローズします。

1.  **振り返り (Retrospective):** YWTまたはKPTを用いて成果と課題を振り返り、**次のアクション（仮説検証や改善案）**を宣言する。
    *   `run_shell_command("echo '## Retrospective: ...'")`
2.  **メモリクリア:** `save_memory` に保存したTodoリストを完了済みに更新（または削除）する。
3.  **活動報告:** `add_issue_comment` で成果、設計整合性、残課題（Technical Debt）に加え、振り返りの内容を報告する。
