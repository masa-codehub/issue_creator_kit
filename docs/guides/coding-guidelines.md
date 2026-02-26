# コーディングガイドライン

このドキュメントは、プロジェクトにおけるコードの品質、一貫性、保守性を高めるためのコーディング規約とベストプラクティスを定義します。

## 1. 基本方針

- **読みやすさ:** コードは書く時間よりも読まれる時間の方が圧倒的に長いため、常に読みやすく、理解しやすいコードを心がけます。
- **一貫性:** プロジェクト全体で統一されたコーディングスタイルを維持します。
- **自動化:** フォーマットや静的解析など、機械的にチェックできることは積極的に自動化し、レビューではより本質的な議論に集中します。

## 2. スタイルガイド

### 2.1. Python コード

基本的には [PEP 8](https://peps.python.org/pep-0008/) に準拠します。コードのフォーマットは `Black` によって自動的に強制されます。

- **フォーマッター:** [Black](https://github.com/psf/black)
  - 1行の最大文字数: `88`
- **リンター:** [Ruff](https://github.com/astral-sh/ruff)
  - `pyproject.toml` の `[tool.ruff.lint]` セクションで定義されたルールセットを有効にしています。
  - コミット前に `pre-commit` フックによって自動的に実行されます。
- **型チェック:** [Mypy](https://mypy-lang.org/)
  - 静的型付けを強制します。原則として、すべての関数・メソッドに型ヒントを付与してください。
  - 型ヒントを付与することにより、`mypy` による静的解析の恩恵を最大限に受けることができ、コードの可読性と堅牢性が向上します。
  - `pyproject.toml` の `[tool.mypy]` で設定が定義されています。

### 2.2. コミットメッセージ

コミットメッセージは [Conventional Commits](https://www.conventionalcommits.org/ja/v1.0.0/) の規約に準拠します。

- **フォーマット:** `<type>(<scope>): <subject>`
- **例:**
  - `feat(auth): Add password reset functionality`
  - `fix(api): Correct response status code for invalid requests`
  - `docs(guide): Update development setup instructions`

## 3. ベストプラクティス

### 3.1. テスト

- 新機能の追加やバグ修正の際には、必ずテストコードを記述します。
- テストフレームワークには `pytest` を使用します。
- テストは `tests/` ディレクトリに、プロダクションコードの構造を反映させて配置します。

### 3.2. pre-commit フック

- このプロジェクトでは `pre-commit` を導入しており、コミット時に自動的に `Ruff` や `Mypy` などのチェックが実行されます。
- 開発を始める前に、必ず `pre-commit install` を実行してフックを有効にしてください。

## 4. ツールの設定

各種ツールの詳細な設定は、すべて `pyproject.toml` ファイルに集約されています。規約やルールを変更する場合は、このファイルを更新してください。
