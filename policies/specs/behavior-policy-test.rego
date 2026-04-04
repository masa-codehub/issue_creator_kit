package spec.behavior_test

import future.keywords.if
import data.spec.behavior.deny

# 1. 有効な service.name を持つセレクタを検証（正常系）
test_valid_service_name_detected if {
	inp := {
		"spec": {
			"specs": [
				{"selector": "span[service.name=\"backend-api\" name=\"process\"]"}
			]
		}
	}
	data_arch := {
		"softwareSystems": [
			{
				"containers": [
					{"name": "backend-api"}
				]
			}
		]
	}

	count(deny) == 0 with input as inp with data.model as data_arch
}

# 2. 不当な service.name を含む場合に deny がメッセージを返すことを検証（異常系）
test_invalid_service_name_detected if {
	inp := {
		"spec": {
			"specs": [
				{"selector": "span[service.name=\"unknown-service\"]"}
			]
		}
	}
	data_arch := {
		"softwareSystems": [
			{
				"containers": [
					{"name": "backend-api"}
				]
			}
		]
	}

	some msg
	deny[msg] with input as inp with data.model as data_arch
	msg == "Service 'unknown-service' defined in Tracetest selector is not found in structurizr.json"
}

# 3. スペースやシングルクォートを含むセレクタから正しく抽出できるか検証（正常系）
test_flexible_regex_extraction if {
	inp := {
		"spec": {
			"specs": [
				{"selector": "span[service.name = 'backend-api']"}
			]
		}
	}
	data_arch := {
		"softwareSystems": [
			{
				"containers": [
					{"name": "backend-api"}
				]
			}
		]
	}

	count(deny) == 0 with input as inp with data.model as data_arch
}

# 4. selector から service.name を抽出できない場合（deny はされない想定）
test_no_service_name_in_selector if {
	inp := {
		"spec": {
			"specs": [
				{"selector": "span[name=\"process\"]"}
			]
		}
	}
	data_arch := {
		"softwareSystems": []
	}

	count(deny) == 0 with input as inp with data.model as data_arch
}
