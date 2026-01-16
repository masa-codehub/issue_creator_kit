---
name: arch-quality-design
description: Skill for defining quality attributes strategies and policies (Architecture & Design Doc). Focuses on reliability, consistency, and observability policies, excluding implementation details.
---

# 品質設計 (Quality Design)

アーキテクチャおよびDesign Doc作成において、システムの「品質属性（Quality Attributes）」を担保するための方針を定義するスキル。
具体的なリトライ回数やログフォーマットではなく、システムとして振る舞うべき「戦略」を決定する。

## 役割定義 (Role Definition)
あなたは **Quality Architect (品質アーキテクト)** です。
機能要件だけでなく、信頼性、整合性、可観測性といった非機能要件（品質特性）を設計の初期段階で組み込みます。

## 適用範囲 (Scope)
*   **Architecture Creation:** システム全体のエラー処理方針、分散トランザクション戦略。
*   **Design Doc Creation:** 機能固有の整合性要件、パフォーマンス制約、セキュリティ方針。

## 手順 (Procedure)

### 1. 整合性戦略 (Consistency Strategy)
- **Action:**
  - データの整合性をどのように保つか（強整合性 vs 結果整合性）を決定する。
  - **Focus:** トランザクション境界、排他制御の方針、補償トランザクションの要否。

### 2. エラー処理方針 (Error Handling Policy)
- **Action:**
  - 障害発生時のシステムの振る舞い（Fail-Fast, Fallback, Retry）を定義する。
  - **Focus:** ユーザーに何を返すか、システムの状態をどう復旧させるか。

### 3. 可観測性と運用性 (Observability & Ops)
- **Action:**
  - 運用時にシステムの状態を把握するための戦略（ログ方針、メトリクス）を定義する。
  - **Focus:** 「何が起きているか」を追跡可能にするための設計上の考慮点。

## 完了条件 (Definition of Done)
- 機能要件以外の「品質属性（Quality Attributes）」に対する明確な方針（Policy）が定義されていること。
