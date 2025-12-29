---
title: "既存スクリプトのリファクタリングと回帰テスト"
labels:
  - "task"
  - "P2"
  - "BACKENDCODER"
roadmap: "reqs/roadmap/active/roadmap-adr002-document-approval-flow.md"
task_id: "T2-4"
depends_on:
  - "issue-T2-3.md"
status: "Draft"
---
# {{title}}

## 親Issue / ロードマップ (Context)
- **Roadmap**: {{roadmap}}
- **Task ID**: {{task_id}}

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: `create_issues.py` は独自の正規表現ロジックでファイルをパースしており、新しく実装された `utils.py` (YAML対応) とロジックが重複・乖離している。
- **To-be (あるべき姿)**: `create_issues.py` が `utils.py` の関数を利用するようにリファクタリングされ、コードベースが統一される。

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `src/issue_creator_kit/scripts/create_issues.py` (改修対象)
- [ ] `src/issue_creator_kit/utils.py` (新ライブラリ)

## 3. 実装手順 (Implementation Steps)

### 3.1. リファクタリング (Refactor)
- [ ] **ファイル**: `src/issue_creator_kit/scripts/create_issues.py`
    - **処理内容**:
        - ファイル読み込み部分を `utils.load_document` に置き換える。
        - 依存関係 (`Depends-On`) の解析ロジックを、YAML辞書からの取得に変更する。
        - 正規表現でのメタデータ解析コードを削除する。

### 3.2. テスト (Test)
- [ ] **ファイル**: `tests/unit/test_create_issues.py` (既存または新規)
    - **処理内容**: リファクタリング後も Issue 起票ロジック（依存関係の解決、Issue作成API呼び出し）が正しく機能することを検証するテストを追加/修正する。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-2-implementation`
- **作業ブランチ (Feature Branch)**: `feature/T2-4-refactor-legacy`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest` が全てパスすること。
- [ ] **手動検証**: ローカルでダミーのMarkdownファイルを対象に `create_issues.py` を実行し、正常に動作することを確認する（Dry-run推奨）。

## 6. 成果物 (Deliverables)
- リファクタリングされた `src/issue_creator_kit/scripts/create_issues.py`