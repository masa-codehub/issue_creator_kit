package spec.interim_path_test

import future.keywords.if
import data.spec.interim_path.deny

# 1. 廃止パス (docs/specs/) を含む Markdown リンクがある場合に deny がメッセージを返すことを検証（異常系）
test_obsolete_path_detected_docs_specs if {
	inp := {
		"path": "design/specs/sample.md",
		"content": "Please refer to [old doc](docs/specs/old-doc.md) for details.",
	}

	some msg
	deny[msg] with input as inp
	expected := sprintf("Obsolete path detected in %s: '%s'. Use 'design/specs/' or 'design/architecture/' instead.", [inp.path, "docs/specs/"])
	msg == expected
}

# 2. 廃止パス (docs/architecture/) を含む Markdown リンクがある場合に deny がメッセージを返すことを検証（異常系）
test_obsolete_path_detected_docs_architecture if {
	inp := {
		"path": "design/specs/sample.md",
		"content": "Refer to [arch doc](docs/architecture/old.md).",
	}

	some msg
	deny[msg] with input as inp
	expected := sprintf("Obsolete path detected in %s: '%s'. Use 'design/specs/' or 'design/architecture/' instead.", [inp.path, "docs/architecture/"])
	msg == expected
}

# 3. 廃止パスをコードブロック内に含む場合、deny がメッセージを返さないことを検証（正常系）
test_obsolete_path_in_codeblock_not_detected if {
	inp := {
		"path": "design/specs/sample.md",
		"content": "Example command: `grep docs/specs/ design/`",
	}

	count(deny) == 0 with input as inp
}

# 4. Merged Files (Traceability) 内での旧パス記述が deny されないことを検証（正常系）
test_merged_files_in_traceability_not_detected if {
	inp := {
		"path": "design/specs/sample.md",
		"content": `
## Traceability
- Merged Files:
  - docs/specs/api/old-api.md
`,
	}

	count(deny) == 0 with input as inp
}

# 5. adr-017 成果物が不適切なパス (例: docs/ 配下) に置かれている場合の警告検証（異常系）
test_adr017_artifact_wrong_location_detected if {
	inp := {
		"path": "docs/adr-017-sample.md",
		"content": "ADR-017 sample content.",
	}

	some msg
	deny[msg] with input as inp
	expected := sprintf("ADR-017 artifact %s must be placed under design/, policies/, or reqs/.", [inp.path])
	msg == expected
}

# 6. adr-017 成果物が許可されたパス (design/ 配下) に置かれている場合に警告されないことを検証（正常系）
test_adr017_artifact_correct_location_not_detected if {
	inp := {
		"path": "design/adr-017-sample.md",
		"content": "ADR-017 sample content.",
	}

	count(deny) == 0 with input as inp
}

# 7. adr-017 成果物が許可されたパス (policies/ 配下) に置かれている場合に警告されないことを検証（正常系）
test_adr017_artifact_policies_location_not_detected if {
	inp := {
		"path": "policies/specs/adr-017-sample.rego",
		"content": "package test",
	}

	count(deny) == 0 with input as inp
}
