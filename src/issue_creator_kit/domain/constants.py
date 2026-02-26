import re

# Regex to parse dependency items in the format: - [ ] #123 (id)
# Group 1: Issue Number, Group 2: Task/ADR ID
RE_DEPENDENCY_ITEM = re.compile(r"-\s*\[[ x]\]\s*#(\d+)\s*\(([\w-]+)\)")

# Regex to extract metadata from HTML comments: <!-- metadata:{...} -->
RE_METADATA = re.compile(r"<!--\s*metadata:(.*?)-->", re.DOTALL)
