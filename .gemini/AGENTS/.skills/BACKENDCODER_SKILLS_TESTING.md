# スキル: テスト戦略と実装 (Skill: Testing Strategy & Implementation)

**単にカバレッジを高めるだけでなく、仕様（Specs）が満たされていることを検証し、将来の変更からシステムを保護するための「生きたドキュメント」としてのテストを構築するプロセスです。**

このドキュメントは、BACKENDCODER が `~/.gemini/GEMINI.md` の「プロジェクト進行フレームワーク（State Machine）」を実行する際に参照するデータソースです。

---

## 1. Planning Phase Inputs (for State 1)

テスト追加計画策定時に、以下のステップで情報を収集し、Todoリストを具体化してください。

### 1.1 プロジェクト進行の初期化 (Protocol)
まず、`~/.gemini/GEMINI.md` の「3. プロジェクト進行（State Machine）」に従い、以下の手順を実行します。
1.  **SMART目標の設定:** テスト追加の具体的なゴール（どの仕様のどのケースをカバーするか）を定義する。
2.  **Todoリストの作成:** **ステータス管理テンプレート**を用いてTodoを作成し、`save_memory` に保存する。

### 1.2 能動的偵察 (Active Reconnaissance)
以下のコマンドと視点を用いて、テストが必要な箇所と検証すべき仕様を特定します。

*   **対象コードと仕様・価値の分析:**
    *   **テスト価値の特定 (User-Value First):** どのようなバグを防ぎ、ユーザー体験を守るかを言語化する。
    *   `read_file` でプロダクションコードと **SSOT (ADR/Design Doc/Specs)** を読み込む。
*   **テスト不足箇所の特定チェックリスト:**
    *   [ ] **正常系の境界条件:** (例: リスト0件, 1件, 最大件数)
    *   [ ] **異常系・エラー系:** (例: 不正フォーマット, null, 権限不足)
    *   [ ] **例外のスロー:** 仕様通りの例外が送出されるか？
    *   [ ] **副作用の検証:** DB更新、ログ出力などが検証されているか？
    *   [ ] **分岐網羅:** すべての if/else パターン。
*   **リスク予兆 (Quantitative Check):**
    *   外部依存（DB/API）と密結合しておりMock化が困難でないか確認。

### 1.3 作業ブランチの計画
*   **Action:** `~/.gemini/GEMINI.md` の **「1. Gitによるバージョン管理」** に従い、作業用ブランチを作成するタスクをTodoの先頭に追加する。
    *   Naming: `test/add-coverage-{対象}`

### 1.4 Testing Plan の作成 (Detailed Output)
Todoリストを作成・更新する際、以下のフォーマットで具体的かつ詳細な「Testing Plan」を策定し、ログに出力してください。

**アウトプット例 (Testing Plan):**
```markdown
## Testing Plan
- **Scope:** Unit Test (`tests/domain/test_order.py`)
- **Spec:** `docs/specs/order-spec.md` Section 3.1 "Order Validation Rules"
- **Strategy:**
    - Data: `OrderFactory` (tests/factories.py) を使用。
    - Mocking: `UserRepository` は Mock を使用し、DB接続は行わない。
- **Scenarios:**
    - `test_should_raise_error_when_items_are_empty`:
        - Given: 商品リストが空の注文データ, When: Order生成, Then: `DomainException.EmptyItems` 送出
    - `test_should_calculate_total_price_correctly`:
        - Given: 100円の商品2個, When: 合計計算, Then: 200円を返す
- **Contingency:** テストが失敗した場合、実装コードの修正は行わず、`@pytest.mark.xfail` を付与してバグ報告Issueを作成する。
```

---

## 2. Execution Phase Actions (for State 2)

Todoを実行する際、以下のステップで効果的なテストを追加します。

### 2.1 Test Design & Implementation

#### Step 1: テストコードの実装 (Implementation)
*   **Action:** `write_file` (新規) または `read_file` -> `write_file`/`replace` (追記) を使用。**既存テストを消さない。**
*   **Naming:** ユビキタス言語を用い、意図が伝わるメソッド名にする。

#### Step 2: テストデータの準備 (Factory Pattern)
*   **Guideline:** 複雑なオブジェクト生成には **Factoryパターン** や **Builderパターン** を利用し、テストコードの可読性を高める。
    ```python
    # Good: Factory使用
    user = UserFactory.create(status='BLACKLISTED')
    ```

#### Step 3: 実行と検証
*   **Action:** `pytest -v -s <path>` を実行。
*   **Failure Analysis:**
    *   **Case A (バグ発見):** 実装コードのバグなら、**コードは修正せず** `pytest.mark.xfail` にして「バグ報告」としてPRする。
    *   **Case B (解決不能):** 作業を破棄してベースブランチに戻る。

#### Step 4: 仕様との整合性チェック
*   [ ] **振る舞いの検証:** 内部実装ではなく「結果」を検証しているか？
*   [ ] **ドメイン言語:** アサーションにユビキタス言語が使われているか？
*   [ ] **独立性:** 他のテストに依存していないか？

---

## 3. Closing Phase Criteria (for State 3)

タスク完了時に、以下の完全性チェックを実行してください。

### 3.1 最終監査 (Final Audit)
成果物に対して、以下の監査を行います。

*   **[品質]**
    *   [ ] 全てのテストがパスしているか？ (`pytest -v -s`)
    *   [ ] Linter/Formatter (ruff, mypy) のチェックをパスしているか？（**今回変更した範囲限定**）
*   **[網羅性]**
    *   [ ] 計画したテストケース（正常系、異常系、境界値）は全て実装されたか？

**判定:** チェックリストに一つでも「No」がある、または少しでも「懸念」が残る場合は、**必ずテストまたは実装を修正し、再度この監査を実行してください（合格するまで繰り返す）。**

### 3.2 成果物の定着

1.  **PR作成/更新:** User Value（保証された仕様、発見されたバグ）、SSOT準拠、Coverage Impact を記述。

### 3.3 プロジェクト進行の完了 (Closing Protocol)
`~/.gemini/GEMINI.md` の「3. プロジェクト進行（State Machine）」に従い、以下の手順を実行してタスクをクローズします。

1.  **振り返り (Retrospective):** YWTまたはKPTを用いて成果と課題を振り返り、**次のアクション（仮説検証や改善案）**を宣言する。
    *   `run_shell_command("echo '## Retrospective: ...'")`
2.  **メモリクリア:** `save_memory` に保存したTodoリストを完了済みに更新（または削除）する。
3.  **活動報告:** `add_issue_comment` で成果、設計整合性、残課題（テスト断念箇所など）に加え、振り返りの内容を報告する。
