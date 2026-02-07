# Architecture Visualization Plan: [Feature/ADR Name]

- **Status**: Draft / Approved
- **Author**: SYSTEM_ARCHITECT
- **Source ADR**: [Link to ADR]

## 1. コンテキストと目的 (Context & Objective)

<!--
【指示】
なぜ今、アーキテクチャ図を作成・更新するのか？
ADRで決定された「あるべき姿」と、現状のギャップを簡潔に記述する。
-->

- **Objective:** ...
- **Key Decision:** (ADRから抜粋)

## 2. 参照したSSOT一覧 (SSOT Audit Log)

<!--
【指示】
この計画を立てるために「実際に読み込んだ」ファイルの一覧。
レビュアーは、ここに重要なファイル（例: system-context.md）が抜けていないかチェックする。
-->

- [ ] `reqs/design/_approved/adr-xxx.md`
- [ ] `docs/system-context.md`
- [ ] `src/...` (コードの実態確認)

## 3. 共通定義とマッピング (Common Definitions & Mapping)

<!--
【重要】
抽象的な用語（概念）と、具体的なコード（物理）の対応関係を定義する。
「なんとなく」の理解を許さず、パスレベルで指定すること。
-->

### 3.1. ユビキタス言語 (Ubiquitous Language)

| 用語 (Term)      | 定義 (Definition)              | コード上の表現 (Class/Variable) |
| :--------------- | :----------------------------- | :------------------------------ |
| _Example: Inbox_ | _承認待ちドキュメントの置き場_ | _`_inbox/` directory_           |
|                  |                                |                                 |

### 3.2. レイヤーとコンポーネント (Layers & Components)

| レイヤー名       | 責務 (Responsibility) | 具体的なディレクトリ/ファイル (Physical Path) | 禁止事項 (Anti-Pattern)              |
| :--------------- | :-------------------- | :-------------------------------------------- | :----------------------------------- |
| _Example: Infra_ | _外部IOの実行_        | _`src/kit/infrastructure/`_                   | _ビジネスロジックを含んではならない_ |
|                  |                       |                                               |                                      |

## 4. 作図戦略 (Diagram Strategy)

<!--
【指示】
作成する図のリスト。なぜその図が必要なのか（Why）を明記する。
-->

| 図の種類 (Type) | ファイル名 (File Name)  | 描く範囲 (Scope/Boundary) | 目的・伝えたいこと (Intent)              |
| :-------------- | :---------------------- | :------------------------ | :--------------------------------------- |
| _C4 Container_  | `arch-structure-xxx.md` | _`src/kit/` 全体_         | _レイヤー間の依存方向が正しいことを示す_ |
|                 |                         |                           |                                          |

## 5. 技術選定 (Technical Decisions)

- **Diagram Tool:** Mermaid.js
- **Style:** Clean Architecture / C4 Model / etc.
