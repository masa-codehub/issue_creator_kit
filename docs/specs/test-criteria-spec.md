# 詳細設計: 検証基準（テストケース）定義 (ADR-002)

## 1. 目的と方針
本ドキュメントは、Issue Creator Kit の品質を保証するためのテスト戦略と具体的な検証シナリオを定義する。
Phase 4 以降のアーキテクチャ刷新に伴い、テスト戦略は以下の二層構造を採用する。

1.  **Usecase テスト (Unit/Mock)**:
    - ビジネスロジック (`usecase/`) の振る舞いを検証する。
    - 外部依存 (`infrastructure/`) はすべて **Mock** 化し、純粋なロジックフローと例外ハンドリング（ロールバック等）を高速に検証する。
2.  **Infrastructure テスト (Unit/Real I/O + Mock)**:
    - 外部システム（ファイルシステム, Git, GitHub）との接続部分 (`infrastructure/`) を検証する。
    - ファイル操作など実ファイルシステムに対しては `tmp_path` を用いた実 I/O を行い、GitHub API クライアントや `subprocess.run` による Git コマンドなど外部サービス呼び出しは `unittest.mock` でモック化して検証する。

## 2. 品質基準 (Quality Standards)
- **カバレッジ (Coverage)**:
    - Unit Test による Branch Coverage **100%** を維持する。
- **Mocking**:
    - Usecase 層のテストでは、原則として Infrastructure 層のクラス（`FileSystemAdapter`, `GitHubAdapter` 等）を実体化せず、`unittest.mock` を使用する。

---

## 3. Usecase 層の検証シナリオ

### 3.1. ApprovalUseCase (`usecase/approval.py`)
`FileSystemAdapter` と `GitHubAdapter` を Mock 化して検証する。

#### 3.1.1. 正常系 (Success Cases)
| ID | シナリオ | 条件 (Given) | 検証内容 (Then) |
| :--- | :--- | :--- | :--- |
| A-1 | 単一ファイルの承認フロー | 正常なドキュメントが存在 | 1. ファイル読み込み<br>2. メタデータ更新 (Status, Date)<br>3. `approved` フォルダへの移動<br>4. GitHub Issue 作成<br>5. メタデータ更新 (Issue番号) |
| A-2 | 複数ファイルの承認 | 複数のドキュメントが存在 | 全てのファイルに対して A-1 のフローが実行されること |
| A-3 | ラベル処理 | リスト形式のラベル (`['A', 'B ']`) | 各ラベルの前後空白がトリムされた上で `['A', 'B']` のように GitHub Adapter にリストとして正しく渡されること |
| A-4 | 長文コンテンツ | 本文が長いドキュメント | Issue 作成時に本文が切り捨てられ、末尾に '...' が追加されること |

#### 3.1.2. 異常系・ロールバック (Error & Rollback Cases)
| ID | シナリオ | 発生エラー (When) | 検証内容 (Then) |
| :--- | :--- | :--- | :--- |
| A-E1 | GitHub 連携失敗 | `create_issue` で例外発生 | 1. 例外が再送出されること<br>2. **ロールバック実行**: 移動したファイルが元の場所に戻される (`safe_move_file` が逆向きに呼ばれる) こと |
| A-E2 | ロールバック失敗 | ロールバック移動も失敗 | 1. 元の例外が送出されること<br>2. ロールバック処理として `safe_move_file` が 2 回呼び出されること |
| A-E3 | ファイルなし | Inbox が空 | 処理を行わず `False` を返すこと |

### 3.2. WorkflowUseCase (`usecase/workflow.py`)
`ApprovalUseCase` と `GitAdapter` を Mock 化して検証する。

#### 3.2.1. シナリオ
| ID | シナリオ | Approval 結果 | 検証内容 (Then) |
| :--- | :--- | :--- | :--- |
| W-1 | 変更ありコミット | `True` (処理あり) | 1. ブランチ作成/Checkout<br>2. 承認プロセス実行<br>3. `git add .`<br>4. `git commit`<br>5. `git push` |
| W-2 | 変更なし (No-op) | `False` (処理なし) | 1. ブランチ作成/Checkout<br>2. 承認プロセス実行<br>3. **Commit/Push が実行されないこと** |

---

## 4. Infrastructure 層の検証シナリオ

### 4.1. FileSystemAdapter (`infrastructure/filesystem.py`)
`pytest` の `tmp_path` フィクスチャを利用し、実際のファイル操作を検証する。
(`tests/unit/infrastructure/test_filesystem.py` に実装)

| ID | メソッド | シナリオ | 期待値 |
| :--- | :--- | :--- | :--- |
| F-1 | `read_document` | 正常な Frontmatter 付き MD | 正しい Metadata と Content が分離されて読み込まれること |
| F-2 | `read_document` | YAML パースエラー | 例外は発生せず、パース失敗として扱われる（メタデータ空、本文保持）こと |
| F-3 | `save_document` | 新規保存 | ファイルが作成され、UTF-8 で書き込まれること |
| F-4 | `update_metadata` | 部分更新 | 指定したキーのみ更新され、他のキーや本文、コメントが維持されること |
| F-5 | `safe_move_file` | 移動成功 | 元ファイルが消え、先ファイルが存在すること |
| F-6 | `safe_move_file` | 移動先重複 (overwrite=False) | `FileExistsError` が発生すること |

### 4.2. GitHubAdapter / GitAdapter
API クライアントのラッパーであるため、外部通信部分を Mock 化した最小限の検証を行う。

- **GitHubAdapter**:
    - トークン欠落時やリポジトリ未設定時のエラーハンドリング (`ValueError`)。
- **GitAdapter**:
    - コマンド実行時の引数組み立てとエラー時の出力サニタイズ（`subprocess.run` の Mock 検証）。
    - ※ 現在の実装は最小限であり、詳細なコマンド成功パターンの網羅は今後の拡張項目とする。