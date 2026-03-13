# Document Model Extension Specification

## Overview

ADR-016 に基づき、DesignDoc (`design-XXX`) を第一級のドキュメントタイプとしてサポートするためのドメインモデルの拡張仕様を定義する。

## Related Documents

- ADR: `reqs/design/_approved/adr-016.md`

## Schema Definition (Domain Models)

`src/issue_creator_kit/domain/models/document.py` における以下の定義を拡張する。

### 1. ADR_ID_PATTERN

`adr-XXX` に加え、`design-XXX` 形式を許容する。

- **Before:** `re.compile(r"^adr-\d{3}(?:-[a-z0-9-]+)?$")`
- **After:** `re.compile(r"^(adr|design)-\d{3}(?:-[a-z0-9-]+)?$")`

### 2. ADR Model

`type` フィールドで `design-doc` を許容する。

- **Field:** `type`
- **Type:** `Literal["adr", "design-doc"]`
- **Constraints:** `adr-XXX` の場合は `type="adr"`、`design-XXX` の場合は `type="design-doc"` であることをバリデーションする（任意）。
  - ※ 簡略化のため、`ADR` クラス名を `L1Document` 等にリネームせず、既存の `ADR` クラスを拡張して使用する。

### 3. Task.adr_number Property

`parent` ID から数値を抽出するロジックを `design-XXX` にも対応させる。

- **Logic:**
  ```python
  @property
  def adr_number(self) -> int | None:
      """Extract the 3-digit number from the parent ID (e.g., adr-010 or design-001 -> 10 or 1)."""
      match = re.search(r"(?:adr|design)-(\d{3})", self.parent)
      return int(match.group(1)) if match else None
  ```

## Migration Strategy

- **既存データへの影響**:
  - `ADR_ID_PATTERN` の拡張は後方互換性がある。
  - `ADR.type` への `design-doc` 追加も既存の `adr` タイプに影響しない。
- **移行手順**:
  - Pydantic モデルの更新のみ。DB 移行などは不要（GitHub Issue のラベルやメタデータ形式に依存するため）。

## Verification Criteria

- [ ] `validate_adr_id("design-001")` がパスすること。
- [ ] `ADR(id="design-001", type="design-doc", ...)` がバリデーションをパスすること。
- [ ] `Task(parent="design-001", ...).adr_number` が `1` を返すこと。
