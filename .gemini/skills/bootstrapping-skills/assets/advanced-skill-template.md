---
name: <skill-name>
# [命名規則]
# - 小文字、数字、ハイフンのみ (kebab-case)
# - 動名詞推奨 (例: processing-pdfs, analyzing-data)
# - 予約語禁止 (gemini, google)

description: <purpose>
# [説明のベストプラクティス]
# - 常に英語(English)で記述してください
# - 常に三人称で記述してください (例: "Analyzes logs..." OK / "I will help analyze..." NG)
# - スキルが「何をするか」と「いつ使用するか」を含めてください
# - 具体的なキーワードを含めてください (Geminiがスキルを選択するトリガーになります)
---

# <スキル タイトル>

## 役割定義 (Role Definition)

<!--
エージェントがこのスキルを使用する際の「役割（人格）」を定義します。
コンテキストウィンドウを節約するため、Geminiが既に知っている一般的な情報は省き、
このタスク特有のコンテキスト（専門性、守るべき規範、価値判断基準）のみを提供してください。
-->

あなたは **<Role Name>** です。
<Role Description: 立ち位置、専門性、守るべき規範など>

## ワークフロー (Workflow)

<!--
複雑なタスクを、チェックリスト形式のステップに分解して記述します。
Geminiはこれを出力にコピーして進捗を管理します。
-->

```markdown
Progress:
- [ ] 1. <Step 1: 調査・分析など>
- [ ] 2. <Step 2: 実行・記述など>
- [ ] 3. <Step 3: 検証・報告など>
```

### 1. <Step 1 Name>
- **Action:**
  <!-- 具体的なアクション、使用するツール、参照すべきファイルを記述 -->
  - <Detailed Action 1>
  - <Detailed Action 2>
- **Output:**
  <!-- このステップで得られる成果物や、標準出力に表示すべき情報を記述 -->
  - <Expected Output>

### 2. <Step 2 Name>
- **Action:**
  - <Detailed Action 1>
  - <Detailed Action 2>

### 3. <Step 3 Name>
- **Action:**
  - <Detailed Action 1>

## 完了条件 (Definition of Done)

<!--
タスクが「完了」したと見なすための客観的な基準を列挙します。
-->

- <Condition 1: 必須ファイルの生成など>
- [ ] <Condition 2: 監査の通過など>

## 高度な使い方

<!--
[段階的開示 (Progressive Disclosure)]
SKILL.mdは500行以内に保ち、詳細は references/ 以下の別ファイルに記述します。
Geminiは必要になった時だけリンク先のファイルを読みに行きます。
リンクは SKILL.md から1階層深さまで (references/xxx.md) に留めてください。
-->

**ワークフロー詳細**: 複雑な手順の詳細は [references/workflows.md](references/workflows.md) を参照してください。

## ユーティリティスクリプト

<!--
Geminiにコードを書かせるのではなく、検証済みのスクリプトを実行させることで信頼性を高めます。
スクリプト内でエラー処理を行い、Geminiに丸投げしないようにしてください。
-->

- `scripts/validate.py`: <!-- [検証ループ] 実行結果を検証するスクリプトを用意し、「実行→検証→修正」のループを回すと品質が向上します。 -->