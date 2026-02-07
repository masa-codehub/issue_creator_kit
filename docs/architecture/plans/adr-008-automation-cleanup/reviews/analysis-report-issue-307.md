# 目的分析レポート (Analysis Report)

## 1. 意図の深掘り (Intent & Context)
- **ユーザーの真の目的 (Outcome):** メタデータ定義にドメインガードレール（制約ルール）を明文化することで、自動化ツール（Scanner 等）や開発者が一貫したバリデーションを行えるようにし、システムの状態（Task/ADR の ID や依存関係）の健全性を保つ。
- **背景と文脈 (Why):** ADR-008 "Domain Guardrails" の導入に伴い、アーキテクチャドキュメントを最新の状態に更新し、物理的な配置だけでなく論理的な整合性（循環参照の禁止など）を SSOT として定義する必要がある。
- **制約条件 (Constraints):**
    - 既存の `docs/architecture/arch-structure-007-metadata.md` の構造を維持しつつ追記する。
    - バリデーションルールは自然言語（Regex 等）で記述し、Pydantic モデルへのマッピングを明示する。
    - 依存の方向性は Clean Architecture に準拠し、ドキュメントからコード（ドメイン層）へのマッピングを明確にする。

## 2. ギャップ分析 (Gap Analysis)
- **現状 (As-Is):**
    - `arch-structure-007-metadata.md` にはフィールドレベルのバリデーションルールが記述されていない。
    - 実装（`document.py`）の ID バリデーションが ADR-008 の規定（`adr-\d{3}-.*` 等）より緩い。
    - 実装コードの配置が `src/issue_creator_kit/domain/models` ではなく `document.py` に集約されている（ドキュメント上のマッピング予定と乖離）。
- **理想 (To-Be):**
    - `arch-structure-007-metadata.md` に各メタデータフィールド（`id`, `depends_on`, `status`, `issue_id`）の具体的な検証ルールが記述されている。
    - 検証ルールが `src/issue_creator_kit/domain/models` で実装されることが明記されている。
- **特定されたギャップ:**
    - バリデーションルール定義の欠落。
    - ドキュメントが想定するディレクトリ構造 (`domain/models`) と現実のファイル配置 (`domain/document.py`) の不一致。

## 3. 仮説オプション (Hypothesis Options)

### 案A: 実証的仮説 (Grounded) - 本命案
*(事実に基づいた最も確実なアプローチ)*
- **アプローチ:** `arch-structure-007-metadata.md` に「Metadata Field Definitions & Guardrails」セクションを追加。`id` (Regex), `depends_on` (DAG Integrity), `status` (Enum), `issue_id` (Conditional mandatory) のルールを記述。実装マッピングとして、これらが将来的に `src/issue_creator_kit/domain/models` に集約される旨を注記する（現状が `document.py` であることも補足）。
- **メリット/デメリット:** 既存ドキュメントの整合性を保ちつつ、ADR-008 の要件を充足できる。 / 実際のコード配置との一時的な乖離が残る。
- **リスク (4大リスク):** 実現可能性 (Feasibility): 高い。単なるドキュメント更新のため。
- **検証の視点:** ドキュメントを読み、Pydantic Validator に変換可能な制約が定義されているか。

### 案B: 飛躍的仮説 (Leap) - 理想案
*(潜在ニーズを捉えた、より高度なアプローチ)*
- **アプローチ:** 案Aに加え、Mermaid JS を用いて「メタデータの状態遷移図」や「依存関係のバリデーションフロー」を視覚化する。
- **メリット/デメリット:** 認知負荷がさらに下がる。 / 作成コストが増加する。
- **リスク:** 複雑さが増し、逆に理解を妨げる可能性がある。
- **検証の視点:** 図解によってバリデーションロジックが直感的に理解できるか。

### 案C: 逆説的仮説 (Paradoxical) - 代替案
*(前提を疑い、別角度から解決するアプローチ)*
- **アプローチ:** メタデータ定義を Markdown ではなく YAML Schema (JSON Schema) として独立させ、ドキュメントからはそれを参照する形式にする。
- **メリット/デメリット:** 自動テストでの利用が容易になる。 / 閲覧性が下がる。
- **リスク:** プロジェクトの既存慣習（Markdownベース）から外れる。
- **検証の視点:** スキーマファイルがドキュメントとして機能するか。

## 4. 推奨される方針 (Recommendation)
- **推奨案:** **案A (実証的仮説)** をベースにし、一部 **案B (Mermaidでの補足)** を取り入れる。
- **理由:** Issue の主目的は「明文化」と「実装マッピング」であり、案Aが最も直接的に応えられる。また、依存関係の制約（循環参照禁止）などは図解があったほうが理解しやすいため、簡単な Mermaid 図を追加する。
- **残存する不確実性 (Unknowns):** `src/issue_creator_kit/domain/models` ディレクトリを今回のタスクで作成すべきか。Issue の指示は「実装される旨を注記」であるため、ドキュメント上の記述に留めるのが安全と判断する。
