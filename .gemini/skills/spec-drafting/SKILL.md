---
name: spec-drafting
description: Creates detailed specification documents using standardized templates. Focuses on clarity, rigor, and implementability.
---

# Specification Drafting

計画された仕様書を、テンプレートを用いて具体的に記述するスキル。
曖昧さを排除し、開発者が「これを見ればコードが書ける」状態にする。

## 役割 (Role)
**Spec Writer (仕様記述者)**
自然言語の曖昧さを排除し、型、制約、挙動を厳密に定義する。

## 手順 (Procedure)

### 1. テンプレート選択 (Template Selection)
作成する仕様書の種類に応じてテンプレートを選択する。
*   **API Spec:** `docs/template/spec-api.md` (新設予定)
*   **Data Spec:** `docs/template/spec-data.md` (新設予定)
*   **Logic Spec:** `docs/template/spec-logic.md` (新設予定)
*   *Note:* テンプレートがない場合は `docs/template/spec-template.md` (汎用) を使用する。

### 2. 仕様の記述 (Drafting)
**Action:**
1.  テンプレートを読み込む。
2.  対象ドキュメント（`docs/specs/**/*.md`）を作成し、内容を記述する。
3.  **記述ルール:**
    - **型定義:** `String` ではなく `UUID`, `EmailStr` (max 255) のように具体的に。
    - **必須/任意:** パラメータの `Required` / `Optional` を明記。
    - **例外:** 正常系だけでなく、エラーケース（400, 404, 500）を網羅する。

### 3. プロトタイピング (Prototyping - Optional)
**Action:**
- ライブラリの挙動や複雑なロジックに確信が持てない場合、一時的なスクリプト (`spike.py`) を作成して動作検証（Spike）を行う。
- 検証結果（「このライブラリで実現可能」という事実）を仕様書の `Note` や `Trade-off` に追記する。

## アウトプット (Output)
*   `docs/specs/` 配下の仕様書。
*   曖昧さがなく、実装可能なレベルで記述されていること。
