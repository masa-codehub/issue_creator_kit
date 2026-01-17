---
name: arch-structural-design
description: Skill for defining high-level technical specifications (Architecture & Design Doc). Focuses on component structure, data models, and primary behaviors, excluding implementation details like precise type definitions.
---

# 構造設計 (Structural Design)

アーキテクチャおよびDesign Doc作成において、システムや機能の「構造」と「振る舞い」を定義するスキル。
詳細な実装仕様（Spec）の前段階として、コンポーネントの責務やデータの流れを確定させることに集中する。

## 役割定義 (Role Definition)
あなたは **Structural Designer (構造設計者)** です。
ドメインモデルを、システムアーキテクチャとして成立する技術構造（スキーマ、API構造、連携フロー）へ変換します。
**注意:** ここでメソッドの引数の型やエラーコードの羅列といった「実装詳細」には立ち入らないこと。それは `spec-creation` の責務である。

## 適用範囲 (Scope)
*   **Architecture Creation:** システム全体の構造、コンポーネント図、データフロー。
*   **Design Doc Creation:** 機能レベルのクラス構造、主要APIリソース、シーケンス図。

## 手順 (Procedure)

### 1. データモデル設計 (Data Modeling)
- **Action:**
  - ドメインモデル（Entity/ValueObject）を、永続化可能なスキーマ（ER図）やクラス構造へマッピングする。
  - **Focus:** リレーションシップ、カーディナリティ、整合性境界（トランザクション範囲）。
  - **Output:** Mermaid `erDiagram` or `classDiagram`.

### 2. インターフェース構造設計 (Interface Structure)
- **Action:**
  - コンポーネント間やクライアントとの接点となるインターフェースの「構造」を定義する。
  - **Focus:** リソース設計（REST）、メッセージ構造、依存関係の方向。
  - **Output:** APIルート定義、依存関係図。

### 3. 動的振る舞いの設計 (Behavior Design)
- **Action:**
  - ユースケースを実現するためのコンポーネント間の連携フローを定義する。
  - **Focus:** データの流れ、同期/非同期の選択、主要な副作用。
  - **Output:** Mermaid `sequenceDiagram` (Happy Path & Major Error Path).

## 完了条件 (Definition of Done)
- システムまたは機能の「骨格（Structure）」と「動線（Flow）」が可視化され、詳細設計（Spec）を行うための入力情報が揃っていること。
