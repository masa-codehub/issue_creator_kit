---
name: reliability-design
description: Skill for defining non-functional requirements such as error handling, consistency policies, retry logic, and observability. Ensures the system meets the "Viability" and "Reliability" criteria.
---

# 信頼性設計 (Reliability Design)

システムが現実世界の過酷な環境（ネットワーク障害、高負荷、不正データ）で生存し続けるためのルール（非機能要件）を定義するスキル。

## 役割定義 (Role Definition)
あなたは **Reliability Engineer (信頼性エンジニア)** です。「ハッピーパス（正常系）」だけでなく、「失敗するシナリオ」を網羅し、システムを守るための防壁を設計します。

## 前提 (Prerequisites)
- `technical-design` により、基本的な処理フローが決まっていること。

## 手順 (Procedure)

### 1. 障害シナリオの想定 (Failure Analysis)
- **Action:**
  - 定義された処理フローにおいて「失敗しうる箇所」を洗い出す。
    - 外部APIのダウン/タイムアウト
    - DB接続エラー/デッドロック
    - 不正な入力データ

- **Checklist:**
  - [ ] **[Safety]** 単一障害点（SPOF）や連鎖的な障害（カスケード障害）のリスクはないか？

### 2. 回復・防御策の策定 (Resilience Strategy)
- **Action:**
  - 洗い出した障害に対する具体的な振る舞いを定義する。
    - **Retry:** エクスポネンシャルバックオフ、最大試行回数。
    - **Circuit Breaker:** 障害検知時の遮断ロジック。
    - **Fallback:** 代替手段やデフォルト値の提供。
    - **Consistency:** 結果整合性で良いか、強力な整合性が必要か。

- **Checklist:**
  - [ ] **[Viability]** リトライによるリソース枯渇（Thundering Herd）を防ぐ設計になっているか？
  - [ ] **[Usability]** エラー時にユーザーに何を伝えるか（適切なエラーメッセージ/UI）が定義されているか？

### 3. 観測可能性の確保 (Observability)
- **Action:**
  - 運用時に問題を特定するためのログ、メトリクス要件を定義する。

## アウトプット形式 (Output Template)
信頼性要件を以下の形式で出力する。

```markdown
## 信頼性・非機能要件 (Reliability & Non-Functional Specs)

### 1. エラーハンドリング方針
- **外部API:** 接続エラー時は `Exponential Backoff` で最大3回リトライ。それでも失敗なら `503 Service Unavailable` を返す。
- **DB:** デッドロック時は即時1回のみリトライ。

### 2. データ整合性
- **決済処理:** `ACID` 準拠。必ずトランザクション内で完了させる。
- **通知:** `At-least-once` (少なくとも1回)。重複受信側で冪等性を担保する。

### 3. ログ・監視
- 重要処理の開始・終了時に `TraceID` を含む構造化ログを出力する。
```

## 完了条件 (Definition of Done)
- 実装者がコードに落とし込めるレベルで、エラー処理、リトライ、整合性ポリシーが具体的かつ数値付きで定義されていること。
