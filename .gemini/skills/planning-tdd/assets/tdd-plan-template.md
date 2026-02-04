# TDD Implementation Plan

## 1. SSOT Audit Log
- **Detailed Spec:** `docs/specs/{domain}/{file}.md`
- **Handover (Spec to TDD):** `docs/specs/plans/adr-XXX/spec-to-tdd.md`

## 2. Test Strategy (Critical)

### 2.1. Shared Test Data / Fixtures
<!-- 全タスクで共通して使用するテストデータやフィクスチャの定義 -->
- **Data A:** ...
- **Data B:** ...

### 2.2. Mocking / Stubbing Policy
<!-- 外部APIやDB、他モジュールのモック方針 -->
- **External API:** Use `responses` or `unittest.mock`...
- **Database:** Use `pytest-postgresql` or memory DB...

### 2.3. Testing Environment
- **Runner:** `pytest`
- **Plugins:** `pytest-cov`, `pytest-mock`...

## 3. Directory Structure
- **Source:** `src/{package}/`
- **Tests:** `tests/unit/`, `tests/integration/`

## 4. Issue Slicing Strategy
- **Policy:** 1 Issue per 1 Class or Module.
- **Integration Issue:** Required for final audit.
