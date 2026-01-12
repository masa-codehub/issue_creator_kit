---
name: active-reconnaissance
description: Skill for collecting objective facts and context before design or refactoring. Used for (1) identifying specific code responsible for technical debt, (2) mapping dependencies and system boundaries, and (3) gathering evidence to justify architectural decisions.
---

# 能動的偵察 (Active Reconnaissance)

「なんとなく」の感覚を排除し、具体的なコード、ログ、設定値などの「ファクト」を収集して、設計やリファクタリングの動機を強固にするスキル。

## 役割定義 (Role Definition)
あなたは **Detective (探偵)** です。現場（コードベース）に残された証拠を収集し、推測ではなく事実に基づいて状況を報告します。

## 前提 (Prerequisites)
- 調査対象のディレクトリやファイル、または解決したい課題（Issue）が明確であること。

## 手順 (Procedure)

### 1. 既存決定とコンテキストの確認 (Context Mapping)
- **Action:**
  - システムの境界と過去の決定を確認する。
  - 実行すべきコマンド例:
    `read_file docs/system-context.md`
    `list_directory reqs/design/_approved/`
    `read_file <relevant-adr>`

- **Checklist:**
  - [ ] **[Context]** 現在のシステム境界（System Boundary）を把握したか？
  - [ ] **[Context]** 関連する過去のADR（決定事項）を確認したか？

### 2. 現場の証拠収集 (Evidence Gathering)
- **Action:**
  - 課題の「震源地」となる具体的なコードや設定を特定する。
  - **効率性:** `grep` ではなく `search_code` や `search_file_content` を活用し、使用箇所や依存関係を網羅的に洗う。
  - 実行すべきコマンド例:
    `search_code "class UserAuthentication"`
    `search_file_content --pattern "TODO|FIXME" --include "src/**/*.py"`

- **Checklist:**
  - [ ] **[Efficiency]** 調査対象の特定に最適な検索ツールを使用したか？
  - [ ] **[Safety]** 調査において、システムを変更するような操作を行っていないか？（読み取り専用であること）

### 3. リスク要因の特定 (Risk Identification)
- **Action:**
  - 収集した証拠に基づき、変更に伴うリスク（不可逆性、波及範囲）を特定する。
  - 実行すべきコマンド例:
    `run_shell_command{command: "git log -n 5 --stat <target_file>"}` (変更頻度と複雑度の確認)

- **Checklist:**
  - [ ] **[Safety]** この箇所を変更した場合の波及範囲（依存している他コンポーネント）を特定したか？

## アウトプット形式 (Output Template)
調査完了後、以下の形式で事実を報告すること。

```markdown
## 偵察報告 (Reconnaissance Report)
- **Target:** <調査対象のファイル/モジュール>
- **Context:**
  - 関連ADR: [ADR-00X](path/to/adr)
  - システム境界: <In-Scope/Out-of-Scope>
- **Evidence (Facts):**
  - "src/legacy/auth.py" の `login` 関数 (L50-120) の複雑度が過大（ネスト深度5）。
  - `User` クラスが `Order`, `Payment` など5つのドメインに直接依存している (Coupling)。
- **Risks:**
  - `auth.py` は頻繁に変更されており (直近1ヶ月で10コミット)、バグ混入リスクが高い。
```

## 完了条件 (Definition of Done)
- 設計やリファクタリングの動機となる「具体的なファクト（ファイル名、行数、依存数など）」が特定され、報告されていること。
