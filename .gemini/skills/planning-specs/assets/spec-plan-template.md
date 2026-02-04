# [Feature Name] Specification Plan

## 1. SSOT Audit Log
- **Source Design Doc:** `reqs/design/_approved/design-XXX-title.md`
- **System Context:** `docs/system-context.md`
- **Common Definitions (Arch):** `docs/architecture/plans/adr-XXX/definitions.md`

## 2. Common Definitions & Standards (Critical)

### 2.1. Ubiquitous Language (Naming)
<!-- コードやドキュメントで統一して使用する用語 -->
- **Term A:** Definition...
- **Term B:** Definition...

### 2.2. Common Data Types
<!-- システム全体で共通の型定義（DDDのValue Object等） -->
| Type Name | Base Type | Constraints (Min, Max, Regex) |
| :--- | :--- | :--- |
| *UserId* | *String* | *UUID v4* |
| *Email* | *String* | *RFC 5322 format* |

### 2.3. API Conventions
<!-- REST APIのパス規則や共通レスポンス構造 -->
- **Base Path:** `/api/v1/...`
- **Pagination:** `?page=1&limit=20` (Default limit: 20)
- **Date Format:** ISO 8601 (`YYYY-MM-DDThh:mm:ssZ`)

### 2.4. Error Handling Policy
<!-- 共通のエラーコード体系 -->
| Error Code | HTTP Status | Description |
| :--- | :--- | :--- |
| *VALIDATION_ERROR* | *400* | *Input validation failed* |
| *RESOURCE_NOT_FOUND* | *404* | *Target resource does not exist* |

## 3. Directory Structure & Naming
<!-- 仕様書の配置ルール -->
- **Specs Directory:** `docs/specs/{domain}/`
- **File Naming:** `kebab-case.md` (e.g., `user-registration.md`)

## 4. Issue Slicing Strategy
<!-- どの単位でIssueを切るか -->
- **Policy:** 1 Issue per 1 Spec File.
