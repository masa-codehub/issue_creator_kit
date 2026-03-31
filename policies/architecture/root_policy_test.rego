package architecture.root_test

import data.architecture.root as policy
import future.keywords.if

# Rule 1: design/ 配下のファイル拡張子をテスト
test_rule1_deny_invalid_extension_in_subdir if {
    test_input := {
        "design_root_files": [
            {"name": "design/architecture/invalid.txt", "is_dir": false}
        ],
        "design_references": []
    }
    policy.deny["Forbidden file extension in design/: design/architecture/invalid.txt"] with input as test_input
}

test_rule1_allow_valid_extension_in_subdir if {
    test_input := {
        "design_root_files": [
            {"name": "design/architecture/workspace.dsl", "is_dir": false}
        ],
        "design_references": []
    }
    count(policy.deny) == 0 with input as test_input
}

# Rule 2: design/ 直下には .md 以外のファイルを置かない
test_rule2_allow_md if {
    test_input := {
        "design_root_files": [
            {"name": "design/system-context.md", "is_dir": false}
        ],
        "design_references": []
    }
    count(policy.deny) == 0 with input as test_input
}

test_rule2_allow_dir if {
    test_input := {
        "design_root_files": [
            {"name": "design/architecture", "is_dir": true}
        ],
        "design_references": []
    }
    count(policy.deny) == 0 with input as test_input
}

test_rule2_deny_non_md if {
    test_input := {
        "design_root_files": [
            {"name": "design/wrong.txt", "is_dir": false}
        ],
        "design_references": []
    }
    policy.deny["Only .md files are allowed in design/ root, found file: design/wrong.txt"] with input as test_input
}

# Rule 3: design/ から reqs/ への参照を禁止
test_rule3_allow_docs_ref if {
    test_input := {
        "design_root_files": [],
        "design_references": [
            {"path": "docs/architecture/l1.md"}
        ]
    }
    count(policy.deny) == 0 with input as test_input
}

test_rule3_deny_reqs_ref if {
    test_input := {
        "design_root_files": [],
        "design_references": [
            {"path": "../reqs/context.md"}
        ]
    }
    policy.deny["Reference from design/ to reqs/ is forbidden: ../reqs/context.md"] with input as test_input
}
