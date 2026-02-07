# Virtual Queue & Adapters Structure (ADR-003)

> **DEPRECATED: This document is based on ADR-003 and has been superseded by the new architecture defined in ADR-007.**
> Please refer to the new architecture documents, such as [`arch-structure-007-metadata.md`](../arch-structure-007-metadata.md) and [`arch-state-007-lifecycle.md`](../arch-state-007-lifecycle.md).

## Context

ADR-003 で導入された「仮想キュー（Virtual Queue）」方式と「フェーズ連鎖（Auto-PR）」を実現するためのコンポーネント構造です。

- **Bounded Context:** Task Lifecycle Management
- **System Purpose:** 物理的なディレクトリ移動（Virtual Queue）をトリガーとして、自律的な Issue 起票とフェーズ推進を自動化する。
