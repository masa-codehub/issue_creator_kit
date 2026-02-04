# Gemini Issue Labels Guide

GitHub Issueに付与することで、Geminiエージェントによる自動化ワークフローをトリガーするためのラベル定義。

## ラベル一覧と対応スキル

| ラベル名 | 対応スキル | 用途 |
| :--- | :--- | :--- |
| **`gemini:arch`** | `drafting-architecture` | アーキテクチャ図（Mermaid）や設計ドキュメントの作成・更新。 |
| **`gemini:spec`** | `drafting-specs` | 詳細仕様書（API定義、データ構造など）の作成・更新。 |
| **`gemini:tdd`** | `implementing-python-tdd` | Pythonコードの実装、テスト作成、リファクタリング。 |

## 運用ルール

1. **単一ラベルの原則**: 1つのIssueにつき、付与する `gemini:*` ラベルは1つのみとする。
   - 理由: 複数のエージェントスキルが競合することを防ぐため。
2. **自動実行**: これらのラベルが付いたIssueが作成（Opened）されるか、既存Issueにラベルが付与（Labeled）されると、GitHub Actionsが起動する。
3. **手動実行**: 自動実行を望まない場合（単なるタスク管理のみの場合）は、これらのラベルを付与しない。
