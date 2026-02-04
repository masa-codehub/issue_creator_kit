# PR Title Template
<type>(<scope>): <subject>
<!-- 
Types: feat, fix, docs, style, refactor, perf, test, chore, build, ci, revert
Example: feat(auth): add google login support
-->

# PR Body Template

## 目的 (Goal)

<!-- なぜこの変更が必要か（背景とアウトカム） -->

## 変更の概要 (Summary)

<!-- 何をどのように変更したか -->

## 関連Issue (References)

Closes #<Issue番号>

## 検証方法 (Verification)

<!-- 実施したテストや動作確認の手順と結果（ログ等） -->

- [ ] Unit Test:
- [ ] Manual Check:

## 品質確認 (Quality Control)

- [ ] リンター・フォーマッター (`ruff`, `mypy`) のチェックを通過した
- [ ] 不要なデバッグログやコメントアウトを削除した