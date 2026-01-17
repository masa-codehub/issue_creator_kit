---
name: spec-refactoring
description: Refines specification documents for clarity, consistency, and completeness. Ensures no logical gaps or ambiguities exist, adhering to Technical Designer values.
---

# Specification Refactoring

記述された仕様書を、開発者が「迷いなく実装できる」レベルまで昇華させるスキル。
`TECHNICAL_DESIGNER` の価値観（厳密性、実装への配慮、整合性）に基づき、曖昧さを徹底的に排除する。

## 役割 (Role)
**Technical Auditor (技術監査員)**
単なる誤字脱字チェックではない。実装者視点で「この定義でコードが書けるか？」をシミュレーションし、論理的な穴や考慮漏れを塞ぐ。

## 手順 (Procedure)

### 1. 実装可能性の強化 (Enhance Implementability)
*   **Type Rigor:** `Any` や `String` などの曖昧な型定義を、`UUID`, `EmailStr`, `Decimal(10,2)` のように具体化する。
*   **Constraints:** 必須/任意、最大長、正規表現パターンなどが明記されているか確認し、追記する。

### 2. 信頼性とエッジケース (Reliability & Edge Cases)
*   **Failure Scenarios:** ネットワークタイムアウト、DB接続エラー、バリデーションエラー時の挙動（HTTP Status, Error Code）が定義されているか確認する。
*   **Consistency:** トランザクション境界や整合性モデル（ACID vs Base）が明記されているか確認する。

### 3. 整合性と標準化 (Integrity & Standardization)
*   **SSOT Check:** `activate_skill{name: "ssot-verification"}` を実行し、ADRやアーキテクチャ図と矛盾していないか確認する。
*   **Formatting:** 見出しレベルや用語がプロジェクトの規約（`system-context.md`）と統一されているか確認する。

### 4. 自己レビューと改善提案 (Self-Review & Proposal)
以下のチェックリストに基づき、仕様書の品質を自律的に向上させる。

*   **Checklist & Proposal:**
    *   [ ] **Clarity & Rigor:** 実装者が「どう実装すればいいか」を質問する必要がないか？
        - *Proposal:* 曖昧な表現の削除、具体的数値への置き換え。
    *   [ ] **Testability:** 入力と出力（正常/異常）の組み合わせが網羅され、テストケースが書けるか？
        - *Proposal:* エッジケースの追記、前提条件（Pre-condition）の明記。
    *   [ ] **Consistency:** 変数名やエンドポイント名は、既存のAPIやDB定義と整合しているか？
        - *Proposal:* 命名のリネーム、参照リンクの追加。
    *   [ ] **Clean Architecture:** 仕様の中に、不適切なレイヤーの関心事（例: ドメイン仕様書にSQLの詳細）が混ざっていないか？
        - *Proposal:* 実装詳細の分離、または抽象化。
    *   [ ] **Security/Privacy:** PII（個人情報）の扱いや、認可スコープは定義されているか？
        - *Proposal:* セキュリティ要件の追記。

*   **Action:**
    - 提案の中から、**最も効果が高く、リスクが低い1つ**を選択し、宣言する。次ステップ（Iterate）へのインプットとする。
    
### 5. 反復 (Iterate)
*   **Input:** Step 4 で選択された改善提案。
*   **Action:**
    - 改善提案が存在する場合、それをターゲットとして **Step 1 に戻り**、仕様書を修正する。
    - 改善提案がない場合、リファクタリングサイクルを終了する。

## アウトプット (Output)
*   洗練された仕様書（`docs/specs/**/*.md`）。
*   矛盾、曖昧さ、考慮漏れが排除された状態。