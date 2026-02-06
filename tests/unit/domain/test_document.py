import pytest

from issue_creator_kit.domain.document import Document
from issue_creator_kit.domain.exceptions import ValidationError


def test_parse_yaml_frontmatter():
    content = """---
id: test-doc
status: Draft
title: Test Document
---
# Content Body
"""
    doc = Document.parse(content)
    assert doc.metadata["id"] == "test-doc"
    assert doc.metadata["status"] == "Draft"
    assert doc.metadata["title"] == "Test Document"
    assert doc.content.strip() == "# Content Body"


def test_metadata_normalization_japanese():
    content = """---
ID: test-001
ステータス: Ready
型: task
フェーズ: domain
親: adr-007
依存:
  - 007-T1
---
"""
    doc = Document.parse(content)
    assert doc.metadata["id"] == "test-001"
    assert doc.metadata["status"] == "Ready"
    assert doc.metadata["type"] == "task"
    assert doc.metadata["phase"] == "domain"
    assert doc.metadata["parent"] == "adr-007"
    assert doc.metadata["depends_on"] == ["007-T1"]


def test_metadata_validation_missing_required():
    content = """---
id: only-id
---
"""
    with pytest.raises(ValidationError) as excinfo:
        Document.parse(content)
    assert "status" in str(excinfo.value).lower()


def test_metadata_validation_invalid_id():
    content = """---
id: Invalid_ID!
status: Draft
---
"""
    with pytest.raises(ValidationError) as excinfo:
        Document.parse(content)
    assert "id" in str(excinfo.value).lower()


def test_metadata_validation_invalid_status():
    content = """---
id: test-001
status: UnknownStatus
---
"""
    with pytest.raises(ValidationError) as excinfo:
        Document.parse(content)
    assert "status" in str(excinfo.value).lower()


def test_metadata_validation_task_specific_fields():
    content = """---
id: 007-t1
status: Draft
type: task
# missing phase, parent, depends_on
---
"""
    with pytest.raises(ValidationError) as excinfo:
        Document.parse(content)
    assert any(
        field in str(excinfo.value).lower()
        for field in ["phase", "parent", "depends_on"]
    )


def test_metadata_validation_issued_without_id():
    content = """---
id: 007-t1
status: Issued
parent: adr-007
type: task
phase: domain
depends_on: []
# missing issue_id
---
"""
    with pytest.raises(ValidationError) as excinfo:
        Document.parse(content)
    assert "issue_id" in str(excinfo.value).lower()


def test_metadata_dict_compatibility():
    content = """---
id: test-001
status: Draft
---
"""
    doc = Document.parse(content)
    # Test dict-like access
    assert doc.metadata["id"] == "test-001"
    assert doc.metadata.get("status") == "Draft"
    assert doc.metadata.get("non-existent", "default") == "default"

    # Test iteration
    keys = list(doc.metadata.keys())
    assert "id" in keys
    assert "status" in keys


def test_to_string_preserves_metadata():
    content = """---
id: test-001
status: Draft
---
Body content"""
    doc = Document.parse(content)
    output = doc.to_string()
    assert "id: test-001" in output
    assert "status: Draft" in output
    assert "Body content" in output
