---
name: architecture-drafting
description: Executes the architecture visualization plan. Updates Mermaid diagrams and documentation to reflect the codebase reality defined in the planning phase, adhering to Technical Designer values.
---

# Architecture Drafting

計画フェーズで特定された「Gap」を解消し、抽象的なアーキテクチャを「実行可能な設計図」へと昇華させるスキル。
`TECHNICAL_DESIGNER` として、ただ図を描くのではなく、**「なぜその構造なのか」という設計意図**をドキュメントに焼き付ける。

## 役割 (Role)
**Technical Draftsman (自律的設計者)**
単なる作図者ではない。コードの実態を解釈し、Clean Architecture や DDD の原則に照らし合わせて、システムの構造を「正しく」かつ「美しく」表現する。

## 手順 (Procedure)

### 1. テンプレート選択 (Template Selection)
作成・更新する図の種類（UML Type）に応じて、適切なテンプレートを選択する。

*   **C4 (Context/Container/Component):** `docs/template/arch-structure.md`
    *   *Usage:* 構造の定義と静的な関係性を記述する。
*   **Sequence Diagram:** `docs/template/arch-behavior.md`
    *   *Usage:* 時系列のフロー、非同期処理、詳細な例外ルールを記述する。
*   **State Diagram:** `docs/template/arch-state.md`
    *   *Usage:* オブジェクトのライフサイクルと遷移ルールを記述する。
*   **ER Diagram:** `docs/template/arch-data.md`
    *   *Usage:* データモデルと永続化要件を記述する。

### 2. 構造定義と記述 (Defining & Drafting)
図を描く前に、テンプレートの定義セクション（Element Definitions / Notes / State Definitions）を埋める。
曖昧さを排除し、実装者が迷わないレベルの厳密さ（Clarity & Rigor）で記述する。

**Action:**
1.  選択したテンプレートを読み込む。
2.  対象ドキュメント（`docs/architecture/*.md`）を作成または開き、テンプレートの内容を適用する。
3.  **Domain-Centric** (ビジネス用語) かつ **Implementation-Aware** (技術的実態) な定義を記述する。

### 3. 図解更新 (Visualization with Mermaid)
定義した要素を Mermaid で可視化する。ここでは「メンタルモデルの統一（Visual Communication）」を最優先する。

*   **Structure (C4):**
    *   システム境界（Boundary）を明確にする。
    *   依存の矢印は必ず「依存する側」から「依存される側」へ引く（Clean Arch準拠）。
*   **Behavior (Sequence):**
    *   外部システムとの境界や、非同期メッセージ（Queue）のやり取りを明確にする。
*   **State/Data:**
    *   許容されない遷移や、あり得ないリレーションを表現しないよう注意する。

### 4. 自律的解決ループ (Autonomy Loop)
コードの意図が読み取れない場合：
1.  **Code Archaeology:** `git blame` や過去のPR/Issueを掘り起こし、当時の文脈（Why）を特定する。
2.  **Trade-off Analysis:** なぜそのような実装になっているのか、トレードオフを推論し、定義セクションの「Trade-off」欄に記述する。
3.  **Conservative Update:** どうしても不明な場合は、事実（Fact）のみを記載し、推測部分は `Note` で注釈する。

## アウトプット (Output)
*   更新された `docs/architecture/*.md` ファイル。
*   適切なテンプレートが適用され、テキスト定義とMermaid図が整合していること。