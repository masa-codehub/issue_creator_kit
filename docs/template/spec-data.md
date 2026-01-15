# [Data Model Name] Specification

## Overview
<!-- データモデルの目的 -->

## Schema Definition
- **Table/Collection Name:** `users`

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK | ... |
| `email` | VARCHAR(255) | Unique, Not Null | ... |
| `created_at` | TIMESTAMP | Default NOW() | ... |

## Indexes
- `idx_users_email` (Unique)

## Relationships
- One-to-Many with `orders` (FK: `user_id`)

## Migration Strategy
<!-- 既存データへの影響と移行手順 -->
- `Safe`: カラム追加のみ。
