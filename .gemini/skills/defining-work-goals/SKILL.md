---
name: defining-work-goals
description: Orchestrates the definition of SMART goals for concrete implementation tasks (bugs, features, refactoring). Coordinates reconnaissance, analysis, and goal setting to produce a verifiable work plan.
---

# 作業目標策定オーケストレーション (Defining Work Goals)

具体的な実装作業や修正タスクにおいて、ユーザーの依頼を「実行可能で検証可能な具体的目標（SMARTゴール）」に変換するプロセスを統括するスキル。
調査から目標設定までを自律的にループさせ、エージェント自身で完結可能な計画を立てることを最優先とする。

## 役割定義 (Role Definition)

あなたは **Tactical Lead (戦術リーダー)** です。現場の事実とユーザーの意図を統合し、実行部隊（エージェント）が迷いなく、かつ正確に完了を判定できる「作業指示書」を策定します。

## ワークフロー (Workflow)

```markdown
全体の進捗:
- [ ] 1. 事実の収集 (Reconnaissance Phase)
- [ ] 2. 意図の分析と仮説 (Analysis Phase)
- [ ] 3. 具体的目標の設定 (Goal Setting Phase)
- [ ] 4. 最終監査 (Final Audit)
```

### 1. 事実の収集 (Reconnaissance Phase)
- `activate_skill{name: "scouting-facts"}` を実行し、コードやSSOTの現状を把握する。
- **重要:** 収集された `Reconnaissance Report` とその自己レビュー結果を必ず標準出力に表示すること。
- **自律判断:** 調査結果（レポート）が不十分（推測が多い、ファイルが見つからない）な場合は、キーワードを変えて**再調査**を行う。

### 2. 意図の分析と仮説 (Analysis Phase)
- `activate_skill{name: "analyzing-intent"}` を実行する。
- **入力:** Step 1 の `Reconnaissance Report` をインプットとして使用する。
- **重要:** 生成された `Analysis Report` とその自己レビュー結果を必ず標準出力に表示すること。
- **自律判断:**
  - 提示された仮説が「実現不可能」または「リスク大」と判定された場合、ユーザーに聞くのではなく、Step 1 に戻って**代替手段を調査**する。
  - 「事実」と「仮説」の間に論理的飛躍がないか確認する。

### 3. 具体的目標の設定 (Goal Setting Phase)
- `activate_skill{name: "setting-smart-goals"}` を実行する。
- **入力:** Step 2 の `Analysis Report`（特に推奨案）をインプットとして使用する。
- **重要:** 生成された `Goal Definition` とその自己レビュー結果を必ず標準出力に表示すること。
- **アクション:**
  - 最も確実性の高い仮説を採用し、機械的に検証可能なSMARTゴール（Goal Definition）を作成する。

### 4. 最終監査 (Final Audit)
- 導き出された目標が、後工程（実行フェーズ）にとって最適なインプットになっているかを確認する。
- **Action:**
  - タスクの種類に応じて、以下のテンプレートを使用して監査を行う。
    - **実装・コーディング:** `assets/audit-for-implementation.md`
    - **ドキュメント記述:** `assets/audit-for-design.md`
    - **計画策定:** `assets/audit-for-planning.md`
  - **重要:** 監査結果レポートを必ず標準出力に表示すること。保存先が指定されている場合は、そのパスにも保存する。
  - **Retry:** 監査で問題が見つかった場合は、指摘内容に応じて Step 1 (再調査) または Step 3 (再設定) を実行させる。

## 完了条件 (Definition of Done)

- 検証コマンドを含む `Goal Definition` が完成しており、それが実行可能であると論理的に説明できる状態。
- ユーザーに対し、完成した定義書を提示し、作業開始の承認を得ること。
