---
name: retrospective
description: Skill for conducting retrospectives using YWT and KPT. Used for (YWT) (1) deep-diving into technical failures, (2) analyzing unexpected tool/system behavior, (3) documenting key learnings from complex bug fixes; and (KPT) (1) improving task estimation and planning accuracy, (2) refining step-by-step procedures, (3) optimizing communication or tool usage workflows.
---

# 振り返り (Retrospective)

完了したタスクの成果と課題を振り返り、次のアクションを決定するためのスキル。
状況に応じて **YWT** または **KPT** を選択（あるいは併用）して実施する。

## 1. YWT (技術・タスクの深掘り)
技術的な失敗、未知の挙動、仕様の誤解などに直面した際に選択する。

- **Y (やったこと):**
  - Todoリストに基づいて実行した、目標達成のための一連の手続き。
  - **周辺事実の収集:** 実行中およびその周辺で起きていた事実関係（システムログ、ツール出力、環境の変化など）を漏れなく収集する。
- **W (わかったこと):**
  - 手続きを実行した結果、実際に何が起きたか（成功、失敗、想定外の挙動）。
  - 当初の想定と実際の挙動의ギャップ。
- **T (次やること / 仮説立案):**
  - `objective-analysis` スキルの「多角的仮説立案」に準じ、「Y」および「W」で収集した事実を根拠に3つの仮説（実証的、飛躍的、逆説的）を立てる。
  - **検証項目の策定:** 各仮説の確からしさを判断するために必要な情報（Unknowns）を特定し、次のアクション（調査、実験、ユーザーへの質問）としてリストアップする。

## 2. KPT (プロセス・効率の改善)
作業の進め方、コミュニケーション、計画の精度などに課題を感じた際に選択する。

- **K (Keep):** スムーズに進行した手順、効果的だった判断（継続すべき点）。
- **P (Problem):** 停滞の要因（情報の不足、スコープの肥大化、手順の不備など）。
- **T (Try):** **具体的な作業手順の修正案、または新しい作業手順の定義**。次回からどのステップをどう変えるかを具体的に記述する。

## アウトプット
選択したフレームワークに基づいて内容を記述し、以下のコマンドで宣言する。

`run_shell_command{command: "echo '## Retrospective: <内容>'"}`
