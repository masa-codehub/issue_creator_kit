# リファクタリング分析レポート: [Title]

## 1. 現状分析 (Current State Analysis)

### A. 静的解析の検出事項 (Static Analysis Findings)

_(`pre-commit run --all-files` を実行し、主要なエラーや警告をここに貼り付けてください)_

- [ ] Linter (Ruff):
- [ ] Type Checker (Mypy):

### B. コードスメルの検出 (Code Smell Detection)

_(非Pythonicなパターン、重複、または過度な複雑性を特定してください)_

- [ ] **複雑度 (Complexity):** (例: 深いネスト、20行を超える関数)
- [ ] **重複 (Duplication):** (例: 複数の関数で繰り返されるロジック)
- [ ] **命名 (Naming):** (例: 不明確な変数名、非標準的なケーシング)

### C. ギャップ分析 (vs SSOT/Clean Architecture)

- [ ] **責務 (Responsibility):** (例: UseCaseロジックがControllerに漏れ出している)
- [ ] **依存関係 (Dependency):** (例: Domain層がInfrastructure層をインポートしている)

## 2. 自己レビュー (Self-Review Checklist)

- [ ] **Pythonic:** イディオム（コンテキストマネージャ、ジェネレータ等）を適切に使用しているか？
- [ ] **型ヒント:** 引数と戻り値に完全な型ヒントがあるか？ (`Any` を排除)
- [ ] **Docstrings:** 公開インターフェースにGoogleスタイルのDocstringがあるか？
- [ ] **SSOT:** 設計ドキュメントやADRと整合しているか？
- [ ] **テスト:** 全てのテストがパスしているか (Green)？

## 3. 改善提案 (Improvement Proposals)

### 優先度 1: 重要 (Critical - Must Fix)

_(型安全性、バグ、重大なアーキテクチャ違反)_

1. 修正: ...
2. 修正: ...

### 優先度 2: 品質 (Quality - Should Fix)

_(可読性、パフォーマンス、標準準拠)_

1. リファクタリング: ...
2. 名称変更: ...

### 優先度 3: 洗練 (Polish - Nice to Have)

_(Docstring、軽微なスタイル調整)_

1. 追加: ...
