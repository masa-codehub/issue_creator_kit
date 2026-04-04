# Workspace JSON の生成について

この `design/architecture/structurizr.json` は、`workspace.dsl` を Structurizr CLI などでエクスポートした生成物です。

- SSOT（単一の情報源）は `workspace.dsl` です。
- `workspace.dsl` を変更した場合は、本ファイルも必ず再生成してください。

## 生成手順 (一例)

```bash
structurizr export -workspace design/architecture/workspace.dsl -format json -output design/architecture/
```

※ 実際のコマンドやパスはプロジェクトの運用に合わせて調整してください。

## 更新タイミング

- アーキテクチャ図や C4 モデルを変更した際 (`workspace.dsl` を編集したタイミング)
- リリース前に設計ドキュメントを最新化したいタイミング

本ファイルを手編集するのではなく、必ず `workspace.dsl` から再生成する運用としてください。
