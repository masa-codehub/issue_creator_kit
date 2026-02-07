# TDD Implementation Plan - ADR-007 Metadata-Driven Lifecycle

## 1. SSOT Audit Log

- **Detailed Spec:**
  - `docs/specs/data/document_model.md`
  - `docs/specs/logic/creation_logic.md`
  - `docs/specs/components/infra_adapters.md`
  - `docs/specs/api/cli_commands.md`
- **Handover (Spec to TDD):** `docs/specs/plans/adr-007-metadata-driven-lifecycle/spec-to-tdd.md`

## 2. Test Strategy (Critical)

### 2.1. Shared Test Data / Fixtures

- **Fixture: Sample Documents**: ADR-007 に準拠した各種メタデータ（Draft, Ready, Issued 等）を持つ Markdown ファイルのディレクトリ構成を `tests/fixtures/adr-007/` に用意する。
- **Fixture: DAG Sets**: 循環依存を含むパターン、深いネストを持つ依存関係などのメタデータセットを定義。

### 2.2. Mocking / Stubbing Policy

- **FileSystemAdapter**: 実ファイルシステムではなく `pyfakefs` を使用することを推奨。
- **GitHubAdapter**: `unittest.mock` もしくは `responses` を使用し、API エラー（429, 500 等）をシミュレートする。
- **GitAdapter**: Git コマンドの出力を Mock し、`--no-renames` が正しく渡されていることを検証。

### 2.3. Testing Environment

- **Runner**: `pytest`
- **Plugins**: `pytest-mock`, `pytest-cov`, `pyfakefs`

## 3. Directory Structure

- **Source**: `src/issue_creator_kit/`
- **Tests**: `tests/unit/`, `tests/integration/`

## 4. Issue Slicing Strategy

- **007-T4-01: [CORE] Data Model & Adapter Protocols (Domain)**
  - `Document`, `Metadata` クラスの実装と、各 Adapter の Interface (Protocol) 定義。
- **007-T4-02: [PARALLEL] Infrastructure Implementation (Infra)**
  - 確定した Interface に基づく具象 Adapter の実装。
  - _Dependency_: `007-T4-01`
- **007-T4-03: [PARALLEL] UseCase Logic (UseCase)**
  - Adapter を Mock して、DAG 解析や起票・移動シーケンスを実装。
  - _Dependency_: `007-T4-01` (T4-02 の完了を待たずに並列実行可能)
- **007-T4-04: CLI Integration (Interface)**
  - `process-diff` の引数追加と UseCase への繋ぎ込み。
  - _Dependency_: `007-T4-03`
- **007-T4-L2: TDD Integration Audit (L2)**
  - 実装アダプターとユースケースの結合テスト。
  - _Dependency_: `007-T4-02`, `007-T4-04`
