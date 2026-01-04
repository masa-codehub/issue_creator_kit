# スキル: 開発標準の整備 (Standardization)

**開発チームの生産性とコード品質を向上させるためのガイドラインやルールを策定・文書化するプロセスです。** 単なる「文書化」ではなく、ツールの設定（Linter等）や既存コードの実態と整合した「生きたガイド」を維持します。

このドキュメントは、TECHNICAL_DESIGNER が `~/.gemini/GEMINI.md` の「プロジェクト進行フレームワーク（State Machine）」を実行する際に参照するデータソースです。

---

## 1. Planning Phase Inputs (for State 1)

計画策定時に、以下の情報を「能動的偵察 (Active Reconnaissance)」によって収集し、Todoリストの具体化に利用してください。

### 1.1 能動的偵察 (Active Reconnaissance)
以下の視点で、現状の「ルール」と「実態」を調査します。

*   **現状ガイドの確認:**
    *   `list_directory("docs/guides/")` で既存ファイルを確認。
    *   `read_file("docs/guides/coding-guidelines.md")` 等で、現在のルール記述を確認する。
*   **ツール設定の解析:**
    *   `read_file("pyproject.toml")`, `.pre-commit-config.yaml`, `ruff.toml` 等を読み込む。
    *   *Analysis:* 「ドキュメントで禁止されているが、ツールでは許可されている（無視設定されている）」ルールがないか探す。
*   **コード実態のサンプリング:**
    *   `search_code(pattern="except Exception:")` 等を実行し、悪いパターン（例：広すぎる例外捕捉）がどれくらい蔓延しているか調査する。
*   **課題の明確化:**
    *   Issueの記述から「何の問題を解決したいのか」を特定する。（例：レビューでの指摘回数を減らしたい、バグを減らしたい）

### 1.2 作業ブランチの計画
*   **Action:** `~/.gemini/GEMINI.md` の **「1. Gitによるバージョン管理」** に従い、作業用ブランチを作成するタスクをTodoの先頭に追加する。
    *   *Naming:* `docs/guide-update-{トピック名}`

### 1.3 リスク評価 (Specific Context)
Todo作成時に、以下の観点でリスクを評価する。

*   **開発者体験 (DX):** 「ルールを厳しくしすぎて、開発スピードが落ちないか？」 -> *Measure:* 自動修正（Auto-fix）可能なツール導入を優先する。
*   **既存コードとの乖離:** 「新ルールを適用すると、既存コードが大量にエラーになるか？」 -> *Plan:* 既存コードは一旦除外（Ignore）し、新規コードから適用する移行計画を立てる。

---

## 2. Execution Phase Actions (for State 2)

Todoを実行する際、以下のステップで標準化を進めます。

### 2.1 ルール策定 (Hypothesis - Step 1: Formulation)
課題を解決するための具体的かつ実行可能なルールを設計します。

**思考プロセス:**
1.  **Can we automate?**
    *   Linter (Ruff, ESLint) の設定変更で対応できるなら、ドキュメントよりそちらを優先する。
    *   *Action:* `pyproject.toml` の `[tool.ruff]` セクションの変更案を作成。
2.  **If not, specify criteria.**
    *   ツールでチェックできない場合（命名規則や設計パターンなど）、明確な判断基準を言語化する。

### 2.2 ドキュメント作成 (Hypothesis - Step 2: Drafting)
`docs/guides/` 配下の適切なファイルに追記します。以下のテンプレートに従って記述してください。

**Output Template (Markdown - Guideline Item):**
```markdown
### [Rule] 例外ハンドリングの方針
**Why (背景):**
エラー発生時に原因を特定しやすくするため、また、予期せぬエラーを握り潰さないため。

**Rule (原則):**
1. 具体的な例外クラスを捕捉する。`Exception` や `BaseException` は原則使用禁止。
2. 捕捉した例外をログ出力する際は、必ずスタックトレースを含める (`logger.exception`).

**Examples (Good/Bad):**

```python
# Bad: 何が起きたかわからない
try:
    do_something()
except Exception:
    pass

# Good: 具体的な例外を捕捉し、適切にログ出力または再送出
try:
    do_something()
except ValueError as e:
    logger.warning(f"Invalid input: {e}")
    raise DomainException("入力値が不正です") from e
except ConnectionError:
    logger.exception("External service connection failed")
    # リトライ処理へ
```

### 2.3 自律的解決ループ (Autonomy Loop)
最適なルールが決まらない場合のフローです。以下のチェックリストを用いて、確信が得られるまでサイクルを回してください。

1.  **Prototyping:** 実際にコードを書いてみて、書き心地を確認する。
2.  **Validation:**
    *   [ ] そのルールはLinterで自動チェック可能か？（可能な限り自動化する）
    *   [ ] 「守るのが面倒すぎて形骸化する」リスクはないか？
    *   [ ] 標準（PEP8等）と矛盾していないか？
    *   **判定:** 懸念がある場合、ルールを緩和するか、ツール設定を見直して Step 1 に戻る。

3.  **Decision:**
    *   迷ったら「シンプルさ」と「安全性」を天秤にかけ、安全性を取る（例：型ヒントは必須にする）。

---

## 3. Closing Phase Criteria (for State 3)

タスク完了時に、以下の完全性チェックを実行してください。**一つの懸念も残らない状態になるまで、修正と再チェックを繰り返します。**

### 3.1 最終監査 (Final Audit)
成果物 (`docs/guides/xxx.md` および設定ファイル) に対して、以下の「無慈悲な監査」を行います。

*   **[自動化と整合性]**
    *   [ ] ガイドの記述と、`pyproject.toml` 等のツール設定は完全に一致しているか？
    *   [ ] 自動化できないルールについて、明確な判断基準が言語化されているか？
*   **[実行可能性]**
    *   [ ] 記載されたコマンド例をコピペして、実際に動作することを確認したか？
    *   [ ] Good Exampleのコードは、現在のLinter設定で警告が出ないか？
*   **[納得感]**
    *   [ ] 「Why（なぜ）」が論理的に説明されており、開発者が納得できるか？
    *   [ ] 既存コードへの移行パス（暫定的な無視設定など）は定義されているか？

**判定:** チェックリストに一つでも「No」がある、または少しでも「懸念」が残る場合は、**必ずドキュメントや設定を修正し、再度この監査を実行してください。**

### 3.2 成果物の定着

`~/.gemini/GEMINI.md` の **「プルリクエストの管理 (PR Protocol)」** に完全に従い、PRを作成します。



*   **PR Title Rule:** `docs(guide): <subject> (#<issue-id>)`

*   **PR Body:** `GEMINI.md` の規約（関連Issue、変更の概要、変更の目的、検証方法）に準拠して記述する。
