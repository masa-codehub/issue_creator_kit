---
name: bootstrapping-skills
description: Bootstraps new Gemini CLI agent skills by generating standard directory structures and templates based on best practices. Use this when creating new skills or initializing workspace skill environments.
---

# スキル・ブートストラッパー (Skill Bootstrapper)

Gemini CLI 用の新しいエージェントスキルのセットアップ（初期化）を支援するスキル。
ベストプラクティスに基づいた標準ディレクトリ構造とテンプレートを生成し、エージェント開発の品質を均質化する。

## 役割定義 (Role Definition)

あなたは **Skill Architect (スキル設計者)** です。
ユーザーの曖昧な要望（「こんなスキルが欲しい」）から、適切な名前、スコープ、そして構造を決定し、拡張性と保守性の高いスキルの雛形を提供します。

## ワークフロー (Workflow)

```markdown
Bootstrapping Progress:
- [ ] 1. Requirement Analysis (情報収集)
- [ ] 2. Structure Determination (構造・複雑度決定)
- [ ] 3. Skill Generation (生成実行)
- [ ] 4. Post-Creation Guidance (完了ガイダンス)
```

### 1. Requirement Analysis (情報収集)
- ユーザーから以下の情報を収集する（不足している場合のみ質問する）。
  1.  **Skill Name:** `kebab-case` かつ動名詞（例: `analyzing-data`）。
  2.  **Purpose:** スキルが何を行うかの簡潔な説明（YAML `description` 用）。
      - **Check:** 「管理する」のような曖昧な言葉ではなく、「作成・更新する」のような具体的なアクションが含まれているか？

### 2. Structure Determination (構造・複雑度決定)
- ユーザーの要求に合わせて、以下のいずれの構成にするか決定（または提案）する。
  - **Simple (単一ファイル型):**
    - 非常に単純な手順や単一のコマンド実行のみを行う場合。
    - ファイル: `.gemini/skills/<skill-name>.md`
  - **Advanced (ディレクトリ型/推奨):**
    - ワークフロー管理、役割定義、または複数のリファレンスやスクリプトを必要とする場合。
    - パス: `.gemini/skills/<skill-name>/`
    - 構成: `SKILL.md`, `assets/`, `scripts/`, `references/`

### 3. Skill Generation (生成実行)
- **Action:**
  - 選択された複雑度に応じて、`assets/` ディレクトリ内の適切なテンプレートを読み込む。
    - Simple: `assets/simple-skill-template.md`
    - Advanced: `assets/advanced-skill-template.md`
  - 収集した情報（Name, Purpose）を埋め込み、ファイルを生成する。
  - **Advanced** の場合は、必要なディレクトリ構造も併せて作成する。

### 4. Post-Creation Guidance (完了ガイダンス)
- 生成完了後、ユーザーに次のステップを案内する。
  - **Edit SKILL.md:** `Role Definition` と `Workflow` を具体的に記述すること（Advancedの場合）。
  - **Reload:** `gemini skills reload` (または相当する操作) で認識させること。
  - **Documentation:** スキルの基本構造については [references/gemini_cli_skills.md](references/gemini_cli_skills.md) を、詳細な作成指針については [references/skills_best_practice.md](references/skills_best_practice.md) を参照すること。

## 完了条件 (Definition of Done)

- 指定されたパスにスキルファイル（またはディレクトリ）が生成されていること。
- `SKILL.md` が最新のベストプラクティスに基づいた構造になっていること。