# スキル: リファクタリング (Skill: Refactoring)

**「ボーイスカウト・ルール」に基づき、既存コードの内部品質を改善するプロセスです。SSOT (ADR/Design Doc/Specs) で定義されたアーキテクチャの境界を強化し、依存性のルールを遵守させることを主眼に置きます。**

このドキュメントは、BACKENDCODER が `~/.gemini/GEMINI.md` の「プロジェクト進行フレームワーク（State Machine）」を実行する際に参照するデータソースです。

---

## 1. Planning Phase Inputs (for State 1)

リファクタリング計画策定時に、以下のステップで情報を収集し、Todoリストを具体化してください。

### 1.1 プロジェクト進行の初期化 (Protocol)
まず、`~/.gemini/GEMINI.md` の「3. プロジェクト進行（State Machine）」に従い、以下の手順を実行します。
1.  **SMART目標の設定:** リファクタリングの具体的なゴール（どのファイルのどの「臭い」を解消し、どういう状態にするか）を定義する。
2.  **Todoリストの作成:** **ステータス管理テンプレート**を用いてTodoを作成し、`save_memory` に保存する。

### 1.2 能動的偵察 (Active Reconnaissance)
以下のコマンドと視点を用いて、リファクタリングの対象と安全性を確認します。

*   **構造分析とリスク把握:**
    *   `read_file` でコードの匂い (Code Smells) とアーキテクチャ違反を特定する。
    *   **アーキテクチャ・チェック:**
        *   [ ] **依存性の逆転:** Domain層が詳細（Infrastructure）に依存していないか？
        *   [ ] **責務の凝集度:** 1つのクラスが複数の責務を抱えていないか？
        *   [ ] **コードの重複:** ロジックが分散していないか？
    *   **定量的リスク評価 (Quantitative Check):**
        *   対象コードが巨大（300行超）または複雑（ネスト3階層超）でないか。
        *   テストカバレッジが低い場合、リファクタリングは **High Risk** と判断する。
*   **安全網の確認:**
    *   `pytest -v -s` を実行し、現状のテストが全てパスすることを確認する。**失敗する状態でのリファクタリングは禁止。**

### 1.3 作業ブランチの計画
*   **Action:** `~/.gemini/GEMINI.md` の **「1. Gitによるバージョン管理」** に従い、作業用ブランチを作成するタスクをTodoの先頭に追加する。
    *   Naming: `refactor/{対象}`

### 1.4 Refactoring Plan の作成 (Detailed Output)
Todoリストを作成・更新する際、以下のフォーマットで具体的な「Refactoring Plan」を策定し、ログに出力してください。

**アウトプット例 (Refactoring Plan):**
```markdown
## Refactoring Plan
- **Target:** `src/interface/controllers/user_controller.py`
- **As-Is:** `register` メソッド内で `email` のフォーマットチェック（正規表現）を直接行っている（Domainロジックの漏洩）。
- **To-Be:** バリデーションロジックは全て Domain 層にカプセル化され、Controller はそれを利用するだけにする（ADR-005）。
- **Options:**
    - **Option A (Full):** `EmailAddress` ValueObject を導入し、システム全体を置き換える。
    - **Option B (Minimal):** `src/domain/rules.py` に `validate_email` 関数を作成し、Controllerから呼ぶ。
- **Selection:** **Option B** (まずはロジック移動のみを行い、広範な影響を避けるため)
- **Steps:**
    1. `src/domain/rules.py` に `validate_email` を実装 （TDD）。
    2. Controller のロジックを `validate_email` 呼び出しに置換。
    3. テスト実行。
- **Contingency:** 既存テスト修正が5件を超えたら Revert する。
```

### 1.5 計画の整合性・網羅性チェック
作成した Refactoring Plan が妥当か最終確認を行います。
以下の観点でセルフチェックを行い、**チェック結果（OK/NG）と、NGの場合の修正内容をログに出力してください。**

*   **網羅性:** 修正によって解決すべき課題が、SSOTの要求事項と一致しているか？
*   **効率性:** 修正範囲が最小限に抑えられており、不要な変更（Over-engineering）が含まれていないか？
*   **整合性:** **SSOT**で定義されたアーキテクチャの原則や、依存性のルールを遵守しているか？

---

## 2. Execution Phase Actions (for State 2)

Todoを実行する際、以下のステップで安全に構造改善を進めます。

### 2.1 Refactoring Steps (Safe Transformation)

#### Step 1: 段階的な適用 (Small Steps)
*   **Action:** 一度に多くのことをやらず、**「1回の移動につき1回のテスト実行」** を厳守する。
*   **Tool:** `replace` または `write_file` を使用。`replace` はコンテキスト（前後3行）を含めて一意にする。

#### Step 2: アーキテクチャ検証
*   **Check:** コード移動後、import文を確認し、**「外側から内側への依存」** ルールが守られているかチェックする。
*   **Check:** `mypy .` で型の不整合がないか確認する。

#### Step 3: 即時検証 (Verify)
*   **Action:** `pytest <relevant_test_path>` を実行。
*   **Failure:** 失敗したら直ちに `git checkout .` で戻し、手順を見直して再試行する（デバッグしない）。

### 2.2 コミット戦略
*   `git commit -m 'refactor: [What] to improve [Why] based on [SSOT]'`

---

## 3. Closing Phase Criteria (for State 3)

タスク完了時に、以下の完全性チェックを実行してください。

### 3.1 最終監査 (Final Audit)
改善後のコードに対して、以下の監査を行います。

*   **[品質]**
    *   [ ] 全てのテストがパスしているか？ (`pytest -v -s`)
    *   [ ] 外部からの振る舞い（APIレスポンス等）が変わっていないか？
    *   [ ] Linter/Formatter (ruff, mypy) のチェックをパスしているか？（**今回変更した範囲限定**）
*   **[成果]**
    *   [ ] コードの重複は排除されたか？
    *   [ ] 依存関係（循環参照など）は整理されたか？

**判定:** チェックリストに一つでも「No」がある、または少しでも「懸念」が残る場合は、**必ずコードを修正し、再度この監査を実行してください（合格するまで繰り返す）。**

### 3.2 成果物の定着

1.  **PR作成/更新:** User Value（保守性向上）、SSOT準拠、Architecture Check を記述。

### 3.3 プロジェクト進行の完了 (Closing Protocol)
`~/.gemini/GEMINI.md` の「3. プロジェクト進行（State Machine）」に従い、以下の手順を実行してタスクをクローズします。

1.  **振り返り (Retrospective):** YWTまたはKPTを用いて成果と課題を振り返り、**次のアクション（仮説検証や改善案）**を宣言する。
    *   `run_shell_command("echo '## Retrospective: ...'")`
2.  **メモリクリア:** `save_memory` に保存したTodoリストを完了済みに更新（または削除）する。
3.  **活動報告:** `add_issue_comment` で成果、設計整合性、残課題（Technical Debt）に加え、振り返りの内容を報告する。
