# Analysis Report - [TDD] CLI Integration (Interface)

## 1. 意図の深掘り (Analyze Intent)
- **目的**: ADR-007 で定義されたメタデータ駆動型ライフサイクルに基づき、特定の ADR ID に関連するタスクのみを抽出して Issue 起票できるようにする。
- **背景**: 大規模なプロジェクトでは多くのタスクが Virtual Queue に溜まるため、特定の設計変更 (ADR) に紐づく単位での実行制御が必要。
- **期待される価値**: 誤ったタスクの起票を防止し、設計意図に沿った段階的な Issue 管理を実現する。

## 2. ギャップ分析 (Gap Analysis)
- **現状 (As-is)**:
    - `cli.py` が古い `IssueCreationUseCase.create_issues_from_virtual_queue` を呼び出している。
    - `--adr-id` 引数が存在せず、バリデーションも未実装。
    - デフォルトパスが古い仕様 (`reqs/tasks/archive/`)。
- **理想 (To-be)**:
    - `cli.py` が `create_issues(adr_id=...)` を呼び出す。
    - `adr-XXX` 形式の厳格なバリデーションが CLI 層で行われる。
    - デフォルトパスが `reqs/tasks/_archive/` に統一されている。

## 3. 仮説の立案 (Formulate Hypotheses)

### 3.1. 実証的仮説 (Grounded - 本命案)
- **内容**: `argparse` の引数追加、正規表現によるバリデーション関数の追加、および UseCase 呼び出しの修正。
- **メリット**: 仕様に忠実であり、実装リスクが低い。
- **デメリット**: 特になし。

### 3.2. 飛躍的仮説 (Leap - 理想案)
- **内容**: ADR ID の型定義 (NewType or ValueObject) を導入し、CLI 層だけでなく UseCase 層でも型レベルでバリデーションを保証する。
- **メリット**: ドメインモデルとしての堅牢性が向上する。
- **デメリット**: 今回のスコープ (CLI 層の修正) を少し超える可能性がある。

### 3.3. 逆説的仮説 (Paradoxical - 別の視点)
- **内容**: CLI ではバリデーションせず、UseCase 側のエラーをキャッチして表示するだけに留める。
- **メリット**: CLI 層が軽量になる。
- **デメリット**: 「CLI 層でバリデーションする」という仕様書に反する。

## 4. 推奨案 (Recommendation)
- **実証的仮説**を採用。仕様書の TDD Criteria に基づき、`argparse` の `type` 引数または実行後のチェックで `adr-XXX` 形式を検証し、失敗時に `sys.exit(1)` する。
