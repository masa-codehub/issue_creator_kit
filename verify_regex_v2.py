import re

def test_regex(key_to_update, new_value, test_cases):
    # 改良版パターン: 
    # 1. 行頭のリストマーカー (- または *)
    # 2. 前後の任意の空白 (\s*)
    # 3. 任意の太字装飾 (\*\*?)
    # 4. キー
    # 5. セパレータと空白
    # キャプチャグループ \1 は「値の直前まで」を保持する
    pattern = rf"^([-*]\s*\*{{0,2}}{key_to_update}\*{{0,2}}:\s*)(.*)$"
    
    print(f"Key: {key_to_update}, Pattern: {pattern}")
    for content in test_cases:
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            # \1 を維持して値を置換
            replaced = re.sub(pattern, rf"\1{new_value}", content, flags=re.MULTILINE)
            print(f"MATCH:    '{content}' -> '{replaced}'")
        else:
            print(f"NO MATCH: '{content}'")

key = "Status"
val = "承認済み"
cases = [
    "- **Status**: 提案中",
    "* **Status**: 提案中",
    "- Status: 提案中",
    "- *Status*: 提案中",
    "  - **Status**: 提案中", # 行頭以外はマッチしない
    "- **Status**:提案中",    # 空白なし
    "- **Date**: 2025-01-01", # キー違いはマッチしない
]

test_regex(key, val, cases)
