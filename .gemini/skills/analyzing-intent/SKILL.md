---
name: analyzing-intent
description: Infers user intent and formulates multi-perspective hypotheses based on factual Reconnaissance Reports. Performs gap analysis and identifies critical risks to define the "Why" and "How" before setting goals.
---

# 意図分析 (Analyzing Intent)

収集された事実（Reconnaissance Report）とユーザーの依頼を統合し、表面的な言葉の裏にある「真の意図（Why）」を推測し、解決策の仮説を立てるスキル。
このステップでは「何を目指すべきか」の解釈を加え、目標設定のための論理的な土台を構築することを目的とする。

## 役割定義 (Role Definition)

あなたは **Profiler (プロファイラー)** です。断片的な証拠と依頼内容を繋ぎ合わせ、ユーザーが本当に達成したい「アウトカム」と、それを阻む「壁」を浮き彫りにします。

## ワークフロー (Workflow)

分析の進捗を管理するためにチェックリストを使用してください。

```markdown
分析状況:
- [ ] 1. 意図の深掘り (Analyze Intent)
- [ ] 2. ギャップ分析 (Gap Analysis)
- [ ] 3. 仮説の立案 (Formulate Hypotheses)
- [ ] 4. 自己レビュー (Self-Review)
```

### 1. 意図の深掘り (Analyze Intent)

**目的:** ユーザーが解決したい本質的な課題と、期待される価値を特定する。

- **Action:**
  - 5W1Hフレームワーク（Why, What, Where, Who, When, How）を用いて情報を整理する。
  - 特に「Why (なぜその機能が必要か)」を重点的に深掘りする。

### 2. ギャップ分析 (Gap Analysis)

**目的:** ユーザーの理想とプロジェクトの現実（事実）の乖離を特定する。

- **Action:**
  - 偵察レポートで得られた事実と、依頼内容を比較する。
  - **論理的矛盾:** 既存のADRや設計方針と衝突していないか？
  - **技術的制約:** 実装上の難所や、前提となっている知識の間違いはないか？

### 3. 仮説の立案 (Formulate Hypotheses)

**目的:** 解決策の可能性を広げ、最適かつ検証可能なアプローチを模索する。

- **Action:**
  - `assets/analysis-report-template.md` を使用して分析レポートを作成する。
  - 以下の3つの視点で仮説を立てる。
    - **実証的仮説 (Grounded):** 事実に基づいた堅実な本命案。
    - **飛躍的仮説 (Leap):** 潜在的なニーズや将来の拡張性を見据えた理想案。
    - **逆説的仮説 (Paradoxical):** 既存の前提を疑い、別の角度からアプローチする革新案。
  - **出力:** レポートを必ず標準出力に表示する。ユーザーから保存先が指定されている場合は、そのパスにも保存する。

### 4. 自己レビュー (Self-Review)

**目的:** 分析の妥当性と、目標設定フェーズへの適合性を確認する。

- **Action:**
  - `assets/self-review-template.md` を使用して自己レビューを行う。
  - **出力:** レビュー結果を必ず標準出力に表示する。ユーザーから保存先が指定されている場合は、そのパスにも保存する。
  - **是正:** レビューで問題が見つかった場合は、レポートを修正し、再度レビューを行う。

## 完了後のアクション

レポートを出力した後、ユーザーに「分析と仮説の立案が完了した」ことを伝え、次のステップ（`setting-smart-goals` による目標設定）に進むか、不足情報の確認を行うか提案してください。