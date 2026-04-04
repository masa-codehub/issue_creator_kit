# Project Structure Specification (ADR-017)

## 1. Overview

本ドキュメントは、テスト駆動アーキテクチャ (TDA) に準拠したプロジェクトの物理構造を「仕様」として定義する。

## 2. Target Structure

Issue Creator Kit の標準ディレクトリ構成は以下の通りとする。

```text
design/                     # [SSOT Root]
├── system-context.md       # システム全体設計
├── adrs/                   # [ARCHIVE] 実装完了済み ADR
├── architecture/           # [MACRO] 階層化図面 (L1-L3)
│   ├── workspace.dsl       # 分散DSLのエントリポイント
│   ├── context/            # L1: people.dsl, system-context.dsl
│   ├── container/          # L2: container-diagram.dsl
│   └── component/          # L3: {container}-components.dsl
└── specs/                  # [DETAIL] 詳細仕様 (API, DB, Behavior)
    ├── api/                # OpenAPI/AsyncAPI
    ├── interface/          # Gherkin/CLI UX
    ├── data/               # DBML/JSON Schema
    ├── logic/              # XState/Sequence
    └── behavior/           # UseCase flows
policies/                   # [CONSTRAINT] OPA/Spectral rules
reqs/                       # [WORKSPACE]
├── design/
│   ├── _inbox/             # [DRAFT] 検討中のADR
│   └── _approved/          # [ACTIVE SSOT] 実装待ちのADR
├── context/                # target-context.md / conversation-logs
└── tasks/                  # GitHub Issue drafts
src/                        # [REALIZATION] Python implementations
tests/                      # [VERIFICATION] unit/integration/tda tests
```

## 3. Constraints

- **[STR-01]**: 全ての詳細設計ファイルは `design/specs/` 配下の適切なサブディレクトリに配置しなければならない。
- **[STR-02]**: `design/specs/` および `policies/specs/` 配下のファイル名には ADR ID を含めず、プレーンで論理的な名前（例: `openapi.yaml`）を維持すること。これにより、将来の ADR による更新時の参照安定性を確保する。
- **[STR-03]**: `reqs/tasks/` 配下のファイルは、処理完了後に `reqs/tasks/_archive/` へ移動（または削除）されるべきである。
- **[STR-04]**: `design/architecture/structurizr.json` はマクロ構造の絶対制約（防波堤）として維持し、詳細設計はこの範囲内で行うこと。
