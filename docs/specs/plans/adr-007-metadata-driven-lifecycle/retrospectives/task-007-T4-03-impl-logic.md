# Retrospective Report (YWT) - Issue Creation Logic Implementation (T4-03)

## 1. 実施内容 (Y: What I did)

- `src/issue_creator_kit/domain/interfaces.py` を新規作成し、Adapter 用のインターフェース (ABC) を定義。
- `IssueCreationUseCase` をリファクタリングし、DI を導入。
- `create_issues(before, after, adr_id=None)` メソッドを 4-step アルゴリズム（Discovery, DAG/Ready, Atomic Creation, Atomic Move）に沿って実装。
- `tests/unit/usecase/test_creation.py` を作成し、TDD サイクルで正常系・異常系・アーカイブ依存関係を検証。

## 2. 観測事実・わかったこと (W: What I learned)

- **技術的発見**:
  - `graphlib.TopologicalSorter` は依存関係が batch 内に閉じていれば非常に強力だが、cross-batch（アーカイブ）の依存関係は事前に `Ready` 判定でフィルタリングする必要がある。
  - `Metadata` が Pydantic モデルに移行していたため、辞書形式の代入 (`doc.metadata["status"]`) がエラーとなり、`update()` メソッドを使用する必要があった。
- **プロセス**:
  - インターフェースを先に定義することで、UseCase のテストにおいて Mock の作成が非常にスムーズになった。
  - `Fail-fast` 構造にすることで、API エラー時の副作用（中途半端なファイル移動）を確実に防げることがコードレベルで確信できた。

## 3. 次にすること (T: What to do next)

- **資産化アクション**:
  - 他の UseCase (`ApprovalUseCase`, `WorkflowUseCase` 等) においても、今回定義した `interfaces.py` を利用するようにリファクタリングを広げる。
  - `Metadata.update()` の挙動について、Pydantic のバリデーションが正しく走ることを確認するためのドメインテストを強化する。
- **改善案**:
  - `is_ready` ロジックにおいて、アーカイブにない場合は GitHub API を引くロジックを追加することで、より堅牢なクロスリポジトリ依存管理が可能になる。

## 4. SSOT へのフィードバック

- `docs/specs/logic/creation_logic.md` のアルゴリズムは非常に明快で、実装時の迷いが少なかった。
- `Document` モデルの変更（Pydantic化）が最新のコードベースに反映されていたため、古いドキュメントの記述との乖離には注意が必要。
