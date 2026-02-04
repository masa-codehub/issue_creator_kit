# [API Name] Specification

## Overview
<!-- APIの目的と概要 -->
- **Endpoint:** `[METHOD] /path/to/resource`
- **Summary:** ...

## Request
### Headers
| Name | Required | Type | Description |
| :--- | :--- | :--- | :--- |
| `Authorization` | Yes | Bearer Token | ... |

### Path/Query Parameters
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | Path | Yes | UUID | ... |

### Body (JSON)
```jsonc
{
  "name": "string (max 255, required)",
  "age": "integer (min 0, optional)"
}
```

## Response

### Success (200 OK)
```jsonc
{
  "id": "UUID",
  ...
}
```

### Errors
| Code | Reason | Body Structure |
| :--- | :--- | :--- |
| 400 | Validation Error | `{ "errors": [...] }` |
| 401 | Unauthorized | ... |

## Processing Logic
<!-- 実装すべき処理の流れ -->
1.  リクエストバリデーション...
2.  権限チェック...
3.  ...
