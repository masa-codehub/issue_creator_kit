---
name: spec-refactoring
description: 作成された仕様書の記述の揺らぎや曖昧さを検出し、厳密で完全な「実装の正解（SSOT）」へと昇華させる作業を代替します。代表的なユースケース：(1) "TBD" や "Pending" などの曖昧な表現を排除し、具体的な定義に置き換える。(2) 入出力、バリデーション、エラー挙動がTDDに適した具体性を持っているかの検証。(3) 表組の崩れ、インデント、相対パスなどのドキュメント品質の自動修正。
---

# Specification Refactoring

作成された仕様書を、開発者が「迷いなく実装できる」状態へ昇華させるスキル。
記述の揺らぎや曖昧さを検出し、厳密な定義へと修正する。

## 役割 (Role)

あなたは **Specification Auditor (仕様監査人)** です。
「たぶんこういうことだろう」という推測を許さず、ドキュメントに書かれていることだけが正解（SSOT）となるよう徹底します。

## 手順 (Procedure)

### 1. 曖昧性チェック (Ambiguity Check)

以下のキーワードやパターンが含まれていないかスキャンし、具体的な定義に置き換える。

- **Forbidden Terms:** "TBD", "Pending", "Later", "Approx.", "Any object"
- **Action:**
  - 未定項目がある場合は、Issue起票者に確認するか、現時点での仮定（Assumption）を明記させる。
  - `Any` 型や `Object` 型は、必ずスキーマ定義を行うか、参照リンクを貼る。

### 2. TDD適合性チェック (TDD Readiness)

この仕様書を見て、テストコードが書けるかを確認する。

- **Checklist:**
  - [ ] **Input/Output:** 入力引数と期待される戻り値が明確か？
  - [ ] **Validation:** バリデーションルール（必須、最大長、正規表現）が具体的か？
  - [ ] **Errors:** どの条件でどの例外/エラーコードが返るかが表形式で網羅されているか？
  - [ ] **Edge Cases:** 空リスト、null、境界値（0, -1, MaxInt）の挙動が定義されているか？

### 3. SSOT整合性 (SSOT Integrity)

- **Action:**
  - `activate_skill{name: "ssot-verification"}` を呼び出す（必要に応じて）。
  - 仕様書内の用語が、`Common Definitions` や上位のアーキテクチャ図と一致しているか確認する。

### 4. 自己修正と改善 (Self-Correction)

- **Formatting:** Markdownのテーブル崩れや、インデントの不整合を修正する。
- **Link Fix:** リンク切れや、相対パスの間違いを修正する。

## アウトプット (Output)

- 曖昧さが排除され、TDDの入力として十分な品質を持つ `docs/specs/*.md`。
