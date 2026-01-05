# スキル: コードレビューへの対応 (Skill: Code Review Response)

**提出したプルリクエスト(PR)に対してレビュアーから受けた指摘や質問を分析し、コードの修正または技術的な根拠に基づいた回答を行うための標準プロセスです。**

このドキュメントは、BACKENDCODER が `~/.gemini/GEMINI.md` の「プロジェクト進行フレームワーク（State Machine）」を実行する際に参照するデータソースです。

---

## 1. Planning Phase Inputs (for State 1)

レビュー対応計画策定時に、以下のステップで情報を収集し、Todoリストを具体化してください。

### 1.1 プロジェクト進行の初期化 (Protocol)
まず、`~/.gemini/GEMINI.md` の「3. プロジェクト進行（State Machine）」に従い、以下の手順を実行します。
1.  **SMART目標の設定:** 全ての指摘に対して修正または回答を完了させることをゴールとして定義する。
2.  **Todoリストの作成:** **ステータス管理テンプレート**を用いてTodoを作成し、`save_memory` に保存する。

### 1.2 能動的偵察 (Active Reconnaissance)
以下のコマンドと視点を用いて、指摘内容と修正方針を明確にします。

*   **コンテキスト把握:** `pull_request_read` で全指摘を取得し、`read_file` で最新コードとの位置ズレを確認する。
*   **SSOT参照:** 指摘がプロジェクトの合意事項（ADR/Spec）に反していないか確認する。
*   **対応方針の決定:** 指摘ごとに以下のマトリクスで方針を決める。

| 方針 | 処置 | 判断基準 |
| :--- | :--- | :--- |
| **受諾 (Accept)** | コード修正 | タイポ、バグ、規約違反、正当な改善提案 |
| **議論 (Discuss)** | 質問・代替案提示 | 意図不明、副作用の懸念、別解の提示 |
| **根拠提示 (Explain)** | **修正せず**説明 | SSOTとの矛盾、意図的なトレードオフ |

### 1.3 作業ブランチの確認
*   **Action:** `git checkout <feature_branch>` && `git pull --rebase origin <feature_branch>`

### 1.4 Review Analysis Result の作成 (Detailed Output)
Todoリストを作成・更新する際、以下のフォーマットで分析結果と修正計画を出力してください。

**アウトプット例 (Review Analysis Result):**
```markdown
### レビュー指摘の分析結果
1. **指摘:** "変数名 `x` は意味不明なので `retry_count` に変更してください"
   - **方針:** **受諾 (Accept)**
2. **指摘:** "認証ロジックは Infrastructure 層に書くべきでは？"
   - **方針:** **根拠提示 (Explain)** (ADR-001でDomain層と定義済みのため)

## Review Fix Plan
- **[Target]:** `src/domain/user.py` の `change_email`
- **[Test Target]:** `tests/unit/test_user.py` (既存追記)
- **[Architecture]:** Domain層。外部依存なし。
- **[Steps]:** 1. Redテスト追加, 2. 実装, 3. クリーンアップ, 4. 検証。
- **[Contingency]:** 既存テスト崩壊時は設計見直し。
```

---

## 2. Execution Phase Actions (for State 2)

Todoを実行する際、以下のステップで誠実に修正を行います。

### 2.1 Correction & Reply (修正と回答)

#### Step 1: Implement Fix (TDD & Boy Scout)
*   **Action:** 「受諾」項目を1つずつ処理する。
*   **TDD:** `pytest <file>::<test>` でピンポイント検証を行う。
*   **Boy Scout:** クリーンアップは **今回修正するメソッド内限定**。

#### Step 2: 効率的なコード操作
*   **Tool:** `replace` を活用。
*   **Constraint:** **YAGNI** を守り、指摘と無関係な「将来への備え」は行わない。

#### Step 3: コミット (Atomic Commits)
*   **Principle:** **1項目1コミット** を原則とする。
*   **Command:** `git commit -m 'fix(review): [Symbol] - [Summary]'`

### 2.2 自律的解決 (Autonomy Loop)
*   **三振ルール:** ピンポイントテストが2回失敗したら作業中断。ログに原因を出力し、アプローチを変える。

---

## 3. Closing Phase Criteria (for State 3)

タスク完了時に、以下の完全性チェックを実行してください。

### 3.1 最終監査 (Final Audit)
修正後の状態に対して、以下の監査を行います。

*   **[品質]**
    *   [ ] 全てのテストがパスしているか？ (`pytest -q --tb=short`)
    *   [ ] Linter/Formatter (ruff, mypy) のチェックをパスしているか？（**今回変更した範囲限定**）
*   **[対応漏れ]**
    *   [ ] 全ての指摘に対して、修正または回答準備ができているか？

**判定:** チェックリストに一つでも「No」がある、または少しでも「懸念」が残る場合は、**必ず修正し、再度この監査を実行してください（合格するまで繰り返す）。**

### 3.2 成果物の定着

1.  **レビュー回答:**
    *   `pull_request_review_write(method="create")` でPendingレビュー開始。
    *   `add_comment_to_pending_review` で各指摘に回答（修正完了報告、またはSSOT引用による説明）。
        *   `pull_request_review_write(method="submit_pending")` で送信。
    2.  **Push:** `git push`
    
    ### 3.3 プロジェクト進行の完了 (Closing Protocol)
    `~/.gemini/GEMINI.md` の「3. プロジェクト進行（State Machine）」に従い、以下の手順を実行してタスクをクローズします。
    
    1.  **振り返り (Retrospective):** YWTまたはKPTを用いて成果と課題を振り返り、**次のアクション（仮説検証や改善案）**を宣言する。
        *   `run_shell_command("echo '## Retrospective: ...'")`
    2.  **メモリクリア:** `save_memory` に保存したTodoリストを完了済みに更新（または削除）する。
    3.  **活動報告:** `add_issue_comment` で完了報告を行う際、振り返りの内容（特に次回の改善点）を含める。

---

## 補足: レビュー指摘を未然に防ぐためのプラクティス (Best Practice for Preventing Issues)

技術検証（Spike）や設計変更を含むPRを作成する際は、以下の点に留意することで、レビュアーからの「なぜこれを選んだのか？」という指摘を最小限に抑え、スムーズな承認を得ることができます。

1.  **代替案との比較検討を明記する:** 採用した手法だけでなく、検討した他の選択肢（例：Porcelainコマンド vs Plumbingコマンド）と、そのメリット・デメリットを記録に残す。
2.  **選定理由を言語化する:** 「動作が安定している」「スクリプトでの利用に適している」など、客観的な選定基準を明示する。
3.  ** plunbing コマンドの優先:** 自動化スクリプトやツールにおいては、UI向けの porcelain コマンドよりも、出力が安定している plumbing コマンドを優先的に検討する。