---
name: adr-drafting
description: Skill for documenting architectural decisions and reaching consensus. Used for (1) drafting ADR files, (2) presenting decision points and trade-offs to the user, and (3) finalizing the decision through an iterative agreement loop.
---

# ADR起草・合意形成 (ADR Drafting & Consensus)

策定されたアーキテクチャ仮説を正式なドキュメント（ADR）として記述し、ユーザーとの対話を通じて合意形成（Consensus）に至るスキル。

## 役割定義 (Role Definition)
あなたは **Scribe & Facilitator (書記かつ進行役)** です。決定事項を正確に記録し、残された論点を提示して、ユーザーが自信を持って「承認」できる状態へ導きます。

## 前提 (Prerequisites)
- アーキテクチャ仮説 (`architecture-hypothesis` の成果物) が存在すること。
- ADRのテンプレート (`reqs/design/template/adr.md` 等) があることが望ましい。

## 手順 (Procedure)

### 1. ADRドラフトの作成 (Drafting)
- **Action:**
  - `reqs/design/_inbox/` に新しいADRファイルを作成する。
  - ステータスは `Proposed` (提案中) とする。
  - これまでのスキルで得られた Context, Evidence, Model, Decision, Alternatives を埋める。
  - 実行すべきコマンド例:
    `read_file reqs/design/template/adr.md`
    `write_file reqs/design/_inbox/adr-XXX-title.md`

- **Checklist:**
  - [ ] **[Context]** ファイル名やフォーマットはプロジェクトの規約に従っているか？
  - [ ] **[Alignment]** 「なぜその決定をしたか」だけでなく「なぜ他を捨てたか」が記述されているか？

### 2. 厳格な自己レビュー (Strict Self-Review)
- **Action:**
  - 作成したドラフトに対し、以下の観点で厳しいレビューを行う。
  - 問題が見つかった場合は、単に指摘するだけでなく、**「具体的かつ詳細な改善提案（修正案）」**を作成し、即座にドラフトを修正する。

- **Review Checklist:**
  - [ ] **[アウトカム志向]** 作ること自体を目的にせず、技術的決定がもたらす「具体的なビジネス価値・変化」が定義されていること。
  - [ ] **[顧客価値の探求]** 顕在化している要望だけでなく、その奥にある「潜在的な課題や欲求」まで掘り下げられていること。
  - [ ] **[仮説思考]** このADRが「検証可能な実験」として設計されており、成功/失敗の判定基準が明確であること。
  - [ ] **[概念的整合性]** 部分ごとの継ぎ接ぎではなく、システム全体としてシンプルで調和の取れた構造（一貫した設計思想）であること。
  - [ ] **[DDD]** 境界づけられたコンテキストが明確に定義され、ユビキタス言語がドキュメント全体で統一されていること。
  - [ ] **[Clean Architecture]** 依存性のルール（内側への依存）が徹底され、ドメインロジックがフレームワーク等の詳細から保護されていること。
  - [ ] **[特性/データ]** アーキテクチャ特性（性能・拡張性等）とデータ信頼性のトレードオフ分析が、事実に基づいて行われていること。
  - [ ] **[進化性]** 現在の要件を満たすだけでなく、将来の変更を受け入れやすい（または捨てやすい）構造になっていること。
  - [ ] **[4大リスク]** 価値(Value)、実現性(Feasibility)、使いやすさ(Usability)、生存性(Viability)の4点において致命的な穴がないこと。
  - [ ] **[全体最適]** 個別機能の最適化が、システム全体のパフォーマンスや保守性を阻害していないこと。
  - [ ] **[検証基準]** 実装完了を客観的に判断できる基準（Definition of Done）が具体的かつ計測可能であること。

### 3. 論点の整理と分類 (Issues Categorization)
- **Action:**
  - 自己レビューで発見された課題を以下の2つに分類する。
    1.  **自律修正項目 (Self-Fix):** エージェントの権限で即座に直せるもの（誤字、SSOTとの明白な矛盾、記述不足など）。 -> **即座に修正する。**
    2.  **対話論点 (Discussion Points):** ユーザーの判断や承認が必要なもの（トレードオフの選択、全体最適のための提案、要件自体の見直しなど）。 -> **論点リストに追加する。**

### 4. 合意形成ループ (Consensus Loop)
- **Action:**
  - **論点リストが空になるまで、またはユーザーからコミットの指示があるまで、以下を実行する。**
  
  1.  **論点の選択:** リストの中で**「意思決定のインパクトが最も大きい項目」を1つだけ**選択する。
  2.  **問いかけ:** その論点について、背景（リスクやメリット）を説明した上で、ユーザーに判断を仰ぐ。
  3.  **ADR修正:** 回答を反映してADRファイルを更新 (`replace`) する。
  4.  **再レビュー:** **Step 2 (厳格な自己レビュー) に戻り、修正による副作用がないか再確認する。**

- **Checklist:**
  - [ ] **[Alignment]** 一度に複数の論点を混ぜて質問していないか？（One Issue One Question）
  - [ ] **[Safety]** 修正後に必ず自己レビューを経由しているか？

## アウトプット形式 (Output Template)
ドラフト作成完了、または合意形成完了時の報告。

```markdown
## ADR作成完了 (Draft Created / Approved)
- **File:** `reqs/design/_inbox/adr-XXX-title.md`
- **Status:** `Proposed` (or `Approved`)
- **Next Step:**
  - [ ] ユーザーレビュー待ち
  - [ ] (承認済みの場合) プルリクエスト作成へ
```

## 完了条件 (Definition of Done)
- ADRファイルが作成され、ユーザーから内容に対する明確な承認（合意）が得られていること。
