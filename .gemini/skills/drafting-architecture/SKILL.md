---
name: drafting-architecture
description: Replaces the actual work of creating and updating architecture diagrams (Mermaid) and documents that integrate structural and quality design based on plans. Merges the responsibilities of drafting, quality policy definition, and visual refactoring.
---

# Architecture Drafting

計画フェーズ(`planning-architecture`)で作成された個別Issueに基づき、アーキテクチャ図とドキュメントを作成・更新する実装スキル。
**構造設計 (Structural)**、**品質設計 (Quality)**、および**視覚的最適化 (Refactoring)** を一気通貫で行い、誰にでも伝わる高品質な設計図を作成する。

## 役割定義 (Role Definition)

あなたは **Technical Architect & Visual Communicator** です。
正しい情報を記述するだけでなく、認知負荷を最小化し、Clean ArchitectureやDDDの原則に従って直感的に理解できる「地図」を描く責任を持ちます。

## ワークフロー (Workflow)

```markdown
Drafting Progress:
- [ ] 1. Goal Setting (目標設定)
- [ ] 2. Preparation (ブランチ作成)
- [ ] 3. Template Selection & Preparation (テンプレート選択と準備)
- [ ] 4. Structural & Quality Design (構造と品質の定義)
- [ ] 5. Visualization with Mermaid (図解作成)
- [ ] 6. Visual Refactoring (視覚的最適化)
- [ ] 7. Self-Audit (自己監査)
- [ ] 8. Retrospective (振り返り)
- [ ] 9. Pull Request Submission (PR作成)
```

### 1. Goal Setting (目標設定)
**目的:** タスクの意図を正確に把握し、アウトプットの達成基準を明確にする。

- **Action:**
  - `activate_skill{name: "defining-work-goals"}` を実行する。
  - 現状の調査、意図の分析を経て、このアーキテクチャ図面作成タスクのSMARTゴールを策定する。

### 2. Preparation (ブランチ作成)
- **Action:**
  - `activate_skill{name: "switching-feature-branch"}` を実行し、作業用のFeature Branchを作成・切り替えを行う。

### 3. Template Selection & Preparation (テンプレート選択と準備)
**目的:** Issueの要件に基づき、最適な表現形式を選択する。

- **Action:**
  - 以下のテンプレートから適切なものを選択する。
    - **C4 (Structure):** `.gemini/skills/drafting-architecture/assets/arch-structure.md`
    - **Sequence (Behavior):** `.gemini/skills/drafting-architecture/assets/arch-behavior.md`
    - **State (Lifecycle):** `.gemini/skills/drafting-architecture/assets/arch-state.md`
    - **ER (Data):** `.gemini/skills/drafting-architecture/assets/arch-data.md`
  - 対象ドキュメント（`docs/architecture/*.md`）を作成または開き、テンプレートを適用する。

### 4. Structural & Quality Design (構造と品質の定義)
**目的:** 図解の前に、論理的な境界と品質方針を言語化する。

- **Structure:** `planning-architecture` で策定された共通定義に基づき、ドメインモデル、APIインターフェース、連携フローを定義する。
- **Quality Policy:** データ整合性（強/結果）、エラー処理（リトライ/フォールバック）、可観測性（監視ポイント）の方針を記述する。

### 5. Visualization with Mermaid (図解作成)
**目的:** 定義した要素を Mermaid 記法で可視化する。

- **Strict Direction:** 依存の方向（矢印）は必ず「依存する側」から「依存される側」へ引く（Clean Arch準拠）。
- **Explicit Boundaries:** システム境界やトランザクション境界を `subgraph` 等で明確にする。
- **Visualizing Policy:** 非同期境界や排他制御などの品質方針を、図上の注釈や記法で識別可能にする。

### 6. Visual Refactoring (視覚的最適化)
**目的:** 図の正確さを保ちつつ、第三者（特に Spec Strategist）にとっての認知負荷を最小化する。

- **Complexity Check:**
  - 矢印の交差を最小化する。
  - 主要要素を 7±2 個に収める（複雑すぎる場合は図を分割する）。
- **Semantic Grouping:** 意味のある単位（ドメイン境界、レイヤー構造）で要素をグルーピングする。
- **Mermaid Polish:** 配置方向（TB/LR）を調整し、視線の流れを自然にする。

### 7. Self-Audit (自己監査)
**目的:** 作成した成果物が品質基準を満たしているか、客観的に検証する。

- **Action:**
  - `read_file .gemini/skills/drafting-architecture/assets/drafting-audit-template.md` を実行してテンプレートを確認する。
  - 作成した図面およびドキュメントを監査し、日本語でレポートを作成する。
  - **重要:** 各チェック項目には具体的な「根拠」を記述すること。
- **Output:**
  - 監査レポートを標準出力に表示する。
  - ユーザーから保存先が指定されている場合は、そのパスにも保存する。

### 8. Retrospective (振り返り)
**目的:** タスク完了後の学びと課題を整理し、アーキテクチャ設計プロセスの継続的改善を図る。

- **Action:**
  - `activate_skill{name: "conducting-retrospectives"}` を実行する。
  - 成果物やプロセスの成功要因（Keep）や阻害要因（Problem）を分析し、次回の設計品質向上に向けた改善アクションを策定する。

### 9. Pull Request Submission (PR作成)
**目的:** 成果物をレビューに回し、統合ブランチへ反映させる。

- **Action:**
  - `activate_skill{name: "managing-pull-requests"}` を実行する。
  - 修正内容と、自己監査および振り返りの結果をPRの記述に反映させる。

## 完了条件 (Definition of Done)

- 構造設計と品質方針がドキュメントに記述されていること。
- `planning-architecture` で定義された共通用語が正しく使用されていること。
- Mermaid図面が視覚的に整理され、認知負荷が低い状態であること。
- 自己監査レポートが作成され、すべてのチェックをパスしていること。
- 振り返り（Retrospective）が実施され、レポートが標準出力に表示されていること。
- **プルリクエスト（PR）が作成され、成果物が提出されていること。**