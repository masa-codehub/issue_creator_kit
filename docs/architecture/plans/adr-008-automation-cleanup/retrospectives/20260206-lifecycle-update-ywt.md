# 振り返りレポート (YWT): Physical State Lifecycle Update

## 1. Y (やったこと)
- **作業の実施内容:**
    - `activate_skill{name: "drafting-architecture"}` を実行し、アーキテクチャ更新プロセスを開始。
    - `docs/architecture/arch-state-007-lifecycle.md` を更新し、ADR-007 (Metadata-driven) から ADR-008 (Physical State) への移行を反映。
    - 状態を `Draft (Inbox)`, `Approved`, `Done (Archive)` の3つに集約。
    - トリガーを「Manual PR Merge」と「Task Completion」に整理。
    - 物理ディレクトリ (`_inbox`, `_approved`, `_archive`) との状態対応を明文化。
- **事象の観測:**
    - ADR-007 の旧定義には、`ick sync` や `ick create` などの CLI ツールに依存した自動遷移が多く含まれていたが、ADR-008 の方針によりこれらを「人間による物理的な移動（マージ）」という単純なルールに置き換えることができた。
- **分析情報の集約:**
    - `docs/architecture/plans/adr-008-automation-cleanup/definitions.md` (Physical State Scanner の定義)
    - `docs/architecture/arch-state-007-lifecycle.md` (編集対象)

## 2. W (わかったこと)
- **結果の確認:**
    - 物理的な位置を SSOT とすることで、ドキュメントの状態管理が Git の標準的なワークフロー（PR とマージ）に統合され、認知負荷が大幅に下がることがわかった。
    - 以前の「Ready」や「Issued」といった中間状態は、物理的には `_approved` の中に含まれる「属性」に過ぎず、ライフサイクル全体としては `Approved` という一つの大きな状態で管理するのが妥当であると結論付けた。

### ギャップ分析
- **理想 (To-Be):**
    - ライフサイクルが「物理ディレクトリ」と「手動承認」のみに基づき、自動化スクリプトによる状態遷移を含まない状態。
- **現状 (As-Is):**
    - 更新前のファイルは、古い CLI ツールの動作を前提とした複雑な遷移（Ready, Issued）を記述していた。
- **ギャップ:**
    - 物理ディレクトリとの対応関係が不明確で、状態遷移のトリガーが分散していた。
- **要因 (Root Cause):**
    - ADR-007 の時点では、ツールの自動化によって状態を管理する設計だったが、その後の運用で「物理的な位置が真実である」という ADR-008 の方針が採用されたため、不整合が生じていた。

## 3. T (次やること / 仮説立案)
- **実証的仮説:**
    - 今回定義した物理状態に基づき、スキャナー (`src/issue_creator_kit/domain/services/scanner.py`) を実装することで、ドキュメントの現状を正確に把握できるようになる。
- **飛躍的仮説:**
    - `_approved` にあるファイルがいつまでも放置されないよう、マージからの経過時間を監視する「滞留検知」のガードレールをスキャナーに追加することで、プロジェクトの停滞を自動で検知できる。
- **逆説的仮説:**
    - そもそも `_inbox` や `_approved` といったディレクトリ移動自体を人間が行うのではなく、GitHub Label の付与に連動して Git 側でファイルを物理移動させる Bot を導入することで、人間の操作を最小限にしつつ物理的 SSOT を維持できるのではないか。

### 検証アクション
- [ ] スキャナーの実装タスク (#305) において、今回定義した `_inbox`, `_approved`, `_archive` のマッピングが正しく動作するかテストコードで検証する。
