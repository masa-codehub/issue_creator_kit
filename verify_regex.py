import re

def test_regex(pattern, test_cases):
    print(f"Pattern: {pattern}")
    for content, new_value, expected_match in test_cases:
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            # 置換シミュレーション
            replaced = re.sub(pattern, rf"\1{new_value}", content, flags=re.MULTILINE)
            print(f"MATCH: '{content.strip()}' -> '{replaced.strip()}'")
            if not expected_match:
                print("  !!! Error: Should NOT have matched.")
        else:
            print(f"NO MATCH: '{content.strip()}'")
            if expected_match:
                print("  !!! Error: Should have matched.")

# 現行の抽出用正規表現 (参考)
# r"^-\s*\*\*(.*?)\*\*:\s*(.*)"

# 置換用の設計
# キーを固定して値を置換する場合
# 例: Status を更新したい
key_to_update = "Status"
# 1. 行頭 (リストマーカー - または *)
# 2. キー (太字 **Key** を想定)
# 3. セパレータ : とその後の空白
# 4. 値 (行末まで)
pattern = rf"^([-*]\s*\*\*{key_to_update}\*\*:\s*)(.*)$"

test_cases = [
    ("- **Status**: 提案中", "承認済み", True),
    ("* **Status**: 提案中", "承認済み", True),
    ("  - **Status**: 提案中", "承認済み", False), # インデントありは除外
    ("- **Status**:提案中", "承認済み", True),    # 空白なし
    ("- **Status** : 提案中", "承認済み", False),  # キーの後に空白（現行も非対応）
    ("- Status: 提案中", "承認済み", False),       # 太字なし（現行も非対応）
    ("本文中の - **Status**: は無視", "承認済み", False),
]

test_regex(pattern, test_cases)
