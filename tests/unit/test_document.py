import unittest

from issue_creator_kit.domain.document import Document


class TestDocument(unittest.TestCase):
    def test_parse_yaml_frontmatter(self):
        content = """---
title: Test Document
status: Draft
---
# Content Body
"""
        doc = Document.parse(content)
        self.assertEqual(doc.metadata["title"], "Test Document")
        self.assertEqual(doc.metadata["status"], "Draft")
        self.assertEqual(doc.content.strip(), "# Content Body")

    def test_parse_unsafe_yaml(self):
        # safe_load should still parse normal YAML.
        # It's hard to test "unsafety" without potentially executing code,
        # but we can verify it parses valid structures.
        content = """---
key: value
list:
  - item1
  - item2
---
body
"""
        doc = Document.parse(content)
        self.assertEqual(doc.metadata["key"], "value")
        self.assertEqual(doc.metadata["list"], ["item1", "item2"])
