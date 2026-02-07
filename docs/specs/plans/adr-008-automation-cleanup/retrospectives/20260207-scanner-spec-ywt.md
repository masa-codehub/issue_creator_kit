# 振り返りレポート (YWT) - FileSystemScanner Specification

## 1. Y (やったこと)
- **作業の実施内容:**
  - ADR-008 に基づき、`FileSystemScanner` の詳細仕様書 (`docs/specs/logic/scanner-logic.md`) を作成。
  - `reqs/` ディレクトリ配下の物理構造を調査し、`_approved` と `_archive` の関係性を確認。
  - YAML メタデータの `id` 重複に関するギャップを特定し、スキャナーロジックにガードレールを追加。
- **事象の観測:**
  - `reqs/tasks/adr-008/task-01-domain.md` と `reqs/tasks/_archive/task-01-archive.md` が同一の ID (`task-008-01`) を持っていることを発見。
- **分析情報の集約:**
  - `docs/architecture/arch-structure-008-scanner.md` (SSOT)
  - `docs/specs/data/domain_models_adr008.md` (Domain Models)
  - `reqs/` 配下の `ls -R` 結果。

## 2. W (わかったこと)
- **結果の確認:**
  - 物理的なファイルパスが異なっても YAML メタデータの `id` が重複する場合があり、単純な ID ベースの「処理済み」判定だけでは、未処理タスクがアーカイブ済み ID と衝突して無視されるリスクがある。

### ギャップ分析
- **理想 (To-Be):**
  - すべての `Task` / `ADR` はグローバルにユニークな ID を持ち、ID 重複は Domain Guardrails により即座に排除される。
- **現状 (As-Is):**
  - アーカイブ済みの古いタスクと、ADR フォルダ配下の新しいタスクで ID 重複が発生している。
- **ギャップ:**
  - ID の一意性が物理的に（ファイルレベルで）保証されていない。
- **要因 (Root Cause):**
  - これまでのタスク作成において、ID の一意性チェックが自動化されておらず、手動管理または古い仕組みでの ID 採番が重複していたため。

## 3. T (次やること / 仮説立案)
- **実証的仮説:**
  - スキャナーの初期化フェーズで全対象ファイルの ID 重複をチェックし、重複があれば `DUPLICATE_ID` エラーで停止させることで、整合性を強制できる。
- **飛躍的仮説:**
  - `TaskParser` を、ファイル読み込み時だけでなく、保存時（`issue-kit create` 等）にも強制適用し、重複 ID を持つファイルの作成自体を物理的に防ぐ仕組みを導入する。
- **逆説的仮説:**
  - ID の重複は許容し、`parent (ADR)` ID と `Task` ID の組み合わせ、あるいはファイルハッシュをキーとして状態を管理する。

### 検証アクション
- [x] `docs/specs/logic/scanner-logic.md` に ID 重複検知ロジックを明記し、TDD 基準に反映した。
- [ ] 実装フェーズにおいて、重複 ID を持つテスト用ディレクトリ構造を作成し、スキャナーが期待通りエラーを出すか検証する。
