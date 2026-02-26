# [Spec] Distributed Hook & Package Entrypoint

## 概要

本仕様書は、Issue Creator Kit（以下、本ツール）を外部プロジェクトから `pre-commit` プラグインとして、あるいは Python パッケージとして容易に利用可能にするための配布仕様を定義する。

利用側に `pip install` を手動で実行させることなく、`pre-commit` が自動で専用仮想環境を構築・管理する構成を実現することを目的とする。

## 関連ドキュメント

- ADR: `reqs/context/specs/adr-014-modular-reusability/definitions.md`
- Architecture: `docs/architecture/structure-distribution.md`

## フック定義 (.pre-commit-hooks.yaml)

リポジトリルートに配置する `.pre-commit-hooks.yaml` の定義。

```yaml
- id: ick-visualize
  name: Issue Kit Visualize
  description: Visualize dependencies of issues and ADRs.
  entry: ick visualize
  language: python
  pass_filenames: false
  always_run: true

- id: ick-sync-relay
  name: Issue Kit Sync Relay
  description: Synchronize issues and transition states (Dry-run).
  entry: ick sync-relay --dry-run
  language: python
  pass_filenames: false
  always_run: true
```

### スキーマ詳細

- **id**: 外部プロジェクトの `.pre-commit-config.yaml` から参照されるユニークな識別子。
- **entry**: 実行されるコマンド。`ick` エントリポイントを使用する。
- **language**: `python`。`pre-commit` はこの指定により `pyproject.toml` を読み込み、環境を構築する。
- **pass_filenames**: `false`。本ツールはファイルパスを引数に取るのではなく、ディレクトリ全体をスキャンするため。
- **always_run**: `true`。特定のファイル変更に関わらず、実行時に全体をスキャンするため。

## エントリポイント (pyproject.toml)

`pyproject.toml` における `[project.scripts]` の定義。

```toml
[project.scripts]
issue-kit = "issue_creator_kit.cli:main"
ick = "issue_creator_kit.cli:main"
```

### 仕様詳細

- **ick**: 推奨される短縮コマンド。
- **issue-kit**: 後方互換性および明示性のためのフルネームコマンド。
- 両コマンドとも `src/issue_creator_kit/cli.py` の `main` 関数を呼び出す。

## 環境構築プロセス

1. **Trigger**: 外部プロジェクトで `pre-commit run <hook-id>` が実行される。
2. **Cloning**: `pre-commit` が本リポジトリを `~/.cache/pre-commit` 配下にクローンする。
3. **Environment Setup**: `language: python` の指定に基づき、`pre-commit` が専用の仮想環境を作成する。
4. **Installation**: 内部的に `pip install .` が実行され、`pyproject.toml` に記述された `dependencies` がすべてインストールされる。
5. **Execution**: 環境構築完了後、`entry` で指定されたコマンドが実行される。

## 検証基準 (Definition of Done)

### TDD Criteria (外部プロジェクト利用シナリオ)

外部プロジェクトの `.pre-commit-config.yaml` に以下の記述を行い、`pre-commit run` が成功することを検証の代替とする。

```yaml
repos:
  - repo: https://github.com/masa-codehub/issue_creator_kit
    rev: <target-sha-or-tag>
    hooks:
      - id: ick-check
      - id: ick-visualize
      - id: ick-sync-relay
```

**期待される挙動:**

- 仮想環境が自動生成されること。
- `ick` コマンドがパスに通り、各フックが正常に終了（または適切なエラーを出力）すること。

## 補足・制約事項

- **Python バージョン**: 実行環境に Python 3.13 以上がインストールされている必要がある。
- **依存関係の重さ**: 現状 `google-generativeai` 等の重い依存関係が含まれているため、初回インストールには時間がかかる。将来的に `optional-dependencies` への分離を検討する。
