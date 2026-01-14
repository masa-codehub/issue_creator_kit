---
name: tdd-planning
description: Analyzes requirements and SSOT to formulate a concrete TDD plan. Used for (1) translating ambiguous requirements into verifiable test scenarios, (2) ensuring new features align with existing architecture before coding, and (3) defining the "Red-Green-Refactor" strategy for complex logic.
---

# TDD Planning

このスキルは、実装に入る前に「何を」「なぜ」「どのように」テストし実装するかを明確にし、手戻りを防ぐための計画策定を目的とします。

## 役割定義 (Role Definition)
あなたは **TDD Architect** です。要件を厳密なテスト仕様に変換し、ドメインの整合性とアーキテクチャの遵守を保証する計画を立てます。

## 前提 (Prerequisites)
- 既存スキル `active-reconnaissance`, `ssot-verification`, `todo-management` が利用可能であること。
- 実装対象の Issue または要件が特定されていること。

## 手順 (Procedure)

### 1. 能動的偵察 (Active Reconnaissance)
- **Action:**
  - `issue_read` を実行し、表面的な要件だけでなく「ユーザー価値（Why）」を特定する。
  - `active-reconnaissance` スキルを活用し、関連する承認済み ADR (`reqs/design/_approved/`) と仕様書 (`docs/specs/`) を読み込む。
    `activate_skill{name: "active-reconnaissance"}`
  - `read_file` で実装対象周辺の既存コードと既存テストを確認する。

### 2. 設計整合性チェック (SSOT Verification)
- **Action:**
  - `ssot-verification` スキルを活用し、以下の観点で現在の理解と設計を照合する。
    `activate_skill{name: "ssot-verification"}`
    - [ ] **ユビキタス言語:** 提案するメソッド名や引数名が、ドキュメントで定義された用語と一致しているか？
    - [ ] **レイヤー構造:** 実装箇所がクリーンアーキテクチャの責務（Domain, UseCase等）に合致しているか？
    - [ ] **依存の方向:** 下位レイヤーへの直接的な依存や、ビジネスロジックの漏洩がないか？

### 3. TDD Plan の策定
- **Action:**
  - 収集した情報に基づき、以下のテンプレートを用いて具体的なシナリオを作成する。
  - **Checklist:**
    - [ ] **Red:** 失敗することが確実な、最小のテストケースは何か？（期待される失敗理由を明記）
    - [ ] **Green:** テストを通すために最低限必要な実装は何か？
    - [ ] **Refactor:** 重複、マジックナンバー、命名、既存コードとの調和をどう整えるか？

### 4. Todo分解 (via todo-management)
- **Action:**
  - `todo-management` スキルをアクティベートし、策定した「TDD Plan」を `.gemini/todo.md` のタスクリストに変換する。
    `activate_skill{name: "todo-management"}`
  - 各サイクル（Red, Green, Refactor）を、それぞれ「Action（ツール実行）」と「Verify（テスト/解析実行）」のペアに分解する。
  - **重要 (Reference):**
    - **Redタスク:** Action には「どの仕様書/ADRに基づいてテストケースを作成するか」を明記する。
    - **Refactorタスク:** Action には「何を基準にリファクタリングするか（Coding Guidelines等）」を明記する。
  - `todo-review` を実行し、計画が原子レベルまで砕かれているか確認する。
    `activate_skill{name: "todo-review"}`

## アウトプット形式 (Output Template)

```markdown
## TDD Plan: [Issue Title/ID]
- **Goal:** [SMARTに基づいた具体的な目標]
- **Context:** [参照したADR/Spec/ファイル]
- **Scenarios:**
  - **Red:** [テストファイルパス] に [テスト名] を追加。期待される失敗: [理由]
  - **Green:** [ソースファイルパス] に最小限の [ロジック/メソッド] を実装。
  - **Refactor:** [改善対象の匂いや構造]
- **Risks:** [4 Big Risks (Value, Feasibility, Usability, Viability) に基づく懸念事項]

---
※ 詳細な実行ステップは `.gemini/todo.md` に作成されました。
```

## 完了条件 (Definition of Done)
- ユーザーに TDD Plan を提示し、合意を得ていること。
- `todo-management` によって、実行フェーズの具体的かつ原子的なステップが `.gemini/todo.md` に定義されていること。

